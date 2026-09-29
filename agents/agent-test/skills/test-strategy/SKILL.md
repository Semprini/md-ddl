---
name: test-strategy
description: Use this skill at the start of any testing engagement, or when the user asks what to test, how much of a domain or data product is covered, which tests run locally versus in the cloud, "is this ready to test", "test coverage", "test plan", or "which worked examples are missing". Maps every testable MD-DDL declaration to a test, a tier, and an owner, and reports the gaps.
---

# Skill: Test Strategy

Decides which tests exist for a domain or data product, at which tier they run, and
what cannot be tested yet. Every test in the suite must trace back to an entry in the
map below.

## MD-DDL Reference

Load before responding:

- `md-ddl-specification/1-Foundation.md § Verification of Generated Artefacts`
- `md-ddl-specification/3-Entities.md`: identifiers, constraints, temporal tracking
- `md-ddl-specification/7-Sources.md`: Entity Fan-Out, Source Schema
- `md-ddl-specification/8-Transformations.md`: transformation types, Worked Examples, fan-in examples
- `md-ddl-specification/9-Data-Products.md`: SLA, masking, logical model

---

## Process

### Step 1 — Check Readiness

Apply the Model Readiness Definition from Agent Ontology's domain-review skill. A
model that is Not Ready produces tests for a moving target. List the blockers and
hand off to Agent Ontology before continuing.

Also check:

- `md-ddl lint` passes on the domain. A worked example with broken YAML can't be
  compiled faithfully.
- Generated models exist (or are about to), so tests have something to run against.
- The product declares a consistency posture and null strategy. Without them,
  `NOT NULL` placement is a guess. Hand off to Agent Architect.
- Source tables have `Open Decisions` entries. Any transformation blocked by an open
  decision is untestable until the decision is made. List these; do not guess.

### Step 2 — Build the Test Map

Walk the declarations in scope and map each one:

Declaration | Assertion | Level | Tier | Origin
--- | --- | --- | --- | ---
`##### Worked Examples` in transform detail | Given source rows produce exactly the listed instances and attribute values | Unit | Local + cloud | `worked-example`
Fan-in worked example (rows from several sources) | Contributions converge to the listed instance; `interim` states hold after each arrival | Unit (canonical model) | Local + cloud | `worked-example`
`Entity Fan-Out` `produces:` | Each produced entity has the declared cardinality per row; conditions route to the declared subtype | Unit (per branch) | Local + cloud | `derived` unless an example covers it
`conditional` / `lookup` transformation | Each case, and the fallback, maps as declared | Unit | Local + cloud | `derived` unless an example covers it
`deduplication` transformation | Each key branch derives the declared key; survivorship picks the declared row | Unit | Local + cloud | `derived` unless an example covers it
`identifier: primary` | Unique and not null (current rows only for SCD2 / bitemporal) | Data | Local + cloud | `declared`
Entity `constraints` (`not_null`, `unique`, `check`) | As declared | Data or contract | Local + cloud | `declared`
Enumeration-typed attribute | Values within the enum | Data | Local + cloud | `declared`
Relationship | Foreign key resolves (to the current parent row where temporal) | Data | Local + cloud | `declared`
`temporal.tracking` | Temporal chain rules: one current row, closed rows have `valid_to`, no inversions, no overlaps, monotonic `recorded_at` | Data (singular) | Local + cloud | `declared`
Transformation `quality_check` (default true) | Target attribute not null after transformation | Data | Local + cloud | `declared`
Product `sla.freshness` and consistency posture | Converged within the window; interim nulls only where the null strategy allows | Integration | Local (synthetic lag) + cloud (source freshness) | `declared`
Product `masking` | Restricted role sees masked values | Integration | Cloud only | `declared`
Product logical model / attribute mapping | Model columns and types match the contract | Contract | Local + cloud | `declared`

Worked examples outrank derived tests. Where a worked example covers the same case
as a derived test, keep the worked example and drop the derived one. They would
assert the same thing, and the example is the contract.

### Step 3 — Find the Gaps

The spec asks for examples that cover every case where the model can be read two
ways (8-Transformations § Worked Examples). Check, for each source table:

Case | Gap if
--- | ---
Each `condition` in Entity Fan-Out | No example routes a row through that branch
Each `deduplication` key branch | No example exercises that branch, or no example has two rows merging
Each `conditional` case and the `fallback` | Case has no example and no derived test
`cardinality: 0..1` / `0..*` | No example shows the zero case
Evaluation order that matters | No example where two cases both match
Entity fed by more than one source | No fan-in example
Entity whose product declares eventual consistency | Fan-in example has no `interim` states

Gaps in the first column of Step 2 are the domain's to fill. You may draft
examples as proposals, but hand them to Agent Ontology for the domain to accept.

### Step 4 — Assign Tiers

Tier | Runs | Contains | Data
--- | --- | --- | ---
Local | Laptop and CI, dbt-core + DuckLake | Unit tests, data tests, contracts, temporal tests, convergence tests on synthetic lag | Worked-example fixtures; Faker data for volume
Cloud | dbt Cloud + warehouse | Everything local, plus masking, grants, source freshness, warehouse-enforced constraints | Warehouse dev/test environment

Tag cloud-only tests (`tags: [cloud_only]`) and exclude them from the local selector.
Do not write separate local and cloud versions of the same test.

### Step 5 — Output the Coverage Report

```markdown
## Test Coverage — [Product or Domain]

### Summary
Declarations in scope: N | Testable now: N | Blocked: N | Gaps: N

### Test Map
Declaration | Test | Level | Tier | Origin | Status (ready / blocked / gap)

### Gaps
- [source table] · [branch or case] — no worked example. Proposed example: (draft YAML)

### Blocked
- [declaration] — blocked by [Open Decision / missing posture / Not Ready item]
```

---

## Boundary Rules

- Every test traces to a declaration. Hand-written tests are allowed but live
  outside generated files and are listed separately.
- A coverage gap is reported, never silently filled with a derived test that
  pretends to be a contract.
- Local and cloud tiers run the same tests. Tier differences are tags, not copies.
