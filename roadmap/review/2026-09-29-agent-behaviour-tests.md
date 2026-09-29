# Agent Behaviour Tests — After the Agent and Skills Simplification

**Date:** 2026-09-29
**Follows:** PR #14 ([agent definitions](2026-09-29-agent-definitions-review.md), [skills](2026-09-29-skills-review.md)). This closes its open test-plan item: spot-check each agent in a live session.

## Method

Each agent ran as a separate session. The session loaded the real `AGENT.md` and followed
its skill-loading instructions, then handled one realistic request against
`examples/Financial Crime/`. The user was non-interactive, so questions were pre-answered.
Each run reported the files it read, its output, and anything unclear. The repository was
read-only, and outputs went to a scratch folder.

Each run was graded against checks it didn't see. The checks targeted the defects PR #14
fixed, to catch regressions, plus general correctness.

## Results

Run | Request | Targeted checks | Result
--- | --- | --- | ---
Agent Guide | Install, agents in Claude Code, linting, verifying dbt output | `pip install md-ddl && md-ddl init`; `/agent-*` commands; `md-ddl lint` exists; validation vs verification | **Pass**
Agent Ontology (draft) | Add a Sanctions Screening Result entity and a confirmed-match event | `identifier: primary`; no FK attributes; `not_null` as a constraint; override-only governance; dictionary event attributes with a timestamp | **Pass.** It also caught that a pre-answer contradicted `enums.md`, and kept the stricter domain retention.
Agent Ontology (review) | Is Financial Crime ready for generation? | Ran lint first; Determinism Review; Observations section; readiness verdict | **Pass.** Verdict: Not Ready (below).
Agent Artifact (DDL) | PostgreSQL DDL for the Canonical Party product | Every relative path resolves; generation-semantics loaded; mapping summary; inheritance reasoning | **Pass.** All `../` paths resolved, and the DDL ran cleanly on PostgreSQL 16 with constraint tests.
Agent Artifact (faker) | UK-bank-profiled factories, safe mode | The module compiles and runs; runtime import works; integrity and temporal checks; safe names | **Pass, with a defect** (B2)
Agent Architect | ODPS manifest for Canonical Party | `Active` → `production`; channel proposed and marked TODO; `PROPOSED` data-quality objectives; accuracy left to the owner; YAML parses | **Pass, with minor defects** (B3)
Agent Governance | Compliance audit for an Australian bank | Staleness warning; spec fields used; no false inheritance gaps; masking routed to Architect | **Pass, with a factual error** (B1)
Agent Test | Coverage report plus one unit test | Lint gate; `derived` label; blocked items routed by owner; drafted examples marked proposed; YAML parses | **Pass**

No regressions of the PR #14 fixes were found.

## B. Defects in Agent Instructions

ID | Where | Defect | Fix
--- | --- | --- | ---
B1 | compliance-audit | Says APRA breach notification is "as soon as possible". CPS 234 requires 72 hours, as `apra.md` says. Carried over during PR #14. | Remove hard-coded timeframes and defer to the regulator file
B2 | faker | The code pattern samples date of birth and country from the profile even in `safe` mode, contradicting the safe-mode table. Locale and country are sampled separately and can disagree. The pre-built profile import isn't shown. There's no guidance for subtypes (`extends`) or inherited temporal columns. | Keep PII fields fixed in safe mode, derive country from the sampled locale, show the import, add a subtype note
B3 | odps-alignment | The template writes `version: 4.0` unquoted, so it parses as a float. Units disagree (`percent`, `percentage`, and `hours`, which isn't in the unit list). Uniqueness ignores primary identifiers. There's no format for relational tables, and no rule for a product exposing PII without masking. | Quote the version, align units with the reference, count identifiers, route unmasked PII to Governance
B4 | standards/bian/README.md | Points to `v13/bo-classes.md`, but the files are directly under `bian/` | Correct the paths
B5 | regulators/apra.md, basel.md | Propose fields (`information_asset`, `cps234_scope`, `apra_reporting`, `risk_category`) that regulatory-compliance now forbids. The mapping has no Australia-only row, and there's no AUSTRAC file although entities cite AUSTRAC. | Align the files with the schema, split the AU and NZ rows, consider an AUSTRAC file
B6 | `.claude/commands/*` | Wrappers never tell the model to load the files named in `{{INCLUDE}}` directives, so loading the Foundation depends on the model noticing an HTML comment | Add one line to each wrapper
B7 | Readiness and handoff rules | Any lint error makes a model Not Ready, even a diagram-vs-YAML mismatch that doesn't affect generation, with no rule on which representation wins. Archived handoff files aren't covered, and neither is a handoff to two agents at once. | State that YAML is authoritative for generation, and define handling of archived and multi-agent handoffs
B8 | Agent Artifact Limits | "Nothing you generate is executed by you" is untrue when a database or runtime is available | Reword: run output when possible, and say so
B9 | postgresql dialect vs generation-semantics | Different key-column naming conventions | Choose one
B10 | Agent Guide skills | Cover the local DuckLake tier but not how it relates to Snowflake or dbt Cloud | Add one line to the Concept Explorer dbt comparison
B11 | Linter | Doesn't check that transform `target`s resolve, or that conditional case keys are valid enum values. Both are mechanical. | Candidate lint rules

## C. The Financial Crime Example Is Not Ready

The domain review, confirmed independently by the Test and Artifact runs, found that the
flagship example fails its own standard:

- 17 lint errors: an enum heading/anchor mismatch, and Data Products links to `products/`
  where the folder is `data_products/`
- 6 of 13 Salesforce transform targets don't resolve (for example Registration Identifier vs
  Registration Number, and PEP Status vs Politically Exposed Person Status). The SAP
  transform targets `Party.Watchlist Match Indicator`, which Party doesn't declare.
