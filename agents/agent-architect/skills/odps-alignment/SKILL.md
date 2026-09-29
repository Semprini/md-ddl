---
name: odps-alignment
description: Map MD-DDL data product declarations to Open Data Product Specification (ODPS) v4.0 YAML manifests for external cataloguing, marketplace publication, and cross-platform interoperability. Use when the user wants to publish data products, generate ODPS YAML, or align with external data product standards.
---

# ODPS Alignment

## Purpose

This skill translates MD-DDL data product declarations into ODPS v4.0 compliant
YAML manifests. ODPS (Open Data Product Specification) is a Linux Foundation
standard for machine-readable data product metadata, enabling interoperability
across catalogues, marketplaces, and governance platforms.

MD-DDL captures the structural and governance intent of a data product. ODPS
captures the publication, access, quality, licensing, and commercial metadata.
This skill bridges the two — extracting what ODPS needs from MD-DDL and flagging
what requires additional business input.

## Load ODPS Reference

Read `references/odps-v4.0.md` (field names and enum vocabularies) before generating manifests.

## Pre-Requisites

Before generating an ODPS manifest, confirm:

1. **MD-DDL data product declarations exist** — product detail files with YAML metadata
2. **Domain file** has a `## Data Products` summary table listing the products
3. **Domain governance** defaults are declared

If product declarations don't exist yet, switch to the Product Design skill first.

## Mapping Process

### Step 1 — Read the MD-DDL Product

Load the product's detail file and extract:

- Product name (level-3 heading)
- Description (prose after heading)
- Class (source-aligned, domain-aligned, consumer-aligned)
- Schema type (if declared)
- Owner
- Consumers
- Status
- Version
- Entities list
- Governance (domain defaults + product overrides)
- Masking rules
- SLA
- Refresh cadence

### Step 2 — Map to ODPS Structure

Use the mapping table below to translate MD-DDL fields to ODPS components.

#### Core Mapping Table

MD-DDL Field | ODPS Component | Mapping Notes
--- | --- | ---
Product name | `product.details.en.name` | Direct mapping
Description | `product.details.en.description` | Direct mapping
`class` | `product.details.en.type` | `source-aligned` → `raw data`; `domain-aligned` → `dataset`; `consumer-aligned` → `derived data`
`status` | `product.details.en.status` | `Draft` → `draft`; `Active` → `production`; `Deprecated` → `sunset`; `Retired` → `retired`
`version` | `product.details.en.productVersion` | Direct mapping
`owner` | `product.dataHolder.en.email` | Owner email maps to dataHolder contact
`consumers` | `product.details.en.visibility` | If consumers are named internal teams → `organisation`; if cross-org → `dataspace`; if public → `public`
`entities` | `product.details.en.description` | Entity list is included in the description. No direct ODPS field for entity-level scoping.
`schema_type` | `product.dataAccess.default.outputPorttype` and `format` | `schema_type` suggests the channel but doesn't decide it. For example: dimensional or normalized warehouse tables → port `SQL`; a file export → port `file` with a CSV or Parquet format; knowledge-graph → port `API` with `GraphQL`. ODPS `format` describes a payload or file (JSON, CSV, Parquet, GraphQL); for a `SQL` port there's no payload format, so omit `format` and put the table or view reference in the access details. Propose a channel and mark it `# TODO: confirm delivery channel`.

#### Governance → ODPS Mapping

MD-DDL Governance | ODPS Component | Mapping Notes
--- | --- | ---
`classification` | `product.license.en.scope.restrictions` | Maps to access restrictions text
`pii: true` | `product.license.en.governance.confidentiality` | Drives confidentiality clause
`retention` | `product.license.en.termination.terminationConditions` | Retention period as licence termination condition
`masking` strategies | `product.license.en.scope.restrictions` | Masking requirements documented in restrictions

#### SLA → ODPS Mapping

MD-DDL SLA | ODPS SLA Dimension | Mapping Notes
--- | --- | ---
`sla.availability` | `SLA.declarative.default.dimensions[uptime]` | Parse percentage value
`sla.freshness` | `SLA.declarative.default.dimensions[updateFrequency]` | Parse time value and unit. `sla.freshness` takes precedence; fall back to the `refresh` cadence (below) only when no freshness is declared.
`sla.latency_p99` | `SLA.declarative.default.dimensions[responseTime]` | Parse milliseconds value

#### Refresh → ODPS Mapping

MD-DDL `refresh` | ODPS `updateFrequency` objective | ODPS unit
--- | --- | ---
`real-time` | `1` | `minutes`
`hourly` | `60` | `minutes`
`daily` | `1` | `days`
`weekly` | `7` | `days`
`on-demand` | *(omit — no scheduled frequency)* |

