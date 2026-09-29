# Skills Review — Simplification for Current Models

**Date:** 2026-09-29
**Follows:** [2026-09-29-agent-definitions-review.md](2026-09-29-agent-definitions-review.md), which simplified the core prompts and named the skills as the next step.
**Scope:** Instruction files only: each `SKILL.md` and the guidance files it loads. Reference data is out of scope and unchanged: industry-standard extracts, regulator files, the ODPS schema, dialect notes, the `references/` include stubs, and the Python runtime.

## Summary

Agent | Before | After
--- | --- | ---
Agent Guide | 1,470 | 533
Agent Ontology | 3,422 | 2,175
Agent Artifact | 2,177 | 1,733
Agent Architect | 1,327 | 1,242
Agent Governance | 909 | 476
Agent Test | 288 | 290
**Total** | **9,593** | **6,449**

The line count matters less than the defects. The review found about 40 bugs where a
skill taught something wrong. The most serious were:

- **Invalid syntax.** Skills taught syntax the spec doesn't accept: `identifier: true`,
  `required:`, `specializes:`, list-form event attributes, and a domain governance wrapper.
  An agent following them produces files that fail review.
- **False audit findings.** Compliance Audit contradicted governance inheritance and would
  have flagged every well-modelled domain.
- **Broken paths and imports.** Cross-agent paths didn't resolve, the faker template's
  import could never run, and Standards Conformance pointed at snapshots that aren't installed.
- **Fabricated or contradictory references.** Standards Alignment's BIAN worked example
  cited class names absent from the index, and ISO 20022 guidance contradicted its own
  local file.
- **Stale facts.** There was a "no linter" claim, pre-`md-ddl init` setup steps,
  wrong example values and folder names, and a stub file with literal placeholders.

Every retained factual claim was checked against the repository. Code in skills was
executed where it could be. The Agent Artifact section corrects the agent-definitions
review, which wrongly recorded the generation skills' paths as correct.

Spec and example follow-ups are listed under each agent. The main ones: governance
extension fields as spec candidates, `masking` placement in `9-Data-Products.md`,
`products/` vs `data_products/`, and two Financial Crime BIAN references to verify.

## Principles

The same as for the core prompts, plus three specific to skills:

1. **Don't restate the core prompt.** The teaching loop, the handoff protocol, and the output rules are already in `AGENT.md`.
2. **Don't restate the spec.** Skills load the spec, so they carry the judgement the spec leaves open, not a paraphrase of it.
3. **Don't copy facts that drift.** Counts, folder names, and install steps belong where they are maintained (`examples/README.md`, `README.md`), and skills point there.

Every factual claim that was kept was checked against the repository. Stale claims are listed as bugs.

---

## Agent Guide

File | Before | After
--- | --- | ---
orientation | 153 | 60
concept-explorer | 663 | 251
worked-examples | 259 | 87
adoption-planning | 121 | 52
platform-setup | 274 | 83
**Total** | **1,470** | **533**

**Bugs**

- GU1: concept-explorer taught "Why MD-DDL doesn't have a traditional linter" and "five pre-flight checks". The repo ships `md-ddl lint`, and pre-flight now also checks agreement between the diagram, the tables, and the YAML. The section was rewritten to describe the linter as tier 1 and to point to `guides/validation-tooling.md`.
- GU2: platform-setup described only manual submodule setup, and said Claude Code has no agent commands. `pip install md-ddl && md-ddl init` is the recommended path and installs `/agent-*` slash commands. It now follows `README.md § Quick Start`.
- GU3: worked-examples said Financial Crime's Transaction is "not dependent on Account". `transaction.md` declares `existence: dependent`.
- GU4: worked-examples pointed to `products/`. The examples use `data_products/`. It also hard-coded entity counts that had drifted, and listed three of the seven examples. It now uses the coverage matrix in `examples/README.md`.
- GU5: the playbook's staleness rule says adoption-planning flags stalled adoptions. The skill never mentioned it. Added.

**Simplifications**

