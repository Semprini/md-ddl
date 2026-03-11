# Plan: Validation Philosophy & Pre-Flight Checks

## TL;DR

MD-DDL is an AI-native, markdown-based standard. Traditional linting — rigid rule enforcement with pass/fail gates — is the wrong model for a standard where agents are more sophisticated than any linter could be, and where organisational flexibility in applying conceptual and governance patterns is a feature, not a bug.

Instead, establish a two-tier validation model: **thin mechanical pre-flight checks** that catch broken syntax no one benefits from debugging, and **agent-driven contextual quality review** that understands intent, organisational context, and domain fitness. Embed this philosophy explicitly in the spec, contributor instructions, and agent prompts so the reasoning is discoverable and reviewable.

---

## The Argument

### Why not a traditional linter

Traditional linting assumes the thing being checked is dumber than the checker. A JSON Schema validator doesn't understand API semantics — it checks structure mechanically. That model breaks for MD-DDL because:

1. **The primary consumer is more sophisticated than any linter.** Agent Ontology already reads domain files, understands intent, identifies gaps, and produces contextually appropriate feedback. A linter saying "missing `mutability` key" does less than the agent already does — with less context about whether the omission was intentional.

2. **Conceptual models are not compilable.** Entity relationships, governance metadata, domain scoping decisions — these are judgment calls informed by business context. "Is 7 years enough retention?" is a compliance question, not a lint error.

3. **Premature rigidity at v0.9.0 kills feedback.** If a healthcare organisation uses `phi: true` instead of `pii: true` because that's their compliance vocabulary, a linter rejects it. An agent understands it, works with it, and flags it as a potential spec contribution. That feedback loop is how standards improve.

4. **Organisational wiggle room is a feature.** Different organisations will adapt MD-DDL to their context. Agents can understand idiosyncrasies and work with SMEs. A linter cannot. Allowing skilled people and agents to "riff" on best practice — while still conforming to core structural rules — produces better adoption and better standard evolution.

### What mechanical checking IS good for

Not all validation is judgment. Five categories of check exist, and only the first genuinely benefits from mechanical tooling:

Level | Category | Example | Lintable? | Why
--- | --- | --- | --- | ---
1 | Syntax | YAML parses, Mermaid renders, markdown links resolve | Yes | Broken syntax silently changes agent interpretation. No wiggle room needed.
2 | Structure | Required sections present, required YAML keys present | Partially | Legitimate exceptions exist (governance inheritance, minimal domains). A structural checker needs domain context to avoid false positives.
3 | Convention | Naming patterns, table column order, heading hierarchy | No | Organisational vocabulary differences are signal, not errors.
4 | Quality | Governance completeness, relationship coverage, event payloads | No | This is judgment. Agents handle it through domain-review and compliance-audit skills.
5 | Domain fitness | Is this the right model for the business? | Never | Requires human domain expertise by definition.

**The split:** Level 1 gets a mechanical pre-flight check. Levels 2–5 stay with agents and humans, where context and judgment live.

---

## Phase 1: Define Pre-Flight Checks in the Spec

### Step 1: Add validation philosophy to 1-Foundation.md

Add a new section to `md-ddl-specification/1-Foundation.md` — "Validation Model" — articulating:

- MD-DDL uses a two-tier validation model: mechanical pre-flight checks and agent-driven quality review
- Pre-flight checks are syntax-level only — they catch broken YAML, invalid Mermaid, dead links, and missing structural anchors
- Pre-flight checks never reject a file for convention, governance completeness, or modelling judgment
- Agents are the quality layer — they understand intent, organisational context, and domain fitness
- Organisational adaptation of vocabulary and patterns is expected and valuable — agents work with deviations rather than rejecting them
- Feedback from real-world usage informs spec evolution — rigid enforcement at the tooling level would suppress this signal

**Relevant file:** `md-ddl-specification/1-Foundation.md`

### Step 2: Define the pre-flight check scope

Document the exact checks that constitute pre-flight validation. These are the *only* mechanical checks the standard endorses:

Check | What it validates | Why it's mechanical
--- | --- | ---
YAML syntax | All YAML code blocks parse without syntax errors | A YAML parse error silently corrupts agent interpretation of every attribute
Mermaid syntax | All Mermaid code blocks use valid diagram syntax | A Mermaid syntax error breaks every rendering of the domain/entity diagram
Internal link integrity | All markdown links (`[text](path)`) resolve to existing files or headings | Dead links break navigation for both humans and agents
Entity reference consistency | Entity names in relationships, events, products, and source mappings match an entity defined in the domain | A typo in an entity name creates a silent reference to nothing
Domain version field | The `version:` key exists in domain metadata | Versionless domains cannot participate in maturity tracking or change management

