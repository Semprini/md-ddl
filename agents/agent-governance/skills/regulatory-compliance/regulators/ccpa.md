# CCPA — California Consumer Privacy Act

> **last_verified:** 2025-03-08

## Overview

The California Consumer Privacy Act (CCPA), as amended by the California Privacy Rights Act (CPRA), grants California consumers rights over their personal information and imposes obligations on businesses that collect, use, or sell personal information.

## Key Requirements for MD-DDL Governance Metadata

### Personal Information

- **Scope:** Information that identifies, relates to, describes, is capable of being associated with, or could reasonably be linked with a particular consumer or household
- `pii: true` required on entities containing personal information
- `pii_fields` must enumerate specific attributes

### Classification

- Sensitive personal information (financial account details, precise geolocation, racial/ethnic origin, biometric data, health data) warrants `classification: "Highly Confidential"`

### Retention

- Personal information must not be retained longer than reasonably necessary for the disclosed purpose
- `retention` and `retention_basis` should reflect the organisation's disclosed retention schedule

### Consumer Rights

- Right to delete — entities must support deletion or anonymisation workflows
- Right to know — entities must support data inventory and disclosure
- Right to opt-out of sale/sharing — consider attribute-level consent tracking

### Breach Notification

- `breach_notification_required: true` for entities containing personal information
- Notification timeframe varies; "expedient" and "without unreasonable delay"

## Regulatory Scope Value

Use in `regulatory_scope`: `CCPA` or `CCPA/CPRA`
