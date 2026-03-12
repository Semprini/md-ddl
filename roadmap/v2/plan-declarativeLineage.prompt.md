# Plan: Declarative Lineage and Anomaly Detection

## TL;DR

MD-DDL already encodes data lineage as a declarative model: sources describe
origin systems, transforms describe column-level mappings, entities describe
canonical targets, and data products describe downstream consumers. This makes
traditional lineage tooling — infrastructure crawlers, connector pipelines,
metadata stores — redundant at design time.

The v2 lineage capability is an agent that reads the declared model and looks
for anomalies: gaps, orphans, and inconsistencies in the stated lineage that
would silently break pipelines or produce empty data products.

---

## The Argument

Traditional data lineage tools (Atlas, Collibra, DataHub) are reactive — they
observe what infrastructure is doing and infer lineage from execution. This
works after deployment but is useless at design time and requires standing up
significant infrastructure to get any signal at all.

MD-DDL flips the model. Lineage is declared, not discovered:

- `sources/<system>/source.md` — what systems feed this domain
- `sources/<system>/transforms/<table>.md` — how source columns map to
  canonical attributes
- `entities/<entity>.md` — what the canonical target looks like
- `products/<product>.md` — what is published downstream and to whom

This declarative lineage can be validated by an agent before a single pipeline
is built. Anomalies in the declaration predict failures in deployment.

---

## Anomaly Classes

An anomaly detection agent would look for:

**Orphaned declarations**
- Source declared in `source.md` with no transform files
- Transform file referencing a source table not listed in `source.md`
- Entity referenced in a transform target that doesn't exist in the domain

**Incomplete lineage**
- Entity in the domain with no source mapping (data never arrives)
- Data product referencing an entity with no populated source mapping (product
  can't be produced)
- Event entity with no source or transform establishing when the event would
  fire

**Internal inconsistencies**
- Transform maps to an attribute name that doesn't match any attribute in the
  target entity's YAML block
- Relationship `source:` or `target:` entities exist in the model but neither
  has a source mapping (the relationship can be declared but never populated)

---

## What Needs Building

1. **Agent Lineage** — a new specialist agent with a lineage-review skill that
   scans a domain folder, constructs the declared lineage graph, and reports
   anomalies by class

2. **Lineage model** — a definition of what "complete declared lineage" looks
   like for an entity, a relationship, and a data product (what source mappings
   must exist for each to be considered reachable)

3. **Spec additions** — a new section in the spec (or a `10-Tooling.md`)
   covering the lineage model and what agents can assert about it mechanically
   vs. what requires human judgment

---

## Decisions (Provisional)

- **Agent-driven, not a linter.** Anomaly detection requires understanding
  intent — a missing transform might be deliberate (manual load, seed data).
  Findings are observations the modeler reviews, not hard failures.
- **Domain-scoped.** The agent operates on one domain at a time. Cross-domain
  lineage (source system shared across domains) is a follow-on concern.
- **Complements pre-flight.** Pre-flight checks syntax. Lineage anomaly
  detection checks semantic completeness. Both are Level 1 in spirit but
  lineage operates at a higher abstraction level.

---

## Further Considerations

- How to represent cross-domain source sharing (one source system feeding
  multiple domains)
- Whether a lineage summary should be generated as a machine-readable artifact
  (e.g. a `lineage.json` or a Mermaid graph) as a byproduct of the review
- Integration with data product ODPS manifests — lineage completeness as a
  precondition for generating a valid manifest
