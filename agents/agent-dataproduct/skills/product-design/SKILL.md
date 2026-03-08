---
name: product-design
description: Design and declare MD-DDL data products from an existing domain model. Use when the user wants to create, update, or review data product declarations — choosing product class, schema type, entity scope, governance overrides, masking strategies, cross-domain references, or SLA. Also use when populating the domain file Data Products summary table.
---

# Product Design

## Pre-Requisites

Before designing data products, confirm these exist and are reviewed:

1. **Domain file** with declared entities, relationships, and events
2. **Entity detail files** with YAML attribute definitions
3. **Domain-level governance** defaults (classification, retention, PII posture)

If any of these are missing, defer to Agent Ontology before proceeding.

## Load the Specification

Read the data products specification for normative rules:

<data_products_spec>
{{INCLUDE: ../../../md-ddl-specification/9-Data-Products.md}}
</data_products_spec>

## Product Design Process

### Step 1 — Inventory the Domain

Read the domain file and build a mental model:

- What entities exist and what are their existence/mutability characteristics?
- What relationships connect them?
- What events capture state changes?
- What source systems feed the domain?
- What governance defaults are declared?
- Do any data products already exist?

### Step 2 — Identify Consumers

Ask the user:

> "Who consumes data from this domain? For each consumer, tell me:
> 1. Their name (team, system, report, or regulatory body)
> 2. What they need (which entities/attributes)
> 3. How they consume it (API, dashboard, batch file, regulatory submission)
> 4. How fresh it needs to be (real-time, hourly, daily, on-demand)"

Group consumers by access pattern — consumers with similar needs may share a product.

### Step 3 — Choose Product Class

For each distinct consumer group, determine the product class:

Question | If Yes → Class
--- | ---
Does the consumer need raw source data for audit, replay, or debugging? | **source-aligned**
Does the consumer need the canonical model in its modelled form? | **domain-aligned**
Does the consumer need data reshaped, denormalized, aggregated, or combined from multiple entities? | **consumer-aligned**

**Decision rules:**

- Start with **domain-aligned** as the default for internal integration consumers.
  Only create consumer-aligned when the canonical shape genuinely doesn't serve
  the consumer's query patterns.
- **Source-aligned** products are for data engineering and audit — not for business
  consumers. Each maps to exactly one source system from `## Source Systems`.
- **Consumer-aligned** is where most design effort goes. This is where you choose
  schema type, masking, and cross-domain scope.

### Step 4 — Scope Entities

For each product, determine which entities to include:

- **Source-aligned:** No `entities` field — use `source` field referencing a source system folder.
- **Domain-aligned:** List canonical entities from the owning domain only.
- **Consumer-aligned:** List entities needed by the consumer. If entities from other
  domains are required, declare them in `cross_domain`.

**Entity inclusion rules:**

- Only include entities the consumer actually needs. A product is not a "select all" view.
- If a consumer needs attributes from a related entity (e.g., Branch name for a
  Transaction), include both entities — the schema_type skill will handle the join
  or denormalization.
- Every entity in the list must exist in the domain's `## Entities` table or in a
  declared `cross_domain` domain.

### Step 5 — Choose Schema Type

For consumer-aligned products, recommend a `schema_type` based on the consumption pattern:

Consumption Pattern | Recommended `schema_type`
--- | ---
Analytical queries with dimensions and measures | `dimensional`
Operational integration, master data, multi-system sync | `normalized`
Dashboard, scan queries, join-minimised consumption | `wide-column`
Graph traversal, relationship-centric exploration | `knowledge-graph`

If the product is logical-only (documenting what is published without triggering
generation), omit `schema_type`.

Domain-aligned products typically do not declare `schema_type` because their shape
matches the canonical model. If a domain-aligned product needs physical generation,
`normalized` is the default.

### Step 6 — Set Governance Overrides

Products inherit governance from the domain by default. Only declare overrides when
the product requires different controls:

Governance Field | When to Override
--- | ---
`classification` | Product exposes a subset of data at a lower classification than the domain default
`pii` | Product includes or excludes PII-bearing entities compared to domain default
`retention` | Product has a different retention requirement (e.g., regulatory report kept longer)
`masking` | Product needs attribute-level masking for PII exposure

#### Cross-Domain Governance Conflicts

For consumer-aligned products with `cross_domain` references, governance may conflict
between the owning domain and referenced domains. Apply these resolution rules:

1. **Read each referenced domain's governance defaults** before setting overrides.
2. **Classification: highest wins.** The product's classification must be at least as
   restrictive as the highest classification among all contributing domains. If you
   declare a lower classification, add a justification comment explaining why (e.g.,
   masking renders data non-sensitive).
3. **Retention: longest wins.** The product's retention must meet the longest period
   required by any contributing domain's regulatory obligations.
