# Generation Semantics — Mapping MD-DDL Vocabulary to Physical Structures

How Agent Artifact interprets the intent vocabularies of the MD-DDL specification when
generating physical artifacts. The spec defines what each value *means*; this reference
defines what the generating agent *does* with it. Load alongside the generation skill
(dimensional, normalized, wide-column, knowledge-graph) for the target output.

## Entity: `existence`

Value | Generation behaviour
--- | ---
`independent` | Candidate dimension in dimensional models; standalone table in normalized models
`dependent` | Candidate fact in dimensional models; child table with owning-side FK in normalized models
`associative` | Bridge table in dimensional models; junction/association table in normalized models

## Entity: `mutability`

Value | Generation behaviour
--- | ---
`immutable` / `append_only` | Belongs at the centre of a star; insert-only physical patterns, no update paths
`slowly_changing` | Apply SCD logic (typically Type 2) in dimensional targets; history table or effective-dating in normalized targets
`frequently_changing` | Current-value storage; history only if temporal tracking demands it
`reference` | Small lookup table; seeded/managed data pattern

## Entity: `temporal.tracking`

Value | Generation behaviour
--- | ---
`valid_time` | Adds effective/expiration date columns; supports point-in-time queries
`transaction_time` | Adds created/superseded timestamps; immutable records
`bitemporal` | Adds both sets of columns; full temporal reconstruction
`point_in_time` | For events — single timestamp, immutable

## Self-Referential Relationships

Self-referential relationships generate a bridge/association table — even at
one-to-many cardinality — to avoid a self-referencing FK on the entity's own primary
key column:

Cardinality | Physical pattern
--- | ---
`many-to-many` | Bridge table with `source_[pk]`, `target_[pk]`, and `relationship_attributes` columns
`one-to-many` (hierarchy) | Bridge table preferred; adjacency list (parent FK on entity) is acceptable for shallow hierarchies where the generation skill supports it explicitly
Any | Unbounded recursion depth is the default; document when depth is bounded and recommend recursive CTE query patterns in platform-specific notes

Directionality is preserved by generating two FK columns pointing to the same entity
table:

- `source_[entity_identifier]` — FK referencing the source instance
- `target_[entity_identifier]` — FK referencing the target instance

For a Party with identifier `Party Identifier`, the bridge table contains
`source_party_identifier` and `target_party_identifier`. For bidirectional
relationships where direction is not meaningful (e.g., "sibling of"), document that
either column may be treated as the source.

## Source: `change_model`

The `change_model` declared on a source guides the pipeline pattern to generate:

Value | Generated pipeline pattern
--- | ---
`real-time-cdc` | Streaming pipeline
`event-driven` | Event consumer
`batch-daily` | Scheduled ETL
`batch-intraday` | Scheduled ETL with frequency
`api-poll` | API ingestion job
`manual` | Manual load template

## Transformations

Transformation definitions ([Section 8](../../../md-ddl-specification/8-Transformations.md)) are used to generate:

- **ETL / ELT logic** — SQL `SELECT` statements, dbt models, or Spark transformations depending on the target platform
- **Lineage graph edges** — source field → transformation → domain attribute nodes in the Knowledge Graph
- **Data quality test stubs** — one test per transformation, asserting the target attribute is non-null after the transformation runs (override with `quality_check: false` on the transformation if the null case is valid)
- **Source-to-domain mapping documentation** — a human-readable crosswalk table per entity, generated from all inline and named source mappings

## Data Product: `schema_type`

The `schema_type` on a data product selects the generation skill:

`schema_type` value | Skill | Output
--- | --- | ---
`normalized` | `skills/normalized/SKILL.md` | DDL, JSON Schema, Parquet contract
`dimensional` | `skills/dimensional/SKILL.md` | Star schema DDL
`wide-column` | `skills/wide-column/SKILL.md` | Denormalized table DDL
`knowledge-graph` | `skills/knowledge-graph/SKILL.md` | Cypher DDL

For domain-aligned products, read the canonical entity detail files for attributes,
types, and constraints. For consumer-aligned products, use the product's logical model
diagram and attribute mapping tables as the generation input — the product defines its
own structure. In both cases, apply the product's `governance` and `masking` metadata
as constraints on the generated artifacts.
