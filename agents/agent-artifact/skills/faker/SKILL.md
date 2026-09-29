---
name: faker
description: Use when the user asks for synthetic, fake, test, sample, or seed data, Python Faker classes, or to "generate data" or "populate with data"; for data that reflects an enterprise's customer mix or products (enterprise profiles); or to validate referential integrity, temporal chains, or eventual-consistency convergence on generated data. Covers source-system, canonical, and destination-physical scopes.
---

# Skill: Faker Synthetic Data

Generate Python factory classes, using the `faker` library, that produce synthetic data
from MD-DDL definitions. The output is a runnable module needing only `pip install faker`,
plus the stdlib runtime files in `runtime/` copied alongside it.

## MD-DDL Reference

Load `md-ddl-specification/3-Entities.md` and `4-Enumerations.md`. Also load
`7-Sources.md` for source scope and `9-Data-Products.md` for destination scope.

---

## Process

1. **Confirm the parameters.** Don't assume them:

   Parameter | Options
   --- | ---
   Scope | `source`: source column names from transform detail; FKs as raw string stubs. `canonical`: attribute names in snake_case; FKs as UUID strings. `destination`: physical column names from the DDL or dbt output; surrogate integer keys.
   PII mode | `safe` (default): obviously fake values ("Test Entity 0001", `@example.invalid`) for shared environments and CI. `realistic`: plausible values, for isolated developer machines only.
   Cardinality | Rows per root entity (default 10), and child sets per parent
   Output | One module, or one file per entity
   Enterprise profile | None, a pre-built profile, or a custom one (below). Offer it when the user names an industry or market, or wants "realistic" or "representative" data.

2. **Read the definitions.** For each entity, read `existence`, `mutability`,
   `temporal.tracking`, attributes, constraints, and governance. Take enum values from
   the domain's enums, never invented ones. Read relationships for FK dependencies and
   generation order. Note `pii: true` attributes, to which PII mode applies, and the
   `identifier: primary` attribute.
3. **Generate** using the mappings, constraint encoding, temporal patterns, and FK order
   below. Write one factory class per entity, then a `DatasetBuilder`.
4. **Output** the module, plus generation notes: scope, PII mode, PII fields, enum values
   used, constraints encoded, generation order, profile, and assumptions. Then offer the
   companion test file and runtime (below).

---

## Type Mapping

Apply the field-name overrides first, then the base type.

**Base types**

MD-DDL type | Generator
--- | ---
`string` | safe: `f"value-{uuid.uuid4().hex[:8]}"`; realistic: `fake.word()`
`integer` | `fake.random_int(min=1, max=9999)`
`decimal` | `round(random.uniform(0.01, 9999.99), 2)`
`boolean` | `fake.boolean()`
`date` | `fake.date_between(start_date='-5y', end_date='today')`
`datetime` | `fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.utc)`
`timestamp` | `datetime.now(tz=timezone.utc)`
`enum:X` | `random.choice(X_VALUES)`, from declared values only
`[type]` array | one to three generated items

**Field-name overrides**

Pattern | safe | realistic
--- | --- | ---
`*name*`, `*legal_name*` | `f"Test Entity {seq:04d}"` | `fake.name()`
`*first_name*` / `*last_name*` | `f"TestFirst{seq:04d}"` / `f"TestLast{seq:04d}"` | `fake.first_name()` / `fake.last_name()`
`*email*` | `f"test.user.{seq:04d}@example.invalid"` | `fake.email()`
`*phone*`, `*mobile*` | `f"+61400000{seq:04d}"` | `fake.phone_number()`
`*address_line*`, `*street*` | `f"Test Street {seq:04d}"` | `fake.street_address()`
`*city*`, `*suburb*` / `*state*`, `*region*` / `*postcode*`, `*zip*` | `"Testville"` / `"TS"` / `"0000"` | `fake.city()` / `fake.state_abbr()` / `fake.postcode()`
`*country*` | `"AU"` | `fake.country_code(representation='alpha-2')`
`*date_of_birth*`, `*dob*` | `date(1970, 1, 1)` | `fake.date_of_birth(minimum_age=18, maximum_age=80)`
`*tax_id*`, `*tfn*` | `f"TAX{seq:09d}"` | `fake.numerify(text='###-###-###')`
`*identifier*` (primary) | `str(uuid.uuid4())` | `str(uuid.uuid4())`
`*number*` (not a key) | `f"NUM{seq:010d}"` | `fake.numerify(text='##########')`
`*amount*`, `*balance*`, `*value*` | `round(random.uniform(1.00, 50000.00), 2)` | same
`*currency*` | `"AUD"` | `fake.currency_code()`
`*reference*` | `f"REF-{seq:08d}"` | `fake.bothify(text='REF-########')`
`*description*`, `*notes*` | `"Synthetic test record"` | `fake.sentence(nb_words=6)`
`*url*`, `*website*` | `"https://example.invalid"` | `fake.url()`

## Constraints

