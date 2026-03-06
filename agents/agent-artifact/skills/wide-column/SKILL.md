---
name: wide-column
description: Use this skill when the user asks for wide-column reporting schemas, denormalized columnar marts, one-table analytics models, or join-minimized read models from MD-DDL.
---

# Skill: Wide Column Schema Design

Covers translation of MD-DDL conceptual and logical models into denormalized, join-minimized columnar schemas designed for reporting and analytics consumption.

This skill is for the pattern where consumers want a single primary table at a stable grain (usually a "thing that happens") with selected descriptive context from related "things that are".

## Load First

- `../../agent-ontology/skills/entity-modelling/SKILL.md`
- `../../agent-ontology/skills/entity-modelling/conceptual-to-physical-realisation.md`
- `../../agent-ontology/skills/relationship-events/SKILL.md`
- `../dimensional/SKILL.md`
- `../normalized/SKILL.md`
- `../../agent-ontology/skills/standards-alignment/SKILL.md` (mandatory in recognized industry domains)

---

## Core Mental Model

Use two buckets to drive modeling choices:

Concept bucket | Typical MD-DDL signals | Typical physical role
--- | --- | ---
Things that are | `existence: independent`, `mutability: slowly_changing` or `reference` | Descriptive context entities (customer, account, product)
Things that happen | `existence: dependent`, `mutability: append_only` or `immutable`, event-heavy semantics | Driving grain for wide table (transaction, claim event, payment)

Default strategy:
- Pick a driving "thing that happens" grain.
- Pull in selected attributes from related "things that are" where relationship paths are stable and cardinality-safe.
- Optimize for consumer queries, not for update minimality.

---

## Research-Backed Practical Guidance

This skill follows common modern warehousing guidance:

1. Denormalization is usually a read-performance optimization that moves joins from query time to build time.
2. Keep entity grain explicit: a wide table should still represent one core concept per row.
3. Avoid flattening high-churn and high-cardinality relationships blindly.
4. For one-to-many details, prefer selective rollups, capped arrays, or nested structures over row explosion.
5. In platforms that support nested/repeated types (for example BigQuery), nested structs and arrays can reduce join and shuffle costs while preserving hierarchy.

Practical source influences:
- dbt marts guidance (wide, denormalized, entity-grained output models)
- ClickHouse denormalization guidance (join-at-ingest trade-off, avoid high-cardinality flattening)
- BigQuery nested/repeated best practices (hierarchical denormalization without full flattening)

---

## Join Admissibility Rules

Use this matrix before denormalizing a relationship into a wide table.

Relationship shape from driving row | Include strategy | Default decision
--- | --- | ---
1:1 | Inline columns | Include
N:1 from driving row to parent | Inline selected parent columns | Include
1:N from driving row to child | Aggregate child info or nested array/struct | Include selectively
M:N | Bridge or separate child mart; optional aggregate summary only | Do not inline raw child rows
High-cardinality 1:N (hundreds/thousands per row) | Keep separate; add summary stats only | Avoid inline expansion

Important: If inclusion changes row grain, stop and redesign. Wide does not mean grain drift.

---

## Realization Procedure

### 1) Pick and lock grain

Define a grain statement in plain language:

- "One row per Transaction"
- "One row per Claim Event"
- "One row per Payment Instruction"

If the grain is not explicit, do not generate output.

### 2) Map relationship paths

From the driving entity, enumerate all immediate and second-hop relationships. Mark each path with:

- cardinality
- mutability/churn risk
- business value to reporting consumers

### 3) Select projection tiers

Bring attributes into the wide table by priority:

Tier | Include guidance
--- | ---
T1 Core keys and timestamps | Always include identifiers and event time
T2 High-use descriptive context | Include stable attributes used in filtering/grouping
T3 Operational metadata | Include if materially used in reporting operations
T4 Rare or volatile details | Exclude from wide table; expose in companion table or nested field

### 4) Handle one-to-many safely

When the driving row has 1:N children, choose exactly one pattern:

Pattern | When to use
--- | ---
Aggregate columns | Need counts/sums/latest flags only
Nested array/struct | Platform supports nested types and consumers can handle them
Companion child wide table | Child details are frequently queried as first-class rows

Do not duplicate driving rows just to materialize child collections unless the user explicitly wants a row-per-child output.

