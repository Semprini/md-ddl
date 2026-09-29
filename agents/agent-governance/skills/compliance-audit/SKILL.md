---
name: compliance-audit
description: Use to evaluate MD-DDL domain, entity, and product files for governance completeness and correctness against loaded regulatory frameworks, when the user asks "is this compliant?", "what's missing?", or for a gap report, and after a regulatory monitoring pass flags a change. Defines how to audit; the requirements come from the regulatory-compliance skill and its regulator files, which must be loaded first.
---

# Skill: Compliance Audit

Audit governance metadata against the regulator files loaded through the
regulatory-compliance skill. That skill also defines the field schema: the spec's core
fields plus the labelled extension fields. This is a quality review, not a lint pass
(`1-Foundation.md § Validation Model`).

Two principles govern every finding:

- **Inheritance is correct by default.** Domain metadata sets the posture, and an entity
  or product without a `governance:` block inherits it. A missing block is a gap only
  when that entity has obligations the domain defaults don't satisfy.
- **Vocabulary deviations are observations.** `phi` for `pii`, or `data_sensitivity` for
  `classification`, is a "potential spec vocabulary gap", not a failure. It's never
  Critical unless an obligation is left unrepresented.

---

## Setup

1. **Regulatory frame.** Start from `regulatory_scope` and ask the user to confirm it's
   complete. If it's absent, ask which jurisdictions apply. Don't infer jurisdiction
   from domain content: the same Financial Crime domain has different obligations at an
   Australian bank and a US bank.
2. **Regulator files.** Load only those that apply, using the mapping in the
   regulatory-compliance skill, and check their `last_verified` dates. Tell the user which
   frameworks the audit covers. Anything else is out of scope.
3. **Scope.** A domain file (following links to detail files), a single entity (note the
   missing domain context), or a whole corpus (one domain at a time, then a summary).

---

## Level 1 — Domain Metadata

The `## Metadata` block of `domain.md`:

Field | Gap if
--- | ---
`classification` | Absent or not a valid tier
`pii` | Absent
`regulatory_scope` | Absent or empty
`default_retention` | Absent
`owners`, `stewards` | Absent: no accountability

Then check it against the loaded frameworks:

- **Residency:** where a framework localises data (e.g. APRA, PDPA), is `data_residency`
  declared, and does it satisfy the requirement?
- **Multiple jurisdictions:** does `regulatory_scope` cover every applicable framework?
- **AML/CTF:** when FATF is loaded, is AML/CTF scope present in `regulatory_scope`?
- **Consistency:** is the domain `classification` at least as restrictive as the most
  sensitive entity override in the domain?

## Level 2 — Entity Governance

For each entity, first decide whether it has obligations beyond the domain defaults. The
signals are a stricter retention period, specific reporting, access logging, breach
notification, and residency. Then:

- **It has none, and there's no block.** Correct. It inherits. Not a gap.
- **It has some, but there's no block.** A gap: name the obligation and the missing field.
- **An annotation says "No specific regulatory requirements identified".** Not a gap. Note
  it as "explicitly excluded; confirm still accurate".

Where a block exists or is needed:

Field | Check
--- | ---
`pii`, `classification`, `retention` | Present only where they differ from the domain. A weaker posture than the domain's needs a justification.
`retention_basis` | Cites the regulatory source whenever `retention` is overridden
`retention` | Not shorter than the regulatory minimum. Its lifecycle trigger (e.g. "post relationship end") exists in the entity.
`compliance_relevance` | Lists the specific acts that apply directly to the entity
`regulatory_reporting` | Names the reports and submissions the entity feeds
`audit_all_access`, `breach_notification_required`, `notification_timeframe`, `data_residency` | Extension fields. Required where a loaded regulator file requires them, and `notification_timeframe` whenever breach notification is required.

