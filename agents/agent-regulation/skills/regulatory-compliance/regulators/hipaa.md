# HIPAA — Health Insurance Portability and Accountability Act

## Overview

HIPAA establishes national standards for the protection of individually identifiable health information (Protected Health Information — PHI) in the United States. It applies to covered entities (health plans, healthcare clearinghouses, healthcare providers) and their business associates.

## Key Requirements for MD-DDL Governance Metadata

### Protected Health Information (PHI)

- **Scope:** Individually identifiable health information held or transmitted by a covered entity or business associate, in any form or medium
- **18 HIPAA identifiers:** Names, dates, phone/fax numbers, email, SSN, medical record numbers, health plan beneficiary numbers, account numbers, certificate/license numbers, vehicle/device identifiers and serial numbers, URLs, IP addresses, biometric identifiers, full-face photos, any other unique identifier
- `pii: true` required on all entities containing PHI
- `pii_fields` must enumerate attributes containing any of the 18 identifiers

### Classification

- PHI: `classification: "Highly Confidential"` at minimum
- De-identified data (per Safe Harbor or Expert Determination method): lower classification acceptable

### Retention

- HIPAA requires covered entities to retain documentation of policies and procedures for 6 years from date of creation or last effective date
- State laws often impose longer retention for medical records (varies by state)
- `retention_basis` should cite specific HIPAA provision and applicable state law

### Breach Notification (Breach Notification Rule)

- `breach_notification_required: true` for entities containing unsecured PHI
- `notification_timeframe: "60 days"` — individuals must be notified within 60 calendar days of discovery
- HHS must be notified: within 60 days for breaches affecting 500+ individuals; annually for smaller breaches

### Access Controls (Security Rule)

- `audit_all_access: true` for entities containing PHI
- Access must be limited to minimum necessary for the intended purpose
- `access_role` should reflect minimum-necessary access designations

### Data Residency

- No specific US localisation requirement under HIPAA, but BAAs (Business Associate Agreements) may restrict location
- Document any residency constraints in `data_residency`

## Regulatory Scope Value

Use in `regulatory_scope`: `HIPAA`
