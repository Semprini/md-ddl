---
name: product-design
description: Design and declare MD-DDL data products from an existing domain model. Use when the user wants to create, update, or review data product declarations — choosing product class, schema type, designing logical models and lineage, entity scope, governance overrides, masking strategies, attribute mappings, or SLA. Also use when populating the domain file Data Products summary table.
---

# Product Design

## Pre-Requisites

Before designing data products, confirm these exist and are reviewed:

1. **Domain file** with declared entities, relationships, and events
2. **Entity detail files** with YAML attribute definitions
3. **Domain-level governance** defaults (classification, retention, PII posture)

If any of these are missing, defer to Agent Ontology before proceeding.

## Load the Specification

Read `md-ddl-specification/9-Data-Products.md` for normative rules.

Platform note: `{{INCLUDE}}` blocks are only processed by include-aware
platforms (for example, VS Code Copilot custom agents). In other platforms,
load the file path above directly.

## Product Design Process

### Step 1 — Inventory the Domain

Read the domain file and build a mental model:

- What entities exist and what are their existence/mutability characteristics?
- What relationships connect them?
- What events capture state changes?
- What source systems feed the domain?
- What governance defaults are declared?
- Do any data products already exist?

### Step 2 — Establish Platform Posture

Check the domain's `platform` metadata block. If present, use it to scope the
design. If absent, ask the platform posture question (see Agent Architect
Mode 2 — Assessment).

Platform posture affects design decisions throughout this process:

- **Single-platform:** All product classes generate for the same target. Schema
  type choices map directly to platform-native constructs.
- **Polyglot:** Each product class may target a different platform. Source-aligned
  products may use streaming/CDC constructs rather than batch tables.
  Domain-aligned products may need both analytical and operational interfaces.
  Consumer-aligned products target the consumer's query engine.
- **Selective:** Skip product classes the org does not recognise. If
  `product_scope` excludes `source-aligned`, do not propose source-aligned
  products — the source layer is infrastructure, not a governed product.

If the platform posture is not yet in the domain metadata, propose adding it.

### Step 3 — Identify Consumers

Ask the user:

> "Who consumes data from this domain? For each consumer, tell me:
> 1. Their name (team, system, report, or regulatory body)
> 2. What they need (which entities/attributes)
> 3. How they consume it (API, dashboard, batch file, regulatory submission)
> 4. How fresh it needs to be (real-time, hourly, daily, on-demand)"

Group consumers by access pattern — consumers with similar needs may share a product.

### Step 4 — Choose Product Class

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

### Step 5 — Define Entities and Lineage

For each product, determine what it publishes (`entities`) and where data comes from (`lineage`):

- **Source-aligned:** No `entities` or `lineage` — use `source` field referencing a source system folder.
- **Domain-aligned:** `entities` lists the canonical entities projected by this product. `lineage` traces to source system tables (referencing `sources/` transforms).
- **Consumer-aligned:** `entities` lists the product's own entities — which may differ from canonical entities when the product reshapes or denormalizes. `lineage` traces to canonical entities from one or more domains. Consumer-aligned products source exclusively from canonical products — never from source systems.

**Entity rules:**

- Only include entities the consumer actually needs. A product is not a "select all" view.
- For consumer-aligned wide-column products, the product typically defines a single denormalized entity (e.g., `Transaction Risk Summary`) even though it sources from many canonical entities.
- For consumer-aligned normalized products, the product entities may share names with canonical entities but represent projections with selected attribute subsets.

**Lineage rules:**

- Domain-aligned lineage must reference source system folders and tables that exist under `sources/`.
- Consumer-aligned lineage must reference domain names and entities that exist in those domains' `## Entities` tables.
- Consumer-aligned products never reference source systems in lineage — they source from canonical products only.

### Step 6 — Choose Schema Type

Every data product must declare a `schema_type`. Recommend based on the consumption pattern:

Consumption Pattern | Recommended `schema_type`
--- | ---
Analytical queries with dimensions and measures | `dimensional`
Operational integration, master data, multi-system sync | `normalized`
Dashboard, scan queries, join-minimised consumption | `wide-column`
Graph traversal, relationship-centric exploration | `knowledge-graph`

