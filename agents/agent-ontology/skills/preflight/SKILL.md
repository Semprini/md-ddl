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

Runs the five Level-1 mechanical checks defined in the MD-DDL Validation
Model against a domain folder and presents the findings to the user.

The checks cover YAML syntax, Mermaid syntax, internal link integrity,
entity reference consistency, and domain version. See
`1-Foundation.md § Pre-Flight Check Scope` for the rationale and exact
scope of each check.

---

## Steps

### 1 — Identify the domain folder

If the domain folder is not clear from context, ask:

> Which domain folder should I check? (e.g. `domains/customer` or the
> current working directory if you are inside a domain folder)

The folder must contain a `domain.md` at its root.

### 2 — Run the script

```bash
python .github/scripts/preflight.py "<domain-folder>"
```

If the `pyyaml` package is not installed, instruct the user to run:

```bash
pip install pyyaml
```

### 3 — Present findings

**Exit code 0 — pass:**
> Pre-flight passed. No mechanical issues found.

The model is clear to commit from a mechanical standpoint. Remind the
user that Levels 2–5 (structure, convention, quality, domain fitness)
are covered by agent-driven review, not this script.

**Exit code 1 — findings:**

Present findings grouped by check type. For each finding, show the file
path, line number, and a plain-language explanation of what needs fixing.

All findings must be resolved before committing — there is no
warning/error distinction. Every finding is a pre-flight failure.

Common fixes by check:

| Check | Typical fix |
|---|---|
| `yaml-syntax` | Find the block at the reported line and fix indentation or quoting |
| `mermaid-syntax` | Ensure the block starts with a valid diagram type (e.g. `graph TD`, `classDiagram`) |
| `internal-links` | Verify the linked file exists; check for typos in path or anchor — applies to markdown links `[text](path)`, HTML `href='path'` inside Mermaid node labels, and same-page anchors `#heading` |
| `entity-references` | Match the value exactly to an entity name in the `## Entities` table in `domain.md` |
| `domain-version` | Add `version: "x.y.z"` to the `## Metadata` YAML block in `domain.md` |

**Exit code 2 — invocation error:**

Report the error and correct the command. Check that the path is a
directory containing `domain.md`.

### 4 — After fixes

Once the user has resolved findings, re-run the script to confirm a
clean pass before they proceed to commit.

---

## Notes

- The `internal-links` check covers three link forms: markdown `[text](path)`,
  HTML `href='path'` or `href="path"` (used in Mermaid node labels), and
  same-page anchors `#heading`. All must resolve.
- `{{INCLUDE: path}}` directives in agent/skill files are not covered — they
  live outside domain folders and are a separate concern.
- The script skips files under `sources/` and `products/` for entity reference
  checks, because those files use the `source:` key for system names, not entity names.
- Checks 1–3 (YAML, Mermaid, links) run against every `.md` file in the
  domain folder tree.
- Checks 4–5 require `domain.md` to exist at the domain folder root.
- This script does not check governance completeness, naming conventions,
  or modelling quality — those are agent-review concerns (Levels 2–5).
