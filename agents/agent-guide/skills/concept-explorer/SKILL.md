---
name: concept-explorer
description: Use when the user asks what an MD-DDL concept is, how a feature works, why the standard makes a design choice, or how it compares with another tool (ER/UML, dbt, Data Mesh, FHIR, catalogues). Also use for validation and linting, multi-viewpoint reviews, lifecycle and versioning, eventual consistency and null handling, synthetic data and enterprise profiles, and trade-offs such as entity vs enum.
---

# Skill: Concept Explorer

Teach any MD-DDL concept through analogy and progressive depth, as described under
Teach in the core prompt. This skill supplies the analogies, the comparisons, and the
explanations of topics users ask about often.

## Spec References

Load the spec section that matches the question before explaining rules. The stubs in
`references/` pull these in on `{{INCLUDE}}`-aware platforms. Elsewhere, read the spec
file directly.

Section | Covers
--- | ---
`md-ddl-specification/1-Foundation.md` | Principles, document structure, two-layer model, validation and verification
`md-ddl-specification/2-Domains.md` | Domain file, metadata, overview diagram, summary tables, lifecycle
`md-ddl-specification/3-Entities.md` | Entity YAML, attributes, types, constraints, inheritance, temporal tracking
`md-ddl-specification/4-Enumerations.md` | Enum formats and naming
`md-ddl-specification/5-Relationships.md` | Relationship types, cardinality, granularity
`md-ddl-specification/6-Events.md` | Event structure, payload, actor and entity
`md-ddl-specification/7-Sources.md` | Source summaries, change models, transform detail, fan-out
`md-ddl-specification/8-Transformations.md` | Transformation types, expressions, worked examples, fan-in
`md-ddl-specification/9-Data-Products.md` | Product classes, declaration, masking, SLA
`md-ddl-specification/10-Adoption.md` | Adoption metadata and baselines

---

## Analogies

Pick the column that matches the user's background.

MD-DDL concept | ER / UML | dbt / SQL | Data Mesh | FHIR | Governance
--- | --- | --- | --- | --- | ---
**Entity** | ER entity, UML class | Model, table | Domain aggregate | Resource (Patient, Encounter) | Governed data asset
**Attribute** | Column, field | Column | Property | Resource element (`Patient.name`) | Classified data element
**Enum** | Lookup / code table | Seed, static reference | Reference data | ValueSet, CodeSystem | Controlled vocabulary
**Relationship** | ER relationship, FK | `ref()`, join | Cross-aggregate reference | Reference type | Lineage link
**Event** | (no ER equivalent) | CDC event, incremental model | Domain event | AuditEvent, Provenance | Audit trail trigger
**Domain** | Subject area, schema | Project, package | Bounded context | Implementation Guide | Catalogue data domain
**Source** | (none) | Source, raw table | External feed | Integration endpoint | System of record
**Transformation** | (none) | SQL expression, staging model | Mapping rule | ConceptMap | ETL specification
**Worked Example** | (none) | Unit test `given`/`expect` | Contract test | Example instance | Control test evidence
**Data Product** | (none) | Exposure | Data product, data contract | (none) | Published data asset
**Attribute Mapping** | (none) | Column-level lineage | Field-level contract | ConceptMap | Attribute provenance
**Version / Lifecycle** | Migration schema version | Model versions, deprecation | Contract versioning | Resource version history | Change control record
**Reconciliation** | Schema compare | Generated vs deployed relation | Contract compatibility check | (none) | Control attestation
**Eventual Consistency** | (none) | Incremental model with overlapping windows | Product freshness window | (none) | Freshness SLA and convergence audit trail

## Showing Structure

When the user wants more than the summary, show the concept's structure with a short
annotated excerpt from a real example (`examples/`; the coverage matrix in
`examples/README.md` shows which example exercises which feature). Don't invent an
example when a real one exists. For each element, cover what it is, what goes wrong if
it's missing or wrong, and the common choices. Rules come last and only on request:
state the rule, its reason, and what it means for the user's work.

