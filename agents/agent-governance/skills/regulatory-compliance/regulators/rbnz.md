# RBNZ (Reserve Bank of New Zealand) - Regulatory Guidance

> **last_verified:** 2025-03-08

## Overview

RBNZ is the central bank and prudential regulator for New Zealand, regulating:

- Registered banks
- Non-bank deposit takers
- Insurers

**Relevance**: If modeling for NZ banks (including NZ subsidiaries of Australian banks).

## Key RBNZ Requirements for Data Modeling

### Banking Supervision Handbook

**Impact on MD-DDL**:

- Governance and risk management
- Data quality for regulatory reporting
- Outsourcing requirements

### BS13 - Governance

Board oversight and risk committee scope are organisational controls, not model metadata.
Add `RBNZ BS13` to `regulatory_scope` for in-scope domains, and to `compliance_relevance`
on entities that feed board risk reporting.

### BS2B - Capital Adequacy

**Entities affected**:

- Loan (credit risk weighted assets)
- Capital positions

Name the capital adequacy return in `regulatory_reporting`. Model the risk-weight
category (Residential Mortgage, Corporate, Retail) as an attribute or enum on the exposure
(see `basel.md`), not as governance metadata.

### Data Residency Requirements

RBNZ requires certain data to be stored in New Zealand.

```yaml
data_residency: ["New Zealand"]   # extension field; domain default or entity override
```

## Dual Regulation (APRA + RBNZ)

For NZ subsidiaries of Australian banks:

Both regulators apply. List both in the domain metadata (top level, not under
`governance:`), and record where each applies:

```yaml
regulatory_scope:
  - APRA CPS 234   # parent company
  - RBNZ BS13      # local subsidiary
data_residency: ["Australia", "New Zealand"]
```

Reporting to both regulators is expressed by naming each return in `regulatory_reporting`
on the entities that feed it.

## RBNZ Reporting

**Key reporting requirements**:

- Financial statements (quarterly)
- Capital adequacy (quarterly)
- Liquidity (monthly)

```yaml
governance:
  regulatory_reporting:
    - RBNZ Financial Statements (quarterly)
    - RBNZ Capital Adequacy (quarterly)
    - RBNZ Liquidity (monthly)
```

## Resources

- RBNZ Website: <https://www.rbnz.govt.nz>
- Banking Supervision Handbook: <https://www.rbnz.govt.nz/regulation-and-supervision/banks/banking-supervision-handbook>
