---
name: concept-explorer
description: Use this skill when the user asks "what is [concept]", "how does [feature] work", "explain [section]", "compare MD-DDL to [tool]", "why does MD-DDL [design choice]", or any question about a specific part of the standard. Also use when the user wants to understand the reasoning behind a design decision or the trade-offs between alternatives (entity vs enum, canonical vs bounded context, etc.). Also use when the user asks about "linting", "validation", "conformance checking", "why no linter", "how do I check my model", "is there a validator", or any question about how MD-DDL enforces or checks correctness. Also use for eventual consistency, strong consistency, consistency posture, propagation lag, freshness SLA, convergence, null handling, partial rows, NOT NULL constraints under eventual consistency, storage format null semantics (Parquet, Avro, Protobuf), transport protocol null handling, how to model or validate eventual consistency in MD-DDL.
---

# Skill: Concept Explorer

Covers interactive teaching of any MD-DDL concept — entities, relationships, events,
enums, domains, sources, transformations, data products, and governance metadata.
Teaches through analogy, progressive depth, and guided self-discovery.

## Spec References

Load the canonical spec section in `md-ddl-specification/` that matches the
user's question. Reference stubs in `references/` document dependencies for
`{{INCLUDE}}`-aware platforms — do not rely on the stub content alone.

Reference | When to load
--- | ---
`md-ddl-specification/1-Foundation.md` (stub: `references/foundation-spec.md`) | Core principles, document structure, two-layer model
`md-ddl-specification/2-Domains.md` (stub: `references/domains-spec.md`) | Domain file format, metadata, overview diagrams, summary tables
`md-ddl-specification/3-Entities.md` (stub: `references/entities-spec.md`) | Entity YAML, attributes, types, constraints, inheritance
`md-ddl-specification/4-Enumerations.md` (stub: `references/enumerations-spec.md`) | Enum formats, naming, dictionary vs simple list
`md-ddl-specification/5-Relationships.md` (stub: `references/relationships-spec.md`) | Relationship types, cardinality, granularity, constraints
`md-ddl-specification/6-Events.md` (stub: `references/events-spec.md`) | Event structure, payload, temporal rules, actor/entity
`md-ddl-specification/7-Sources.md` (stub: `references/sources-spec.md`) | Source file format, change models, domain feed tables
`md-ddl-specification/8-Transformations.md` (stub: `references/transformations-spec.md`) | Transformation types, expression language, mapping rules
`md-ddl-specification/9-Data-Products.md` (stub: `references/dataproducts-spec.md`) | Data product classes, declaration, governance, masking

---

## Teaching Protocol

Follow this sequence for every concept question. Adjust depth based on user signals.

### Step 1 — Anchor to the Familiar

Before explaining the MD-DDL concept, connect it to something the user already knows.
Use the archetype from the core prompt to select the right analogy:

MD-DDL Concept | ER / UML analogy | dbt / SQL analogy | Data Mesh analogy | FHIR analogy | Governance analogy
--- | --- | --- | --- | --- | ---
**Eventual Consistency** | — | Incremental model with overlapping refresh windows | Data product SLA / freshness window | — | Freshness SLA declaration; convergence audit trail
**Entity** | ER entity, UML class | dbt model, table | Domain aggregate | FHIR Resource (Patient, Encounter) | Governed data asset
**Attribute** | Column, field | Column in model | Property | Resource element (e.g. `Patient.name`) | Data element with classification
**Enum** | Lookup table, code table | Seed file, static reference | Reference data | ValueSet, CodeSystem | Controlled vocabulary
**Relationship** | ER relationship, FK | ref() in dbt, join | Cross-aggregate reference | FHIR Reference type | Lineage link
**Event** | — (no direct ER equivalent) | CDC event, incremental model | Domain event | FHIR AuditEvent, Provenance | Audit trail trigger
**Domain** | Subject area, schema | Project, package | Bounded context | Implementation Guide | Data domain in catalogue
**Source** | — | Source in dbt, raw table | External system feed | Integration endpoint | System of record
**Transformation** | — | dbt transformation, SQL expression | Mapping rule | ConceptMap | ETL specification
**Data Product** | — | Exposure in dbt | Data product / data contract | — | Published data asset
**Lineage** | — | Source/ref lineage in dbt | Data provenance chain | — | Data flow audit trail
**Logical Model** | Logical ER diagram | — | Product schema contract | — | Governed data structure
**Attribute Mapping** | — | Column-level lineage | Field-level data contract | ConceptMap | Attribute provenance
**Version / Lifecycle** | Schema version in migration tool | dbt project version, model deprecation | Domain version, contract versioning | Resource version history | Change control record
**Change Manifest** | Change log with typed impacts | dbt `state:modified` selector | Contract change record | — | Audit change register
**Reconciliation** | Schema compare tool | Compare generated model to deployed relation | Contract compatibility check | — | Control attestation compare

