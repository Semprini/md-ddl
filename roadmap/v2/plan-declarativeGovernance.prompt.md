# Plan: Declarative Governance

## TL;DR

MD-DDL already encodes governance as a declarative model: sources describe
origin systems, transforms describe column-level mappings, entities describe
canonical targets with governance metadata, relationships and events define
data behaviour, and data products describe downstream consumers. This makes
traditional governance tooling — lineage crawlers, data quality rule engines,
access control catalogues, metadata stores — redundant at design time.

The v2 governance capability is a suite of agents that read the declared model
and assert what can be known mechanically: lineage anomalies, data quality
obligations, access control expectations, and compliance posture — all before
a single pipeline is built.

---

## The Argument

Traditional data governance tools are reactive — they observe what
infrastructure is doing and infer governance posture from execution. This
works after deployment but requires standing up significant infrastructure,
produces stale metadata, and catches problems after data has already moved.

MD-DDL flips the model. Governance is declared, not discovered:

- `sources/<system>/source.md` — what systems feed this domain
- `sources/<system>/transforms/<table>.md` — how source columns map to
  canonical attributes
- `entities/<entity>.md` — canonical target with governance, retention,
  classification, and PII metadata
- `products/<product>.md` — what is published downstream and to whom
- Relationships, events, and enums — data behaviour and valid states

Every declared element is a governance assertion. Agents can validate
completeness and consistency of those assertions before deployment, and flag
anomalies that predict governance failures.

---

## Governance Domains in Scope

### Lineage

Declared lineage can be validated for completeness and internal consistency.
An anomaly here predicts a pipeline that will silently fail or produce empty
data products.

**Anomaly classes:**

*Orphaned declarations*
- Source declared in `source.md` with no transform files
- Transform file referencing a source table not listed in `source.md`
- Entity referenced in a transform target that doesn't exist in the domain

*Incomplete lineage*
- Entity in the domain with no source mapping (data never arrives)
- Data product referencing an entity with no populated source mapping
- Event entity with no source or transform establishing when it would fire

*Internal inconsistencies*
- Transform maps to an attribute name that doesn't match any attribute in the
  target entity's YAML block
- Relationship entities exist in the model but neither has a source mapping
  (the relationship can be declared but never populated)

### Data Quality

Governance metadata on entities and attributes implies data quality
obligations. An agent can surface what quality rules are implied by the model
and flag where quality obligations are declared but have no enforcement path.

*To be planned in detail.*

### Access Control

Classification, PII, and retention metadata on entities implies access control
requirements. An agent can assert what access tiers each entity requires and
flag inconsistencies (e.g. a high-classification entity published in a
low-governance data product).

*To be planned in detail.*

### Compliance Posture

Regulatory scope declared on a domain implies a set of obligations. Agent
Regulation already handles this for individual audits. A declarative governance
agent would extend this to portfolio-level: which domains are compliant,
which have gaps, and which have conflicting obligations across domain
boundaries.

*To be planned in detail.*

---

## What Needs Building

1. **Agent Governance** — a new specialist agent (or an extended Agent
   Regulation) with skills covering each governance domain above

2. **Governance model** — a definition of what "complete declared governance"
   looks like for an entity, a relationship, and a data product

3. **Spec additions** — coverage of the governance model and what agents can
   assert mechanically vs. what requires human judgment

---

## Decisions (Provisional)

- **Agent-driven, not a linter.** Governance anomaly detection requires
  understanding intent. Findings are observations, not hard failures.
- **Domain-scoped first.** Each capability operates on one domain at a time.
  Portfolio-level and cross-domain views are follow-on.
- **Complements pre-flight.** Pre-flight checks syntax. Governance anomaly
  detection checks semantic completeness and obligation coverage.

---

## Further Considerations

- How to represent cross-domain source sharing (one source system feeding
  multiple domains)
- Whether a governance summary should be generated as a machine-readable
  artifact (e.g. JSON or a Mermaid graph) as a byproduct of review
- Integration with data product ODPS manifests — governance completeness as a
  precondition for generating a valid manifest
- Relationship to Agent Regulation — whether governance anomaly detection is
  a new agent or an extended capability of the existing regulation agent
