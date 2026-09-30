# MD-DDL Agent & Standard Effectiveness Report — 2026-09-30 (Layer 3: Stakeholder Simulation)

**Spec version evaluated:** Draft 0.10.0 (`md-ddl-specification/1-Foundation.md:1`)
**Package:** `md-ddl` 0.10.0, installed editable from this working tree
**Agents evaluated:** Guide, Ontology, Artifact, Architect, Governance, **Test** (added to the brief's scope)
**Brief:** `.prompts/md-ddl-evaluation-prompt.md`, run under `.prompts/md-ddl-layered-review-process.md` (Layer 3)
**Owner's question for this layer:** for real adopters, what must be true at v1 for them to adopt MD-DDL and keep using it?

Every finding is labelled one of two ways:

- **Blocks adoption at v1**: a persona following the documented path would reject MD-DDL, or would adopt it and then leave.
- **v1.x friction**: it costs adopters time, but they can work around it and it can ship in a minor release.

---

## How this evaluation was run

**Reading.** I read the brief, the orchestration prompt, `CLAUDE.md`, `README.md` and the three prior reviews. I read all six `AGENT.md` files, `agents/CONVENTIONS.md`, all five Agent Guide skills, and these skills in full:

- Ontology: domain-scoping, entity-modelling, standards-alignment, baseline-capture, schema-import (to line 120)
- Artifact: dbt-project
- Test: test-strategy, worked-example-compilation (Steps 3 to 6)
- Governance: compliance-audit (Level 4 onwards), regulatory-compliance (to line 60), `regulators/hipaa.md`

The remaining skills I read by outline and targeted grep: domain-review, lifecycle, source-mapping, product-design, odps-alignment, normalized, dimensional, knowledge-graph, reconciliation, and the three dialect files.

For the spec, I read `1-Foundation.md` and targeted sections of §5, §7, §8 and §9. For examples, I read Simple Customer in full, plus Financial Crime `table_account.md`, the Healthcare domain header and Brownfield Retail's domain and baselines.

**Hands-on first-run path**, in scratch venvs under the session scratchpad:

1. `pip install -e /home/user/md-ddl`, then `md-ddl init` in an empty directory. I read what landed: `.md-ddl/`, `CLAUDE.md`, `.github/copilot-instructions.md` and the wrappers.
2. `md-ddl lint .` on the empty project, then again after copying Financial Crime and Simple Customer under `domains/`.
3. A newcomer's first hand-written `Claims` domain with three deliberate mistakes, in **the layout that `md-ddl init` writes into `CLAUDE.md`**. Then the same model in the domain-rooted layout.
4. `md-ddl init` into a git repo that already has a `CLAUDE.md`, then a re-init.
5. Mutation tests on a Financial Crime transform `target` (separator and typo variants).
6. **Agent Test's local tier.** I installed `dbt-core` 1.12.5 and `dbt-duckdb` 1.11.0 (DuckDB 1.5.6) and built a minimal project using the dbt-project skill's `profiles.yml`. I then ran a worked-example-style `unit_tests` block, and the skill's current-time macro-override pattern, against plain DuckDB.

No agent was executed. Agent behaviour below is predicted from the prompts, the same limitation Layers 1 and 2 declared.

**Brief deviations, noted rather than followed:**

- The brief says "Draft 0.9.0", "five agents" and "write to `review.md`" (Layer 1 S3/S4). I used the dated path and 0.10.0, and added scenarios T1–T3 and X6 for Agent Test.
- The brief's G4 asks whether setup matches "the submodule pattern". The primary path is now PyPI, so I evaluated both.
- The brief's scenario A2 names `products/analytics.md`, which is correct. Its "Comparison with Previous Evaluation" section references `review.md`, so I compared against `roadmap/review/2026-03-13-layer3-review.md` instead.

---

## What This Evaluation Cannot Assess

- **Real stakeholder reactions.** The ten personas are simulated by pattern-matching. Whether Sarah would really push back on a given point, or Priya would accept the report format, is unknown. The verdicts below are informed opinions.
- **Runtime agent behaviour.** I predicted skill loading and outputs from prompt text. Models often recover from prompt defects: they search for missing files, or ignore a stale rule. My scores may understate that recovery. They may also overstate it, since long prompts get partially ignored.
- **VS Code Copilot behaviour.** I could not test whether Copilot custom agents expand `{{INCLUDE: …}}`. For the VS Code personas (Alex, James) that is the main open risk (see B8).
- **DuckLake.** The DuckDB `ducklake` extension download failed from this sandbox (HTTP 403 via the proxy). I verified the dbt unit-test mechanics on plain DuckDB but **not** the skill's DuckLake `attach` syntax.
- **Regulatory correctness.** I cannot say whether the APRA, RBNZ, FATF or HIPAA content is right. My comments on regulator files cover currency and structure only.
- **Domain accuracy.** I cannot say whether the Claims, AML, FHIR or TM Forum modelling advice matches practice. ACORD in particular is membership-gated, and the skill says so.
- **Learning-curve reality.** I cannot measure how long a real analyst takes to become productive. My learnability scores rest on file size, concept count and the friction I hit myself.
- **Scale.** I did not run a 100+ entity domain or a 200-table import.
- **AI-evaluating-AI bias.** I am an AI reviewing a largely AI-authored corpus, after reading two AI reviews. Anchoring on their findings is likely, and I have tried to add only what they did not cover. YAML-heavy notation probably looks more approachable to me than it will to Marcus or Priya.

---

## Executive Summary

MD-DDL at 0.10.0 is a coherent, unusually well-bounded agent suite on top of a spec that is expressive but still settling.

- **Strongest.** Boundary discipline and honesty rules are the most consistent strength. Every agent has a Boundaries table, a Limits section and "don't invent" rules, and these hold up across all 39 scenarios. The individual skills are strongest where they meet a named persona's exact situation: Standards Alignment's decomposition protocol, Regulatory Compliance's AU/NZ file map, Normalized's inheritance templates, and Agent Test's worked-example-to-unit-test compilation, whose dbt pattern I ran and which works.
- **Weakest.** The weakest area is the **first hour and the first month**:
  - The layout `md-ddl init` tells a project to use makes the linter skip entity files silently.
  - The starter and flagship examples break the spec's own rules.
  - No example shows any generated output or test run.
  - A team has no way to pin which MD-DDL version its agents run.
- **Cross-agent workflows** average 2.7/5. The 0.10 source-layer features are not implemented downstream (Layer 2 L2-19). As a result, source-to-product-to-test chains break exactly where the new features are used.
- **Top priority.** Make the documented path and the linted path the same, then ship one example whose generated DDL, dbt project and passing test run are committed. Everything else in the adoption-blocker list is secondary to "a newcomer's first model gets a true lint result, and an engineer can see real output before investing".

**Overall directional scores:**

- Agent effectiveness: **3.6/5** (March 2026 Layer 3: 4.2)
- Cross-agent workflows: **2.7/5** (March: 3.3)
- Standard: **3.3/5** (March: 3.7)

The drop is partly method, not only regression. This run included hands-on execution and applied the anti-sycophancy rule, while the March run averaged above 4.

---

## Cross-reference to Layers 1–2 and the readiness review

Layers 1–2 and the readiness review identified the issues below. Each row shows which stakeholder scenarios it affects and how.

Prior finding | Scenarios affected | Effect on the persona
--- | --- | ---
L1 S7 (four layouts), V1-04 (linter is folder-coupled) | G4, X5, O1, O7, O8 | **Confirmed and made worse** (B1). The layout in the generated `CLAUDE.md` loses all entity checks, not only source checks.
L1 S6 (false "generated artifacts" claim) | G2, A1–A6, X1, X6 | James, looking for proof, finds none (B3).
L1 S9 (regulator files 18 months stale) | R1, R2, R4, X2 | Priya's first audit opens with a staleness warning on every file except AUSTRAC (B7).
L1 S12 (dead `review-md-ddl` route) | G6, O5 | Kenji or Alex is routed to an agent that isn't installed. Low impact: Ontology Domain Review covers the need.
L2-03 (no cardinality optionality) | A1, A3, A5, X1 | Every generated FK's nullability is a guess (B5).
L2-04 (masking may name nonexistent attributes) | A2, D2, D3, R2, X1 | The flagship consumer product "masks" attributes it doesn't have and publishes names in clear. Neither Governance nor Architect would catch it. This is the worst single trust failure for Marcus and Priya (B4).
L2-05 (no precision/scale/length) | A1, A2, A5, T2 | James sees `NUMBER(38,0)` or `NUMERIC(18,2)` for 4-decimal money and rejects the output (B5).
L2-08, L2-16 (cross-domain conflicts and refs) | D4, X1 | Aisha's Customer 360 is expressible only through product lineage. Relationships and `extends` can't cross domains. See the disagreement section on whether this blocks v1.
L2-18 (handoff file naming) | X1–X6 | Minor in practice. The primary handoff is the inline block the user pastes. See the disagreement section.
L2-19 (0.10 semantics missing from Artifact and Test) | A2, T1, T2, X3, X6 | Tomás's contributing tables compile to empty expectations, and James's dbt canonical model unions rows it should merge.
L2-20 (identifier rule vs inherited keys) | O5, T1, G2 | Kenji's review and Agent Test's readiness gate both mark Financial Crime subtypes Not Ready. The **Simple Customer starter** has the same pattern (N6).
V1-01 (no versioning policy) | O6, D5, all "stay" questions | Adopters can't tell what an upgrade will break (B6, with N4).
V1-03 (untested linter) | X5, G4 | Covered by readiness; my mutation tests add the `.` separator hole (N2).
V1-05, V1-06 (unsoaked features; non-conforming examples) | G2, O4, R4, X3 | Healthcare, the FHIR persona's reference example, uses the pre-0.10 source layout.
V1-07 (CC BY on code) | All enterprise personas | This gate comes before any scenario runs (B2).
Readiness S-12 (`{{INCLUDE}}` unverified on Copilot) | G4, X5, every VS Code persona | Alex uses VS Code. If Copilot doesn't expand the include, Alex's first session is a generic assistant (B8).

---

## New findings from this layer

These are not in Layers 1–2 or the readiness review. Each was reproduced in the scratchpad unless marked as read-only.

### N1 — The layout `md-ddl init` writes silently disables entity linting (Blocks adoption)

`md-ddl init` writes the following into the generated `CLAUDE.md` and `.github/copilot-instructions.md` ("Project layout"):

```
domains/           Domain files (one per business domain)
entities/          Entity detail files
```

Layer 1 S7 noted that this disagrees with the spec. What had not been tested is the result. I wrote `domains/claims/domain.md` and `entities/claim.md` in exactly that layout, with three mistakes:

- `extends: Polcy` (a typo)
- an undeclared enum `Claim Status`
- a YAML attribute `Approved` missing from the diagram

`md-ddl lint .` reported only the domain file's problems. None of the three entity errors appeared. `md-ddl lint entities/claim.md` exits 2 with "no domain.md found above". Moving the same files to `claims/entities/` surfaced all three as errors (`entity-references`, `entity-enum-in-diagram`, `entity-attribute-consistency`).

Agents read `CLAUDE.md` as project instructions, so Agent Ontology will plausibly write files where it says. The newcomer then gets a **green lint on a model with broken references, produced by following the tool's own setup output**. This is the readiness review's "worst failure mode for a conformance tool", reached by a more common path than the README layout it tested.

### N2 — An ASCII `.` in a transform `target` silently switches off target checking (v1.x friction; fix cheaply before v1)

The spec's target notation is `Entity · Attribute`, using U+00B7 MIDDLE DOT (`8-Transformations.md:52`). Most keyboards can't type it. The Source Schema `Destination` column in the same files uses an ASCII `.` (`Party.Party Identifier`, `table_account.md`).

I changed `target: Party · Party Status` to `target: Party.Party Stauts` (ASCII dot and a typo), and separately to `Party - Party Status`. Both lint clean (exit 0). Only the `·`/`•` form is parsed (`lint.py:1161`, `TARGET_SEP_RE`).

`·` is also overloaded. `Party · Company` means Parent · Subtype, while `Party · Party Identifier` means Entity · Attribute. Tomás will type `.` on day one and lose the check the Ontology prompt calls "this layer's most common defect" (`agent-ontology/AGENT.md:92-96`).

Fix: accept `.` (and ` - `) as equivalent separators, or warn on any `target` the linter can't parse.

### N3 — No example shows what MD-DDL produces (Blocks adoption for the engineer persona)

No example contains generated output: DDL, JSON Schema, Cypher, a dbt project, test results or an ODPS manifest. There is `factories.py` for Faker, but that's all. The `Financial Crime/generated/` directory is gitignored, and Layer 1 S6 flagged the README claim.

James's first question is "show me the output". Answering it today needs a full Agent Artifact session against a flagship that Layer 2 shows has semantic defects.

A committed reference output also serves as the regression baseline. Generation is done by an LLM, and the rule "naming is deterministic" (`agent-artifact/AGENT.md`) is an instruction, not a guarantee. Without a golden output, nobody, including the maintainer, can see when an agent or skill edit changes what is generated.

### N4 — A team can't pin which MD-DDL its agents run (Blocks staying)

- `md-ddl init` writes `.md-ddl/.gitignore` containing `*`, so the standard is not committed.
- No file in the project records the installed version. I grepped the committed wrappers, `CLAUDE.md` and `.md-ddlignore`: no `0.10.0` anywhere.
- A teammate who clones the repo gets `.claude/commands/*.md` that point at a `.md-ddl/` that doesn't exist until they run `pip install md-ddl && md-ddl init`, and pip installs whatever is latest.
- Two modellers can therefore run different spec versions and different agent prompts against the same domain.

V1-01 proposes a per-model `md_ddl:` target key. That covers models, but not the tooling. The fix is to write the installed version into a committed file (e.g. `.md-ddl-version`, or a line in `.md-ddlignore`), and have `md-ddl check` and `lint` warn on mismatch. The README should also recommend pinning `md-ddl==x.y.z` in the project's requirements.

### N5 — An existing `CLAUDE.md` is skipped without guidance (v1.x friction)

Claude Code users usually already have a `CLAUDE.md`. `md-ddl init` prints `CLAUDE.md (exists, skipped)` and nothing else. The agent table, the lint instructions and the auto-routing text never reach the project. The slash commands still work, but the routing ("which agent do I use?") that `CLAUDE.md` provides in this repo is lost.

Fix: print the block to paste, or write `CLAUDE.md.md-ddl` beside the existing file.

### N6 — The starter example teaches two defects (Blocks adoption: examples are copied)

`examples/Simple Customer/details.md` is the "first look" example (worked-examples skill).

- **Two primary identifiers.** `Customer extends Party Role` and declares `Customer Id` as `identifier: primary` (line 91-93), while Party Role already declares `Role Identifier` as primary (lines 40-42). This is the L2-20 pattern that Financial Crime 2.0.0 fixed as a *breaking* defect (`LIFECYCLE.md:48`). It survives in the starter.
- **Links to the upstream repo.** Every diagram link is an absolute `https://github.com/Semprini/md-ddl/blob/main/examples/Simple%20Customer/...` URL (lines 29, 79-80, 143; `domain.md` overview). A newcomer who copies the starter as a template gets diagrams that link to the MD-DDL repository, not their own files.
- **Two attribute shapes.** The event's `attributes:` is a list of single-key maps (`- event timestamp:`, line 242), while entity attributes are maps. Alex has to learn both.

### N7 — The local test tier needs a network download that the skill doesn't mention (v1.x friction)

The dbt-project skill's local profile uses `extensions: [ducklake]` (`dbt-project/SKILL.md:149`). DuckDB fetches the extension at runtime from `extensions.duckdb.org`. From this sandbox that failed with HTTP 403, and a bank behind an egress proxy (the PyPI-via-artifactory audience the README targets) will hit the same wall.

The skill gives no offline install route and no plain-DuckDB fallback.

The rest of the design works. With `path: local.duckdb`, a worked-example `unit_tests` block (`given` source rows verbatim, `expect` canonical rows) and the `overrides: macros: current_ts:` pattern from `worked-example-compilation/SKILL.md:82-84` both **passed on dbt-core 1.12.5 / dbt-duckdb 1.11.0**. The worked-example-as-contract idea is sound in practice, not only on paper.

Minor: the default view materialisation emits "Constraint types are not supported for view materializations" when contracts carry `not_null`. The skill could say to materialise contracted models as tables in the local tier.

### N8 — Brownfield at real scale has no operating guidance (v1.x friction; high value)

- **No batching guidance.** Schema Import and Baseline Capture have no guidance on batching, splitting by schema, or session boundaries (grep for batch/chunk/large/at a time returns nothing). Rachel's scenario is 45 tables (O7) or 200+ tables across 8 systems (G5), and a single chat can't hold that. She needs "one schema per session, baselines first, then import per subject area, handoff file between sessions".
- **A stalled example.** The Brownfield Retail example's `adoption.target_date: 2025-06-30` has passed while it sits at `mapped`. By Agent Guide's own rule (`adoption-planning/SKILL.md`, "Stalled adoption") the example is stalled.
- **The journey stops at Level 2.** The example only reaches Level 2. Levels 3 (Governed) and 4 (Declarative, with regenerate-and-reconcile) exist only as prose in `worked-examples/SKILL.md`, so Rachel can't see what "done" looks like at the levels she is being sold.

### N9 — Diagram/YAML double entry is a permanent maintenance cost (v1.x friction)

Tier 1 makes the classDiagram and the YAML agree (`entity-attribute-consistency`, `entity-enum-in-diagram` are errors). Every attribute is therefore written twice, and every rename or retype is two edits. For agent-authored models that's cheap. For Sarah and Kenji, who hand-edit in review, it is the edit they'll resent most by month three.

Tooling that renders or fixes the diagram from the YAML (`md-ddl lint --fix`, or `md-ddl render`) would turn an error class into a no-op. It's additive and can ship in 1.x.

### N10 — FHIR polymorphic references and choice types have no guidance (v1.x friction)

- `Observation.subject: Reference(Patient | Group | Device | Location)` and `value[x]` are everyday FHIR.
- §5 relationships have one `target`. Neither the spec nor `standards/fhir/README.md` nor `entity-modelling/guidance.md` mentions polymorphic targets or choice types (grep: nothing).
- Dr. Kowalski's stated pain point ("will push back if MD-DDL can't express FHIR's polymorphic reference types") is unanswered. Workarounds exist (an abstract parent, or one relationship per target), but nothing teaches them.

### N11 — Agent Guide has no archetype for Alex (v1.x friction)

The Guide's archetype table (`agent-guide/AGENT.md:89-99`) has no junior analyst or SQL user. Alex maps to "Data Engineer", whose explanation ("logical-to-physical translation … dbt") assumes more than Alex has. Neither Orientation nor Concept Explorer has a canned answer to G1's literal question, "how is this different from CREATE TABLE?".

---

## Agent Scorecards

Scores are directional. A 5 cites its evidence. The Avg column is the row mean.

### Agent Guide

| Scenario | Skill Loading | Behaviour Mode | Output Quality | Boundary Respect | Persona Fit | Avg |
| --- | --- | --- | --- | --- | --- | --- |
| G1 — What is MD-DDL | 4 | 4 | 3 | 4 | 3 | 3.6 |
| G2 — Walkthrough | 4 | 4 | 3 | 4 | 3 | 3.6 |
| G3 — Entity vs enum | 4 | 4 | 4 | 4 | 4 | 4.0 |
| G4 — Platform setup | 4 | 3 | 2 | 4 | 3 | 3.2 |
| G5 — Adoption planning | 4 | 4 | 3 | 4 | 3 | 3.6 |
| G6 — Agent navigation | 3 | 4 | 3 | 4 | 3 | 3.4 |
| **Average** | 3.8 | 3.8 | 3.0 | 4.0 | 3.2 | **3.6** |

- **G1.** Orientation triggers cleanly and its "two-sentence answer, then depth" rule suits Alex. Output is 3 because there's no analyst archetype and no stock "vs CREATE TABLE" framing (N11).
- **G2.** The skill correctly steers to Simple Customer first, and says to read the files rather than recall them. But the files it reads teach the N6 defects. The Financial Crime walkthrough presents L2-10 (Payer/Payee collapse without dedup) and L2-04 (dangling masking) as correct practice. The skill's own step 3 note ("The file doesn't state why it's dependent. Ask the user") is good teaching.
- **G3.** The entity/enum/attribute table in entity-modelling, relayed by Concept Explorer, answers "in SQL I'd make a lookup table" well: "Nobody will ask 'tell me everything about this value'".
- **G4.** This is the weakest Guide scenario. Platform Setup matches the README, but:
  - it never says where model files go, or that `md-ddl lint .` exits 2 on an empty project;
  - it doesn't warn that an existing `CLAUDE.md` is skipped (N5);
  - it doesn't mention version pinning (N4);
  - it can't confirm Copilot include expansion (B8).
  Its troubleshooting table is good, and "Got a demonstration instead of production files" is a sharp line.
- **G5.** The signal-to-pattern table and "one well-understood domain first" are sound. There's no scale guidance for 200 tables (N8), and the example it points to is itself stalled.
- **G6.** The Agent Directory and seven-step workflow are clear, and offering to draft the opening request is excellent practice. Six agents is a lot for Alex. The directory still lists the uninstalled `review-md-ddl` (L1 S12).

**Strengths.** Calibration rules: skip profiling for returning users; stop when they have what they need. "Demonstrate, don't produce" is enforced by a rule and by the troubleshooting table.

**Gaps.** No junior archetype. Setup stops at "commands appear" rather than "your first domain lints". No mention of team setup.

**Persona feedback (Alex):** "It explained things at my level once I told it I use SQL, and the example was small. But I made the folders its instructions told me to, the linter said 'no findings', and later it turned out half my files were never checked."

**Persona feedback (Rachel):** "The maturity ladder makes sense, and 'pick one domain' is what I'd do anyway. It didn't tell me how to feed 200 tables through a chat, and the example it showed me never got past Level 2."

### Agent Ontology

| Scenario | Skill Loading | Behaviour Mode | Output Quality | Boundary Respect | Persona Fit | Avg |
| --- | --- | --- | --- | --- | --- | --- |
| O1 — New Claims domain | 4 | 4 | 3 | 4 | 4 | 3.8 |
| O2 — Entity/enum/attribute | 4 | 4 | 4 | 4 | 4 | 4.0 |
| O3 — BIAN / ISO 20022 alignment | 5 | 4 | 4 | 4 | 4 | 4.2 |
| O4 — Healthcare FHIR | 4 | 4 | 3 | 4 | 3 | 3.6 |
| O5 — Domain review of Financial Crime | 4 | 4 | 2 | 4 | 3 | 3.4 |
| O6 — Model evolution (Reinsurance) | 4 | 4 | 3 | 4 | 3 | 3.6 |
| O7 — Baseline capture, 45 tables | 4 | 4 | 3 | 4 | 3 | 3.6 |
| O8 — Schema import | 4 | 4 | 3 | 4 | 4 | 3.8 |
| **Average** | 4.1 | 4.0 | 3.1 | 4.0 | 3.5 | **3.75** |

- **O1.** Interview mode is explicit ("On first contact, don't write MD-DDL yet … two or three focused questions per turn"). Domain Scoping's five interview areas cover purpose, boundaries, governance and standards. The Purpose step turns consumer needs into modelling constraints, which Sarah will respect.
  - Inheritance for internal and external adjusters is handled by "Roles are not subtypes": an adjuster who is an employee *or* a contractor is a role question, and the skill pushes the right discussion.
  - Output is 3 because the files will land in the N1 layout, and ACORD is membership-gated. The skill honestly says "state your confidence".
- **O2.** The four inheritance questions ("Do subtypes add meaningful attributes … roughly three or more") map directly onto "Motor needs registration, Property needs address". The skill would recommend `extends:` with trade-offs. This is solid, but it doesn't reach 5 because the spec has no discriminator-driven required-field construct: required-per-subtype is expressible only through subtype `not_null` constraints.
- **O3 (Skill Loading 5).** Evidence: the skill's trigger names BIAN and ISO 20022. Its "When Decompositions Differ" protocol (compare, evaluate, resolve four ways, record) is exactly Marcus's problem (Customer / Account Holder / Beneficial Owner vs BIAN Party). The worked example shows 6 of 10 plausible-looking BIAN citations failing the local index, which models the honesty it asks for. Behaviour is 4 rather than 5 because nothing forces staying in Interview mode for a single-concept question. The shortcut rule could rush Marcus.
- **O4.** ValueSet-to-enum and resource-to-entity are covered, and `standards/fhir/` is substantial. There is no guidance on polymorphic references or choice types (N10). The Healthcare example uses the pre-0.10 source layout (V1-06). Persona Fit is 3: Dr. Kowalski will ask "what does this add over FHIR?", and the answer (governance, temporal, generation) is in Orientation, not Ontology.
- **O5 (Output 2).** The review protocol (Pre-Flight → Inventory → Structural → Decision Quality → Standards → Regulatory → Source) is the systematic checklist Kenji wants. But on the flagship it would:
  - (a) mark Customer, Payer, Payee, Merchant and Teller Not Ready for lacking their own primary key (L2-20);
  - (b) not catch the masking and Rule 8 defects Layer 2 found (L2-04, L2-10);
  - (c) pass the unsourced-attribute problem (L2-23).
  Kenji's complaint is "approved with hidden quality issues", and this gate reproduces that complaint.
- **O6.** The brownfield path ("Draft only the change") and the Lifecycle skill's version-bump flow fit. Output is 3 because "breaking" is self-contradictory (L2-17), and the owning domain can't list external consumers (L2-16). Sarah's "without breaking what's published" can't be answered from the model.
- **O7.** "Never present a blank YAML template" and "does NOT create canonical entity files" are good boundaries. There is no batching for 45 tables (N8).
- **O8.** The inference table is clear and honest about confidence ("Medium-High" for FK to relationship) and enforces "no FK attributes". The export commands for Snowflake, Postgres, SQL Server and Databricks are practical. Scale is again unaddressed.

**Strengths.** An interview-first posture with a real single-concept shortcut. Standards honesty. Brownfield delta discipline.

**Gaps.** Review can't see cross-file semantic defects. The primary-identifier rule conflicts with inheritance. There's no scale guidance.

**Persona feedback (Sarah):** "It argues like a modeller, and I like that it asks before drafting. I'll push back on having to write every attribute twice, in the diagram and the YAML."

**Persona feedback (Marcus):** "The side-by-side reconciliation with BIAN is exactly the conversation I'd have with an architect."

**Persona feedback (Dr. Kowalski):** "Fine for Patient and Encounter. The moment I model `Observation.subject` it has nothing to say."

**Persona feedback (Kenji):** "Good checklist. But it would fail the reference example for the wrong reason and pass it on the things that matter."

**Persona feedback (Rachel):** "Import is the right primary path. Tell me how to run it 20 tables at a time."

### Agent Artifact

| Scenario | Skill Loading | Behaviour Mode | Output Quality | Boundary Respect | Persona Fit | Avg |
| --- | --- | --- | --- | --- | --- | --- |
| A1 — Dimensional, Snowflake | 4 | 4 | 3 | 4 | 3 | 3.6 |
| A2 — Product-scoped wide-column, Databricks | 4 | 4 | 2 | 4 | 3 | 3.4 |
| A3 — Class-table inheritance DDL | 5 | 4 | 4 | 4 | 4 | 4.2 |
| A4 — Knowledge graph (Neo4j) | 4 | 4 | 3 | 4 | 3 | 3.6 |
| A5 — JSON Schema contracts | 3 | 4 | 2 | 4 | 3 | 3.2 |
| A6 — Reconciliation | 4 | 4 | 3 | 4 | 3 | 3.6 |
| **Average** | 4.0 | 4.0 | 2.8 | 4.0 | 3.2 | **3.6** |

- **A1.** Assess mode is explicit (a five-item confirm list). The Snowflake dialect covers VARIANT and clustering. Money precision (L2-05) and FK nullability (L2-03) are exactly what James checks first.
- **A2 (Output 2).** Scoping by product and honouring `schema_type` are well specified ("Consumer-aligned: the product's logical model … are the input"). But the input is Transaction Risk Summary, which:
  - masks attributes it doesn't have (L2-04);
  - maps canonical attributes no source populates (L2-23);
  - traverses a path that multiplies the grain (L2-13).
  A faithful generator produces a table with clear-text PII and fan-out rows. The dialect file has TBLPROPERTIES, Change Data Feed and Unity Catalog.
- **A3 (Skill Loading 5).** Evidence: `normalized/SKILL.md` has an Inheritance Strategy Decision Table, three DDL patterns including "Pattern 2 — Class-Table Inheritance (Parent + Child)", and a null-bloat heuristic ("switch to class-table" above ~30%). This is Sarah's exact request, pre-answered.
- **A4.** Nodes, multi-label inheritance, uniqueness constraints and enum seed data are covered. Output is 3 because relationship properties inherit L2-M1 (untyped `relationship_attributes`), and unsourced relationships (L2-01) have no data path.
- **A5 (Output 2).** JSON Schema is a 4-line bullet inside the Normalized skill (`normalized/SKILL.md:253-256`). It has no draft version, no `$ref` convention, no type mapping table and no nullability rule. This is a real skill gap for an output the README advertises.
- **A6.** The reconciliation skill correlates diffs with `LIFECYCLE.md` to separate intended change from "regeneration noise". That's a thoughtful idea, and the need for it is itself evidence of N3: there is no deterministic generator.

**Strengths.** The readiness gate before generating. "YAML is authoritative". Deterministic-naming intent. A mapping summary with every generation.

**Gaps.** Lossless types. JSON Schema depth. No reference output to compare against.

**Persona feedback (James):** "The skills know Snowflake and Databricks. I still can't see a single generated table before committing my team, and the reference product would hand me unmasked names."

**Persona feedback (Sarah):** "The inheritance patterns are what I'd draw myself."

### Agent Architect

| Scenario | Skill Loading | Behaviour Mode | Output Quality | Boundary Respect | Persona Fit | Avg |
| --- | --- | --- | --- | --- | --- | --- |
| D1 — Three-consumer design | 4 | 4 | 3 | 4 | 4 | 3.8 |
| D2 — PII masking | 4 | 4 | 4 | 4 | 4 | 4.0 |
| D3 — ODPS manifest | 4 | 4 | 3 | 4 | 4 | 3.8 |
| D4 — Cross-domain Customer 360 | 4 | 3 | 2 | 4 | 3 | 3.2 |
| D5 — Product versioning | 4 | 4 | 3 | 4 | 3 | 3.6 |
| **Average** | 4.0 | 3.8 | 3.0 | 4.0 | 3.6 | **3.7** |

- **D1.** Product Design's 11 steps (inventory → platform posture → consumers → class → lineage → schema type …) are what Aisha wants. Output is 3 because "consumer products source only from canonical products" can't be checked: lineage can't name a product (L2-09).
- **D2.** The spec's strategies (`year-only`, `hash`, `redact`, `truncate`; `9-Data-Products.md:362-373`) cover the ask, and "Masking is product-scoped" is stated as a rule. It doesn't reach 5 because nothing validates that a masked attribute exists (L2-04).
- **D3.** The inference rules (`not_null` → completeness, etc.) and a "Requires Business Input" gap list are the right shape. Output is 3 because the source product is defective, and ODPS v4.0 conformance is asserted but not checked (no schema validation step).
- **D4.** Governance conflict detection compares domain defaults only, and the flagship's scope union is wrong (L2-08). Relationships can't cross domains (L2-16). Aisha can declare the product, but the model can't express how the three domains connect.
- **D5.** The lifecycle states, `deprecated_date`, `successor` and `migration_note` exist, and Product Lifecycle Mode is in the skill. The breaking/non-breaking definition is contradictory (L2-17), and there's no consumer registry to notify.

**Persona feedback (Aisha):** "The design process is better than most data-mesh playbooks I've read. The cross-domain product is where it goes vague."

**Persona feedback (Marcus):** "The masking advice is right. I'd assumed the tool would stop me masking a column that isn't there."

### Agent Governance

| Scenario | Skill Loading | Behaviour Mode | Output Quality | Boundary Respect | Persona Fit | Avg |
| --- | --- | --- | --- | --- | --- | --- |
| R1 — APRA / RBNZ / FATF audit | 5 | 4 | 3 | 4 | 4 | 4.0 |
| R2 — Product governance review | 4 | 4 | 2 | 4 | 3 | 3.4 |
| R3 — Remediation (data residency) | 4 | 4 | 4 | 5 | 4 | 4.2 |
| R4 — HIPAA | 4 | 4 | 3 | 4 | 3 | 3.6 |
| **Average** | 4.25 | 4.0 | 3.0 | 4.25 | 3.5 | **3.8** |

- **R1 (Skill Loading 5).** Evidence: `regulatory-compliance/SKILL.md` has a row for "NZ banking (incl. NZ subsidiaries of Australian banks) | `rbnz.md`, `basel.md`, `fatf.md`, plus `apra.md` for the parent". That is Priya's organisation verbatim. The Critical/Advisory/Not-assessed severities and the "not legal advice" banner fit her.
  - Output is 3 for two reasons. Every file but AUSTRAC triggers the >12-month staleness warning (L1 S9). And the conflict default is stated three ways (L2-07: "apply the more conservative", "don't apply either side", and a "Default applied" column).
  - Priya asked for Critical/High/Medium/Advisory. The skill offers Critical/Advisory. That's a vocabulary gap she'll notice.
- **R2 (Output 2).** The Level 4 checks are well chosen ("Source-aligned raw feeds | Raw PII without restricted consumers …"). They don't detect masking entries that resolve to nothing (L2-04) or entity-level classification conflicts (L2-08). On the flagship, the audit would report a masked product as masked.
- **R3 (Boundary Respect 5).** Evidence: the Remediation scope rule lists exactly what Governance may edit ("domain-level `governance:` … entity `governance:` blocks … `retention_basis` … Nothing else"). It requires before/after YAML diffs, one at a time with confirmation, and gives a structural-change handoff to Ontology. `data_residency` is in the schema.
- **R4.** `hipaa.md` exists with Safe Harbor identifier-to-masking guidance, which the brief's question expected might be missing. Gaps:
  - There is no `deidentification_method` field, and "Don't invent further fields" forbids adding one. The method used can live only in prose.
  - The PHI-vs-PII synonym isn't mapped (Layer 2 Validation philosophy).
  - `hipaa.md` is stale.

**Persona feedback (Priya):** "It found the right regulator files for a bank with an NZ sub, which I didn't expect. Then it told me every file was 18 months old."

**Persona feedback (Dr. Kowalski):** "Safe Harbor is there. I can't record which de-identification method we used."

**Persona feedback (Marcus):** "It trusts the product's masking list more than I would."

### Agent Test (added to scope)

Scenarios written for this layer:

- **T1 — Coverage report (Kenji / James).** "What can we test for the Canonical Party product, and what's missing?"
- **T2 — Compile and run locally (James).** "Turn the Account worked examples into dbt unit tests and run them on my laptop."
- **T3 — Failure triage (James).** "This unit test fails. Whose problem is it?"

| Scenario | Skill Loading | Behaviour Mode | Output Quality | Boundary Respect | Persona Fit | Avg |
| --- | --- | --- | --- | --- | --- | --- |
| T1 — Coverage report | 4 | 4 | 2 | 5 | 4 | 3.8 |
| T2 — Compile and run locally | 4 | 4 | 3 | 4 | 3 | 3.6 |
| T3 — Failure triage | 4 | 4 | 4 | 5 | 4 | 4.2 |
| **Average** | 4.0 | 4.0 | 3.0 | 4.7 | 3.7 | **3.9** |

- **T1 (Boundary 5).** Evidence:
  - an explicit Failure → Owner table (`agent-test/AGENT.md:67-71`);
  - "Never weaken, drop, or edit an assertion to make a test pass";
  - `derived` tests labelled as unable to catch wrong YAML;
  - drafted examples are "proposals" until the domain accepts them.
  These are the best-drawn boundaries in the suite. Output is 2 because on the flagship, Step 1 readiness trips on L2-20 and the Step 1 subtype check trips on the SAP fan-in (L2-19). The five contributing tables would compile to empty expectations (L2-19).
- **T2.** I verified the compilation pattern, the `unit_tests` shape and the macro override on dbt-core 1.12.5 + DuckDB (N7). What James can't do:
  - start without a template project and an Agent Artifact–generated dbt project (no reference project exists; N3);
  - reach DuckLake from behind a proxy (N7);
  - get a "first test in 10 minutes" path.
- **T3.** Triage by owner, with expected-vs-actual diffs and `meta.md_ddl` tracing back to the heading anchor, is precise and actionable.

**Persona feedback (James):** "This is the agent that would make me trust the rest. The worked-example-as-unit-test idea works, and I ran it. Give me one example repo where it's already green."

---

## Cross-Agent Workflow Scorecards

| Scenario | Handoff Clarity | Context Continuity | End-to-End Coherence | Avg |
| --- | --- | --- | --- | --- |
| X1 — Model → product → generate → audit | 3 | 3 | 3 | 3.0 |
| X2 — Compliance gap → model change → products | 3 | 3 | 2 | 2.7 |
| X3 — Source onboarding → product | 3 | 2 | 2 | 2.3 |
| X4 — Brownfield adoption | 4 | 3 | 3 | 3.3 |
| X5 — New user → first model | 3 | 2 | 2 | 2.3 |
| X6 — Source mapping → dbt → tests (new) | 3 | 3 | 2 | 2.7 |
| **Average** | 3.2 | 2.7 | 2.3 | **2.7** |

- **X1.** The product declaration is a real input contract for Artifact (`schema_type`, logical model, consistency posture). The handoff block format is consistent across agents (`CONVENTIONS.md`). Continuity breaks where the product is wrong (L2-04, L2-09), and Governance Level 4 doesn't catch that. The pipeline is coherent in shape and defective in its reference content.
- **X2.** Governance's structural handoff to Ontology is explicit. Ontology has "After a version bump that affects entities in data products, flag those products". But nothing prompts Architect to re-check masking for the new `consent_basis` attribute unless the user carries it across. The chain of custody lives in `LIFECYCLE.md`, if the Lifecycle skill is run.
- **X3 (weakest with X5).** Tomás can declare the Shopify source and map attributes. He can't populate relationships whose target entity isn't unique or that carry edge attributes (L2-01). He can't mark unsourced attributes (L2-23). There's no inverse index to tell Aisha which products are affected (L2-16). His `.` separators silently skip checks (N2).
- **X4.** Guide to Ontology to Governance is the best-sequenced journey, with a clear skill for each step. It loses points on scale (N8) and on Level 3 and 4 having no example.
- **X5.** Every step works on its own. The seams fail: setup writes the N1 layout, the starter teaches N6, lint gives false green, and an empty project's lint exits 2 without guidance.
- **X6.** The Artifact/Test ownership table in the dbt skill is the clearest multi-agent contract in the repo. The workflow breaks on the 0.10 features (contributions, `when_absent`, `earliest`) that neither agent implements (L2-19).

**Strongest workflow:** X4, because every stage has a named skill and a clear exit criterion (maturity level).

**Weakest workflows:** X3 and X5. X3's source-to-product lineage isn't traceable in reverse, and X5's first-run seams produce silent false confidence.

**Handoff pattern:** consistent (one block format, one protocol, per-agent Boundaries tables). Friction comes from content defects and missing propagation, not from the handoff mechanism.

---

## Standard Scorecards

| Scenario | Expressiveness | Completeness | Learnability | Avg |
| --- | --- | --- | --- | --- |
| G1 | 4 | 4 | 3 | 3.7 |
| G2 | 4 | 3 | 3 | 3.3 |
| G3 | 4 | 4 | 4 | 4.0 |
| G4 | 3 | 2 | 3 | 2.7 |
| G5 | 4 | 3 | 3 | 3.3 |
| G6 | 4 | 4 | 3 | 3.7 |
| O1 | 4 | 3 | 3 | 3.3 |
| O2 | 4 | 3 | 4 | 3.7 |
| O3 | 4 | 4 | 3 | 3.7 |
| O4 | 3 | 2 | 3 | 2.7 |
| O5 | 3 | 3 | 3 | 3.0 |
| O6 | 3 | 2 | 3 | 2.7 |
| O7 | 4 | 4 | 4 | 4.0 |
| O8 | 4 | 3 | 3 | 3.3 |
| A1 | 3 | 2 | 3 | 2.7 |
| A2 | 3 | 3 | 3 | 3.0 |
| A3 | 4 | 4 | 4 | 4.0 |
| A4 | 3 | 3 | 3 | 3.0 |
| A5 | 3 | 2 | 3 | 2.7 |
| A6 | 4 | 3 | 3 | 3.3 |
| D1 | 4 | 3 | 3 | 3.3 |
| D2 | 4 | 3 | 4 | 3.7 |
| D3 | 4 | 3 | 3 | 3.3 |
| D4 | 2 | 2 | 3 | 2.3 |
| D5 | 3 | 3 | 3 | 3.0 |
| R1 | 3 | 3 | 4 | 3.3 |
| R2 | 3 | 2 | 3 | 2.7 |
| R3 | 4 | 4 | 4 | 4.0 |
| R4 | 3 | 3 | 3 | 3.0 |
| T1 | 4 | 3 | 3 | 3.3 |
| T2 | 4 | 3 | 3 | 3.3 |
| T3 | 4 | 4 | 4 | 4.0 |
| **Average** | 3.5 | 3.0 | 3.3 | **3.3** |

Learnability rarely exceeds 3. Two reasons:

- **Size.** The normative text is roughly 150 KB over ten sections (`MD-DDL-Complete.md` is 144,600 bytes). §7–§9 alone are about 81 KB.
- **Parallel notations.** The source layer uses `·` for two different things, `.` in Destination cells, `Reference: <Entity>`, `Parent · Subtype`, and both list and map attribute shapes.

The spec is readable, but it's a reference manual. The agents are the on-ramp, which is by design and a reasonable bet.

---

## Standard Critique

### 1. Conceptual Completeness — Adequate

The lifecycle from discovery to testing is covered end to end. There's no cliff at sources and transformations: Source Mapping (344 lines) and §7–§8 are the most detailed parts of the standard, which reverses the March review's concern.

The cliffs are elsewhere:

- no cross-domain reference syntax (L2-16);
- no way to say "unsourced" (L2-23);
- no Level 3 or 4 adoption example (N8);
- JSON Schema is advertised but thinly supported (A5).

### 2. Learning Curve — Needs Work

- **Alex** is carried by the Guide, but tripped by setup (N1, N5) and the starter (N6).
- **Sarah** gains versioned Markdown and semantics, and pays the diagram/YAML double entry (N9).
- **James** gets value only once he sees output (N3).
- **Marcus and Priya** can read governance YAML. The regulator-file staleness costs credibility on first use.
- **Tomás** faces the steepest notation (N2).
- **Kenji** gets a systematic checklist that mis-grades the reference model (O5).
- **Dr. Kowalski** meets gaps at FHIR's hardest constructs (N10).
- **Rachel** has a credible ladder, but no scale mechanics.

The investment is justified for a platform team. It's heavy for a single analyst.

### 3. Agent Handoff Friction — Adequate

The mechanism is consistent and well documented, with one block format and one protocol. Friction comes from content: product defects propagate unchallenged, and model changes don't push to product owners. L2-18's file-naming issue matters less than Layer 2 suggests (see the disagreement section).

### 4. Governance Integration — Adequate

Governance appears at domain scoping ("Governance and platform" interview step) and during entity authoring ("Apply governance as you draft"), so it isn't bolted on. The weak points are structural:

- a single `retention` field (L2-07);
- domain-default-only conflict detection (L2-08);
- unvalidated masking names (L2-04);
- no PHI or de-identification vocabulary (R4).

A risk manager *can* audit without modelling knowledge. The Gap Report format is designed for that.

### 5. Industry Alignment — Adequate

- **Strong:** BIAN (local v13 index, verification discipline), FHIR resources, TM Forum SID, ISO 20022 business components.
- **Weaker:** ACORD (membership-gated, honestly flagged), FHIR polymorphism (N10), and no local GS1 or retail standard. The Retail examples cite none.
- **ODPS:** the ODPS skill infers quality dimensions from constraints, which is genuinely useful, but nothing validates the output.

### 6. Scalability — Needs Work

The two-layer summary/detail split helps AI context. There's no grouping below the domain level, and a 100-entity `domain.md` is roughly 100 KB (L2-16 estimate). Brownfield imports have no batching (N8). Multi-source fan-in semantics are underdetermined (L2-02). None of this bites a one-domain pilot. All of it bites by domain three.

### 7. Physical Generation Gap — Needs Work

The mapping rules (`existence`/`mutability` → structure in `generation-semantics.md`) are clear, the dialect files are substantive, and the inheritance templates are strong (A3). But:

- types are lossy (L2-05);
- FK optionality is undetermined (L2-03);
- JSON Schema is thin (A5);
- no committed reference output exists (N3);
- generation is non-deterministic by nature, with no golden baseline to detect drift.

Debuggability rests on the mapping summary and `meta.md_ddl`, which are good.

### 8. Source and Transformation Coverage — Adequate

The vocabulary is broad: direct, derived, conditional, lookup, deduplication, reconciliation, aggregation, fan-out and fan-in. Worked examples as contracts is the standard's best idea, and I confirmed it compiles to working dbt unit tests.

The gaps:

- Relationship sourcing (L2-01) and repeating groups (L2-21) are real brownfield needs.
- Semantics for the newest constructs are unsoaked (V1-05).
- Notation friction (N2).
- Reverse lineage isn't traceable.

### 9. Model Evolution and Lifecycle — Needs Work

The lifecycle states and `LIFECYCLE.md` manifests exist for both domains and products. But:

- the breaking-change definition contradicts itself (L2-17);
- external consumers are invisible (L2-16);
- the standard itself has no compatibility policy (V1-01);
- projects can't pin the tooling version (N4).

For "adopt and stay", this is the weakest dimension.

### 10. Brownfield Adoption — Adequate

The maturity ladder is realistic and per-domain, and coexistence is explicit. Schema Import is correctly positioned as the primary path. Missing:

- scale mechanics;
- Level 3 and 4 exemplars;
- a non-stale example (N8);
- a way to trace one baseline to several entities (`superseded_by` is a single path, L2-M12).

### 11. Verification and Testability (added) — Adequate, with the best upside

`1-Foundation.md § Verification of Generated Artefacts` plus Agent Test is a differentiator no comparable standard has: domain-written examples outrank derived tests. The design is sound, and the dbt mechanics work (N7). What's missing is a reference run, an offline local tier, and support for the 0.10 fan-in constructs (L2-19).

---

## Stakeholder Verdict

| Persona | Would Adopt? | Why / Why Not | Key Improvement Needed |
| --- | --- | --- | --- |
| Alex (New User) | Maybe | The Guide is a good on-ramp, but first-run seams produce false confidence | One consistent layout that lint fully checks (B1); fix the starter (N6) |
| Sarah (Modeller) | Yes, with reservations | Modelling guidance respects her expertise; inheritance DDL is right | Diagram/YAML tooling (N9); FK optionality (L2-03) |
| Marcus (Steward) | Maybe | Governance-in-model is the pitch he wants; masking isn't validated | Masking resolution check (L2-04) in lint or Governance Level 4 |
| Priya (Risk Manager) | Maybe | File selection is precise; staleness on every file undermines trust | Re-verified regulator files (B7); consistent conflict rule (L2-07) |
| James (Engineer) | Not yet | No visible output; lossy types; DuckLake needs network | Committed reference output and green test run (B3); precision/scale (B5) |
| Aisha (Product Owner) | Yes, for single-domain products | Product design is strong; cross-domain is vague | Cross-domain references (L2-16) in 1.x |
| Dr. Kowalski (Healthcare) | Maybe | Governance and temporal add value above FHIR; polymorphism unanswered; example non-conforming | FHIR patterns guide (N10); rebuild the Healthcare source layer (V1-06) |
| Tomás (Integration) | Maybe | Worked examples as contracts is compelling; notation and relationship sourcing hurt | Accept `.` separators (N2); relationship sourcing (L2-01) |
| Kenji (Review Lead) | Maybe | Systematic protocol, but mis-grades the reference domain | Fix the identifier rule (L2-20); add cross-file semantic checks |
| Rachel (Brownfield Lead) | Yes, for a pilot | Ladder and import path are credible | Scale guidance and a Level 3/4 exemplar (N8) |

No persona says "no" outright. The pattern is "yes to the idea, not yet to the evidence". That fits a standard whose design is ahead of its reference content and tooling.

---

## Comparison with Previous Evaluation (2026-03-13 Layer 3)

Area | March 2026 | Now | Note
--- | --- | --- | ---
Guide | 4.3 | 3.6 | Mostly method: hands-on setup found N1/N5; March didn't run the install
Ontology | 4.2 | 3.75 | Source Mapping and Schema Import are much improved; Domain Review's blind spots are now visible via Layer 2
Artifact | 4.4 | 3.6 | dbt and Faker added; the lack of reference output now weighs more
Architect | 3.8 | 3.7 | Product lifecycle and consistency posture added; cross-domain still weak
Governance | 4.3 | 3.8 | `hipaa.md` now exists (a March gap); staleness and conflict-rule contradictions cost points
Test | n/a | 3.9 | New agent; strongest boundaries in the suite
Workflows | 3.3 | 2.7 | X3 (2.7 → 2.3) remains weakest; X5 fell with the hands-on first run
Standard | 3.7 | 3.3 | Expressiveness up (source layer); completeness and learnability down as scope grew

**Closed since March:** source and transformation agent support (the March X3 "no skill" concern), HIPAA coverage, product lifecycle states, and a testing story.

**Still open:** cross-domain expressiveness, reverse lineage, new-user seams.

**New:** N1–N11.

---

## Disagreement with Prior Layers

1. **L2-16 (cross-domain relationships and `extends`) and L2-12 (valid-time mapping) should not block v1.** Layer 2 argues these are "frozen grammar". Adding a *new* optional reference form (`Domain.Entity` in `extends`/`target`) or a *new* optional key (`valid_from:`) is additive under any semver policy V1-01 is likely to adopt. Existing 1.0 models stay valid. Adopters also start with one domain (`adoption-planning/SKILL.md`: "Recommend one well-understood domain"), so they meet cross-domain limits months after adopting. **They are "stay" issues for 1.1–1.2, not adoption blockers**, provided the 1.0 text doesn't forbid the future syntax. By the same reasoning, L2-05's new `precision`/`scale` properties are additive. I still rank L2-05 as a blocker, but for adoption reasons (James rejects lossy money columns on day one), not grammar-freeze reasons.

2. **L2-02 (multi-source semantics) and L2-11's finer points (delimiter escaping, normalise order, tie-breaks) are largely theoretical in year one.** Few adopters will use `contributes`/`when_absent` fan-in in their first months. Resolving every reading before 1.0 risks more same-day spec churn, which V1-05 warns against. I agree with the readiness review's option 3: mark these constructs **provisional in 1.0**. Resolve (a) re-emission and (b) default merge now, because generators hit them immediately, and defer the rest.

3. **L2-18 (handoff files) is overstated for real users.** The primary handoff is the inline block the user pastes (`CONVENTIONS.md` Sending steps 1–2). Files are the cross-session fallback. The `agent-artifact` vs `artifact` naming mismatch matters only if the receiving agent searches literally, and a model with file search will likely find `handoff-to-artifact.md`. The one-pending rule bites only when two agents hand off to the same receiver in the same domain before it runs, which is rare for small teams. Fix the naming, but it isn't an adoption blocker.

4. **Layer 1 S3/S4 (review prompts' output path and staleness) are not v1 blockers from an adopter's standpoint.** `.prompts/` isn't packaged (`DOCS_PAYLOAD`), so no adopter sees it. It's maintainer hygiene and can be fixed at any time.

5. **Layer 1 S1 (`## Sources` vs `## Source Systems`) is mostly invisible to users**, because agents write both headings. It matters to third-party parsers, which don't exist yet. Keep it on the v1 list as grammar hygiene, but at low adoption impact.

6. **The readiness review's V1-02 (conformance definition) matters less to adopters than V1-04 or N1.** Users don't read conformance clauses. They trust the green lint. A precise conformance section with a linter that skips the documented layout helps no one, so fix the linter behaviour first.

7. **Understated: V1-07 (licence) and L1 S9 (regulator staleness).** The README's stated distribution route is "pulled through a corporate artifactory". In banking, the flagship's own industry, the licence scanner is the literal first gate, and CC BY on Python code commonly fails it. Regulator staleness on every file but one is the first thing Priya sees. Both are cheap and both are gating, so I rank them higher than the prior reviews did.

8. **Agreement with Layer 1's "boundaries are clean" against Layer 2's handoff concerns.** Across 39 scenarios, Boundary Respect is the highest-scoring dimension (average ~4.1). Personas never saw an agent do another agent's work. The prompts' boundary design is real strength, not surface conformance.

9. **Understated in all prior layers: the absence of generated reference output (N3).** Layer 1 treated it as a false README claim. For adopters it is the evidence gap: a standard whose value proposition is "model once, generate everything" ships with nothing generated.

---

## Priority Recommendations

### Fix existing (before v1)

1. Make `cli.py`'s generated layout, the README, the Foundation and §7 name one layout, and make lint check it fully. Warn on `.md` files that belong to no domain. (N1, L1 S7, V1-04)
2. Fix Simple Customer: a single primary identifier, relative links, and consistent attribute shapes. (N6)
3. Fix the flagship consumer product's masking, and add a masking-resolves check to lint or Governance Level 4. (L2-04)
4. Accept `.` and ` - ` as target separators, or warn when a target can't be parsed. (N2)
5. Record the installed md-ddl version in a committed file and warn on mismatch. Recommend pinning in the README. (N4)
6. Re-verify regulator files, or ship with a prominent "verification pending" banner. (L1 S9)
7. Tell the user what to add when `CLAUDE.md` or `copilot-instructions.md` already exists. (N5)

### Extend capability (1.0 or early 1.x)

1. Commit one reference output set for one example: DDL for one dialect, a dbt project, a test run log and an ODPS manifest. Treat it as the regression baseline for agent changes. (N3, readiness S-11)
2. Add a plain-DuckDB fallback and offline extension install notes to the dbt-project skill; materialise contracted models as tables locally. (N7)
3. Brownfield scale playbook (batch per schema or subject area, session boundaries), a Level 3/4 continuation of Brownfield Retail, and a refreshed `target_date`. (N8)
4. Diagram render or fix tooling from YAML. (N9)
5. A JSON Schema generation section with a draft version, `$ref` convention, type table and nullability. (A5)
6. A FHIR patterns note covering polymorphic references and choice types. (N10)
7. An analyst archetype and a "vs CREATE TABLE" answer in Agent Guide. (N11)

### Spec improvements

1. `precision`/`scale`/`max_length` attribute properties; cardinality optionality. (L2-05, L2-03)
2. Mark the 0.10 fan-in constructs provisional in 1.0. (L2-02, V1-05)
3. Cross-domain reference syntax and a `sourced: false` declaration as 1.x additive features. State in 1.0 that they're planned, so adopters know. (L2-16, L2-23)
4. A de-identification method field, or an explicit mapping from PHI to PII. (R4)

---

## Ranked adoption blockers for v1

Ranked by how likely a real adopter is to hit the issue, multiplied by how much trust it costs when they do. "Adopt" means the evaluation and first model; "stay" means the first three months.

Rank | Blocker | Stage | Source | Why it ranks here
--- | --- | --- | --- | ---
**B1** | The documented project layout is not the linted layout; `md-ddl init`'s own instructions produce a false green on entity files | Adopt | **N1**, L1 S7, V1-04 | Every newcomer, and every agent following `CLAUDE.md`, hits it on the first model, and the failure is silent
**B2** | CC BY 4.0 on the Python package; no name-use terms | Adopt | V1-07 | Enterprise intake (the README's target route) gates on it before anyone runs anything
**B3** | No generated reference output or test run exists; README claims otherwise | Adopt | **N3**, L1 S6 | The engineer persona can't evaluate the core value proposition; there's no regression baseline for agent changes
**B4** | Starter and flagship examples violate the spec's own rules (two primary keys in Simple Customer; dangling masking and unmasked PII in the flagship consumer product; Healthcare/Telecom sources pre-0.10) | Adopt | **N6**, L2-04, L2-20, V1-06 | Examples are what agents and users copy; the governance defect is the kind a steward or risk manager would never forgive
**B5** | Generated DDL is lossy: no precision, scale or length; FK nullability undetermined | Adopt → stay | L2-05, L2-03 | A data engineer rejects `NUMBER(38,0)` money on sight; wrong FK nullability fails the first load
**B6** | No compatibility policy, no changelog, and no way for a team to pin the MD-DDL version its agents run | Stay | V1-01, **N4** | Upgrades silently change agents and lint rules under every teammate; this is what makes adopters leave in month two
**B7** | 12 of 13 regulator files are stale by the agent's own rule | Adopt (governance buyers) | L1 S9 | The first compliance audit opens with a staleness warning on nearly every file; cheap to fix
**B8** | Copilot `{{INCLUDE}}` expansion unverified; the Copilot wrappers, unlike the Claude ones, don't tell the model to read the include | Adopt (VS Code users) | Readiness S-12 | If it fails, half the audience gets a generic assistant on first use. **Verify before v1**: if it works, this drops off the list
**B9** | Silent linter holes adopters hit in normal use: `.` target separator, `.venv/` not ignored, YAML `Yes`/`No` crash, no tests | Stay | **N2**, V1-03, S-06 | Each is small, but together they erode trust in the green check that the whole Tier 1 model rests on

These are not blockers, and can be improved in v1.x:

- cross-domain references and `extends` (L2-16);
- valid-time mapping (L2-12);
- repeating groups (L2-21);
- the remaining multi-source semantics, once marked provisional (L2-02);
- FHIR polymorphism (N10);
- diagram/YAML double entry (N9);
- brownfield scale guidance and a Level 3/4 exemplar (N8);
- DuckLake offline (N7);
- an existing `CLAUDE.md` merge (N5);
- handoff file naming (L2-18);
- JSON Schema depth (A5);
- Guide archetypes (N11).