- Conditional cases use values that aren't in their target enums (`Suspended`, `Confirmed`,
  `Unknown`, `Pending`, `Failed`)
- Party Role subtypes each declare their own primary identifier on top of the inherited one
- The Salesforce mapping has no Entity Fan-Out, worked examples, or open decisions, and no
  fan-in example for Party or Customer
- Transform files use pre-spec heading levels, and event payload keys are snake_case
- Two BIAN references (`LegalEntity`, `Payment`) aren't in the local v13 index
- The canonical product declares no consistency posture, and retention text (7 years)
  disagrees with the field (10 years)

Because the example is what agents and users learn from, bringing it up to the standard
should come before adding more features.

## Recommended Next Steps

1. Fix B1 through B4 and B6. They're small, and B1 and B2 were introduced by PR #14.
2. Repair Financial Crime with Agent Ontology, using the domain review in this run as its
   work list.
3. Take B5, B7, and B11 into the next spec and tooling round.

---

## Resolution (same day)

### Instruction defects

ID | Resolution
--- | ---
B1 | compliance-audit no longer quotes notification windows; it defers to the regulator file. `apra.md` now records the CPS 234 windows, checked against apra.gov.au: 72 hours for material incidents, 10 business days for material control weaknesses.
B2 | faker keeps `pii: true` fields at safe-mode placeholders even with a profile. A new `country_for_locale()` helper derives the country from the sampled locale. The skill shows the profile import and covers subtypes. The code pattern was executed in three modes.
B3 | ODPS version quoted; units follow the reference (`percent` for SLA, `percentage` for data quality, minutes for timeliness); uniqueness counts identifiers; SQL ports have no `format`; unmasked PII goes to Agent Governance; `sla.freshness` takes precedence over `refresh`.
B4 | The BIAN README points at the index files that exist.
B5 | `apra.md`, `basel.md`, and `rbnz.md` use only schema fields; business facts (risk categories, PD/LGD, providers) become modelled attributes. `apra.md` records CPS 230's 1 July 2025 commencement, replacing CPS 231. A new `austrac.md` records the verified AML/CTF record-keeping periods. The regulator mapping splits the AU and NZ rows.
B6 | Claude command wrappers tell the model to read `{{INCLUDE}}` targets.
B7 | Domain review separates lint errors that break the YAML (Critical) from representation disagreements (Major, which block promotion but not generation). The YAML is authoritative. The handoff conventions cover consumed and archived files, and multiple recipients.
B8 | Agent Artifact runs its output when a database or runtime is available, and says when it hasn't.
B9 | Bridge columns are named `source_`/`target_` plus the referenced key column, so they follow the dialect.
B10 | Concept Explorer explains the local and cloud dbt tiers.
B11 | New lint rules `transform-target-resolve` (including `Reference:` destinations) and `transform-case-values`.

### Spec decisions

- Security and residency fields (`data_residency`, `cross_border_transfer`, `audit_all_access`, `breach_notification_required`, `notification_timeframe`) are part of the governance schema.
- `masking` is declared under `governance`. Products declare `consistency` (posture, null strategy) as a field, not a comment.
- Entity Fan-Out gains `contributes: true` for sources that add to an instance another source establishes. `references` may name existing instances. Reference-only columns use `Reference: <Entity>`. Joins between source tables aren't declared, so extracts carry parent keys.
- Identity: `derived` suffices when rows don't merge. Composite deduplication keys are `prefix:v1|v2|…`. Survivorship gains `earliest`.
- `abstract: true` declares abstract entities in YAML. `relationship_attributes` applies to any relationship with link attributes. Columns omitted from a worked example's `given` are null.
- Example folders are `products/`, as the spec says. `Production` isn't a lifecycle status, so the examples use `Active`.

### Examples

All seven examples lint with no findings, including under the two new rules. Financial Crime is rebuilt as domain 2.0.0 (see its `LIFECYCLE.md`). Healthcare's transform targets were corrected. Telecom, Brownfield Retail, and Simple Customer diagram and summary defects were fixed, and a same-file enum false positive in the linter was removed.

### Remaining

- Healthcare's and Telecom's source layers still use the pre-spec layout (source-rooted headings, a `Comment` column, no fan-out or worked examples, benign fallbacks such as `fallback: Active`). They lint clean but would fail a domain review's Determinism Test. Rebuild them the way Financial Crime was rebuilt.
- `rbnz.md` was last verified on 2025-03-08. It needs re-verification by Agent Governance, including the NZ AML/CFT Act section 58 retention that Financial Crime cites. The RBNZ and AUSTRAC sites couldn't be fetched from this environment, so only search-visible facts were verified.
