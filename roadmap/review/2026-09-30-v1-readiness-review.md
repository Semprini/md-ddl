# MD-DDL v1.0 Readiness Review

**Date:** 2026-09-30
**Scope:** Specification (Draft 0.10.0), agents, guides, examples, and the `md-ddl` Python package (0.10.0, tag `v0.10.0` at `02e39f7`)
**Lens:** What does a 1.0 promise, and is the project ready to keep that promise?
**Out of scope:** Link checking, structural consistency, and adversarial spec semantics. Another reviewer covers those.

---

## Executive Summary

**Verdict: not ready for 1.0.** The package installs and works for the path it was built around. The spec's register has improved a lot since the July complexity review. But the project can't yet make the four promises a 1.0 carries:

1. **The spec is stable.** It isn't yet. Five of the features named in the brief (`when_absent`, product `consistency`, survivorship `earliest`, `abstract: true`, and fan-in worked examples) entered the spec on 2026-09-29. So did the settled `contributes: true` semantics. Twenty-eight of the repository's 97 commits landed on 29–30 September. Only one example (Financial Crime) exercises the new semantics.
2. **Breaking changes follow a declared policy.** There is no policy. No spec versioning policy, deprecation policy, changelog, release notes, migration guide, or governance or contribution process exists. A model also has no way to declare which MD-DDL version it targets.
3. **Adopters can tell whether a model conforms.** They can't. The spec never defines conformance. It uses the term "validation error" in eight places without saying which validation tier reports it. The reference linter answers "no findings" for models that plainly break the spec: two of the seven shipped examples, and the project layout the README recommends.
4. **The tooling is tested and supported.** There are no automated tests and no CI on pull requests. The linter crashes with a traceback on an attribute named `Yes` or `No`, and its checks depend on folder names in ways the spec explicitly disclaims.

There are **7 must-fix items**. Most are S–M effort. The largest cost is calendar time: a release-candidate soak for the features added on 29 September.

### Must-fix before v1 (summary)

ID | Finding | Effort
--- | --- | ---
V1-01 | No spec versioning, compatibility, deprecation or governance policy; no changelog or migration notes; models can't declare a target version | M
V1-02 | No conformance definition; "validation error" is undefined; the normative-language policy is declared but not applied | M
V1-03 | Linter has zero automated tests and no PR CI; it crashes on YAML 1.1 boolean or integer keys | M
V1-04 | Linter coverage depends on folder names; the README's recommended layout gets no source-layer linting at all | M
V1-05 | Recently added spec features haven't soaked; no release candidate | S (plus time)
V1-06 | Shipped examples don't conform but lint clean (Healthcare, Telecom source layers; Brownfield Retail `identifier: true`) | M–L
V1-07 | CC BY 4.0 covers the Python code too; no patent, trademark or name-use terms for the standard | S

---

## Method

- Read `CLAUDE.md`, `README.md`, `pyproject.toml`, `.github/workflows/publish.yml`, all of `src/md_ddl/`, `md-ddl-specification/1-Foundation.md`, `guides/validation-tooling.md`, `guides/lifecycle-versioning.md`, the three roadmap reviews named in the brief, and `roadmap/v2/*.md`.
- Grepped the spec for normative keywords and draft markers.
- Used git history to date feature introductions.
- Built the sdist and wheel from a clean clone with `python -m build`. Installed the wheel into fresh venvs and ran the README quickstart.
- Ran the linter on every example, on Python 3.9, 3.10, 3.11, 3.13 and 3.14 (rc2) via `uv`.
- Built about 30 edge-case fixtures in the scratchpad: empty dir, no domain, binary and empty `domain.md`, malformed YAML/JSON/Mermaid, deleted entity file, unicode names, CRLF, UTF-8 BOM, backslash paths, renamed folders, README layout, and a YAML shape fuzz.

No repository files were modified other than this report.

---

## 1. Spec Normativity & Stability

### Evidence

**Normative keywords.** The spec has no RFC 2119 / BCP 14 declaration.

- Uppercase keywords: `MUST` appears once (`6-Events.md:119`). `SHOULD`, `MAY` and "conform" appear zero times.
- Lowercase counts across sections 1–10: `must` 81, `should` 25, `may` 68, `required` 28, `optional` 26.

**The policy exists but isn't applied.** `1-Foundation.md:40` reserves **must** for "rules whose violation breaks AI interpretation", and says naming, file layout and table columns are conventions. The sections contradict it:

- `3-Entities.md:377`: "Entity and attribute names **must** use natural language". The Foundation lists naming as a convention.
- `9-Data-Products.md:249, :442`: every product with a `schema_type` "**must** include a Mermaid class diagram". Diagrams are renderings; the July complexity review recommended "recommended, not required".
- `9-Data-Products.md:500-523` (Multi-Domain Governance Conflict Resolution): "must be resolved explicitly … not permitted", "highest wins". This is organisational policy that the July review (action 6 and the governance-patterns guide) said to relocate. It is still normative.
- `6-Events.md:119`: the only uppercase `MUST` in the spec. It sits beside lowercase `must`, and nothing says whether the two differ.

