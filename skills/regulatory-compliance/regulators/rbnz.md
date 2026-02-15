# RBNZ (Reserve Bank of New Zealand) - Regulatory Guidance

## Overview

RBNZ is the central bank and prudential regulator for New Zealand, regulating:
- Registered banks
- Non-bank deposit takers
- Insurers

**Relevance**: If modeling for NZ banks (including NZ subsidiaries of Australian banks).

## Key RBNZ Requirements for Data Modeling

### Banking Supervision Handbook

**Impact on MD-DDL**:
- Governance and risk management
- Data quality for regulatory reporting
- Outsourcing requirements

### BS13 - Governance

**Metadata to include**:
```yaml
governance:
  board_oversight: true
  risk_committee_scope: true
```

### BS2B - Capital Adequacy

**Entities affected**:
- Loan (credit risk weighted assets)
- Capital positions

**Metadata to include**:
```yaml
governance:
  capital_adequacy_reporting: true
  risk_weight_category: "Residential Mortgage" | "Corporate" | "Retail"
```

### Data Residency Requirements

RBNZ requires certain data to be stored in New Zealand.

**Metadata to include**:
```yaml
governance:
  data_residency: ["New Zealand"]
  rbnz_data_sovereignty: true
```

## Dual Regulation (APRA + RBNZ)

For NZ subsidiaries of Australian banks:

**Both regulators apply**:
```yaml
governance:
  regulatory_scope:
    - APRA CPS 234 (parent company)
    - RBNZ BS13 (local subsidiary)
  
  data_residency: ["Australia", "New Zealand"]
  
  dual_reporting: true
```

## RBNZ Reporting

**Key reporting requirements**:
- Financial statements (quarterly)
- Capital adequacy (quarterly)
- Liquidity (monthly)

**Metadata to include**:
```yaml
governance:
  rbnz_reporting:
    financial_statements: true
    capital_adequacy: true
    liquidity: true
  reporting_frequency: "Quarterly" | "Monthly"
```

## Resources

- RBNZ Website: https://www.rbnz.govt.nz
- Banking Supervision Handbook: https://www.rbnz.govt.nz/regulation-and-supervision/banks/banking-supervision-handbook
```

---

## **How AI Uses This Architecture**

### **Scenario: User starts modeling**
```
User: "I'm modeling financial crime for a New Zealand bank owned by an Australian parent. We need to align with BIAN."

AI: 
1. Loads domain-discovery/SKILL.md
2. Asks: "What regulatory jurisdictions apply?"
3. User says: "APRA and RBNZ, plus FATF for AML"
4. AI loads:
   - external-standard-mapping/standards/bian.md
   - regulatory-compliance/regulators/apra.md
   - regulatory-compliance/regulators/rbnz.md
   - regulatory-compliance/regulators/fatf.md
5. AI now has context to:
   - Find BIAN BOM references
   - Apply APRA CPS 234 metadata
   - Apply RBNZ data residency requirements
   - Apply FATF AML requirements
6. AI does NOT load ACORD, TM Forum, GDPR, CCPA (not relevant)