# Path to v1.0: Consolidated Review

**Date:** 2026-09-30
**Reviewed:** spec Draft 0.10.0, `md-ddl` 0.10.0 (commit `02e39f7`)
**Inputs:** four reviews run in separate sessions, following `.prompts/md-ddl-layered-review-process.md`

Review | Lens | Report
--- | --- | ---
Layer 1: Structural | Is the repository internally consistent? | [layer1-structural-review](2026-09-30-layer1-structural-review.md) (S1–S30)
Layer 2: Adversarial (run on a different model) | What would break, fail, or mislead? | [layer2-adversarial-review](2026-09-30-layer2-adversarial-review.md) (L2-01–L2-23, L2-M1–M12)
Layer 3: Stakeholder | Would real adopters adopt and stay? | [layer3-stakeholder-review](2026-09-30-layer3-stakeholder-review.md) (N1–N11, B1–B9)
v1 readiness | What does a 1.0 promise, and can the project keep it? | [v1-readiness-review](2026-09-30-v1-readiness-review.md) (V1-01–07, S-01–17, C-01–06)

Before consolidating, I checked the following claims against the files: S1 (heading names), L2-04 (masking names), L2-10 (Rule 8 and the role identifiers), the `normalise()` crash (V1-03), and the licence (V1-07). All were confirmed.

---

## Verdict

**MD-DDL is not ready for 1.0, but the gap is mostly finite and known.** The agent suite's boundary design is a real strength: all layers agree, and Layer 3 scored it highest across 39 scenarios. The worked-example-to-dbt-unit-test idea was executed and works.

What's missing is what a 1.0 promises. There is no written compatibility promise. The tooling can't yet be trusted to give a true green. The examples break the spec's own rules. The features added on 29 September haven't been exercised beyond one example, and that example doesn't fully comply.

