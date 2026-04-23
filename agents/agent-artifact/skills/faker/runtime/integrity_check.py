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
