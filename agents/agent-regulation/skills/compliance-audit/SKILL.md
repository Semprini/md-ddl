---
name: compliance-audit
description: Systematically evaluate MD-DDL domain and entity files for governance metadata completeness and correctness against loaded gulatory frameworks. Use when auditing a domain file or corpus for compliance gaps, when the user asks "is this compliant" or "what's missing", when preparing a gap report, or after a regulatory monitoring pass identifies a potential impact. Always load the regulatory-compliance skill and relevant regulator files before running an audit — this skill defines how to audit, not what the requirements are.
---

# Skill: Compliance Audit

Defines the systematic process for evaluating MD-DDL files against regulatory
requirements. This skill does not contain regulatory requirements — those live
in `skills/regulatory-compliance/` and its regulator reference files. Load those
first, then use this skill to drive the audit.

---

## Pre-Audit Setup

Before beginning any audit, complete this setup. Do not skip steps.

### 1. Establish the regulatory frame

Confirm with the user which jurisdictions and frameworks apply. Do not infer
jurisdiction from domain content alone — a Financial Crime domain at an
Australian bank and the same domain at a US bank have different obligations.

If `regulatory_scope` is declared in the domain metadata, use it as the starting
point but ask the user to confirm it is complete:

> "Your domain metadata declares [frameworks]. Before I audit, can you confirm
> this list is complete and current? Are there jurisdictions or frameworks that
> apply but aren't listed here?"

If `regulatory_scope` is absent, ask directly:

> "I don't see a `regulatory_scope` declared in this domain's metadata. Before
> I can audit effectively, I need to know which regulatory frameworks apply.
> What jurisdictions does this data operate under?"

### 2. Load regulator files

Load only the regulator files that apply. Reference
`skills/regulatory-compliance/SKILL.md` for the jurisdiction-to-file mapping.
Confirm which files are loaded before proceeding:

> "I've loaded requirements for: [list]. I'll audit against these frameworks only.
> Anything not covered by these files is out of scope for this audit."

### 3. Establish corpus scope

Determine what is being audited:

- **Single domain file** — audit the domain metadata and all entity references
  within it, then follow links to entity detail files if available
- **Entity detail file only** — audit that entity in isolation; note that
  domain-level context may be missing
- **Full corpus** — audit all domain files; treat each domain as a separate
  audit scope with its own regulatory frame

For full corpus audits, process one domain at a time and produce a gap report
per domain, then a summary across all domains.

---

## The Three Governance Levels

MD-DDL governance obligations exist at three distinct levels. An audit must
check all three — gaps at any level are compliance risks.

```
Level 1: Domain Metadata          (domain.md → ## Metadata → YAML block)
Level 2: Entity Governance Block  (entity detail file → ## Entities → ### Entity → governance: YAML)
Level 3: Attribute-Level Flags    (entity detail file → attributes: → individual fields)
Level 4: Product Governance       (products/*.md → ### Product → governance: + masking: YAML)
```

**Inheritance rule:** Domain-level metadata sets the default posture. Entities
inherit that posture unless they explicitly override it. An entity with no
`governance:` block is not automatically compliant — it inherits the domain
defaults, which may themselves be incomplete. Products inherit domain governance
and must justify any overrides.

---

## Level 1 — Domain Metadata Audit

Evaluate the domain `## Metadata` YAML block.

### Required fields checklist

For every domain, regardless of regulatory frame, check:

| Field | Check | Gap if absent |
|---|---|---|
| `classification` | Present and uses a valid tier | Domain sensitivity undefined |
| `pii` | Present as boolean | PII posture not declared |
| `regulatory_scope` | Present, non-empty list | No regulatory frame established |
| `default_retention` | Present with a defined period | Retention obligations unknown |
| `owners` | At least one entry | No data accountability |
| `stewards` | At least one entry | No governance accountability |

### Regulatory frame checks

Once regulator files are loaded, evaluate additional fields:

