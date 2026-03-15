# Model-Driven Generation

Covers the model as source of truth, automated generation of schemas and
infrastructure from the canonical model, and the operational-to-analytics
transformation pattern.

## Source Material

{{INCLUDE: ../../../../../references/architecture/2021-07-07_model-driven-generation.md}}

{{INCLUDE: ../../../../../references/architecture/2021-04-05_automated-operational-analytics-transform.md}}

## Key Concepts

- **Model as Source of Truth** — The MD-DDL model is the authoritative definition
  of data semantics. Physical schemas, API contracts, and infrastructure are generated
  from it, not hand-crafted independently.
- **Automated Op-to-Analytics Transform** — A recursive traversal algorithm that walks
  the entity graph from a starting entity back through its relationships to generate
  denormalised analytical schemas automatically. The model drives the denormalisation
  logic — no manual ETL design required.
- **Metadata-Driven Denormalisation** — Entity existence (independent/dependent),
  mutability, and relationship cardinality determine how operational data is flattened
  into analytical wide-column formats.

## Relevant Tenets

- Tenet 4: Model for business semantics
- Tenet 6: Use polyglot persistence
- Tenet 7: Embrace small, regular change
- Tenet 11: Canonical models + key mapping
