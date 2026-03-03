---
name: physical-dimensional-modelling
description: Use this skill when the user asks for a physical dimensional model, star schema, fact/dimension design, bridge strategy. Also use when deciding how `existence`, `mutability`, and temporal tracking should influence physical realization.
---

# Skill: Physical Dimensional Modelling

Covers how to translate MD-DDL conceptual/logical definitions into dimensional physical design choices (dimension, fact, bridge), including SQL-shape guidance and decision quality checks.

For normalized operational physical designs, use `../physical-3nf-modelling/SKILL.md`.

## Load First

- `../entity-modelling/conceptual-to-physical-realisation.md`
- `../entity-modelling/SKILL.md`
- `../relationship-events/SKILL.md`
- `../standards-alignment/SKILL.md` (mandatory for industry-standard domains)

Use this skill only after domain-level conceptual structure is stable enough to map.

---

## Core Mapping Matrix

### Existence → Physical Candidate

`existence` | Primary physical candidate | Typical shape
--- | --- | ---
`independent` | Dimension | `dim_*` with surrogate key and SCD controls where needed
`dependent` | Fact | `fact_*` row per event/measurement/context occurrence
`associative` | Bridge | `bridge_*` for many-to-many + relationship attributes/effective dates

### Mutability → Storage/History Strategy

`mutability` | Typical dimensional treatment | Notes
--- | --- | ---
`reference` | Small static/conformed dimension | Rarely changes; controlled admin updates
`slowly_changing` | SCD Type 2 style dimension | `valid_from`, `valid_to`, `is_current`
`frequently_changing` | Fact or mini-dimension pattern | Avoid excessive SCD churn in wide dimensions
`append_only` | Fact/event table | Immutable inserts, no in-place updates
`immutable` | Ledger/event-style fact | Strict non-update semantics

### Temporal Tracking → Physical Columns

`temporal.tracking` | Minimum physical expectation
--- | ---
`valid_time` | effective start/end dates/timestamps for business validity
`transaction_time` | record created/superseded timestamps for system capture timeline
`bitemporal` | both valid-time and transaction-time columns
`point_in_time` | event timestamp and ordering surrogate (if needed)

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

---

## Output Contract for Physical Modelling Requests

When producing a physical model proposal or SQL DDL, always include:

- Mapping summary (entity → dim/fact/bridge)
- Justification for each non-obvious mapping
- Temporal strategy summary
- Enum handling strategy summary
- Inheritance strategy summary
- Assumptions and open questions

If user asks for SQL, keep naming deterministic and implementation-ready for requested dialect.