**No conformance definition.**

- Nothing defines a "valid" or "conforming" MD-DDL model, a conforming generator, or a conforming validator.
- The July review's own target structure says "the core defines what a *valid* model is" (`2026-07-25-standard-complexity-review.md:214`). That definition was never written.
- The spec calls several things a "validation error" but never says which tier reports them:
  - `7-Sources.md:552`: a feed table without a transform.
  - `7-Sources.md:558`: an undeclared fan-out.
  - `8-Transformations.md:54` and `:499`: an abstract target without a fan-out.
  - `8-Transformations.md:325`: an undeclared predicate field.
  - `8-Transformations.md:421`: a worked example that disagrees with the fan-out.
- None of these is implemented in the linter. The Foundation's Tier 1 list doesn't include them, and the Tier 2 agents aren't named as the enforcers.

**Draft markers.** The spec proper has no TODO, TBD or FIXME. Every section heading reads "Draft 0.10.0". Agent content carries open markers:

- `agents/agent-ontology/skills/standards-alignment/standards/bian/README.md:14`: v14 "not yet populated".
- FHIR terminology rows carrying upstream "TODO" descriptions (`fhir/terminology.md:35-36`). These are upstream data, so harmless.

**Feature churn.** Dates of first appearance, from `git log -G` on `md-ddl-specification/[0-9]*.md`:

Feature | First in spec
--- | ---
`when_absent` | 2026-09-29 (`0bbbcb9`)
product `consistency:` | 2026-09-29 (`c1215a8`)
survivorship `earliest` | 2026-09-29 (`c1215a8`)
`abstract: true` | 2026-09-29 (`c1215a8`)
Fan-in worked examples | 2026-09-29 (`dcdcdd4`)
`contributes: true` (settled semantics) | 2026-09-29 (`de08db5`)
`survivorship`, `evaluation`, Open Decisions | 2026-08-03 (`2579670`)

Commit cadence: 24 commits on 2026-09-29 and 4 on 2026-09-30, out of 97 total. A whole agent (Agent Test) and a shared dbt skill were added on 29 September. `git diff --stat v0.9.2 HEAD` shows +644/−60 across the spec, guides and linter.

**Other normativity gaps.**

- *YAML version.* The spec doesn't say which YAML version applies. PyYAML (the reference linter) implements YAML 1.1, where `Yes`, `No`, `On` and `Off` are booleans, `1.0` is a float, and dates become `date` objects. See V1-03 and S-05 for the concrete consequences.
- *JSON and PlantUML.* `1-Foundation.md:17` allows "YAML or JSON blocks" and "Mermaid or PlantUML". The tooling validates neither JSON detail blocks nor PlantUML (see S-03 and S-10).

---

## 2. Versioning & Compatibility Policy

### Evidence

**What is missing.**

- No `CHANGELOG`, release notes or migration guide anywhere. `ls CHANGELOG* CONTRIBUTING* SECURITY* CODE_OF_CONDUCT* GOVERNANCE*` finds nothing.
- `roadmap/` holds plans and reviews, not release notes.
- `LIFECYCLE.md` exists only as a convention for *models*. There is one instance, `examples/Financial Crime/LIFECYCLE.md`.

**Model versioning vs spec versioning.** `guides/lifecycle-versioning.md` is thorough, but it covers the versioning of *a user's domain*, and it is explicitly non-normative (line 3). Nothing describes versioning of *the standard itself*:

- what a spec major, minor or patch change means;
- whether a 1.x model stays valid under 1.y;
- how long deprecated constructs are honoured;
- whether adding a Tier 1 lint rule counts as a breaking change.

That last question matters. 0.10.0 added two error-severity rules (`transform-target-resolve`, `transform-case-values`). `guides/validation-tooling.md:36` and `:84` still call the check set "fixed and closed". An adopter's CI that passed on 0.9.2 can fail on 0.10.0 with no model change.

**Breaking changes shipped without notes.** Between 0.9.2 and 0.10.0 the product folder convention changed from `data_products/` to `products/` (commit `5df7160`), and Financial Crime jumped to domain 2.0.0. The spec gives no upgrade notes.

**Models can't declare a target version.** No `md_ddl_version`, `spec_version` or equivalent key exists in the spec (grep of spec, guides, agents and examples). Agents therefore can't tell a 0.9-era model from a 1.0 model. The Healthcare and Telecom source layers are exactly this case (see V1-06).

**Spec version and package version are the same number.**

- The spec heading says `Draft 0.10.0`, the README says `Version 0.10.0`, and `src/md_ddl/__init__.py` has `__version__ = "0.10.0"`.
- Nothing states whether a linter bug fix (package 1.0.1) means spec 1.0.1.
- The package also ships agents, which change far faster than the grammar.

