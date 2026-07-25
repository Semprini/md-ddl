# Standard Complexity & Prescriptiveness Review

**Date:** 2026-07-25
**Review type:** Ad-hoc viewpoint review (per `.prompts/md-ddl-layered-review-process.md`)
**Viewpoint:** "Is MD-DDL a lean information-structuring standard, or has it become a prescriptive methodology?"
**Scope:** `md-ddl-specification/MD-DDL-Complete.md` (Draft 0.9.2, ~3,460 lines, concatenated from sections 1–10)
**Trigger:** Maintainer assessment that the spec is too complex to serve as a "standard" — MD-DDL is meant to be a way of structuring the information users need to capture so AI can consume it and produce consistent artifacts. It is not supposed to be dogmatic or prescriptive.

---

## Executive Summary

The concern is well-founded. The specification currently conflates **four distinct kinds of content**, and only the first is genuinely "the standard":

1. **Structural grammar** — where information lives and what shape it takes: heading hierarchy, two-layer structure, summary tables, YAML vocabularies for entities/enums/relationships/events/sources/transforms/products. This is the standard. It is roughly **30–40% of the current text**.
2. **Style conventions** — exact Mermaid configuration, diagram element ordering, table column sets, file naming patterns, naming casing. Useful defaults, currently written as mandates.
3. **Agent and generation behaviour** — what generating agents do with `mutability`, `existence`, `schema_type`, transformation types; skill-selection tables; validation tool interfaces. This is implementation guidance for the MD-DDL agents, not part of the language.
4. **Organisational methodology** — the adoption maturity model, lifecycle/versioning processes, platform posture, multi-domain governance conflict resolution, drift detection. This tells organisations *how to work*, which is exactly what the maintainer says MD-DDL should not do.

The recommended direction (confirmed with the maintainer) is **core spec + companion guides**: shrink the official standard to the structural grammar plus a small set of clearly-marked default conventions, and relocate categories 2–4 to non-normative companion documents and agent skills. A realistic slimmed core is **~1,200–1,400 lines** across the numbered spec sections — roughly a 60% reduction — with no information lost, only re-homed.

