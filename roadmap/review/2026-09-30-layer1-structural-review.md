# MD-DDL Review — 2026-09-30 (Layer 1: Structural)

**Spec version reviewed:** Draft 0.10.0 (from `md-ddl-specification/1-Foundation.md:1`)
**Package version:** `md-ddl` 0.10.0 (`src/md_ddl/__init__.py:17`)
**Commit reviewed:** `02e39f7` (working tree clean)
**Brief:** `.prompts/md-ddl-review-prompt.md`, run under `.prompts/md-ddl-layered-review-process.md` (Layer 1), plus v1-readiness structural checks requested by the owner.

Severity scale used in this report (the owner asked for this scale rather than the prompt's Critical/Advisory split):

- **Critical**: the normative spec contradicts itself, or a published claim or link is broken in a way that misleads users or agents.
- **Major**: a documented structure, contributor rule, or shipped prompt is out of step with the repository and would mislead a contributor, a reviewer, or an installed agent.
- **Minor**: a local inconsistency, a stale detail, or a cosmetic defect.

"Blocks v1?" means: should this be resolved before a 1.0.0 freeze of the spec and package.

---

## How this review was run

Every finding below was checked by reading the cited file or running a command. Tools used:

- A Markdown link and anchor checker (GitHub slug rules; inline code and non-Mermaid fences excluded) run over `README.md`, `CLAUDE.md`, `agents/`, `guides/`, `md-ddl-specification/`, `examples/`, `.github/`, `.claude/`, `.prompts/`, `roadmap/v1/` and `scripts/`. That is 295 files.
- A backtick path-reference checker over `agents/`, `guides/`, `.github/`, `.prompts/`, `CLAUDE.md` and `README.md`. It also checked every `file.md § Section` reference against the headings in the target file.
- `python scripts/md_ddl_lint.py "<example>"` on all 7 examples.
- `md_ddl.includes.scan/unresolved` over the payload directories.
- A Python port of `scripts/concat-md-ddl-specs.ps1`, diffed against `MD-DDL-Complete.md`.
- A wheel built with hatchling, installed into a clean venv, then `md-ddl init --name demo`, `md-ddl check`, and `md-ddl lint` run in an empty directory.
- An import and lint run under Python 3.9 (via `uv`), the declared minimum.
- `grep` sweeps for version strings, stale names, agent counts, and rule restatements.

---

## Summary table

ID | Severity | Blocks v1? | Area | Finding (short)
--- | --- | --- | --- | ---
S1 | Critical | Yes. v1 freezes heading names that parsers key on | Spec | The domain section for sources is `## Source Systems` in §2 but `## Sources` in §7, so detail files cannot "repeat the relevant level-2 heading"
S2 | Major | Yes. v1 freezes field vocabularies | Spec / examples | Source `status:` has no defined vocabulary; every source uses `Production`, which is outside the domain/product lifecycle vocabulary
S3 | Major | Yes. The v1 sign-off reviews run from these prompts | Review tooling | `CLAUDE.md:70-71` says each `.prompts/` file carries the dated output path. None does: all write to `review.md`, which `.gitignore:208` ignores
S4 | Major | Yes. The v1 sign-off reviews run from these prompts | Review tooling | The Layer 1/2/3 prompts predate Agent Test ("five AI agents", agent lists without agent-test, "Draft 0.9.0", "12 rules", baseline "mapping blocks")
S5 | Major | Yes. It is the contributor source of truth | Contributor guidance | `.github/copilot-instructions.md` is stale: no Agent Test, 4 skills missing from the layout, "exactly 5 checks" (there are 14), "no build system"
S6 | Major | Yes. It is the public face | README / examples | README and `examples/README.md` claim "generated artifacts" for Financial Crime (never committed; `generated/` is gitignored). Brownfield Retail is missing from both example tables, and README says "Five reference domains" while 7 exist
S7 | Major | Yes. Onboarding contradiction | Layout docs | Four incompatible project layouts are documented (spec, README, `md-ddl init` output, bootstrap scripts)
S8 | Major | Yes. Affects every installed project | Agents (packaging) | Agent prompts cite repo-root paths (`md-ddl-specification/…`, `agents/…`, `guides/…`) that do not exist at a consumer's root, and no path base is declared. The contributor guide contradicts itself on this
S9 | Major | Yes. The shipped prompt triggers its own warning on every use | Agent Governance | 12 of 13 regulator files are `last_verified: 2025-03-08`, over 12 months old, which trips the agent's own staleness rule
S10 | Major | Yes. v1 of a shipped linter needs regression protection | Tooling / release | No tests for `lint.py` (1,752 lines) or `cli.py`; CI runs only on release; nothing checks `MD-DDL-Complete.md` sync or links on PRs
S11 | Major | Yes. A 1.0 standard needs a change record | Release hygiene | No spec CHANGELOG or version history; version bumps are only visible in git (`dd3923e` moved 0.9.2 to 0.10.0)
S12 | Major | Yes. Dead route in a shipped prompt | Agent Guide | The Agent Directory routes users to `review-md-ddl`, which is deliberately not installed in consumer projects and has no Claude equivalent
S13 | Minor | No | Examples | Example source layout (`source.md` + `transforms/table_lowercase.md`) differs from the §7 convention (`sources/sources.md`, `table_<SOURCE_CASING>.md`)
S14 | Minor | No | Examples | Feeds tables use `batch`, which is not a `change_model` value. The coverage matrix claims `change_model: batch` for 3 examples that don't use it
S15 | Minor | No | Spec | §2 Domain Structure Example puts `### Domain Overview Diagram` under `## Source Systems`, and §2 uses two different source-link targets
S16 | Minor | No | Spec | The one-mapping-path rule is stated in both §7 and §8, near-verbatim
S17 | Minor | No (Layer 2 to judge) | Spec | §9 says consumer-aligned lineage is from canonical *entities* (l.149, l.210) and also from canonical *products* (l.229)
S18 | Minor | No | Agents | Dead section name: Ontology `AGENT.md:117-118` cites "Governance Authoring Protocol", but the heading is "Governance While Authoring"
S19 | Minor | No | Agents | Concept Explorer's reference table lists §10 but has no `adoption-spec.md` stub; the Guide is told to load from these stubs first
S20 | Minor | No | Agents | Ontology `AGENT.md:86` makes ELK a flat rule; the only source is the non-normative guide, which says "for complex graphs"
S21 | Minor | No | Agents | compliance-audit rates an invalid `status` value Critical, against the vocabulary-deviation-is-advisory philosophy
S22 | Minor | No | Wrappers | Copilot wrapper descriptions are stale (Artifact: "dimensional/3NF" only; Ontology: no sources or brownfield)
S23 | Minor | No | Wrappers | `.github/agents/*.agent.md` include `../../.md-ddl/…`, which does not exist in this repo, so the Copilot agents don't work when contributing here
S24 | Minor | No | Packaging | The `review.md` exclusion in `cli.py:24` and both bootstrap scripts matches no file
S25 | Minor | No | Standards refs | Two dead relative links copied from FHIR (`operations.html`, `terminologies.html`)
S26 | Minor | No | Roadmap | `roadmap/v1/completed/plan-brownfieldAdoption.prompt.md:639-648` has 9 dead `../../` links (the file moved one level deeper)
S27 | Minor | No | README | Relative links break on the PyPI project page (`readme = "README.md"`)
S28 | Minor | No | Contributor guidance | Stale counts and paths in copilot-instructions (17 blog posts vs 18; `industry_standards/bian/` path; shared-skills list)
S29 | Minor | No | Review tooling | The review prompt asks about Claude.ai Projects integration; neither README nor platform-setup documents it
S30 | Minor | No | Tooling | `MD-DDL-Complete.md` can only be regenerated with PowerShell (the file is in sync today)

---

## Critical findings

### S1 — The Sources section heading contradicts itself across §2 and §7

- `md-ddl-specification/2-Domains.md:88` says source systems "must be declared under a level-2 heading immediately after `## Metadata`". Line 101 and line 158 name that heading `## Source Systems`. `9-Data-Products.md:29` agrees: "the domain's `## Source Systems` section".
- `md-ddl-specification/2-Domains.md:164` says split-out detail files repeat "the relevant level-2 section heading".
- `md-ddl-specification/7-Sources.md:25` says "`## Sources` is a domain section like `## Entities` or `## Enums`". Line 30 and line 67 put `## Sources` at level 2 in detail files, and `1-Foundation.md:116` repeats this.
- Every example follows both rules at once: `domain.md` uses `## Source Systems` (e.g. `examples/Financial Crime/domain.md:122`) and every source file uses `## Sources` (e.g. `examples/Financial Crime/sources/salesforce-crm/transforms/table_account.md:3`). So the level-2 heading in a source detail file never matches the domain section it belongs to.

§7:40 says parsers locate content "by heading hierarchy, not by path". The two-layer discovery structure is one of the few things `1-Foundation.md:40` reserves **must** for. As written, a reassembler cannot join `## Sources` detail to the `## Source Systems` summary without a special case.

**Recommended fix:** pick one name for the level-2 section, use it in §1, §2, §7 and §9, then run one pass over the examples. Alternatively, state in §2 that `## Sources` in detail files is the detail-level name of the `## Source Systems` section. Either way, the linter's heading-hierarchy logic should enforce whichever is chosen.

---

## Major findings

### S2 — Source `status` has no defined vocabulary

- The source metadata example uses `status: Production` (`md-ddl-specification/7-Sources.md:101`, `:453`), and so do all 7 example sources (e.g. `examples/Financial Crime/sources/salesforce-crm/source.md:25`, `examples/Healthcare/sources/hospital-ehr/source.md:28`, `examples/Telecom/sources/bss-oss/source.md:24`, `examples/Brownfield Retail/sources/pos-system/source.md:22`).
- §7 defines vocabularies for `change_model` and `data_quality_tier` but has no table for `status`.
- The only lifecycle vocabulary in the spec is `Draft | Active | Deprecated | Retired`, used for domains (`2-Domains.md:244`) and products (`9-Data-Products.md:147`). `Production` is not in it.
- Consequence: `agents/agent-governance/skills/compliance-audit/SKILL.md:128` rates an invalid `status` as **Critical**. It is undefined whether a source's `Production` is invalid.

**Fix:** define the source `status` vocabulary in §7, or align it with the lifecycle vocabulary, and update the §7 examples and the 7 example files to match.

### S3 — The review prompts write to a gitignored `review.md`, contradicting CLAUDE.md

- `CLAUDE.md:70-71`: "The `.prompts/` files contain the prompts for each layer of review. Each prompt already includes the correct output path instruction."
- In fact:
  - `.prompts/md-ddl-review-prompt.md:20`: "Write the findings to the review.md file"
  - `.prompts/md-ddl-adversarial-review-prompt.md:12`: same
  - `.prompts/md-ddl-evaluation-prompt.md:23`: same, and `:1251` compares against "a previous `review.md`"
  - `.github/agents/review-md-ddl.agent.md:46`: "Write findings to `review.md`"
- `.gitignore:208` ignores `review.md`, so a reviewer following the prompts produces output that is never committed. This contradicts the `roadmap/review/YYYY-MM-DD-…` rule at `CLAUDE.md:52-62`.

**Fix:** change the four instructions to `roadmap/review/<YYYY-MM-DD>-layer<N>-….md`. Either remove `review.md` from `.gitignore` or keep it deliberately as a scratch file and say so.

### S4 — The Layer 1/2/3 prompts predate Agent Test and the current spec

- `.prompts/md-ddl-review-prompt.md:4` says "five AI agents" (there are six). The required reading list at `:28-34` and the ownership lens at `:59-76` omit Agent Test entirely.
- `.prompts/md-ddl-review-prompt.md:142-144` checks that "baselines have mapping blocks". `10-Adoption.md` (Baseline File Header) now says "Baseline files carry no `mapping:` blocks".
- `.prompts/md-ddl-adversarial-review-prompt.md:22-24` says "All 5 agent files" and omits agent-test. Line `:109` says the pre-flight set grew "to 12 rules"; there are 14 (see "Clean areas").
- `.prompts/md-ddl-evaluation-prompt.md:14` says "a standard at Draft 0.9.0". Its reading list at `:48-78` omits `agents/agent-test/**`, `agent-ontology/skills/lifecycle`, `agent-artifact/skills/{faker,dbt-project}`, `agent-architect/skills/architecture`, and `examples/Simple Customer`. There is no Agent Test scenario section; the sections at `:427-719` cover five agents.
- Grep confirms: `agent-test`/`Agent Test` occurs 0 times in the Layer 1, Layer 2 and orchestration prompts, and once in the Layer 3 prompt.

**Fix:** add Agent Test and its skills throughout, remove version literals (reference `1-Foundation.md` instead), and update the brownfield checks to match §10.

### S5 — `.github/copilot-instructions.md` is materially stale

- **Repository layout (`:24-115`).**
  - Agent Test is missing, both from `agents/` and from the wrapper list at `:93-100`.
  - Agent Artifact lists 5 skills (`:70-75`); disk has 7 plus `dialects/` and `references/generation-semantics.md`. `faker` and `dbt-project` are missing.
  - Agent Ontology lists 8 skills (`:58-66`); disk has 10. `lifecycle` and `preflight` are missing.
  - `src/`, `scripts/`, `roadmap/`, `.claude/` and `agents/CONVENTIONS.md` are absent.
- **Agent responsibilities table (`:224-230`):** no Agent Test row, although `:268` says new agents must be added to it.
- **Shared skills (`:248-257`):** only `regulatory-compliance` is listed. `dbt-project` and `faker` are shared with Agent Test (`agents/agent-test/AGENT.md:35-36`), and `domain-review`'s Model Readiness Definition is read by Artifact and Test.
- **`:328`:** "There are exactly 5 checks (YAML syntax, Mermaid syntax, internal link integrity, entity reference consistency, domain version field)." `guides/validation-tooling.md:36-68`, `agents/agent-ontology/skills/preflight/SKILL.md` and `src/md_ddl/lint.py` all define 14 rule ids.
- **`:370`:** "There is no build system … or via a linter if one is added." A linter, a PyPI package and a release workflow now exist.
- **`:205` vs `:215-218`:** it forbids workspace-root paths, then tells skill authors to write "Load md-ddl-specification/3-Entities.md". See S8.

**Fix:** regenerate the layout and tables from disk, fix the check count (or point to the guide rather than restating it), and state the path convention once.

### S6 — README and examples README carry false or incomplete claims

- **Unimplemented claim.**
  - `README.md:173`: Financial Crime has "generated artifacts".
  - `examples/README.md:119`: "Generated physical artifacts | ✓ (3NF JSON, Dimensional SQL)".
  - `examples/Financial Crime/generated/` does not exist, is ignored by `.gitignore` ("Generated Financial Crime physical model outputs"), and `git log` shows it was never committed.
- **Brownfield Retail omitted.**
  - `README.md:168` says "Five reference domains", and the table at `:170-176` omits Brownfield Retail, while the layout at `:204-211` lists 7 examples.
  - `examples/README.md:9-16` and the whole feature matrix (`:25-119`) omit Brownfield Retail. The adoption features (`adoption:` block, baselines, `batch-daily`) therefore have no row.
- **Coverage matrix out of date.** It has no rows for features added in 0.9–0.10: Entity Fan-Out, fan-in worked examples, `deduplication`, `lookup`, `reconciliation`, contributions/`when_absent`, and Agent Test coverage. It can't serve as the "maps every spec feature" claim at `README.md:178`.

**Fix:** remove the generated-artifacts claims (or commit a generated sample), add Brownfield Retail to both tables, correct the count, and extend the matrix to the §7/§8 features.

### S7 — Four incompatible project layouts are documented

Where | Layout
--- | ---
Spec (`1-Foundation.md:73-89`, `7-Sources.md:44-53`) | `domains/customer/entities/…`, and `sources/` **inside** the domain folder ("The source layer belongs to the domain", `7-Sources.md:25`)
`README.md:139-162` | `domains/customer/{domain.md,entities/,products/}` but `sources/` at the **project root**, with `source.md` + `transforms/`
`md-ddl init` instructions (`src/md_ddl/cli.py:71-86`) | `domains/` and a top-level `entities/` as siblings
`scripts/start-project.sh:141-150`, `scripts/start-project.ps1:95-100,144-149` | Same as `cli.py`: top-level `entities/`

The spec says file layout is the author's choice. Even so, the README and the generated `CLAUDE.md`/`copilot-instructions.md` are the first thing a new project sees, and they disagree with the spec's own illustrations and with each other.

**Fix:** pick one illustrative layout and use it in all four places. The spec's domain-rooted layout is the only one consistent with §7:25.

### S8 — Repo-root paths in shipped prompts don't resolve in consumer projects

- In a consumer project the standard lives at `.md-ddl/`. The wrapper rewrite (`cli.py:28-31`, `start-project.sh:59-60`) fixes only the wrappers, not the AGENT.md or SKILL.md bodies.
- There are 107 backticked `agents/…`, `md-ddl-specification/…`, `guides/…` or `examples/…` references inside `agents/`. For example:
  - `agents/agent-artifact/AGENT.md:10` (`agents/agent-ontology/skills/domain-review/SKILL.md`)
  - `agents/agent-architect/AGENT.md:39,74`
  - `agents/agent-ontology/AGENT.md:51-52`
  - every "MD-DDL Reference" block in the ontology skills (e.g. `entity-modelling/SKILL.md:13-16`)
- Other references in the same files are file-relative (`../CONVENTIONS.md`, `../agent-artifact/skills/dbt-project/SKILL.md` in `agents/agent-test/AGENT.md:35`, `references/…`). No file states which base the root-style paths are relative to.
- `.github/copilot-instructions.md:205` forbids workspace-root paths; `:215-218` prescribes them.
- An agent with search tools will often recover, but structurally the cited path does not exist.

**Fix:** declare the base once (e.g. in `agents/CONVENTIONS.md` and the Foundation include preamble: "paths beginning `agents/`, `md-ddl-specification/`, `guides/`, `examples/` are relative to the MD-DDL root, `.md-ddl/` in an installed project"), or convert them to file-relative. Then reconcile the two contributor rules.

### S9 — Regulator files trip Agent Governance's own staleness rule

- `agents/agent-governance/AGENT.md:35-37`: if a regulator file's `last_verified` is "more than 12 months old, tell the user and ask them to confirm".
- 12 of 13 files in `agents/agent-governance/skills/regulatory-compliance/regulators/` carry `last_verified: 2025-03-08` (`apra.md:3`, `basel.md:3`, `ccpa.md:3`, `eba.md:3`, `fatf.md:3`, `fdic.md:3`, `federal-reserve.md:3`, `gdpr.md:3`, `hipaa.md:3`, `occ.md:3`, `rbnz.md:3`, `sox.md:3`). That is 18+ months before this review. Only `austrac.md:3` (2026-09-29) is current.
- As shipped, every compliance audit outside AUSTRAC opens with a staleness warning.

**Fix:** re-verify the files before v1, or record the re-verification. Whether their content is still correct is outside Layer 1.

### S10 — No automated tests or PR-time CI for the package and repo invariants

- `git ls-files` contains no test suite for `src/md_ddl/` (`lint.py` is 1,752 lines; `cli.py` 367; `includes.py` 88). The only test-named file is the Faker template `agents/agent-artifact/skills/faker/runtime/test_template.py`.
- `.github/workflows/publish.yml` triggers only on `release` and `workflow_dispatch`. Its smoke test lints only `Simple Customer` (`publish.yml:83`).
- Nothing checks the following on push or PR: lint of all examples, `MD-DDL-Complete.md` regeneration parity, dead links, include resolution in the source tree, or the Python 3.9 floor. Each passes today (see "Clean areas") only because they were run manually.
- The action versions (`actions/checkout@v7`, `setup-python@v7`, `upload-artifact@v7`, `download-artifact@v8`) could not be verified from here (see "What I Cannot Evaluate").

**Fix:** add a PR workflow that runs lint on every example, a concat-parity check, `md-ddl check` on the source tree, and a small unit-test suite for the lint rules (one fixture per rule id, for both error and warning tiers).

### S11 — No spec changelog

- There is no `CHANGELOG.md` or version-history section anywhere outside `roadmap/`. `dd3923e` bumped every section header from `Draft 0.9.2` to `Draft 0.10.0` with no recorded list of rule changes. The rule changes are in `0bbbcb9`, `c1215a8`, `de08db5`, `dcdcdd4`: contributions/`when_absent`, survivorship `timestamp_field`, `fallback: reject`, fan-in example requirements, and others.
- `.github/copilot-instructions.md:161` defines when a version bump is required but nowhere to record it.
- The standard asks domains to keep `LIFECYCLE.md`/CHANGELOG (`guides/lifecycle-versioning.md:52-63`) but does not do so itself.

**Fix:** add a spec changelog before 1.0, backfilled at least from 0.9.x, and decide whether the "Draft" label and the `Development Status :: 4 - Beta` classifier (`pyproject.toml:29`) change at 1.0.

### S12 — Agent Guide routes to an agent that isn't installed

- `agents/agent-guide/AGENT.md:69` lists **review-md-ddl** in the Agent Directory as a destination.
- `src/md_ddl/cli.py:22-24` and `scripts/start-project.sh:110` / `.ps1:110` deliberately don't install that wrapper in consumer projects. There is no Claude slash command for it at all (`.claude/commands/` has only the six agents).
- The Guide's own workflow and Concept Explorer steer review requests there (`AGENT.md:53-54`).

**Fix:** remove the row, or mark it "source repository only". Alternatively, route consumer review requests to Agent Ontology (Domain Review) and Agent Governance.

---

## Minor findings

- **S13. Example source layout differs from the §7 convention.** §7 (`7-Sources.md:44-59`) illustrates `sources/sources.md` for summaries and `sources/<system>/table_<SOURCE_CASING>.md` ("Match the source system's own casing"). Every example instead uses `sources/<system>/source.md` and `sources/<system>/transforms/table_<lowercase>.md` (see `find examples -path '*sources*'`). §2's own example uses both forms: `2-Domains.md:105-106` links to `sources/sources.md#…`, while `2-Domains.md:302` links to `sources/salesforce-crm/source.md` with no anchor, although `:94` says the link targets "the source's summary heading". This is allowed, since layout is author's choice, but the quality benchmark doesn't show the convention the spec describes. **Fix:** align one example to the convention, or change the convention.

- **S14. `batch` is used as a change model but isn't in the vocabulary.** The §7 vocabulary is `batch-daily | batch-intraday` (`7-Sources.md:114-121`). Feeds rows use `batch` at `examples/Healthcare/sources/hospital-ehr/source.md:47-50` and `examples/Telecom/sources/bss-oss/source.md:42`. Financial Crime correctly uses `batch-intraday` (`sap-fraud-management/source.md:55`). `examples/README.md:88` claims "`change_model: batch`" for Financial Crime, Healthcare and Telecom. No example sets a batch `change_model:`; only Brownfield Retail (`batch-daily`, absent from the matrix) does.

- **S15. The §2 example has structural slips.** In `2-Domains.md:294-305` the example domain file puts `### Domain Overview Diagram` after `## Source Systems`, which makes it a child of that section. Elsewhere (`:127`, and all examples, e.g. `examples/Financial Crime/domain.md:38`) it sits under `## Metadata`.

- **S16. The same rule is stated in two spec sections.** The one-mapping-path constraint appears at `7-Sources.md:312` and `8-Transformations.md:493`, near-verbatim ("two rules must not write the same attribute"). It is also restated in `agents/agent-ontology/skills/source-mapping/SKILL.md:161`. This goes against `.github/copilot-instructions.md:143` ("edit the owning section only"). **Fix:** keep it in §8 and link to it from §7.

- **S17. §9 lineage wording is inconsistent.** `9-Data-Products.md:149` and `:210` say consumer-aligned lineage is from canonical **entities**. `:229` says consumer-aligned products "source exclusively from canonical (domain-aligned) **products**". These may be meant as the same thing, but as written they name different objects. This is flagged for Layer 2; it is not a structural fix.

- **S18. Dead section name.** `agents/agent-ontology/AGENT.md:117-118` cites "Entity Modelling skill, Governance Authoring Protocol". The heading is `## Governance While Authoring` (`agents/agent-ontology/skills/entity-modelling/SKILL.md:102`).

- **S19. A reference stub is missing.** `agents/agent-guide/skills/concept-explorer/SKILL.md:30` lists `10-Adoption.md`, but `concept-explorer/references/` has stubs only for §1–§9. `agents/agent-guide/AGENT.md:36-37` tells the Guide to load from that directory first.

- **S20. An agent rule has no normative source.** `agents/agent-ontology/AGENT.md:86` states "Mermaid diagrams use the ELK layout engine" as a rule. The spec has no ELK requirement; it appears only in example YAML at `7-Sources.md:151`. The non-normative guide makes it conditional: "for complex graphs" (`guides/diagram-style.md:36`).

- **S21. Severity language conflicts with the validation philosophy.** `agents/agent-governance/skills/compliance-audit/SKILL.md:128` rates an invalid `status` **Critical**. The review brief and `.github/copilot-instructions.md:327` treat vocabulary deviations as observations. S2 makes this concrete, because source `status` has no vocabulary.

- **S22. Stale wrapper descriptions.**
  - `.github/agents/agent-artifact.agent.md:3-4` describes only "dimensional star schemas, normalized 3NF designs, SQL DDL, JSON Schema, and Parquet", with hint "(dimensional/3NF)". It omits wide-column, knowledge graph/Cypher, dbt, Faker, reconciliation and dialects.
  - `.github/agents/agent-ontology.agent.md:3` omits source mapping, brownfield import/baselines, lifecycle and preflight.
  - Copilot uses these descriptions for agent selection.

- **S23. The Copilot wrappers don't work in this repo.** Every `.github/agents/agent-*.agent.md:10` includes `../../.md-ddl/agents/…`. This repo has no `.md-ddl/`, so Copilot contributors here get empty agents. `src/md_ddl/includes.py:30-34` acknowledges this by marking `.github` inert. **Fix:** document it in the contributor guidance, or provide a dev symlink.

- **S24. A stale exclusion.** `src/md_ddl/cli.py:24`, `scripts/start-project.sh:57` and `scripts/start-project.ps1:59` exclude a `review.md` slash command that doesn't exist in `.claude/commands/`.

- **S25. Dead FHIR links.** `agents/agent-ontology/skills/standards-alignment/standards/fhir/resources.md:111` links `operations.html` and `resources-detail.md:1188` links `terminologies.html`. Both are relative links copied from FHIR descriptions. **Fix:** strip the links or make them absolute to hl7.org.

- **S26. Dead links in the roadmap.** `roadmap/v1/completed/plan-brownfieldAdoption.prompt.md:639-648` has 9 `../../md-ddl-specification/…` and `../../agents/…` links that need `../../../`. This is historical and not packaged.

- **S27. PyPI rendering.** `pyproject.toml:9` uses `README.md` as the long description. Its relative links (`README.md:11,69,172-178`) resolve on GitHub but not on pypi.org. **Fix:** use absolute GitHub URLs for links that matter on the PyPI page.

- **S28. Stale counts and paths in the contributor guide.**
  - `.github/copilot-instructions.md:337` says "17 blog posts"; `references/architecture/` has 18 dated posts plus 3 external references and 7 diagrams.
  - `:255` cites `industry_standards/bian/` etc. The actual paths are `references/industry_standards/…`, and the distilled references are under `agents/agent-ontology/skills/standards-alignment/standards/`.
  - `:111-114` names only Financial Crime as the reference example, which is fine, but lists two files as the reference set.

- **S29. Claude.ai Projects integration is undocumented.** `.prompts/md-ddl-review-prompt.md:161-162` asks whether README integration covers "VS Code Copilot, Claude Code, and Claude.ai Projects". Neither `README.md` nor `agents/agent-guide/skills/platform-setup/SKILL.md` mentions Claude.ai Projects (grep: 0 hits). Either document it or drop it from the prompt.

- **S30. Regeneration needs PowerShell.** `.prompts/concat-md-ddl-specs.prompt.md:5` and `.github/copilot-instructions.md:153` offer only the PowerShell script. The file is byte-identical to a fresh regeneration today. A Python equivalent (or a `md-ddl` subcommand) would let the CI parity check from S10 run on Linux.

---

## Clean areas: what was checked and found consistent

- **Version strings.** All 10 section headers read `Draft 0.10.0` (`md-ddl-specification/*-*.md:1`), as do `README.md:5`, `src/md_ddl/__init__.py:17` and the `MD-DDL-Complete.md:1` header. No `Draft 0.9` remains outside `.prompts/md-ddl-evaluation-prompt.md:14` (S4) and `roadmap/`. No agent, guide or example file carries a spec version string. Example domains carry their own domain versions, which is correct.
- **`MD-DDL-Complete.md`.** It is byte-identical to a Python re-implementation of `scripts/concat-md-ddl-specs.ps1` over sections 1–10. It has no `...next:` lines, and every section heading is present.
- **Stale names.** There are no `data_products/` folder references outside one external blog URL (`references/architecture/BIAN Coreless Banking vs Data Autonomy.md:99`). `Production` status is covered under S2.
- **`{{INCLUDE}}` directives.** All 44 in the payload directories resolve (`md_ddl.includes.unresolved` returns `[]`). All are file-relative. After `md-ddl init`, 50 directives resolve, including the wrappers.
- **Packaging.**
  - The wheel builds and contains 322 files, no `__pycache__`/`.pyc`, and no `examples/Financial Crime/generated/`.
  - `md-ddl init --name demo` installs 6 Claude commands and 6 Copilot wrappers and correctly excludes `review-md-ddl.agent.md`. It rewrites the Claude paths to `.md-ddl/`, and `md-ddl check` passes.
  - The package imports and `lint` runs under Python 3.9.23.
  - `DOCS_PAYLOAD` (`src/md_ddl/__init__.py:37-43`) matches `pyproject.toml:65-73` force-include and `CLAUDE.md:47`.
- **Wrappers.** `.claude/commands/` and `.github/agents/` each have exactly one wrapper per agent (6 agents), plus the internal `review-md-ddl.agent.md`. The agent tables in `CLAUDE.md:13-20`, `cli.py:44-57` and both bootstrap scripts agree. They are duplicated four times, though, which is debt.
- **Skill indexes vs disk.** Every `SKILL.md` path in all six `AGENT.md` Skills tables exists, and every `skills/*/SKILL.md` on disk is indexed by its agent (28 skills). `agent-artifact/skills/dialects/` has no `SKILL.md` by design: it is data referenced at `agent-artifact/AGENT.md:43-45`. All `SKILL.md` files are under 500 lines (max 444, `product-design`). All have frontmatter with `name` matching the directory and one `description`.
- **Cross-agent shared paths.** These all exist:
  - `agents/CONVENTIONS.md` with a "Handoff Protocol" section
  - `domain-review` "Model Readiness Definition"
  - `9-Data-Products.md` "SLA Declaration"
  - `source-mapping` "The Determinism Test"
  - `3-Entities.md` "Governance Metadata Schema"
  - all 13 regulator files named in `regulatory-compliance/SKILL.md:15-24`
  - every `file.md § Section` reference across agents, guides and spec
- **Dead links.** No dead relative links or anchors in `agents/` (except S25), `guides/`, `md-ddl-specification/` (including `MD-DDL-Complete.md`), `examples/`, `README.md`, `CLAUDE.md`, `.github/`, `.claude/` or `.prompts/`. Placeholder links inside inline code were excluded on purpose.
- **Examples.** `md_ddl_lint.py` reports "no findings" for all 7 examples. None uses list-style `- name:` attributes, `logic:` constraints, relationships without `type:`/`granularity:`, entities without `existence`/`mutability`, or detail H1s that fail to link back to the domain.
  - **Brownfield Retail** has an `adoption:` block (`domain.md:45-55`). All 5 baseline files carry `type`, `source_system`, `captured_date`, `captured_by` and `status: active`, and none has `superseded_by` or `mapping:` blocks, which matches §10. `maturity: mapped` agrees with 3 canonical entities plus source transforms.
  - **Cross-domain product names** cited in the matrix resolve to real headings.
- **Validation model.** The rule set agrees across `1-Foundation.md:122-126`, `guides/validation-tooling.md:36-68`, `agents/agent-ontology/skills/preflight/SKILL.md:84-100` and `src/md_ddl/lint.py`: 14 rule ids, same names, with the same error and warning split. The one outlier is copilot-instructions (S5). `domain-review/SKILL.md:12` states "contextual quality review, not a lint pass", and `:315` bans error language for Levels 3–5.
- **Architecture.** The 13 tenets match between `agents/agent-architect/skills/architecture/SKILL.md:80-92` and `.github/copilot-instructions.md:341-353`. The six stubs in `architecture/references/` include all 21 `.md` files under `references/architecture/` (the 7 diagram conversions are not included directly; they are inlined in posts).
- **Rule duplication audit.** Five rules were sampled:
  - No FK attributes: `3-Entities.md:369`, paraphrased in `agent-ontology/AGENT.md:82` and `entity-modelling/SKILL.md:130`.
  - `identifier: primary`: paraphrased with rationale in `agent-ontology/AGENT.md:83-85`.
  - Consumer-aligned lineage: `9-Data-Products.md:229,434-436`, paraphrased in `agent-architect/AGENT.md:76-80`.
  - ELK: S20.
  - One-mapping-path: S16.
  - Only S16 is near-verbatim and it sits across two spec sections. The agent restatements are paraphrases that name the spec, which is acceptable.
- **Lifecycle boundary audit.** The Boundaries tables in all six `AGENT.md` files hand off consistently. Overlaps are declared explicitly as shared, not silent:
  - Ontology owns worked examples; Test may only draft them as proposals (`agent-test/AGENT.md:81-82`, `agent-ontology/AGENT.md:107,115`).
  - Artifact and Test share `dbt-project` and `faker` with an ownership table.
  - Governance recommends product fixes and Architect applies them (`agent-governance/AGENT.md:102`, `agent-architect/AGENT.md:101-104`).
  - There are no undeclared overlaps. The one structural boundary defect is S12.

---

## What I Cannot Evaluate

- **Whether any rule is correct.** Layer 1 checks that rules are stated consistently, not that they are right. S1, S2 and S17 need a design decision, not just an edit.
- **Semantic accuracy of examples.** Whether the Financial Crime, Healthcare and Telecom models match real AML, FHIR or TM Forum practice, and whether BIAN, FHIR and TM Forum references are accurate, is not assessed. The distilled standards files (`standards-alignment/standards/**`, about 60% of `agents/` by size) were only link-checked.
- **Regulatory content.** S9 is a date check only. I did not verify any retention period, notification timeframe or obligation in the regulator files.
- **Agent behaviour.** Whether the prompts produce correct output, load the right skills, or recover from the root-path problem in S8 at runtime needs Layer 2/3 or live agent runs. I did not execute any agent.
- **Copilot `{{INCLUDE}}` processing and Claude Code slash-command behaviour on real platforms.** I verified the files and paths, not platform rendering.
- **GitHub Actions validity.** I could not confirm that `actions/checkout@v7`, `actions/setup-python@v7`, `actions/upload-artifact@v7` and `actions/download-artifact@v8` exist, or that the PyPI Trusted Publisher is configured. The workflow was not run.
- **PyPI state.** I did not compare the published 0.10.0 artifact on pypi.org with the local build.
- **Mermaid rendering.** The linter checks diagram type declarations, not full Mermaid grammar. I rendered no diagrams.
- **Anchor semantics inside `MD-DDL-Complete.md`.** Duplicate headings across sections (e.g. "Splitting Across Files" in §2 and §7) get `-1` suffixes. I checked that anchors exist, not that each resolves to the intended occurrence.
- **Windows behaviour** of `start-project.ps1` and `concat-md-ddl-specs.ps1`. PowerShell was not run.
- **Subjective quality**, learnability and stakeholder fit are out of scope for Layer 1 by design.

---

## Suggested agenda for next spec version (pre-1.0)

**Fix existing (v1 blockers):**

1. Settle the Sources level-2 heading name (S1) and define the source `status` vocabulary (S2). Update §1/§2/§7/§9 and all examples in one pass.
2. Bring the review tooling up to date: the output path (S3) and Agent Test coverage, versions and §10 checks (S4). Then run Layers 2 and 3 against 0.10.0 with the corrected prompts.
3. Regenerate `.github/copilot-instructions.md` from disk (S5), and declare the path base for agent prompts (S8).
4. Correct the README and examples README claims and tables (S6). Unify the documented project layout across the spec, README, `cli.py` and the bootstrap scripts (S7).
5. Re-verify the regulator files (S9), and fix the Agent Guide's review routing (S12).
6. Add PR-time CI and linter unit tests (S10), a spec CHANGELOG, and a decision on the "Draft" label and Beta classifier at 1.0 (S11).

**Fix existing (non-blocking):** S13–S30. Most are single-line edits. S16 (dedupe the one-path rule) and S14 (the `batch` vocabulary) are worth doing in the same pass as item 1.

**Extend capability (not a Layer 1 finding, noted for the roadmap):**

- A domain-level declaration of which spec version a model targets. There is currently no field for it, which matters once 1.x revisions start.
- A single source for the agent table, which is currently duplicated in `CLAUDE.md`, `cli.py`, `start-project.sh` and `start-project.ps1`.