**Release process.** Tags exist remotely for `v0.9.2` and `v0.10.0`. Publishing is via Trusted Publishing on GitHub release (`publish.yml`), which is good. The bootstrap scripts, however, add the submodule at `main` (`scripts/start-project.sh:40`), and the README's `curl | bash` pulls `main`. Submodule adopters therefore track unreleased work.

---

## 3. Tooling Quality

### 3.1 Tests and CI

- **No automated tests.** There is no `tests/` directory and no `conftest.py`, pytest config, tox or nox. The only `test_*.py` is `agents/agent-artifact/skills/faker/runtime/test_template.py`, a template shipped to users.
- **No CI on PRs.** `.github/workflows/` contains only `publish.yml`, which triggers on `release: published` and `workflow_dispatch`.
- **Release smoke test is thin.** `publish.yml`:
  - lints only `".md-ddl/examples/Simple Customer"`, so a regression in any of the other six examples, or a false positive the linter introduces, would publish;
  - runs its matrix on Python 3.9 and 3.13 only, while the classifiers claim 3.9–3.14;
  - uses floating action tags, and `pypa/gh-action-pypi-publish@release/v1` is not SHA-pinned.
- **Dependencies.** `pyyaml>=5.1` is the only dependency. The lower bound is never tested.

### 3.2 Quickstart

The README quickstart works.

- `pip install <wheel>` followed by `md-ddl init` in an empty directory unpacks `.md-ddl/`, writes both wrapper sets, `CLAUDE.md` and `.github/copilot-instructions.md`, and reports "Verified 50 include directives resolve."
- `md-ddl check` exits 0.
- `md-ddl lint ".md-ddl/examples/Simple Customer"` exits 0.
- The linter passes on every example (all seven, individually and as `examples/`, with and without `--strict`) on Python 3.9.23, 3.10.20, 3.11.15, 3.13.12 and 3.14.0rc2.

Two first-run rough edges:

- `md-ddl lint .` in the freshly initialised project exits **2** with `error: no domain.md found in or under .`. The quickstart doesn't mention this, and a new project's CI fails on it.
- `.md-ddlignore` defaults to `.md-ddl/` and `venv/` only. With a `.venv/` in the project (the PyPA and uv default), `md-ddl lint .` walks `site-packages` and lints the eight packaged example domains. This was confirmed by breaking the installed copy's `version:`, which gave `.venv/lib/python3.11/site-packages/md_ddl/docs/examples/Simple Customer/domain.md:7 error domain-version`.

### 3.3 Linter edge cases (scratchpad fixtures)

Case | Result | Assessment
--- | --- | ---
Empty dir / dir with no `domain.md` / nonexistent path | stderr message, exit 2 | OK
Empty or binary `domain.md` | 1 error + 1 warning, exit 1 | OK
Malformed YAML block | `yaml-syntax` error at correct line, exit 1 | OK
Entity detail file deleted | 8 errors; `transform-target-resolve` says "entity 'Appointment' is **not declared in this domain**" although it is in the Entities table | Misleading message
CRLF line endings | clean | OK
UTF-8 BOM (Windows editors) | **false error**: `entity-heading-link: detail file has no level-1 heading` | Bug (reads with `utf-8`, not `utf-8-sig`, `lint.py:260`)
Backslash in link (`.\details.md`) | error | Acceptable
**Attribute key `Yes`, `No`, `On`, `Off` or an integer** | **Traceback** `AttributeError: 'bool' object has no attribute 'lower'` at `lint.py:197` via `lint.py:1470`; exit 1, the same code as "errors found" | Crash
Enum value `No` (unquoted) + conditional case key `"No"` | **false error** `transform-case-values: case value 'No' is not a valid enum 'Loyalty Tier' value` | YAML 1.1 bug
`attributes: null` / list / scalar YAML | "no findings", even though the diagram lists attributes the YAML lacks | Silent pass
`extends: 7` | no `entity-references` error; warns "inherited from '7'?" | Silent pass
**Unicode entity name** (`Präferenz Kunde`) plus an extra YAML attribute missing from the diagram | only a warning "no class named … found"; the attribute mismatch is **not reported**. The ASCII control reports `entity-attribute-consistency` error | False negative. The id regexes are ASCII-only (`lint.py:410, 415, 498, 504`)
Invalid Mermaid body under a valid `classDiagram` keyword | clean | `mermaid-syntax` checks only the first keyword (`lint.py:787`)
Malformed ```` ```json ```` block in a detail file | clean | JSON is checked only in domain metadata (`lint.py:1265`)
**README layout** (`domains/customer/` and `sources/crm/` as siblings), with a YAML syntax error, a broken link and a misspelt target in the source file | `lint .` gives **"no findings", exit 0**. Linting the file directly gives "no domain.md found above", exit 2 | Silent pass on the documented layout
**Domain's `sources/` folder renamed** to `integration/` (the spec says layout is free) | **12 false `entity-references` errors**, and the real target typo is **missed**. The control with `sources/` catches it | Path-coupled rules

The spec says "Parsers and linters locate content by heading hierarchy, not by path, so no particular directory structure is required" (`7-Sources.md:40`). The implementation contradicts this: `NON_ENTITY_REF_DIRS = {"sources", "products", "baselines"}` (`lint.py:109`), and transform checks run only when `rel_parts[0] == "sources"` (`lint.py:1569`). The layouts in `README.md` ("Suggested project layout") and `1-Foundation.md:84-89` place `sources/` beside `domains/`, which the linter never visits. `7-Sources.md:44-52` places it inside the domain.

### 3.4 CLI quality

- `md-ddl --help` and `md-ddl lint --help` are clear.
- `--list-rules` doesn't show each rule's severity, although some rules emit both severities.
- `lint --help` doesn't document exit codes or `.md-ddlignore`. The module docstring does, but argparse doesn't show it.
- The module docstring (`lint.py:5-6`) cites a nonexistent `linter.md`.
- `--disable nope` gives exit 2 with a clear message. `--format xml` gives exit 2. Good.
- A crash exits 1, so CI can't tell a crash from findings.

### 3.5 Spec Tier 1 promise vs linter

Foundation Tier 1 item (`1-Foundation.md:122`) | Linter rule(s) | Gap
--- | --- | ---
YAML syntax | `yaml-syntax` | YAML only; JSON detail blocks unchecked
Mermaid syntax ("Mermaid renders", `validation-tooling.md:25`) | `mermaid-syntax` | Diagram-type keyword only; the body is never parsed. PlantUML is unsupported
Internal link integrity | `link-resolve` | Only under a folder containing `domain.md`
Entity reference consistency | `entity-references`, `transform-target-resolve` | Path-coupled; false positives if folders are renamed
Domain `version:` present | `domain-version` | OK
Diagram / tables / YAML agreement | `domain-diagram-coverage`, `domain-table-coverage`, `domain-link-consistency`, `entity-*` | ASCII identifiers only; entity diagrams only under `## Entities`
*(not in Tier 1 list)* | `transform-case-values` | Added in 0.10.0 while the set is described as "closed"
Spec "validation errors" (`7-Sources.md:552, 558`; `8-Transformations.md:54, 325, 421, 499`) | none | Unassigned to a tier