---

## Comparisons

Structure a comparison around what the user cares about.

**ER / UML.** Same: entities, attributes, relationships, inheritance. Different:
Markdown-native and diff-friendly, governance built in, events first-class, no GUI.
Added: sources, transformations, data products, and compliance in one model.

**dbt.** Same: text-based and version-controlled. Different: MD-DDL defines what the
data *means*; dbt defines how to build it. Complementary: Agent Artifact generates a dbt
project per data product from the organisation's template, and Agent Test compiles
worked examples into dbt unit tests. The same project runs in two tiers: locally on
dbt-core + DuckLake for fast unit and data tests, then in dbt Cloud on the warehouse
(Snowflake by default) for everything plus masking, grants, and source freshness. Only
the profile differs.

**Data Mesh / data contracts.** Same: domain ownership and data as a product. Different:
MD-DDL is a concrete language with formal product declarations (schema type,
governance, masking, SLA) that drive generation, not a conceptual framework.

**FHIR.** FHIR is a healthcare interoperability standard; MD-DDL is domain-agnostic.
Entities align to FHIR resources and enums to ValueSets, and MD-DDL adds governance,
temporal tracking, source mapping, and generation.

**Catalogues (Collibra, Alation).** Catalogues index existing data; MD-DDL defines data
from the start, with governance in the model. ODPS manifests can publish products to a
catalogue.

---

## Validation and Linting

Load `md-ddl-specification/1-Foundation.md § Validation Model`, and
`guides/validation-tooling.md` for detail.

MD-DDL uses two tiers:

1. **Pre-flight checks.** These are mechanical and implemented by `md-ddl lint
   <domain-folder>`. They cover what breaks AI interpretation (YAML and Mermaid syntax,
   links, entity references, the domain `version`) and what the model contradicts
   about itself (diagram, tables, and YAML disagreeing).
2. **Agent-driven review.** This covers convention, quality, and domain fitness: Agent
   Ontology's domain-review and Agent Governance's compliance-audit skills.

Explain why the linter stops at tier 1 using the guide's five validation levels: only
syntax is mechanically decidable without false positives. Convention and quality need
context, and domain fitness needs people. Vocabulary deviations (`phi` for `pii`) are
signal, not errors. Agents work with them and note them as possible spec contributions.

Validation checks the model. **Verification** checks what's generated from it
(Foundation § Verification of Generated Artefacts): worked examples become unit tests,
constraints become data tests, and SLAs become integration tests. That's Agent Test.

---

## Multi-Viewpoint Reviews

For "second opinion" or stress-testing requests on any artifact: define the target and
question, choose three to five viewpoints with different concerns, run each as an
independent pass that ends with "what I cannot evaluate", then consolidate agreements,
disagreements, and blind spots into a prioritised action list with owners.

Viewpoint | Question
--- | ---
Structural | Is it coherent and mechanically sound?
Adversarial | How could it fail in production?
Stakeholder | Would practitioners actually use it?
Operator | Can it be run and maintained safely?
Governance | Would it satisfy audit and policy obligations?
New user | Can someone new follow it?

Route execution: MD-DDL standard, agents, or examples → `review-md-ddl`; a domain model →
Agent Ontology (domain-review) and Agent Governance (compliance-audit); architecture or
product decisions → Agent Architect.

---

## Lifecycle and Evolution

Load `2-Domains.md` and `9-Data-Products.md`. The key point: the authoritative diff is at
the **logical** layer. Regenerated physical output can differ without any change in meaning.

The change workflow:

1. Change the model.
2. Classify the change: breaking, additive, or corrective.
3. Bump the version.
4. Record the change in `LIFECYCLE.md` with its change manifest.
5. Regenerate.
6. Reconcile against deployed state, using the manifest to separate intended change
   from regeneration noise.

Products may lag their domain (a `Draft` product in an `Active` domain) but never lead it.

