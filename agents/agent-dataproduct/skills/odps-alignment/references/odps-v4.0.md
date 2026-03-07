# ODPS v4.0 — Structure Reference

*Open Data Product Specification v4.0 — Linux Foundation standard for machine-readable
data product metadata. Released July 2025.*

*Canonical source: <https://opendataproducts.org/v4.0/>*
*YAML Schema: <https://opendataproducts.org/v4.0/schema/odps.yaml>*
*JSON Schema: <https://opendataproducts.org/v4.0/schema/odps.json>*

---

## Document Root (Required)

```yaml
schema: https://opendataproducts.org/v4.0/schema/odps.yaml
version: 4.0
product:
  # all product components below
```

Field | Type | Required | Description
--- | --- | --- | ---
`schema` | URL | Yes | URL to the ODPS YAML schema for validation
`version` | string | Yes | ODPS version (e.g., `4.0`)
`product` | object | Yes | Root element containing all product components

---

## Product Details (`product.details`)

Defines business and catalogue metadata. Language-scoped using ISO 639-1 codes.

### Required Fields

Field | Type | Description
--- | --- | ---
`details` | object | Container for product business details
`en` (or language code) | object | Language-scoped detail block
`name` | string (max 256) | Product name
`productID` | string (max 256) | Unique product identifier
`visibility` | enum | `private`, `invitation`, `organisation`, `dataspace`, `public`
`status` | enum | `announcement`, `draft`, `development`, `testing`, `acceptance`, `production`, `sunset`, `retired`
`type` | enum | `raw data`, `derived data`, `dataset`, `reports`, `analytic view`, `3D visualisation`, `algorithm`, `decision support`, `automated decision-making`, `data-enhanced product`, `data-driven service`, `data-enabled performance`, `bi-directional`

### Optional Fields

Field | Type | Description
--- | --- | ---
`valueProposition` | string (max 512) | Value statement for consumers
`description` | string | Detailed product description
`productSeries` | string | Product family grouping
`productVersion` | string (SemVer) | Version of the data product
`versionNotes` | string | Release notes
`categories` | array | Product categories
`standards` | array | Applicable standards (e.g., ISO 8000)
`tags` | array | Searchable tags
`contentSample` | URL | Sample output for preview
`logoURL` | URL | Product logo
`outputFileFormats` | array | Available output formats (JSON, XML, CSV, etc.)
`useCases` | array | Related use cases with title, description, URL
`recommendedDataProducts` | array | URLs to related ODPS products

---

## Data Contract (`product.contract`)

Links product to a formal data contract. All fields optional.

Field | Type | Description
--- | --- | ---
`id` | string | Contract UUID
`type` | enum | `ODCS` or `DCS`
`contractVersion` | string | Version of the contract standard
`contractURL` | URL | Link to contract in management system
`spec` | YAML | Inline contract definition
`$ref` | URI | External contract file reference

---

## Data SLA (`product.SLA`)

Declarative and executable service level definitions with 11 standardised dimensions.

### Dimensions

`latency`, `uptime`, `responseTime`, `errorRate`, `endOfSupport`, `endOfLife`,
`updateFrequency`, `timeToDetect`, `timeToNotify`, `timeToRepair`, `emailResponseTime`

### Structure

```yaml
SLA:
  declarative:
    default:                    # Required if SLA is used
      name:
        en: "SLA Name"
      description:
        en: "SLA Description"
      dimensions:
        - dimension: uptime
          displaytitle:
            en: Uptime
          objective: 99
          unit: percent
    premium:                    # Additional named profiles optional
      # same structure as default
  executable:                   # Optional — monitoring as code
    - dimension: uptime
      type: prometheus          # prometheus, custom, etc.
      reference: "URL to docs"
      spec: |
        # monitoring query
  support:
    phoneNumber: "+1234567890"
    email: "support@example.com"
```

### Units

`percent`, `milliseconds`, `seconds`, `minutes`, `days`, `weeks`, `months`, `years`, `never`, `date`, `null`

---

## Data Quality (`product.dataQuality`)

Declarative and executable quality definitions with 8 standardised dimensions.

### Dimensions

`accuracy`, `completeness`, `conformity`, `consistency`, `coverage`,
`timeliness`, `validity`, `uniqueness`

### Structure

```yaml
dataQuality:
  declarative:
    default:                    # Required if dataQuality is used
      displaytitle:
        en: "Quality Profile Name"
      description:
        en: "Quality Profile Description"
      dimensions:
        - dimension: accuracy
          displaytitle:
            en: Data Accuracy
          objective: 95
          unit: percentage
  executable:                   # Optional — DQ monitoring as code
    - dimension: accuracy
      type: SodaCL              # SodaCL, Montecarlo, DQOps, Custom
      reference: "URL to docs"
      spec:
        # monitoring rules
```