> "In ER modelling, you would call this an entity with attributes. In MD-DDL, it is
> the same idea — but defined in Markdown with YAML blocks, version-controlled, and
> AI-readable."

### Step 2 — Two-Sentence Summary

Give a concise definition. Do not quote the spec verbatim — rephrase for clarity.

Examples:

- **Entity:** "An entity represents a distinct business concept — something your
  organisation needs to identify, describe, and track over time. In MD-DDL, each
  entity has a name, attributes with types and constraints, and metadata about
  how it behaves (mutable or immutable, independent or dependent)."

- **Relationship:** "A relationship connects two entities and describes how they
  relate in the business domain — who owns what, who participates in what. MD-DDL
  captures the cardinality, whether it is identifying, and what attributes belong
  to the relationship itself."

- **Data Product:** "A data product declares what data is published, for whom, in
  what shape, and under what governance rules. Domain-aligned products are projections
  of the canonical model with lineage to source system tables. Consumer-aligned
  products define their own logical model — with attribute-level mapping back to
  canonical entities — and never source from source systems directly."

### Step 3 — Check Understanding

After the summary, check before going deeper:

> "Does that match how you think about [concept]? Or would you like me to go into
> the structure and rules?"

If the user wants more depth, proceed to Step 4. If they are satisfied, stop or
move to their next question.

### Step 4 — Structure and Syntax

Show the concept's MD-DDL structure with a brief, annotated example. Use the
examples from `examples/Simple Customer/` or `examples/Financial Crime/` where
possible — do not invent examples when real ones exist.

For each structural element, explain:

- **What it is** — the field name and its purpose
- **Why it matters** — what goes wrong if it is missing or wrong
- **Common choices** — the typical values and when to use each

### Step 5 — Rules and Edge Cases

Only reach this level if the user asks for it or hits a specific edge case.
Load the relevant spec reference stub and present the applicable rules with
context:

> "The spec says [rule]. The reason is [rationale]. In practice, this means
> [implication for what the user is doing]."

### Step 6 — Try It Yourself

Invite the user to apply the concept to their own domain:

> "Describe a concept from your domain and I will show you how it would look
> in MD-DDL."

When the user describes something, sketch it in MD-DDL as a **demonstration** —
mark it clearly as an illustration, not a production artifact. Then discuss:

- Does this capture the concept correctly?
- What would you change?
- Are there edge cases or alternatives we should consider?

If the user is ready to create production artifacts, transition to Navigate mode
and hand off to Agent Ontology.

---

## Comparing MD-DDL to Other Tools

When a user asks "how does MD-DDL compare to [tool]", structure the comparison around
what they care about most:

### vs ER Diagrams / UML

- **Same:** Entities, attributes, relationships, inheritance
- **Different:** Markdown-native (version-controlled, diff-friendly); governance
  metadata built in; events as first-class concepts; AI-agent-friendly structure;
  no GUI dependency
- **Added value:** Source mappings, transformations, data products, regulatory
  compliance — all in one model

### vs dbt