Domain-aligned products default to `normalized` because their shape matches the
canonical model structure.

### Step 7 — Set Governance Overrides

Products inherit governance from the domain by default. Only declare overrides when
the product requires different controls:

Governance Field | When to Override
--- | ---
`classification` | Product exposes a subset of data at a lower classification than the domain default
`pii` | Product includes or excludes PII-bearing entities compared to domain default
`retention` | Product has a different retention requirement (e.g., regulatory report kept longer)
`masking` | Product needs attribute-level masking for PII exposure

#### Multi-Domain Governance Conflicts

For consumer-aligned products with multi-domain `lineage`, governance may conflict
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

### Step 8 — Declare Consistency Posture, SLA, and Refresh

#### Consistency Posture

Before setting the freshness SLA, ask the user:

> "Does this product require **strong consistency** (all sources must propagate
> before the product updates) or **eventual consistency** (sources propagate
> independently; the product converges within a declared window)?"

Use the source systems' declared `change_model` values to guide the answer:
- If all sources are `real-time-cdc` and the product can wait for all → **strong**
- If sources have mixed cadences (e.g., one `real-time-cdc`, one `batch-intraday`) → **eventual**

Record the decision as a comment in the product YAML:

```yaml
# Consistency posture: eventual (convergence SLA: < 1 hour)
# Consistency posture: strong (synchronous propagation required)
```

#### Null Strategy Under Eventual Consistency

If the user chooses eventual consistency, also decide the null strategy for
partially-received rows — rows where some source attributes have arrived but
others have not yet propagated:

| Strategy | Description | Physical schema implication |
| --- | --- | --- |
| `nullable-staging` | Partial rows inserted with `NULL`s; a view enforces completeness for consumers | `NOT NULL` on view, `NULL` in staging table |
| `reject-partial` | Application blocks insert until all sources have contributed | `NOT NULL` on base table — effectively strong consistency |
| `nullable-final` | Schema accepts `NULL` permanently; convergence window is advisory | `NULL` allowed on base table; consumers handle nulls |

Add the null strategy as a comment alongside the consistency posture:

```yaml
# Null strategy: nullable-staging (partial rows in base; converged view for consumers)
```

**Important:** Communicate both the consistency posture and null strategy to
Agent Artifact in your handoff note. Agent Artifact's DDL skills generate `NOT NULL`
constraints from the entity's `not_null` attribute declarations — but under eventual
consistency with `nullable-staging`, those columns must be nullable in the base
table and enforced only at the view layer. Without this signal, Agent Artifact
will generate physically incorrect DDL.

#### SLA and Refresh

For products serving operational consumers, declare:

```yaml
sla:
  freshness: "< 15 minutes"
  availability: "99.9%"
  latency_p99: "< 200ms"

refresh: real-time
```

For eventual-consistency products, set `freshness` to the declared convergence
window (e.g., `"< 1 hour"` if the slowest source is `batch-intraday` at 60 min).

SLA fields are informational — they document expectations without generating
runtime enforcement.

Refresh options: `real-time`, `hourly`, `daily`, `weekly`, `on-demand`.

### Step 9 — Write the Product Declaration

Produce the MD-DDL product declaration following this structure:

````markdown
### [Product Name]

[One or two sentences describing what this product provides and for whom.]

```yaml
class: [source-aligned | domain-aligned | consumer-aligned]
schema_type: [normalized | dimensional | wide-column | knowledge-graph]
owner: [team or individual email]
consumers:
  - [Consumer 1]
  - [Consumer 2]
status: [Draft | Active | Deprecated]
version: "[semver]"

entities:                    # or 'source:' for source-aligned
  - [Entity 1]
  - [Entity 2]

lineage:                     # domain-aligned: source tables; consumer-aligned: canonical entities
  - source: [source-id]     # for domain-aligned
    tables:
      - [transform_file]
  - domain: [Domain Name]   # for consumer-aligned
    entities:
      - [Entity]

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
```
````

### Step 10 — Create the Logical Model

