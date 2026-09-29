---
name: worked-example-compilation
description: Use this skill when the user asks to turn MD-DDL worked examples into tests, generate dbt unit tests or fixtures from transform detail, test a fan-out or fan-in, check that worked examples agree with their transformations and Entity Fan-Out, or draft missing worked examples. Also use when the user says "compile the examples", "unit tests from the spec", "fixtures", or "given / produces".
---

# Skill: Worked Example Compilation

Compiles `##### Worked Examples` from transform detail into executable tests. A worked
example is a contract: a source row, or several, and the exact canonical instances
they must produce (8-Transformations § Worked Examples). Compilation must keep that
contract intact. Nothing is added to it, and no assertion is weakened.

The default target is a dbt project generated with the shared dbt-project skill
(`../../../agent-artifact/skills/dbt-project/SKILL.md`). The consistency checks and the
example-to-assertion mapping do not depend on dbt and apply to any harness.

## MD-DDL Reference

Load before responding:

- `md-ddl-specification/8-Transformations.md § Worked Examples`, including fan-in examples
- `md-ddl-specification/7-Sources.md § Entity Fan-Out`
- The transform detail files for every source table in scope
- The generated project's model YAML, whose `meta.md_ddl` entries map declarations to models and columns

---

## Process

### Step 1 — Check Each Example Against Its Declarations

Before compiling, confirm the example is consistent with the model. An inconsistent
example is a declaration defect. Report it to Agent Ontology. Do not compile around it.

Check | Defect if
--- | ---
`produces` entities | An entity the source table's Entity Fan-Out does not declare (spec validation error)
`given` columns | A column not in the source table's Source Schema
`produces` attributes | An attribute not declared on the entity or inherited from its parent
Enum-typed attribute values | A value not in the enum
Fan-out conditions | The `given` row satisfies a different branch from the one the example produces
Cardinality | More instances of an entity than its fan-out `cardinality` allows
Fan-in `from` references | A source or table heading that does not resolve, or a contributing source whose Entity Fan-Out does not declare the entity

Also compare the example with the transformation YAML. If working through the YAML
by hand gives a different value from the one the example states, one of them is
wrong. Report both. Do not choose between them.

### Step 2 — Choose the Test Form

Example | Test form | Why
--- | --- | ---
Single source table, no source idiosyncrasy involved | **Unit test** per produced entity, on the intermediate model | Fast, isolated, one model per test
Depends on `null_as`, `format`, or `normalise` handling | **Unit test on the staging model** plus a unit test on the intermediate model, chained by the staging expectation | The idiosyncrasy lives in staging
`given` is a list of rows from one table (deduplication) | Unit test with all rows as input | Merge and survivorship are within one model
Fan-in (`given` entries with `from:`) | **Fixture test** through the whole chain | Rows cross several models; a dbt unit test covers only one model
Fan-in with `interim` states, or incremental / SCD2 behaviour | Fixture test, one build per arrival step | Each step is a real incremental run

### Step 3 — Compile Unit Tests

For each produced entity in the example, one `unit_tests` entry on the model that
emits that entity from this source table:

```yaml
unit_tests:
  - name: address__individual_with_dpid_matched_residential_address
    model: int_postal_address__crm_address
    description: >
      Party is abstract, so the concrete instance is an Individual, selected by the
      OWNER_TYPE_ENUM condition in Entity Fan-Out.
    config:
      tags: [md_ddl, worked_example]
      meta:
        md_ddl:
          declaration: sources/crm/table_ADDRESS.md#worked-examples
          example: Individual with a DPID-matched, customer-confirmed residential address
          origin: worked-example
    given:
      - input: ref('stg_crm__address')
        rows:
          - {ADDRESS_ID: "3f2b-aaa1", OWNER_ID: "8c14-p001", OWNER_TYPE_ENUM: 1, DPID_N: "1234567"}
    overrides:
      macros:
        current_ts: "'2026-01-01 00:00:00'"
    expect:
      rows:
        - {address_identifier: "DPID:1234567", delivery_point_id: 1234567}
```