Recommended route: **four workstreams, then `1.0.0rc1` with a comment window, then 1.0.0.** See [Plan](#plan).

---

## 1. Cross-layer agreement (highest confidence)

These were found independently by two or more reviews.

\# | Issue | Found by | v1?
--- | --- | --- | ---
A1 | **Documented layout ≠ linted layout.** Four layouts are documented. The layout that `md-ddl init` writes into `CLAUDE.md` makes the linter silently skip entity files. The README layout skips source files. The linter keys on folder names, although §7 says it locates content by heading. | S7, V1-04, N1 (reproduced by two reviews) | **Block**
A2 | **No versioning or compatibility policy, and no changelog.** A model can't declare its target version. A team can't pin the MD-DDL version its agents run. "Breaking" is defined so that every additive change is breaking. | S11, V1-01, L2-17, N4 | **Block**
A3 | **The linter has no tests and there's no PR CI.** It crashes on YAML keys `Yes`/`No`. It has silent holes (the ASCII `.` target separator, `.venv/` not ignored, Unicode names, BOM). The release smoke test lints one example. | S10, V1-03, S-01/02/06, N2 | **Block** (tests, CI, crash). The other holes are cheap and should be fixed too.
A4 | **The examples break the spec.** | V1-06, L2-04/09/10/11/13/23, N6, S6, S14 | **Block** (see §4)
A5 | **Features added on 29 September haven't soaked,** and downstream agents don't implement them. Agent Artifact, Agent Test and generation-semantics don't mention `contributes`, `when_absent`, `earliest` or product `consistency`. | V1-05, L2-02, L2-19, workflows score 2.7/5 | **Block** (see Contradiction C2 for scope)
A6 | **Regulator files are stale by the agent's own rule.** 12 of 13 are dated 2025-03-08. | S9, S-17, B7 | **Block** (cheap)
A7 | **CC BY 4.0 on the Python code,** with no name-use terms. | V1-07, B2 | **Block** (cheap now, costly later)
A8 | **Copilot `{{INCLUDE}}` expansion is unverified.** Unlike the Claude wrappers, the Copilot wrappers don't tell the model to read the include. | S-12, B8, S23 | **Verify before v1**
A9 | **No conformance definition.** "Validation error" appears 8 times with no tier assigned. The normative-language policy isn't applied (81 lowercase "must"). | V1-02, L2-M8 | **Block** (Layer 3 ranks it below A1; see C5)
A10 | **No generated reference output anywhere.** The README claims Financial Crime has "generated artifacts", which were never committed. There is no regression baseline for agent changes. | S6, N3, S-11 | **Block** (at minimum, correct the claim; see C6)

## 2. Single-layer findings that should still block v1

These are grammar or normative text that can only be tightened by a major bump once frozen, or defects a first user hits.

ID | Issue | Why v1
--- | --- | ---
S1 | `## Source Systems` (§2) vs `## Sources` (§7). Every example uses both. | Heading names are the parse keys
S2, L2-M9 | Source `status:` has no vocabulary (everything says `Production`). Domains and entities have 5 status values; products have 4. | Vocabulary freeze
L2-01 | `references` is keyed by entity name, so two relationships to the same entity (debit and credit account, base and quote currency) can't be sourced. There is also no way to map relationship attributes or m:n links. Financial Crime silently omits 5 relationships. | Key shape freezes
L2-03 | Relationship `cardinality` has no defined vocabulary and no optionality. Foreign-key nullability can't be determined from the YAML. | Every generated FK
L2-04 | `masking` can name attributes that don't exist. Transaction Risk Summary masks "Date of Birth" but publishes "Payer Date of Birth" in clear. | The one control applied to generated output
L2-05 | No `precision`, `scale` or `max_length` properties, but the dialect files "map them from entity YAML". Money becomes `NUMBER(38,0)`. | First-day rejection by engineers (Layer 3 B5)
L2-06 | Domain `pii` is defined as "any entity" but inherited as "every entity". Subtype governance inheritance is unstated. | Normative definition
L2-07 | "Longest retention wins" can't express a maximum. The Governance agent gives three contradictory instructions. | Normative rule; needs a compliance SME
L2-08 | Multi-domain conflict detection compares domain defaults only. Both cross-domain flagship products list the wrong regulatory scope (BSA, EU AMLD and PATRIOT instead of AUSTRAC, NZ AML/CFT and CPS 234). | Normative rule plus a visible example error
L2-09 | "Consumer products source only from canonical products", but lineage can't name a product, and no domain-aligned product publishes Transaction or Account. | A stated "never" that the flagship breaks
L2-10 | Payer, Payee and Initiator roles repeat across payments with a `derived` identity. That breaks Rule 8, which I introduced on 29 September. | Flagship vs its own rule
L2-11 | The dedup key can merge unrelated addresses: city isn't in the key, and a null postcode becomes an empty string. Normalise order, delimiter escaping and scalar string forms are undefined. | Key-composition rules freeze
L2-15 | A source is identified three ways (`id`, folder name, table casing). The spec's own §7 and §9 examples disagree. | "Must match" reference keys
L2-20 | Agent Ontology says "every entity gets `identifier: primary`", which undoes the Financial Crime 2.0.0 fix. It's undefined whether a subtype inherits the key and what two primaries mean. Simple Customer, the starter, has two primaries. | Starter teaches a defect
S8 | 107 repo-root paths in agent prompts don't resolve in an installed project (`.md-ddl/`), and no path base is declared. | Every installed project
S12 | Agent Guide routes users to `review-md-ddl`, which isn't installed. | Dead route in a shipped prompt

## 3. Contradictions between layers, and how to resolve them

\# | Disagreement | Resolution
--- | --- | ---
C1 | Layer 2 says cross-domain references (L2-16) and valid-time mapping (L2-12) block v1 as "frozen grammar". Layer 3 says both are additive under semver, and adopters start with one domain. | **Layer 3 is right.** Defer to 1.x, but the 1.0 text must not forbid the future syntax, and should say it's planned. Lineage version pinning (part of L2-16) is also additive.
C2 | Layer 2 wants every multi-source reading settled (L2-02 a–f). Layers 3 and V1-05 warn that more same-day churn is itself a risk. | **Settle the four readings a generator hits immediately:** (a) re-emission by the establishing source merges per attribute; (b) disjoint contributions merge per attribute by default; (c) `hold` applies per entry, not per row; (e) absent `references` target, by adding `when_absent` to references. Mark `contributes`/`when_absent`/fan-in **provisional in 1.0** and leave (d) and (f) to 1.x. Then implement them in Agent Artifact and Agent Test (L2-19).
C3 | Layer 1 found handoffs consistent; Layer 2 found handoff defects (L2-18); Layer 3 says L2-18 is overstated because the primary handoff is the pasted block. | Fix the file-name mismatch (`handoff-to-artifact.md` vs `agent-artifact`). It's cheap and ships to users. Set `consumed` on completion. The one-pending rule can wait. **Not a blocker.**
C4 | Layer 1 made S3/S4 (stale review prompts writing to a gitignored `review.md`) blockers; Layer 3 says adopters never see `.prompts/`. | **Not an adopter blocker, but fix before the rc:** the rc sign-off reviews run from these prompts. This consolidation had to work around them.
C5 | V1-02 (conformance) is a blocker for readiness; Layer 3 says users trust the green lint, not the clause. | **Both matter; sequence them.** Fix the linter (A1, A3) first, then write the conformance section that describes what the linter enforces.
C6 | Layer 1 treats the missing generated output as a false README claim (S6); Layer 3 treats it as the engineer's evidence gap and the missing regression baseline (N3). | **Minimum for v1:** remove the false claim. **Recommended:** commit one reference output set for one example (DDL for one dialect, a dbt project with passing unit tests, an ODPS manifest), regenerated per release.
C7 | Layer 2 corrected Layer 1 S2: domain status has 5 values (with `Review`), not 4. | Layer 2 is right. Covered under S2/L2-M9.

## 4. Examples

The examples are what agents and users copy, so at 1.0 they are effectively normative.

Example | Before v1
--- | ---
Financial Crime | Fix L2-04 (masking), L2-10 (dedup roles or relax Rule 8), L2-11 (address key), L2-08 (scope union), L2-13 (Account path), L2-M5 (the old name "Instructing Agent"). Add `## Sources` / `## Source Systems` alignment and relationship sourcing (L2-01) once decided. Record unsourced attributes (L2-23).
Simple Customer | One primary identifier; relative links instead of upstream GitHub URLs; one attribute shape (N6).
Healthcare, Telecom | Rebuild their source layers to the 0.10 spec (V1-06). This doubles as the soak for the provisional features (V1-05), or stop packaging them until rebuilt.
Brownfield Retail | Replace `identifier: true`; refresh the stalled `target_date`; add it to the README and `examples/README.md` tables (S6, N8).
All | `batch` isn't a `change_model` value (S14). Correct "Five reference domains" and the generated-artifacts claim (S6).

## 5. Blind spots declared across all reviews

- **No agent was run** in any review. Agent behaviour is predicted from prompts. The last real run was on 2026-09-29, before these findings.
- **Regulatory correctness** wasn't assessed: L2-07, L2-08, L2-M11, the regulator files and the AML confidentiality question. **A compliance specialist should read these before the retention and conflict rules are rewritten.**
- **Real adopter models** weren't available. Everything was tested on shipped examples and synthetic fixtures.
- **Platform behaviour** (Copilot include expansion, Windows paths, GitHub Actions versions) wasn't verified.
- **The DuckLake local tier** couldn't be tested (its extension download was blocked). Plain DuckDB with dbt-core 1.12.5 worked.
- **AI evaluating AI.** Every review was an AI reading a largely AI-authored repository. The Layer 2 model differed from the authoring model, which helps but isn't independence. Human review of the grammar decisions in §2 is the one thing none of these reviews can substitute for.

---

## Plan

Four workstreams. W1 comes first because it sets the rules the others follow. W2–W4 can proceed in any order once W1's decisions are made.

### W1 — Policy and decisions (mostly writing; owner decisions needed)

1. **Versioning and compatibility policy** (`GOVERNANCE.md` or `0-Versioning.md`):
   - semver for the grammar: what counts as breaking, including new error-level lint rules;
   - a deprecation window;
   - separate spec and package versions;
   - agents versioned with the package but outside the grammar promise.
   (V1-01, L2-17)
2. **Fix the "breaking" definition** in §2 and the lifecycle guide (L2-17).
3. **Start `CHANGELOG.md`**, backfilled from 0.9.x, with a 0.x→1.0 migration section (S11).
4. **Target-version key and pinning.** Add an optional domain key `md_ddl: "1.0"`. `md-ddl init` records the installed version in a committed file, and `check`/`lint` warn on mismatch (V1-01, N4).
5. **Conformance section** in `1-Foundation.md`:
   - define a conforming model and a conforming validator;
   - assign each "validation error" to Tier 1 or Tier 2;
   - declare the YAML semantics (quote `Yes`/`No`/versions, or use YAML 1.2).
   (V1-02)
6. **Normative-language sweep:** "must" only where the Foundation reserves it (V1-02).
7. **Relicense:** CC BY 4.0 for the spec, guides and examples; Apache-2.0 (or MIT) for code; add a name-use statement (V1-07).
8. **CONTRIBUTING, SECURITY, issue templates** (S-13). SECURITY should cover prompt injection via source schemas and execution of generated code.

### W2 — Spec grammar (decide, then write; each is small once decided)

1. Rename one of `## Sources` / `## Source Systems` everywhere (S1). Define the source `status` vocabulary and align the three status vocabularies (S2, L2-M9).
2. Source keys: `id` for `source:` and lineage, and the heading text for tables (L2-15). Restate Rule 5 so that direct mappings count.
3. Relationship cardinality vocabulary with optionality (L2-03). Add `precision`/`scale`/`max_length`, and reconcile `timestamp`/`datetime` (L2-05).
4. Allow `references` to be keyed by relationship name. Add a link entry for m:n relationships and edge attributes (L2-01).
5. Settle the multi-source readings a, b, c, e and mark the fan-in constructs provisional (C2, L2-02, V1-05).
6. Dedup key rules: an all-null key rejects; define normalise order, delimiter escaping and scalar string forms; say whether `earliest` means by timestamp or by arrival (L2-11). Resolve Rule 8 for shared roles (L2-10).
7. Inherited and composite primary identifiers (L2-20).
8. Governance:
   - `pii` as the default, with the precedence chain domain → parent → child (L2-06);
   - masking entries must resolve to an attribute (L2-04);
   - retention minimum/maximum/anchor, and "surface, don't resolve" for conflicts, **after SME review** (L2-07);
   - conflict detection against each entity's effective governance (L2-08).
9. Consumer lineage: either it names a product, or the rule becomes "from canonical entities" (L2-09).
10. State which 1.x additions are planned: cross-domain references, valid time, repeating groups, `sourced: false` (C1).
11. Regenerate `MD-DDL-Complete.md`.

### W3 — Tooling (tests first)

1. Add a `tests/` pytest suite:
   - one fixture per rule, covering its pass, error and warning paths;
   - every example lints clean;
   - the readiness edge cases.
   (V1-03)
2. Add `.github/workflows/ci.yml` on PRs:
   - pytest on Python 3.9–3.14;
   - lint all examples;
   - check that `MD-DDL-Complete.md` matches a fresh regeneration (add a Python regenerator, S30);
   - run `md-ddl check` after a fresh `init`.
   Also make the release smoke test lint every example. (S10, V1-03)
3. Classify files by H2 section rather than folder name; lint the one documented layout fully; warn on orphan `.md` files (V1-04, N1). Make `cli.py`, the README, the Foundation and §7 show that one layout (S7).
4. Small fixes:
   - YAML key crash; exit code 3 for internal errors;
   - accept `.` as a target separator, or warn when a target can't be parsed (N2);
   - default-ignore `.venv/`, `.git/` and `node_modules/` (S-06);
   - read with `utf-8-sig`; Unicode identifiers (S-01, S-02);
   - validate JSON blocks (S-03);
   - add a masking-resolves rule (L2-04);
   - `--list-rules` shows severity (S-08).
5. Policy for new rules: ship them as warnings for one minor version before promoting to errors (S-07).
6. `init`: when `CLAUDE.md` or `copilot-instructions.md` already exists, print the block to paste (N5). Set the classifier to Production/Stable at 1.0 (S-09).

### W4 — Agents and examples

1. Implement the settled 0.10 semantics in `generation-semantics.md`, the dbt-project skill and Agent Test:
   - contributions, hold/reject, `earliest`, `references` to existing instances;
   - a seeding step for contributing-table examples;
   - per-row, subtype-aware Step 1 checks.
   (L2-19)
2. Fix the Ontology identifier rule (L2-20) and the Guide's dead route (S12). Declare the path base for repo-root paths (S8). Fix the handoff file naming (L2-18).
3. Re-verify the regulator files, or ship each with a visible "verification pending" note (S9).
4. Verify Copilot `{{INCLUDE}}` expansion. Add the Claude wrappers' "read the included file" line to the Copilot wrappers (A8).
5. Regenerate `.github/copilot-instructions.md` from disk (S5). Update the review prompts: Agent Test, output paths, no version literals (S3, S4).
6. Fix the examples as in §4. Commit one reference output set (C6).
7. Store the 2026-09-29 behaviour-test scenarios and checks as data, with a scripted runner. Run it on the rc (S-11).

### Release

1. Cut **`1.0.0rc1`** when W1–W4 are done. Open a 4–6 week comment window.
2. During the window, rerun the four reviews with the updated prompts and run the agent scenarios against the rc.
3. Release **1.0.0** once no breaking change requests remain.

### Can wait (1.x / 2.x)

- Cross-domain `extends`/relationships and lineage version pins (L2-16)
- Valid-time mapping (L2-12)
- Repeating groups (L2-21)
- The `hold` time bound (L2-22)
- `sourced: false` (L2-23)
- Traversal multiplicity (L2-13)
- The `check` expression language and `lifecycle_stage` (L2-14)
- FHIR polymorphism guidance (N10)
- Diagram render/fix tooling (N9)
- Brownfield scale playbook and a Level 3/4 exemplar (N8)
- DuckLake offline notes (N7)
- Guide analyst archetype (N11)
- JSON Schema for YAML blocks (C-03)
- More `--ai` platforms (C-05)
- BIAN v14 (C-01)
- Declarative Governance agents (C-02)
- The remaining Minor findings in all four reports

---

## Decisions needed from the owner

Each shapes a workstream and can't be settled by review:

1. **Licence.** Is Apache-2.0 (patent grant) or MIT right for the code, and should CC BY 4.0 stay for the spec? Is there a sponsoring organisation whose legal team should weigh in?
2. **Version decoupling.** Should the spec and package keep one number, or should the spec be 1.0 with the package at 1.0.x independently?
3. **Fan-in features.** Settle readings a, b, c, e now and mark the rest provisional (recommended), or settle everything before rc1?
4. **Healthcare and Telecom.** Rebuild them to the 0.10 spec before 1.0 (recommended, since it doubles as the soak), or stop packaging them until rebuilt?
5. **Rule 8 vs shared roles.** Should Payer, Payee and Initiator become deduplicated roles, or should Rule 8 allow a repeating `derived` key when a row contributes no attributes to the instance?
6. **Section name.** Should it be `## Sources` or `## Source Systems`?
7. **Compliance SME.** Who can review the retention and conflict rules (L2-07, L2-08) before they're rewritten?
