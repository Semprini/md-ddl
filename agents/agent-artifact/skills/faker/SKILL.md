---
name: faker
description: Use this skill when the user asks for synthetic data, fake data, test data, sample data, seed data, or Python Faker classes. Also use when the user says "generate data", "generate data for testing", "populate with data", or "create test records", or when the user references the Python `faker` library. Applies to all three data scopes: source system data (raw source column names), canonical entity data (entity attribute names), and destination physical output data (dimensional, normalized, or wide-column column names).
---

# Skill: Python Faker Synthetic Data Generation

Covers generation of Python factory classes using the `faker` library that produce
synthetic data from MD-DDL entity definitions. Output is a self-contained, runnable
Python module requiring only `pip install faker`.

This skill does not generate DDL, JSON Schema, Parquet contracts, or Cypher. For
physical schema artifacts use the Dimensional, Normalized, Wide Column, or Knowledge
Graph skills. Faker generation may be requested alongside those skills in the same session.

## MD-DDL Reference

Load before responding:

- `md-ddl-specification/3-Entities.md`
- `md-ddl-specification/4-Enumerations.md`
- `md-ddl-specification/7-Sources.md` (source-scope only)
- `md-ddl-specification/9-Data-Products.md` (destination-scope only)

---

## Process

### Step 1 — Confirm Scope

Confirm all four parameters before generating. Do not assume defaults silently.

**Scope:**

