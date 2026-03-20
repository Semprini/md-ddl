# MD‑DDL Specification (Draft 0.9.2)

*Part of the MD‑DDL Specification. See [1-Foundation.md](./1-Foundation.md) for core principles and document structure.*

---

## **Data Products**

A Data Product in MD-DDL is a governed, publishable unit of data that serves a specific audience. Data products are the bridge between the canonical domain model and the consumers of that model — analytics teams, downstream systems, regulatory reports, and operational dashboards.

The canonical entities, relationships, and events remain the single source of truth. Domain-aligned data products are direct projections of that truth. Consumer-aligned data products define their own logical structure — entities shaped for a specific audience — with explicit lineage back to the canonical model. In both cases, the product declares what is published, in what shape, for whom, and under what governance.

---

### **Why Data Products Are First-Class**

Without data products, the gap between a well-modelled domain and a usable output is filled by undocumented views, ad-hoc queries, and shadow pipelines. Data products close that gap by making the publication contract explicit:

- **What** is published (which entities, attributes, relationships)
- **How** it is shaped (normalized, denormalized, aggregated)
- **Who** consumes it (team, system, or regulatory body)
- **Why** it exists (business purpose and SLA)

By declaring data products in the same Markdown-native format as the rest of the model, MD-DDL ensures that publication intent is version-controlled, reviewable, and traceable from source through canonical model to consumer.

---

### **Data Product Classes**

MD-DDL defines three classes of data product, each serving a distinct purpose in the data lifecycle. These classes are not tiers or layers — they are independent publication intents that may coexist within a single domain.

#### Source-Aligned

A source-aligned product publishes raw or lightly cleansed data from a single source system. It preserves the source schema and change model, making operational data available for audit, replay, and debugging without interpretation.

- **Scope:** Single source system within the domain
- **Shape:** Mirrors source structure; no joins across sources
- **Governance:** Inherits domain defaults; typically lower classification than domain-aligned products
- **Consumers:** Data engineers, audit teams, integration debugging
- **Cross-domain dependencies:** None — source-aligned products are self-contained within a domain

Source-aligned products reference a source system declared in the domain's `## Source Systems` section. Their schema corresponds to the source table structure defined in `sources/<system>/source.md`.

#### Domain-Aligned

A domain-aligned product publishes the canonical model itself — governed entities, relationships, and events in their modelled form. It is the standard representation of the domain's truth, ready for consumption by systems that understand the canonical schema.

- **Scope:** One or more canonical entities within the owning domain
- **Shape:** Matches the canonical model structure (normalized or as-modelled)
- **Governance:** Inherits domain defaults; represents the highest-fidelity view
- **Consumers:** Domain services, master data consumers, cross-domain integration
- **Cross-domain dependencies:** None — domain-aligned products publish only concepts owned by the declaring domain

Domain-aligned products reference entities from the domain's `## Entities` section. Their schema corresponds directly to the entity YAML definitions and relationship structure. Their `lineage` declares which source system tables feed the canonical entities, providing traceability from source through canonical to consumer.

#### Consumer-Aligned

A consumer-aligned product reshapes domain data for a specific audience or use case. It may denormalize, aggregate, filter, or combine entities to suit the consumer's query patterns and performance needs.

- **Scope:** Defines its own entities shaped for the consumer's use case. Sources exclusively from canonical (domain-aligned) products — never from source systems directly.
- **Shape:** Tailored to consumer needs — wide tables, star schemas, aggregated summaries
- **Governance:** Inherits domain defaults with possible overrides (e.g., PII masking, restricted retention)
- **Consumers:** Named team, application, report, or regulatory body
- **Multi-domain:** Consumer-aligned products may source from canonical entities across multiple domains when the consumer's use case spans domain boundaries. The `lineage` field declares which domains and entities are consumed.

Consumer-aligned products define their own logical model with a Mermaid class diagram and an attribute mapping section that traces every product attribute back to its canonical source using the same table-based format as source transforms. The `schema_type` declared on the product determines which Agent Artifact skill produces the physical output.

---

### **Platform Posture**