---

## 4. Project Hygiene

Item | Status | Note
--- | --- | ---
LICENSE | CC BY 4.0 for everything, including `src/md_ddl/*.py` (`pyproject.toml:15` `license = "CC-BY-4.0"`) | Creative Commons advises against CC licences for software. There's no patent grant, and nothing protects the "MD-DDL" name, so anyone can publish a modified "MD-DDL 1.0". Contributors today are one maintainer plus Claude and Copilot commits (`git log`), so relicensing is cheap now and expensive after external contributions
CONTRIBUTING | missing | The spec invites "potential spec contributions" (`1-Foundation.md:40, 126`) but gives no channel
Governance of the standard | missing | Who decides, how to propose (RFC or issue), review period, versioning authority
SECURITY | missing | Relevant: agents execute generated code (B8 resolution) and read untrusted source schemas (prompt-injection surface); the package runs `shutil.rmtree` inside `.md-ddl/` on re-init
CODE_OF_CONDUCT, issue/PR templates | missing | `.github/` has no `ISSUE_TEMPLATE/` or PR template
README accuracy | mostly accurate | "Five reference domains" table (`README.md:168`) omits Brownfield Retail, though the repository layout lists seven examples. Quickstart doesn't cover the empty-project `lint` exit 2
Classifier | `Development Status :: 4 - Beta` | Must change at 1.0. Python 3.9 has been EOL since Oct 2025; decide whether 1.0 keeps it
Duplicated setup text | `cli.py:_instructions`, `start-project.sh`, `start-project.ps1` each carry their own copy of the agent table and instructions | Drift risk. The scripts also don't create `.md-ddlignore`
`MD-DDL-Complete.md` | in sync on spot checks (`when_absent`, `earliest`, `abstract: true`, `cardinality: 0`, `Reference: <Entity>`) | Regeneration relies on an AI prompt plus a PowerShell script; no CI diff check

---

## 5. Agent Layer Stability

- **No evaluation harness.** `roadmap/review/2026-09-29-agent-behaviour-tests.md` was a one-off manual run: one session per agent, a single scenario, all against Financial Crime, graded by hidden checks. It found 11 instruction defects (B1–B11), including a regulatory factual error (B1). None of it is repeatable. The checks aren't stored as data, the scenarios aren't scripted, and no release gate re-runs them. `.prompts/` holds review prompts for the *spec*, not agent regression tests.
- **Agent behaviour changes fast.** 30 `SKILL.md` files and 6 `AGENT.md` files (761 lines) were substantially rewritten in PR #14 and the 29 September fixes. A 1.0 needs to say whether agent behaviour is inside the stability promise.
- **Platform integration claims are unverified.**
  - `guides/validation-tooling.md:113` states that `{{INCLUDE}}` "is processed by the AI platform (e.g. VS Code Copilot custom agents, Claude Code)".
  - The B6 fix contradicts this for Claude Code: the wrappers now *tell the model* to read include targets (`.claude/commands/agent-test.md:1`).
  - The Copilot wrappers (`.github/agents/*.agent.md`) consist almost entirely of an `{{INCLUDE}}`. If Copilot doesn't expand it, the agent works only because the model chooses to read the file.
  - `md-ddl check` verifies that the paths resolve, not that any platform expands them.
