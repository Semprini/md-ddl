"""
MD-DDL Faker — Eventual Consistency Scenario Simulator

Simulates what each source feed has received at a given observation instant,
given per-feed propagation lags. Works on any DatasetBuilder output dict.

Known simplification: the Financial Crime domain's source systems each contribute
*different attributes* to the same canonical entity (Salesforce → party_status;
SAP → risk_rating). The generated factories capture the full entity state per SCD2
row rather than per-attribute deltas. This module therefore models "the whole
current row arrived at recorded_at + lag" — a useful approximation for SLA
validation and convergence demonstration, not a field-level attribution model.

Zero external dependencies — Python stdlib only (dataclasses, datetime, typing).

Usage:
    from consistency_scenario import SourceFeed, generate_scenario, check_convergence

    feeds = [
        SourceFeed("salesforce-crm", lag_minutes=5,  change_model="real-time-cdc"),
        SourceFeed("sap-fraud-mgmt", lag_minutes=30, change_model="batch-intraday"),
        SourceFeed("slow-consumer",  lag_minutes=60, change_model="batch-intraday"),
    ]
    scenario = generate_scenario(dataset, feeds, temporal_entities={"Party": "party_identifier"})
    violations = check_convergence(scenario, sla_minutes=60)
    print_convergence_report(scenario, violations, {"Party": "party_identifier"}, sla_minutes=60)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SourceFeed:
    """Represents one source system with its propagation characteristics."""
    name: str
    lag_minutes: int        # propagation delay: how many minutes after recorded_at
                            # before this feed considers the row received
    change_model: str = ""  # informational: "real-time-cdc", "event-driven", "batch-intraday"


@dataclass
class ConvergenceViolation:
    """One entity instance that will not converge within the declared SLA."""
    entity: str
    entity_id: Any
    max_lag_minutes: int    # lag of the slowest feed that has not received the current row
    sla_minutes: int
    over_by_minutes: float  # minutes beyond the SLA before convergence
    message: str


@dataclass
class ConsistencyScenario:
    """
    Full output of generate_scenario().

    canonical          : complete dataset as generated (ground truth)
    source_views       : {feed_name: {entity_name: [rows received by this feed by as_of]}}
    divergent          : {entity_name: [pk_values of instances not yet seen by all feeds]}
    convergence_delta_minutes : {entity_name: {pk_value: float minutes until all feeds converge}}
                                 0.0 means already converged
    as_of              : the observation instant used
    feeds              : the feed list used
    """
    canonical: dict[str, list[dict]]
    source_views: dict[str, dict[str, list[dict]]]
    divergent: dict[str, list[Any]]
    convergence_delta_minutes: dict[str, dict[Any, float]]
    as_of: datetime
    feeds: list[SourceFeed]


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def _coerce_utc(dt: datetime) -> datetime:
    """Ensure datetime is timezone-aware (UTC) for safe comparison."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def apply_source_lag(
    rows: list[dict],
    lag_minutes: int,
    as_of: datetime,
    recorded_at_col: str = "recorded_at",
) -> list[dict]:
    """
    Filter rows to those a source feed would have received by as_of, given lag.

    A row is considered received when:
        recorded_at + timedelta(minutes=lag_minutes) <= as_of

    Rows without a recorded_at column (reference / append_only entities that
    carry no transaction time) are always included — they are treated as
    statically propagated.

    Parameters
    ----------
    rows            : list of row dicts for one entity
    lag_minutes     : propagation delay in minutes
    as_of           : observation instant
    recorded_at_col : column carrying transaction time (default: "recorded_at")

    Returns
    -------
    Subset of rows the feed has received by as_of.
    """
    as_of = _coerce_utc(as_of)
    result = []
    for row in rows:
        recorded_at = row.get(recorded_at_col)
        if recorded_at is None:
            # No transaction time — treat as always available (reference / static)
            result.append(row)
        else:
            try:
                arrival = _coerce_utc(recorded_at) + timedelta(minutes=lag_minutes)
                if arrival <= as_of:
                    result.append(row)
            except (TypeError, AttributeError):
                result.append(row)  # unparseable timestamp — include conservatively
    return result


