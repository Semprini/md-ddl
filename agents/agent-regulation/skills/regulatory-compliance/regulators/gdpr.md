# GDPR — General Data Protection Regulation (EU)

## Overview

The General Data Protection Regulation (EU 2016/679) is the primary data protection and privacy regulation for the European Union. It governs the processing of personal data of individuals within the EU/EEA.

## Key Requirements for MD-DDL Governance Metadata

### PII and Personal Data

- **Scope:** Any information relating to an identified or identifiable natural person
- **Special categories (Article 9):** Racial/ethnic origin, political opinions, religious beliefs, trade union membership, genetic data, biometric data, health data, sex life or sexual orientation — require explicit consent or specific legal basis
- **PII flag:** `pii: true` required on all entities containing personal data
- **pii_fields:** Must enumerate all attributes containing personal data

### Classification

- Entities containing special category data should be classified `Highly Confidential` at minimum

### Retention

- Data must not be kept longer than necessary for the purpose for which it was collected (Article 5(1)(e))
- Specific retention periods depend on the legal basis and purpose — consult the organisation's data protection impact assessment
- `retention_basis` should cite the specific legal basis (e.g., "Legitimate interest under Article 6(1)(f)" or "Legal obligation under Article 6(1)(c)")

### Breach Notification

- `breach_notification_required: true` for entities containing personal data
- `notification_timeframe: "72 hours"` — supervisory authority must be notified within 72 hours of becoming aware (Article 33)

### Data Residency

- Transfer restrictions under Chapter V — personal data may only leave the EU/EEA with adequate safeguards
- `data_residency` should reflect any localisation requirements
- `cross_border_transfer` should be flagged where applicable

### Rights of Data Subjects

- Right to erasure (Article 17) — consider whether entities support deletion or anonymisation
- Right to portability (Article 20) — consider export format requirements
- Right to rectification (Article 16) — consider mutability implications

## Regulatory Scope Value

Use in `regulatory_scope`: `GDPR`
