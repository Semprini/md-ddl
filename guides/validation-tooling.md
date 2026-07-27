# MD-DDL Validation Tooling Guide

*A non-normative companion guide to the MD-DDL specification. The spec's [Validation Model](../md-ddl-specification/1-Foundation.md#validation-model) states the principle: syntax is checked mechanically, everything else is agent and human judgment. This guide holds the detail for tooling implementers — the full validation level taxonomy, the pre-flight check definitions, the tool interface, and the `{{INCLUDE}}` directive mechanics.*

---

## Why Not a Traditional Linter

MD-DDL is an AI-native standard. The primary consumer of an MD-DDL model is an AI agent that already understands intent, domain context, and organisational conventions — capabilities that no rule-based linter can match. Applying rigid pass/fail enforcement above the syntax level would:

- Reject legitimate organisational vocabulary differences (e.g., `phi` instead of `pii`) that agents understand and can work with
- Suppress feedback that drives spec evolution — when organisations adapt MD-DDL to their context, that signal is valuable
- Produce false positives for intentional exceptions (governance inheritance, minimal reference domains) that require domain context to evaluate correctly

Traditional linters assume the checker is smarter than the thing being checked. For MD-DDL, the inverse is true.

This is why the tooling stops at self-contradiction. A model that says one thing in its diagram and another in its YAML is wrong by its own account — no domain knowledge is needed to see it, and mechanical checking is the cheapest way to catch it. Everything past that point, where being different is not the same as being wrong, is reported as an observation rather than a failure.

## Validation Levels

Five categories of check exist across the MD-DDL model. Only Level 1 benefits from mechanical tooling:

Level | Category | Example | Mechanically checked?
--- | --- | --- | ---
1 | Syntax | YAML parses, Mermaid renders, markdown links resolve | Yes — broken syntax silently corrupts agent interpretation with no wiggle room
1b | Reference integrity | The diagram, the summary tables and the YAML all name the same things | Yes — a model that contradicts itself has one wrong answer, not a judgment call
2 | Structure | Required sections present, required YAML keys present | Partially, as **warnings** — legitimate exceptions exist, so these inform rather than fail
3 | Convention | Naming patterns, column order, heading hierarchy | No — organisational vocabulary differences are signal, not errors
4 | Quality | Governance completeness, relationship coverage, event payloads | No — this is judgment; agents handle it through domain-review and compliance-audit
5 | Domain fitness | Is this the right model for the business? | Never — requires human domain expertise by definition

**The split:** Levels 1 and 1b get mechanical pre-flight checks that fail the run. Level 2 gets warnings that report but do not fail. Levels 3–5 stay with agents and humans, where context and judgment live.

## Pre-Flight Check Scope

The following checks are the complete set of mechanical validation that MD-DDL endorses. The set is deliberately minimal and closed — anything beyond syntax and reference integrity belongs to agent judgment, not mechanical enforcement.

**Syntax and reference integrity** — these fail the run:

Rule id | What it validates | Why it is mechanical
--- | --- | ---
`yaml-syntax` | All YAML code blocks parse without syntax errors | A YAML parse error silently corrupts agent interpretation of every attribute in the block
`mermaid-syntax` | All Mermaid code blocks declare a recognised diagram type | A Mermaid syntax error breaks every rendering of the domain or entity diagram
`link-resolve` | All markdown links (`[text](path)`) and Mermaid `href` targets resolve to existing files and headings | Dead links break navigation for both humans and agents
`entity-references` | `extends`, `source`, `target` and `entity` values name an entity defined in the domain | A typo in an entity name creates a silent reference to nothing
`domain-version` | The `version:` key exists in domain metadata | Versionless domains cannot participate in maturity tracking or change management
`domain-diagram-coverage` | Every node in the overview diagram is declared in the Entities or Enums table, and every `is a` edge matches the `Specializes` column | A concept drawn but never declared is invisible to every agent that reads the tables first
`domain-link-consistency` | Summary links reach a detail heading of the same name, and diagram links agree with the table links | The summary is the router; if it points somewhere else than the diagram does, the two disagree about what the model is
`entity-heading-link` | A detail file's level‑1 heading links back to its domain | Without it a detail file cannot be reassembled into its domain
`entity-diagram-links` | Outgoing and inheritance targets in a `classDiagram` link to their detail markdown | An unlinked reference class is a dead end for navigation
`entity-enum-in-diagram` | Every enum used by an attribute is declared in the entity diagram | An attribute typed to an enum the diagram never shows contradicts its own rendering
`entity-attribute-consistency` | Attribute names and types agree between the `classDiagram` and the YAML | The YAML is authoritative and the diagram renders it; where they differ, one of them is lying

**Structural observations** — these report but do not fail:

Rule id | What it observes
--- | ---
`domain-table-coverage` | An entity declared in the Entities table that the overview diagram never draws
`domain-diagram-coverage` (partial) | A labelled edge whose verb does not match any Relationships entry, or an unlabelled edge
`entity-attribute-consistency` (partial) | Attributes shown in a child's diagram that may be inherited, and identifier markers that disagree

The warning tier is where organisational deviation lives. A team that deliberately draws only part of its ontology, or names relationship labels differently from relationship names, is making a choice — the tool reports it as an observation and moves on, exactly as an agent would.

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

- **Input:** a domain folder path, a folder containing several domains, or a single markdown file
- **Output:** a list of findings, each with file path, line number, rule id, severity, and message
- **Exit behaviour:** report all findings; do not stop on first error
- **Severity:** two levels. `error` for syntax and reference integrity — the model contradicts itself or fails to parse. `warning` for structural observations, where a deliberate organisational choice is a legitimate explanation. Only errors fail the run.
- **Configuration:** rules may be disabled by id, and warnings may be promoted to failures. Nothing else is configurable — the check set itself is fixed and closed.

The reference implementation lives at `scripts/md_ddl_lint.py` in the MD-DDL source repository:

```shell
python scripts/md_ddl_lint.py <domain-folder>
python scripts/md_ddl_lint.py <folder-of-domains> --strict
python scripts/md_ddl_lint.py <file.md> --format json
python scripts/md_ddl_lint.py --list-rules
```

`--format json` emits findings as `{file, line, column, severity, rule, message}`, for editor integration. `--disable <rule-id>,...` skips named rules. `--strict` makes warnings fail the run. Exit code is `1` when any error is reported, `0` otherwise.

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