Name each encoded constraint in a comment (`# Constraint: <name from entity YAML>`).

Constraint | Encoding
--- | ---
`not_null` | Never produce `None` for the field
`unique` | `uuid4()` or an incrementing sequence
`check` | Guard logic. For example, `end_date > start_date` becomes `start_date + timedelta(days=randint(1, 730))`; `amount > 0` becomes `max(0.01, abs(x))`; and "Closed requires end date" means setting a past end date when the status is Closed.
Cross-entity rule (e.g. PEP requires high risk) | Pass the parent's field into the child factory. Such rules hold within one `DatasetBuilder.build()`, not across separate factory calls.

## Temporal Patterns

Mutability and tracking | Rows
--- | ---
`immutable`, `append_only` | One row with a past event timestamp
`slowly_changing` + `valid_time` | The current row (`valid_from`, `valid_to: None`, `is_current: True`). With `with_history=True`, a prior closed row too. `build()` returns a list, and `batch()` flattens it.
`slowly_changing` + `bitemporal` | As valid time, plus `recorded_at` and `superseded_at`
`frequently_changing` | One current row with `last_updated`
`reference` | One static row

History rows of an entity share its identifier, so check PK uniqueness on current rows
only (`unique_current_pk` in `integrity_check.py`).

## Foreign Keys and Order

Generate in this order: reference entities, independent roots, dependent, associative,
then transaction and event entities. Inject parent key pools through constructors
(`AccountFactory(customer_ids=[...])`), never hard-coded. Associative factories take
both parents' key pools.

## Source and Destination Scope

- **Source:** use the column names and source-side types from transform detail, and
  source-side codes from lookup and conditional transforms, not canonical values. Name
  classes `<SourceId><Table>Factory`.
- **Destination:** use physical column names from the generated DDL or dbt models, with
  surrogate keys as integers from 1 (a module-level counter). For a dbt project, write
  the rows as seeds or DuckLake loads for Agent Test.

---

## Enterprise Profile

`runtime/enterprise_profile.py` provides the `EnterpriseProfile`, `AgeBand`, and
`ProductSpec` dataclasses and three pre-built profiles. A profile weights
distribution-sensitive fields toward the enterprise's real mix. It changes only the
fields below; all other generation is unchanged.

Before generating with a profile, confirm:

- the industry and primary markets
- the geographic split
- the age skew
- the customer mix (individual, corporate, SME)
- the products, with the customer types each is restricted to

If the user can't answer, start from the closest pre-built profile and adjust it.

Function | For | Locales and currency
--- | --- | ---
`uk_retail_bank_profile()` | UK retail bank; individual and SME products (current account, savings, mortgage, loans, cards, business account) | GB-weighted with IE, FR, DE; GBP
`us_fintech_profile()` | US digital fintech with a young skew (checking, savings, BNPL, debit) | US, including `es_US` and `zh_CN` customer segments; USD
`apac_insurance_profile()` | APAC insurer; individual lines (life, health, home, motor) and corporate lines (group life, health) | AU, TW, JP, KR, SG; AUD

Field pattern | With a profile
--- | ---
`*country*`, `*locale*`, `*region*` | Sample the locale once per record (`locale = profile.sample_locale()`), build `Faker(locale)` from it, and take the country from `country_for_locale(locale)`, so a record's names, address, and country agree.
`*date_of_birth*`, `*dob*` | `profile.sample_date_of_birth()` in realistic mode only (it's PII)
`*customer_type*`, `*party_type*`, `*entity_type*` | `profile.sample_customer_type()`
`*product_code*`, `*product_name*`, `*product_type*` | `profile.sample_product(customer_type)`, filtered by eligibility
`*amount*`, `*balance*`, `*premium*`, `*limit*` | `profile.sample_amount(product)`
`*currency*` | `profile.sample_currency(product)`
`*sector*`, `*industry*` | `profile.sample_sector()`

A profile doesn't lift PII mode. In `safe` mode, every attribute marked `pii: true` (names,
contact details, date of birth, nationality, and so on) keeps its safe-mode placeholder,
even when a profile is active. The profile still shapes the non-PII fields: customer
type, products, amounts, currency, and non-PII country fields.

**Subtypes.** For an entity that `extends` a parent (Person and Company extend Party),
generate one factory per concrete subtype. Each builds the parent's attributes plus its
own, shares the parent's identifier, and inherits the parent's temporal tracking. Don't
generate rows for an abstract parent on its own.

---

## Code Pattern

