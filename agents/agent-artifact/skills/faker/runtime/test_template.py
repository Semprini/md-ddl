"""
MD-DDL Faker — Pytest Test Template

Copy this file alongside your generated factories module. Update the three
sections marked UPDATE to match your domain and generated module, then run:

    pip install faker pytest
    pytest test_factories.py -v

This template validates:
  - All expected entities are present in the dataset
  - Row counts meet cardinality expectations
  - Referential integrity (FK, not_null, enum, PK uniqueness)
  - PII-safe mode produces no realistic-looking personal data
  - Seeded output is deterministic (same seed → same first row)
  - Temporal columns are internally consistent

Replace every comment block beginning with  # UPDATE  with your values.
"""

from __future__ import annotations
import sys
import os
import pytest

# ---------------------------------------------------------------------------
# UPDATE 1 — import your generated factories module
# ---------------------------------------------------------------------------
# Adjust the path if your factories file is not in the same directory as
# this test file.  Example:
#
#   sys.path.insert(0, os.path.dirname(__file__))
#   from financial_crime_factories import DatasetBuilder
#
# UPDATE:
# sys.path.insert(0, os.path.dirname(__file__))
# from your_generated_factories import DatasetBuilder
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# UPDATE 2 — integrity spec for your domain
# ---------------------------------------------------------------------------
# Copy the FK/not-null/enum/PK specs that match your entity model.
# These mirror the relationship declarations in your entity YAML files.
#
# from integrity_check import FKSpec
#
# FK_SPECS = [
#     FKSpec("Account",     "currency_code",             "Currency", "currency_code"),
#     FKSpec("Transaction", "currency_code",             "Currency", "currency_code"),
#     FKSpec("Transaction", "debit_account_identifier",  "Account",  "account_identifier", nullable=True),
#     FKSpec("Transaction", "credit_account_identifier", "Account",  "account_identifier", nullable=True),
# ]
#
# NOT_NULL = {
#     "Party":       ["party_identifier", "legal_name"],
#     "Account":     ["account_identifier", "currency_code"],
#     "Transaction": ["transaction_identifier", "amount", "currency_code"],
# }
#
# ENUM_VALUES = {
#     "Party":       {"party_status": ["Active", "Under Review", "Restricted", "Inactive", "Closed"]},
#     "Account":     {"account_status": ["Pending", "Active", "Dormant", "Frozen", "Suspended", "Closed"]},
#     "Transaction": {"transaction_status": ["Pending", "Authorised", "Cleared", "Settled",
#                                            "Failed", "Reversed", "Cancelled", "Under Review"]},
# }
#
# unique_pk applies to ALL rows — use for reference and append_only entities
# (Currency, Transaction) where every row has a distinct surrogate key.
# UNIQUE_PK = {
#     "Currency":    "currency_code",
#     "Transaction": "transaction_identifier",
# }
#
# unique_current_pk applies to CURRENT rows only (is_current=True or valid_to is None).
# Use for slowly_changing / bitemporal entities (Party, Account) where SCD2 history
# rows legitimately share the same entity identifier across prior/current pairs.
# UNIQUE_CURRENT_PK = {
#     "Party":   "party_identifier",
#     "Account": "account_identifier",
# }
#
# UPDATE:
FK_SPECS: list = []
NOT_NULL: dict = {}
ENUM_VALUES: dict = {}
UNIQUE_PK: dict = {}
UNIQUE_CURRENT_PK: dict = {}
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# UPDATE 3 — expected entity names and minimum row counts after build()
# ---------------------------------------------------------------------------
# EXPECTED_ENTITIES lists entity names that must appear as keys in the dataset.
# MIN_ROWS is a lower bound on len(dataset[entity]) after build(n_roots=20, ...).
#
# UPDATE:
EXPECTED_ENTITIES: list[str] = []   # e.g. ["Currency", "Party", "Account", "Transaction"]
MIN_ROWS: dict[str, int] = {}       # e.g. {"Party": 20, "Transaction": 40}
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def dataset() -> dict[str, list[dict]]:
    """Build a medium-sized dataset with history rows for thorough coverage."""
    # UPDATE: replace with your DatasetBuilder import above
    pytest.skip("DatasetBuilder not imported — update UPDATE 1 above")


@pytest.fixture(scope="module")
def dataset_no_history() -> dict[str, list[dict]]:
    """Build a dataset without history rows (current state only)."""
    pytest.skip("DatasetBuilder not imported — update UPDATE 1 above")


# ---------------------------------------------------------------------------
# Structural tests
# ---------------------------------------------------------------------------

def test_expected_entities_present(dataset: dict) -> None:
    missing = [e for e in EXPECTED_ENTITIES if e not in dataset]
    assert not missing, f"Missing entities in dataset: {missing}"


