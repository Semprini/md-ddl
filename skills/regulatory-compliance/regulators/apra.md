# APRA (Australian Prudential Regulation Authority) - Regulatory Guidance

## Overview

APRA is the prudential regulator for the Australian financial services industry, regulating:

- Banks
- Credit unions and building societies  
- General and life insurance companies
- Superannuation funds

**Relevance**: If modeling for Australian financial institutions or NZ banks owned by Australian parents.

## Key APRA Prudential Standards for Data Modeling

### CPS 234 - Information Security

**Impact on MD-DDL**:

- Data classification required for all entities
- Information asset inventory (entities in domain model)
- Data residency requirements

**Metadata to include**:

```yaml
governance:
  classification: "Confidential" | "Highly Confidential" | "Public"
  information_asset: true
  cps234_scope: true
  data_residency: ["Australia", "New Zealand"]
  security_controls:
    - Encryption at rest
    - Encryption in transit
    - Access logging
```

**Entities particularly affected**:

- Customer (PII, highly confidential)
- Account (financial data, confidential)
- Transaction (payment data, confidential)

### CPS 220 - Risk Management

**Impact on MD-DDL**:

- Risk assessment metadata on entities
- Material risk identification

**Metadata to include**:

```yaml
governance:
  risk_category: "Credit Risk" | "Operational Risk" | "Market Risk" | "Liquidity Risk"
  material_risk: true | false
```

### CPS 231 - Outsourcing

**Impact on MD-DDL**:

- Track if data is processed by third parties
- Identify material outsourcing arrangements

**Metadata to include**:

```yaml
governance:
  outsourced_processing: true | false
  material_outsourcing: true | false
  service_provider: "Provider Name"
```

### APS 222 - Associations with Related Entities

**Impact on MD-DDL**:

- Track related party relationships
- Cross-border data flows

**Relationships to model**:

```markdown
### Related Entity Relationship
Tracks associations between the institution and related entities for regulatory reporting.
```

## APRA Reporting Requirements

### Data Quality Standards

APRA expects:

- Data accuracy
- Data completeness
- Data timeliness
- Data validity

**MD-DDL Constraints**:

```yaml
constraints:
  Data Quality - Completeness:
    not_null: [Customer ID, Account Number, Transaction Date]
    description: "APRA reporting requires complete core identifiers"
    
  Data Quality - Validity:
    check: "Transaction Date <= CURRENT_DATE"
    description: "APRA reporting requires valid dates"
```

### Regulatory Reporting Entities

Key entities for APRA reporting:

- Customer (ARF 320 series)
- Loan (ARF 320 series)  
- Capital positions (APS 110)
- Liquidity (APS 210)

**Metadata to include**:

```yaml
governance:
  apra_reporting:
    arf_320_0: true  # Statement of Financial Position
    arf_320_1a: true  # Balance Sheet
  reporting_frequency: "Quarterly" | "Monthly"
```

## Data Retention Requirements

APRA expects institutions to retain data for:

- **Financial records**: 7 years minimum
- **Superannuation records**: Longer retention

**Metadata to include**:

```yaml
governance:
  retention: "7 years post account closure"
  retention_basis: "APRA CPS 234, APS 220"
```

## Cross-Border Data Flows

If data crosses borders (e.g., NZ to Australia):

**Metadata to include**:

```yaml
governance:
  cross_border_transfer: true
  transfer_destinations: ["Australia", "New Zealand"]
  transfer_basis: "Group consolidation under APRA oversight"
```

## Material Data Breach Notification

CPS 234 requires notification of material data breaches.

**Metadata to include**:

```yaml
governance:
  breach_notification_required: true
  notification_timeframe: "72 hours"
```

## APRA + Basel Integration

APRA implements Basel standards in Australia. When modeling:

**Load both**:

- [APRA](apra.md) for Australian-specific requirements
- [Basel](basel.md) for international capital/liquidity standards

**Example**:

```yaml
governance:
  regulatory_scope:
    - APRA CPS 234
    - Basel III Capital Requirements (via APRA APS 110)
```

## Common APRA-Impacted Entities

Entity | APRA Standard | Key Metadata
------ | ------------- | ------------
Customer | CPS 234, APS 222 | classification: "Highly Confidential", pii: true
Account | CPS 234, ARF 320 | apra_reporting: true, retention: "7 years"
Transaction | CPS 234, APS 210 | classification: "Confidential", audit_all_access: true
Loan | CPS 220, ARF 320 | risk_category: "Credit Risk", apra_reporting: true
Related Entity | APS 222 | related_party: true

## Resources

- [APRA Website](https://www.apra.gov.au)
- [CPS 234](https://www.apra.gov.au/sites/default/files/CPS_234_July_2019_0.pdf)
- [Prudential Standards](https://www.apra.gov.au/prudential-framework)
