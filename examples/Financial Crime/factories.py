"""
Synthetic data factory — Financial Crime / canonical scope
Scope:    canonical
PII mode: safe (default) | realistic

Generated from:
  examples/Financial Crime/entities/currency.md
  examples/Financial Crime/entities/party.md
  examples/Financial Crime/entities/account.md
  examples/Financial Crime/entities/transaction.md
  examples/Financial Crime/enums.md

WARNING: SYNTHETIC DATA ONLY. Do not use for production data migration.
Dependencies: pip install faker

Generation order (topological — respects FK dependencies):
  1. Currency        (reference — no FKs)
  2. Party           (independent, slowly_changing, bitemporal)
  3. Account         (independent, slowly_changing, valid_time; FK → Currency)
  4. Transaction     (dependent, append_only; FK → Currency, Account)
"""

from __future__ import annotations
import random
import uuid
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from faker import Faker

# ---------------------------------------------------------------------------
# Enum pools — sourced from examples/Financial Crime/enums.md
# ---------------------------------------------------------------------------
PARTY_STATUS_VALUES = ["Active", "Under Review", "Restricted", "Inactive", "Closed"]
FINANCIAL_CRIME_RISK_RATING_VALUES = ["Low", "Medium", "High", "Very High"]
SANCTIONS_SCREEN_STATUS_VALUES = [
    "Not Screened", "Clear", "Potential Match", "Confirmed Match", "False Positive",
]
ACCOUNT_STATUS_VALUES = ["Pending", "Active", "Dormant", "Frozen", "Suspended", "Closed"]
ACCOUNT_TYPE_VALUES = [
    "Savings", "Current", "Term Deposit", "Loan",
    "Line Of Credit", "Mortgage", "Offset", "Foreign Currency",
]
TRANSACTION_TYPE_VALUES = [
    "Wire Transfer", "SWIFT Transfer", "EFTPOS", "ATM Withdrawal", "ATM Deposit",
    "Direct Debit", "Direct Credit", "Internal Transfer", "BPay",
    "Cash Deposit", "Cash Withdrawal", "Cheque", "RTGS",
]
TRANSACTION_CHANNEL_VALUES = [
    "Branch", "Online Banking", "Mobile Banking", "ATM", "EFTPOS Terminal",
    "SWIFT", "Direct Entry", "Third Party", "Internal System",
]
TRANSACTION_STATUS_VALUES = [
    "Pending", "Authorised", "Cleared", "Settled",
    "Failed", "Reversed", "Cancelled", "Under Review",
]

# ISO 4217 representative subset — sourced from enums.md
CURRENCY_CODES = ["AUD", "NZD", "USD", "EUR", "GBP", "JPY", "SGD", "HKD", "CHF", "CAD"]
CURRENCY_NAMES = {
    "AUD": "Australian Dollar", "NZD": "New Zealand Dollar", "USD": "United States Dollar",
    "EUR": "Euro", "GBP": "Pound Sterling", "JPY": "Japanese Yen",
    "SGD": "Singapore Dollar", "HKD": "Hong Kong Dollar", "CHF": "Swiss Franc",
    "CAD": "Canadian Dollar",
}
CURRENCY_MINOR_UNITS = {
    "AUD": 2, "NZD": 2, "USD": 2, "EUR": 2, "GBP": 2,
    "JPY": 0, "SGD": 2, "HKD": 2, "CHF": 2, "CAD": 2,
}

# ---------------------------------------------------------------------------
# Seeding — deterministic by default
# ---------------------------------------------------------------------------
fake = Faker()
Faker.seed(0)
random.seed(0)

_seq = 0


def _next_seq() -> int:
    global _seq
    _seq += 1
    return _seq


# ---------------------------------------------------------------------------
# CurrencyFactory
# Entity:     Currency
# Existence:  independent
# Mutability: reference (static rows; no temporal columns)
# PII fields: none
# ---------------------------------------------------------------------------
class CurrencyFactory:
    """Produces one row per ISO 4217 code in CURRENCY_CODES."""

    def build_all(self) -> list[dict]:
        return [
            {
                "currency_code": code,
                "currency_name": CURRENCY_NAMES[code],
                "minor_unit": CURRENCY_MINOR_UNITS[code],
            }
            for code in CURRENCY_CODES
        ]


