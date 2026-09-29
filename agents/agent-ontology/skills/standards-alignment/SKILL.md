---
name: standards-alignment
description: Use when the user names an industry standard (BIAN, ISO 20022, FHIR, ACORD, TM Forum), when modelling a recognised industry domain (banking, payments, insurance, healthcare, telecom, retail), when filling the Reference column of a summary table, when asking whether a concept already exists in a standard, or when the model's decomposition differs from a standard's.
---

# Skill: Standards Alignment

Find, evaluate, and reference industry standards honestly. References go in the
`Reference` column of summary tables and in entity descriptions. There is no dedicated
spec section.

## Standards and Local Guidance

Use the local guidance before anything online. Each file defines its own lookup order,
reference files, and no-guess rules.

Industry | Standards | Local guidance
--- | --- | ---
Banking | BIAN BOM (v13 default until v14 snapshots exist), FIBO | `standards/bian/README.md`
Payments | ISO 20022 Business Model (Business Components and Elements, not message definitions), PCI DSS | `standards/iso20022.md`
Insurance | ACORD (membership-gated, so state your confidence), IAIS | `standards/acord/README.md`
Healthcare | HL7 FHIR, SNOMED CT, ICD-10, LOINC | `standards/fhir/README.md`
Telecom | TM Forum SID, eTOM | `standards/tmforum/README.md`
Retail and supply chain | GS1, eCl@ss | (none locally)
Cross-industry | ISO 8601, ISO 4217, ISO 3166 | (none needed)

Regulatory frameworks (GDPR, APRA, Basel, FATF, HIPAA, SOX, and others) belong in
`regulatory_scope`, not the Reference column. Their obligations are in Agent Governance's
regulator files.

---

## Applying a Reference

1. **Verify the counterpart exists.** Look the name up in the local index (for example
   `standards/bian/bo-classes.md`) and check its definition and hierarchy. Never
   reference a class name you haven't found, and never make up a URL. A missing
   reference is honest; a wrong one misleads everyone who trusts it.
2. **Judge the fit:**

   Fit | Action
   --- | ---
   Name and definition match | Reference directly
   Your concept specialises the standard's | Reference the parent and note the specialisation
   Partial overlap | Reference with "Partial alignment: [difference]"
   No counterpart | Leave the Reference empty

3. **Say so when your meaning differs.** Tell the user explicitly and record the
   extension in the entity description.
4. **Format.** In the Reference column, name the standard and class and link to its
   definition. Put the most specific standard first when several apply.

## When Decompositions Differ

Use this protocol when the difference is structural rather than a naming mismatch. It
applies when one of your concepts maps to several standard objects, several map to one,
or they overlap with distinct extensions.

1. **Compare side by side:** your concept, the standard's, the overlap, the gap, and the
   options.
2. **Evaluate each option** on ownership, lifecycle, attributes, governance,
   interoperability gained, and what breaks if you diverge.
3. **Resolve each row** in one of four ways:
   - adopt the standard's decomposition, when it adds real value
   - keep yours and reference with a qualification, when yours reflects real
     operational boundaries
   - hybrid: the standard's abstract parent with your subtypes
   - no alignment, when the similarity is only superficial
4. **Record the decision** in the entity description (the standard equivalent, the
   decision, and why), so nobody reopens it later.

## Worked Example: Verifying Financial Crime Against BIAN v13

Financial Crime's Entities table references BIAN classes. Checking each one against
`standards/bian/bo-classes.md` (v13):

Entity | Referenced class | In v13 index? | Action
--- | --- | --- | ---
Party | Party | Yes | Keep
Person | Person | Yes | Keep
Party Role, Customer | PartyRole | Yes | Keep. Customer specialises it.
Account | Account | Yes | Keep
Company | LegalEntity | **No** | Look for the v13 equivalent (`Organisation` is present). Confirm its definition before changing anything.
Transaction | Payment | **No** | Look for candidates (e.g. `AccountEntry`, a posting to an account, which is narrower than Transaction) and record any match as a partial alignment

The lesson: references that look plausible can still fail the lookup. Run every
reference through the index, and for the ones that fail, apply the Judge-the-fit step
with the user rather than guessing a replacement.

## Regulatory Scope Prompt

Teams often leave `regulatory_scope` thin, assuming compliance is someone else's job.
Ask:

- Personal data? GDPR, CCPA, PDPA.
- Financial reporting? SOX, BCBS 239.
- Transactions or payments? PCI DSS, AML/CTF, FATF.
- Credit risk? Basel III.
- Health information? HIPAA.
- Regulated in Australia (APRA CPS 234, CPG 235), the EU (DORA, AMLD), or the UK (FCA)?

For each framework that applies, confirm whether it affects `classification`, `pii`,
`default_retention`, or attribute-level governance. Hand detailed obligations to Agent
Governance.
