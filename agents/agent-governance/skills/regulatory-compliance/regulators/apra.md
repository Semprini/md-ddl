# APRA (Australian Prudential Regulation Authority) - Regulatory Guidance

> **last_verified:** 2025-03-08
> **partially re-verified:** 2026-09-29. CPS 234 notification windows and the CPS 230
> commencement were checked against apra.gov.au. The rest of the file still dates
> from the original verification.

## Overview

APRA is the prudential regulator for Australian banks, credit unions, building societies,
general and life insurers, and superannuation funds. Load this file when modelling for an
Australian APRA-regulated entity, or an NZ bank owned by an Australian parent (with
`rbnz.md`).

Examples below use the governance fields of `3-Entities.md § Governance Metadata Schema`.
Where a standard implies *business data*
(risk categories, service providers), model it as entity attributes or relationships with
Agent Ontology, not as governance keys.

## CPS 234 — Information Security

- Every entity needs a classification. The entities in the domain model form the
  information asset inventory.
- Notify APRA **as soon as possible and no later than 72 hours** after becoming aware of a
  material information security incident.
- Notify APRA **no later than 10 business days** after becoming aware of a material control
  weakness that the entity expects it can't remediate in time.

```yaml
# Domain metadata
classification: "Highly Confidential"
regulatory_scope:
  - APRA CPS 234
breach_notification_required: true    
notification_timeframe: "72 hours"      # material incidents; control weaknesses: 10 business days
```

Record security controls (encryption, access logging) with `audit_all_access` where every
access must be logged. Other controls are platform concerns, not model metadata.

Entities most affected: Customer (PII, highly confidential), Account and Transaction
(financial data, confidential).

## CPS 230 — Operational Risk Management

CPS 230 commenced on **1 July 2025** and replaced CPS 231 (Outsourcing) and CPS 232
(Business Continuity). For pre-existing service-provider contracts, the requirements apply
from the earlier of the next contract renewal or 1 July 2026.

For data modelling, record reliance on material service providers as a relationship
(e.g. Account `processed_by` Service Provider) or a source system declaration, not as a
governance key. Add `APRA CPS 230` to `regulatory_scope` when material service providers
process the domain's data.

## CPS 220 — Risk Management

Risk categories (credit, operational, market, liquidity) and materiality are business
facts. Model them as attributes or enums where the domain needs them. Cite the standard in
`compliance_relevance` on the entities it governs.

## APS 222 — Associations with Related Entities

Model related-entity associations as relationships (e.g. a Related Entity relationship on
Party) so they can be reported on. Cross-border flows use the security and residency fields:

```yaml
governance:
  cross_border_transfer: true
  data_residency: ["Australia", "New Zealand"]
  description: "Group consolidation under APRA oversight"
```

## Regulatory Reporting (ARF series)

Name the returns an entity feeds with `regulatory_reporting`, and the standards with
`compliance_relevance`:

```yaml
governance:
  compliance_relevance:
    - APRA CPS 234
  regulatory_reporting:
    - ARF 320.0 Statement of Financial Position
```

Reporting frequency is a property of the return, not of the entity. Leave it out of the
model.

APRA's reporting expects complete, valid data. Express this as entity constraints:

```yaml
constraints:
  Core Identifiers Present:
    not_null: [Customer Number, Account Number]
    description: APRA reporting requires complete core identifiers
```

## Retention

This file doesn't cite a specific APRA retention period. For AML/CTF records, use
`austrac.md` (7 years from the end of the relationship or completion of the transaction).
For other financial records, confirm the period and its source with the compliance team
before setting `retention` and `retention_basis`.

## APRA and Basel

APRA implements Basel III in Australia (e.g. APS 110 capital adequacy). Load `basel.md`
alongside this file for capital and liquidity data, and list both in `regulatory_scope`.

## Common APRA-Impacted Entities

Entity | Standards | Typical metadata
--- | --- | ---
Customer | CPS 234, APS 222 | `classification: "Highly Confidential"`, `pii: true`
Account | CPS 234, ARF 320 | `regulatory_reporting`, retention per `austrac.md`
Transaction | CPS 234 | `classification: "Confidential"`, `audit_all_access: true`
Loan | CPS 220, ARF 320 | risk category modelled as an attribute; `regulatory_reporting`
Related Entity | APS 222 | Modelled as a relationship

## Resources

- [APRA](https://www.apra.gov.au)
- [CPS 234 Information Security](https://www.apra.gov.au/standards/cps-234)
- [CPS 230 Operational Risk Management](https://www.apra.gov.au/standards/cps-230)