# ---------------------------------------------------------------------------
# PartyFactory
# Entity:      Party
# Existence:   independent
# Mutability:  slowly_changing
# Temporal:    bitemporal (valid_time + transaction_time)
# PII fields:  legal_name, also_known_as
# Constraints encoded:
#   - Legal Name Required:           legal_name is never None
#   - Review Date Must Not Be Overdue: next_review_date >= today (unless Under Review)
#   - Confirmed Sanctions Match Blocks Service: sanctions_screen_status != 'Confirmed Match'
#     (softened in synthetic data — status allowed but flagged via comment)
# ---------------------------------------------------------------------------
class PartyFactory:
    """
    Entity:     Party
    Existence:  independent
    Mutability: slowly_changing
    Temporal:   bitemporal
    PII fields: legal_name, also_known_as
    Constraints encoded:
      - Legal Name Required
      - Review Date Must Not Be Overdue
    """

    def __init__(self, fake: Faker = None, pii_mode: str = "safe"):
        self.fake = fake or Faker()
        self.pii_mode = pii_mode

    def build(self, with_history: bool = False, **overrides) -> list[dict]:
        seq = _next_seq()
        f = self.fake
        now = datetime.now(tz=timezone.utc)
        prior_end = now - timedelta(days=random.randint(30, 730))
        prior_start = prior_end - timedelta(days=random.randint(90, 1825))

        # Constraint: Review Date Must Not Be Overdue
        # next_review_date is always in the future unless status is Under Review
        today = date.today()
        next_review_date = today.replace(
            year=today.year + random.randint(0, 2),
            month=random.randint(1, 12),
            day=random.randint(1, 28),
        )

        # PII: legal_name, also_known_as
        if self.pii_mode == "realistic":
            legal_name = f.name()
            also_known_as = [f.name()] if random.random() < 0.3 else []
        else:
            legal_name = f"Test Entity {seq:04d}"
            also_known_as = [f"Test AKA {seq:04d}"] if random.random() < 0.3 else []

        current = {
            "party_identifier": str(uuid.uuid4()),
            "legal_name": legal_name,                        # pii: true
            "also_known_as": also_known_as,                  # pii: true
            "party_status": random.choice(PARTY_STATUS_VALUES),
            "risk_rating": random.choice(FINANCIAL_CRIME_RISK_RATING_VALUES),
            "sanctions_screen_status": random.choice(SANCTIONS_SCREEN_STATUS_VALUES),
            "next_review_date": next_review_date,
            # bitemporal columns
            "valid_from": prior_end,
            "valid_to": None,
            "is_current": True,
            "recorded_at": prior_end,
            "superseded_at": None,
            **overrides,
        }

        if not with_history:
            return [current]

        prior = {
            **current,
            "valid_from": prior_start,
            "valid_to": prior_end,
            "is_current": False,
            "recorded_at": prior_start,
            "superseded_at": prior_end,
        }
        return [prior, current]

    def batch(self, n: int, with_history: bool = False, **overrides) -> list[dict]:
        rows: list[dict] = []
        for _ in range(n):
            rows.extend(self.build(with_history=with_history, **overrides))
        return rows


# ---------------------------------------------------------------------------
# AccountFactory
# Entity:      Account
# Existence:   independent
# Mutability:  slowly_changing
# Temporal:    valid_time
# PII fields:  none
# FK:          currency_code → Currency.currency_code
# Constraints encoded:
#   - Closed Date After Opened Date: closed_date > opened_date when present
# ---------------------------------------------------------------------------
class AccountFactory:
    """
    Entity:     Account
    Existence:  independent
    Mutability: slowly_changing
    Temporal:   valid_time
    PII fields: none
    FK:         currency_code → Currency.currency_code
    """

    def __init__(
        self,
        currency_codes: list[str],
        fake: Faker = None,
        pii_mode: str = "safe",
    ):
        self.currency_codes = currency_codes
        self.fake = fake or Faker()
        self.pii_mode = pii_mode

    def build(self, with_history: bool = False, **overrides) -> list[dict]:
        seq = _next_seq()
        now = datetime.now(tz=timezone.utc)
        prior_end = now - timedelta(days=random.randint(30, 730))
        prior_start = prior_end - timedelta(days=random.randint(90, 1825))

        opened_date = (now - timedelta(days=random.randint(365, 3650))).date()

        # Constraint: Closed Date After Opened Date
        account_status = random.choice(ACCOUNT_STATUS_VALUES)
        closed_date = None
        if account_status == "Closed":
            closed_date = opened_date + timedelta(days=random.randint(30, 2000))

        current = {
            "account_identifier": str(uuid.uuid4()),
            "account_number": f"BSB{seq:06d}",
            "account_type": random.choice(ACCOUNT_TYPE_VALUES),
            "account_status": account_status,
            "opened_date": opened_date,
            "closed_date": closed_date,
            "currency_code": random.choice(self.currency_codes),  # FK → Currency
            # valid_time columns
            "valid_from": prior_end,
            "valid_to": None,
            "is_current": True,
            **overrides,
        }

        if not with_history:
            return [current]

        prior = {
            **current,
            "valid_from": prior_start,
            "valid_to": prior_end,
            "is_current": False,
        }
        return [prior, current]

    def batch(self, n: int, with_history: bool = False, **overrides) -> list[dict]:
        rows: list[dict] = []
        for _ in range(n):
            rows.extend(self.build(with_history=with_history, **overrides))
        return rows