Organisations differ fundamentally in how they relate data products to platforms. This architectural decision shapes which product classes apply, what artifacts get generated, and what infrastructure is assumed. The platform posture must be established before designing data products.

MD-DDL defines three platform postures:

#### Single-Platform

All data products are self-contained on one platform (e.g., Snowflake, Databricks, BigQuery). Source ingestion, transformation, canonical storage, and consumer access all happen within the same platform.

- **Effect on classes:** All three classes (source-aligned, domain-aligned, consumer-aligned) are typically recognised as data products
- **Effect on artifacts:** Agent Artifact generates for one target platform; `schema_type` maps directly to platform-native constructs
- **Effect on infrastructure:** Minimal integration complexity; the platform provides compute, storage, and access control
- **Typical pattern:** Source-aligned = raw/staging schemas; domain-aligned = curated schemas; consumer-aligned = materialized views or denormalized tables

#### Polyglot

Different product classes leverage different platforms and technologies depending on the data's lifecycle stage and access pattern. The organisation accepts that data products span infrastructure boundaries.

- **Effect on classes:** Each class may target a different platform stack:
  - **Source-aligned** — CDC, streaming (Kafka, Flink), operational data stores, event buses
  - **Domain-aligned / foundational** — polyglot persistence (relational + document + graph), analytical and operational interfaces, potentially spanning OLTP and OLAP stores
  - **Consumer-aligned** — purpose-built for the consumer's query engine (data warehouse, API layer, search index, dashboard cache)
- **Effect on artifacts:** Agent Artifact may need to generate for multiple target platforms per domain; `schema_type` maps to platform-appropriate constructs for each product
- **Effect on infrastructure:** Higher integration complexity; requires cross-platform lineage tracking, consistent governance enforcement, and potentially different access control mechanisms per platform

#### Selective Scope

The organisation does not consider all classes as "data products." Some layers are treated as infrastructure or engineering concerns rather than governed, published products.

- **Common pattern:** Source-aligned feeds are infrastructure (CDC pipelines, staging areas) managed by data engineering — not declared as data products. Only domain-aligned and consumer-aligned outputs are governed as products.
- **Alternative pattern:** Only consumer-aligned outputs are products. Domain-aligned canonical models are internal reference architectures, not published products.
- **Effect on MD-DDL:** Product classes that fall outside the org's product scope are still valid as infrastructure concepts but are not declared in `products/`. Source declarations and transforms still exist in `sources/` regardless of whether source-aligned products are declared.

#### Declaring Platform Posture

Platform posture is declared in domain metadata under the `platform` block:

```yaml
platform:
  posture: single-platform | polyglot | selective
  technologies:
    - "Snowflake"
  product_scope:
    - source-aligned
    - domain-aligned
    - consumer-aligned
  notes: "All data products are self-contained in Snowflake."
```

Field | Required | Purpose
--- | --- | ---
`posture` | Yes (when `platform` block exists) | The organisation's platform strategy for this domain
`technologies` | No | List of platforms and technologies used by data products in this domain
`product_scope` | No | Which product classes the organisation recognises as data products. Defaults to all three. If omitted, all classes are in scope.
`notes` | No | Free-text context on platform decisions, constraints, or migration plans

Platform posture is typically an organisation-wide decision, but is declared per domain because different parts of the organisation may be at different stages of platform strategy. When all domains share the same posture, use consistent values across domain files.

---

### **Data Product Declaration**

A data product is declared using a **level-3 Markdown heading** inside a detail file stored in the `products/` subfolder of the domain:

```markdown
### Customer 360 Profile
```

The heading is the product's name — its identity in the Knowledge Graph.

#### Metadata

Product metadata is expressed as YAML inside a fenced code block immediately after the heading:

````markdown
### Customer 360 Profile

A denormalized wide-column view combining customer identity, preferences,
account summary, and risk indicators for the retail analytics team.

