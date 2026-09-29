# Agent Definitions Review — Simplification for Current Models

**Date:** 2026-09-29
**Scope:** The six core prompts (`agents/*/AGENT.md`), `agents/CONVENTIONS.md`, and the Claude command wrappers (`.claude/commands/`). Skills (`agents/*/skills/`) are out of scope except where they reference the core prompts.
**Trigger:** Current models (Opus 5.5 class) follow plain instructions closely and infer good behaviour from intent. Prompts written for earlier models over-specify: scripted phrases, repeated rules, and emphatic wording now cost context and cause over-application more than they prevent mistakes.

---

## Summary

The agent definitions total about 1,630 lines, before the Foundation that each one includes. Roughly a third is repetition: the same handoff protocol written six times, skill tables restated as prose protocols, boundaries stated two or three times in one file, and two agents with duplicate "cannot validate" sections. That repetition has already caused drift. Command wrappers list stale skill sets, the Artifact prompt's assessment list is mis-numbered, and Governance's modes cross-reference each other incorrectly.

Simplification keeps every rule that encodes a real MD-DDL decision and removes scaffolding a capable model does not need.

## Simplification Principles

1. **One source of truth per rule.** The handoff protocol lives in `CONVENTIONS.md`. Each agent keeps only *when* to hand off and *to whom*.
2. **State intent, not scripts.** Remove canned transition and opening phrases; keep what must be confirmed or asked.
3. **Plain rules with reasons, not emphasis.** "Non-Negotiable", bold "Always", and "do not skip ahead" lead current models to apply rules rigidly outside their intended scope. A rule with its reason generalises better.
4. **No restated tables.** A skill table with good triggers does not need a prose loading protocol repeating it. Keep only loading rules that add something (ordering, preconditions).
5. **No brittle counts or copies.** "You have nine skills" and skill lists in wrappers drift as skills are added.
6. **Keep the substance.** Drafting order, target verification, regulator staleness, remediation scope, materiality, the worked-example contract, and ownership boundaries all stay.

## Cross-Cutting Findings

ID | Finding | Where | Action
--- | --- | --- | ---
X1 | Handoff protocol (inline block, handoff file, `status` lifecycle, session-start check) repeated in every agent, 3–5 times in some | All six | Consolidate into `CONVENTIONS.md § Handoff Protocol`; agents keep a routing table
X2 | Skill table followed by a "Skill Loading Protocol" that restates each row | Artifact, Architect, Guide, Test | Keep the table; keep only non-obvious loading rules
X3 | Boundaries stated in Identity, then "What You Are Not", then in each handoff section | All six | One boundaries/routing table
X4 | Scripted transition, opening, and handoff phrases in quotes | All six | Replace with what to confirm or ask
X5 | Emphatic framing ("Non-Negotiable", "When in doubt, load the skill. The cost of…") | All six | Plain "Rules" section with reasons
X6 | Skill counts in prose | Guide, Ontology, Architect, Artifact, Governance | Remove
X7 | Command wrappers duplicate AGENT.md protocol with stale skill lists (Ontology missing three skills, Guide missing Adoption Planning) | `.claude/commands/` | Wrappers point to AGENT.md only

## Per-Agent Findings

### Agent Guide (273 lines)
- G1: The ASCII workflow diagram is misaligned and duplicates the numbered list below it. Remove it and keep the list.
- G2: "Mark demonstrations as demonstrations" is stated three times (Mode 2, Rules, Teaching Limitations). Keep one rule.
- G3: "Check understanding" after every concept reads as patronising with experienced users. Make it situational.
- G4: The archetype table's "Common first questions" column adds little that a model cannot infer. Keep the columns that change behaviour. The orientation skill references this table, so keep the table.
- G5: The agent directory is the most useful part of the prompt. Keep it.

### Agent Ontology (257 lines)
- O1: The loading protocol mixes restatement with real rules (verify every `target`, never map to the nearest plausible attribute, run the Determinism Test, brownfield delta-only). Keep the rules and drop the restatement.
- O2: Four handoff sections, each with its own template, repeat `CONVENTIONS.md`. Replace with a routing table.
- O3: The "Hallucinated domain facts" limit restates the "never invent" rule. Merge.
- O4: **Bug:** "Every entity must have at least one `identifier: true` attribute" contradicts the spec. 3-Entities uses `identifier: primary`, and treats an identifier as "should" (entities without one become Logic Objects).

### Agent Artifact (243 lines)
- A1: **Bug:** the Assessment list is mis-numbered. Item 6 ("If so:") is split by the Faker item 7, and the product sub-bullets sit under item 7.
- A2: **Stale:** "Both skills reference guidance…" dates from when there were two skills.
- A3: The loading protocol restates the skill table for every skill.
- A4: The Assessment checklist has no dbt questions (template, tier), though the dbt-project skill covers them. Point to the skill rather than duplicating.
- A5: **Bug:** the Upstream Dependencies paths (`../../agent-ontology/...`) are relative to a skill folder, not to AGENT.md, so they don't resolve from where they are written. Architect has the same defect.

### Agent Architect (337 lines)
- R1: **Duplicate sections:** "External Validation Requirements" and "What This Agent Cannot Validate" list the same four items. There is also a formatting defect (`.---`) where they join.
- R2: The Identity paragraph lists four "you do not" boundaries, then "What You Are Not" repeats them.
- R3: The archetype table duplicates the architecture skill's own archetype section. Remove it from the core prompt.
- R4: The Design mode's 11 steps partly restate the output rules (class scope, lineage, logical model). Keep the steps and drop the restated rules.

### Agent Governance (324 lines)
- V1: **Bug:** Mode 2 says regulator currency "is Mode 2"; it is Mode 3. The compliance-audit skill also calls monitoring "Mode 2" in two places.
- V2: The gap report format lives in AGENT.md while the compliance-audit skill, which produces the report, defers to it. Move the format into the skill.
- V3: The Identity section is four paragraphs of boundaries that repeat "What You Are Not".
- V4: The staleness check, materiality threshold, remediation scope, and conflict rule are substantive. Keep them.

### Agent Test (199 lines)
- T1: Written last session in the older house style. Apply the same principles; the triage model and contract rules stay.

## Out of Scope — Recommended Follow-Up

Skills total about 40 files and carry most of the procedural weight. They show the same patterns (scripted phrases, emphatic rules, restated spec text), and should be reviewed next, one agent's skills at a time.

## Changes Made

All findings were applied.

File | Before | After
--- | --- | ---
`agent-guide/AGENT.md` | 273 | 134
`agent-ontology/AGENT.md` | 257 | 139
`agent-artifact/AGENT.md` | 243 | 119
`agent-architect/AGENT.md` | 337 | 126
`agent-governance/AGENT.md` | 324 | 122
`agent-test/AGENT.md` | 199 | 118
`CONVENTIONS.md` | 89 | 77
**Total** | **1,722** | **835**

Each core prompt now has the same shape: Identity, Foundation, Skills, How You Work, Rules, Boundaries (a routing table), Limits, Opening. The handoff protocol lives only in `CONVENTIONS.md § Handoff Protocol`. The gap-report format moved into the compliance-audit skill. The command wrappers are now three lines each and point at the core prompt.

**Related fixes outside the core prompts:**

- `compliance-audit/SKILL.md`: two references to "Mode 2" corrected to Regulatory Monitoring
- `product-design/SKILL.md`: mode reference updated to "Assessment step"
