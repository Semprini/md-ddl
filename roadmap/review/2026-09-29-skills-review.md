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
