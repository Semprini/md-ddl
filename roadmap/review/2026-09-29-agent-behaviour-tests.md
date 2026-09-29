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