- **Same:** Text-based, version-controlled, describes data
- **Different:** MD-DDL is the *logical* model; dbt is the *physical* transformation
  layer. MD-DDL defines *what the data means*; dbt defines *how to build it*
- **Complementary:** Agent Artifact can generate dbt-compatible output from MD-DDL
  data products

### vs Data Mesh / Data Contracts

- **Same:** Domain ownership, data-as-a-product thinking, consumer focus
- **Different:** MD-DDL is a concrete modelling language with structured syntax, not
  a conceptual framework. Data products in MD-DDL have formal declaration syntax
  with schema type, governance, masking, and generation rules
- **Added value:** MD-DDL provides the *implementation* of Data Mesh principles in a
  format that drives automated generation

### vs FHIR

- **Same:** Structured data definitions, coded concepts, resource types
- **Different:** FHIR is a healthcare interoperability standard; MD-DDL is a
  domain-agnostic modelling language. MD-DDL adds governance, temporal tracking,
  source mapping, and physical generation that FHIR does not cover
- **Complementary:** MD-DDL entities align to FHIR resources via standards alignment;
  enums align to ValueSets; the model adds a semantic governance layer above FHIR

### vs Data Catalogues (Collibra, Alation)

- **Same:** Metadata management, ownership, classification
- **Different:** Catalogues index existing data; MD-DDL *defines* data from the
  start. Governance metadata lives in the model, not in a separate system
- **Complementary:** MD-DDL data product manifests (ODPS) can publish to catalogues

---

## Explaining the Validation Model

When a user asks about linting, validation, conformance checking, or why MD-DDL has no traditional linter, explain the two-tier model clearly. Load `md-ddl-specification/1-Foundation.md` (stub: `references/foundation-spec.md`) to access the normative definition.

### Core explanation to give

MD-DDL uses a **two-tier validation model**:

1. **Mechanical pre-flight checks** — syntax-level only. Five checks: YAML syntax, Mermaid syntax, internal link integrity, entity reference consistency, and domain version field. These are binary (broken or not broken) and have no exceptions.

2. **Agent-driven quality review** — everything above syntax. Structure, convention, governance completeness, domain fitness. This is handled by Agent Ontology's domain-review skill and Agent Governance's compliance-audit skill, because these concerns require context and judgment that no rule engine can provide.

### Why MD-DDL doesn't have a traditional linter

Use this 5-level categorisation to explain why each level is — or isn't — mechanically checkable:

Level | Category | Example | Mechanically checked?
--- | --- | --- | ---
1 | Syntax | YAML parses, links resolve | Yes — no wiggle room; broken syntax corrupts agent interpretation
2 | Structure | Required sections present | Partially — legitimate exceptions exist (governance inheritance, minimal domains)
3 | Convention | Naming patterns, vocabulary choices | No — organisational adaptations are valuable signal, not errors
4 | Quality | Governance completeness, relationship coverage | No — requires judgment about intent and context
5 | Domain fitness | Is this the right model for the business? | Never — requires human domain expertise

The key insight: **the primary consumer of an MD-DDL model is more sophisticated than any linter**. Agent Ontology already reads intent, identifies gaps, and produces contextual feedback. A linter saying "missing `mutability` key" adds less than the agent — with less context about whether the omission was intentional.

### Handling vocabulary deviations

When an organisation uses `phi` instead of `pii`, or `data_class` instead of `classification`, that is not an error — it is signal. Agents work with deviations and flag them as potential spec vocabulary gaps. This is how the standard improves.

> "In your domain, what terminology do you use for data sensitivity classification? MD-DDL uses `classification`, but if you have existing vocabulary, your agents will understand it and can note the gap for spec consideration."

---

## Explaining Multi-Viewpoint Reviews (Generic)

When a user asks for "second opinions", "different viewpoints", "stress testing",
or broader review quality, teach a multi-viewpoint protocol they can apply to any
artifact (spec, domain model, architecture proposal, migration plan, or governance
design).

