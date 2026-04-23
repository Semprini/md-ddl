"""
Eventual Consistency Demonstration — Financial Crime / canonical scope

Shows how Party entity updates converge (or fail to converge) across three
source feeds with different propagation lags, and validates the canonical
product's declared SLA of < 1 hour.

Source feeds modelled (from examples/Financial Crime/sources/):
  1. salesforce-crm   — real-time-cdc,  lag =  5 min  (party identity fields)
  2. sap-fraud-mgmt   — batch-intraday, lag = 30 min  (risk_rating, sanctions_screen_status)
  3. temenos-payment  — batch-intraday, lag = 60 min  (slowest contributing system)

Canonical SLA: freshness < 1 hour
  (from examples/Financial Crime/products/canonical.md)

Consistency posture: eventual
  (sources have heterogeneous change_models; synchronous propagation not achievable)

Null strategy: nullable-staging
  (partial rows admitted to staging; converged view used by consumers)

Usage:
    cd examples/Financial\ Crime
    python consistency_example.py

    # Or with runtime on path explicitly:
    PYTHONPATH=../../agents/agent-artifact/skills/faker/runtime python consistency_example.py
"""

from __future__ import annotations
import sys
import os

# ---------------------------------------------------------------------------
# Path setup — inject faker runtime so integrity_check and consistency_scenario
# can be imported regardless of working directory
# ---------------------------------------------------------------------------
_runtime_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..",
                 "agents", "agent-artifact", "skills", "faker", "runtime")
)
if _runtime_path not in sys.path:
    sys.path.insert(0, _runtime_path)

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
try:
    from factories import (
        DatasetBuilder,
        FK_SPECS_FINANCIAL_CRIME,
        NOT_NULL_FINANCIAL_CRIME,
        ENUM_VALUES_FINANCIAL_CRIME,
        UNIQUE_PK_FINANCIAL_CRIME,
        UNIQUE_CURRENT_PK_FINANCIAL_CRIME,
    )
except ImportError as e:
    print(f"[ERROR] Could not import factories.py — run from the "
          f"'examples/Financial Crime/' directory: {e}")
    sys.exit(1)

try:
    from integrity_check import (
        check_integrity, print_report,
        check_temporal_chain, print_temporal_report,
    )
    from consistency_scenario import (
        SourceFeed, generate_scenario,
        check_convergence, print_convergence_report,
    )
except ImportError as e:
    print(f"[ERROR] Could not import runtime modules from {_runtime_path}: {e}")
    sys.exit(1)

from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Source feeds — modelled on the Financial Crime domain's declared source systems
FEEDS = [
    SourceFeed(name="salesforce-crm",  lag_minutes=5,  change_model="real-time-cdc"),
    SourceFeed(name="sap-fraud-mgmt",  lag_minutes=30, change_model="batch-intraday"),
    SourceFeed(name="temenos-payment", lag_minutes=60, change_model="batch-intraday"),
]

# Entities with valid_time or bitemporal tracking (candidate for convergence analysis)
TEMPORAL_ENTITIES = {
    "Party":   "party_identifier",
    "Account": "account_identifier",
}

# Canonical product SLA (from products/canonical.md: freshness: "< 1 hour")
SLA_MINUTES = 60

# ---------------------------------------------------------------------------
# Section 1 — Build dataset
# ---------------------------------------------------------------------------
print("=" * 60)
print("Financial Crime — Eventual Consistency Demonstration")
print("=" * 60)

print("\n[1] Building synthetic dataset (20 parties, history=True)…")
dataset = DatasetBuilder(pii_mode="safe").build(
    n_parties=20,
    accounts_per_party=2,
    txns_per_account=3,
    with_history=True,
)
total_rows = sum(len(v) for v in dataset.values())
print(f"    Built: {total_rows} total rows across {len(dataset)} entities")
for entity, rows in dataset.items():
    print(f"      {entity}: {len(rows)} rows")

# ---------------------------------------------------------------------------
# Section 2 — Baseline integrity check
# ---------------------------------------------------------------------------
print("\n[2] Baseline integrity check…")
integrity_errors = check_integrity(
    dataset,
    fk_specs=FK_SPECS_FINANCIAL_CRIME,
    not_null=NOT_NULL_FINANCIAL_CRIME,
    enum_values=ENUM_VALUES_FINANCIAL_CRIME,
    unique_pk=UNIQUE_PK_FINANCIAL_CRIME,
    unique_current_pk=UNIQUE_CURRENT_PK_FINANCIAL_CRIME,
)
print_report(integrity_errors)
if integrity_errors:
    print("[WARN] Integrity violations present — convergence analysis may be misleading")