**What is explicitly NOT checked:**
- Presence or absence of optional YAML keys (mutability, temporal, governance fields)
- Naming conventions or vocabulary choices
- Governance metadata completeness or correctness
- Relationship granularity or cardinality appropriateness
- Event payload structure completeness
- Standards alignment accuracy
- Any modelling judgment

**Relevant file:** `md-ddl-specification/1-Foundation.md` (validation model section)

### Step 3: Write pre-flight check tooling specification

Define the interface for a pre-flight check tool (language-agnostic — could be implemented in Python, TypeScript, or as an agent skill):

- Input: a domain folder path
- Output: a list of findings, each with file path, line number, check name, and message
- Exit behaviour: report all findings, do not stop on first error
- Severity: all findings are the same severity ("pre-flight failure") — there is no warning/error distinction because all checks are binary
- No configuration: the checks are fixed and minimal. There are no rules to enable/disable.

This step defines the spec for the tool. Implementation is a separate concern (and could be a standalone script, a VS Code extension, or an agent skill).

**Relevant file:** `md-ddl-specification/1-Foundation.md` or a new `md-ddl-specification/10-Tooling.md` if the section grows beyond a page

---

## Phase 2: Embed Philosophy in Contributor Instructions

### Step 4: Update copilot-instructions.md

Add a new section "Validation philosophy" to `.github/copilot-instructions.md` under the cross-cutting rules. Content:

- MD-DDL distinguishes between **mechanical pre-flight checks** (syntax, links, references) and **agent-driven quality review** (structure, convention, governance, fitness)
- Contributors should not add lint-style enforcement rules to agent prompts. If an agent rejects a file for a convention violation, that's a prompt bug.
- Agents flag deviations from spec patterns as **observations**, not errors — unless the deviation is at the syntax level (broken YAML, dead links)
- When reviewing agent prompts, verify that validation language uses "flag" / "note" / "suggest" for convention and quality issues, and "error" / "reject" only for syntax-level failures
- The validation section in `1-Foundation.md` is the normative reference for what constitutes a pre-flight check vs. agent-driven review

**Relevant file:** `.github/copilot-instructions.md`

### Step 5: Update CLAUDE.md

Add a brief note to `CLAUDE.md` pointing to the validation philosophy:

- MD-DDL uses agent-driven quality review, not traditional linting. See `1-Foundation.md` for the validation model.
- Agents should work with organisational deviations from convention, not reject them.

**Relevant file:** `CLAUDE.md`

---

## Phase 3: Update Agent Prompts

### Step 6: Update Agent Guide to explain the philosophy

Agent Guide is where users go to learn. It should be able to explain *why* MD-DDL doesn't have a traditional linter when asked. Add to the Agent Guide skill index or concept-explorer skill:

- A trigger for questions about "linting", "validation", "conformance checking", "why no linter"
- Response guidance: explain the two-tier model, the 5-level categorisation (syntax → structure → convention → quality → fitness), and why only Level 1 is mechanically checked
- Reference to `1-Foundation.md` validation model section

**Relevant file:** `agents/agent-guide/AGENT.md` or `agents/agent-guide/skills/concept-explorer/SKILL.md`

### Step 7: Update Agent Ontology domain-review skill

The domain-review skill already implements the right approach (6-step protocol with explicit "What AI Cannot Validate" boundaries). Strengthen it by:

- Adding an explicit statement that the review is *not* a lint pass — it is contextual quality review
- Reinforcing that convention deviations are flagged as observations with rationale, not as errors
- Adding guidance that organisational vocabulary differences (e.g., `phi` instead of `pii`, `data_class` instead of `classification`) should be noted as "potential spec vocabulary gap" rather than "non-conformance"
- Reference the validation philosophy in `1-Foundation.md`

**Relevant file:** `agents/agent-ontology/skills/domain-review/SKILL.md`

### Step 8: Update Agent Governance compliance-audit skill

Agent Governance audits governance metadata. It should:

