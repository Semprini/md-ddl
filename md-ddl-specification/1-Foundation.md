# MD‑DDL Specification (Draft 0.9.2)

*A Markdown‑native Data Definition Language for human-AI collaboration.*

---

## **Overview**

MD‑DDL is a **Markdown‑first**, **AI‑friendly** standard for defining domains, entities, attributes, enums, relationships, events, source mappings, and data products. It is designed to be readable by humans, generatable by AI, and transformable into:

- Data catalogs
- Knowledge graphs
- Data product definitions
- Schemas and technical artifacts (DDL, JSON Schema, Parquet contracts)
- ETL/ELT logic and source-to-domain lineage

MD‑DDL uses Markdown structure as its primary syntax, with YAML or JSON blocks for structured definitions and Mermaid or PlantUML for diagramming. Structural consistency is enforced by AI agents that validate, generate, and maintain model artifacts.

---

## **Core Principles**

1. **Source of Truth**  
   Every concept is defined once in the domain, in one canonical location. A design choice is whether to follow Domain Driven Design (DDD) and allow domain concepts to be mutually exclusive or not.

   This principle extends to source mappings: canonical entities contain no source references — they define meaning, not origin. Source definitions and transform files are self-contained under `sources/<system>/` within each domain (see [Section 7 — Sources](./7-Sources.md)).

2. **Markdown‑Native**  
   Headings define structure; prose defines meaning.

3. **AI‑Friendly**  
   No redundant fields. No manually maintained lists. Minimal boilerplate.

4. **Agent‑Driven**  
   AI agents infer domain membership, index entities, validate relationships, and generate physical artifacts from the model.

5. **Graph‑Powered**  
   The knowledge graph acts as the semantic runtime for reasoning, lineage, and governance.

6. **Natural‑Language Naming**
   Entities, attributes, and relationships use human‑readable names rather than code‑style casing.

7. **Adoption is Incremental**
   MD-DDL supports incremental adoption. Organisations can begin by documenting their existing data landscape — dimensional models, canonical models, ETL pipelines, governance metadata — and progressively evolve toward declarative, AI-generated artifacts. The `baselines/` folder captures existing state; the adoption maturity model tracks the journey; the canonical model is the destination. See [Section 10 — Adoption](./10-Adoption.md) for the full maturity model and adoption workflow.

### Normative Language

MD-DDL reserves **must** for rules whose violation breaks AI interpretation of the model — syntax, reference integrity, and the two-layer discovery structure. Everything else — naming, file layout, table columns, value vocabularies — is a **default convention**: the shape agents generate by default and recognise on sight. Conventions are extensible, and deviations from them are observations to work with (and potential spec contributions), not errors. See the [Validation Model](#validation-model) below.

---

## **Document Structure**

MD‑DDL is composed of several logical components:

- [Domains](./2-Domains.md)
- [Entities](./3-Entities.md)
- [Enumerations](./4-Enumerations.md)
- [Relationships](./5-Relationships.md)
- [Events](./6-Events.md)
- [Sources](./7-Sources.md)
- [Transformations](./8-Transformations.md)
- [Data Products](./9-Data-Products.md)
- [Adoption](./10-Adoption.md)

MD‑DDL uses a **two‑layer structure** for Entities, Enums, Relationships, Events, and Data Products:

1. A **summary definition**
2. A **detailed definition**

During adoption (see [Section 10](./10-Adoption.md)), a transitional layer may also exist:

- **Layer 0 — Baselines** (existing state documentation) — transitional; captured in `baselines/` subfolders within the domain

Baselines document what exists today. They are not part of the canonical model and are never used for generation. They are superseded as the domain advances through adoption maturity levels.

This structure supports both human readability and AI context management.

Example domain layout:

```shell
domains/customer/domain.md
domains/customer/entities/customer.md
domains/customer/entities/customer-preference.md
domains/customer/relationships/customer-has-preferences.md
domains/customer/products/analytics.md
domains/customer/diagrams/overview.md
```

Example source layout:

```shell
Financial Crime/sources/salesforce-crm/source.md
Financial Crime/sources/salesforce-crm/transforms/table_account.md
Financial Crime/sources/salesforce-crm/transforms/table_contact_point.md
Financial Crime/sources/sap-fraud-management/source.md
Financial Crime/sources/temenos-payment/source.md
```

Domain files and source files are co-located at the domain level. Domain files define meaning. Source folders define operational origin and mapping logic for that specific domain context.

---

### **Two‑Layer Structure**

#### **AI Context Management**

- The domain file provides a compact summary of all conceptual objects.  
- AI agents load only the summaries initially.  
- When deeper context is needed, they follow the `detail:` link to load the full definition.

#### **Human Readability**

- The domain file becomes a clean, navigable table of contents.  
- Detail files remain focused, concise, and free from clutter.

#### **Structural Predictability**

- AI agents know exactly where to find summaries and details.  
- Both layers are merged into a unified conceptual, logical, and physical model.

#### Detail File Flexibility

Detail files are not restricted to a single entity. Authors may organise detail files to suit their modelling style — for example, one entity per file, one file per subdomain cluster, or a file combining an entity with its enumerations and originating relationships.
The only structural requirement is that every detail file begins with a level‑1 heading naming the domain (with a link back to the domain file), followed by one or more level‑2 section headings (## Entities, ## Enums, ## Relationships, ## Events, ## Data Products) containing the relevant definitions.

Source transform files follow the same two-layer pattern but are scoped to a source system within a domain context. They begin with a level-1 heading linking back to `./source.md` in the same source folder, followed by a level-2 heading for the source table and optional level-3 rule sections for non-direct mappings.

---

## **Validation Model**

MD-DDL uses a two-tier validation model. **Tier 1 — mechanical pre-flight checks** covers only what breaks AI interpretation outright: YAML and Mermaid syntax, internal link integrity, entity reference consistency, and the presence of a domain `version:` field. **Tier 2 — agent-driven quality review** covers everything else: structure, convention, quality, and domain fitness are judgment calls that need context, so they belong to agents and humans, not rule-based linters.

Agents treat organisational deviations from convention — a field named `phi` instead of `pii`, `data_class` instead of `classification` — as observations to work with and potential spec vocabulary contributions, not errors.

The full validation level taxonomy, pre-flight check definitions, the tool interface, and the `{{INCLUDE}}` directive used by agent prompt files are collected in the non-normative [Validation Tooling Guide](../guides/validation-tooling.md).

---

...next: [Domains](2-Domains.md)