4. **PII: union of obligations.** If any contributing domain declares `pii: true`,
   the product must either declare `pii: true` with masking entries, or demonstrate
   that masking eliminates the PII obligation.
5. **Regulatory scope: union of frameworks.** The product is subject to the combined
   regulatory scope of all contributing domains.

When conflicts exist, flag them explicitly in the product description or as a comment
in the governance block. Do not silently inherit weaker controls.

**Masking strategy selection:**

Strategy | Use When
--- | ---
`hash` | Need to preserve joinability across products (e.g., matching customer records)
`redact` | Value must be completely hidden
`year-only` | Date attribute where year is analytically useful but full date is PII
`truncate` | Partial value is useful (e.g., postcode prefix for regional analysis)
`tokenize` | Need reversible masking with a tokenization service
`null` | Value should not appear at all in the published output

### Step 7 — Declare SLA and Refresh

For products serving operational consumers, declare:

```yaml
sla:
  freshness: "< 15 minutes"
  availability: "99.9%"
  latency_p99: "< 200ms"

refresh: real-time
```

SLA fields are informational — they document expectations without generating
runtime enforcement.

Refresh options: `real-time`, `hourly`, `daily`, `weekly`, `on-demand`.

### Step 8 — Write the Product Declaration

Produce the MD-DDL product declaration following this structure:

````markdown
### [Product Name]

[One or two sentences describing what this product provides and for whom.]

```yaml
class: [source-aligned | domain-aligned | consumer-aligned]
schema_type: [normalized | dimensional | wide-column | knowledge-graph]  # optional
owner: [team or individual email]
consumers:
  - [Consumer 1]
  - [Consumer 2]
status: [Draft | Production | Deprecated]
version: "[semver]"

entities:                    # or 'source:' for source-aligned
  - [Entity 1]
  - [Entity 2]

governance:                  # only if overriding domain defaults
  classification: [level]
  pii: [true/false]
  retention: "[period]"
  masking:
    - attribute: "[Attribute Name]"
      strategy: [hash | redact | year-only | truncate | tokenize | null]

sla:                         # optional, for operational consumers
  freshness: "[target]"
  availability: "[target]"

refresh: [cadence]           # optional

cross_domain:                # only for consumer-aligned spanning domains
  - domain: [Domain Name]
    entities:
      - [Entity]
```
````

### Step 9 — Update the Domain Summary Table

Add or update the entry in the domain file's `## Data Products` section:

```markdown
Name | Class | Consumers | Status
--- | --- | --- | ---
[Product Name](products/[file].md#[anchor]) | [class] | [Primary Consumer] | [Status]
```

The anchor is the product name in lowercase with spaces replaced by hyphens.

## Quality Checklist

Before declaring a product complete, verify:

- [ ] Class is appropriate for the consumer's needs
- [ ] Every entity in `entities` exists in the domain or `cross_domain` declaration
- [ ] `cross_domain` is only used on consumer-aligned products
- [ ] Governance overrides are genuine differences from domain defaults (not duplicates)
- [ ] Cross-domain products resolve governance conflicts (classification, retention, PII, regulatory scope)
- [ ] Masking strategies are appropriate for the sensitivity level and consumer access
- [ ] Source-aligned products use `source` field, not `entities`
- [ ] Product appears in both domain summary table and detail file
- [ ] Product name is unique within the domain
- [ ] Description clearly states what the product provides and for whom
- [ ] Status is a valid lifecycle state (`Draft`, `Production`, `Deprecated`, `Retired`)
- [ ] Deprecated products include `deprecated_date` and ideally `successor`

## Product Review

When reviewing existing products, check for:

- **Scope creep:** Products that include entities the consumer doesn't actually need
- **Missing products:** Consumer groups that don't have a product serving them
- **Stale status:** Products marked Production that are no longer consumed
- **Governance drift:** Products whose governance overrides no longer match current policy
- **Orphaned products:** Products in detail files that are missing from the domain summary table (or vice versa)

## Product Lifecycle Management

When managing existing products, apply the lifecycle rules from the Data Products
specification:

### Status Transitions

Transition | Required Actions
--- | ---
Draft → Production | All quality checklist items pass; governance overrides reviewed
Production → Deprecated | Add `deprecated_date` to metadata; add `successor` if a replacement exists; notify declared consumers
Deprecated → Retired | Add `sunset_date` to metadata; confirm no active consumers remain; product remains in detail file for audit

### Managing Deprecation

When a user deprecates a product:

1. Set `status: Deprecated` and add `deprecated_date`
2. If a replacement exists, add `successor: "[New Product Name]"`
3. Update the domain summary table status
4. Identify consumers that need to migrate — review the `consumers` list

### Retired Products

Retired products are immutable records. Do not delete them from detail files.
They remain as lineage evidence. If a similar product is needed later, create
a new product with a new name — do not revive a retired product.