- **Wrapper consistency.** The wrappers are consistent: six agents in each of `.claude/commands/`, `.github/agents/`, `cli.py:AGENTS` and the bootstrap scripts, all including `agent-test`. `cli.py:24` lists a `review.md` in `INTERNAL_WRAPPERS` that doesn't exist; this is harmless. `--ai` supports only `claude|copilot|both`.

---

## 6. Known Open Items — Disposition

Item (source) | Disposition | Rationale
--- | --- | ---
Healthcare and Telecom source layers use the pre-spec layout: source-rooted H1, `## <Table>` instead of `## Sources`, a `Comment` column, no fan-out or worked examples, `fallback: Active` (behaviour-tests "Remaining"; confirmed: `examples/Healthcare/sources/hospital-ehr/transforms/table_appointment.md:1-3`, 0 files with `Entity Fan-Out` or `Worked Examples` across both) | **Blocks v1** (V1-06) | The package ships these examples and agents learn from them. They lint clean, which shows the conformance gap directly
`rbnz.md` re-verification (behaviour-tests "Remaining") | Should-fix before v1 announcement, not a blocker | Reference content, not grammar. Add a visible "last verified 2025-03-08" caveat now
BIAN v14 migration (`roadmap/v2/plan-bianV14Migration.prompt.md`) | Can wait (v1.x) | Blocked on external API access. v13 is labelled the production baseline. Make sure the plan's claim "defaults to v14 for new work" (line 19) doesn't leak into agent guidance, which currently says use v13
Declarative Governance agent suite (`roadmap/v2/plan-declarativeGovernance.prompt.md`) | Can wait (v2) | New capability, not stabilisation
Complexity review action 4: apply the normative-language policy | **Blocks v1** (part of V1-02) | Deciding what is "must" *is* the 1.0 contract. Loosening later is compatible; tightening later is breaking
Complexity review: relocate multi-domain governance conflict rules and remaining generation guidance | Decide normative status before v1; the physical move can be v1.x | Removing normative text after 1.0 is a compatible loosening, but it has to be decided first
Complexity review internal inconsistencies (identifier, Source Systems table, plurality, `.github/` path) | Mostly resolved in spec. `identifier: true` survives in `examples/Brownfield Retail/entities/{product,store,sale}.md` | Fold into V1-06
B11 follow-ons: more mechanical checks for spec "validation errors" | Classify before v1 (V1-02); implement in v1.x | 

---

## Findings

### Must-fix before v1

#### V1-01 — No versioning, compatibility, deprecation or governance policy for the standard

- **Area:** Versioning / governance
- **Evidence:** No CHANGELOG, release notes, migration guide, CONTRIBUTING or GOVERNANCE file. `guides/lifecycle-versioning.md` covers user domains only and is non-normative. No model-level target-version key. Spec, package and agent versions are all one number (`__init__.py:17`, spec headings, `README.md:5`). 0.10.0 changed the folder convention (`data_products/` to `products/`) and added error-level lint rules with no upgrade notes. Submodule bootstrap tracks `main`.
- **Why it matters:** "1.0" is a promise about what happens at 1.1 and 2.0. Without a written policy, the promise can't be kept or checked.
- **Fix:**
  1. Add `md-ddl-specification/0-Versioning.md` or a `GOVERNANCE.md`. It should define: semver for the grammar, where a 1.x model stays valid under 1.y; what counts as breaking (new required keys, new error-level lint rules, narrowed vocabularies); and deprecation (announce in minor N, remove no earlier than the next major).
  2. Decouple versions: spec `1.0`, package `1.0.x`, and state that agents and skills are versioned with the package but outside the grammar's compatibility promise.
  3. Add an optional domain metadata key, e.g. `md_ddl: "1.0"`, which agents and the linter read.
  4. Start `CHANGELOG.md`, with a 0.9 to 1.0 migration section.
  5. Pin the bootstrap scripts to the latest release tag.
  6. Write a short governance statement: who decides, how to propose (issue template), and how long changes stay open for comment.
- **Effort:** M
- **v1 blocker:** Yes

#### V1-02 — Conformance is undefined, and the normative-language policy isn't applied