```yaml
class: consumer-aligned
schema_type: wide-column
owner: retail.analytics@example.com
consumers:
  - Retail Analytics Team
  - Customer Insights Dashboard
status: Active
version: "1.0.0"

entities:
  - Customer 360 Profile

lineage:
  - domain: Retail
    entities:
      - Customer
      - Customer Preferences
      - Account
      - Party

governance:
  classification: Confidential
  pii: true
  retention: "5 years"
  masking:
    - attribute: "Date of Birth"
      strategy: year-only
    - attribute: "Tax Identification Number"
      strategy: hash
```
````

#### Required Metadata Fields

Field | Purpose
--- | ---
`class` | One of `source-aligned`, `domain-aligned`, `consumer-aligned`.
`schema_type` | Physical output style: `normalized`, `dimensional`, `wide-column`, `knowledge-graph`. Drives Agent Artifact's skill selection for generation and determines the logical model shape.
`owner` | The team or individual accountable for this product's correctness and availability.
`consumers` | List of named consumers — teams, systems, reports, or regulatory bodies.
`status` | Lifecycle state: `Draft`, `Active`, `Deprecated`, `Retired`.
`entities` | The entities the product defines and publishes. For domain-aligned products these are the canonical entities projected by the product. For consumer-aligned products these are the product's own entities — which may differ from canonical entities when the product reshapes, denormalizes, or aggregates.
`lineage` | Declares where the product's data comes from. For domain-aligned products: source system tables. For consumer-aligned products: canonical entities from one or more domains. See [Lineage](#lineage) for structure.

#### Optional Metadata Fields

Field | Purpose
--- | ---
`version` | Semantic version of the product definition.
`governance` | Governance overrides that differ from domain defaults. Only declare fields that differ.
`masking` | Attribute-level masking rules for sensitive data. Each entry names the product attribute and a masking strategy.
`sla` | Service-level attributes (freshness, availability, latency).
`refresh` | Refresh cadence: `real-time`, `hourly`, `daily`, `weekly`, `on-demand`.

#### Source-Aligned Metadata

Source-aligned products include a `source` field instead of an `entities` field:

````markdown
### Salesforce CRM Raw Feed

Raw audit feed from Salesforce CRM preserving source schema and change events
for replay and integration debugging.

```yaml
class: source-aligned
source: salesforce-crm
owner: data.engineering@example.com
consumers:
  - Data Engineering
  - Audit & Compliance
status: Active

governance:
  classification: Internal
  retention: "3 years"
```
````

Field | Purpose
--- | ---
`source` | The source system identifier matching a folder under `sources/`. Used instead of `entities` for source-aligned products.

#### Lineage

The `lineage` field declares the data provenance of a product — where its data comes from. Lineage structure differs by product class:

**Domain-aligned products** trace lineage to source system tables:

```yaml
lineage:
  - source: salesforce-crm
    tables:
      - table_account
      - table_contact
      - table_contact_point
  - source: sap-fraud-management
    tables:
      - table_sanctions_screening
```

Each `source` value must match a source system folder under `sources/`. Each `tables` entry must match a transform file declared in that source system's feeds table.

**Consumer-aligned products** trace lineage to canonical entities from one or more domains:

```yaml
lineage:
  - domain: Financial Crime
    entities:
      - Transaction
      - Party
      - Party Role
  - domain: Customer
    entities:
      - Customer
      - Customer Preferences
  - domain: Geography
    entities:
      - Country
      - Jurisdiction
```

Each `domain` value must match the domain name declared in the referenced domain's `domain.md` level-1 heading. Each `entities` entry must match an entity declared in that domain's `## Entities` summary table. Consumer-aligned products source exclusively from canonical (domain-aligned) products — never from source systems directly.

Multi-domain lineage creates edges in the Knowledge Graph linking the data product to entities it does not own. The owning domain retains governance authority over those entities — the consuming product inherits their governance posture unless explicit overrides are declared. Multi-domain lineage is unidirectional: declaring lineage from another domain does not modify the referenced domain and does not create an inverse reference entry.

#### Masking Precedence

For multi-domain products, product-level `masking` declarations are authoritative
for the published output. If contributing domains use different masking strategies
for similar attributes, the consuming product must explicitly declare the strategy
it will publish.

#### SLA Scope

SLA metadata is a product-level publication contract. It does not imply per-entity
freshness or source-level cadence guarantees for each contributing domain.