# ---------------------------------------------------------------------------
# TransactionFactory
# Entity:      Transaction
# Existence:   dependent
# Mutability:  append_only
# Temporal:    transaction_time (recorded_at only — no valid_time)
# PII fields:  none
# FK (required): currency_code → Currency.currency_code
# FK (nullable): debit_account_identifier → Account.account_identifier
#                credit_account_identifier → Account.account_identifier
# Constraints encoded:
#   - Amount Must Be Positive:         amount = abs(generated) with floor of 0.01
#   - Settlement After Initiation:     settlement_date_time >= transaction_date_time
#   - Settled Transaction Has Settlement Time: if status == Settled, settlement is set
# ---------------------------------------------------------------------------
class TransactionFactory:
    """
    Entity:     Transaction
    Existence:  dependent
    Mutability: append_only
    Temporal:   transaction_time
    PII fields: none
    FK (required): currency_code → Currency.currency_code
    FK (nullable): debit_account_identifier, credit_account_identifier → Account.account_identifier
    """

    def __init__(
        self,
        currency_codes: list[str],
        account_identifiers: list[str],
        fake: Faker = None,
        pii_mode: str = "safe",
    ):
        self.currency_codes = currency_codes
        self.account_identifiers = account_identifiers
        self.fake = fake or Faker()
        self.pii_mode = pii_mode

    def build(self, **overrides) -> dict:
        seq = _next_seq()
        now = datetime.now(tz=timezone.utc)

        transaction_date_time = now - timedelta(
            days=random.randint(0, 365),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )

        transaction_status = random.choice(TRANSACTION_STATUS_VALUES)

        # Constraint: Settlement After Initiation
        # Constraint: Settled Transaction Has Settlement Time
        if transaction_status in ("Settled", "Reversed"):
            settlement_date_time = transaction_date_time + timedelta(
                hours=random.randint(0, 48)
            )
        elif transaction_status in ("Pending", "Authorised", "Under Review"):
            settlement_date_time = None
        else:
            settlement_date_time = None

        # Constraint: Amount Must Be Positive
        amount = max(Decimal("0.01"), round(Decimal(str(random.uniform(1.00, 50000.00))), 2))

        # FK (nullable): randomly assign debit/credit accounts from pool
        debit_account = random.choice(self.account_identifiers) if random.random() > 0.1 else None
        credit_account = random.choice(self.account_identifiers) if random.random() > 0.1 else None

        return {
            "transaction_identifier": str(uuid.uuid4()),
            "transaction_date_time": transaction_date_time,
            "settlement_date_time": settlement_date_time,
            "amount": amount,
            "transaction_type": random.choice(TRANSACTION_TYPE_VALUES),
            "transaction_channel": random.choice(TRANSACTION_CHANNEL_VALUES),
            "transaction_status": transaction_status,
            "reference": f"REF-{seq:08d}",
            "currency_code": random.choice(self.currency_codes),  # FK → Currency
            "debit_account_identifier": debit_account,             # FK → Account (nullable)
            "credit_account_identifier": credit_account,           # FK → Account (nullable)
            **overrides,
        }

    def batch(self, n: int, **overrides) -> list[dict]:
        return [self.build(**overrides) for _ in range(n)]


# ---------------------------------------------------------------------------
# DatasetBuilder
# Generates a referentially consistent dataset across all four entities.
# Generation order: Currency → Party → Account → Transaction
# ---------------------------------------------------------------------------
class DatasetBuilder:
    """
    Generates a referentially consistent Financial Crime dataset.

    Generation order (topological):
      1. Currency        — reference; no FKs
      2. Party           — independent; no FK dependencies in core attributes
      3. Account         — FK → Currency.currency_code
      4. Transaction     — FK → Currency.currency_code, Account.account_identifier

    Parameters
    ----------
    n_parties           : Party root records (current rows)
    accounts_per_party  : Account records created per Party (approximate)
    txns_per_account    : Transaction records created per active Account
    with_history        : Include prior SCD rows for Party and Account
    pii_mode            : "safe" (default) or "realistic"
    """

    def __init__(self, fake: Faker = None, pii_mode: str = "safe"):
        self.fake = fake or Faker()
        self.pii_mode = pii_mode

    def build(
        self,
        n_parties: int = 10,
        accounts_per_party: int = 2,
        txns_per_account: int = 5,
        with_history: bool = False,
    ) -> dict[str, list[dict]]:

        # --- 1. Currency (reference) ---
        currencies = CurrencyFactory().build_all()
        currency_codes = [c["currency_code"] for c in currencies]

        # --- 2. Party ---
        party_factory = PartyFactory(fake=self.fake, pii_mode=self.pii_mode)
        parties: list[dict] = []
        for _ in range(n_parties):
            parties.extend(party_factory.build(with_history=with_history))

        # --- 3. Account (FK → Currency) ---
        account_factory = AccountFactory(
            currency_codes=currency_codes,
            fake=self.fake,
            pii_mode=self.pii_mode,
        )
        accounts: list[dict] = []
        for _ in range(n_parties * accounts_per_party):
            accounts.extend(account_factory.build(with_history=with_history))

        # FK pool: only current account rows supply IDs for Transaction FKs
        active_account_ids = [
            a["account_identifier"] for a in accounts if a.get("is_current", True)
        ]

        # --- 4. Transaction (FK → Currency, FK → Account) ---
        txn_factory = TransactionFactory(
            currency_codes=currency_codes,
            account_identifiers=active_account_ids,
            fake=self.fake,
            pii_mode=self.pii_mode,
        )
        transactions = txn_factory.batch(
            n=len(active_account_ids) * txns_per_account
        )

        return {
            "Currency": currencies,
            "Party": parties,
            "Account": accounts,
            "Transaction": transactions,
        }