Scope | Input read | Field names | FK references
--- | --- | --- | ---
`source` | source.md + transform files | Source column names verbatim | Raw string stubs
`canonical` | entities/*.md | Canonical attribute names in snake_case | UUID strings
`destination` | Product file + entity files | Physical column names from DDL skill | Surrogate integer keys

**PII mode:**

Mode | When to use | Effect
--- | --- | ---
`safe` (default) | Shared environments, CI/CD, staging | Clearly fake: "Test Entity 0001", test@example.invalid
`realistic` | Isolated developer laptops | Plausible-looking Faker provider values

**Cardinality:** rows per root entity (default 10); FK-linked child sets if required.

**Output:** single combined module or one file per entity.

**Enterprise profile (optional):** ask whether the data should reflect a specific enterprise's demographic and product characteristics. See the Enterprise Profile section below. If the user describes an industry, market, or named customer base, offer to activate a profile before generating.

Transition phrase: "I have enough context to generate the Faker classes. Shall I proceed?"

### Step 2 — Read Entity Definitions

For each entity in scope:

1. Read entity YAML: existence, mutability, temporal.tracking, attributes, constraints, governance.
2. Read enum values from domain enums.md — never invent values.
3. Read relationships to identify FK dependencies and generation order.
4. Note `pii: true` attributes — apply PII mode to these.
5. Note `identifier: primary` — generate PK with uuid4() or sequential integer per scope.

### Step 3 — Apply Type-to-Faker Mapping

Apply field-name context overrides first; fall back to base type mapping.

### Step 4 — Apply Constraint Handling

Constraint type | Faker handling
--- | ---
`not_null: [attr]` | Never produce None for that field
`unique: [attrs]` | Use uuid4() or incrementing sequence
`check: "expr"` | Encode as guard logic with a comment naming the constraint
`enum:` attribute | random.choice(ENUM_VALUES) from declared values only

### Step 5 — Apply Temporal Strategy

Map mutability + temporal.tracking to the pattern in the Temporal Generation section.

### Step 6 — Assemble the Python Module

One factory class per entity. Append DatasetBuilder after all entity classes if requested.

### Step 7 — Output

1. Complete Python file(s) in a fenced code block.
2. **Generation notes**: scope, PII mode, PII fields, enum values used, constraints encoded, entity generation order, assumptions.

---

## Boundary Rules

- Python only. No SQL DDL, JSON Schema, Parquet, or Cypher.
- Only `faker` library and Python stdlib (uuid, random, datetime, decimal).
- Enum values always from domain enums.md. Never invented.
- FK keys injected via constructor — never hardcoded.
- `pii_mode='realistic'` does not remove the WARNING docstring requirement.

---

## Type-to-Faker Mapping

### Base Types

MD-DDL type | safe mode | realistic mode
--- | --- | ---
`string` | `f"value-{uuid.uuid4().hex[:8]}"` | `fake.word()`
`integer` | `fake.random_int(min=1, max=9999)` | same
`decimal` | `round(random.uniform(0.01, 9999.99), 2)` | same
`boolean` | `fake.boolean()` | same
`date` | `fake.date_between(start_date='-5y', end_date='today')` | wider window
`datetime` | `fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.utc)` | wider window
`timestamp` | `datetime.now(tz=timezone.utc)` | same
`enum:X` | `random.choice(X_VALUES)` | same
`[type]` array | list comprehension, randint(1,3) items | same

### Field-Name Context Overrides

Pattern | safe mode | realistic mode
--- | --- | ---
`*name*`, `*legal_name*` | `f"Test Entity {seq:04d}"` | `fake.name()`
`*first_name*` | `f"TestFirst{seq:04d}"` | `fake.first_name()`
`*last_name*` | `f"TestLast{seq:04d}"` | `fake.last_name()`
`*email*` | `f"test.user.{seq:04d}@example.invalid"` | `fake.email()`
`*phone*`, `*mobile*` | `f"+61400000{seq:04d}"` | `fake.phone_number()`
`*address_line*`, `*street*` | `f"Test Street {seq:04d}"` | `fake.street_address()`
`*city*`, `*suburb*` | `"Testville"` | `fake.city()`
`*state*`, `*region*` | `"TS"` | `fake.state_abbr()`
`*postcode*`, `*zip*` | `"0000"` | `fake.postcode()`
`*country*` | `"AU"` | `fake.country_code(representation='alpha-2')`
`*date_of_birth*`, `*dob*` | `date(1970, 1, 1)` | `fake.date_of_birth(minimum_age=18, maximum_age=80)`
`*tax_id*`, `*tfn*` | `f"TAX{seq:09d}"` | `fake.numerify(text='###-###-###')`
`*identifier*` (primary) | `str(uuid.uuid4())` | `str(uuid.uuid4())`
`*number*` (non-PK) | `f"NUM{seq:010d}"` | `fake.numerify(text='##########')`
`*amount*`, `*balance*`, `*value*` | `round(random.uniform(1.00, 50000.00), 2)` | same
`*currency*` | `"AUD"` | `fake.currency_code()`
`*reference*` | `f"REF-{seq:08d}"` | `fake.bothify(text='REF-########')`
`*description*`, `*notes*` | `"Synthetic test record"` | `fake.sentence(nb_words=6)`
`*url*`, `*website*` | `"https://example.invalid"` | `fake.url()`

---

## Enterprise Profile

An `EnterpriseProfile` is an optional declarative configuration layer that shapes
synthetic data to match an enterprise's actual demographic mix and product portfolio.
When active, it overrides base Faker provider calls for fields where distributional
realism matters: geography, customer age, customer type, monetary values, and
product references.

### When to offer it

Offer enterprise profile configuration when the user:

- Names a specific industry, geography, or market segment ("UK bank", "US fintech", "APAC insurer")
- Asks for "realistic", "representative", or "tailored" data rather than random test data
- References a specific customer demographic, value tier, or product catalogue
- Needs monetary amounts, currencies, or product eligibility to respect the enterprise's actual offer

### Confirming the profile (before Step 2)

Ask the following before generating:

1. **Industry / market** — What sector and primary market(s) does the enterprise operate in?
2. **Geographic distribution** — Which geographies, and roughly what share each?
3. **Age profile** — Any known skew in the customer age distribution?
4. **Customer mix** — What proportion of customers are individual vs. corporate vs. SME?
5. **Product catalogue** — What products does the enterprise offer? Are any restricted by customer type?

If the user cannot answer, offer the closest pre-built profile as a starting point and note it can be adjusted by copying and modifying the dataclass fields.

### Pre-built profiles

Three starting-point profiles ship with `enterprise_profile.py`:

Function | Enterprise type | Primary markets | Currency | Key characteristics
--- | --- | --- | --- | ---
`uk_retail_bank_profile()` | UK retail bank | GB, IE, FR, DE | GBP | Individual + SME mix; current account, savings, mortgage, personal loan, credit card, business account
`us_fintech_profile()` | US digital fintech | US, ES, ZH | USD | Young demographic skew; checking, savings, BNPL, debit card
`apac_insurance_profile()` | APAC regional insurer | AU, TW, JP, KR, SG | AUD | Mid-career skew; life, health, home, motor (individual); group life, corporate health (corporate)

### Profile-aware field overrides

When a profile is supplied, apply these overrides in addition to the base field-name
context rules. Profile rules take priority.

Field pattern | Profile-driven behaviour
--- | ---
`*country*`, `*locale*`, `*region*` | Sampled from `geo_weights`; Faker locale set per-record via `profile.sample_locale()`
`*date_of_birth*`, `*dob*` | `profile.sample_date_of_birth()` — age drawn from `age_bands` distribution
`*customer_type*`, `*party_type*`, `*entity_type*` | `profile.sample_customer_type()` — drawn from `customer_type_weights`
`*product_code*`, `*product_name*`, `*product_type*` | `profile.sample_product(customer_type)` — drawn from `products` catalogue, filtered by eligibility
`*amount*`, `*balance*`, `*premium*`, `*limit*` | `profile.sample_amount(product)` — uses `product.value_range`
`*currency*` | `profile.sample_currency(product)` — uses `product.currency`
`*sector*`, `*industry*` | `profile.sample_sector()` — drawn from `sector_weights` (B2B domains)

### Per-record locale sampling

When `geo_weights` is defined, construct a per-record Faker instance using the sampled
locale. This produces locale-appropriate names, addresses, phone numbers, and postcodes:

```python
locale = profile.sample_locale()
f = Faker(locale)
name    = f.name()     # Japanese name for ja_JP; French name for fr_FR; etc.
address = f.address()  # locale-appropriate street and postcode format
```

### Generating a custom profile

If no pre-built profile fits, generate a custom `EnterpriseProfile` inline:

```python
from agents.agent_artifact.skills.faker.runtime.enterprise_profile import (
    AgeBand, EnterpriseProfile, ProductSpec,
)

profile = EnterpriseProfile(
    geo_weights={"en_AU": 60, "en_NZ": 30, "en_SG": 10},
    age_bands=[
        AgeBand(18, 34, 25),
        AgeBand(35, 54, 45),
        AgeBand(55, 75, 30),
    ],
    customer_type_weights={"Individual": 70, "SMSF": 20, "Corporate": 10},
    products=[
        ProductSpec("Term Deposit", "TD", weight=50,
                    value_range=(10_000, 500_000), currency="AUD"),
        ProductSpec("Investment Account", "INV", weight=35,
                    value_range=(5_000, 2_000_000), currency="AUD"),
        ProductSpec("Margin Lending", "ML", weight=15,
                    value_range=(20_000, 300_000), currency="AUD",
                    eligible_customer_types=["Individual", "SMSF"]),
    ],
)
```

---

## Temporal Generation Patterns

### immutable / append_only

Single row with a past event timestamp. No valid-time or transaction-time columns.

### slowly_changing + valid_time

Current row by default. `with_history=True` prepends a prior row.

```python
def build(self, with_history: bool = False, **overrides) -> list[dict]:
    now = datetime.now(tz=timezone.utc)
    prior_end = now - timedelta(days=random.randint(30, 730))
    prior_start = prior_end - timedelta(days=random.randint(90, 1825))
    current = {"valid_from": prior_end, "valid_to": None, "is_current": True}
    if not with_history:
        return [{**current, **overrides}]
    prior = {**current, "valid_from": prior_start, "valid_to": prior_end, "is_current": False}
    return [prior, {**current, **overrides}]
```

When `with_history=True`, `build()` returns `list[dict]`. Flatten in `batch()`.

### slowly_changing + bitemporal

Same as valid_time, plus `recorded_at` / `superseded_at` columns mirroring the valid-time values.

### reference

Single static row. No temporal columns unless declared.

### frequently_changing

Single current-state row with `last_updated = datetime.now(tz=timezone.utc)`.

---

## Constraint Encoding

Add a comment naming each constraint from the entity YAML:

```python
# Constraint: Constraint Name From Entity YAML
```

Common patterns:

Constraint | Guard
--- | ---
`Status != 'Closed' OR end_date IS NOT NULL` | If status is 'Closed', set end_date to a past date
`end_date > start_date` | `end_date = start_date + timedelta(days=random.randint(1, 730))`
`amount > 0` | `max(0.01, abs(generated_amount))`
Cross-entity (e.g. PEP requires high risk) | Inject parent field as parameter; add `_constraint_satisfied: bool` field

---

## FK Relationship Handling

**Generation order:**
1. Reference entities (no FK dependencies)
2. Root independent entities
3. Dependent entities
4. Associative entities
5. Transaction/event entities

**Constructor injection:**

```python
class AccountFactory:
    def __init__(self, customer_ids: list[str], fake: Faker = None, pii_mode: str = "safe"):
        self.customer_ids = customer_ids
        self.fake = fake or Faker()
        self.pii_mode = pii_mode

    def build(self, **overrides) -> dict:
        return {
            "account_identifier": str(uuid.uuid4()),
            "customer_id": random.choice(self.customer_ids),
            **overrides,
        }
```

M:N associative factories accept both parent key lists as constructor parameters.

---

## Source-Scope Generation

Read transform files for source column names and source-side data types.

- Class names: `SourceIdTableNameFactory` (e.g. `SalesforceCrmAccountFactory`)
- Use source-side enum values from transform Map columns, not canonical values

---

## Destination-Scope Generation

Use physical column names from the applicable DDL skill output.

- Dimensional: `dim_*` / `fact_*` column names; surrogate keys as sequential integers from 1
- Normalized: snake_case DDL column names; surrogate integer keys
- Wide-column: flat snake_case; no FK columns

```python
_sk_counter = 0

def _next_sk() -> int:
    global _sk_counter
    _sk_counter += 1
    return _sk_counter
```

---

## Code Pattern

### Module header

```python
"""
Synthetic data factory — Domain / scope
Scope:    source | canonical | destination
PII mode: safe | realistic
Profile:  None | uk_retail_bank | us_fintech | apac_insurance | custom

WARNING: SYNTHETIC DATA ONLY. Do not use for production data migration.
Dependencies: pip install faker
"""

from __future__ import annotations
import random, uuid
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from faker import Faker

# Enterprise profile — optional; omit the import and pass profile=None to use
# base Faker generation without demographic or product-catalogue weighting.
from agents.agent_artifact.skills.faker.runtime.enterprise_profile import (
    EnterpriseProfile,
    uk_retail_bank_profile,   # swap for the closest pre-built profile
)

# Enum pools — sourced from domain/enums.md
PARTY_STATUS_VALUES = ["Active", "Under Review", "Inactive", "Closed"]

fake = Faker()
Faker.seed(0)
random.seed(0)

_seq = 0

def _next_seq() -> int:
    global _seq
    _seq += 1
    return _seq
```

### Factory class

Profile is accepted as a constructor argument. When `profile` is `None` the factory
falls back to the base Faker generation rules with no distributional weighting.

```python
class PartyFactory:
    """
    Entity:     Party
    Existence:  independent
    Mutability: slowly_changing
    Temporal:   bitemporal
    PII fields: legal_name, also_known_as
    Constraints encoded:
      - Legal Name Required: legal_name is never None
      - Review Date Must Not Be Overdue: next_review_date >= today
    """

    def __init__(self, fake: Faker = None, pii_mode: str = "safe",
                 profile: EnterpriseProfile = None):
        self.fake = fake or Faker()
        self.pii_mode = pii_mode
        self.profile = profile

    def build(self, with_history: bool = False, **overrides) -> list[dict]:
        seq = _next_seq()

        # Per-record locale when a profile is active; otherwise use shared instance.
        if self.profile:
            locale = self.profile.sample_locale()
            f = Faker(locale)
        else:
            locale = None
            f = self.fake

        # Profile-driven fields; fall back to base rules when no profile.
        customer_type = (
            self.profile.sample_customer_type() if self.profile else "Individual"
        )
        product = (
            self.profile.sample_product(customer_type) if self.profile else None
        )
        dob = (
            self.profile.sample_date_of_birth() if self.profile
            else f.date_of_birth(minimum_age=18, maximum_age=80)
        )
        country = (
            self.profile.sample_country() if self.profile
            else (f.country_code(representation="alpha-2")
                  if self.pii_mode == "realistic" else "AU")
        )
        amount = (
            self.profile.sample_amount(product) if self.profile
            else round(random.uniform(1.0, 50_000.0), 2)
        )
        currency = (
            self.profile.sample_currency(product) if self.profile else "AUD"
        )

        now = datetime.now(tz=timezone.utc)
        prior_end = now - timedelta(days=random.randint(30, 730))
        prior_start = prior_end - timedelta(days=random.randint(90, 1825))

        # Constraint: Review Date Must Not Be Overdue
        next_review_date = date.today().replace(
            year=date.today().year + random.randint(0, 1),
            month=random.randint(1, 12),
        )

        current = {
            "party_identifier": str(uuid.uuid4()),
            "legal_name": f.name() if self.pii_mode == "realistic" else f"Test Entity {seq:04d}",
            "party_type": customer_type,
            "date_of_birth": dob,
            "country": country,
            "party_status": random.choice(PARTY_STATUS_VALUES),
            "next_review_date": next_review_date,
            "product_code": product.code if product else None,
            "amount": amount,
            "currency": currency,
            "valid_from": prior_end,
            "valid_to": None,
            "is_current": True,
            "recorded_at": prior_end,
            "superseded_at": None,
            **overrides,
        }
        if not with_history:
            return [current]
        prior = {**current,
            "valid_from": prior_start, "valid_to": prior_end,
            "is_current": False, "recorded_at": prior_start, "superseded_at": prior_end,
        }
        return [prior, current]

    def batch(self, n: int, with_history: bool = False, **overrides) -> list[dict]:
        rows = []
        for _ in range(n):
            rows.extend(self.build(with_history=with_history, **overrides))
        return rows
```

### DatasetBuilder

`profile` is threaded through to every factory so all entities in a dataset
share the same distributional constraints. Omit it (or pass `None`) for
uniform-random baseline generation.

```python
class DatasetBuilder:
    """
    Generates a referentially consistent dataset.
    Generation order: root entities first, then dependents, then associative, then events.
    """

    def __init__(self, fake: Faker = None, pii_mode: str = "safe",
                 profile: EnterpriseProfile = None):
        self.fake = fake or Faker()
        self.pii_mode = pii_mode
        self.profile = profile

    def build(self, n_roots: int = 10, children_per_root: int = 2,
              with_history: bool = False) -> dict[str, list[dict]]:
        root_factory = PartyFactory(
            fake=self.fake, pii_mode=self.pii_mode, profile=self.profile
        )
        roots: list[dict] = []
        for _ in range(n_roots):
            roots.extend(root_factory.build(with_history=with_history))

        root_ids = [r["party_identifier"] for r in roots if r["is_current"]]

        # Build dependent entities using root_ids as FK pool
        # child_factory = ChildFactory(parent_ids=root_ids, profile=self.profile, ...)

        return {"Party": roots}


if __name__ == "__main__":
    import json
    from agents.agent_artifact.skills.faker.runtime.enterprise_profile import (
        uk_retail_bank_profile,
    )

    # Without profile — uniform-random baseline
    dataset_base = DatasetBuilder(pii_mode="safe").build(n_roots=5)

    # With profile — demographically and product-catalogue weighted
    dataset_profiled = DatasetBuilder(
        pii_mode="realistic", profile=uk_retail_bank_profile()
    ).build(n_roots=5, with_history=True)

    for name, rows in dataset_profiled.items():
        print(f"\n=== {name} ({len(rows)} rows) ===")
        print(json.dumps(rows[0], indent=2, default=str))
```

---

## Supporting Runtime

The following files ship with the faker skill and should be offered alongside any generated module.

File | Purpose
--- | ---
`agents/agent-artifact/skills/faker/runtime/enterprise_profile.py` | Declarative demographic and product configuration. Provides `EnterpriseProfile`, `AgeBand`, and `ProductSpec` dataclasses plus three pre-built profiles (`uk_retail_bank_profile`, `us_fintech_profile`, `apac_insurance_profile`). Pass a profile to any factory or `DatasetBuilder` to weight geographic, age, customer-type, and monetary fields toward the enterprise's actual distribution. Stdlib only.
`agents/agent-artifact/skills/faker/runtime/integrity_check.py` | Validates FK resolution, not-null, enum membership, PK uniqueness, and bitemporal chain coherence (`check_temporal_chain()`). Zero external dependencies — stdlib only.
`agents/agent-artifact/skills/faker/runtime/consistency_scenario.py` | Eventual-consistency scenario simulator. Define `SourceFeed` objects (name, lag_minutes, change_model), call `generate_scenario()` to produce per-feed source views and convergence deltas, then `check_convergence()` to validate against a declared SLA window. Zero external dependencies — stdlib only.
`agents/agent-artifact/skills/faker/runtime/test_template.py` | Pytest template. Copy alongside the generated module, fill in the four `# UPDATE` sections (import, integrity spec, temporal/SLA config, expected entities), run `pytest test_factories.py -v`.

**Reference generated examples:**
- `examples/Financial Crime/factories.py` — complete canonical-scope factory covering Currency → Party → Account → Transaction with embedded integrity spec constants.
- `examples/Financial Crime/consistency_example.py` — end-to-end eventual consistency demonstration: three source feeds (5/30/60 min lag), convergence report, SLA validation, and null handling illustration.

### Offering the runtime

At Step 7, after delivering the generated module, add:

> "Would you like me to also generate a companion test file (`test_<module>.py`) pre-filled with the integrity and temporal-consistency spec for this domain? Copy `integrity_check.py` and `consistency_scenario.py` from the faker runtime alongside it and run `pytest` to verify referential integrity, temporal chain coherence, and eventual-consistency convergence end-to-end."

If the user did not supply an enterprise profile and the domain has a recognisable industry or market context, also offer:

> "I can also apply an enterprise profile to weight the generated data toward a specific customer demographic and product catalogue — for example a UK retail bank, a US fintech, or an APAC insurer. Would you like me to activate one of the pre-built profiles, or describe your enterprise's mix and I'll build a custom one?"

### When to offer consistency_scenario.py

Offer it when:
- The domain has multiple source systems with different `change_model` values.
- Any entity has `temporal.tracking: bitemporal` or `temporal.tracking: valid_time`.
- The user asks about propagation lag, freshness SLA, or in-flight data state.

Do **not** offer it for `reference` or `append_only` entities with no `recorded_at` column.

---

## Handoff

**To DDL skills:** generate DDL first, then use physical column names for destination-scope Faker generation.

**To Agent Ontology:** if primary identifier undeclared, enum missing from enums.md, or existence/mutability absent — flag and defer. Do not invent.

---

## Generation Limitations

- Syntactically valid but untested. Run `python -m py_compile file.py` before use.
- Cross-entity constraints enforced within a single `DatasetBuilder.build()` call. Use `integrity_check.py` to verify the full dataset after generation.
- One-to-one cardinality honored within `DatasetBuilder.build()` but not across independent factory calls.
- `pii_mode='realistic'` is fictional data. Caller must ensure it never reaches production.