def generate_scenario(
    dataset: dict[str, list[dict]],
    feeds: list[SourceFeed],
    as_of: datetime | None = None,
    temporal_entities: dict[str, str] | None = None,
    recorded_at_col: str = "recorded_at",
) -> ConsistencyScenario:
    """
    Simulate what each source feed has received at as_of, given propagation lags.

    Parameters
    ----------
    dataset           : canonical dataset from DatasetBuilder.build()
    feeds             : list of SourceFeed objects (each with lag_minutes)
    as_of             : observation instant; defaults to datetime.now(UTC)
    temporal_entities : {entity_name: pk_column} — entities to analyse for divergence.
                        If None, all entities where any row has recorded_at are included.
    recorded_at_col   : column holding transaction time (default: "recorded_at")

    Returns
    -------
    ConsistencyScenario
    """
    if as_of is None:
        as_of = datetime.now(tz=timezone.utc)
    as_of = _coerce_utc(as_of)

    # Auto-detect temporal entities if not specified
    if temporal_entities is None:
        temporal_entities = {}
        for entity, rows in dataset.items():
            if any(recorded_at_col in row for row in rows):
                # Heuristic: look for a uuid-like string PK column
                for row in rows:
                    for col, val in row.items():
                        if "identifier" in col and isinstance(val, str):
                            temporal_entities[entity] = col
                            break
                    if entity in temporal_entities:
                        break

    # Build source views
    source_views: dict[str, dict[str, list[dict]]] = {}
    for feed in feeds:
        source_views[feed.name] = {
            entity: apply_source_lag(rows, feed.lag_minutes, as_of, recorded_at_col)
            for entity, rows in dataset.items()
        }

    # Analyse divergence and convergence deltas
    divergent: dict[str, list[Any]] = {}
    convergence_delta_minutes: dict[str, dict[Any, float]] = {}

    for entity, pk_col in temporal_entities.items():
        canonical_rows = dataset.get(entity, [])
        if not canonical_rows:
            continue

        # Group canonical rows by pk, find the current version per entity instance
        canonical_current: dict[Any, dict] = {}
        for row in canonical_rows:
            pk = row.get(pk_col)
            if pk is None:
                continue
            is_current = row.get("is_current")
            # Accept is_current=True, or rows without is_current (reference/append_only)
            if is_current is True or is_current is None:
                existing = canonical_current.get(pk)
                if existing is None:
                    canonical_current[pk] = row
                else:
                    # Keep the row with the later recorded_at
                    try:
                        if (
                            row.get(recorded_at_col) is not None
                            and _coerce_utc(row[recorded_at_col])
                            > _coerce_utc(existing.get(recorded_at_col, datetime.min.replace(tzinfo=timezone.utc)))
                        ):
                            canonical_current[pk] = row
                    except (TypeError, AttributeError):
                        pass

        divergent[entity] = []
        convergence_delta_minutes[entity] = {}

        for pk, canonical_row in canonical_current.items():
            canonical_recorded_at = canonical_row.get(recorded_at_col)
            if canonical_recorded_at is None:
                convergence_delta_minutes[entity][pk] = 0.0
                continue
            canonical_recorded_at = _coerce_utc(canonical_recorded_at)

            # Find the slowest feed that has not yet received this row
            max_remaining: float = 0.0
            entity_divergent = False

            for feed in feeds:
                feed_rows = source_views[feed.name].get(entity, [])
                # Find this feed's current version of this entity instance
                feed_current: dict | None = None
                for row in feed_rows:
                    if row.get(pk_col) != pk:
                        continue
                    is_current = row.get("is_current")
                    if is_current is True or is_current is None:
                        existing = feed_current
                        if existing is None:
                            feed_current = row
                        else:
                            try:
                                if (
                                    row.get(recorded_at_col) is not None
                                    and _coerce_utc(row[recorded_at_col])
                                    > _coerce_utc(existing.get(recorded_at_col, datetime.min.replace(tzinfo=timezone.utc)))
                                ):
                                    feed_current = row
                            except (TypeError, AttributeError):
                                pass

                # Is this feed behind?
                if feed_current is None:
                    # Feed has not received any version of this entity yet
                    entity_divergent = True
                    arrival = canonical_recorded_at + timedelta(minutes=feed.lag_minutes)
                    remaining = max(0.0, (arrival - as_of).total_seconds() / 60)
                    max_remaining = max(max_remaining, remaining)
                else:
                    feed_recorded_at = feed_current.get(recorded_at_col)
                    if feed_recorded_at is not None:
                        try:
                            feed_recorded_at = _coerce_utc(feed_recorded_at)
                            if feed_recorded_at < canonical_recorded_at:
                                entity_divergent = True
                                arrival = canonical_recorded_at + timedelta(minutes=feed.lag_minutes)
                                remaining = max(0.0, (arrival - as_of).total_seconds() / 60)
                                max_remaining = max(max_remaining, remaining)
                        except (TypeError, AttributeError):
                            pass

            convergence_delta_minutes[entity][pk] = max_remaining
            if entity_divergent:
                divergent[entity].append(pk)

    return ConsistencyScenario(
        canonical=dataset,
        source_views=source_views,
        divergent=divergent,
        convergence_delta_minutes=convergence_delta_minutes,
        as_of=as_of,
        feeds=feeds,
    )


def check_convergence(
    scenario: ConsistencyScenario,
    sla_minutes: int,
) -> list[ConvergenceViolation]:
    """
    Identify entity instances that will not converge within sla_minutes.

    Parameters
    ----------
    scenario    : output of generate_scenario()
    sla_minutes : the SLA window in minutes (e.g. 60 for "< 1 hour")

    Returns
    -------
    List of ConvergenceViolation; empty means all entities converge within the SLA.
    """
    violations: list[ConvergenceViolation] = []
    for entity, deltas in scenario.convergence_delta_minutes.items():
        for pk, delta_minutes in deltas.items():
            if delta_minutes > sla_minutes:
                max_lag = max(f.lag_minutes for f in scenario.feeds)
                violations.append(ConvergenceViolation(
                    entity=entity,
                    entity_id=pk,
                    max_lag_minutes=max_lag,
                    sla_minutes=sla_minutes,
                    over_by_minutes=delta_minutes - sla_minutes,
                    message=(
                        f"converges in {delta_minutes:.1f} min; "
                        f"SLA is {sla_minutes} min; "
                        f"over by {delta_minutes - sla_minutes:.1f} min"
                    ),
                ))
    return violations


