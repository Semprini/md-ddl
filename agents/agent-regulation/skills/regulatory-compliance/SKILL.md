---
name: regulatory-compliance
description: Apply regulatory and compliance metadata to MD-DDL entities based on applicable jurisdictions and frameworks. Use when modeling domains with regulatory requirements or when user mentions compliance, regulations, or specific regulatory bodies (APRA, RBNZ, GDPR, Basel, etc.).
---

# Regulatory Compliance

## Identify Applicable Regulators

Ask user: "What regulatory jurisdictions and compliance frameworks apply to this data?"

Common regulators by jurisdiction:

Jurisdiction | Regulators | Regulator Files to Load
-------------|-----------|------------------------
Australia/NZ Banking | APRA, RBNZ, Basel, FATF | [apra.md](regulators/apra.md), [rbnz.md](regulators/rbnz.md), [basel.md](regulators/basel.md), [fatf.md](regulators/fatf.md)
EU | GDPR, Basel, EBA | [gdpr.md](regulators/gdpr.md), [basel.md](regulators/basel.md), [eba.md](regulators/eba.md)
US Banking | Federal Reserve, OCC, FDIC, Basel | [federal-reserve.md](regulators/federal-reserve.md), [occ.md](regulators/occ.md), [fdic.md](regulators/fdic.md), [basel.md](regulators/basel.md)
US General | CCPA, SOX | [ccpa.md](regulators/ccpa.md), [sox.md](regulators/sox.md)
Global AML/CTF | FATF | [fatf.md](regulators/fatf.md)
Healthcare (US) | HIPAA | [hipaa.md](regulators/hipaa.md)
Healthcare (Global) | Various | Depends on jurisdiction

## Load Only Relevant Regulators

**Critical**: Only load regulator guidance files that apply to the user's jurisdiction and industry.

**Example**:
```
User: "We're a New Zealand bank owned by an Australian parent, need APRA and RBNZ compliance"
AI: Loading regulators/apra.md, regulators/rbnz.md, regulators/basel.md, regulators/fatf.md...
AI: (Does NOT load gdpr.md, ccpa.md, hipaa.md, etc.)
```

**If user mentions specific compliance frameworks**:
```
User: "We need to comply with GDPR for EU customers and APRA for Australian operations"
AI: Loading regulators/gdpr.md and regulators/apra.md...
```

## Apply Regulatory Metadata

Once relevant regulator(s) loaded:

1. User defines entity: "We need to model Customer"
2. Consult loaded regulator guidance for metadata requirements
3. Apply appropriate governance metadata to entity
4. Include regulatory scope in domain and entity metadata

**Example with APRA loaded**:
```
User: "Model Customer entity"
AI: Checks regulators/apra.md → identifies PII requirements, CPS 234 scope
AI: Applies metadata:
  governance:
    classification: "Highly Confidential"
    pii: true
    regulatory_scope:
      - APRA CPS 234
      - APRA APS 222
```

## Common Regulatory Metadata Properties

Property | Description | Example Values
---------|-------------|---------------
`classification` | Data sensitivity level | "Public", "Internal", "Confidential", "Highly Confidential"
`pii` | Contains personally identifiable information | `true`, `false`
`regulatory_scope` | Which regulations apply | List of regulations
`retention` | How long data must be kept | "7 years", "10 years post closure"
`data_residency` | Where data must be stored | `["Australia", "New Zealand"]`
`cross_border_transfer` | Data crosses jurisdictional borders | `true`, `false`
`audit_all_access` | All access must be logged | `true`, `false`
`breach_notification_required` | Must notify regulator of breaches | `true`, `false`

## Domain-Level Regulatory Metadata

Set default regulatory posture at domain level:

```yaml
# In domain.md Metadata section
governance:
  classification: "Highly Confidential"  # Default for all entities
  pii: true
  regulatory_scope:
    - APRA CPS 234
    - RBNZ BS13
    - Basel III
    - FATF AML/CTF
  default_retention: "7 years post relationship end"
  data_residency: ["Australia", "New Zealand"]
```

Entities can override domain defaults when needed.

## Entity-Level Regulatory Metadata

Apply specific requirements to individual entities:

```yaml
# In entities/customer.md
governance:
  classification: "Highly Confidential"
  pii: true
  pii_fields:
    - Date of Birth
    - Tax Identification Number
    - Email Address
  regulatory_scope:
    - APRA CPS 234 (Information Security)
    - APRA APS 222 (Associations with Related Entities)
    - RBNZ BS13 (Governance)
  retention: "10 years post relationship end"
  retention_basis: "APRA record keeping requirements"
  audit_all_access: true
  breach_notification_required: true
  notification_timeframe: "72 hours"
```

## Dual/Multiple Jurisdiction Scenarios

For organizations operating in multiple jurisdictions:

```yaml
governance:
  regulatory_scope:
    - APRA CPS 234 (parent company - Australia)
    - RBNZ BS13 (local subsidiary - New Zealand)
    - Basel III (international capital standards)
  
  data_residency: ["Australia", "New Zealand"]
  
  dual_reporting: true
  reporting_frameworks:
    - APRA ARF 320 (quarterly)
    - RBNZ Financial Statements (quarterly)
```

## Compliance Framework Mapping

Map entities to specific reporting frameworks:

```yaml
governance:
  apra_reporting:
    arf_320_0: true   # Statement of Financial Position
    arf_320_1a: true  # Balance Sheet
  
  rbnz_reporting:
    financial_statements: true
    capital_adequacy: true
  
  basel_reporting:
    credit_risk_exposure: true
    operational_risk: true
```

## AML/CTF Specific Metadata

For financial crime monitoring (FATF requirements):

```yaml
governance:
  aml_relevant: true
  ctf_relevant: true
  fatf_scope: true
  
  monitoring_required: true
  screening_required: true
  screening_lists:
    - UN Sanctions
    - OFAC
    - Local Sanctions
  
  enhanced_due_diligence: false  # Default, override for high-risk
  pep_screening: true
```

## Loading Additional Regulators Mid-Modeling

If during modeling you discover need for another regulator:

**Ask user**:
"I notice you're modeling {concept} which may be subject to {additional regulator}. Should we include that compliance framework?"

**Example**:
```
User modeling customer data (APRA loaded)
AI: "I notice you're collecting EU customer data. Should we also apply GDPR requirements?"
User: "Yes, we have EU operations"
AI: Loading regulators/gdpr.md...
AI: Applying GDPR-specific metadata (right to erasure, consent tracking, etc.)
```

**Only load when**:
- User explicitly requests
- Clear regulatory trigger identified (e.g., cross-border data, specific data types)
- User confirms the additional regulator applies

## Validation

Before applying regulatory metadata:
1. Confirm loaded regulator guidance applies to this entity
2. Check entity type against regulator requirements (e.g., APRA CPS 234 applies to "material information assets")
3. Verify retention periods align with business lifecycle
4. Ensure data residency requirements are feasible

## When No Regulatory Requirements

If entity has no specific regulatory requirements:
- Omit detailed regulatory metadata
- May still include basic classification and retention
- Document in detail file: "No specific regulatory requirements identified"

## Related Skills

- [external-standard-mapping](../external-standard-mapping/SKILL.md) - Standards and regulations often overlap
- [domain-discovery](../domain-discovery/SKILL.md) - Initial regulatory identification happens during domain discovery