---

### **Logical Model**

Every data product with a `schema_type` must include a logical model — a Mermaid class diagram under a `#### Logical Model` heading that captures enough structural information to accurately and repeatably generate physical schema artifacts.

The logical model differs by product class:

#### Domain-Aligned Logical Models

A domain-aligned logical model is a **projection of the canonical domain model** scoped to the product's declared entities. It shows:

- Each entity as a class with all its attributes and types, matching the canonical entity definitions
- Inheritance relationships (e.g., Person → Party)
- Association cardinalities between entities
- Entity names hyperlinked to their detail files — the logical model is a view into the canonical model, not a copy of it

Because domain-aligned products publish the canonical structure directly, their logical model can be mechanically derived from the entity detail files. The entity detail files remain authoritative for constraints, governance, and temporal tracking.

#### Consumer-Aligned Logical Models

A consumer-aligned logical model defines the **product's own structure**, which may differ substantially from the canonical model it sources from. It shows:

- The product's entities as classes with their attributes and types
- Relationships between the product's entities (which may differ from canonical relationships)
- For denormalized products (wide-column): typically a single class with all attributes flattened
- For normalized products: multiple classes preserving entity boundaries but with selected attribute subsets

Consumer-aligned logical models must be accompanied by an `#### Attribute Mapping` section that traces every product attribute back to its canonical source using the table-based format aligned with source transform tables. This mapping is the contract that enables generation and ensures the product's structure is reproducible.

#### Attribute Mapping

Consumer-aligned products declare an `#### Attribute Mapping` section following the logical model diagram. The mapping uses the same table-based format as source transform files (see [Section 8 — Transformations](./8-Transformations.md)), providing a consistent lineage format from source through canonical to product.

Each mapping table traces product attributes to their canonical source:

- **Direct mapping:** Place the canonical `Entity.Attribute` (or `Domain.Entity.Attribute` for cross-domain) in the Source column.
- **Non-direct mapping:** Link to a breakout section (e.g., `[Derive Risk Category](#derive-risk-category)`) in the Transform column. Define the transformation logic under that heading using the same YAML transformation types as source transforms (`derived`, `conditional`, `lookup`, `aggregation`).

For **wide-column products**, the mapping is a single flat table. A Path column captures the relationship traversal from the product's grain entity to each source attribute. For **dimensional products**, the mapping uses the same 4-column format but grouped by fact and dimension entity under level-5 headings — the Path column captures foreign key lookups in the fact table:

```markdown
#### Attribute Mapping

Product Attribute | Source | Path | Transform
--- | --- | --- | ---
Transaction Identifier | Transaction.Transaction Identifier | — | —
Amount | Transaction.Amount | — | —
Payer Legal Name | Party.Legal Name | Transaction → Payer → Party | —
Payer PEP Status | Person.Politically Exposed Person Status | Transaction → Payer → Party → Person | —
Branch Code | Branch.Branch Code | Transaction → Payer → Customer → Account → Branch | —
Risk Category | — | — | [Derive Risk Category](#derive-risk-category)

##### Derive Risk Category

Derives a simplified risk category from the canonical risk rating and
sanctions screen status for dashboard consumption.

​```yaml
type: conditional
target: Risk Category
source:
  field: Party.Risk Rating
cases:
  High: "Risk Rating == 'High' OR Sanctions Screen Status == 'Confirmed Match'"
  Medium: "Risk Rating == 'Medium'"
  Low: "Risk Rating == 'Low'"
fallback: Unknown
​```
```

Use `—` (em-dash) for cells that are not applicable (e.g., no path traversal, no transform). If an individual entity within a normalized product includes attributes traversed from another entity, that entity's table may use the 4-column format with a Path column.

For **normalized products** (and knowledge-graph), the mapping is grouped by product entity — one table per entity under a level-5 heading. No Path column is needed because the entity structure is preserved:

