# SOX — Sarbanes-Oxley Act

> **last_verified:** 2025-03-08

## Overview

The Sarbanes-Oxley Act of 2002 establishes requirements for financial reporting, internal controls, and audit trails for publicly traded companies in the United States.

## Key Requirements for MD-DDL Governance Metadata

### Internal Controls (Section 404)

- Entities feeding financial statements require documented internal controls
- `audit_all_access: true` for entities contributing to financial reporting
- `sox_scope: true` at domain or entity level where applicable

### Record Retention (Section 802)

- Audit work papers and related records: minimum 7 years
- `retention: "7 years"` for entities supporting financial audit
- `retention_basis: "SOX Section 802 — record retention"`

### Data Integrity

- Entities must support immutability or append-only semantics for financial records
- `mutability: immutable` or `mutability: append_only` for ledger and transaction entities in SOX scope

### Classification

- Financial reporting entities: `classification: "Confidential"` or higher
- Pre-release financial data: `classification: "Highly Confidential"`

### Governance Metadata

- `owners` must include the financial controller or CFO organisation
- `stewards` must include internal audit or compliance function

## Regulatory Scope Value

Use in `regulatory_scope`: `SOX`