```python
"""
Synthetic data factory: <Domain> / <scope>
Scope: source | canonical | destination    PII mode: safe | realistic
Profile: none | uk_retail_bank | us_fintech | apac_insurance | custom

WARNING: SYNTHETIC DATA ONLY. Do not use for production data migration.
Dependencies: pip install faker. Copy enterprise_profile.py (if used) from the faker runtime alongside this file.
"""
from __future__ import annotations
import random, uuid
from datetime import date, datetime, timedelta, timezone
from faker import Faker

try:  # copy enterprise_profile.py from the faker runtime to use a profile
    from enterprise_profile import country_for_locale, uk_retail_bank_profile
except ImportError:
    country_for_locale = uk_retail_bank_profile = None

# Enum pools, from the domain's enums
PARTY_STATUS_VALUES = ["Active", "Under Review", "Inactive", "Closed"]

Faker.seed(0)
random.seed(0)
_seq = 0

def _next_seq() -> int:
    global _seq
    _seq += 1
    return _seq


class PartyFactory:
    """Party | independent | slowly_changing | bitemporal | PII: legal_name, date_of_birth"""

    def __init__(self, fake: Faker | None = None, pii_mode: str = "safe", profile=None):
        self.fake = fake or Faker()
        self.pii_mode = pii_mode
        self.profile = profile

    def build(self, with_history: bool = False, **overrides) -> list[dict]:
        seq = _next_seq()
        realistic = self.pii_mode == "realistic"
        locale = self.profile.sample_locale() if self.profile else None
        f = Faker(locale) if locale else self.fake

        # date_of_birth is PII: safe mode keeps the placeholder even with a profile.
        if not realistic:
            dob = date(1970, 1, 1)
        elif self.profile:
            dob = self.profile.sample_date_of_birth()
        else:
            dob = f.date_of_birth(minimum_age=18, maximum_age=80)
        # country is not PII here, so the profile shapes it in either mode.
        country = country_for_locale(locale) if locale else ("AU" if not realistic else f.country_code())

        now = datetime.now(tz=timezone.utc)
        prior_end = now - timedelta(days=random.randint(30, 730))
        prior_start = prior_end - timedelta(days=random.randint(90, 1825))

        current = {
            "party_identifier": str(uuid.uuid4()),
            # Constraint: Legal Name Required
            "legal_name": f.name() if realistic else f"Test Entity {seq:04d}",
            "date_of_birth": dob,
            "country": country,
            "party_status": random.choice(PARTY_STATUS_VALUES),
            "valid_from": prior_end, "valid_to": None, "is_current": True,
            "recorded_at": prior_end, "superseded_at": None,
            **overrides,
        }
        if not with_history:
            return [current]
        prior = {**current, "valid_from": prior_start, "valid_to": prior_end, "is_current": False,
                 "recorded_at": prior_start, "superseded_at": prior_end}
        return [prior, current]

    def batch(self, n: int, with_history: bool = False, **overrides) -> list[dict]:
        return [row for _ in range(n) for row in self.build(with_history, **overrides)]


class DatasetBuilder:
    """Referentially consistent dataset: reference, roots, dependents, associative, events."""

    def __init__(self, fake: Faker | None = None, pii_mode: str = "safe", profile=None):
        self.fake, self.pii_mode, self.profile = fake or Faker(), pii_mode, profile

    def build(self, n_roots: int = 10, with_history: bool = False) -> dict[str, list[dict]]:
        parties = PartyFactory(self.fake, self.pii_mode, self.profile).batch(n_roots, with_history)
        party_ids = [p["party_identifier"] for p in parties if p["is_current"]]
        # Dependent factories take party_ids as their FK pool.
        return {"Party": parties}
```

`examples/Financial Crime/factories.py` is a complete canonical-scope module (Currency,
Party, Account, Transaction) with its integrity spec.

---

## Supporting Runtime

The runtime is stdlib-only. The user copies the files next to the generated module (or
adds `runtime/` to `sys.path`).

File | Purpose
--- | ---
`runtime/integrity_check.py` | FK resolution, not-null, enum membership, PK uniqueness (all rows or current rows), and bitemporal chain coherence (`check_temporal_chain()`)
`runtime/consistency_scenario.py` | Eventual consistency. Define `SourceFeed`s with lags, then `generate_scenario()` and `check_convergence()` against an SLA window. Offer it when sources have different `change_model`s, entities are valid-time or bitemporal, or the user asks about lag or freshness.
`runtime/test_template.py` | A pytest template. Fill in its four `# UPDATE` sections.
`runtime/enterprise_profile.py` | Enterprise profiles (above)

`examples/Financial Crime/consistency_example.py` demonstrates eventual consistency end
to end.

After delivering a module, offer a companion `test_<module>.py` pre-filled with the
domain's integrity and temporal spec. If the domain has a clear industry and no profile
was chosen, offer one.

## Boundaries

- Python only. For DDL, JSON Schema, Parquet, or Cypher, use the generation skills. For
  destination scope, generate those first.
- The only dependencies are `faker`, the stdlib, and the runtime files.
- Enum values come from the domain. If an identifier, enum, `existence`, or `mutability`
  is missing, flag it for Agent Ontology rather than inventing it.
- Every module carries the synthetic-data WARNING, in either PII mode. Realistic data is
  still fictional and must never reach production.
- Synthetic data complements worked examples; it doesn't replace them. Agent Test
  compiles worked examples into behaviour tests.