A secondary finding reinforces the case: the spec's size is already exceeding the project's ability to keep it internally consistent (duplicated rules drifting apart, contradictory field definitions — see [Internal Inconsistencies](#internal-inconsistencies-observed-en-route)). A smaller normative core is not just philosophically cleaner; it is more maintainable.

---

## The Test Applied

Each section of the spec was classified using one question:

> **Does this text define how information is structured so an AI can consume it — or does it tell people and organisations how to work?**

Content passing the first clause is core. Content failing it is either a default convention (keep, but soften), guidance (relocate), or rationale (sidebar or remove).

A second, internal test was also applied. Section 1 (Foundation) declares the standard's own philosophy:

> "Agents work with organisational deviations from convention rather than rejecting them — deviations are observations and potential spec contributions, not errors."

Any passage elsewhere in the spec written as a hard mandate ("must", "non-negotiable", "do not use alternatives") that an agent is simultaneously instructed to *tolerate deviations from* is self-contradictory. Either the rule is load-bearing for AI interpretation (keep it normative) or it is a convention (say so). The spec currently does not distinguish, which is the root of the "dogmatic" feel.

---

## Section-by-Section Disposition

Legend: **Core** = stays in the standard as normative grammar. **Convention** = stays, reworded as a non-normative default. **Relocate** = move to a companion guide or agent skill. **Redundant** = merge or delete.

### Section 1 — Foundation (215 lines)

| Content | Disposition | Notes |
| --- | --- | --- |
| Overview, Core Principles | Core | The best statement of what MD-DDL actually is. Principle 7 (incremental adoption) can shrink to one sentence pointing at the Adoption guide. |
| Document Structure, two-layer structure, detail file flexibility | Core | This *is* the standard. |
| "Mirrors Anthropic's skills concept but improves on it by…" | Relocate/remove | Marketing rationale. Dates the document and adds nothing an agent or author needs. |
| Include Directive | Convention | Explicitly "not part of the MD-DDL modelling language itself" by its own admission — candidate for a tooling appendix. |
| Validation Model: the two-tier principle | Core (1 paragraph) | The principle ("syntax is mechanical, everything else is judgment") is genuinely foundational. |
| "Why Not a Traditional Linter", validation level table, pre-flight check scope, tool interface | Relocate | Rationale + tooling spec. The pre-flight tool interface (input/output/exit behaviour/severity/configuration) is an implementer's contract, not modelling grammar. → tooling/validation guide. |

### Section 2 — Domains (557 lines)

| Content | Disposition | Notes |
| --- | --- | --- |
| Domain declaration, description, metadata block, metadata key table | Core | |
| Source Systems table, six summary tables (Entities, Enums, Relationships, Events, Data Products), Rules for Summary Definitions | Core | The router/summary-table shape is the heart of the format. Exact column sets should be worded as the default shape, extensible. |
| Domain Overview Diagram: *that one exists* and edge labels match relationship names | Core | The only structurally load-bearing diagram rules. |
| ELK layout config, `mergeEdges: false`, `nodePlacementStrategy`, theme, PascalCase node ids, "plain anchor tags with no CSS class attributes", "Why the diagram matters" | Relocate | Pure style guide. ~120 lines of the section. → Diagram Style Guide. |
| Conceptual vs Logical diagram distinction | Core (compressed) | The *distinction* matters for interpretation; one short table suffices. |
| Domain Lifecycle: status value list | Convention | The vocabulary (`Draft`/`Review`/`Active`/`Deprecated`/`Retired`) is useful shared vocabulary. |
| Lifecycle transition rules, version-bump rules, breaking-change taxonomy, evolution workflow, `LIFECYCLE.md` convention (~140 lines) | Relocate | This is change-management process, not information structure. → Lifecycle & Versioning Guide. `LIFECYCLE.md`'s file format can travel with it. |

### Section 3 — Entities (550 lines)

| Content | Disposition | Notes |
| --- | --- | --- |
| Entity declaration, description, YAML definition (extends, attributes, constraints), Key-as-Name principle | Core | |
| Attribute properties, type system, arrays and cardinality syntax | Core | |
| Constraint definition | Core | |
| Entity classDiagram: *that one is recommended* showing attributes and immediate relationships | Convention | Currently "must include"; downgrade to recommended. |
| Subject-class rules, reference-class link syntax, enum-class rendering patterns, inheritance arrow direction, ordering-within-the-diagram (6-step ordering list), worked diagram examples (~200 lines) | Relocate | The single most prescriptive stretch of the spec. Ordering of elements *inside a Mermaid block* has zero effect on AI consumption. → Diagram Style Guide. |
| Governance metadata schema + inheritance rules | Core (compressed) | Field vocabulary and the inheritance principle ("domain defaults apply; override only when different") are core. Currently stated here *and* in Domains *and* per-object rules — state once. |
| Entity lifecycle fields (`status`, `since`, `deprecated_at`, `breaking_in`) | Convention | Vocabulary stays; the process rules around them move with the Lifecycle guide. |
| Temporal tracking, Existence, Mutability value lists | Core | Good examples of what the standard *should* be: small vocabularies capturing intent AI can act on. |
| "The generating agent uses this to decide whether to create a candidate dimension or fact…" (generation guidance sentences) | Relocate | → Agent Artifact skill docs. The value lists stay; what the agent does with them moves. |
| Naming rules | Convention | Natural-language naming is a principle (keep); the detailed enforcement wording softens. |

### Section 4 — Enumerations (79 lines)

| Content | Disposition | Notes |
| --- | --- | --- |
| Entire section | Core | Already close to the right size and register. External-standard subset pattern is a good convention. Plural-naming rule → convention. |

### Section 5 — Relationships (146 lines)

| Content | Disposition | Notes |
| --- | --- | --- |
| Declaration, YAML definition (source/type/target/cardinality/granularity/ownership), constraints | Core | |
| Relationship type vocabulary (`owns`, `has`, `references`…) | Convention | Useful shared vocabulary; should be explicitly extensible, not a closed list. |
| Granularity | Core | Small vocabulary, drives generation semantics. |
| Self-referential: declaration + `relationship_attributes` | Core | |
| Self-referential generation guidance (FK column naming, bridge-table decision table, recursive CTE advice) | Relocate | Physical-generation strategy. → Agent Artifact skill docs. |

### Section 6 — Events (145 lines)

| Content | Disposition | Notes |
| --- | --- | --- |
| Entire section | Core, lightly trimmed | Right altitude overall. Rules 1–10 mix grammar (keep) with judgment guidance ("payloads should focus on the delta") which becomes advisory wording. |

### Section 7 — Sources (488 lines)

| Content | Disposition | Notes |
| --- | --- | --- |
| Source concept, folder structure, `source.md` format, metadata, change models, domain feed table, transform file structure, source schema table, idiosyncrasy annotations (`null_as`, `quality`, `format`, `normalise`) | Core | This is genuine structural grammar. |
| "Canonical data products replace Systems of Record" argument (stated three times in this section alone) | Redundant | State once in Foundation principles; reference elsewhere. |
| Complete worked example (~120 lines) | Convention/relocate | Examples are valuable but the spec text and `examples/` both carry them. One compact example inline; full worked examples belong in `examples/`. |
| Source Rules 1–7 | Core (compressed) | Several restate things already said (entity purity, governance inheritance). |
| `data_quality_tier`, change-model → "generated pipeline pattern" column | Split | The fields are core vocabulary; the generated-pipeline-pattern column is agent guidance. |

### Section 8 — Transformations (355 lines)

| Content | Disposition | Notes |
| --- | --- | --- |
| Transformation envelope, the six types (`direct`, `derived`, `reconciliation`, `lookup`, `conditional`, `aggregation`), expression syntax table | Core | The type vocabulary is exactly what an AI needs to generate consistent ETL. Function lists (`trim`, `coalesce`, …; `sum`, `count`, …) should be marked extensible. |
| "What Transformations are not" | Core (compressed) | Genuinely disambiguating; three bullets suffice. |
| Generation Behaviour section | Relocate | → Agent Artifact skill docs. |
| Duplicated structure rules (repeats Section 7's file layout, naming pattern, Destination-column mechanics) | Redundant | Sections 7 and 8 currently share ~80 lines of overlapping content; define structure in 7, types in 8, cross-reference. |

### Section 9 — Data Products (632 lines — the largest section)

| Content | Disposition | Notes |
| --- | --- | --- |
| Product declaration, metadata fields, three classes, lineage structure, logical model requirement, attribute mapping format | Core | The publication contract is core. |
| "Why Data Products Are First-Class" | Relocate/remove | Rationale. |
| Platform Posture (single-platform / polyglot / selective, ~60 lines) | Relocate | Architecture strategy discussion. → Agent Architect architecture skill (`agents/agent-architect/skills/architecture/SKILL.md` territory). The `platform:` metadata block itself can stay as an optional vocabulary. |
| Masking strategies table | Convention | Keep as default vocabulary, extensible. |
| Product-Driven Generation (schema_type → Agent Artifact skill table) | Relocate | Names this repo's specific agents inside the standard — an implementation binding, not language. → Agent Artifact docs. |
| Product Lifecycle: states, transition rules, lifecycle metadata fields, product versioning triggers, product-domain consistency rules (~90 lines) | Relocate | Process. → Lifecycle & Versioning Guide (status vocabulary stays as convention). |
| Multi-Domain Governance Conflict Resolution (~40 lines) | Relocate | "Highest classification wins / longest retention wins" is governance *policy* — sensible, but an organisational decision MD-DDL should offer, not impose. → Governance Patterns guide. |
| Rules 1–11 | Core (compressed) | Roughly half restate content from earlier in the same section. |

### Section 10 — Adoption (341 lines)

| Content | Disposition | Notes |
| --- | --- | --- |
| Entire section | Relocate | The clearest case in the spec. Maturity levels, advancement criteria, regression/staleness rules, baseline file format, journey patterns A–D, coexistence/cutover, drift detection, portfolio adoption — all methodology. → **Adoption Playbook** companion guide. The standard keeps: the `adoption:` and `baseline:` metadata block shapes (so agents can parse them) and one paragraph saying adoption is incremental, see the playbook. |

---

## Prescriptiveness Audit

Quoted examples of mandate-register language that conflicts with the Foundation's own deviations-are-observations philosophy:

- **"This separation is non-negotiable."** (Source Rules, on entity purity.) The principle is sound and arguably *is* core — but "non-negotiable" is the vocabulary of dogma, and it sits in a spec whose validation model says agents must work with files that violate it.
- **"This field name is standardised — do not use alternatives such as `pii_attributes` or `personal_data_fields`."** (`pii_fields`, governance schema.) Meanwhile the Validation Model section uses *exactly this scenario* (`phi` instead of `pii`, `data_class` instead of `classification`) as its example of a deviation agents should note and work with. The spec contradicts itself within the same concern.
- **"No additional checks should be added without a spec version bump."** (Pre-flight scope.) A governance rule about the spec's own change process, embedded in the spec.
- **"Explicitly forbid Customer Id appearing inside a Preference entity YAML."** (Entity Rules.) The no-FK principle is core; the register is dogmatic.
- **"Transform file names… must follow this pattern: `table_<source-table>.md`"** — file naming is a convention; agents resolve links, they don't pattern-match filenames.
- **"The Domain Overview Diagram uses `graph TD`… with the ELK layout engine"**, **"no additional CSS class attributes"**, **"follow this ordering: 1…6"** — rendering preferences stated as spec requirements.
- Mandatory register on diagrams generally: "Every entity detail file **must** include a classDiagram", "The Domain Overview Diagram is **required**." Diagrams aid humans; agents read the YAML. Recommended, not required.

**Recommendation:** adopt an explicit normative-language policy for the slimmed core. Reserve "must" for rules whose violation breaks AI interpretation (syntax, reference integrity, the two-layer discovery contract). Use "by convention"/"by default" for everything else, with an explicit statement that conventions are extensible and deviations are observations. This one editorial rule, applied consistently, resolves most of the "dogmatic" feel even before content moves.

---

## Internal Inconsistencies Observed En Route

Not the review's focus, but these strengthen the case that the spec has outgrown its maintainability — duplicated statements have already drifted:

1. **`identifier` field contradiction.** The attribute property table defines `identifier` values as `primary`, `alternate`, `natural`, `surrogate`; the Entity Rules section says "at least one attribute marked `identifier: true`"; the first entity example uses `identifier: true`, a later example uses `identifier: primary`.
2. **Source Systems table defined twice with different columns.** Once as "Business Application | Platform | Capability Domain", later (Domain Structure) as "Application | Platform | Capability Domain".
3. **Enum plurality rule vs its own examples.** "Enums should be named as a plural — e.g. Customer Types," yet the worked examples throughout use `Loyalty Tier`, `Party Status`, `Country Code` (singular).
4. **Stale path reference.** The Validation Model refers to "structured review prompts in `.github/`"; they live in `.prompts/`.
5. **Governance inheritance stated at least five times** (domain metadata, governance schema, entity rules, relationship rules, event rules, product rules) with slightly different wording each time — a drift risk every future edit compounds.
6. **Sections 7 and 8 overlap** on transform file structure, naming, and Destination-column mechanics (~80 lines of near-duplicate content).

Each duplicate exists because the spec is long enough that authors (human and AI) restate context locally rather than trusting a cross-reference. A smaller core reduces the incentive to duplicate.

---

## Recommended Target Structure

**Slimmed normative core** (stays in `md-ddl-specification/`, estimated ~1,200–1,400 lines total vs ~3,460 today):

```text
md-ddl-specification/
  1-Foundation.md        principles, document structure, two-layer contract,
                         two-tier validation principle (1 paragraph)
  2-Domains.md           declaration, metadata vocabulary, summary tables,
                         "overview diagram exists" requirement only
  3-Entities.md          declaration, attributes, types, constraints,
                         governance vocabulary + inheritance (stated once),
                         temporal/existence/mutability vocabularies
  4-Enumerations.md      as-is (minor register softening)
  5-Relationships.md     declaration, type vocabulary (extensible), granularity,
                         self-referential declaration
  6-Events.md            as-is (minor register softening)
  7-Sources.md           source/transform file structure, metadata, feed tables,
                         idiosyncrasy annotations
  8-Transformations.md   transformation type vocabulary + expression syntax
  9-Data-Products.md     classes, declaration, lineage, logical model,
                         attribute mapping, status vocabulary
  MD-DDL-Complete.md     regenerated concatenation
```

**Non-normative companion guides** (new `guides/` folder, or folded into agent skills where noted):

| Guide | Absorbs | Approx. lines moved |
| --- | --- | --- |
| `guides/adoption-playbook.md` | All of Section 10: maturity model, criteria, journey patterns, baselines detail, drift detection, coexistence | ~320 |
| `guides/diagram-style.md` | ELK configs, subject/reference-class rules, enum rendering, ordering rules, worked diagram examples from Sections 2–3, source overview diagram styling | ~300 |
| `guides/lifecycle-versioning.md` | Domain lifecycle transitions, version-bump rules, breaking-change taxonomy, `LIFECYCLE.md` format, product lifecycle/versioning/consistency rules | ~250 |
| `guides/governance-patterns.md` | Multi-domain conflict resolution, masking strategy discussion, strictness-direction rules | ~80 |
| Agent skill docs (`agents/agent-artifact/…`) | All "Generation Behaviour"/"Generation Guidance" content, schema_type→skill table, pipeline-pattern column, self-referential physical patterns | ~120 |
| Agent Architect skill | Platform posture discussion | ~60 |
| Tooling appendix (location TBD) | Pre-flight check scope + tool interface, Include directive mechanics | ~70 |

Companion guides are referenced from the core with one-line pointers. Agents may still load them — they are guidance for producing *good* models, while the core defines what a *valid* model is.

**Implementation-pass dependencies** (out of scope here, flagged for the roadmap):

- `.prompts/concat-md-ddl-specs.prompt.md` must be updated for the new file set (decide whether `MD-DDL-Complete.md` concatenates core only, or core + guides in a marked non-normative appendix — core-only is recommended, since AI context economy was the original motivation for the complete file).
- Agent `SKILL.md` reference stubs that `{{INCLUDE}}` spec sections will need re-pointing where content moves.
- Section 10's removal renumbers nothing (it is last), but internal cross-references to `10-Adoption.md` exist in Sections 1, 2, 7, 8, 9 and must be redirected to the playbook.
- `examples/` should be checked for reliance on relocated mandates (e.g. diagram ordering) — none of it becomes *invalid*, since conventions remain valid choices.

---

## Prioritised Action List

Ordered by value-to-effort; each item is independently shippable:

1. **Extract Section 10 → `guides/adoption-playbook.md`.** Largest single win, cleanest boundary, no grammar entangled beyond the `adoption:`/`baseline:` metadata shapes (which stay in core).
2. **Extract diagram prescriptions → `guides/diagram-style.md`** and downgrade diagram requirements to recommendations. Removes the most prescriptive material in the spec (~300 lines across Sections 2–3).
3. **Extract lifecycle/versioning process → `guides/lifecycle-versioning.md`**, keeping status/version vocabularies in core.
4. **Apply the normative-language policy** across the remaining core: "must" only where AI interpretation breaks; conventions labelled as conventions; closed lists marked extensible. Fix the audit items quoted above.
5. **De-duplicate**: governance inheritance stated once; Section 7/8 overlap resolved; Systems-of-Record argument stated once; fix the `identifier`, Source Systems table, enum-plurality, and `.github/` inconsistencies.
6. **Relocate generation guidance to agent skills** and platform posture to the architecture skill.
7. **Move validation tool interface + Include directive to a tooling appendix**; regenerate `MD-DDL-Complete.md` and update the concat prompt.

---

## What This Review Cannot Assess

Per the layered-review process, declared blind spots:

- **Whether real adopters experience the spec as too prescriptive.** This review operationalised the maintainer's stated intent; actual user friction data does not exist yet. It is possible some adopters *want* the methodology content inside the standard.
- **Whether companion guides will actually be read.** Relocated content may effectively disappear from agent and human attention if the guides are not wired into agent skill-loading protocols.
- **Whether the ~30–40% core estimate survives implementation.** Some entanglements (e.g. governance vocabulary vs governance policy) may prove harder to separate than a line-count analysis suggests.
- **Impact on generated-artifact consistency.** Some prescriptions dismissed here as "style" (e.g. diagram conventions) may in practice contribute to output consistency across AI sessions. If artifact drift increases after relocation, individual rules may deserve promotion back to core — that is an empirical question this review cannot answer.
- **AI-evaluating-AI limits.** This review was produced by an AI reading an AI-assisted spec; shared blind spots (e.g. tolerance for YAML-heavy formats, underweighting human learnability) apply as described in the review process document.