### Step 3 — Generate ODPS YAML

Produce the ODPS manifest following this structure. Mark fields that require
business input beyond MD-DDL with `# TODO: [what's needed]`.

```yaml
schema: https://opendataproducts.org/v4.0/schema/odps.yaml
version: "4.0"                 # a string in ODPS; unquoted YAML parses as a number
product:
  details:
    en:
      name: "[from MD-DDL product name]"
      productID: "[generate: kebab-case of product name]"
      description: "[from MD-DDL product description + entity list summary]"
      visibility: "[mapped from consumers scope]"
      status: "[mapped from MD-DDL status]"
      type: "[mapped from MD-DDL class]"
      productVersion: "[from MD-DDL version]"
      categories:
        - "[from MD-DDL domain name]"
      tags:
        - "[derived from entity names and domain]"

  SLA:
    declarative:
      default:
        name:
          en: "Default SLA"
        description:
          en: "Service level agreement for [product name]"
        dimensions:
          # mapped from MD-DDL sla fields
          - dimension: uptime
            displaytitle:
              en: Availability
            objective: # from sla.availability percentage
            unit: percent
          - dimension: updateFrequency
            displaytitle:
              en: Data Freshness
            objective: # from refresh cadence
            unit: minutes
    support:
      email: "[from MD-DDL owner]"
      # TODO: Add phone support details

  dataQuality:
    declarative:
      default:
        displaytitle:
          en: "Default Data Quality"
        description:
          en: "Data quality expectations for [product name]"
        dimensions:
          # Derive from entity constraints — see inference rules below
          - dimension: completeness
            displaytitle:
              en: Data Completeness
            objective: # see constraint-based inference
            unit: percentage
          - dimension: validity
            displaytitle:
              en: Data Validity
            objective: # see constraint-based inference
            unit: percentage

  dataAccess:
    default:
      name:
        en: "Default access to [product name]"
      description:
        en: "[from MD-DDL product description]"
      outputPorttype: "[mapped from schema_type]"
      format: "[mapped from schema_type]"
      # TODO: Provide access URL for the published endpoint or file location
      # TODO: Specify authentication method (API key, OAuth, IAM role, etc.)
      # TODO: Add schema specification URL or inline schema reference

  license:
    en:
      scope:
        definition: "[TODO: Define license purpose]"
        restrictions: "[from governance classification and masking rules]"
        geographicalArea:
          - "[TODO: Define geographical scope]"
        permanent: false
        exclusive: false
      termination:
        terminationConditions: "[from governance retention period]"
      governance:
        confidentiality: "[from governance PII and classification]"
        # TODO: Add ownership, warranties, applicable laws

  dataHolder:
    en:
      legalName: "[TODO: Organisation legal name]"
      email: "[from MD-DDL owner]"
      # TODO: Add business details (address, URL, taxID)
```

### Step 4 — Infer Data Quality Dimensions

MD-DDL declares *which* quality rules exist (constraints, identifiers, temporal
tracking), not target percentages. Use the rules below to propose which dimensions to
include and a starting objective. Mark every inferred objective
`# PROPOSED: confirm with the product owner`, because the numbers are heuristics, not
facts derived from the model. Where Agent Test runs the product's data tests, their
pass rates are the better evidence for setting objectives.

#### Constraint-Based Inference Rules

MD-DDL Constraint | ODPS Dimension | Inference Logic
--- | --- | ---
`not_null` on attributes | `completeness` | Count NOT NULL attributes / total attributes across product entities. If >80% are NOT NULL → objective: 95. If >50% → objective: 90. If <50% → objective: 85.
`check` constraints | `validity` | Presence of CHECK constraints implies data rules exist. Set objective: 95 (high confidence in source validation).
`identifier: primary`, `identifier: alternate`, or `unique` | `uniqueness` | Keys imply one row per instance. Add a uniqueness dimension with a proposed objective of 99.
`temporal.tracking` declared | `timeliness` | If entities declare temporal tracking, infer a timeliness dimension. Map `refresh` cadence: `real-time` → objective 1 minute; `hourly` → 60 minutes; `daily` → 24 hours.
`pii: true` on entities | `accuracy` | Propose an accuracy dimension, since errors in personal data carry regulatory risk. Leave the objective for the owner to set.
No constraints found | Generic fallback | Use completeness: 90 as baseline. Add TODO for user to define explicit DQ dimensions.

#### Example Inference

Given a product including `Customer` entity with:

