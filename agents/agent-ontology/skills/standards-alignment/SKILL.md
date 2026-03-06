---
name: standards-alignment
description: Use this skill when the user mentions a named industry standard (BIAN, ISO 20022, FHIR, ACORD, TM Forum, etc.), when modelling a recognised industry domain (banking, payments, insurance, healthcare, telecoms, retail), or when populating the Reference column of any MD-DDL summary table. Also use when the user asks whether a concept already exists in a standard, or when two modelled concepts might map to the same standard object.
---

# Skill: Standards Alignment

Covers how to find, evaluate, and reference external industry standards within
MD-DDL models. No additional spec section is required — standards are referenced
in the `Reference` column of domain summary tables and in entity YAML.

---

## Standards by Domain

| Industry | Primary Standards | Use for |
|---|---|---|
| Banking / Financial Services | BIAN BOM, FIBO | Entity and relationship semantics |
| Payments | ISO 20022, SWIFT MX, PCI DSS | Message schemas, party roles, transaction types |
| Risk & Compliance | Basel III / BCBS, FATF | Risk entities, regulatory metadata |
| Local Compliance | APRA (AU), FCA (UK), OCC (US) | Retention, classification, regulatory_scope |
| Cross-jurisdiction Privacy | GDPR, CCPA, PDPA | PII metadata, retention, consent events |
| Insurance | ACORD, IAIS | Policy, claim, underwriting entities |
| Healthcare | HL7 FHIR, SNOMED CT, ICD-10 | Clinical entities, terminology |
| Telecoms | TM Forum SID, eTOM | Party, product, service entities |
| Retail / Supply Chain | GS1, eCl@ss | Product, location, shipment entities |
| Cross-industry | ISO 8601 (dates), ISO 4217 (currency), ISO 3166 (country) | Attribute types and enum values |

---

## How to Apply a Standard Reference

### Step 1 — Confirm the mapping exists
Do not silently map a concept to a standard if the fit is approximate. Check that
the standard actually defines a counterpart to the entity or attribute being modelled.

For BIAN BOM, use the dedicated guidance in [BIAN standard guidance](./standards/bian.md).
It defines the deterministic lookup sequence, candidate disambiguation rules,
version parameters, and no-guess policy.

For ISO 20022, consult the message definition catalogue for the relevant message type.

For HL7 FHIR, reference the resource definitions at `https://hl7.org/fhir/resourcelist.html`

### Step 2 — Note material differences
If the standard's definition differs from the user's intent, say so explicitly:

> "In BIAN BOM, 'Party' is defined as [standard definition]. Your usage adds [X].
> This is close enough to reference BIAN, but we should note the extension in the
> entity description."

### Step 3 — Format the reference link
Use the `Reference` column in summary tables and in entity descriptions:

```markdown
| `Customer` (`entities/customer.md#customer`) | `Party Role` (`entities/party_role.md#party-role`) | A Party with an active product relationship. | `BIAN BOM - Party Role` (`https://bian-modelapi-v4.azurewebsites.net/BOClassByName/PartyRole`) |
```

For multiple applicable standards, list the most specific first.

### Step 4 — Carry references into metadata
When a regulatory standard applies to the domain, add it to `regulatory_scope`
in the domain YAML — not just to the Reference column:

```yaml
regulatory_scope:
  - GDPR
  - BCBS 239
  - APRA CPS 234
```

---

## Approximate vs. Exact Mapping

| Signal | Action |
|---|---|
| Concept name and definition match the standard closely | Reference directly; no note needed |
| Concept is a specialisation of a standard object | Reference the parent; note the specialisation in the entity description |
| Concept partially overlaps a standard object | Reference with a qualification: "Partial alignment — [difference]" |
| No standard counterpart exists | Do not force a reference; leave the Reference column empty |

**Never fabricate a reference URL** to make the model look more aligned than it is.
A missing reference is honest; a wrong one is harmful.

For BIAN specifics (including endpoint order and exact-name resolution), follow [BIAN standard guidance](./standards/bian.md).

---

## Regulatory Metadata Prompt

When a domain's `regulatory_scope` is being populated, prompt the user with this
checklist. Many teams underspecify this because they assume "someone else handles
compliance."

- Does this domain hold personal data about individuals? → GDPR / CCPA / PDPA
- Does this domain support financial reporting? → SOX / BCBS 239
- Does this domain hold transaction or payment data? → PCI DSS / AML / FATF
- Does this domain support credit risk assessment? → Basel III
- Does this domain hold health information? → HIPAA / HL7
- Is the institution regulated in Australia? → APRA CPS 234 / CPG 235
- Is the institution regulated in the EU? → DORA / EU 5AMLD / 6AMLD
- Is the institution regulated in the UK? → FCA COBS / SYSC

For each applicable framework, confirm with the user whether it affects:
- The `classification` or `pii` flags
- The `default_retention` value
- Any specific attribute-level governance (e.g., credit scores under ECOA)
