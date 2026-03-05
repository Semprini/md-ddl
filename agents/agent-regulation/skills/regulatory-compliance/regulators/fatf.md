# FATF — Financial Action Task Force

## Overview

The Financial Action Task Force sets international standards for combating money laundering, terrorist financing, and proliferation financing. FATF Recommendations are implemented through national legislation in member jurisdictions.

## Key Requirements for MD-DDL Governance Metadata

### AML/CTF Relevance

- `regulatory_scope` should include `FATF Recommendations` or `FATF AML/CTF` for domains handling party identification, transaction monitoring, or suspicious activity reporting
- Entities representing parties, transactions, and accounts are in scope

### Customer Due Diligence (Recommendations 10–12)

- Party and customer entities must support identification and verification attributes
- Enhanced due diligence required for high-risk categories (PEPs, high-risk countries, complex structures)
- Ongoing due diligence — entities should support periodic review tracking

### Record Keeping (Recommendation 11)

- `retention: "5 years"` minimum after the business relationship has ended or after the date of the occasional transaction
- Some jurisdictions require longer (e.g., 7–10 years) — defer to local regulator file
- `retention_basis: "FATF Recommendation 11 — record keeping obligations"`

### Suspicious Transaction Reporting (Recommendation 20)

- Transaction entities should support flagging and reporting workflows
- `audit_all_access: true` recommended for entities involved in suspicious activity investigations

### Sanctions Screening (Recommendation 6)

- Party entities must support screening against UN, OFAC, EU, and local sanctions lists
- `screening_required: true` and `screening_lists` should be declared where applicable

### Wire Transfers (Recommendation 16)

- Transaction entities involving cross-border funds transfers must carry originator and beneficiary information

## Regulatory Scope Value

Use in `regulatory_scope`: `FATF Recommendations` or `FATF AML/CTF`