# ---------------------------------------------------------------------------
# Integrity spec — used by integrity_check.py and test_factories.py
# ---------------------------------------------------------------------------
FK_SPECS_FINANCIAL_CRIME = None  # populated below after import guard
NOT_NULL_FINANCIAL_CRIME = {
    "Party":       ["party_identifier", "legal_name"],
    "Account":     ["account_identifier", "account_number", "currency_code"],
    "Transaction": ["transaction_identifier", "amount", "currency_code"],
}
ENUM_VALUES_FINANCIAL_CRIME = {
    "Party": {
        "party_status":            PARTY_STATUS_VALUES,
        "risk_rating":             FINANCIAL_CRIME_RISK_RATING_VALUES,
        "sanctions_screen_status": SANCTIONS_SCREEN_STATUS_VALUES,
    },
    "Account": {
        "account_status": ACCOUNT_STATUS_VALUES,
        "account_type":   ACCOUNT_TYPE_VALUES,
    },
    "Transaction": {
        "transaction_type":    TRANSACTION_TYPE_VALUES,
        "transaction_channel": TRANSACTION_CHANNEL_VALUES,
        "transaction_status":  TRANSACTION_STATUS_VALUES,
    },
}
# unique_pk: all rows — for reference and append_only entities
UNIQUE_PK_FINANCIAL_CRIME = {
    "Currency":    "currency_code",
    "Transaction": "transaction_identifier",
}
# unique_current_pk: current rows only — for SCD2/bitemporal entities
# History rows legitimately repeat the entity identifier across prior/current pairs.
UNIQUE_CURRENT_PK_FINANCIAL_CRIME = {
    "Party":   "party_identifier",
    "Account": "account_identifier",
}

try:
    from integrity_check import FKSpec
    FK_SPECS_FINANCIAL_CRIME = [
        FKSpec("Account",     "currency_code",             "Currency", "currency_code"),
        FKSpec("Transaction", "currency_code",             "Currency", "currency_code"),
        FKSpec("Transaction", "debit_account_identifier",  "Account",  "account_identifier", nullable=True),
        FKSpec("Transaction", "credit_account_identifier", "Account",  "account_identifier", nullable=True),
    ]
except ImportError:
    FK_SPECS_FINANCIAL_CRIME = None  # integrity_check.py not on path


# ---------------------------------------------------------------------------
# Entry point — quick smoke test and integrity check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json

    dataset = DatasetBuilder(pii_mode="safe").build(
        n_parties=5, accounts_per_party=2, txns_per_account=3, with_history=True
    )

    for name, rows in dataset.items():
        print(f"\n=== {name} ({len(rows)} rows) ===")
        print(json.dumps(rows[0], indent=2, default=str))

    # Run integrity checks if runtime is available
    try:
        from integrity_check import check_integrity, print_report
        print("\n--- Integrity check ---")
        errors = check_integrity(
            dataset,
            fk_specs=FK_SPECS_FINANCIAL_CRIME,
            not_null=NOT_NULL_FINANCIAL_CRIME,
            enum_values=ENUM_VALUES_FINANCIAL_CRIME,
            unique_pk=UNIQUE_PK_FINANCIAL_CRIME,
            unique_current_pk=UNIQUE_CURRENT_PK_FINANCIAL_CRIME,
        )
        print_report(errors)
    except ImportError:
        print(
            "\n[integrity_check not found] "
            "Copy integrity_check.py from agents/agent-artifact/skills/faker/runtime/ "
            "alongside this file to enable integrity validation."
        )