- concept-explorer's six-step teaching protocol repeated the core prompt's Teach loop. Only the analogy table and the structure-showing guidance were kept.
- The eventual-consistency section (135 lines) duplicated Agent Architect's architecture skill. It was cut to what a learner needs to know and how it's declared, with a pointer to the architecture skill.
- The synthetic-data section (180 lines) duplicated the faker skill's profile mechanics. Only the conversational discovery questions, which are unique to the Guide, were kept.
- Scripted overview quotes in orientation became a table of what to emphasise for each archetype. The workflow table was removed because it repeats the core prompt.
- Analogy table: added Worked Example. The dbt comparison now covers dbt project generation and Agent Test.

---

## Agent Ontology

File | Before | After
--- | --- | ---
domain-scoping (+ domain-boundaries, unchanged) | 475 | 221
entity-modelling | 246 | 141
entity-modelling/guidance (absorbed inheritance-patterns) | 670 | 100
entity-modelling/conceptual-to-physical-realisation (unchanged) | 148 | 148
relationship-events | 192 | 101
standards-alignment | 255 | 104
domain-review | 304 | 296
source-mapping | 400 | 331
schema-import | 288 | 289
lifecycle | 192 | 191
preflight | 127 | 128
baseline-capture (unchanged) | 125 | 125
**Total** | **3,422** | **2,175**

**Bugs**

- ON1: `inheritance-patterns.md` was an unfinished stub. It contained literal placeholders (`[Deep explanation]`, `[Detailed edge case handling]`, `[Full worked examples from each industry]`) and a dangling code fence, used a `specializes:` key (the spec uses `extends:`), and listed Creditor and Debtor as Party Role subtypes while `guidance.md` called them relationship attributes. A completed, consistent version now lives in `guidance.md`, and the stub was deleted.
- ON2: `guidance.md` examples used `- specializes:` bullets and `# Entities` H1s. That isn't MD-DDL syntax, and an agent copying them would produce invalid files. Its examples are now decision tables.
- ON3: `identifier: true` appeared in entity-modelling, domain-review (the readiness definition), schema-import, and lifecycle. The spec value is `identifier: primary`, and entities without an identifier are Logic Objects (a "should", not a "must").
- ON4: schema-import mapped nullability to `required: true/false`, a property the spec doesn't have (nullability is a `not_null` constraint). It also never said that FK columns become relationships rather than attributes.
- ON5: relationship-events' timestamp example used a list of single-key maps, which `6-Events.md` Rule 8 forbids. It also omitted `related_to` and self-referential relationships, and called an extensible type list "approved".
- ON6: standards-alignment's BIAN worked example cited `IndividualEntity` and `CustomerRole`, which are absent from the local v13 index. The skill was demonstrating the fabrication it forbids. The example now shows verifying each reference against the index.
- ON7: standards-alignment said to consult the ISO 20022 *message definition* catalogue, while the local `standards/iso20022.md` says to reference Business Components, "NOT Message Definitions". It never pointed to the local file.
- ON8: entity-modelling contradicted itself and the spec on governance blocks. It required a `retention_basis`-only block for inheriting entities, where the spec says one "may" be included.
- ON9: the Preflight skill wasn't listed in Agent Ontology's skill table, so nothing routed to it. Its rule table also lacked `domain-table-coverage`.
- ON10: lifecycle gated promotion to Active on the "Layer 1/2/3 review", which is the process for reviewing the MD-DDL standard itself. It now gates on Domain Review and Preflight.
- ON11: domain-review never ran the linter for the mechanical tier. It also referred to "four summary tables", and to an Observations section its output format didn't define.
- ON12: schema-import set `adoption.maturity: mapped` on the first draft, before any transform detail existed.
- ON13: entity-modelling still called Agent Governance the "Regulation Agent".

**Simplifications**

- domain-scoping's requirements-intake and user-story tables duplicated entity-modelling. The user-story mapping now lives only in entity-modelling.
- source-mapping and relationship-events re-explained spec content they load (fan-out keys, worked-example format, relationship type definitions). They now keep the judgement and point to the spec for the format. The transform-detail checklist now defers to the Determinism Test it duplicated.
- Scripted user-facing quotes were replaced by what to ask or say, throughout.

**Follow-up (not changed here)**

