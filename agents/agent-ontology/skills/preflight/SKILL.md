---
name: preflight
description: >
  Use this skill when the user wants to validate their MD-DDL model before
  committing or publishing, asks "is this valid?", "run pre-flight checks",
  "check my domain", or indicates they are ready to commit. Also offer to
  run this at the end of any modelling session where domain files were
  created or modified.
---

# Skill: Pre-Flight Check

Runs the Level-1 mechanical checks defined in the MD-DDL Validation Model
against a domain folder and presents the findings to the user.

The checks cover syntax (YAML, Mermaid), reference integrity (links, entity
references, domain version), and agreement between a model's three
representations — the overview diagram, the summary tables, and the YAML.
See `guides/validation-tooling.md § Pre-Flight Check Scope` for the
rationale and exact scope of each rule.

---

## Steps

### 1 — Identify the domain folder

If the domain folder is not clear from context, ask:

> Which domain folder should I check? (e.g. `domains/customer` or the
> current working directory if you are inside a domain folder)

The folder must contain a `domain.md` at its root. A parent folder holding
several domains, or a single markdown file, may also be passed.

### 2 — Run the script

```bash
python scripts/md_ddl_lint.py "<domain-folder>"
```

If the `pyyaml` package is not installed, instruct the user to run:

```bash
pip install pyyaml
```

Use `--list-rules` to show the available rule ids, `--disable <id>,...` to
skip rules the organisation has deliberately deviated from, and `--strict`
to make warnings fail the run.

### 3 — Present findings

**Exit code 0 — pass:**
> Pre-flight passed. No errors found.

The model is clear to commit from a mechanical standpoint. Warnings may
still be present — report them as observations. Remind the user that
Levels 3–5 (convention, quality, domain fitness) are covered by
agent-driven review, not this script.

**Exit code 1 — errors:**

Present findings grouped by file. For each finding, show the file path,
line number, and a plain-language explanation of what needs fixing.

Findings carry two severities:

- **`error`** — the model fails to parse or contradicts itself. Resolve
  all errors before committing.
- **`warning`** — a structural observation with a possible legitimate
  explanation. Discuss with the user rather than assuming it is a defect.
  If it reflects a deliberate organisational choice, note it as a potential
  spec contribution and move on.

Common fixes by rule:

| Rule | Typical fix |
|---|---|
| `yaml-syntax` | Find the block at the reported line and fix indentation or quoting |
| `mermaid-syntax` | Ensure the block starts with a valid diagram type (e.g. `graph TD`, `classDiagram`) |
| `link-resolve` | Verify the linked file exists; check for typos in path or anchor — applies to markdown links `[text](path)`, HTML `href='path'` inside Mermaid node labels, and same-page anchors `#heading` |
| `entity-references` | Match the value to an entity name in the `## Entities` table in `domain.md` |
| `domain-version` | Add `version: "x.y.z"` to the `## Metadata` YAML block in `domain.md` |
| `domain-diagram-coverage` | Add the drawn concept to the Entities or Enums table, or fix the `Specializes` column to match an `is a` edge |
| `domain-link-consistency` | Point the summary link at the detail heading of the same name, or rename one of them so they agree |
| `entity-heading-link` | Make the level-1 heading a link back to the domain, e.g. `# [My Domain](../domain.md)` |
| `entity-diagram-links` | Declare the referenced class with a link: `class Foo["<a href='foo.md'>Foo</a>"]` |
| `entity-enum-in-diagram` | Add the enum to the diagram: `class FooType["<a href='...'>Foo Type</a>"]{<<enumeration>>}` |
| `entity-attribute-consistency` | Bring the `classDiagram` attributes and types into line with the YAML — the YAML is authoritative |

**Exit code 2 — invocation error:**

Report the error and correct the command. Check that the path exists and
that a `domain.md` can be found at or above it.

### 4 — After fixes

Once the user has resolved the errors, re-run the script to confirm a
clean pass before they proceed to commit.

---

## Notes

- The `link-resolve` check covers three link forms: markdown `[text](path)`,
  HTML `href='path'` or `href="path"` (used in Mermaid node labels), and
  same-page anchors `#heading`. All must resolve. External `http(s)` links
  are not fetched.
- `{{INCLUDE: path}}` directives in agent/skill files are not covered — they
  live outside domain folders and are a separate concern.
- Files under `sources/`, `products/` and `baselines/` are skipped for entity
  reference checks, because those files use the `source:` key for system
  names, not entity names.
- Syntax and link checks run against every `.md` file in the domain folder
  tree. Domain-level checks require `domain.md` at the domain folder root;
  entity-level checks apply to files carrying a `## Entities` section.
- `--format json` emits findings as `{file, line, column, severity, rule,
  message}` for editor integration.
- This script does not check governance completeness, naming conventions,
  or modelling quality — those are agent-review concerns (Levels 3–5).
