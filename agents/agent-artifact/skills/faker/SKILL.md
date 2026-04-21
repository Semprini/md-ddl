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

WARNING: SYNTHETIC DATA ONLY. Do not use for production data migration.
Dependencies: pip install faker
"""

from __future__ import annotations
import random, uuid
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from faker import Faker

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
        next_review_date = date.today().replace(
            year=date.today().year + random.randint(0, 1),
            month=random.randint(1, 12),
        )

        current = {
            "party_identifier": str(uuid.uuid4()),
            "legal_name": f.name() if self.pii_mode == "realistic" else f"Test Entity {seq:04d}",
            "party_status": random.choice(PARTY_STATUS_VALUES),
            "next_review_date": next_review_date,
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

```python
class DatasetBuilder:
    """
    Generates a referentially consistent dataset.
    Generation order: root entities first, then dependents, then associative, then events.
    """

    def __init__(self, fake: Faker = None, pii_mode: str = "safe"):
        self.fake = fake or Faker()
        self.pii_mode = pii_mode

    def build(self, n_roots: int = 10, children_per_root: int = 2,
              with_history: bool = False) -> dict[str, list[dict]]:
        root_factory = PartyFactory(fake=self.fake, pii_mode=self.pii_mode)
        roots: list[dict] = []
        for _ in range(n_roots):
            roots.extend(root_factory.build(with_history=with_history))

        root_ids = [r["party_identifier"] for r in roots if r["is_current"]]

        # Build dependent entities using root_ids as FK pool
        # child_factory = ChildFactory(parent_ids=root_ids, ...)

        return {"Party": roots}


if __name__ == "__main__":
    import json
    dataset = DatasetBuilder(pii_mode="safe").build(n_roots=5, with_history=True)
    for name, rows in dataset.items():
        print(f"\n=== {name} ({len(rows)} rows) ===")
        print(json.dumps(rows[0], indent=2, default=str))
```

---

## Handoff

**To DDL skills:** generate DDL first, then use physical column names for destination-scope Faker generation.

**To Agent Ontology:** if primary identifier undeclared, enum missing from enums.md, or existence/mutability absent — flag and defer. Do not invent.

---

## Generation Limitations

- Syntactically valid but untested. Run `python -m py_compile file.py` before use.
- Cross-entity constraints enforced approximately within a single build() call only.
- One-to-one cardinality honored within DatasetBuilder.build() but not across independent factory calls.
- `pii_mode='realistic'` is fictional data. Caller must ensure it never reaches production.