**PII.** When an entity is PII-bearing (its own or the domain's `pii: true`), review its
attributes against the loaded frameworks' definitions. Look at names, date of birth,
government identifiers, contact details, biometrics, account numbers, and IP addresses
under GDPR. Check that each is marked, either by `pii: true` on the attribute or by
listing it in `pii_fields`. `pii_fields` itself is optional; it's required only where a
loaded framework demands an enumerated inventory (GDPR Article 30, HIPAA Safe Harbor).

**Breach notification.** Check `notification_timeframe` against the loaded file (for
example GDPR 72 hours, RBNZ 72 hours, APRA "as soon as possible"; US state laws vary).

## Level 3 — Attributes

Run this level when an entity is PII-bearing, when a regulator file sets attribute-level
obligations, or when the user asks. Look for:

- attributes whose names suggest sensitivity (Health Status, Biometric Data) but which
  aren't marked PII
- attribute `classification` above the entity's
- under GDPR, Article 9 special categories: ethnicity, political opinions, religion,
  union membership, genetic, biometric, health, and sex life or orientation data

## Level 4 — Data Products

Run this level for full-corpus audits, product questions, and after product design.
Products may narrow visibility by design, but must never weaken protections below what
regulation requires.

Check | Gap if
--- | ---
Classification override | Lower than the domain's without justification
PII masking | A PII attribute from any included entity (attribute markers or `pii_fields`) has no `masking` entry
Masking adequacy | The strategy is too weak (e.g. `truncate` on a government ID) or too strong for the need (e.g. `redact` where joinability is required)
Source-aligned raw feeds | Raw PII without restricted consumers, declared retention, and either masking or a documented justification (e.g. audit replay)
Multi-domain lineage | Classification below the highest contributing domain's; retention below the longest; PII or regulatory scope from another domain unacknowledged
Overrides | An override without a stated reason
Consumers | Broad audiences on a highly confidential product
Declaration completeness | Missing `lineage`, missing a logical model where `schema_type` is set, or a consumer-aligned product without an Attribute Mapping

Masking and scope fixes are recommendations. Agent Architect applies them.

## Level 5 — Lifecycle Consistency

This checks the integrity of lifecycle fields, not promotion readiness (that's Agent
Ontology's lifecycle skill).

Check | Severity
--- | ---
Domain, entity, or product `status` invalid, or more advanced than its parent domain | Critical
Active domain without `version` | Critical
Active domain below `1.0.0`; invalid semver | Advisory
Deprecated domain without `superseded_by`; deprecated entity without `deprecated_at`; post-1.0.0 entity without `since` | Advisory
Active product without `version`; deprecated product without `deprecated_date` (and `successor` where one exists) | Advisory
Active product depending on deprecated entities or domains, with no `migration_note` | Advisory

---

## Jurisdiction Conflicts

When several regulator files are loaded, look for conflicts before reporting:

Conflict | Default
--- | ---
Retention | The longer period
Classification | The higher tier
Notification timeframe | The shorter window
Residency | None. It needs a legal decision, so report it as Critical.

List conflicts in a Jurisdiction Conflicts section of the report and don't apply either
side until the conflict has been reviewed.

## Severity

**Critical:** an obligation is clearly unmet, or a required anchor is missing entirely:

- a missing Level 1 field
- retention below the regulatory minimum
- a notification window exceeding the maximum
- PII attributes unmarked where the loaded framework requires identification
- GDPR special-category data with no Article 9 treatment
- an unmasked PII attribute in a product
- a residency conflict
- a regulator-required extension field that's absent

**Advisory:** a best practice is unmet, or something needs confirmation:

- `retention_basis` missing
- a sensitivity-suggesting attribute left unmarked
- a recommended (not mandated) extension field missing
- an explicit exclusion that may be outdated
- a vocabulary deviation

**Not assessed:** there wasn't enough information. For example, detail files were
unavailable, jurisdiction was unconfirmed, or attributes weren't visible.

---

## Gap Report

```markdown
## Compliance Gap Report — [Domain Name]
**Assessed against:** [frameworks] | **Regulator files verified:** [dates] | **Date:** [date]
**Scope:** [full | incremental — triggered by <change>; last full audit <date>]

### Summary
[n] gaps across [n] entities and [n] products: [n] critical, [n] advisory, [n] not assessed.

> Requirements are taken from regulator guidance files last verified on the dates shown.
> This is not legal advice. Confirm obligations with qualified legal or compliance counsel.

### Critical Gaps
| Level | Entity / Product | Gap | Required by | Recommended fix |

### Advisory Gaps
| Level | Entity / Product | Gap | Framework | Recommended action |

### Jurisdiction Conflicts
| Frameworks | Conflict | Default applied | Decision needed |

### Observations
Vocabulary deviations and explicit exclusions to confirm.

### Not Assessed
What couldn't be assessed, and why.

### Coverage
Entities [n of n] · Attribute level [run / not run, and why] · Products [run / not run] · Lifecycle [run / not run]
```

**Incremental audits** follow a Regulatory Monitoring pass. Audit only the fields affected
by each material change, and say so in the report header. Otherwise already-known gaps
resurface as noise.

If the regulator files are stale, recommend a Regulatory Monitoring pass before treating
the audit as definitive.