def print_convergence_report(
    scenario: ConsistencyScenario,
    violations: list[ConvergenceViolation],
    temporal_entities: dict[str, str],
    sla_minutes: int,
) -> None:
    """Print a human-readable convergence summary to stdout."""
    print(f"\n=== Convergence Report (as_of: {scenario.as_of.isoformat()}) ===")
    print(f"SLA: {sla_minutes} min | Feeds: " +
          ", ".join(f"{f.name}({f.lag_minutes}m)" for f in scenario.feeds))

    for entity in temporal_entities:
        deltas = scenario.convergence_delta_minutes.get(entity, {})
        total = len(deltas)
        in_flight = sum(1 for v in deltas.values() if v > 0)
        converged = total - in_flight
        sla_violated = sum(1 for v in deltas.values() if v > sla_minutes)
        print(f"\n  {entity}: {total} instances | "
              f"converged={converged} | in-flight={in_flight} | "
              f"SLA violations={sla_violated}")
        if in_flight:
            samples = [(pk, v) for pk, v in deltas.items() if v > 0][:3]
            for pk, mins in samples:
                pk_short = str(pk)[:8] + "…" if len(str(pk)) > 8 else str(pk)
                print(f"    {pk_short}  converges in {mins:.1f} min")

    if violations:
        print(f"\n  FAIL — {len(violations)} SLA violation(s):")
        for v in violations[:5]:
            pk_short = str(v.entity_id)[:8] + "…" if len(str(v.entity_id)) > 8 else str(v.entity_id)
            print(f"    [{v.entity}] {pk_short}: {v.message}")
    else:
        print(f"\n  PASS — all instances converge within the {sla_minutes}-minute SLA")


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from datetime import datetime, timezone, timedelta

    # Minimal inline dataset: two Party rows (prior + current, bitemporal)
    now = datetime.now(tz=timezone.utc)
    _dataset: dict[str, list[dict]] = {
        "Party": [
            # Entity A — current row recorded 2 minutes ago
            {
                "party_identifier": "aaa",
                "is_current": True,
                "valid_from": now - timedelta(hours=2),
                "valid_to": None,
                "recorded_at": now - timedelta(minutes=2),
                "superseded_at": None,
            },
            # Entity A — prior row
            {
                "party_identifier": "aaa",
                "is_current": False,
                "valid_from": now - timedelta(hours=10),
                "valid_to": now - timedelta(hours=2),
                "recorded_at": now - timedelta(hours=10),
                "superseded_at": now - timedelta(hours=2),
            },
            # Entity B — current row recorded 45 minutes ago
            {
                "party_identifier": "bbb",
                "is_current": True,
                "valid_from": now - timedelta(hours=1),
                "valid_to": None,
                "recorded_at": now - timedelta(minutes=45),
                "superseded_at": None,
            },
        ],
        "Currency": [
            {"currency_code": "AUD", "currency_name": "Australian Dollar", "minor_unit": 2},
        ],
    }

    _feeds = [
        SourceFeed("fast-feed",  lag_minutes=5,  change_model="real-time-cdc"),
        SourceFeed("slow-feed",  lag_minutes=60, change_model="batch-intraday"),
    ]

    _scenario = generate_scenario(
        _dataset, _feeds,
        as_of=now,
        temporal_entities={"Party": "party_identifier"},
    )

    _violations = check_convergence(_scenario, sla_minutes=60)
    print_convergence_report(_scenario, _violations, {"Party": "party_identifier"}, sla_minutes=60)

    # Entity A: recorded 2 min ago → fast(5m) not yet received, slow(60m) not yet received
    assert "aaa" in _scenario.divergent.get("Party", []), "entity aaa should be divergent"
    # Entity B: recorded 45 min ago → fast(5m) received (45+5=50≤now), slow(60m) not yet (45+60>now)
    assert "bbb" in _scenario.divergent.get("Party", []), "entity bbb should be divergent"

    # With 60-min SLA: entity A needs up to 60 min from recorded_at=2min_ago → 58 min remaining > 0
    # Entity B needs up to 60 min from recorded_at=45min_ago → 15 min remaining → within SLA
    sla_violations = check_convergence(_scenario, sla_minutes=60)
    # entity A converges in 58 min → within 60-min SLA (58 ≤ 60) — PASS
    # entity B converges in 15 min → within 60-min SLA — PASS
    assert len(sla_violations) == 0, f"Expected 0 SLA violations at 60 min, got {sla_violations}"

    # With 10-min SLA: entity A (58 min) and entity B (15 min) both violate
    tight_violations = check_convergence(_scenario, sla_minutes=10)
    assert len(tight_violations) == 2, f"Expected 2 SLA violations at 10 min, got {tight_violations}"

    print("\nSelf-test passed.")
