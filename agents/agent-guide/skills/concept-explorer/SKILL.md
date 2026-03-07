---
name: concept-explorer
description: Use this skill when the user asks "what is [concept]", "how does [feature] work", "explain [section]", "compare MD-DDL to [tool]", "why does MD-DDL [design choice]", or any question about a specific part of the standard. Also use when the user wants to understand the reasoning behind a design decision or the trade-offs between alternatives (entity vs enum, canonical vs bounded context, etc.).
---

# Skill: Concept Explorer

Covers interactive teaching of any MD-DDL concept — entities, relationships, events,
enums, domains, sources, transformations, data products, and governance metadata.
Teaches through analogy, progressive depth, and guided self-discovery.

## Spec References

Each spec section has a reference stub in `references/`. Load the one matching the
user's question — do not load all nine at once.

Reference | When to load
--- | ---
`references/foundation-spec.md` | Core principles, document structure, two-layer model
`references/domains-spec.md` | Domain file format, metadata, overview diagrams, summary tables
`references/entities-spec.md` | Entity YAML, attributes, types, constraints, inheritance
`references/enumerations-spec.md` | Enum formats, naming, dictionary vs simple list
`references/relationships-spec.md` | Relationship types, cardinality, granularity, constraints
`references/events-spec.md` | Event structure, payload, temporal rules, actor/entity
`references/sources-spec.md` | Source file format, change models, domain feed tables
`references/transformations-spec.md` | Transformation types, expression language, mapping rules
`references/dataproducts-spec.md` | Data product classes, declaration, governance, masking

---

## Teaching Protocol

Follow this sequence for every concept question. Adjust depth based on user signals.

### Step 1 — Anchor to the Familiar

Before explaining the MD-DDL concept, connect it to something the user already knows.
Use the archetype from the core prompt to select the right analogy:

MD-DDL Concept | ER / UML analogy | dbt / SQL analogy | Data Mesh analogy | FHIR analogy | Governance analogy
--- | --- | --- | --- | --- | ---
**Entity** | ER entity, UML class | dbt model, table | Domain aggregate | FHIR Resource (Patient, Encounter) | Governed data asset
**Attribute** | Column, field | Column in model | Property | Resource element (e.g. `Patient.name`) | Data element with classification
**Enum** | Lookup table, code table | Seed file, static reference | Reference data | ValueSet, CodeSystem | Controlled vocabulary
**Relationship** | ER relationship, FK | ref() in dbt, join | Cross-aggregate reference | FHIR Reference type | Lineage link
**Event** | — (no direct ER equivalent) | CDC event, incremental model | Domain event | FHIR AuditEvent, Provenance | Audit trail trigger
**Domain** | Subject area, schema | Project, package | Bounded context | Implementation Guide | Data domain in catalogue
**Source** | — | Source in dbt, raw table | External system feed | Integration endpoint | System of record
**Transformation** | — | dbt transformation, SQL expression | Mapping rule | ConceptMap | ETL specification
**Data Product** | — | Exposure in dbt | Data product / data contract | — | Published data asset

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
  what shape, and under what governance rules. It is the contract between the model
  and the consumers. Agent Artifact uses it to decide what physical schemas to
  generate."

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