**For any jurisdiction with data localisation requirements (e.g. APRA, PDPA):**
- Is `data_residency` declared?
- Does the declared residency satisfy the loaded requirements?

**For multi-jurisdiction domains:**
- Is `dual_reporting` declared where applicable?
- Are all `reporting_frameworks` listed?

**For AML/CTF scope (FATF loaded):**
- Is the domain's AML/CTF relevance indicated in `regulatory_scope`?

### Classification consistency check

The `classification` value at domain level must be at least as restrictive as
the most sensitive entity within the domain. If you find an entity with
`classification: "Highly Confidential"` in a domain marked `classification:
"Internal"`, that is a Level 1 gap.

---

## Level 2 — Entity Governance Block Audit

For each entity in the domain, locate the `governance:` block in its detail file
and evaluate it. If the detail file is not available, note this and audit only
what can be seen from the domain summary table.

### Distinguishing absence types

Before logging a gap, determine *why* a `governance:` block is absent:

**Type A — Not yet applied:** The entity has no `governance:` block and no
`# No specific regulatory requirements identified` annotation. Treat as a gap.
Recommend: full governance pass by Agent Regulation.

**Type B — Explicitly excluded:** The entity has a `# No specific regulatory
requirements identified` annotation. Do not log as a gap. Note in the audit
report as "Governance explicitly excluded — confirm this is still accurate."

**Type C — Inherited from domain:** The entity has no `governance:` block but
the domain-level metadata covers all applicable obligations for this entity type.
Evaluate the domain-level metadata against entity-specific requirements. Log a
gap only if entity-specific obligations exist that cannot be satisfied by domain
inheritance.

### Entity governance checklist

For each entity with a `governance:` block (or where one is required):

| Field | Check | When required |
|---|---|---|
| `classification` | Present and consistent with domain level | Always |
| `pii` | Present as boolean | Always |
| `pii_fields` | Lists specific attributes containing PII | When `pii: true` |
| `regulatory_scope` | Lists applicable frameworks for this entity | When entity has specific obligations beyond domain defaults |
| `retention` | Specific period declared | When retention obligation applies |
| `retention_basis` | Cites the specific regulatory source | When `retention` is present |
| `audit_all_access` | Declared | When regulator requires access logging |
| `breach_notification_required` | Declared | When regulator requires notification |
| `notification_timeframe` | Declared | When `breach_notification_required: true` |
| `data_residency` | Declared | When entity data may be subject to localisation rules different from domain default |

### Retention consistency check

When an entity has a `retention` value, verify it is consistent with the loaded
regulator guidance. Flag as a gap if:
- The declared period is shorter than the regulatory minimum
- The declared period references a lifecycle event not defined in the entity
  (e.g. "post relationship end" when no relationship end date attribute exists)
- The `retention_basis` cites a standard that is not in the loaded regulator files

### PII completeness check

When `pii: true` is declared on an entity:
1. Review the entity's attributes (from detail file YAML or domain summary)
2. Identify attributes that carry personal data under the loaded regulatory
   definitions of PII
3. Compare against the declared `pii_fields` list
4. Flag as a gap if attributes that qualify as PII under the loaded frameworks
   are not listed

Common PII attributes to check for: name fields, date of birth, government
identifiers (tax numbers, passport, licence), contact details (email, phone,
address), biometric data, financial account numbers, IP addresses (under GDPR).

### Notification timeframe verification

When `breach_notification_required: true` is declared, verify the
`notification_timeframe` against the loaded regulator requirement. Flag as
critical if:
- The declared timeframe exceeds the regulatory maximum
- The field is absent when `breach_notification_required: true`

Common timeframes to verify against loaded files: GDPR 72 hours, APRA
"as soon as possible", RBNZ 72 hours, US state laws vary.

---

## Level 3 — Attribute-Level Audit

Evaluate individual attributes within entity YAML for PII and sensitivity flags
that may be missing or inconsistent.

### When to run Level 3