# ---------------------------------------------------------------------------
# Section 3 — Temporal chain validation
# ---------------------------------------------------------------------------
print("\n[3] Temporal chain validation…")
temporal_errors = check_temporal_chain(dataset, TEMPORAL_ENTITIES)
print_temporal_report(temporal_errors)

# ---------------------------------------------------------------------------
# Section 4 — Generate eventual consistency scenario
# ---------------------------------------------------------------------------
print("\n[4] Generating eventual consistency scenario…")
print(f"    Feeds:  " +
      " | ".join(f"{f.name} (lag={f.lag_minutes}m, {f.change_model})" for f in FEEDS))

as_of = datetime.now(tz=timezone.utc)
scenario = generate_scenario(
    dataset=dataset,
    feeds=FEEDS,
    as_of=as_of,
    temporal_entities=TEMPORAL_ENTITIES,
)

# ---------------------------------------------------------------------------
# Section 5 — Convergence report
# ---------------------------------------------------------------------------
print("\n[5] Convergence analysis…")
print(f"    Observation time: {as_of.strftime('%Y-%m-%d %H:%M:%S UTC')}")

for entity, pk_col in TEMPORAL_ENTITIES.items():
    deltas = scenario.convergence_delta_minutes.get(entity, {})
    divergent_ids = scenario.divergent.get(entity, [])
    converged = [pk for pk, d in deltas.items() if d == 0.0]
    in_flight = [pk for pk, d in deltas.items() if d > 0.0]

    print(f"\n    {entity} ({len(deltas)} current instances):")
    print(f"      Fully converged : {len(converged)}")
    print(f"      In-flight       : {len(in_flight)}")

    if in_flight:
        print(f"      In-flight sample (showing up to 5):")
        for pk in in_flight[:5]:
            mins = deltas[pk]
            pk_short = str(pk)[:8] + "…"
            # Show which feeds still need to receive this row
            late_feeds = []
            for feed in FEEDS:
                feed_rows = scenario.source_views[feed.name].get(entity, [])
                feed_pks = {r.get(pk_col) for r in feed_rows if r.get("is_current") is True}
                if pk not in feed_pks:
                    late_feeds.append(f"{feed.name}({feed.lag_minutes}m)")
            print(f"        {pk_short}  converges in {mins:.1f} min "
                  f"[pending: {', '.join(late_feeds) or 'none'}]")

# ---------------------------------------------------------------------------
# Section 6 — SLA check
# ---------------------------------------------------------------------------
print(f"\n[6] SLA validation (freshness < {SLA_MINUTES} min)…")
violations = check_convergence(scenario, sla_minutes=SLA_MINUTES)

if not violations:
    print(f"    PASS — all entity instances converge within the "
          f"{SLA_MINUTES}-minute SLA.")
else:
    print(f"    FAIL — {len(violations)} instance(s) violate the "
          f"{SLA_MINUTES}-minute SLA:")
    for v in violations[:5]:
        pk_short = str(v.entity_id)[:8] + "…"
        print(f"      [{v.entity}] {pk_short}: {v.message}")
    if len(violations) > 5:
        print(f"      … and {len(violations) - 5} more")

# ---------------------------------------------------------------------------
# Section 7 — Null handling illustration
# ---------------------------------------------------------------------------
print("\n[7] Null handling under eventual consistency…")
print("""
    Scenario: salesforce-crm (lag=5m) has delivered party_status.
              sap-fraud-mgmt (lag=30m) has NOT yet delivered risk_rating.

    In-flight canonical row (nullable-staging pattern):
      party_identifier : "aaa-bbb-ccc…"    ← arrived from salesforce-crm
      party_status     : "Active"            ← arrived from salesforce-crm
      risk_rating      : NULL                ← not yet received from sap-fraud-mgmt
      sanctions_screen_status : NULL         ← not yet received from sap-fraud-mgmt

    Storage concern   : Parquet cannot distinguish this NULL from a genuinely
                        absent risk_rating. Downstream readers see identical bytes.
    Transport concern : JSON omits absent keys; Avro encodes both as null union.
                        Only Protobuf hasField() can distinguish "not set" vs null.
    DDL concern       : A hard NOT NULL on risk_rating would block this insert.
                        With nullable-staging pattern, the base table allows NULL;
                        the converged view filters to rows where all fields are set.
""")

print("=" * 60)
print("Demonstration complete.")
print("=" * 60)
