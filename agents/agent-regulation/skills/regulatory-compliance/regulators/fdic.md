# FDIC — Federal Deposit Insurance Corporation

> **last_verified:** 2025-03-08

## Overview

The FDIC insures deposits, examines and supervises financial institutions for safety and soundness, and manages receiverships. It regulates state-chartered banks that are not members of the Federal Reserve System.

## Key Requirements for MD-DDL Governance Metadata

### Data Governance

- FDIC-supervised institutions must maintain adequate data governance as part of safety and soundness standards
- `owners` and `stewards` should be declared at domain level
- Data supporting deposit insurance calculations requires strict lineage

### Deposit Insurance Determination

- Entities supporting deposit account records must enable accurate and timely deposit insurance determination
- `classification: "Confidential"` or higher for deposit-related entities
- Account and customer entities should support the FDIC's large-bank deposit insurance determination requirements (12 CFR Part 370)

### BSA/AML Compliance

- FDIC enforces BSA/AML for state non-member banks
- See `fatf.md` for AML/CTF–specific metadata requirements

### Retention

- BSA records: minimum 5 years
- Deposit account records: retain per institution policy, typically life of account plus 5–7 years
- `retention_basis` should cite specific FDIC regulation or Part 370

### Breach Notification

- FDIC-supervised institutions must notify the FDIC of computer-security incidents within 36 hours (FDIC FIL-29-2022)
- `breach_notification_required: true` for entities containing customer financial information
- `notification_timeframe: "36 hours"` for incident notification to FDIC

## Regulatory Scope Value

Use in `regulatory_scope`: `FDIC`