def test_minimum_row_counts(dataset: dict) -> None:
    for entity, minimum in MIN_ROWS.items():
        actual = len(dataset.get(entity, []))
        assert actual >= minimum, (
            f"{entity}: expected >= {minimum} rows, got {actual}"
        )


def test_no_empty_entities(dataset: dict) -> None:
    empty = [name for name, rows in dataset.items() if not rows]
    assert not empty, f"Entities with zero rows: {empty}"


# ---------------------------------------------------------------------------
# Referential integrity
# ---------------------------------------------------------------------------

def test_referential_integrity(dataset: dict) -> None:
    """All FK columns resolve; not_null and enum constraints hold."""
    try:
        from integrity_check import check_integrity, print_report
    except ImportError:
        pytest.skip("integrity_check.py not on sys.path")

    errors = check_integrity(
        dataset,
        fk_specs=FK_SPECS or None,
        not_null=NOT_NULL or None,
        enum_values=ENUM_VALUES or None,
        unique_pk=UNIQUE_PK or None,
        unique_current_pk=UNIQUE_CURRENT_PK or None,
    )
    if errors:
        print_report(errors)
    assert not errors, f"{len(errors)} integrity violation(s) — see output above"


def test_pk_uniqueness(dataset: dict) -> None:
    """PK values are unique: all rows for append_only entities, current rows for SCD2."""
    try:
        from integrity_check import check_integrity
    except ImportError:
        pytest.skip("integrity_check.py not on sys.path")

    errors = check_integrity(
        dataset,
        unique_pk=UNIQUE_PK or None,
        unique_current_pk=UNIQUE_CURRENT_PK or None,
    )
    assert not errors, f"Duplicate PK(s): {errors}"


# ---------------------------------------------------------------------------
# PII-safe mode
# ---------------------------------------------------------------------------

def test_safe_mode_no_real_emails(dataset: dict) -> None:
    """safe mode must not produce real-looking email addresses."""
    for entity, rows in dataset.items():
        for row in rows:
            for col, value in row.items():
                if "email" in col.lower() and isinstance(value, str):
                    assert value.endswith("example.invalid") or "@" not in value, (
                        f"{entity}.{col}: safe-mode email looks real: {value!r}"
                    )


def test_safe_mode_no_real_names(dataset: dict) -> None:
    """safe mode legal_name / first_name / last_name must follow the test pattern."""
    for entity, rows in dataset.items():
        for row in rows:
            for col, value in row.items():
                if col in ("legal_name", "first_name", "last_name") and isinstance(value, str):
                    assert (
                        value.startswith("Test") or value == ""
                    ), f"{entity}.{col}: safe-mode name looks real: {value!r}"


# ---------------------------------------------------------------------------
# Temporal consistency
# ---------------------------------------------------------------------------

def test_bitemporal_valid_time_ordering(dataset: dict) -> None:
    """valid_from must be <= valid_to (or valid_to is None for current row)."""
    for entity, rows in dataset.items():
        for idx, row in enumerate(rows):
            vf = row.get("valid_from")
            vt = row.get("valid_to")
            if vf is not None and vt is not None:
                assert vf <= vt, (
                    f"{entity} row {idx}: valid_from {vf} > valid_to {vt}"
                )


def test_transaction_settlement_ordering(dataset: dict) -> None:
    """Settlement date must not precede initiation date."""
    for idx, row in enumerate(dataset.get("Transaction", [])):
        tdt = row.get("transaction_date_time")
        sdt = row.get("settlement_date_time")
        if tdt is not None and sdt is not None:
            assert sdt >= tdt, (
                f"Transaction row {idx}: settlement_date_time {sdt} < transaction_date_time {tdt}"
            )


def test_transaction_amount_positive(dataset: dict) -> None:
    """Transaction amounts must always be positive."""
    for idx, row in enumerate(dataset.get("Transaction", [])):
        amount = row.get("amount")
        if amount is not None:
            assert amount > 0, f"Transaction row {idx}: amount={amount} is not positive"


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------

def test_seeded_output_is_deterministic() -> None:
    """Two builds with the same seed must produce identical first rows."""
    try:
        from integrity_check import check_integrity  # noqa: F401 — ensure runtime path works
    except ImportError:
        pass

    # UPDATE: replace skip with actual DatasetBuilder calls once imported
    pytest.skip("DatasetBuilder not imported — update UPDATE 1 above")

    # Example once imported:
    # ds1 = DatasetBuilder(pii_mode="safe").build(n_roots=3)
    # ds2 = DatasetBuilder(pii_mode="safe").build(n_roots=3)
    # for entity in ds1:
    #     assert ds1[entity][0] == ds2[entity][0], (
    #         f"{entity}: seeded build produced different first rows"
    #     )
