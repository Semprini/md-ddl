# OCC — Office of the Comptroller of the Currency

## Overview

The OCC charters, regulates, and supervises national banks, federal savings associations, and federal branches and agencies of foreign banks in the United States. Key guidance includes the Comptroller's Handbook and OCC Bulletins.

## Key Requirements for MD-DDL Governance Metadata

### Data Governance (OCC 2014-09, Heightened Standards)

- Covered institutions must establish enterprise-wide data governance frameworks
- `owners` and `stewards` required at domain level
- Data quality and completeness must be documented for entities feeding risk management

### BSA/AML Compliance

- OCC enforces BSA/AML compliance for national banks
- See `fatf.md` for AML/CTF–specific metadata requirements
- `regulatory_scope` should include `BSA` for entities in AML scope

### Retention

- Minimum 5 years for BSA records (currency transaction reports, SARs)
- Loan records: typically retain through life of loan plus applicable statute of limitations
- `retention_basis` should cite specific OCC guidance or BSA provision

### Classification

- Customer financial information: `classification: "Confidential"` per OCC privacy guidance
- Examination-related data: `classification: "Highly Confidential"`

## Regulatory Scope Value

Use in `regulatory_scope`: `OCC`