Rules:

- **Name:** `<entity>__<example slug>`. The example name is unique within a source table.
- **`description`:** the example's `notes`, so a failure explains itself.
- **`given`:** source column names verbatim, only the columns the example lists. dbt
  fills the rest with nulls. If the template renames columns in staging, translate
  through the staging model's rename map and say so in the test description.
- **`expect`:** only the attributes the example lists, as column names from the
  model's `meta.md_ddl` mapping. Values are copied verbatim. Enum values use the
  stored representation (label or code), per the enum strategy in Agent Artifact's
  generation notes.
- **Entities the example does not list:** if the fan-out entry has a `condition` or a
  `0..` cardinality, compile a test on that entity's model with `expect: rows: []`.
  The example routes around it. If the fan-out entry has cardinality `1`, do not
  assert. Flag the example as incomplete instead.
- **`cardinality` stated in the example:** expect exactly that many rows.
- **Time:** override the project's current-time macro with a fixed value. Never let
  an expected value depend on the clock.
- **Incremental models:** compile the non-incremental path. Add an
  `is_incremental: true` variant only when the example is about incremental behaviour.

Generated unit tests go in `_<model>__unit_tests.yml` next to the model, or wherever
the template puts them. These files are regenerated from the spec and are never
hand-edited.

### Step 4 — Compile Fixture Tests (Fan-In and Interim States)

A fan-in example lists rows from several source tables, in arrival order, and the
single instance they converge to. `interim` entries give the instance's state
after the first *n* arrivals. See 8-Transformations § Fan-in examples.

Generate, per example:

1. **Fixture rows:** one CSV per source table under
   `fixtures/<example slug>/<source_id>__<table>.csv`, with an `_arrival` column
   holding each row's position in `given`.
2. **Expected state per step:** `fixtures/<example slug>/expected__step_<n>.csv`
   for each `interim` entry, plus the final `produces` as the last step.
3. **Assertion:** a singular test per step comparing the canonical model with the
   expected state in both directions (`except` both ways), limited to the
   example's identifiers and the attributes the example lists. Tag it
   `fixture__<example slug>__step_<n>`.
4. **Runner:** `fixtures/run_fixtures.py` (Python stdlib + the `duckdb` package)
   that, for each step, loads the rows with `_arrival <= n` into the local-tier
   source tables, runs `dbt build --target local --select +<canonical model>`, then
   `dbt test --select tag:fixture__<example slug>__step_<n>`.

Examples do not share identifiers, so all examples' fixtures can be loaded together
per step. If two examples use the same identifier, report it. It is almost always
an authoring mistake.

Where an `interim` state asserts `null` for an attribute that has not arrived yet,
check it against the product's null strategy. `reject-partial` means the instance
must not exist yet, so compile the interim step as zero rows and flag the example
if it says otherwise.

### Step 5 — Draft Missing Examples (Proposals Only)

For each gap in the Test Strategy coverage report, draft an example in the spec
format, working the expected values from the transformation YAML by hand and
showing the working in `notes`. Label every draft **Proposed — not a contract until
accepted**. Hand drafts to Agent Ontology. Drafts are never compiled as
`worked-example` tests. Until accepted, the same case is covered by a `derived` test.

### Step 6 — Output

1. Consistency findings from Step 1, each with declaration path and a proposed owner.
2. Generated test files.
3. A compilation table: example → tests generated → form → tier.
4. Proposed examples, clearly labelled.

---

## Boundary Rules

- Never change an expected value to match generated output. Only the domain changes a contract.
- Never compile an example that fails Step 1. Report it instead.
- Assert only what the example states. Extra assertions belong in `derived` or
  `declared` tests, not inside a compiled example.
- Drafted examples are proposals until the user accepts them into transform detail.
