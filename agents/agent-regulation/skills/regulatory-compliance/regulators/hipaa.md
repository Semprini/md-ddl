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

### De-Identification Methods

HIPAA provides two methods for de-identifying PHI. Data that has been properly
de-identified is no longer considered PHI and is not subject to HIPAA privacy
requirements. This directly affects the `classification` and `pii` metadata
on MD-DDL entities and data products.

#### Safe Harbor Method (§ 164.514(b))

Remove all 18 identifier categories from the data. The entity or data product
must confirm that none of the following are present or derivable:

Identifier Category | Examples | Masking Guidance
--- | --- | ---
Names | First, last, middle | `redact` or `hash`
Geographic subdivisions smaller than state | Street address, city, ZIP code (except first 3 digits if population > 20,000) | `truncate` for ZIP, `redact` for address
Dates more specific than year | Birth date, admission date, discharge date, death date | `year-only`
Phone numbers | All | `redact`
Fax numbers | All | `redact`
Email addresses | All | `redact` or `hash`
Social Security numbers | All | `redact` or `hash`
Medical record numbers | All | `redact` or `hash`
Health plan beneficiary numbers | All | `redact` or `hash`
Account numbers | All | `hash`
Certificate/license numbers | All | `redact`
Vehicle identifiers and serial numbers | VIN, license plate | `redact`
Device identifiers and serial numbers | All | `redact`
Web URLs | All | `redact`
IP addresses | All | `redact`
Biometric identifiers | Fingerprints, voiceprints, retinal scans | `redact`
Full-face photographs | And comparable images | `redact`
Any other unique identifying number, characteristic, or code | Except re-identification codes assigned by the covered entity | `redact` or `hash`

After removing all 18 categories, the covered entity must have no actual
knowledge that the remaining data could identify an individual.

**MD-DDL implication:** If a data product applies masking entries that fully
cover all 18 identifier categories for every included entity, and no
residual re-identification risk exists, the product may declare
`classification` below `Highly Confidential` and `pii: false` with a
comment citing Safe Harbor de-identification.

#### Expert Determination Method (§ 164.514(a))

A qualified statistical or scientific expert determines that the risk of
identifying an individual from the data is very small. The expert must document:

- The methods and results of the analysis
- That the risk is "very small" per accepted statistical and scientific principles

**MD-DDL implication:** If Expert Determination is used, document the expert's
finding in the product or entity governance block as a comment. The `pii` flag
may be set to `false` only when the expert determination is current and documented.

### PHI vs PII Distinction

In MD-DDL, the `pii` flag covers both PII and PHI. When auditing HIPAA-scoped
domains, treat `pii: true` as encompassing PHI obligations. The distinction
matters for regulatory reporting:

- **PHI** — individually identifiable health information (HIPAA scope)
- **PII** — broader personally identifiable information (GDPR, state privacy laws)
- An attribute may be PII but not PHI (e.g., employment history outside healthcare context)
- All PHI is PII, but not all PII is PHI

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