- **Area:** Specification
- **Evidence:** Zero occurrences of "conform". No RFC 2119 statement. `must` is used 81 times, including for conventions the Foundation says are not musts (`3-Entities.md:377`, `9-Data-Products.md:249/442/500-523`). A lone uppercase `MUST` (`6-Events.md:119`). Eight "validation error" statements not assigned to Tier 1 or Tier 2.
- **Why it matters:** Adopters, tool vendors and auditors need to know what "valid MD-DDL 1.0" means, and who (linter or agent) decides it.
- **Fix:**
  1. Add a "Conformance" section to `1-Foundation.md`:
     - A *conforming model* passes every Tier 1 check and satisfies every **must**.
     - A *conforming validator* implements the Tier 1 list exactly.
     - Everything else is convention.
  2. Adopt BCP 14 wording (or state explicitly that lowercase is normative).
  3. Sweep the spec against the policy, one pass per section.
  4. Label each "validation error" as Tier 1 (with a lint rule id, current or planned) or Tier 2 (agent review).
  5. Declare YAML 1.2 semantics, or require quoting of `Yes`/`No`/`On`/`Off` and version strings.
- **Effort:** M
- **v1 blocker:** Yes

#### V1-03 — Reference linter is untested and has no PR CI; crashes on common YAML

- **Area:** Tooling
- **Evidence:** No tests (§3.1). Only `publish.yml`, which runs on release, and its smoke test lints one example. The traceback on an attribute named `Yes`/`No`, or an integer key (`lint.py:197` via `:1470`), exits 1 and looks like "findings". The YAML 1.1 false positive on enum value `No`. Behaviour-tests B11 added two rules and a false-positive fix on 29 September with no regression tests.
- **Why it matters:** The linter *is* the executable definition of Tier 1 conformance. At 1.0, a false positive breaks adopters' CI, and a false negative certifies non-conformant models.
- **Fix:**
  1. Add a `tests/` pytest suite:
     - one fixture per rule, covering its pass, error and warning paths;
     - every example must lint clean;
     - the edge cases in §3.3.
  2. Stringify YAML keys safely (`normalise(str(k))`) everywhere. Better, load YAML with a YAML 1.2-style resolver, or a `SafeLoader` subclass without the bool/float implicit resolvers for keys and values.
  3. Exit 3 on an internal error, with a friendly message.
  4. Add `.github/workflows/ci.yml` on `pull_request`: pytest on 3.9–3.14, lint all examples, check `MD-DDL-Complete.md` is up to date, and run `md-ddl check` in a fresh `init`.
  5. Make the release smoke test lint all examples.
- **Effort:** M
- **v1 blocker:** Yes

#### V1-04 — Linter coverage depends on folder names; the recommended layout is silently skipped

- **Area:** Tooling / spec alignment
- **Evidence:** The README and Foundation layout gives "no findings", exit 0, with a YAML error, a broken link and a bad target in `sources/`. Renaming a domain's `sources/` gives 12 false errors and misses the real one (§3.3). The code keys on `lint.py:109` and `:1569`, while `7-Sources.md:40` promises that linters locate content "by heading hierarchy, not by path". The README layout also contradicts `7-Sources.md:44-52` on where `sources/` lives.
- **Why it matters:** An adopter following the README gets a green check on a broken model. That is the worst failure mode for a conformance tool.
- **Fix:**
  1. Pick one canonical layout and make the README, the Foundation and 7-Sources agree.
  2. Classify files by their H2 section (`## Sources`, `## Data Products`, `## Entities`) rather than their parent folder name.
  3. Let `md-ddl lint .` discover source and product files that link to a domain via their H1, even when they live outside the domain folder.
  4. Report `.md` files that belong to no domain as a warning, instead of passing them silently.
- **Effort:** M
- **v1 blocker:** Yes

#### V1-05 — Recently added spec features haven't soaked

- **Area:** Specification stability
- **Evidence:** Feature table in §1. 28 of 97 commits landed on 29–30 September. Only Financial Crime exercises fan-in, `contributes`, `when_absent`, `earliest` and `abstract`. Its source layer was "rebuilt" on 29 September and then changed again by two follow-up reviews the same day.
- **Why it matters:** Features frozen into 1.0 can only change by major bump. Semantics settled in a single day by AI review, with one exemplar, is the pattern most likely to need breaking revision.
- **Fix:**
  1. Cut `1.0.0rc1` and hold a public comment window (e.g. 4–6 weeks).
  2. During it, exercise the new constructs in at least one more example (Healthcare or Telecom; see V1-06) and one real adopter model.
  3. Alternatively, mark these constructs "provisional in 1.0 (may change in 1.x)" in the spec, and have the linter and agents surface them as such.
- **Effort:** S (plus calendar time)
- **v1 blocker:** Yes

#### V1-06 — Shipped examples don't conform to the spec but lint clean

- **Area:** Examples
- **Evidence:**
  - Healthcare and Telecom source layers: H1 links to `../source.md`, not the domain; `## Appointment` instead of `## Sources`; no fan-out or worked examples; `fallback: Active` (`examples/Healthcare/sources/hospital-ehr/transforms/table_diagnosis.md:31`, `table_location.md:43`, `table_care_plan.md:30`).
  - `examples/Brownfield Retail/entities/{product,store,sale}.md` use `identifier: true`, which is not in the `primary|alternate|natural|surrogate` vocabulary (`3-Entities.md:301`).
  - All of these pass `md-ddl lint`.
