---
name: reconciliation
description: Use this skill when the user wants to compare generated MD-DDL artifacts with existing state, or when mentions "reconcile", "compare", "diff", "gap analysis", "check against existing", or when transitioning a domain from Level 3 (Governed) to Level 4 (Declarative) and needs to validate generated output against current physical assets.
---

# Skill: Reconciliation

Compares physical artifacts generated from canonical MD-DDL entities against
existing baseline documentation or deployed schemas. Produces a structured gap
report and recommends resolution for each difference.

## MD-DDL Reference

Load before responding:

- `md-ddl-specification/10-Adoption.md` — Adoption maturity model, coexistence
  and cutover rules, drift detection
- The applicable generation skill (`skills/dimensional/SKILL.md`,
  `skills/normalized/SKILL.md`, etc.) for producing the generated artifacts

---

## Process

### Step 1 — Identify Comparison Scope

Ask:

- Which domain and entities are being reconciled?
- What is being compared against? Options:
  - Baseline files in `baselines/` (documented existing state)
  - Live deployed schema (user provides current DDL)
  - Both
- What physical style was used for generation? (dimensional, normalized, etc.)

### Step 2 — Generate Physical Artifacts

Generate physical artifacts from the canonical MD-DDL model using the
appropriate generation skill (Dimensional, Normalized, Wide Column, or
Knowledge Graph). This produces the "target state" for comparison.

If artifacts have already been generated, use the existing output.

### Step 3 — Load Comparison Source

Load the comparison source:

- **From baselines:** Read the relevant `baselines/dimensional/`,
  `baselines/canonical/`, or other baseline files. Extract the column/attribute
  definitions from the type-specific YAML blocks.
- **From live DDL:** Parse the user-provided CREATE TABLE statements or
  schema descriptions.

### Step 4 — Produce Gap Report

Compare the generated artifacts against the comparison source. Report
differences in a structured table:

#### Gap Report Format

```markdown
## Reconciliation Report — [Domain Name]

**Generated from:** MD-DDL canonical model (entities/)
**Compared against:** [baselines/ | live DDL | both]
**Date:** [date]

### Summary

- Entities compared: [n]
- Exact matches: [n]
- Differences found: [n]
- New in generated (not in existing): [n]
- Missing from generated (in existing only): [n]

### Differences

Entity | Item | Type | In Generated | In Existing | Resolution
--- | --- | --- | --- | --- | ---
Customer | date_of_birth | Column type | DATE | VARCHAR(10) | Update source to use DATE
Customer | etl_batch_id | Column | Not present | Present | Technical column — exclude from canonical
Customer | Email Verified | Attribute | Present | Not present | New attribute added in canonical model
Sale | discount_pct | Column | DECIMAL(5,2) | DECIMAL(3,2) | Precision increase — intentional
```

#### Difference Types

Type | Description
--- | ---
Column present in existing but not generated | Potential missing entity/attribute in canonical model, or intentional exclusion (technical/audit column)
Column present in generated but not in existing | New addition from canonical model — expected for model extensions
Type mismatch | Data type differs between generated and existing
Constraint mismatch | Nullability, primary key, unique constraint, or foreign key differs
Name mismatch | Column/table naming convention differs (e.g., snake_case vs natural language)

### Step 5 — Recommend Resolution

For each gap, recommend one of:

Resolution | When to use
--- | ---
**Update canonical model** | Existing state reveals a missing attribute or relationship the canonical model should include
**Accept difference** | Difference is intentional (e.g., new attribute, improved data type, dropped technical column)
**Flag for SME review** | Difference is ambiguous — requires business context to resolve
**Update existing state** | Generated artifact is correct; existing state should be migrated

Present recommendations in the gap report table's Resolution column.

---

## Boundary Rules

- **This skill does not modify the canonical model.** If the reconciliation
  reveals gaps in the canonical model, recommend changes and defer to Agent
  Ontology for implementation.
- **This skill does not modify baseline files.** Baseline status updates
  (`superseded`, `archived`) are done by the user or by the baseline-capture
  skill after reconciliation is accepted.
- **This skill produces reports, not deployments.** The gap report is a
  decision-support artifact. Actual deployment or migration is outside
  MD-DDL's scope.

---

## Handoff

After reconciliation:

- **To fix canonical model gaps** → Agent Ontology (brownfield modelling)
- **To update baseline status** → baseline-capture skill
- **To proceed with deployment** → outside MD-DDL scope; user's CI/CD process
