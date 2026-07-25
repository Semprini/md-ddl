# MD‑DDL Specification (Draft 0.9.2)

*Part of the MD‑DDL Specification. See [1-Foundation.md](./1-Foundation.md) for core principles and document structure.*

---

## **Adoption**

MD-DDL supports incremental adoption. Organisations can begin by importing existing schemas — DDL, dbt models, catalog exports — and progressively evolve toward declarative, AI-generated artifacts. The primary brownfield path is **schema-import**: provide your existing DDL and receive a draft canonical domain. Baseline capture is an optional secondary path for organisations that need to document existing state before modelling.

This section defines only the structural shapes agents rely on: the adoption maturity vocabulary, the `adoption:` domain metadata block, and the `baseline:` file header. The adoption methodology — maturity model detail, advancement criteria, journey patterns, coexistence and cutover, drift detection, and portfolio-level adoption — lives in the non-normative [Adoption Playbook](../guides/adoption-playbook.md).

---

### **Adoption Maturity Vocabulary**

Maturity is tracked at the domain level; the domain advances as a whole. The `maturity` field uses these values:

Value | Meaning
--- | ---
`documented` | Existing state captured as baseline files; no canonical entities yet
`mapped` | Canonical entities defined; mappings derivable from source transforms
`governed` | Governance metadata complete on all canonical entities
`declarative` | MD-DDL is the source of truth; physical artifacts generated and drift-monitored
`automated` | CI/CD generates, deploys, and enforces from MD-DDL

See the [Adoption Playbook](../guides/adoption-playbook.md) for level characteristics, advancement criteria, and the regression and staleness rules.

---

### **Domain Adoption Metadata**

Domain metadata (defined in [Section 2 — Domains](./2-Domains.md)) is extended with an `adoption` block when a domain uses the brownfield adoption workflow.

```yaml
adoption:
  maturity: documented | mapped | governed | declarative | automated
  adoption_started: 2024-01-15
  target_maturity: declarative
  target_date: 2025-06-30
  progress:
    at_level: 12
    total: 15
  notes: "Phase 1 captured existing DW star schema. Next: complete governance metadata for Level 3."
```

Field | Required | Purpose
--- | --- | ---
`maturity` | Yes (when any baseline file exists) | Current adoption maturity level
`adoption_started` | Yes | ISO 8601 date when the first baseline was captured
`target_maturity` | No | The maturity level the domain is targeting
`target_date` | No | ISO 8601 date by which the target maturity should be reached
`progress` | No | Structured count of advancement within the current level. `at_level` is the number of entities/assets that have reached the current level's criteria. `total` is the total number of entities/assets in the domain. Agents use `at_level / total` to compute percentage and detect stalls.
`notes` | No | Free-text migration context

The `adoption` block is required once any baseline file exists in the domain. It is optional for greenfield domains that start directly at canonical modelling.

---

### **Baseline File Header**

The `baselines/` folder captures existing state documentation within a domain. Baseline files are reference documentation only — they are never used as inputs for physical artifact generation. Physical artifacts are generated exclusively from canonical entities in `entities/`.

Every baseline file begins with this metadata block, followed by a free-form body (verbatim DDL, column listings, pipeline descriptions — whatever best describes the existing asset):

```yaml
baseline:
  type: dimensional | canonical | etl | catalog
  source_system: "Snowflake DW" | "Informatica" | "Collibra" | etc.
  captured_date: 2024-01-15
  captured_by: "Jane Smith"
  status: active | superseded | archived
  superseded_by: "entities/customer.md"  # populated when superseded
```

- `type` identifies the baseline category and determines the subfolder under `baselines/`
- `source_system` names the platform or tool where the existing asset lives
- `captured_date` is the date the baseline was documented (ISO 8601)
- `captured_by` identifies who documented the baseline (person or agent)
- `status` tracks the baseline's lifecycle: `active` (in use), `superseded` (replaced by canonical entity), or `archived` (retained for history)
- `superseded_by` links to the canonical entity definition that replaced this baseline

Baseline files carry no `mapping:` blocks — baseline-to-canonical mappings are derived from source transform detail ([Section 8 — Transformations](./8-Transformations.md)), which defines the operational data flow. The transform *is* the mapping.

See the [Adoption Playbook](../guides/adoption-playbook.md) for the baseline folder structure, free-form body guidance, and how agents generate baselines and derive mapping views.

---

...next: [Foundation](1-Foundation.md)