```markdown
#### Attribute Mapping

##### Transaction

Product Attribute | Source | Transform
--- | --- | ---
Transaction Identifier | Transaction.Transaction Identifier | —
Amount | Transaction.Amount | —

##### Patient

Product Attribute | Source | Transform
--- | --- | ---
Patient Identifier | Healthcare.Patient.Patient Identifier | —
Given Name | Healthcare.Patient.Given Name | —
Masked DOB | — | [Year Only From DOB](#year-only-from-dob)

##### Year Only From DOB

Extracts year from the canonical date of birth for pseudonymised analytics.

​```yaml
type: derived
target: Masked DOB
expression: "year(Date of Birth)"
inputs:
  Date of Birth:
    field: Healthcare.Patient.Date of Birth
​```
```

Cross-domain attributes are prefixed with the domain name (e.g., `Healthcare.Patient.Given Name`) to distinguish them from same-domain canonical attributes.

Domain-aligned products do not require an attribute mapping because their entities are identity projections of the canonical model — the mapping is implicit.

---

### **Masking Strategies**

When a data product exposes PII or sensitive attributes, `masking` entries define how those attributes are protected in the published output.

Strategy | Behaviour
--- | ---
`hash` | One-way hash of the value; preserves joinability across products using the same salt.
`redact` | Replace with a fixed placeholder (e.g., `***REDACTED***`).
`year-only` | For date attributes: retain the year, zero out month and day.
`truncate` | Retain a prefix of the value (e.g., first 3 characters of a postcode).
`tokenize` | Replace with a reversible token managed by a tokenization service.
`null` | Replace the value with null in the published output.

Masking is declared at the product level, not the entity level. The same entity may appear in multiple products with different masking rules depending on the consumer's access level.

---

### **Product-Driven Generation**

The `schema_type` field on a data product is the entry point for physical artifact generation. When an AI agent encounters a data product with a `schema_type`, it selects the corresponding Agent Artifact skill:

`schema_type` value | Agent Artifact skill | Output
--- | --- | ---
`normalized` | Normalized | DDL, JSON Schema, Parquet contract
`dimensional` | Dimensional | Star schema DDL
`wide-column` | Wide Column | Denormalized table DDL
`knowledge-graph` | Knowledge Graph | Cypher DDL

The product's logical model and `entities` list scope the generation. For domain-aligned products, the agent reads the canonical entity detail files to obtain attributes, types, and constraints. For consumer-aligned products, the agent uses the logical model diagram and attribute mapping tables as the generation input — the product defines its own structure. In both cases, the product's `governance` and `masking` metadata are applied as constraints on the generated artifacts.

---

### **SLA Declaration**

Products that serve operational consumers may declare service-level attributes:

```yaml
sla:
  freshness: "< 15 minutes"
  availability: "99.9%"
  latency_p99: "< 200ms"
```

SLA fields are informational — they document expectations but do not generate runtime enforcement. Monitoring and alerting are orchestration concerns outside MD-DDL's scope.

---

### **Two-Layer Structure**

Data products follow the same two-layer pattern as entities, relationships, and events:

1. **Summary** — A `## Data Products` table in the domain file listing all products with class, consumers, and status
2. **Detail** — Individual product definitions in `products/` detail files using level-3 headings and YAML blocks

This allows the domain file to act as a complete index of what the domain publishes, while detail files contain the full product specification.

#### Domain File Summary Table

The domain file includes a `## Data Products` section with a summary table:

Column | Purpose
--- | ---
**Name** | The product name, linked to its detail definition.
**Class** | `source-aligned`, `domain-aligned`, or `consumer-aligned`.
**Consumers** | Primary consumers of this product.
**Status** | Lifecycle state.

Example:

```markdown
## Data Products

Name | Class | Consumers | Status
--- | --- | --- | ---
[Customer 360 Profile](products/analytics.md#customer-360-profile) | consumer-aligned | Retail Analytics Team | Active
[Salesforce CRM Raw Feed](products/source-feeds.md#salesforce-crm-raw-feed) | source-aligned | Data Engineering | Active
[Canonical Party](products/canonical.md#canonical-party) | domain-aligned | Cross-domain Integration | Active
```

#### Detail File Structure

Product detail files follow the same structural rules as entity detail files:

