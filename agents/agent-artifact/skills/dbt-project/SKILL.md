---
name: dbt-project
description: Use this skill when the user asks for a dbt project, dbt models, dbt sources, dbt unit tests, or dbt data tests generated from MD-DDL; mentions "dbt-core", "dbt Cloud", "DuckLake", "DuckDB", "local testing", "project template", "template project", or "data product repo"; or wants to run MD-DDL-derived transformations locally before promoting to a cloud warehouse such as Snowflake. Shared by Agent Artifact (project, sources, models, contracts) and Agent Test (unit tests, data tests, local execution).
---

# Skill: dbt Project Generation

Generates a dbt project for one data product from its MD-DDL declarations. The
project is built from the organisation's **template project** and runs in two tiers:
**dbt-core + DuckLake** on a laptop or CI runner, then **dbt Cloud + the target
warehouse** (typically Snowflake). The same models and tests run in both tiers.
Only the profile changes.

This skill is shared. Each agent owns a different part of the project:

Part of the project | Owner | What it contains
--- | --- | ---
Scaffold from template, `sources.yml`, staging / intermediate / canonical / product models, model contracts, masking hooks | Agent Artifact | Transformation logic derived from transform detail and product declarations
`unit_tests:` blocks, generic and singular data tests, fixtures, synthetic seeds, selectors, local profile | Agent Test | Assertions derived from worked examples, constraints, temporal rules, and SLA

Each agent writes only its own part. When one agent finds a defect in the other's
part, it hands off; it does not patch the other agent's files.

## MD-DDL Reference

Load before responding:

- `md-ddl-specification/7-Sources.md` — source schema tables, Entity Fan-Out, source idiosyncrasies
- `md-ddl-specification/8-Transformations.md` — transformation types, expression language, worked examples
- `md-ddl-specification/9-Data-Products.md` — `schema_type`, logical model, attribute mapping, masking, SLA
- `../../references/generation-semantics.md` — `existence`, `mutability`, `temporal`, `change_model` to physical structure
- The generation skill that matches the product's `schema_type` (`../normalized/`, `../dimensional/`, `../wide-column/`)
- `../dialects/snowflake.md` when the cloud tier is Snowflake

---

## Process

### Step 1 — Confirm Scope

Confirm before generating:

1. **Data product** in scope. One dbt project per data product is the default.
   Ask before combining products into one project.
2. **Template project**: its path or repository. If the organisation has none, say
   so and use the default layout in Step 3. Do not make one up.
3. **Cloud tier**: warehouse and dbt Cloud or dbt-core in CI. Default: Snowflake.
4. **dbt version** available locally. Unit tests need dbt-core 1.8 or later.
5. **Consistency posture and null strategy** from the product declaration (see
   Agent Architect product-design Step 8). These decide whether `NOT NULL` goes into
   contracts or only into tests.

Transition phrase: "I have enough context to generate the dbt project for [product]. Shall I proceed?"

### Step 2 — Read the Template Project

The template is the organisation's standard. Its conventions override every default
in this skill. Read it and record:

What to read | What it decides
--- | ---
`dbt_project.yml` | Project name pattern, model paths, materialisation defaults per folder, `+schema`, `+tags`, required `vars`
Folder layout under `models/` | Layer names (e.g. `staging`/`intermediate`/`marts` vs `raw`/`clean`/`serve`)
File naming examples | Model prefixes (`stg_`, `int_`, `fct_`, ...), YAML naming (`_<folder>__models.yml`, `schema.yml`, ...)
`packages.yml` | Available packages (`dbt_utils`, `dbt_expectations`, internal packages). Use what is there. Add a package only with the user's agreement.
`macros/` | Organisation macros for masking, audit columns, surrogate keys, generate_schema_name. Call these; do not reimplement them.
`profiles.yml` template or CI config | Target names, how credentials are injected, whether a local target already exists
Linting (`.sqlfluff`, pre-commit) | SQL style that generated models must pass
Placeholders (`{{ product_name }}`, cookiecutter/copier variables) | Values to fill from the product declaration

Produce a short **template profile** (layer names, prefixes, packages, macros,
targets) in the output before generating. If the template has no local target,
add one following Step 6 and note it as an addition.

### Step 3 — Map MD-DDL to Project Layers

Default layout, used when there is no template and renamed to the template's layers
when there is one:

MD-DDL construct | dbt artefact | Default name
--- | --- | ---
Source summary + transform detail Source Schema table | `sources:` entry per source system, `tables:` per source table, `columns:` with `data_type` and description | `models/staging/<source_id>/_<source_id>__sources.yml`
Source table | Staging model: cast and apply `null_as` / `format` / `normalise` idiosyncrasies. Source column names are kept verbatim; renaming to attribute names happens in the intermediate model, where the `Destination` column declares it. This lets worked-example `given` rows be used as staging rows unchanged. No business logic. | `stg_<source_id>__<table>`
Entity Fan-Out entry (one per produced entity) | Intermediate model per produced entity per source table, applying that table's transformations and the fan-out `condition` | `int_<entity>__<source_id>_<table>`
`deduplication` transformation | Window/`qualify` over the intermediate model, key branches in declared order, survivorship as ordering | inside the intermediate model
Canonical entity with several contributing sources (fan-in) | Canonical model unioning the intermediate models on the entity identifier, applying `reconciliation` transformations per attribute | `<entity>` (canonical layer)
`temporal.tracking` / `mutability` | Incremental model or snapshot per `generation-semantics.md` | per temporal strategy
Data product `schema_type` + logical model | Product models shaped by the matching generation skill | template's mart/serve layer
Product `masking` | Organisation masking macro or warehouse masking policy via `post-hook`; recorded in `meta` | product models
Entity and product governance | `meta:` on models and columns (`classification`, `pii`, `retention`) | model YAML

