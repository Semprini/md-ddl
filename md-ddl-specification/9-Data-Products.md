# MD‑DDL Specification (Draft 0.8.2)

*Part of the MD‑DDL Specification. See [1-Foundation.md](./1-Foundation.md) for core principles and document structure.*

---

## **Data Products**

A Data Product in MD-DDL is a governed, publishable unit of data that serves a specific audience. Data products are the bridge between the canonical domain model and the consumers of that model — analytics teams, downstream systems, regulatory reports, and operational dashboards.

Data products do not duplicate the domain model. They declare what subset of the model is published, in what shape, for whom, and under what governance. The canonical entities, relationships, and events remain the single source of truth; data products are curated projections of that truth.

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

Domain-aligned products reference entities from the domain's `## Entities` section. Their schema corresponds directly to the entity YAML definitions and relationship structure.

#### Consumer-Aligned

A consumer-aligned product reshapes domain data for a specific audience or use case. It may denormalize, aggregate, filter, or combine entities to suit the consumer's query patterns and performance needs.

- **Scope:** One or more canonical entities, potentially from multiple domains
- **Shape:** Tailored to consumer needs — wide tables, star schemas, aggregated summaries
- **Governance:** Inherits domain defaults with possible overrides (e.g., PII masking, restricted retention)
- **Consumers:** Named team, application, report, or regulatory body
- **Cross-domain dependencies:** Permitted — consumer-aligned products may reference entities from other domains when the consumer's use case spans domain boundaries

Consumer-aligned products are the primary trigger for physical artifact generation. The `schema_type` declared on a consumer-aligned product determines which Agent Artifact skill produces the output.

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
status: Production
version: "1.0.0"

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
`owner` | The team or individual accountable for this product's correctness and availability.
`consumers` | List of named consumers — teams, systems, reports, or regulatory bodies.
`status` | Lifecycle state: `Draft`, `Production`, `Deprecated`.
`entities` | List of canonical entity names included in this product.

#### Optional Metadata Fields

Field | Purpose
--- | ---
`schema_type` | Physical output style: `normalized`, `dimensional`, `wide-column`, `knowledge-graph`. When declared, this drives Agent Artifact's skill selection for generation.
`version` | Semantic version of the product definition.
`governance` | Governance overrides that differ from domain defaults. Only declare fields that differ.
`masking` | Attribute-level masking rules for sensitive data. Each entry names the canonical attribute and a masking strategy.
`sla` | Service-level attributes (freshness, availability, latency).
`refresh` | Refresh cadence: `real-time`, `hourly`, `daily`, `weekly`, `on-demand`.
`cross_domain` | List of external domain references for consumer-aligned products that span domains. Each entry names the domain and entities consumed.

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
status: Production

governance:
  classification: Internal
  retention: "3 years"
```
````

Field | Purpose
--- | ---
`source` | The source system identifier matching a folder under `sources/`. Used instead of `entities` for source-aligned products.

#### Cross-Domain References

Consumer-aligned products that span domain boundaries must declare their external dependencies explicitly using the `cross_domain` field:

````markdown
### Suspicious Activity Report

Combines financial crime transaction data with customer identity from the
Customer domain for SAR filing.

```yaml
class: consumer-aligned
schema_type: normalized
owner: compliance.team@example.com
consumers:
  - Regulatory Reporting System
  - FATF Compliance
status: Production

entities:
  - Transaction
  - Party
  - Party Role

cross_domain:
  - domain: Customer
    entities:
      - Customer
      - Customer Preferences
  - domain: Geography
    entities:
      - Country
      - Jurisdiction

governance:
  classification: Highly Confidential
  pii: true
  retention: "10 years"
```
````

Cross-domain references create edges in the Knowledge Graph linking the data product to entities it does not own. The owning domain retains governance authority over those entities — the consuming product inherits their governance posture unless explicit overrides are declared.

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

The product's `entities` list scopes the generation — only the declared entities and their relationships are included in the physical output. The product's `governance` and `masking` metadata are applied as constraints on the generated artifacts.

If no `schema_type` is declared, the product is a logical declaration only. It documents what is published but does not trigger physical generation.

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
[Customer 360 Profile](products/analytics.md#customer-360-profile) | consumer-aligned | Retail Analytics Team | Production
[Salesforce CRM Raw Feed](products/source-feeds.md#salesforce-crm-raw-feed) | source-aligned | Data Engineering | Production
[Canonical Party](products/canonical.md#canonical-party) | domain-aligned | Cross-domain Integration | Production
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

1. **Class determines scope.** Source-aligned products reference a single source system. Domain-aligned products reference canonical entities within the owning domain. Consumer-aligned products may span domains.

2. **Cross-domain only for consumer-aligned.** Only consumer-aligned products may declare `cross_domain` references. Source-aligned and domain-aligned products are self-contained within their domain.

3. **Entities must exist.** Every entity listed in `entities` must be declared in the domain's `## Entities` table (or in a referenced domain for `cross_domain` entries).

4. **Governance inheritance.** Products inherit governance metadata from the domain by default. Only declare `governance` overrides when the product requires stricter or different controls than the domain default.

5. **Masking is product-scoped.** Masking rules are declared per product, not per entity. The same attribute may be masked differently in different products.

6. **Schema type drives generation.** When `schema_type` is declared, the product definition is the input contract for Agent Artifact. The agent generates physical artifacts scoped to the product's entity list and constrained by its governance and masking rules.

7. **Products do not define structure.** Products reference canonical entities — they do not redefine attributes, types, or constraints. If a consumer needs a derived attribute, it should be modelled as a canonical attribute or transformation first.

8. **Source field for source-aligned.** Source-aligned products use `source` instead of `entities`. The value must match a source system folder under `sources/`.

9. **Two-layer compliance.** Every data product must appear in both the domain file summary table and a detail file. The domain file is the index; the detail file is the contract.

10. **Name uniqueness.** Data product names must be unique within a domain. The level-3 heading is the product's identity in the Knowledge Graph.