Level 3 audit is triggered by:
- `pii: true` on an entity — verify individual attribute flags are consistent
- A regulator file that specifies attribute-level obligations (e.g. GDPR special
  categories of personal data)
- A specific concern raised in the user's audit request

### Attribute flags to check

| Flag | Check |
|---|---|
| `pii: true` on attribute | Present on attributes identified as PII in Level 2 check |
| `classification` on attribute | Present if attribute sensitivity exceeds entity default |
| Sensitive type patterns | Attributes with names suggesting high sensitivity but no PII flag (e.g. `Health Status`, `Biometric Data`, `Sexual Orientation`) |

### Special categories check (GDPR)

If GDPR is in the loaded frameworks, check for attributes that may constitute
special categories of personal data under Article 9:
racial or ethnic origin, political opinions, religious beliefs, trade union
membership, genetic data, biometric data, health data, sex life or orientation data.

If any such attributes are present without explicit GDPR special category
governance metadata, log as a critical gap.

---

## Multi-Jurisdiction Conflict Detection

When multiple regulator files are loaded, conflicts may exist between their
requirements. Detect and surface these before producing the gap report.

### Conflict types

**Retention conflict:** Two frameworks require different retention periods.
Resolution: apply the longer period; note the conflict.

**Classification conflict:** Two frameworks classify the same data type at
different sensitivity levels.
Resolution: apply the higher classification; note the conflict.

**Residency conflict:** Two frameworks require data to reside in different
jurisdictions.
Resolution: do not resolve automatically — this requires legal/compliance
team input. Flag as a critical gap requiring human decision.

**Notification conflict:** Two frameworks require notification within different
timeframes.
Resolution: apply the shorter timeframe; note the conflict.

When a conflict is detected, add it to the gap report under a dedicated
"Jurisdiction Conflicts" section and do not apply either requirement
automatically until the conflict section is reviewed.

---

## Producing the Gap Report

Use the gap report format defined in `agents/agent-regulation/AGENT.md`.
Apply these severity rules when classifying gaps:

### Critical
A regulatory obligation is clearly unmet and the gap creates direct exposure:
- Required field absent entirely
- Retention period shorter than regulatory minimum
- Breach notification timeframe exceeds regulatory maximum
- PII declared but `pii_fields` empty
- GDPR special category data with no Article 9 governance metadata
- Jurisdiction conflict on data residency (human decision required)
- `breach_notification_required` absent on entities in scope

### Advisory
Best practice is not met, or a field needs confirmation to determine if a
gap exists:
- `retention_basis` absent (retention is declared but source not cited)
- Entity-level `classification` not declared (inheriting from domain — confirm
  this is correct)
- `audit_all_access` not set on entities where regulator guidance recommends
  but does not mandate it
- `regulatory_scope` at entity level not declared where entity has obligations
  that differ from the domain default
- Attributes with sensitivity-suggesting names but no PII flag
- Type B absences (explicit exclusion annotations that may be outdated)

### Not Assessed
Gaps that cannot be evaluated due to missing information:
- Entity detail file not available (only domain summary table accessible)
- `regulatory_scope` absent and user was unable to confirm jurisdiction
- Attribute list not visible (cannot complete Level 3 audit)

---

## Incremental Audit (Post-Monitoring)

When running an audit triggered by a regulatory monitoring pass (Mode 2 in
AGENT.md), focus the audit scope on the specific changes identified:

1. Load the monitoring report
2. For each material change flagged, identify the affected metadata fields
3. Audit only those fields across the relevant domains — do not re-run the
   full audit unless requested
4. Note in the gap report header: "Incremental audit — triggered by [change].
   Full audit last run [date if known]."

This keeps monitoring-triggered audits focused and actionable rather than
producing noise by re-surfacing already-known gaps.

---

## Level 4 — Product Governance Audit

Evaluate each data product declaration for governance adequacy. Product governance
sits on top of domain and entity governance — a product may relax visibility
(by design) but must not weaken protections below what regulations require.