`<source_id>` in model and file names is the source's `id` with hyphens replaced by
underscores (`salesforce-crm` becomes `salesforce_crm`), since dbt names must be valid identifiers.

Every model and column carries `meta.md_ddl` with the declaration it came from
(file path and heading anchor). This is how Agent Test and reconciliation trace a
failing assertion back to the spec.

### Step 4 — Generate Models

Rules for the models themselves:

- **Expressions:** translate the MD-DDL expression language (8-Transformations) into
  SQL through dbt cross-database macros (`dbt.concat`, `dbt.dateadd`, `dbt.datediff`,
  `dbt.safe_cast`, `dbt.hash`, `dbt.type_string`, ...). Use `adapter.dispatch` for
  anything without a built-in macro. Do not use Snowflake-only or DuckDB-only syntax
  directly in a model, because the same model must run in both tiers.
- **`conditional`:** a `case` expression with cases in declared order and the
  `fallback` as `else`. Evaluation order is part of the contract.
- **`lookup`:** a join to the enum/reference model, or an inline `case` for inline
  lookups. Unmatched values follow the transformation's declared behaviour.
- **Identifier quoting:** source column names are used verbatim. Set
  `quoting: identifier: true` on sources whose columns are mixed case
  (e.g. Salesforce `ExternalPartyId`). Snowflake folds unquoted names to upper case
  and DuckDB does not, so unquoted mixed-case names behave differently in the two tiers.
- **Current time:** use a project macro (e.g. `{{ current_ts() }}`) rather than
  `current_timestamp` inline, so unit tests can override it.
- **Incremental models:** guard incremental logic with `is_incremental()` so unit
  tests can exercise both paths.

### Step 5 — Contracts and Constraints

Declare a model contract (`contract: {enforced: true}`) on canonical and product
models, with every column's `data_type`. Put constraints in the contract only where
both tiers enforce them. Declare everything else as a data test (Agent Test's part).

Constraint | Snowflake | DuckLake | Where it goes
--- | --- | --- | ---
`not_null` | Enforced | Enforced | Contract, unless the null strategy is `nullable-staging` or `nullable-final` (then data test on the converged view only)
Primary key / `unique` | Declared, not enforced | Not supported | Data test
Foreign key (relationship) | Declared, not enforced | Not supported | Data test (`relationships`)
`check` | Not supported | Not supported | Data test (`dbt_utils.expression_is_true` or singular)

For SCD2 and bitemporal entities, uniqueness applies to current rows only. Scope the
test with `where: "is_current"` rather than dropping it.

### Step 6 — Profiles for the Two Tiers

Local tier: dbt-core with the `dbt-duckdb` adapter and a DuckLake catalog. DuckLake
keeps table metadata in a catalog database and data as Parquet files, which is close
to how the cloud warehouse behaves while staying on a laptop.

```yaml
# profiles.yml (local target only; cloud target comes from the template / dbt Cloud)
<project_name>:
  target: local
  outputs:
    local:
      type: duckdb
      path: ":memory:"
      extensions: [ducklake]
      attach:
        - path: "ducklake:.ducklake/catalog.ducklake"
          alias: lake
          options:
            data_path: ".ducklake/data/"
      database: lake
      schema: "{{ env_var('DBT_SCHEMA', 'dev') }}"
      threads: 4
```

Confirm the `attach` syntax against the installed `dbt-duckdb` version, since
DuckLake support in the adapter is recent. Add `.ducklake/` to `.gitignore`.

Cloud tier: use the template's target unchanged. Never write credentials into
generated files. Point to the template's mechanism (env vars, dbt Cloud environment).

### Step 7 — Output

1. The project tree, with each file marked **new**, **from template**, or **template modified**.
2. Model and YAML files in fenced code blocks.
3. **Generation notes:** template profile, layer mapping, fan-out and fan-in models,
   contract vs test placement of each constraint, cross-dialect macros used,
   assumptions, and open questions.
4. Run instructions:

```bash
pip install dbt-core dbt-duckdb
dbt deps
dbt build --target local                      # models + data tests
dbt test --target local --select test_type:unit
```

---

## Boundary Rules

- The template wins. Where this skill and the template disagree, follow the template
  and record the difference in the generation notes.
- Models implement declared transformations only. A mapping that is not in transform
  detail or product attribute mapping is not generated. Flag it to Agent Ontology.
- No warehouse-specific SQL in models. Use cross-database macros or dispatch.
- No credentials in generated files.
- Generated files are regenerated from the spec. Hand-written models and tests go
  in files the generator does not own, as the template directs.
- Scheduling, orchestration, and deployment jobs are out of scope. Those are the
  platform's concern (dbt Cloud jobs, Airflow, etc.).

---

## Handoff

**Agent Artifact → Agent Test:** after generating or regenerating models, hand the
project to Agent Test to compile worked examples into unit tests and run the local
tier. Include the template profile and the constraint placement table.

**Agent Test → Agent Artifact:** when a unit test fails because the model does not
implement the declared transformation. Include the failing test, the worked example,
and the transformation YAML.

**Either → Agent Ontology:** when a transformation, fan-out, or worked example is
ambiguous or contradicts itself, so no correct model or test can be written.

---

## Limitations

- Snapshots cannot be unit tested in dbt. Temporal behaviour implemented as
  snapshots is covered by data tests only.
- Unit tests need the input relations' columns to exist. In the local tier, build
  upstream models with `--empty` first, and create source tables from the Source
  Schema table (Agent Test generates this).
- DuckLake does not enforce primary key, unique, or foreign key constraints, so
  these rely on data tests in the local tier, as they do on Snowflake.
- Masking policies, warehouse grants, and source freshness can only be verified
  in the cloud tier.