- Financial Crime's `domain.md` references BIAN `LegalEntity` and `Payment`, which aren't in the local v13 class index. They may come from the v4 API naming. This needs a standards check by Agent Ontology.
- The spec's example layout uses `products/`, while the example domains use `data_products/`. One of them should change.

---

## Agent Artifact

File | Before | After
--- | --- | ---
dimensional | 279 | 231
normalized | 326 | 278
wide-column | 264 | 248
knowledge-graph | 288 | 277
reconciliation | 188 | 188
faker | 609 | 288
dbt-project (current) | 223 | 223
**Total** | **2,177** | **1,733**

The generation skills carry real design knowledge: inheritance DDL patterns, grain and
join admissibility, graph mapping. They were trimmed, not rewritten.

**Bugs**

- AR1: dimensional, normalized, wide-column, and knowledge-graph referenced
  `../../agent-ontology/...`. From `skills/<name>/`, that resolves to a folder that doesn't
  exist (`agents/agent-artifact/agent-ontology/`). The correct path is
  `../../../agent-ontology/...`. The agent-definitions review wrongly recorded these as correct.
- AR2: faker's code template imported
  `agents.agent_artifact.skills.faker.runtime.enterprise_profile`. The folder is
  hyphenated and `agents/` isn't a package, so the import fails
  (`ModuleNotFoundError`). The template now imports the runtime copied alongside the
  module. The code pattern was executed to confirm it runs in both PII modes, with and
  without a profile.
- AR3: faker's example factory generated realistic birth dates in `safe` mode,
  contradicting its own override table. It also put product, amount, and currency on
  Party. The example now follows the table and models Party alone.
- AR4: faker described the US fintech profile's markets as "US, ES, ZH". The profile's
  locales are `es_US` and `zh_CN` customer segments, and "ZH" is not a country.
- AR5: knowledge-graph offered a Cypher `CHECK` constraint for enum values, which Neo4j
  doesn't have. Its "composite" node-key example used one property, and it didn't note
  that `NODE KEY` is Enterprise-only.
- AR6: normalized described the classDiagram inheritance arrow as "Entity YAML".
- AR7: reconciliation handed baseline status updates to "the baseline-capture skill",
  which belongs to Agent Ontology and can't be loaded by Agent Artifact.

**Simplifications**

- The existence, mutability, and temporal matrices in dimensional and normalized repeated
  `references/generation-semantics.md`, which `AGENT.md` loads for every generation. Only
  the style-specific notes were kept.
- The "Output Contract" and "Generation Limitations" sections duplicated `AGENT.md`'s
  Generate step and Limits. Where a skill's output contract was style-specific
  (wide-column's grain statement, knowledge-graph's templates), it was kept.
- Generation skills no longer load Agent Ontology's authoring skills (entity-modelling,
  relationship-events) on every request. Only `conceptual-to-physical-realisation.md` is
  needed. Wide-column no longer loads both sibling skills.
- faker: 609 lines down to 288, removing a duplicate profile walkthrough, the scripted
  offers, and a 150-line example factory.

---

## Agent Architect

File | Before | After
--- | --- | ---
architecture | 489 | 420
product-design (+ platform-posture) | 511 | 496
odps-alignment | 327 | 326
**Total** | **1,327** | **1,242**

These skills are mostly substantive: the tenet table with counter-positions, the
comparison framework, output formats, and the product design steps. The changes here
are corrections more than cuts.

**Bugs**

- AA1: odps-alignment mapped a `Production` status that MD-DDL products don't have, and
  had no mapping for `Active` or `Retired`. It is now Draft → draft, Active →
  production, Deprecated → sunset, Retired → retired, all checked against the local ODPS
  vocabulary.
- AA2: odps-alignment mapped `dimensional` to format `SQL`, but SQL is an ODPS output
  port type, not a format. It also treated `schema_type` as deciding the delivery
  channel. The channel is now proposed and marked for confirmation.
- AA3: odps-alignment presented invented data-quality objectives (PII implies 98%
  accuracy, more than 80% not-null implies 95% completeness) as if derived from the
  model. They are now marked `# PROPOSED`, the accuracy target is left to the owner,
  and Agent Test's data-test results are named as better evidence.