Every product must include a `#### Logical Model` section with a Mermaid class diagram.

**Domain-aligned products:** Project the canonical model. Show each entity as a class
with all its attributes and types, inheritance and association cardinalities. Hyperlink
entity names to their detail files — the diagram is a view into the canonical model.

**Consumer-aligned products:** Define the product's own structure. The shape depends on
the schema type:
- **wide-column:** A single class with all flattened attributes and their types
- **normalized:** Multiple classes preserving entity boundaries with selected attributes
- **dimensional:** Fact and dimension classes with their attributes

For consumer-aligned products, follow the logical model with an `#### Attribute Mapping`
section using the same table-based format as source transform files. This creates a
consistent lineage format from source through canonical to product.

- **Wide-column products**: a single flat table with columns
  `Product Attribute | Source | Path | Transform`. Source is the canonical
  `Entity.Attribute`. Path is the relationship traversal from the product's grain.
  Transform links to a breakout section for non-direct mappings.
- **Dimensional products**: one table per fact or dimension entity under a level-5
  heading, with columns `Product Attribute | Source | Path | Transform`. The Path
  column captures foreign key lookups in the fact table (e.g., traversing from
  Usage Record through Service and Subscription to reach Customer). Dimensions
  that map directly to canonical entities use `—` in the Path column.
- **Normalized products** (and knowledge-graph): one table per product entity under
  a level-5 heading, with columns `Product Attribute | Source | Transform`. No Path
  column is needed because entity boundaries are preserved. If an individual entity
  includes attributes traversed from another entity, that entity's table may use the
  4-column format with Path. Cross-domain attributes are prefixed with the domain
  name (e.g., `Healthcare.Patient.Given Name`).

Direct mappings place the canonical `Entity.Attribute` in the Source column with an
empty Transform cell. Non-direct mappings link to a breakout section
(e.g., `[Derive Risk Category](#derive-risk-category)`) in the Transform column,
with the transformation logic defined using the same YAML types as source transforms
(`derived`, `conditional`, `lookup`, `aggregation`).

Domain-aligned products do not need an attribute mapping because their entities are
identity projections of the canonical model — the mapping is implicit.

### Step 11 — Update the Domain Summary Table

Add or update the entry in the domain file's `## Data Products` section:

```markdown
Name | Class | Consumers | Status
--- | --- | --- | ---
[Product Name](products/[file].md#[anchor]) | [class] | [Primary Consumer] | [Status]
```

The anchor is the product name in lowercase with spaces replaced by hyphens.

## Domain Lifecycle Awareness

Data products inherit lifecycle context from their parent domain. When designing
or reviewing products, apply these lifecycle-aware rules:

### Status Propagation

- A product's `status` should not be more advanced than its parent domain's `status`.
  A product cannot be `Active` in a `Draft` or `Review` domain.
- When a domain transitions to `Deprecated`, flag all products within that domain.
  Products built on a deprecated domain should either be deprecated themselves or
  declare a documented `migration_note`.
- When a domain transitions to `Retired`, all products must be `Retired`.

### Domain Status and Product Design

Domain Status | Product Design Guidance
--- | ---
`Draft` | Products may be sketched for planning but should be `Draft`. Do not declare `Active` products against a draft domain.
`Review` | Products may be declared as `Draft` to support review feedback. Warn the user that breaking changes to the domain are still possible.
`Active` | Normal product design applies. Products may be `Draft` or `Active`.
`Deprecated` | Do not create new products. Existing products should be reviewed for migration. Flag any `Active` product on a deprecated domain as a lifecycle inconsistency unless it carries a `migration_note`.
`Retired` | No products should be active. All must be `Retired`.

### Multi-Domain Lifecycle Checks

For consumer-aligned products with multi-domain `lineage`:

- Check the `status` of each domain referenced in `lineage`. If any is
  `Deprecated`, warn the user that the product depends on a deprecated domain
  and recommend planning for migration.
- If a referenced domain is `Retired`, the lineage reference is invalid.
  The product must remove the reference or be retired itself.

### Version Alignment