### Core explanation to give

A single review pass often misses issues because each reviewer has blind spots.
Quality improves when the same artifact is reviewed from different explicit
viewpoints, then findings are compared.

### Generic multi-viewpoint protocol

1. Define the review target and question clearly.
2. Select 3 to 5 viewpoints with intentionally different concerns.
3. Run each viewpoint as an independent pass with a fixed lens.
4. Require each pass to include "What I Cannot Evaluate".
5. Consolidate findings: agreement, disagreement, blind spots, and priorities.
6. Convert the consolidated findings into an action list with owners.

### Viewpoint menu (generic)

Viewpoint | Lens | Typical question
--- | --- | ---
Structural | Internal consistency, completeness, broken references | "Is this coherent and mechanically sound?"
Adversarial | Failure modes, contradictions, abuse cases | "How could this fail in production?"
Stakeholder | Usability and adoption by real roles | "Would practitioners actually use this?"
Operator | Runability, migration risk, operational burden | "Can this be implemented and maintained safely?"
Governance | Compliance, controls, accountability | "Would this satisfy audit and policy obligations?"
New User | Learnability and onboarding friction | "Can someone new follow this successfully?"

### Practical teaching template

Use this script when users ask how to run better reviews:

> "Pick your target artifact, then run three passes: structural, adversarial,
> and stakeholder. Keep each pass independent, force a limitations section,
> and only then merge findings into one prioritised action list."

### Handoff guidance

- For MD-DDL standard/agent/example reviews: route to `review-md-ddl` for layered execution.
- For a domain model quality check: route to Agent Ontology (`domain-review`) and Agent Governance (`compliance-audit`) for complementary viewpoints.
- For architecture and product decision stress testing: route to Agent Architect and ask for explicit trade-off framing per viewpoint.

---

## Explaining Lifecycle and Evolution

When a user asks about versioning, lifecycle, change history, migration planning,
or how model changes propagate to generated artifacts, load both
`md-ddl-specification/2-Domains.md` and `md-ddl-specification/9-Data-Products.md`.

### Core explanation to give

MD-DDL separates **logical evolution** from **physical regeneration**.

- **Logical evolution** is the intentional change to the domain model: adding an
  entity, deprecating an entity, changing a relationship, or updating a product
  contract. This is what domain and product semantic versions describe.
- **Physical regeneration** is the act of generating a new schema, graph, or file
  contract from the updated logical model. Generated output may differ physically
  even when the logical meaning has not changed.

The key teaching point is: **the authoritative diff lives at the logical layer, not
the physical layer**.

### Workflow to explain

Use this sequence whenever the user asks how MD-DDL handles change:

1. Make the logical change in the MD-DDL model.
2. Classify it as breaking, additive, or corrective.
3. Bump the domain or product version accordingly.
4. Record the change in `LIFECYCLE.md`, including the machine-readable change manifest.
5. Regenerate physical artifacts from the updated model.
6. Reconcile generated output against deployed or baseline state.
7. Use the change manifest to distinguish intentional changes from regeneration noise.
8. Hand the annotated gap report to the user's migration toolchain if a deployment change is needed.

### Product and Domain Lifecycle Relationship

Explain the relationship this way:

- Domains and products both have lifecycle states and versions.
- Products can lag behind a domain. A product may stay `Draft` while its domain is `Active`.
- Products cannot lead a domain. A product cannot be `Active` if its domain is still `Draft` or `Review`.
- Products referencing deprecated entities or deprecated upstream domains need either deprecation or an explicit migration note.

### Handoff Guidance

When the user moves from explanation to action, route them explicitly:

- **Domain promotion, version bump, entity lifecycle** → Agent Ontology
- **Product promotion, product version bump, deprecation planning** → Agent Architect
- **Generated vs deployed schema comparison** → Agent Artifact
- **Lifecycle consistency or governance audit** → Agent Governance

### Short analogy to use