- AA4: odps-alignment's reference path was relative to the wrong folder.
- AA5: product-design's declaration template omitted the `Retired` status.
- AA6: `platform-posture.md` pointed to "AGENT.md discovery step 3", which no longer exists.

**Simplifications**

- architecture's teaching protocol repeated Agent Guide's progressive-depth loop. It now
  references that loop and keeps its concept anchor table. The Discussion Triggers list
  duplicated the frontmatter. The extensibility section (30 lines of
  repository-maintenance steps) became one paragraph.
- Scripted questions in all three skills became plain instructions. product-design's
  Status Propagation bullets duplicated the domain-status table beside them.

**Follow-up (spec)**

- `9-Data-Products.md` lists `masking` as a top-level optional field but nests it under
  `governance` in its example. The skills follow the example. The spec should settle on
  one of them.

---

## Agent Governance

File | Before | After
--- | --- | ---
compliance-audit | 531 | 214
regulatory-compliance | 214 | 102
standards-conformance | 164 | 160
**Total** | **909** | **476**

**Bugs**

- GO1: compliance-audit contradicted the spec's inheritance model. It treated an entity
  with no `governance:` block as a gap, required `classification` and `pii` in every
  entity block, and flagged "entity-level classification not declared" as advisory. Under
  `3-Entities.md § Governance Metadata Schema`, blocks hold overrides only and
  inheriting is correct. An audit run as written would have produced false findings on
  every well-modelled domain.
- GO2: compliance-audit rated "PII declared but `pii_fields` empty" as Critical. The spec
  makes `pii_fields` optional, with attribute-level `pii: true` as the default mechanism,
  so the product masking check that read only `pii_fields` could miss PII. Both now
  accept either mechanism.
- GO3: regulatory-compliance presented a parallel governance schema. Extension fields
  (`data_residency`, `audit_all_access`, `breach_notification_required`,
  `notification_timeframe`, `cross_border_transfer`) appeared as if standard. It also
  invented one-off structures (`apra_reporting.arf_320_0`, `aml_relevant`,
  `screening_lists`, `dual_reporting`) instead of the spec's `regulatory_reporting` and
  `compliance_relevance`, which no Governance skill used. The skill now separates the
  spec's core fields from labelled extension fields and routes reports and AML scope
  through the spec fields.
- GO4: regulatory-compliance's domain example wrapped the defaults in `governance:`. The
  spec places them at the top level of the domain metadata.
- GO5: standards-conformance loaded standards from `industry_standards/bian/`, `fhir/r4/`,
  and `tmforum/v4/`. Those raw snapshots are excluded from the PyPI package, so the paths
  don't exist in installed projects. It now uses the shipped guidance under Agent
  Ontology's standards-alignment skill, and treats a name missing from the index as a
  finding.
- GO6: compliance-audit's levels ran 1, 2, 3, 5, then 4 after the report section. The
  description also had a typo ("gulatory").

**Follow-up (spec)**

- The four extension fields used consistently across the regulator files and the audit
  (`data_residency`, `audit_all_access`, `breach_notification_required`,
  `notification_timeframe`) are candidates for `3-Entities.md § Governance Metadata
  Schema`. Until then, they're a documented organisational extension.

---

## Agent Test

File | Before | After
--- | --- | ---
test-strategy | 119 | 121
worked-example-compilation | 169 | 169

Written last session in the current style. All references resolve. Test Strategy's
readiness check now requires `md-ddl lint` to pass, since a worked example with broken YAML
can't be compiled faithfully.

The shared dbt-project skill's paths were made relative to the skill file itself, because
Agent Test loads it from outside Agent Artifact.

## Verification

- `md-ddl init` in a fresh project, then `md-ddl check`: all 50 include directives resolve.
- A script resolved every backticked path in the agents and skills. The only remaining
  unresolved names are placeholders for user-project files (`domain.md`, `LIFECYCLE.md`,
  `sources/sources.md`) and filenames cited in prose next to their folder.
- The faker skill's code pattern ran in both PII modes, with and without a profile.
  `enterprise_profile.py` imported successfully using the documented copy-alongside pattern.