- Distinguish between *structurally missing* governance fields (pre-flight concern — the YAML key isn't there at all) and *substantively incomplete* governance (quality concern — the value exists but may not be sufficient)
- Flag governance vocabulary deviations as potential spec contributions, not compliance failures
- Maintain the existing severity model (Critical Gap, Advisory Gap, Not Assessed) but ensure Critical is reserved for things that break downstream processing, not for convention deviations

**Relevant file:** `agents/agent-governance/skills/compliance-audit/SKILL.md`

---

## Phase 4: Update Review Process

### Step 9: Update structural review prompt

The Layer 1 structural review (`.github/md-ddl-review-prompt.md`) should include a check that:

- Agent prompts do not use "error" / "reject" / "fail" language for convention or quality issues
- Agent prompts use "flag" / "note" / "suggest" / "observe" for non-syntax concerns
- The validation philosophy section exists in `1-Foundation.md` and is consistent with agent behaviour

**Relevant file:** `.github/md-ddl-review-prompt.md`

### Step 10: Update adversarial review prompt

The Layer 2 adversarial review (`.github/md-ddl-adversarial-review-prompt.md`) should probe:

- "What happens when an organisation uses non-standard vocabulary? Does the standard accommodate or reject?"
- "Is there a hidden rigidity in agent prompts that contradicts the stated validation philosophy?"
- "Could the pre-flight checks grow into a de facto linter over time? What prevents scope creep?"

**Relevant file:** `.github/md-ddl-adversarial-review-prompt.md`

---

## Phase 5: Implementation (Optional — Deferred)

### Step 11: Implement pre-flight check script

Write a minimal script (Python or PowerShell) that runs the 5 pre-flight checks against a domain folder. This is optional and deferred because:

- The checks are simple enough that agents already perform them implicitly
- The value is in CI/CD pipelines, not interactive sessions
- Implementation depends on whether a build/tooling pipeline is established (currently there is none)

If implemented:
- Input: `preflight-check ./examples/Financial\ Crime/`
- Output: list of findings or "All pre-flight checks passed"
- No configuration files, no rule toggles, no severity levels

**Relevant files:** New script in `.github/scripts/` or `tools/`

---

## Relevant Files

- `md-ddl-specification/1-Foundation.md` — validation model section (Steps 1–3)
- `.github/copilot-instructions.md` — validation philosophy for contributors (Step 4)
- `CLAUDE.md` — brief validation note (Step 5)
- `agents/agent-guide/AGENT.md` or concept-explorer skill — explain philosophy to users (Step 6)
- `agents/agent-ontology/skills/domain-review/SKILL.md` — strengthen contextual review language (Step 7)
- `agents/agent-governance/skills/compliance-audit/SKILL.md` — governance audit language (Step 8)
- `.github/md-ddl-review-prompt.md` — structural review check (Step 9)
- `.github/md-ddl-adversarial-review-prompt.md` — adversarial probe (Step 10)

## Verification

1. Read `1-Foundation.md` validation model section — confirm it articulates two-tier model and lists exactly 5 pre-flight checks
2. Read `.github/copilot-instructions.md` — confirm validation philosophy section exists and references `1-Foundation.md`
3. Grep all agent AGENT.md and SKILL.md files for "error" / "reject" / "fail" in validation context — confirm these words are used only for syntax-level issues
4. Grep agent prompts for "flag" / "note" / "suggest" / "observe" — confirm these are used for convention and quality issues
5. Read Agent Guide concept-explorer — confirm it can explain the validation philosophy when asked about linting
6. Read domain-review SKILL.md — confirm organisational vocabulary deviations are treated as observations, not errors
7. Read `.github/md-ddl-review-prompt.md` — confirm it checks agent validation language consistency
8. Read `.github/md-ddl-adversarial-review-prompt.md` — confirm it probes for hidden rigidity

## Decisions

- **No traditional linter.** The standard explicitly rejects rigid rule enforcement for anything above syntax level. This is a deliberate design choice, not an omission.
- **Pre-flight checks are fixed and minimal.** 5 checks, no configuration, no rule toggles. Scope creep into convention or quality checking is a bug in the tool, not a feature request.
- **Agents are the quality layer.** Domain-review, compliance-audit, and structured reviews handle everything above syntax. They have context that no linter can have.
- **Deviations are feedback, not failures.** When an organisation uses non-standard vocabulary, that's signal about how the spec should evolve. Agents capture this signal; linters suppress it.
- **Implementation is deferred.** The philosophy and spec changes come first. A pre-flight script is optional and only valuable once a CI/CD pipeline exists.

## Dependencies

- Steps 1–3 are independent (spec work)
- Steps 4–5 are independent (contributor instructions)
- Steps 6–8 depend on Steps 1–3 (agents reference the spec section)
- Steps 9–10 are independent (review prompts)
- Step 11 is deferred and depends on all prior steps
- No dependencies on other plans (brownfield, example completeness, cross-domain)

## Further Considerations

1. **Scope creep prevention.** The biggest risk is that pre-flight checks gradually accumulate new rules until they become a de facto linter. The adversarial review probe (Step 10) is designed to catch this. Additionally, the spec should state that adding a new pre-flight check requires a spec version bump — making it a deliberate, reviewed decision rather than a casual addition.

2. **Agent validation language audit.** Steps 7–8 call for updating agent language, but a full audit of all agent prompts for inadvertent lint-style language ("must have", "required", "error if missing") would be valuable. This could be a one-time sweep or a recurring review check.

3. **Community contribution pathway.** When agents flag organisational deviations as "potential spec vocabulary gaps," there should be a mechanism for feeding those back to the spec. This is out of scope for this plan but is a natural follow-on — potentially a `CONTRIBUTING.md` or issue template that captures real-world vocabulary divergences.