### 5) Apply temporal correctness

For slowly changing "things that are":

- Join "as of" the event timestamp from the driving row.
- Snapshot attributes into the wide row to make reports historically reproducible.
- Document late-arriving update policy (restate vs forward-fix).

### 6) Define refresh policy

Denormalized wide outputs need explicit rebuild strategy:

- incremental append for immutable event grains
- targeted backfill for changed dimensions
- full refresh window for high-impact historical corrections

---

## MD-DDL-Specific Mapping Guidance

### Existence and Mutability

MD-DDL signal | Wide-column implication
--- | ---
`existence: dependent` + `append_only`/`immutable` | Strong candidate driving grain
`existence: independent` + `reference` | Good candidate for inline descriptive enrichment
`mutability: slowly_changing` | Use as-of joins and snapshot columns
`mutability: frequently_changing` | Include cautiously; consider volatile fields separately
`existence: associative` | Usually preserve as separate structure unless only summary is needed

### Relationships and granularity

- `granularity: atomic` is generally easiest to inline as context columns.
- `granularity: period` often needs validity-window joins and effective date columns.
- `granularity: group` often maps better to aggregated summaries than direct flattening.

### Events

Events are strong drivers for wide tables because they naturally encode "things that happen".

Include event-level attributes plus selected actor/entity context fields needed for common reporting questions.

---

## Example Pattern (Financial Transactions)

Goal: one row per transaction with account and customer context pre-joined.

Input semantics:
- Transaction is the driving "thing that happens".
- Account and Customer are "things that are".
- Typical relationships: Customer 1:N Account, Account 1:N Transaction.

Recommended wide projection:

Column group | Example columns
--- | ---
Transaction core | transaction_id, transaction_timestamp, amount, currency_code, channel
Account context | account_id, account_type, account_status, opened_date
Customer context | customer_id, customer_segment, risk_rating, residency_country
Operational flags | is_high_risk, sanctions_hit_flag, aml_case_id

SQL-shape example (platform-agnostic):

```sql
SELECT
  t.transaction_id,
  t.transaction_timestamp,
  t.amount,
  t.currency_code,
  t.channel,
  a.account_id,
  a.account_type,
  a.account_status,
  a.opened_date,
  c.customer_id,
  c.customer_segment,
  c.risk_rating,
  c.residency_country,
  t.is_high_risk,
  t.sanctions_hit_flag,
  t.aml_case_id
FROM fact_transaction t
LEFT JOIN dim_account a
  ON t.account_id = a.account_id
  AND t.transaction_timestamp >= a.valid_from
  AND (a.valid_to IS NULL OR t.transaction_timestamp < a.valid_to)
LEFT JOIN dim_customer c
  ON a.customer_id = c.customer_id
  AND t.transaction_timestamp >= c.valid_from
  AND (c.valid_to IS NULL OR t.transaction_timestamp < c.valid_to);
```

This pattern keeps transaction grain while reducing common downstream joins.

---

## Platform Notes for Columnar Engines

Engine capability | Recommended shape
--- | ---
Flat-column optimized warehouses | Wide flat columns with controlled duplication
Nested-capable engines | Use STRUCT/ARRAY for bounded 1:N child context
High-ingest analytical engines | Prefer build-time joins and periodic refresh for stable dimensions

When nested structures are used, provide both:
- base wide columns for common BI filtering
- nested details for advanced drill-through

---

## Output Contract

When producing a wide-column schema, always include:

1. Grain statement
2. Attribute inclusion map (source entity attribute -> output column)
3. Join path map with cardinality and temporal join logic
4. Volatility notes (fields intentionally excluded due to churn)
5. DDL or schema contract for requested platform
6. Build strategy (incremental/full refresh/restate policy)
7. Consumer notes (expected query patterns and known trade-offs)
8. Open questions and assumptions

---

## Quality Checklist

Before finalizing:

- [ ] Grain is explicit and unchanged by joins
- [ ] Every included relationship passed admissibility rules
- [ ] M:N relationships are not naively flattened
- [ ] High-cardinality child sets are aggregated or separately modeled
- [ ] SCD/as-of logic is defined for slowly changing context
- [ ] Included columns reflect real reporting use cases
- [ ] Rebuild and correction policy is specified
- [ ] Governance-sensitive fields (PII/classification) are clearly tagged
