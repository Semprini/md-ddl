# Federal Reserve — US Federal Reserve System

> **last_verified:** 2025-03-08

## Overview

The Federal Reserve System is the central bank of the United States. It supervises and regulates bank holding companies, state-chartered member banks, and certain other financial institutions. Key regulatory frameworks include Regulation Y, Regulation YY (enhanced prudential standards), and SR Letters providing supervisory guidance.

## Key Requirements for MD-DDL Governance Metadata

### Data Governance (SR 11-7, SR 15-18)

- Model risk management (SR 11-7) requires data lineage and quality documentation for entities feeding risk models
- `owners` and `stewards` must be declared for entities in risk model scope
- `audit_all_access: true` for entities feeding supervisory reporting

### Regulatory Reporting

- Entities contributing to FR Y-9C, FR Y-14, Call Reports, and other regulatory filings require strict lineage and governance
- `classification: "Confidential"` or higher for regulatory reporting entities

### Retention

- Bank examination records: minimum 5 years (varies by record type)
- BSA/AML records: 5 years (see FATF and BSA-specific requirements)
- `retention_basis` should cite specific regulation or SR Letter

### Capital and Stress Testing (Regulation YY)

- Entities supporting CCAR/DFAST stress testing require documented data quality controls
- `data_quality_tier` should be declared on source systems feeding stress test models

## Regulatory Scope Value

Use in `regulatory_scope`: `Federal Reserve`
