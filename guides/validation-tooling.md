# MD-DDL Validation Tooling Guide

*A non-normative companion guide to the MD-DDL specification. The spec's [Validation Model](../md-ddl-specification/1-Foundation.md#validation-model) states the principle: syntax is checked mechanically, everything else is agent and human judgment. This guide holds the detail for tooling implementers — the full validation level taxonomy, the pre-flight check definitions, the tool interface, and the `{{INCLUDE}}` directive mechanics.*

---

## Why Not a Traditional Linter

MD-DDL is an AI-native standard. The primary consumer of an MD-DDL model is an AI agent that already understands intent, domain context, and organisational conventions — capabilities that no rule-based linter can match. Applying rigid pass/fail enforcement above the syntax level would:

- Reject legitimate organisational vocabulary differences (e.g., `phi` instead of `pii`) that agents understand and can work with
- Suppress feedback that drives spec evolution — when organisations adapt MD-DDL to their context, that signal is valuable
- Produce false positives for intentional exceptions (governance inheritance, minimal reference domains) that require domain context to evaluate correctly

Traditional linters assume the checker is smarter than the thing being checked. For MD-DDL, the inverse is true.

## Validation Levels

Five categories of check exist across the MD-DDL model. Only Level 1 benefits from mechanical tooling:

Level | Category | Example | Mechanically checked?
--- | --- | --- | ---
1 | Syntax | YAML parses, Mermaid renders, markdown links resolve | Yes — broken syntax silently corrupts agent interpretation with no wiggle room
2 | Structure | Required sections present, required YAML keys present | Partially — legitimate exceptions exist; structural checks need domain context to avoid false positives
3 | Convention | Naming patterns, column order, heading hierarchy | No — organisational vocabulary differences are signal, not errors
4 | Quality | Governance completeness, relationship coverage, event payloads | No — this is judgment; agents handle it through domain-review and compliance-audit
5 | Domain fitness | Is this the right model for the business? | Never — requires human domain expertise by definition

**The split:** Level 1 gets mechanical pre-flight checks. Levels 2–5 stay with agents and humans, where context and judgment live.

## Pre-Flight Check Scope

The following checks are the complete set of mechanical validation that MD-DDL endorses. The set is deliberately minimal and closed — anything beyond syntax and reference integrity belongs to agent judgment, not mechanical enforcement.

Check | What it validates | Why it is mechanical
--- | --- | ---
YAML syntax | All YAML code blocks parse without syntax errors | A YAML parse error silently corrupts agent interpretation of every attribute in the block
Mermaid syntax | All Mermaid code blocks use valid diagram syntax | A Mermaid syntax error breaks every rendering of the domain or entity diagram
Internal link integrity | All markdown links (`[text](path)`) resolve to existing files or headings | Dead links break navigation for both humans and agents
Entity reference consistency | Entity names in relationships, events, products, and source mappings match an entity defined in the domain | A typo in an entity name creates a silent reference to nothing
Domain version field | The `version:` key exists in domain metadata | Versionless domains cannot participate in maturity tracking or change management

**What is explicitly not checked mechanically:**

- Presence or absence of optional YAML keys (mutability, temporal, governance fields)
- Naming conventions or vocabulary choices
- Governance metadata completeness or correctness
- Relationship granularity or cardinality appropriateness
- Event payload structure completeness
- Standards alignment accuracy
- Any modelling judgment

## Pre-Flight Check Tool Interface

Any tool implementing pre-flight checks must conform to this interface:

- **Input:** a domain folder path
- **Output:** a list of findings, each with file path, line number, check name, and message
- **Exit behaviour:** report all findings; do not stop on first error
- **Severity:** all findings are a single severity ("pre-flight failure") — there is no warning/error distinction because all checks are binary
- **Configuration:** none — the checks are fixed and minimal; there are no rules to enable or disable

The reference implementation lives at `.github/scripts/preflight.py` in the MD-DDL source repository.

## Agent-Driven Quality Review

Everything above Level 1 is the responsibility of agents. The MD-DDL agents' review and audit skills (domain review, compliance audit) and structured review prompts handle structural, convention, quality, and domain-fitness concerns. They understand context and intent. They flag deviations as observations, not errors.

When an agent encounters an organisational vocabulary deviation — a field named `phi` instead of `pii`, `data_class` instead of `classification` — the correct response is to note it as a **potential spec vocabulary gap** and work with it, not reject the file.

---

## The Include Directive

Agent prompt files and skill reference stubs use an `{{INCLUDE: <path>}}` directive to inject content from other files at prompt-load time. This is processed by the AI platform (e.g. VS Code Copilot custom agents, Claude Code) before the prompt reaches the model — it is not part of the MD-DDL modelling language itself.

The directive appears on its own line and takes a file-relative path:

```text
{{INCLUDE: ../../../md-ddl-specification/3-Entities.md}}
```

Paths must be relative to the file containing the directive. Do not use workspace-root paths, as MD-DDL repositories are commonly consumed as submodules where absolute paths break.

This mechanism enables the spec reference stub pattern: skill reference files contain a brief description and an `{{INCLUDE}}` pointing to the canonical spec section, so that spec updates propagate automatically without duplicating content across agent files.