- Begin with a level-1 heading naming the domain, linked back to the domain file
- Use level-2 heading `## Data Products`
- Define individual products under level-3 headings with YAML metadata blocks

```markdown
# [Financial Crime](../domain.md)

## Data Products

### Customer 360 Profile
...product definition...

### Transaction Risk Summary
...product definition...
```

---

### **Rules for Data Products**

1. **Class determines scope.** Source-aligned products reference a single source system. Domain-aligned products project canonical entities within the owning domain. Consumer-aligned products define their own entities and may source from multiple domains.

2. **Multi-domain lineage only for consumer-aligned.** Only consumer-aligned products may declare lineage from multiple domains. Source-aligned and domain-aligned products are self-contained within their domain.

3. **Entities are what the product publishes.** For domain-aligned products, `entities` lists the canonical entities projected by the product. For consumer-aligned products, `entities` lists the product's own entities — which may differ from canonical entities when the product reshapes, denormalizes, or aggregates.

4. **Lineage declares provenance.** Every non-source-aligned product must declare `lineage`. For domain-aligned products, lineage traces to source system tables. For consumer-aligned products, lineage traces to canonical entities from one or more domains. Consumer-aligned products source exclusively from canonical products — never from source systems directly.

5. **Logical model required.** Every product with a `schema_type` must include a Mermaid class diagram under a `#### Logical Model` heading. The diagram must contain sufficient structural detail (attributes, types, cardinalities) to accurately and repeatably generate physical schema artifacts. Consumer-aligned products must also include an `#### Attribute Mapping` section using the table-based format aligned with source transform tables.

6. **Governance inheritance.** Products inherit governance metadata from the domain by default. Only declare `governance` overrides when the product requires stricter or different controls than the domain default.

7. **Masking is product-scoped.** Masking rules are declared per product, not per entity. The same attribute may be masked differently in different products.

8. **Schema type drives generation.** The `schema_type` is required and determines which Agent Artifact skill produces the physical output. The product's logical model, `entities` list, and `governance`/`masking` metadata are the generation input contract.

9. **Source field for source-aligned.** Source-aligned products use `source` instead of `entities`. The value must match a source system folder under `sources/`.

10. **Two-layer compliance.** Every data product must appear in both the domain file summary table and a detail file. The domain file is the index; the detail file is the contract.

11. **Name uniqueness.** Data product names must be unique within a domain. The level-3 heading is the product's identity in the Knowledge Graph.

---

### **Brownfield Adoption Note**

In brownfield adoption contexts (see [Section 10 — Adoption](./10-Adoption.md)):

- At maturity levels 1–2, data products may reference existing physical artifacts that are not yet MD-DDL-generated
- At maturity level 4+, all data products should be generated from MD-DDL declarations
- Products can begin their lifecycle at `Draft` even when based on existing physical artifacts — the product declaration documents intent while the underlying assets are being migrated to declarative MD-DDL

---

### **Product Lifecycle**

Data products progress through defined lifecycle states. The `status` field declares the current state; optional date fields document transition timing.

#### Lifecycle States

State | Meaning
--- | ---
`Draft` | Product is being designed. Not yet available to consumers. May change without notice.
`Active` | Product is live and governed. Changes follow the product versioning and consistency rules defined below.
`Deprecated` | Product is marked for retirement. Consumers should migrate to an alternative. Still available but no longer enhanced.
`Retired` | Product is no longer available. Retained in the domain file for lineage and audit traceability but not published or generated.

#### Transition Rules

- `Draft` → `Active`: Product has passed quality review, names at least one consumer, and declares version `1.0.0` or higher.
- `Active` → `Deprecated`: A `deprecated_date` field must be added to the product metadata. A `successor` field should name the replacement product if one exists.
- `Deprecated` → `Retired`: A `sunset_date` field must be added. After this date the product is no longer generated or published. The declaration remains in the detail file for audit purposes.
- `Retired` → any: Not permitted. Retired products are immutable records. If the concept needs to be revived, create a new product with a new name.

#### Lifecycle Metadata Fields

