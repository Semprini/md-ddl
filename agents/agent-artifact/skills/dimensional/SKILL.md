---
name: dimensional
description: Use this skill when the user asks for a physical dimensional model, star schema, fact/dimension design, bridge strategy. Also use when deciding how `existence`, `mutability`, and temporal tracking should influence physical realization.
---

# Skill: Physical Dimensional Modelling

Covers how to translate MD-DDL conceptual/logical definitions into dimensional physical design choices (dimension, fact, bridge), including SQL-shape guidance and decision quality checks.

For normalized operational physical designs, use `../normalized/SKILL.md`.

## Load First

- `../../references/generation-semantics.md`: the `existence`, `mutability`, and
  `temporal.tracking` mappings (dimension, fact, bridge; SCD; temporal columns). They
  are not repeated here.
- `../../../agent-ontology/skills/entity-modelling/conceptual-to-physical-realisation.md`:
  ownership vs existence, and many-to-many bridges
- `../../../agent-ontology/skills/standards-alignment/SKILL.md` in industry-standard
  domains, before finalising the physical shape

Dimensional specifics beyond the shared mapping:

- `frequently_changing` attributes on a wide dimension cause SCD churn. Split them into a
  mini-dimension or carry them on the fact.
- `reference` entities become small conformed dimensions, updated only through controlled
  admin changes.
- SCD Type 2 columns are `valid_from`, `valid_to`, and `is_current`. Bitemporal entities
  add the transaction-time pair.

---

## Decision Framework (Must Apply Explicitly)

For each entity and relationship, decide in this order:

1. Conceptual role (master concept, event, or association)
2. `existence` and whether it implies dimension/fact/bridge
3. `mutability` and history strategy
4. temporal tracking and required columns
5. relationship cardinality and whether bridge is required
6. standards/regulatory constraints that force stricter treatment

If a choice conflicts with any previous step, stop and resolve; do not silently continue.

---

## Inheritance Guidance for Dimensional Models

When parent/child entities exist:

- Prefer parent dimension + child extension dimensions when subtypes add meaningful attributes.
- Prefer single dimension with discriminator when subtype differences are shallow.
- Do not duplicate shared parent attributes across multiple child dimensions unless denormalization is explicitly required.
- Preserve surrogate-key lineage: child extension rows should reference parent surrogate key.

Use this quick rule:

Case | Physical preference
--- | ---
Subtypes mostly labels | single `dim_*` + subtype enum/discriminator
Subtypes materially different attributes | parent `dim_*` + child extension tables
Subtypes independent operational lifecycles | separate dimensions + conformed bridge/reference strategy

### Inheritance DDL Patterns (Dimensional)

#### Pattern 1 — Single Dimension with Discriminator

Use when subtypes differ by label or ≤2 attributes. All rows in one dimension.

```sql
CREATE TABLE dim_party (
    party_sk       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    party_bk       VARCHAR(50) NOT NULL,
    party_type     VARCHAR(30) NOT NULL,  -- discriminator
    -- shared attributes
    full_name      VARCHAR(200),
    tax_id         VARCHAR(30),
    -- subtype-specific (nullable for other types)
    date_of_birth  DATE,          -- Individual only
    gender         VARCHAR(10),   -- Individual only
    registration_number VARCHAR(50),  -- Organisation only
    -- SCD2 temporal
    valid_from     TIMESTAMP NOT NULL,
    valid_to       TIMESTAMP,
    is_current     BOOLEAN DEFAULT TRUE
);
```

Fact tables reference `party_sk` directly. The discriminator enables filtering
by subtype without additional joins.

#### Pattern 2 — Parent Dimension + Extension Dimensions

Use when subtypes add ≥3 meaningful attributes. Parent dimension carries shared
attributes and the surrogate key. Extension dimensions carry subtype-specific
attributes with FK to parent SK.

