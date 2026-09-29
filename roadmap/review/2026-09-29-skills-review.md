# Skills Review — Simplification for Current Models

**Date:** 2026-09-29
**Follows:** [2026-09-29-agent-definitions-review.md](2026-09-29-agent-definitions-review.md), which simplified the core prompts and named the skills as the next step.
**Scope:** Instruction files only: each `SKILL.md` and the guidance files it loads. Reference data is out of scope and unchanged: industry-standard extracts, regulator files, the ODPS schema, dialect notes, the `references/` include stubs, and the Python runtime.

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
**Total** | **3,422** | **2,375**

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