- **Why it matters:** The examples ship in the wheel (`pyproject.toml` force-include) and are what agents and users copy. At 1.0 they are de facto normative.
- **Fix:**
  1. Rebuild the Healthcare and Telecom source layers the way Financial Crime was rebuilt.
  2. Correct Brownfield Retail.
  3. Alternatively, stop packaging them and mark them "pre-1.0, non-conforming" until rebuilt.
  4. Add linter coverage for the source-file H1 link, so this class of drift is caught.
- **Effort:** M–L
- **v1 blocker:** Yes

#### V1-07 — Licensing unsuited to code and to a standard

- **Area:** Legal / hygiene
- **Evidence:** `LICENSE` is CC BY 4.0. `pyproject.toml:15` gives `license = "CC-BY-4.0"` for the Python package. There's no patent or name-use statement.
- **Why it matters:** Enterprise artifactory intake, the README's stated distribution path, routinely flags CC licences on code. CC BY gives no patent grant, and without name-use terms any fork can call itself "MD-DDL 1.0". Relicensing is cheap only while contributors are few (today: one maintainer plus AI commits).
- **Fix:**
  1. Dual-license: CC BY 4.0 for the spec, guides and examples; Apache-2.0 (patent grant) or MIT for `src/`, `scripts/` and the agent runtime `.py` files.
  2. Update `pyproject.toml` to an SPDX expression, e.g. `Apache-2.0 AND CC-BY-4.0`.
  3. Add a short name-use statement: only the maintainers' releases may be called "MD-DDL x.y".
  4. Take legal advice if an organisation will sponsor the standard.
- **Effort:** S
- **v1 blocker:** Yes

### Should-fix (before or soon after 1.0)