Analogy: the model is source code, `LIFECYCLE.md` is typed release notes, and
reconciliation compares the new build with what's running.

Route: domain versioning → Agent Ontology; product versioning → Agent Architect;
generated vs deployed → Agent Artifact (reconciliation); lifecycle audit → Agent Governance.

---

## Eventual Consistency

Load `7-Sources.md` and `9-Data-Products.md`. Agent Architect's architecture skill has
the full architectural treatment. Here, teach what it is and how to express it.

**Summary.** Sources update a canonical entity with different lags. The product declares
the window within which the entity converges. Bitemporal tracking makes the lag
measurable: `valid_from` is when something became true, `recorded_at` is when the
canonical system learned it, and the gap between them is the lag.

**Analogies:** Kafka consumer groups at different offsets (engineer); DNS propagation
within a TTL (architect); a master record whose fields different feeds update
(steward); CDC fan-out at different cadences (integration).

**How it's declared:**

1. Each source's `change_model` sets its expected lag.
2. Bitemporal tracking on the entity records when each update arrived.
3. The product's `sla.freshness` is the convergence window.
4. The product declares `consistency` (posture and null strategy).
5. Fan-in worked examples with `interim` states pin what a partly converged instance
   looks like.

**The null problem.** Mid-convergence, some attributes are null because they haven't
arrived yet, not because they are genuinely empty. That matters in three places:

- **Storage.** Parquet and Arrow can't tell the two kinds of null apart.
- **Transport.** JSON, Avro, and Protobuf each handle "absent" differently; only
  Protobuf's `hasField()` distinguishes it cleanly.
- **DDL.** A hard `NOT NULL` blocks partial rows.

The strategies are:

- `nullable-staging`: a nullable base table, with a converged view for consumers (the
  usual choice)
- `reject-partial`: effectively strong consistency
- `nullable-final`: consumers handle nulls themselves

**When not to use it.** Real-time fraud decisioning, payment authorisation, and
sanctions hard-stops, where acting on stale data is the failure.

**Validation:** `agents/agent-artifact/skills/faker/runtime/consistency_scenario.py`,
the runnable `examples/Financial Crime/consistency_example.py`, and Agent Test for
fan-in examples.

---

## Synthetic Data and Enterprise Profiles

Agent Artifact's faker skill generates Python Faker factories from entity definitions.
They produce referentially consistent, PII-safe datasets with correct temporal
patterns. An optional **enterprise profile** weights the generated values toward the
enterprise's real geography, age mix, customer types, products, and value ranges. It
helps when data must look believable to stakeholders (demos, UAT). It doesn't matter
when only structural validity is being tested.

Your role is to help the user answer the profile questions before handing off.
Ask them conversationally, and rough answers are fine:

Question | Drives
--- | ---
Industry and primary market? | Which pre-built profile to start from
Geographies served, in rough proportions? | Per-record Faker locale; country and region fields
Customer age distribution (rough bands)? | Date of birth
Customer type mix (individual, corporate, SME)? | Party type and product eligibility
Main products, which customer types they're restricted to, typical values? | Product, amount, balance, premium, currency

Then hand off to Agent Artifact (faker skill) with the scope (source, canonical, or
destination), PII mode, cardinality, and these answers. Its skill lists the pre-built
profiles and how each field is influenced.

---

## Design Trade-offs

Present both options and the criteria. Let the user decide.

- **Entity vs enum.** Own attributes, relationships, or lifecycle → entity. A fixed set of
  labels → enum. Unsure → start as an enum and promote it if it grows.
- **Entity vs attribute.** Can it exist on its own → entity. Always a property of
  something else → attribute.
- **Canonical vs bounded context.** Must mean the same everywhere → canonical. Has
  meaningfully different attributes per context → bounded context.
- **Inheritance vs discriminator.** Subtypes add attributes or constraints →
  inheritance. Just a label → discriminator attribute.

For deeper analysis, load the spec section or route to Agent Ontology's entity-modelling skill.
