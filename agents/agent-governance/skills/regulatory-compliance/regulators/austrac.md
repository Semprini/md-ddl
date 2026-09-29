# AUSTRAC (Australian Transaction Reports and Analysis Centre) - Regulatory Guidance

> **last_verified:** 2026-09-29. Record-keeping periods checked against austrac.gov.au
> guidance. The AML/CTF reforms (new guidance and 2026 transitional rules) weren't
> reviewed in detail. Confirm reform obligations with the compliance team.

## Overview

AUSTRAC is Australia's AML/CTF regulator and financial intelligence unit. It administers
the *Anti-Money Laundering and Counter-Terrorism Financing Act 2006* (AML/CTF Act) for
reporting entities: banks and other financial services, remittance, gambling, bullion,
and, under the reforms, additional "tranche 2" sectors.

Load this file with `apra.md` for Australian banks, and with `fatf.md` for the
international AML/CTF framework it implements.

## Record Keeping (AML/CTF Act, s 116 and related provisions)

Record | Keep for
--- | ---
Customer due diligence records | At least 7 years from the date the business relationship ends
Transaction records | At least 7 years from the date the transaction was completed
AML/CTF program records | 7 years from when the record is no longer relevant to demonstrating compliance

Under the reform guidance, retained information must be deleted at the end of the
7-year period. Confirm how this applies to your entity, because it affects retention
settings and purge processes.

```yaml
# Entity governance, e.g. Party or Customer (CDD records)
governance:
  retention: "7 years post relationship end"
  retention_basis: "AML/CTF Act 2006 record keeping (AUSTRAC): CDD records 7 years from end of business relationship"
  compliance_relevance:
    - AML/CTF Act 2006
```

```yaml
# Entity governance, e.g. Transaction
governance:
  retention: "7 years post transaction completion"
  retention_basis: "AML/CTF Act 2006 record keeping (AUSTRAC): transaction records 7 years from completion"
  compliance_relevance:
    - AML/CTF Act 2006
```

A longer domain default (e.g. 10 years for other obligations) satisfies these minimums.
Record the AML/CTF basis in `retention_basis` rather than shortening the retention.

## Reporting

Name the reports an entity feeds with `regulatory_reporting`, for example the Suspicious
Matter Report (SMR), Threshold Transaction Report (TTR), and International Funds Transfer
Instruction (IFTI) report. Confirm the current report set and thresholds with the
compliance team; this file doesn't record them.

## Resources

- [AUSTRAC record keeping](https://www.austrac.gov.au/industry-and-business/obligations-and-guidance/your-amlctf-program/develop-your-amlctf-programs/record-keeping)
- [AUSTRAC AML/CTF reform guidance](https://www.austrac.gov.au/amlctf-reform)
