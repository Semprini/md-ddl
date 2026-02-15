# Inheritance Patterns - Detailed Guidance

## Overview
Entity inheritance in MD-DDL allows modeling "is-a" relationships...

## Core Principles
[Deep explanation]

## Industry Pattern Library

### Banking / Financial Services (BIAN)

**Party Hierarchy**:
```
Party (abstract)
├─ Individual
│   └─ Minor (optional specialization)
└─ Legal Entity
    ├─ Corporation
    ├─ Partnership
    └─ Trust
```

**Example: Individual.md**
```yaml
specializes: Party

attributes:
  # Inherited from Party: Party ID, Legal Name, Country of Residence
  First Name:
    type: string
  Date of Birth:
    type: date
```

**Party Role Hierarchy**:
```
Party Role (abstract)
├─ Customer
├─ Merchant
├─ Creditor
├─ Debtor
└─ Instructing Agent
```

Why this pattern works:
- Customer team owns Customer with KYC requirements
- Merchant Services owns Merchant with different compliance
- Each role has distinct attributes and lifecycle

### Insurance (ACORD)

**Party Hierarchy**:
```
Party (abstract)
├─ Person
└─ Organization
```

**Coverage Hierarchy**:
```
Coverage (abstract)
├─ Auto Coverage
│   ├─ Liability Coverage
│   └─ Comprehensive Coverage
├─ Property Coverage
│   ├─ Home Coverage
│   └─ Renters Coverage
└─ Life Coverage
    ├─ Term Life
    └─ Whole Life
```

**Example: Auto Coverage.md**
```yaml
specializes: Coverage

attributes:
  # Inherited from Coverage: Coverage ID, Policy Reference, Effective Date
  Vehicle VIN:
    type: string
  Vehicle Type:
    type: enum:Vehicle Type
  Garage Location:
    type: string
```

### Telecommunications (TM Forum SID)

**Party Hierarchy**:
```
PartyRole (TM Forum concept)
├─ Individual
├─ Organization
└─ Customer
```

**Product Hierarchy**:
```
Product (abstract)
├─ Mobile Product
│   ├─ Prepaid Mobile
│   └─ Postpaid Mobile
├─ Broadband Product
│   ├─ Fiber Broadband
│   └─ Cable Broadband
└─ TV Product
```

[Complete examples with TM Forum SID references]

### Healthcare (FHIR)

FHIR uses flat resources, but MD-DDL can model:
```
Party (abstract)
├─ Patient
├─ Practitioner
└─ Organization
```

[Complete examples with FHIR references]

## When NOT to Use Inheritance

❌ **Anti-pattern**: Creating inheritance just for code reuse
❌ **Anti-pattern**: More than 3 levels deep
❌ **Anti-pattern**: Children that override >50% of parent attributes

✅ **Use composition instead**: Relationships between entities

## Edge Cases
[Detailed edge case handling]

## Complete Case Studies
[Full worked examples from each industry]
```

---