- Products should declare their own `version` field using semantic versioning.
- When the parent domain undergoes a major version bump (breaking change), review
  all products for impact. Products that include affected entities will likely
  need their own version bump.
- Use product versioning semantics from the Data Products spec:
  - major = breaking consumer contract change
  - minor = additive schema or contract expansion
  - patch = corrective or descriptive change with no consumer break
- Record promotions, version bumps, deprecations, and retirements in the owning
  domain's `LIFECYCLE.md` when that file exists.

---

## Quality Checklist

Before declaring a product complete, verify:

- [ ] Class is appropriate for the consumer's needs
- [ ] `schema_type` is declared
- [ ] `entities` lists what the product publishes (canonical entities for domain-aligned, product's own entities for consumer-aligned)
- [ ] `lineage` is declared for all non-source-aligned products
- [ ] Consumer-aligned `lineage` references canonical entities only (no source system references)
- [ ] Multi-domain lineage is only used on consumer-aligned products
- [ ] Logical model (Mermaid class diagram) is present with sufficient detail for generation
- [ ] Consumer-aligned products include `#### Attribute Mapping` tables tracing every attribute to canonical source
- [ ] Governance overrides are genuine differences from domain defaults (not duplicates)
- [ ] Multi-domain products resolve governance conflicts (classification, retention, PII, regulatory scope)
- [ ] Masking strategies are appropriate for the sensitivity level and consumer access
- [ ] Source-aligned products use `source` field, not `entities`
- [ ] Product appears in both domain summary table and detail file
- [ ] Product name is unique within the domain
- [ ] Description clearly states what the product provides and for whom
- [ ] Status is a valid lifecycle state (`Draft`, `Active`, `Deprecated`, `Retired`)
- [ ] Product status is not more advanced than the parent domain status
- [ ] No lineage references point to `Deprecated` or `Retired` domains without justification
- [ ] Deprecated products include `deprecated_date` and ideally `successor`

## Product Review

When reviewing existing products, check for:

- **Scope creep:** Products that include entities the consumer doesn't actually need
- **Missing products:** Consumer groups that don't have a product serving them
- **Stale status:** Products marked `Active` that are no longer consumed
- **Version drift:** Products whose version does not reflect a known upstream domain change
- **Governance drift:** Products whose governance overrides no longer match current policy
- **Orphaned products:** Products in detail files that are missing from the domain summary table (or vice versa)

## Product Lifecycle Mode

When managing existing products, apply the lifecycle rules from the Data Products
specification:

### Mode Triggers

Use lifecycle mode when the user asks to promote a product, bump a product version,
deprecate or retire a product, or assess the impact of an upstream domain version bump.

### Status Transitions

Transition | Required Actions
--- | ---
Draft → Active | All quality checklist items pass; governance overrides reviewed; parent domain status supports activation; product version is `1.0.0` or higher; at least one named consumer is declared
Active → Deprecated | Add `deprecated_date` to metadata; add `successor` if a replacement exists; add `migration_note` when consumers need an interim migration path
Deprecated → Retired | Add `sunset_date` to metadata; confirm no active consumers remain; product remains in detail file for audit

### Version Bump Workflow

When a user changes a product directly, or when Agent Ontology provides an
`affected_products` block after a domain version bump:

1. Identify the contract change:
  - removing an entity or reducing scope = breaking
  - adding an entity or additive upstream change = additive
  - masking/SLA/consumer change without contract break = minor or patch
2. Propose the new product version.
3. Update product metadata and the domain summary table if status changes.
4. If the domain maintains `LIFECYCLE.md`, append or update the product's current
  status/version snapshot there.

### Managing Deprecation

When a user deprecates a product:

1. Set `status: Deprecated` and add `deprecated_date`
2. If a replacement exists, add `successor: "[New Product Name]"`
3. If the product remains available while upstream domains or entities are deprecated, add `migration_note`
4. Update the domain summary table status
5. Identify consumers that need to migrate — review the `consumers` list

### Retired Products

Retired products are immutable records. Do not delete them from detail files.
They remain as lineage evidence. If a similar product is needed later, create
a new product with a new name — do not revive a retired product.