```sql
-- Parent dimension: shared attributes and surrogate key
CREATE TABLE dim_party (
    party_sk       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    party_bk       VARCHAR(50) NOT NULL,
    party_type     VARCHAR(30) NOT NULL,  -- discriminator
    full_name      VARCHAR(200),
    tax_id         VARCHAR(30),
    valid_from     TIMESTAMP NOT NULL,
    valid_to       TIMESTAMP,
    is_current     BOOLEAN DEFAULT TRUE
);

-- Extension dimension: Individual-specific attributes
CREATE TABLE dim_party_individual (
    party_sk       BIGINT PRIMARY KEY REFERENCES dim_party(party_sk),
    date_of_birth  DATE,
    gender         VARCHAR(10),
    nationality    VARCHAR(50),
    marital_status VARCHAR(20)
);

-- Extension dimension: Organisation-specific attributes
CREATE TABLE dim_party_organisation (
    party_sk       BIGINT PRIMARY KEY REFERENCES dim_party(party_sk),
    registration_number VARCHAR(50),
    industry_code  VARCHAR(10),
    incorporation_date DATE,
    legal_form     VARCHAR(30)
);
```

**Rules:**

- Fact tables always reference the parent `dim_party.party_sk`
- Extension dimensions share the parent's SK as their PK and FK
- SCD2 temporal columns live on the parent dimension only
- Extension dimensions do not repeat parent attributes
- When querying, join fact → parent → extension as needed

#### Pattern 3 — Fully Separate Dimensions

Use only when subtypes are operationally independent and never appear in the
same fact table.

```sql
CREATE TABLE dim_individual (
    individual_sk  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    individual_bk  VARCHAR(50) NOT NULL,
    full_name      VARCHAR(200),
    date_of_birth  DATE,
    gender         VARCHAR(10),
    nationality    VARCHAR(50),
    valid_from     TIMESTAMP NOT NULL,
    valid_to       TIMESTAMP,
    is_current     BOOLEAN DEFAULT TRUE
);

CREATE TABLE dim_organisation (
    organisation_sk BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    organisation_bk VARCHAR(50) NOT NULL,
    full_name      VARCHAR(200),
    registration_number VARCHAR(50),
    industry_code  VARCHAR(10),
    valid_from     TIMESTAMP NOT NULL,
    valid_to       TIMESTAMP,
    is_current     BOOLEAN DEFAULT TRUE
);
```

**Rules:**

- Each dimension has independent SK sequences
- Parent attributes are repeated (full denormalization)
- Fact tables reference the specific subtype SK, not a shared parent
- Only use when cross-subtype analysis is not expected

---

## Enum Guidance (Low Cardinality and Physicalization)

Enums are default low-cardinality classification attributes:

- Keep as constrained text columns in the owning dimension/fact when stable and small.
- Promote to separate reference dimension when one or more apply:
  - multilingual labels / metadata required
  - governance ownership independent of entity
  - value lifecycle/versioning needs auditability
  - high reuse across many tables with central stewardship

Avoid over-normalizing every enum into its own table without a clear governance/lineage need.

---

## Relationship Realization Guidance

Relationship pattern | Physical realization
--- | ---
1:N with low volatility | foreign-key reference from child to parent dimension/fact
M:N with relationship semantics | bridge table (effective dates + optional role attributes)
Temporal relationship validity | effective-dated bridge (`valid_from`, `valid_to`, `is_current`)
Event-driven relationship changes | fact/event plus bridge update strategy

If conceptual relationship is owned by source A, preserve that ownership intent in naming and ETL flow (for example, `bridge_customer_account`).

---

## Fact Design Guidance

A table is a fact candidate when it records:

- an event (something happened)
- a measurement at a grain (amount, count, score)
- a periodic snapshot

For each fact, define explicitly:

- grain statement (one row represents what?)
- event/business time column(s)
- conformed keys to dimensions
- additive/semi-additive/non-additive measures
- late-arrival and correction handling policy

---

## Regulatory and Standards Overlays

Before finalizing physical shape:

- Validate retention and historical requirements against regulatory scope.
- Ensure temporal strategy is sufficient for audit reconstruction.
- Ensure sensitive classifications are enforceable in downstream physical design.
- In regulated domains, prefer explicit history over overwrite when obligations require traceability.