> "Think of MD-DDL like source code plus release notes for data meaning. The model is the source, `LIFECYCLE.md` is the typed release history, and reconciliation is the step where you compare the newly built artifact to what is already running."

---

## Explaining Eventual Consistency in Canonical Data Products

When a user asks about eventual consistency, propagation lag, freshness SLA,
partial rows, or null handling for multi-source canonical entities, follow this
teaching protocol. Load `md-ddl-specification/9-Data-Products.md` and
`md-ddl-specification/7-Sources.md` before responding substantively.

For deep architectural discussion or product design decisions, hand off to
Agent Architect. For implementation work (declaring the product, updating DDL
generation), hand off to Agent Architect then Agent Artifact.

### Step 1 — Anchor to the Familiar

Select the analogy that matches the user's background:

| User type | Analogy |
| --- | --- |
| Data engineer | "Like Kafka consumer groups at different offsets — the canonical entity is the eventually-consistent view all consumers converge to. Each source is a producer at its own throughput; the canonical product's SLA is the guaranteed catch-up window." |
| Data architect | "Like DNS propagation — a record change propagates to different resolvers at different speeds, but within the TTL window all resolvers agree. The canonical data product's `freshness` SLA is the TTL." |
| Data steward | "Like a master record in a catalogue where different source systems update different fields — the catalogue view is eventually correct once all feeds have processed. The governance question is: what does the record look like mid-update?" |
| Integration engineer | "Like CDC fan-out where downstream consumers subscribe at different cadences. The canonical entity accumulates updates from each source as they arrive; the bitemporal record shows exactly when each arrived." |

### Step 2 — Two-Sentence Summary

Eventual consistency in a canonical data product means that updates from different
source systems arrive with different propagation lags, and the canonical entity
converges to the correct state within a declared SLA window. MD-DDL makes this
measurable: the `recorded_at` timestamp (transaction time) captures when the
canonical system received each update, while `valid_from` (valid time) captures
when it was true in the real world — the gap between them is the observable
propagation lag.

### Step 3 — How to Declare It in MD-DDL

Teach this four-step pattern:

1. **Source `change_model`** — each source declares how it propagates changes.
   This governs expected lag per source:
   ```yaml
   change_model: real-time-cdc      # < 1 minute lag
   change_model: batch-intraday     # 15–60 minute lag
   ```

2. **Entity temporal tracking** — bitemporal entities record both when a fact
   was true (`valid_from`/`valid_to`) and when the system received it
   (`recorded_at`/`superseded_at`). This is the audit trail for convergence.

3. **Product `freshness` SLA** — the convergence window the product commits to:
   ```yaml
   sla:
     freshness: "< 1 hour"   # slowest source is batch-intraday at 60 min
   ```

4. **Consistency posture comment** — records the architectural decision:
   ```yaml
   # Consistency posture: eventual (convergence SLA: < 1 hour)
   # Null strategy: nullable-staging (partial rows in base; converged view for consumers)
   ```

### Step 4 — The Null Handling Problem

This is the hardest practical consequence of eventual consistency. Teach it
progressively — lead with the engineering reality, not the theory.

**The problem:** During the convergence lag window, a canonical row may be
partially populated. One source has delivered its attributes; another hasn't
yet. The row exists but some fields are `NULL` — not because they are genuinely
null, but because they haven't arrived yet.

**Three layers where this bites:**

*Storage (Parquet / Arrow):* These columnar formats cannot distinguish `null`
(explicitly set to null) from *absent* (not yet received). Both encode as `null`.
Any downstream reader sees identical bytes for "genuinely unknown" and
"temporarily missing". If downstream ML models or analytics treat `null` as
"genuinely absent", they may draw incorrect conclusions from in-flight rows.

*Transport protocols:* Each protocol handles absent-vs-null differently. JSON
omits absent keys but most deserializers collapse the distinction. Avro requires
a `union [null, <type>]` schema for optional fields. Protobuf's `hasField()` is
the most expressive — it can distinguish "not set" from "set to zero or empty".
The **choice of transport protocol is an architectural dependency** of the
consistency posture: if the user needs to distinguish absent-from-null, they
must choose Protobuf or a custom Avro convention.

