---
name: regulatory-compliance
description: Use whenever governance metadata is applied, reviewed, or evaluated for a jurisdiction or framework (APRA, RBNZ, GDPR, CCPA, Basel, EBA, FATF, Federal Reserve, OCC, FDIC, HIPAA, SOX), when the user mentions compliance or a regulator, and before stating any retention period, notification timeframe, or regulatory obligation. Shared with Agent Ontology for first-pass governance while modelling.
---

# Skill: Regulatory Compliance

Apply governance metadata from the regulator guidance files in `regulators/`. They are
the authority for specific obligations; training knowledge is not. Load only the files
that apply.

## Choosing Regulator Files

Ask which jurisdictions and frameworks apply, then load the matching files:

Jurisdiction | Files
--- | ---
Australian banking | `apra.md`, `austrac.md`, `basel.md`, `fatf.md`
NZ banking (incl. NZ subsidiaries of Australian banks) | `rbnz.md`, `basel.md`, `fatf.md`, plus `apra.md` for the parent
EU | `gdpr.md`, `basel.md`, `eba.md`
US banking | `federal-reserve.md`, `occ.md`, `fdic.md`, `basel.md`
US general | `ccpa.md`, `sox.md`
AML/CTF (global) | `fatf.md`; add the local AML regulator's file where one exists (`austrac.md` for Australia)
US healthcare | `hipaa.md`
Other healthcare | (no file yet) Say so, and don't infer obligations.

Load another file mid-session only when the user asks, or when a clear trigger appears
(EU customers suggest GDPR; health data suggests HIPAA) and the user confirms it applies.

Before citing a file, check its `last_verified` date. If it's older than 12 months, warn
the user and ask them to confirm current obligations with their compliance team.

---

## The Governance Schema

**Core fields.** These are defined by `md-ddl-specification/3-Entities.md § Governance
Metadata Schema`, which holds the full rules:

Level | Field | Notes
--- | --- | ---
Domain metadata (top level, no `governance:` wrapper) | `classification`, `pii`, `regulatory_scope`, `default_retention` | Defaults inherited by every entity, relationship, event, and product
Entity `governance:` (overrides only) | `pii`, `pii_fields`, `classification`, `retention`, `retention_basis`, `access_role`, `description` | Only fields that differ from the domain. A weaker posture needs a justification.
Entity `governance:` (entity-specific) | `compliance_relevance` (the acts and standards that apply), `regulatory_reporting` (named reports and submissions) | Map domain frameworks to specific obligations

**Security and residency fields.** These are defined in the same spec section and may be set
as domain defaults or entity overrides:

Field | Meaning
--- | ---
`data_residency` | Jurisdictions where the data must be stored, e.g. `["Australia", "New Zealand"]`
`cross_border_transfer` | Whether the data crosses jurisdictional borders
`audit_all_access` | Every access must be logged
`breach_notification_required` | Breaches must be notified to a regulator
`notification_timeframe` | The notification deadline, e.g. `"72 hours"` under GDPR, taken from the regulator file

These fields and the core fields are the whole schema. Don't invent further fields. Express reports and AML/CTF scope through
`regulatory_reporting` and `compliance_relevance`, not new keys.

## Applying It

1. Set domain defaults first, from the loaded regulator files:

   ```yaml
   # domain.md, ## Metadata
   classification: "Highly Confidential"
   pii: true
   regulatory_scope:
     - APRA CPS 234
     - RBNZ BS13
     - FATF Recommendations
   default_retention: "7 years post relationship end"
   ```

2. Give an entity a `governance:` block only where it differs from the domain or has
   entity-specific obligations:

   ```yaml
   # entities/customer.md
   governance:
     retention: "10 years post relationship end"
     retention_basis: "APRA record-keeping requirements"   # cite the regulator file
     compliance_relevance:
       - AUSTRAC AML/CTF Act 2006
     regulatory_reporting:
       - Suspicious Matter Report (SMR)
     audit_all_access: true
     breach_notification_required: true
     notification_timeframe: "72 hours"
   ```

3. Before applying anything, check that the regulator's scope covers the entity (e.g. CPS 234
   applies to material information assets), that retention fits the business lifecycle,
   and that residency is feasible.

**Multiple jurisdictions.** List every framework in `regulatory_scope`, noting which
entity or operation each applies to. Where two frameworks conflict (for example,
different retention periods), apply the more conservative value and record the conflict
in a `# NOTE:` comment for the compliance team.

**No requirements.** If an entity has no specific obligations, it gets no block. It
inherits the domain defaults.