### When to run Level 4

Level 4 is triggered by:

- User asks "are the governance overrides appropriate for each product?"
- User asks about product-level compliance or masking adequacy
- Full corpus audit (always include Level 4 if product declarations exist)
- After product design or modification (as a quality gate)

### Product governance checklist

For each product declaration (files under `products/`):

Check | What to verify | Gap if failed
--- | --- | ---
**Classification override** | If product declares `classification` lower than domain default, is there a justified reason? | Unjustified classification downgrade
**PII exposure** | If product includes entities where `pii: true`, does the product declare `masking` entries? | PII-bearing product with no masking strategy
**Masking completeness** | Every attribute listed in included entities' `pii_fields` has a corresponding `masking` entry in the product | PII attribute exposed without masking
**Masking strategy adequacy** | Masking strategy is appropriate for the attribute type and consumer context | Weak masking for high-sensitivity attribute
**Source-aligned raw exposure** | Source-aligned products that expose raw PII: is retention constrained and access restricted? | Raw PII feed with permissive governance
**Cross-domain governance** | For `cross_domain` references: does the product honour the governance posture of the owning domain? | External entity exposed with weaker controls than source domain
**Governance override justification** | Every field in the product's `governance:` block that differs from domain default has a documented rationale | Override present without justification
**Consumer appropriateness** | Are the declared `consumers` appropriate for the product's classification and PII posture? | Highly confidential product visible to broad audiences

### Masking adequacy cross-reference

This is the critical product-level check that connects entity PII declarations
to product masking rules.

For each product where `pii: true` applies (inherited or declared):

1. Collect all entities in the product's `entities` list
2. For each entity, read its `pii_fields` from the entity governance block
3. Build a complete list of PII attributes exposed by this product
4. Compare against the product's `masking` entries
5. Flag gaps:

Gap Type | Severity | Description
--- | --- | ---
PII attribute with no masking entry | Critical | Attribute is exposed unmasked to product consumers
Masking strategy mismatch | Advisory | Strategy may be too weak (e.g., `truncate` for a government ID) or too strong (e.g., `redact` when joinability is needed)
PII attribute not in `pii_fields` | Critical | Attribute appears to be PII but is not declared — escalate to Level 2/3

### Source-aligned product controls

Source-aligned products are inherently higher-risk because they expose raw or
lightly cleansed data. Apply these checks:

- `classification` should be at least as restrictive as any entity in the source feed
- `retention` should be declared (raw data often has shorter retention than canonical)
- `consumers` should be limited to data engineering and audit teams
- If the source contains PII, the product should either declare `masking` or
  document why raw PII access is justified (e.g., audit replay requirements)

### Product governance gap report format

Add a "Product Governance" section to the gap report:

```markdown
### Product Governance Gaps

| Product | Gap | Severity | Recommended Fix |
|---|---|---|---|
| Transaction Risk Summary | `Date of Birth` in Customer entity not covered by `masking` entries | Critical | Add `masking: - attribute: "Date of Birth" strategy: year-only` |
| Salesforce Raw Feed | Source-aligned product exposes raw PII with no masking | Advisory | Confirm audit-replay justification or add masking entries |
```

---

## Audit Completion Statement

Close every audit with a structured statement before handing the gap report
to the user:

```
Audit complete.
Scope: [domain name(s)]
Frameworks assessed: [list]
Regulator files loaded: [list]
Entities assessed: [n] of [n] (note any not assessed)
Attribute-level audit: [run / not run — reason if not run]
Gaps identified: [n] critical, [n] advisory, [n] not assessed
Conflicts detected: [n — list frameworks in conflict if any]

Refer to the gap report below for details and recommended remediation.
Note: This audit reflects requirements as defined in the loaded regulator files.
If those files have not been updated recently, run a regulatory monitoring pass
(Mode 2) to confirm currency before treating this audit as definitive.
```