ID | Area | Evidence | Why it matters | Fix | Effort | Blocker
--- | --- | --- | --- | --- | --- | ---
S-01 | Linter | Unicode entity or class names bypass `entity-attribute-consistency` (§3.3). The id regexes are ASCII-only (`lint.py:410, 415, 498, 504`) | The spec mandates natural-language naming, and non-English adopters get false negatives | Use `[\w]` with `re.UNICODE`; add a test | S | No
S-02 | Linter | A UTF-8 BOM gives a false `entity-heading-link` error (`lint.py:260` reads `utf-8`) | Windows editors add BOMs | Read with `utf-8-sig` | S | No
S-03 | Linter | Malformed ```` ```json ```` detail blocks pass. `1-Foundation.md:17` allows JSON as an alternative to YAML | A Tier 1 hole | Parse JSON blocks under `yaml-syntax` (or a new `json-syntax` rule) | S | No
S-04 | Linter / docs | `mermaid-syntax` checks only the first keyword (`lint.py:787`). The guide says "Mermaid renders" (`validation-tooling.md:25`) | Overclaims Tier 1 coverage | Rename or re-describe the rule honestly, or add an optional `mmdc`-based check | S | No
S-05 | Linter / spec | YAML 1.1 coercion: a false positive on enum value `No` versus case key `"No"`; `version: 1.0` parses as a float | Silent semantic drift between the linter, agents and generators | Covered by V1-02/V1-03, plus a spec note to quote such scalars | S | No
S-06 | CLI | `.md-ddlignore` defaults omit `.venv/`, `.git/` and `node_modules/`, so `md-ddl lint .` lints `site-packages` (§3.2) | A future example regression breaks every adopter's CI | Add those defaults, and skip any path containing `site-packages` | S | No
S-07 | Tooling policy | New error rules break CI with no opt-in (0.10.0 added two). The guide still calls the set "closed" | Compatibility | Introduce new rules as warnings for one minor release before promoting them; add `--rules <version>` or document the policy | S | No
S-08 | CLI | `--list-rules` omits severity; `lint --help` omits exit codes and `.md-ddlignore`; the docstring cites nonexistent `linter.md`; misleading "not declared in this domain" when only the detail file is missing | Supportability | Add an epilog and a severity column; fix the messages | S | No
S-09 | Packaging / CI | Classifier is `4 - Beta`. CI covers only 3.9 and 3.13 while 3.14 is claimed. The `pyyaml>=5.1` floor is untested. Action tags float | 1.0 signal and supply chain | Set `5 - Production/Stable`; widen the matrix; add a min-deps job; SHA-pin actions | S | No
S-10 | Spec / tooling | PlantUML is allowed by `1-Foundation.md:17` but unsupported: a domain with PlantUML only gets a "no overview diagram" warning and no consistency checks | Promise the tooling can't keep | Drop PlantUML from 1.0, or scope it as "not mechanically validated" | S | No
S-11 | Agents | No repeatable agent evaluation. The 2026-09-29 run found 11 defects, including a regulatory factual error | Agents are first-class, and prompt edits regress silently | Store the 2026-09-29 scenarios and hidden checks as data (e.g. `evals/<agent>/<case>.yaml`); add a scripted runner (Claude Agent SDK or `claude -p`) that grades YAML parse, lint pass and key assertions; make it a release checklist item | M | No, if V1-01 scopes agent behaviour out of the compatibility promise
S-12 | Agents / docs | `validation-tooling.md:113` claims platforms process `{{INCLUDE}}`. The B6 fix shows Claude Code doesn't, and Copilot's support is unverified | The agent layer's loading mechanism rests on an unverified claim | State that the directive is a *convention the model is instructed to follow*; verify with each platform; record findings | S | No
S-13 | Hygiene | No SECURITY.md, CODE_OF_CONDUCT or issue/PR templates | Standard 1.0 expectations; agents execute code and read untrusted inputs | Add all four; SECURITY.md should cover prompt injection via source schemas and generated-code execution | S | No
S-14 | README | "Five reference domains" table omits Brownfield Retail. Nothing explains the empty-project `lint .` exit 2 | First-run confusion | Update the table; add a "your first domain" step | S | No
S-15 | Scripts | Agent table and instructions are duplicated in `cli.py`, `start-project.sh` and `start-project.ps1`. The scripts don't create `.md-ddlignore` | Drift between the pip and submodule flows | Have the scripts call `md-ddl init`-equivalent logic, or generate them from one template | S | No
S-16 | Spec | `9-Data-Products.md:500-523` multi-domain governance policy, and the remaining generation guidance, are still normative | The July review said relocate | Decide normative status now (V1-02); move the text in v1.x | M | No
S-17 | Reference data | `rbnz.md` last verified 2025-03-08, including the AML/CFT s.58 retention cited by Financial Crime | Regulatory claims shipped in a 1.0 | Re-verify, or add a visible staleness caveat | S | No

### Can wait (v1.x / v2)

ID | Item | Why it can wait
--- | --- | ---
C-01 | BIAN v14 migration (`roadmap/v2/plan-bianV14Migration.prompt.md`) | Externally blocked; v13 is the labelled baseline; additive when it lands
C-02 | Declarative Governance agent suite (`roadmap/v2/plan-declarativeGovernance.prompt.md`) | New capability
C-03 | Machine-readable JSON Schema for every YAML block type (entity, relationship, transform, product), published with the spec | High value for third-party tooling, but additive. Use `additionalProperties: true` to respect the deviations-are-observations philosophy
C-04 | Mechanical checks for the remaining spec "validation errors" (feed table vs transforms, fan-out declared, predicate fields declared, worked example vs fan-out) | Classification must happen before v1 (V1-02); implementation can follow in minors, as warnings first (S-07)
C-05 | More AI platforms for `md-ddl init --ai` (Cursor, Codex `AGENTS.md`, Gemini) | Additive
C-06 | Linter handles named files whose nearest ancestor `domain.md` is unrelated (`_find_domain_file` walks to the filesystem root, `lint.py:1641`) | Edge case

---

## Recommended Path to 1.0

1. **Policy first (V1-01, V1-02, V1-07).** Write the versioning, governance and conformance text and fix the licence. This is mostly writing, and it sets the rules for everything else.
2. **Tooling hardening (V1-03, V1-04, S-01–S-08).** Write the tests first, then fix the bugs they expose. Add PR CI.
3. **Examples (V1-06).** Rebuild Healthcare and Telecom, which also exercises the new constructs (V1-05).
4. **Cut `1.0.0rc1`**, with a changelog, migration notes and a comment window. Run the agent scenarios (S-11) against the rc.
5. **Release 1.0.0** when the window closes with no breaking change requests outstanding.

---

## What This Review Cannot Assess

- **Real adopter experience.** No external adopter models were available. The quickstart and linter were exercised only against the shipped examples and synthetic fixtures.
- **Agent behaviour.** No agent was run for this review. The agent-layer assessment rests on the 2026-09-29 behaviour tests and on reading the prompts. Whether agents interpret the new constructs (`contributes`, `when_absent`, fan-in) consistently across sessions and models is an empirical question.
- **Platform `{{INCLUDE}}` semantics.** Whether VS Code Copilot custom agents expand `{{INCLUDE: ...}}` could not be verified from this environment (S-12).
- **GitHub Actions versions.** `actions/checkout@v7`, `setup-python@v7`, `upload-artifact@v7` and `download-artifact@v8` were not verified against the Actions marketplace. The release workflow was not executed.
- **Windows and macOS behaviour.** Only Linux was tested. Path handling on Windows (drive letters, `\` in `.md-ddlignore` patterns, long paths under `.md-ddl/`) is unverified beyond the release smoke matrix.
- **Legal adequacy.** The licensing finding (V1-07) is an engineering observation, not legal advice.
- **Spec semantics and cross-document consistency.** Deliberately out of scope; covered by the parallel structural and adversarial reviews.
- **The PyPI artifact itself.** The wheel was rebuilt from a clean clone at HEAD. The published 0.10.0 artifact on PyPI was not downloaded or compared.
- **AI-evaluating-AI limits.** This review was produced by an AI reading a largely AI-authored repository. Shared blind spots may apply, especially around tolerance for YAML-heavy formats and underweighting human learnability.