- 12 attributes, 8 marked NOT NULL → completeness objective: 95%
- `Customer Number` is the primary identifier → uniqueness objective: 99%
- `pii: true`, `pii_fields: [Full Name, Date of Birth, Tax ID]` → accuracy dimension, objective left for the owner
- `refresh: daily` → timeliness objective: 24 hours

Generated ODPS:

```yaml
dataQuality:
  declarative:
    default:
      dimensions:
        - dimension: completeness
          displaytitle:
            en: Data Completeness
          objective: 95        # PROPOSED: confirm with the product owner
          unit: percentage
        - dimension: uniqueness
          displaytitle:
            en: Record Uniqueness
          objective: 99        # PROPOSED: confirm with the product owner
          unit: percentage
        - dimension: accuracy
          displaytitle:
            en: Data Accuracy
          objective:           # TODO: set by the product owner (PII present)
          unit: percentage
        - dimension: timeliness
          displaytitle:
            en: Data Timeliness
          objective: 1440      # from refresh: daily
          unit: minutes
```

**PII without masking.** If the product exposes PII-bearing attributes (entity or
attribute `pii: true`) and declares no `masking`, don't publish silently. List it
first under gaps and hand it to Agent Governance for a Level 4 review before the
manifest goes to a catalogue.

### Step 5 — Identify Gaps

After generating, clearly list:

1. **Automatically mapped** — Fields populated from MD-DDL (no user action needed)
2. **Requires business input** — ODPS fields with no MD-DDL equivalent (marked TODO)
3. **Optional enrichment** — ODPS features the user may want to add (pricing plans,
   payment gateways, data contracts, use cases, recommended products)

Present gaps as an actionable checklist:

```markdown
## ODPS Manifest Gaps

### Requires Business Input
- [ ] `dataHolder.legalName` — Organisation's legal name
- [ ] `license.scope.definition` — Purpose statement for the licence
- [ ] `license.scope.geographicalArea` — Jurisdictions where product is available
- [ ] `license.governance.applicableLaws` — Governing legal framework
- [ ] `dataAccess.default.accessURL` — Endpoint or download URL
- [ ] `dataAccess.default.authenticationMethod` — How consumers authenticate
- [ ] `support.phoneNumber` — Phone support contact

### Optional Enrichment
- [ ] `pricingPlans` — Define pricing if product will be monetised
- [ ] `paymentGateways` — Configure payment processing
- [ ] `contract` — Link to or inline a data contract (ODCS/DCS)
- [ ] `details.useCases` — Document use cases for catalogue presentation
- [ ] `details.recommendedDataProducts` — Cross-link related products
- [ ] `dataQuality.executable` — Add monitoring-as-code rules (SodaCL, DQOps)
- [ ] `SLA.executable` — Add SLA monitoring logic (Prometheus, etc.)
```

## Multi-Product Manifests

When a domain has multiple data products, generate one ODPS manifest per product.
Each manifest is a standalone YAML file.

**Naming convention:** `odps-[product-name-kebab-case].yaml`

**File location:** Place generated manifests in `generated/odps/` under the domain folder.

## ODPS Feature Coverage

The following ODPS components can be fully or partially populated from MD-DDL:

ODPS Component | MD-DDL Coverage | Notes
--- | --- | ---
`details` | High | Name, description, status, type, version all map directly
`SLA` | Medium | Availability, freshness, latency map; support details need input
`dataQuality` | Low | MD-DDL doesn't define DQ dimensions; infer from entity constraints
`dataAccess` | Medium | Output type maps from schema_type; URLs and auth need input
`license` | Medium | Governance and retention map; legal text needs input
`dataHolder` | Low | Only owner email maps; org details need input
`pricingPlans` | None | No MD-DDL equivalent — fully requires business input
`paymentGateways` | None | No MD-DDL equivalent — fully requires business input
`contract` | None | No MD-DDL equivalent — requires contract management input

## Quality Checklist

Before declaring an ODPS manifest complete:

- [ ] Schema URL is `https://opendataproducts.org/v4.0/schema/odps.yaml`
- [ ] Version is the string `"4.0"`
- [ ] Units come from the reference: SLA uses `percent` and time units (`minutes`, `days`, …); data-quality dimensions use `percentage`
- [ ] Product name, productID, visibility, status, and type are populated (ODPS required fields)
- [ ] All TODO markers have been reviewed with the user
- [ ] SLA dimensions have valid objectives and units
- [ ] Data access format matches the product's schema_type
- [ ] License governance reflects the product's PII and classification posture
- [ ] File is valid YAML