*DDL constraints:* A hard `NOT NULL` column in the physical schema blocks partial
row insertion entirely. MD-DDL's `not_null` attribute constraint declares business
intent ("Legal Name must never be permanently null"). The physical `NOT NULL`
constraint is a separate choice — and under eventual consistency, it may need to
be relaxed on the staging table and enforced only at the view layer.

**Three design patterns, teach the trade-offs:**

| Pattern | How it works | When to choose |
| --- | --- | --- |
| Nullable staging + converged view | Base table has `NULL` columns; a view exposes only rows where all expected fields are populated | Best for most eventual-consistency canonical products |
| Reject-partial inserts | Application blocks insert until all sources have contributed | Equivalent to strong consistency; use only if all sources can coordinate |
| Nullable final schema | Base table nullable permanently; consumers handle nulls themselves | Avoid unless consumers are explicitly designed for it |

### Step 5 — How to Validate It

Point the user to the faker runtime for concrete demonstration:

- **`consistency_scenario.py`** (in `agents/agent-artifact/skills/faker/runtime/`)
  simulates what each source feed has delivered at a given moment and shows which
  entity instances are still in-flight vs fully converged.
- **`examples/Financial Crime/consistency_example.py`** is a runnable end-to-end
  demonstration: three source feeds (5 min, 30 min, 60 min lag) converging on
  the Party entity, with SLA validation and a convergence report.
- **`check_temporal_chain()`** in `integrity_check.py` validates that the
  bitemporal chain for each entity instance is coherent (no duplicate current
  rows, no inverted valid-time periods, monotonically increasing `recorded_at`).

### Step 6 — When Not to Use Eventual Consistency

Teach the conditions where **strong consistency is required**:
- Real-time fraud decisioning — a transaction must not be approved against a
  stale risk rating
- Payment authorisation — account status must be current at the moment of authorisation
- Regulatory hard-stops — a party with `sanctions_screen_status: Confirmed Match`
  must not transact; eventual lag could allow a blocked transaction through

In these cases, either all source systems must support synchronous propagation
(real-time-cdc with sub-minute lag), or the product must be scoped to exclude
the slow-source attributes and rely on real-time enrichment at query time.

### Step 7 — Handoff Guidance

| Next step | Route to |
| --- | --- |
| Architect wants to *discuss* the consistency posture decision | Agent Architect (architecture skill) |
| User wants to *declare* the product with consistency posture and null strategy | Agent Architect (product-design skill, Step 8) |
| User wants to *generate DDL* for a nullable-staging pattern | Agent Artifact (dimensional or normalized skill, with consistency posture handoff note) |
| User wants to *validate* eventual consistency with synthetic data | Agent Artifact (faker skill) — generate factories then run `consistency_example.py` |

---

## Design Decision Guidance

When users ask about trade-offs ("should I use X or Y?"), explain both options
and the decision criteria. Do not make the choice for them — present the trade-off
and let them decide.

Common trade-offs to be ready for:

- **Entity vs Enum** — Does the concept have its own attributes, relationships, or
  lifecycle? → Entity. Is it a fixed set of labels with no independent behaviour?
  → Enum. Uncertain? → Start as enum, promote to entity if it grows.
- **Entity vs Attribute** — Could it exist independently? → Entity. Is it always
  a property of something else? → Attribute.
- **Canonical vs Bounded Context** — Must the concept mean the same thing everywhere?
  → Canonical. Does it have meaningfully different attributes in different contexts?
  → Bounded context.
- **Inheritance vs Discriminator** — Do subtypes add meaningful attributes or
  constraints? → Inheritance. Is the distinction just a label? → Discriminator
  attribute.

For deeper trade-off analysis, load the relevant spec reference and/or defer to
Agent Ontology's entity-modelling skill.
