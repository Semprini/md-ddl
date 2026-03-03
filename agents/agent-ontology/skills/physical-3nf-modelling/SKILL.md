---
name: physical-3nf-modelling
description: Use this skill when the user asks for a normalized operational model, practical/pragmatic 3NF, OLTP schema design, or non-dimensional physical outputs. Also use when producing database DDL, JSON Schema, or Parquet-oriented schema contracts from MD-DDL.
---

# Skill: Physical 3NF Modelling

Covers translation of MD-DDL conceptual/logical artifacts into practical third normal form (3NF) physical designs for operational and integration use cases.

This is **pragmatic/practical 3NF**:

- normalization is the baseline,
- selective duplication is acceptable when it materially improves usability, readability, or operational performance,
- every deviation from strict 3NF is intentional and documented.

## Load First

- `../entity-modelling/SKILL.md`
- `../entity-modelling/conceptual-to-physical-realisation.md`
- `../relationship-events/SKILL.md`
- `../standards-alignment/SKILL.md` (mandatory in recognized industry domains)

---

## Core Mapping Rules

### Entity Realization

`existence` | Typical 3NF realization | Notes
--- | --- | ---
`independent` | Core table | Stable business object with primary key
`dependent` | Child/transaction table | Exists in context of parent or process
`associative` | Intersection table | Resolves many-to-many and carries link attributes

### Mutability and Temporal Realization

`mutability` | Practical relational strategy
--- | ---
`reference` | Reference table with controlled updates and audit metadata
`slowly_changing` | Versioned table or history companion table
`frequently_changing` | Current-state table with optional change log/audit table
`append_only` | Append-only transaction/event table
`immutable` | Immutable ledger/event table

`temporal.tracking` | Minimum column expectation
--- | ---
`valid_time` | business valid-from / valid-to
`transaction_time` | recorded-at / superseded-at
`bitemporal` | both valid-time and transaction-time sets
`point_in_time` | event timestamp (+ sequence when needed)

---

## Practical 3NF Heuristics

Use these to decide when selective denormalization is acceptable.

### Keep strict normalization when

- update anomalies are likely,
- values are high-volatility and centrally governed,
- data integrity risk outweighs query convenience.

### Allow pragmatic duplication when

- duplicated values are low-volatility descriptors,
- duplication removes repeated multi-join burden in dominant operational queries,
- duplicated fields are clearly designated as derived/cache fields,
- a reconciliation path exists (source-of-truth column/table remains clear).

When duplicating, document:

- authoritative source attribute,
- synchronization approach,
- acceptable staleness tolerance,
- integrity checks.

---

## Inheritance Guidance (3NF)

Pattern | When to use
--- | ---
Single-table with discriminator | shallow subtype differences, low null-bloat risk
Class-table inheritance (parent + child tables) | meaningful subtype-specific attributes and constraints
Concrete table per subtype | rare; use only when subtypes are operationally independent

Default preference: parent table + subtype extension tables for clear semantics and maintainability.

---

## Enum and Low-Cardinality Guidance

- Keep enums as constrained columns (check constraints or domain types) when stable and local.
- Promote enums to lookup/reference tables when:
  - values carry metadata,
  - values are shared broadly,
  - values are managed by separate stewardship,
  - value lifecycle/history must be auditable.

Avoid creating lookup tables for every small enum by default.

---

## Relationship Realization Guidance

Relationship shape | Practical relational realization
--- | ---
1:N | foreign key in child table
M:N | junction/intersection table (plus effective dates if temporal)
Temporal relationship | effective-dated junction or relationship history table
Relationship with heavy semantics | explicit relationship table as first-class object

Foreign keys are expected in 3NF physical outputs even though conceptual MD-DDL avoids FK attributes in logical entity YAML.

---

## Output Targets

For physical-output requests, support one or more of the following targets:

1. **Database DDL** (dialect-specific)
   - PostgreSQL, SQL Server, Snowflake, Databricks SQL (as requested)
   - include keys, FKs, constraints, indexes, and naming conventions

2. **JSON Schema**
   - one schema per logical entity/table contract
   - include required fields, type constraints, enums, and format hints
   - include relationship references via IDs/keys where applicable

3. **Parquet-oriented schema contracts**
   - define field names, logical/physical types, nullability
   - partitioning recommendations for large event/transaction tables
   - evolution notes (additive vs breaking changes)

If user requests “generate all,” provide consistent naming and field compatibility across all targets.

---

## Decision Checklist

Before finalizing a pragmatic 3NF design, confirm:

- [ ] Table grain and PK are explicit for every table
- [ ] FK paths reflect conceptual relationships
- [ ] Denormalization decisions are intentional and documented
- [ ] Temporal columns align with declared tracking semantics
- [ ] Enum handling rationale is explicit (column constraint vs lookup table)
- [ ] Inheritance strategy is selected and justified
- [ ] Regulatory retention/audit requirements are reflected
- [ ] Output artifacts are consistent across requested targets (DDL/JSON/Parquet)

---

## Output Contract

When returning a pragmatic 3NF design, include:

- mapping summary (entity/relationship → table[s])
- strict-vs-pragmatic decisions list
- assumptions and open questions
- generated artifacts in requested format(s): DDL, JSON Schema, Parquet schema contract
