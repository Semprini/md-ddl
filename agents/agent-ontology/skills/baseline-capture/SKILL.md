---
name: baseline-capture
description: Use this skill when the user wants to document existing schemas, models, ETL pipelines, or catalog metadata as MD-DDL baselines for audit or history purposes. This is the secondary brownfield path — use schema-import instead when the goal is to create canonical entities. Triggers include "capture baseline", "document existing state", "record current state", or when the user explicitly wants documentation-only baseline files (not canonical entities).
---

# Skill: Baseline Capture

Documents existing data assets as MD-DDL baseline files within a domain's
`baselines/` folder. This is the **secondary brownfield path** — use it when
the goal is documentation and audit, not when the user wants canonical
entities (use schema-import for that).

Baselines are **agent-generated from raw input**. The user provides DDL, dbt
models, catalog exports, pipeline descriptions, or natural-language notes.
The agent structures the baseline file. The user should never be asked to
author YAML templates manually.

## MD-DDL Reference

Load the Adoption specification from `md-ddl-specification/10-Adoption.md`
before responding. Key sections to apply:

- **Baselines** — folder structure, file format, metadata header
- **Adoption Maturity Model** — Level 1 (Documented) criteria

---

## Process

### Step 1 — Identify Baseline Type

Determine which subfolder to use based on the asset:

- **Dimensional model** → `baselines/dimensional/`
- **Canonical/enterprise model** → `baselines/canonical/`
- **ETL/ELT pipeline** → `baselines/etl/`
- **Catalog metadata** → `baselines/catalog/`

If the type is obvious from the input (e.g., CREATE TABLE with `fact_` prefix),
do not ask — just proceed.

### Step 2 — Accept Raw Input

Accept whatever the user provides in whatever form they have:

- DDL (CREATE TABLE statements) — pasted directly
- dbt model SQL or schema.yml
- Catalog export (CSV, JSON, or described fields)
- ERD or data model documentation
- Natural-language description of a pipeline or process
- Screenshots or copy-paste from documentation tools

Do not ask the user to restructure their input. Take it as-is.

### Step 3 — Generate Baseline File

From the raw input, produce a baseline file with:

1. **`baseline:` metadata header** — `type`, `source_system`, `captured_date`,
   `captured_by`, `status` (default: `active`)
2. **Free-form body** — the raw input preserved (DDL in fenced code blocks,
   descriptions as prose, catalog data as tables or YAML) plus any structured
   summary the agent can extract (column listings, quality notes, etc.)

The body format should match what the user provided. If they pasted DDL, the
DDL appears verbatim. If they described a pipeline, the description appears
as prose. The agent may add structure (e.g., a column summary table) but
must not require it.

### Step 4 — Identify Candidate Entities

After documenting the baselines, identify business concepts that could
become canonical entities:

- **From dimensional baselines:** Facts → business processes, Dimensions → business entities
- **From canonical baselines:** Existing entities may map 1:1 or need restructuring
- **From ETL baselines:** Pipeline targets reveal entities; sources reveal operational systems
- **From catalog baselines:** Catalog assets and lineage reveal entity candidates

Present candidates as a list — do not create entity files.

### Step 5 — Set Domain Adoption Metadata

If the domain file exists, update (or propose adding) the `adoption` block:

```yaml
adoption:
  maturity: documented
  adoption_started: <today's date>
  target_maturity: # TODO:
  target_date: # TODO:
  progress:
    at_level: 0
    total: <number of baseline assets>
  notes: "Initial baseline capture of existing assets."
```

If the domain file does not exist, note that one should be created and
suggest handing off to the domain-scoping skill.

---

## Boundary Rules

- **This skill documents existing state.** It does NOT create canonical
  entity files in `entities/`. That is schema-import or entity-modelling.
- **This skill does not generate physical artifacts.** Baselines are
  documentation only.
- **This skill does not create mapping blocks.** Mappings are derived from
  source transform files, not stored in baselines.
- **Baselines are agent-generated.** Never present a blank YAML template
  and ask the user to fill it in. Parse their raw input and produce the file.

---

## Handoff

After baseline capture is complete:

- **To create canonical entities from existing schemas** → schema-import
  skill (recommended primary path)
- **To create canonical entities via full interview** → domain-scoping skill
- **To review the domain** → domain-review skill
