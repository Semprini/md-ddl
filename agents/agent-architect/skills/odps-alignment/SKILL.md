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

Read `skills/odps-alignment/references/odps-v4.0.md` before generating manifests.

Platform note: `{{INCLUDE}}` blocks are only processed by include-aware
platforms (for example, VS Code Copilot custom agents). In other platforms,
open the reference file directly.

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
`status` | `product.details.en.status` | `Draft` → `draft`; `Production` → `production`; `Deprecated` → `sunset`
`version` | `product.details.en.productVersion` | Direct mapping
`owner` | `product.dataHolder.en.email` | Owner email maps to dataHolder contact
`consumers` | `product.details.en.visibility` | If consumers are named internal teams → `organisation`; if cross-org → `dataspace`; if public → `public`
`entities` | `product.details.en.description` | Entity list is included in the description. No direct ODPS field for entity-level scoping.
`schema_type` | `product.dataAccess.default.format` | `normalized` → `JSON`; `dimensional` → `SQL`; `wide-column` → `CSV` or `Parquet`; `knowledge-graph` → `GraphQL`

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
`sla.freshness` | `SLA.declarative.default.dimensions[updateFrequency]` | Parse time value and unit
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
version: 4.0
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

Before marking data quality as TODO, attempt to derive ODPS dimensions from
MD-DDL entity constraints. This reduces the number of TODOs and produces a
more useful starting manifest.

#### Constraint-Based Inference Rules

MD-DDL Constraint | ODPS Dimension | Inference Logic
--- | --- | ---
`not_null` on attributes | `completeness` | Count NOT NULL attributes / total attributes across product entities. If >80% are NOT NULL → objective: 95. If >50% → objective: 90. If <50% → objective: 85.
`check` constraints | `validity` | Presence of CHECK constraints implies data rules exist. Set objective: 95 (high confidence in source validation).
`unique` constraints | `uniqueness` | Presence of UNIQUE key attributes implies deduplication. Add a uniqueness dimension with objective: 99.
`temporal.tracking` declared | `timeliness` | If entities declare temporal tracking, infer a timeliness dimension. Map `refresh` cadence: `real-time` → objective 1 minute; `hourly` → 60 minutes; `daily` → 24 hours.
`pii: true` on entities | `accuracy` | PII-bearing entities typically require higher accuracy. Add accuracy dimension with objective: 98 when PII is present.
No constraints found | Generic fallback | Use completeness: 90 as baseline. Add TODO for user to define explicit DQ dimensions.

#### Example Inference

Given a product including `Customer` entity with:

- 12 attributes, 8 marked NOT NULL → completeness objective: 95%
- `customer_id` marked unique → uniqueness objective: 99%
- `pii: true`, `pii_fields: [Full Name, Date of Birth, Tax ID]` → accuracy objective: 98%
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
          objective: 95
          unit: percentage
        - dimension: uniqueness
          displaytitle:
            en: Record Uniqueness
          objective: 99
          unit: percentage
        - dimension: accuracy
          displaytitle:
            en: Data Accuracy
          objective: 98
          unit: percentage
        - dimension: timeliness
          displaytitle:
            en: Data Timeliness
          objective: 24
          unit: hours
```

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
- [ ] Version is `4.0`
- [ ] Product name, productID, visibility, status, and type are populated (ODPS required fields)
- [ ] All TODO markers have been reviewed with the user
- [ ] SLA dimensions have valid objectives and units
- [ ] Data access format matches the product's schema_type
- [ ] License governance reflects the product's PII and classification posture
- [ ] File is valid YAML