---

## Pricing Plans (`product.pricingPlans`)

12 standardised pricing models. Language-scoped.

### Pricing Units

`One-time-payment`, `Pay-per-use`, `Recurring`, `Revenue-sharing`, `Data-volume`,
`Pay-what-you-want`, `Freemium`, `Open-data`, `Value-based`, `On-request`, `Trial`,
`Dynamic pricing`

### Structure

```yaml
pricingPlans:
  declarative:
    en:
      - name: "Plan Name"
        priceCurrency: USD      # ISO 4217
        price: 50
        billingDuration: month  # instant, day, week, month, year
        unit: recurring
        maxTransactionQuantity: 10000
        offering:
          - "Feature 1"
          - "Feature 2"
        # References to other components
        paymentGateway:
          $ref: '#/product/paymentGateways/default'
        dataQuality:
          $ref: '#/product/dataQuality/declarative/default'
        SLA:
          $ref: '#/product/SLA/declarative/default'
        access:
          $ref: '#/product/dataAccess/API'
```

---

## Data Access (`product.dataAccess`)

Named access configurations. `default` is required if `dataAccess` is used.

### Structure

```yaml
dataAccess:
  default:
    name:
      en: "Access Method Name"
    description:
      en: "Description"
    outputPorttype: API         # file, API, SQL, AI, gRPC, sFTP, etc.
    format: JSON                # JSON, XML, CSV, Excel, zip, GraphQL, MCP
    authenticationMethod: OAuth # OAuth, Token, API key, HTTP Basic, none
    specification: OAS          # OAS, RAML, Slate, MCP
    accessURL: "https://..."
    specsURL: "https://..."
    documentationURL: "https://..."
  agent:                        # Optional — AI/MCP access
    outputPorttype: AI
    specification: MCP 2025-03-26
    format: MCP
```

---

## Data Licensing (`product.license`)

Language-scoped licensing with scope, termination, and governance sections.

### Structure

```yaml
license:
  en:
    scope:
      definition: "License purpose statement"
      restrictions: "Usage restrictions"
      geographicalArea:
        - EU
        - US
      permanent: false
      exclusive: false
      rights:
        - Reproduction
        - Display
        - Distribution
        - Adaptation
    termination:
      noticePeriod: 90          # days
      terminationConditions: "Conditions text"
      continuityConditions: "Continuity text"
    governance:
      ownership: "IP ownership statement"
      confidentiality: "Confidentiality requirements"
      applicableLaws: "Governing law"
      warranties: "Warranty disclaimer"
      audit: "Audit cooperation terms"
      forceMajeure: "Force majeure clause"
```

---

## Data Holder (`product.dataHolder`)

Organisation metadata. Language-scoped.

### Required Fields (if used)

Field | Type | Description
--- | --- | ---
`legalName` | string (max 256) | Official org name
`email` | string | Contact email
`URL` | URL | Organisation website
`streetAddress` | string | Street address

### Optional Fields

`businessId`, `taxID`, `vatID`, `telephone`, `postalCode`, `addressRegion`,
`addressLocality`, `addressCountry`, `description`, `logoURL`, `aggregateRating`,
`ratingCount`, `slogan`, `parentOrganization`

---

## Payment Gateways (`product.paymentGateways`)

Named payment configurations. `default` is required if `paymentGateways` is used.

### Structure

```yaml
paymentGateways:
  default:
    description:
      en: "Gateway description"
    type: Stripe                # Stripe, Axio, Checkout, Custom
    version: 1
    reference: "https://docs.stripe.com/"
    spec: |
      # payment integration code
```

---

## Referencing

ODPS supports `$ref` for both internal and external references:

```yaml
# Internal reference
SLA:
  $ref: '#/product/SLA/declarative/default'

# External reference
dataQuality:
  $ref: 'https://example.org/DQ/all-packages.yaml'
```

---

## Specification Extensions

Custom fields use the `x-` prefix:

```yaml
product:
  details:
    en:
      name: "My Product"
      x-internal-id: "custom-value"
```

---

## Minimal Valid ODPS Document

```yaml
schema: https://opendataproducts.org/v4.0/schema/odps.yaml
version: 4.0
product:
  details:
    en:
      name: My Data Product
      productID: my-data-product-001
      visibility: private
      status: draft
      type: dataset
```
