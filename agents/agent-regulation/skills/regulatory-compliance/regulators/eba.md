# EBA — European Banking Authority

## Overview

The European Banking Authority is the EU agency responsible for ensuring effective and consistent prudential regulation and supervision across the European banking sector. Key regulations include CRD/CRR capital requirements and EBA Guidelines on data governance.

## Key Requirements for MD-DDL Governance Metadata

### Data Governance (EBA/GL/2017/11)

- Data quality frameworks must cover accuracy, completeness, timeliness, and consistency
- `owners` and `stewards` should be declared at domain level
- Data lineage must be traceable — source-to-canonical mappings support this requirement

### Capital Requirements (CRD V / CRR II)

- Entities supporting risk calculation (exposure, counterparty, position) require strict governance
- `classification: "Confidential"` or higher for risk-related entities
- `audit_all_access: true` for entities feeding regulatory capital calculations

### BCBS 239 Implementation

- EBA expects compliance with BCBS 239 principles for risk data aggregation
- See `basel.md` for BCBS 239–specific requirements

### Retention

- Regulatory reporting data: retain for the period specified by national competent authority
- Typical minimum: 5 years for transaction records
- `retention_basis` should cite specific EBA guideline or national transposition

## Regulatory Scope Value

Use in `regulatory_scope`: `EBA Guidelines`