Field | Required | Purpose
--- | --- | ---
`deprecated_date` | When status is `Deprecated` | ISO 8601 date when the product was marked for retirement.
`successor` | Advisory when `Deprecated` | Name of the replacement product (if any), linked to its detail heading.
`migration_note` | Advisory when the product remains active during upstream deprecation | Free-text migration guidance explaining how consumers should respond to deprecated upstream entities or domains.
`sunset_date` | When status is `Retired` | ISO 8601 date after which the product is no longer published.

Example:

```yaml
status: Deprecated
deprecated_date: "2025-03-15"
successor: "Customer 360 Profile v2"
```

#### Product Versioning

The `version` field uses semantic versioning (`MAJOR.MINOR.PATCH`) to track the evolution of the product contract. Product versions are independent from domain versions: a product may remain `Draft` while its domain is `Active`, and a product may lag behind the latest domain version while consumers migrate.

Trigger | Version Impact
--- | ---
Domain breaking change affecting an entity in the product's `lineage` | Major bump
Domain additive change affecting an entity in the product's `lineage` and reflected in the product's logical model | Minor bump
Product removes an entity from its `entities` list | Major bump
Product adds an entity to its `entities` list | Minor bump
Product changes masking rules, SLA, consumers, or other governance contract details without reducing schema scope | Minor or patch bump depending on consumer impact
Corrective documentation or descriptive fixes with no contract impact | Patch bump

Use a major bump when a correctly-authored consumer must change to keep working. Use a minor bump when the published contract is extended but existing consumers can continue unchanged. Use a patch bump for non-breaking clarifications or corrective metadata changes.

#### Product-Domain Lifecycle Consistency

Products evolve independently, but they cannot be more mature than the model they publish.

- A product's `status` must not be more advanced than the owning domain's status. A product cannot be `Active` if its domain is `Draft` or `Review`.
- Products may lag the domain. A product may remain `Draft` while its domain is `Active`.
- Promoting a domain to `Active` does not automatically promote any products declared within it.
- An `Active` product should declare version `1.0.0` or higher.
- If a product references deprecated entities or draws from a deprecated lineage dependency, it must either move to `Deprecated` or declare a `migration_note` explaining the consumer migration path.
- When a domain version bump changes referenced entities, affected products should evaluate their own version independently using the rules above and record the result in the domain's `LIFECYCLE.md` when that file is maintained.

#### Lifecycle History Recording

Product promotions, version bumps, deprecations, and retirements should be recorded in the owning domain's `LIFECYCLE.md` file when present. The domain owns the lifecycle history file because product lifecycle is part of the domain's publication history.

---

### **Multi-Domain Governance Conflict Resolution**

When a consumer-aligned data product spans multiple domains via `lineage`, governance metadata may conflict between the owning domain and the referenced domains. These conflicts must be resolved explicitly — silent inheritance of weaker controls is not permitted.

#### Conflict Detection

For each domain in `lineage`, compare the owning domain's governance defaults with the referenced domain's defaults across:

Field | Conflict Exists When
--- | ---
`classification` | Referenced domain has a higher classification than the product declares
`retention` | Domains declare different retention periods
`pii` | Referenced domain declares `pii: true` but the product does not acknowledge it
`regulatory_scope` | Referenced domain is subject to regulatory frameworks not listed in the product's owning domain

#### Resolution Rules

1. **Classification: highest wins.** The product's effective classification is the highest of all contributing domains. If the product declares a lower classification, it must include an explicit `governance.classification` override with a justification comment explaining why the lower classification is appropriate (e.g., masking renders the data non-sensitive).

2. **Retention: longest wins.** The product's effective retention is the longest period required by any contributing domain's regulatory obligations. A shorter retention may be declared only if the product's masking or aggregation removes the retention trigger.

3. **PII: union of obligations.** If any contributing domain declares `pii: true`, the product must either declare `pii: true` with appropriate masking entries, or demonstrate that all PII attributes are masked to a level where PII obligations no longer apply.

4. **Regulatory scope: union of frameworks.** The product is subject to the combined regulatory scope of all contributing domains. The owning domain's `regulatory_scope` does not shield the product from obligations in the referenced domains.
