"""
MD-DDL Faker — Referential Integrity Checker

Run against DatasetBuilder output (dict[str, list[dict]]) to verify that:
  - FK columns point to PKs that exist in the parent entity
  - not_null columns contain no None values
  - enum columns contain only declared values
  - PK columns are unique within each entity

Usage:
    from integrity_check import FKSpec, check_integrity, print_report

    errors = check_integrity(
        dataset,
        fk_specs=[
            FKSpec("Account", "currency_code", "Currency", "currency_code"),
            FKSpec("Transaction", "currency_code", "Currency", "currency_code"),
            FKSpec("Transaction", "debit_account_identifier", "Account", "account_identifier", nullable=True),
        ],
        not_null={"Party": ["legal_name"], "Transaction": ["amount"]},
        enum_values={"Party": {"party_status": PARTY_STATUS_VALUES}},
        unique_pk={"Party": "party_identifier", "Account": "account_identifier"},
    )
    print_report(errors)
    assert not errors, f"{len(errors)} integrity violation(s)"
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class FKSpec:
    """Declares one FK relationship to validate."""
    child_entity: str
    child_column: str
    parent_entity: str
    parent_column: str
    nullable: bool = False  # True = None is an allowed FK value


@dataclass
class IntegrityError:
    entity: str
    column: str
    row_index: int
    value: Any
    message: str

    def __str__(self) -> str:
        return (
            f"[{self.entity}] row {self.row_index}: "
            f"{self.column}={self.value!r} — {self.message}"
        )


def check_integrity(
    dataset: dict[str, list[dict]],
    fk_specs: list[FKSpec] | None = None,
    not_null: dict[str, list[str]] | None = None,
    enum_values: dict[str, dict[str, list[str]]] | None = None,
    unique_pk: dict[str, str] | None = None,
    unique_current_pk: dict[str, str] | None = None,
) -> list[IntegrityError]:
    """
    Validate a DatasetBuilder output dictionary.

    Parameters
    ----------
    dataset           : {entity_name: [row_dict, ...]} — output from DatasetBuilder.build()
    fk_specs          : FK relationships to enforce
    not_null          : {entity: [column, ...]} — columns that must not be None
    enum_values       : {entity: {column: [valid_value, ...]}} — enum membership checks
    unique_pk         : {entity: pk_column} — PK uniqueness across ALL rows (use for
                        immutable / append_only entities, e.g. Transaction, Currency)
    unique_current_pk : {entity: pk_column} — PK uniqueness among current rows only
                        (rows where is_current=True or valid_to is None).
                        Use for slowly_changing / bitemporal entities where SCD2 history
                        rows legitimately share the same entity identifier.

    Returns
    -------
    List of IntegrityError; empty list means the dataset is clean.
    """
    errors: list[IntegrityError] = []

    # Pre-build parent PK pools for FK resolution
    pk_pools: dict[tuple[str, str], set] = {}
    if fk_specs:
        for spec in fk_specs:
            key = (spec.parent_entity, spec.parent_column)
            if key not in pk_pools:
                pk_pools[key] = {
                    row[spec.parent_column]
                    for row in dataset.get(spec.parent_entity, [])
                    if row.get(spec.parent_column) is not None
                }

    # --- FK validation ---
    if fk_specs:
        for spec in fk_specs:
            pool = pk_pools.get((spec.parent_entity, spec.parent_column), set())
            for idx, row in enumerate(dataset.get(spec.child_entity, [])):
                value = row.get(spec.child_column)
                if value is None:
                    if not spec.nullable:
                        errors.append(IntegrityError(
                            entity=spec.child_entity,
                            column=spec.child_column,
                            row_index=idx,
                            value=value,
                            message=(
                                f"non-nullable FK → "
                                f"{spec.parent_entity}.{spec.parent_column} is None"
                            ),
                        ))
                elif value not in pool:
                    errors.append(IntegrityError(
                        entity=spec.child_entity,
                        column=spec.child_column,
                        row_index=idx,
                        value=value,
                        message=(
                            f"FK value not found in "
                            f"{spec.parent_entity}.{spec.parent_column} "
                            f"(pool size: {len(pool)})"
                        ),
                    ))

    # --- Not-null validation ---
    if not_null:
        for entity, columns in not_null.items():
            for idx, row in enumerate(dataset.get(entity, [])):
                for col in columns:
                    if row.get(col) is None:
                        errors.append(IntegrityError(
                            entity=entity,
                            column=col,
                            row_index=idx,
                            value=None,
                            message="not_null constraint violated",
                        ))

    # --- Enum membership validation ---
    if enum_values:
        for entity, col_map in enum_values.items():
            for idx, row in enumerate(dataset.get(entity, [])):
                for col, valid in col_map.items():
                    value = row.get(col)
                    if value is not None and value not in valid:
                        errors.append(IntegrityError(
                            entity=entity,
                            column=col,
                            row_index=idx,
                            value=value,
                            message=f"value not in declared enum set {valid}",
                        ))

    # --- PK uniqueness validation (all rows) ---
    if unique_pk:
        for entity, pk_col in unique_pk.items():
            seen: set = set()
            for idx, row in enumerate(dataset.get(entity, [])):
                pk = row.get(pk_col)
                if pk in seen:
                    errors.append(IntegrityError(
                        entity=entity,
                        column=pk_col,
                        row_index=idx,
                        value=pk,
                        message="duplicate PK — uniqueness constraint violated",
                    ))
                if pk is not None:
                    seen.add(pk)

    # --- PK uniqueness validation (current rows only — for SCD2/bitemporal entities) ---
    # A row is "current" if is_current is True, OR if valid_to is None and is_current
    # is absent (reference/append_only entities that don't carry temporal flags).
    if unique_current_pk:
        for entity, pk_col in unique_current_pk.items():
            seen = set()
            for idx, row in enumerate(dataset.get(entity, [])):
                is_current = row.get("is_current")
                valid_to = row.get("valid_to")
                # Include row if it is explicitly current, or has no temporal marker
                if is_current is False:
                    continue
                if is_current is None and valid_to is not None:
                    continue
                pk = row.get(pk_col)
                if pk in seen:
                    errors.append(IntegrityError(
                        entity=entity,
                        column=pk_col,
                        row_index=idx,
                        value=pk,
                        message=(
                            "duplicate PK among current rows — "
                            "uniqueness constraint violated"
                        ),
                    ))
                if pk is not None:
                    seen.add(pk)

    return errors


def print_report(errors: list[IntegrityError]) -> None:
    """Print a human-readable integrity report to stdout."""
    if not errors:
        print("OK — no integrity violations found.")
        return
    print(f"FAIL — {len(errors)} integrity violation(s):")
    for err in errors:
        print(f"  {err}")


# ---------------------------------------------------------------------------
# Temporal chain validation
# ---------------------------------------------------------------------------

@dataclass
class TemporalError:
    """One violation of within-entity temporal chain coherence."""
    entity: str
    entity_id: Any          # pk_column value for this entity instance
    row_index: int
    rule: str               # short code identifying which check failed
    message: str

    def __str__(self) -> str:
        return (
            f"[{self.entity}] entity_id={self.entity_id!r} row {self.row_index}: "
            f"({self.rule}) {self.message}"
        )


def check_temporal_chain(
    dataset: dict[str, list[dict]],
    temporal_entities: dict[str, str],
    warn_on_overlap: bool = True,
) -> list[TemporalError]:
    """
    Validate the bitemporal / valid_time chain for each entity instance.

    For each entity listed in temporal_entities, rows are grouped by their pk
    value and the following rules are checked per group:

      multiple_current        — at most one row may have is_current=True
      open_row_has_valid_to   — current row (is_current=True) must have valid_to=None
      closed_row_missing_valid_to — closed row (is_current=False) must have valid_to set
      valid_time_inversion    — valid_from must be <= valid_to for closed rows
      recorded_at_non_monotonic — recorded_at must be non-decreasing across rows
                                  sorted by valid_from (bitemporal entities only)
      superseded_at_missing   — closed rows on bitemporal entities must have
                                superseded_at set (detected automatically when any
                                row in the group has a superseded_at key)
      valid_time_overlap      — no two closed rows may have overlapping valid periods
                                (guarded by warn_on_overlap; O(n²) per group)

    Parameters
    ----------
    dataset           : {entity_name: [row_dict, ...]}
    temporal_entities : {entity_name: pk_column} — only listed entities are checked
    warn_on_overlap   : set False to skip the overlap scan for large datasets

    Returns
    -------
    List of TemporalError; empty list means all temporal chains are clean.
    """
    errors: list[TemporalError] = []

    for entity, pk_col in temporal_entities.items():
        rows_with_idx = list(enumerate(dataset.get(entity, [])))
        if not rows_with_idx:
            continue

        # Group rows by pk value
        groups: dict[Any, list[tuple[int, dict]]] = {}
        for idx, row in rows_with_idx:
            pk = row.get(pk_col)
            if pk is None:
                pk = "__null_pk__"
                errors.append(TemporalError(
                    entity=entity, entity_id=None, row_index=idx,
                    rule="null_pk",
                    message=f"pk column '{pk_col}' is None — cannot validate temporal chain",
                ))
            groups.setdefault(pk, []).append((idx, row))

        for entity_id, group in groups.items():
            if entity_id == "__null_pk__":
                continue

            # Detect bitemporal: any row has a recorded_at key
            is_bitemporal = any("recorded_at" in row for _, row in group)

            # 1. Count current rows
            current_rows = [(idx, row) for idx, row in group if row.get("is_current") is True]
            if len(current_rows) > 1:
                errors.append(TemporalError(
                    entity=entity, entity_id=entity_id,
                    row_index=current_rows[1][0],
                    rule="multiple_current",
                    message=f"found {len(current_rows)} rows with is_current=True; expected at most 1",
                ))

            for idx, row in group:
                is_current = row.get("is_current")
                valid_from = row.get("valid_from")
                valid_to = row.get("valid_to")

                # 2. Current row must have valid_to=None
                if is_current is True and valid_to is not None:
                    errors.append(TemporalError(
                        entity=entity, entity_id=entity_id, row_index=idx,
                        rule="open_row_has_valid_to",
                        message=f"is_current=True but valid_to={valid_to!r} (should be None)",
                    ))

                # 3. Closed row must have valid_to set
                if is_current is False and valid_to is None:
                    errors.append(TemporalError(
                        entity=entity, entity_id=entity_id, row_index=idx,
                        rule="closed_row_missing_valid_to",
                        message="is_current=False but valid_to is None",
                    ))

                # 4. valid_time inversion for closed rows
                if is_current is False and valid_from is not None and valid_to is not None:
                    try:
                        if valid_from > valid_to:
                            errors.append(TemporalError(
                                entity=entity, entity_id=entity_id, row_index=idx,
                                rule="valid_time_inversion",
                                message=f"valid_from={valid_from} > valid_to={valid_to}",
                            ))
                    except TypeError:
                        pass  # mixed tz-aware/naive; skip comparison

                # 5. superseded_at missing on bitemporal closed rows
                if is_bitemporal and is_current is False:
                    if row.get("superseded_at") is None:
                        errors.append(TemporalError(
                            entity=entity, entity_id=entity_id, row_index=idx,
                            rule="superseded_at_missing",
                            message="bitemporal closed row has superseded_at=None",
                        ))

            # 6. recorded_at monotonicity (bitemporal only)
            if is_bitemporal:
                rows_with_vf = [
                    (idx, row) for idx, row in group
                    if row.get("valid_from") is not None and row.get("recorded_at") is not None
                ]
                try:
                    sorted_rows = sorted(rows_with_vf, key=lambda t: t[1]["valid_from"])
                    prev_recorded_at = None
                    for idx, row in sorted_rows:
                        recorded_at = row["recorded_at"]
                        if prev_recorded_at is not None and recorded_at < prev_recorded_at:
                            errors.append(TemporalError(
                                entity=entity, entity_id=entity_id, row_index=idx,
                                rule="recorded_at_non_monotonic",
                                message=(
                                    f"recorded_at={recorded_at} is earlier than "
                                    f"recorded_at={prev_recorded_at} of a prior valid period"
                                ),
                            ))
                        # Only advance if strictly greater (equal is fine — same instant)
                        if prev_recorded_at is None or recorded_at > prev_recorded_at:
                            prev_recorded_at = recorded_at
                except TypeError:
                    pass  # mixed types; skip

            # 7. Valid-time overlap scan (O(n²); guarded)
            if warn_on_overlap:
                closed = [
                    (idx, row) for idx, row in group
                    if row.get("is_current") is False
                    and row.get("valid_from") is not None
                    and row.get("valid_to") is not None
                ]
                for i in range(len(closed)):
                    for j in range(i + 1, len(closed)):
                        idx_a, row_a = closed[i]
                        idx_b, row_b = closed[j]
                        a_from, a_to = row_a["valid_from"], row_a["valid_to"]
                        b_from, b_to = row_b["valid_from"], row_b["valid_to"]
                        try:
                            # Touching (a_to == b_from) is allowed; strict overlap only
                            if a_from < b_to and b_from < a_to:
                                errors.append(TemporalError(
                                    entity=entity, entity_id=entity_id, row_index=idx_b,
                                    rule="valid_time_overlap",
                                    message=(
                                        f"valid periods overlap: "
                                        f"row {idx_a} [{a_from}, {a_to}] ∩ "
                                        f"row {idx_b} [{b_from}, {b_to}]"
                                    ),
                                ))
                        except TypeError:
                            pass

    return errors


def print_temporal_report(errors: list[TemporalError]) -> None:
    """Print a human-readable temporal chain report to stdout."""
    if not errors:
        print("OK — no temporal chain violations found.")
        return
    print(f"FAIL — {len(errors)} temporal chain violation(s):")
    for err in errors:
        print(f"  {err}")


# ---------------------------------------------------------------------------
# Self-test: run directly to verify the checker catches a deliberate violation
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from datetime import datetime, timezone

    _dataset: dict[str, list[dict]] = {
        "Currency": [
            {"currency_code": "AUD", "currency_name": "Australian Dollar", "minor_unit": 2},
        ],
        "Account": [
            # Good row — FK resolves
            {
                "account_identifier": "acc-001",
                "currency_code": "AUD",
                "account_status": "Active",
                "valid_from": datetime.now(tz=timezone.utc),
                "valid_to": None,
                "is_current": True,
            },
            # Bad row — FK does not resolve
            {
                "account_identifier": "acc-002",
                "currency_code": "JPY",  # not in Currency pool
                "account_status": "Active",
                "valid_from": datetime.now(tz=timezone.utc),
                "valid_to": None,
                "is_current": True,
            },
        ],
        "Transaction": [
            # Bad row — not_null on amount violated
            {
                "transaction_identifier": "txn-001",
                "currency_code": "AUD",
                "amount": None,
                "debit_account_identifier": "acc-001",
            },
        ],
    }

    _errors = check_integrity(
        _dataset,
        fk_specs=[
            FKSpec("Account", "currency_code", "Currency", "currency_code"),
            FKSpec("Transaction", "currency_code", "Currency", "currency_code"),
            FKSpec(
                "Transaction", "debit_account_identifier",
                "Account", "account_identifier",
                nullable=True,
            ),
        ],
        not_null={"Transaction": ["amount"]},
        unique_pk={"Account": "account_identifier"},
    )

    assert len(_errors) == 2, f"Expected 2 errors, got {len(_errors)}: {_errors}"
    print("Self-test passed — detected expected violations:")
    print_report(_errors)
