# MD‑DDL Specification (Draft 0.9.0)

*Part of the MD‑DDL Specification. See [1-Foundation.md](./1-Foundation.md) for core principles and document structure.*

---

## **Adoption**

MD-DDL supports incremental adoption. Organisations can begin by importing existing schemas — DDL, dbt models, catalog exports — and progressively evolve toward declarative, AI-generated artifacts. The `baselines/` folder captures existing state for reference; the adoption maturity model tracks the journey; the canonical model is the destination.

The primary brownfield path is **schema-import**: paste your DDL, answer two or three questions, and receive a draft canonical domain. Baseline capture is an optional secondary path for organisations that need to document existing state before modelling.

Coexistence between baseline documentation and canonical entities is transitional. The goal is always full conversion to declarative MD-DDL, but the timeline may span months or years depending on organisational readiness, domain complexity, and the number of existing systems to absorb.

---

### **Adoption Maturity Model**

Maturity is tracked at the domain level. Individual entities do not carry their own maturity — the domain advances as a whole. Domain maturity equals the lowest level all entities have reached. The `progress` field in domain metadata shows forward momentum within a level as a structured count.

#### Maturity Levels

Level | Name | Description | Characteristics
--- | --- | --- | ---
1 | Documented | Existing state captured as MD-DDL baseline files | `baselines/` folder populated; no canonical entities yet; existing schemas, ETLs, catalog entries recorded as-is
2 | Mapped | Canonical entities defined; mappings derivable from source transforms | `entities/` folder populated; `sources/` with transform files define the lineage from source fields to canonical attributes; baseline-to-canonical mappings are auto-generated from transforms, not manually authored
3 | Governed | Governance metadata complete on all canonical entities | Classification, PII, retention, regulatory scope, compliance relevance all populated; domain review passed
4 | Declarative | MD-DDL is the source of truth; physical artifacts generated and drift-monitored | Agent Artifact generates DDL/schemas from MD-DDL; existing physical artifacts replaced or reconciled; baselines superseded; basic drift detection flags divergence between declarations and deployed state. **Requires external tooling** — drift detection mechanisms (CI/CD hooks, database introspection, scheduled agent runs) must be implemented outside MD-DDL
5 | Automated | CI/CD generates, deploys, and enforces from MD-DDL | Pipeline generates, deploys, and monitors physical artifacts; automated drift detection with remediation triggers; baseline folder can be removed. **Requires external tooling** — CI/CD pipeline integration, automated deployment, and remediation infrastructure must be implemented outside MD-DDL

#### Advancement Criteria

Each level has explicit exit criteria that must be satisfied before advancing. These are structural checks (verifiable by agents) plus SME attestations.

**Level 1 → Level 2:**

- All known existing assets documented as baseline files in `baselines/`
- Each baseline file has the required `baseline:` metadata header
- Domain metadata contains an `adoption` block with `maturity: documented`
- Candidate canonical entities identified (documented in baseline file notes or a separate assessment)

**Level 2 → Level 3:**

- Canonical entity files exist in `entities/` for all business concepts identified from baselines
- Source transform files in `sources/*/transforms/` define mappings from source fields to canonical attributes (see [Section 8 — Transformations](./8-Transformations.md))
- Domain metadata updated to `maturity: mapped`

**Level 3 → Level 4:**

- All canonical entities have complete governance metadata (classification, PII, retention, regulatory scope)
- Domain review passed (Agent Ontology domain-review skill)
- Domain metadata updated to `maturity: governed`

**Level 4 → Level 5:**

- Agent Artifact generates physical artifacts from canonical entities
- Generated artifacts reconciled against existing state — differences are intentional
- Baseline files marked `status: superseded` with `superseded_by:` pointing to canonical entities
- Basic drift detection in place: divergence between MD-DDL declarations and deployed physical state is flagged
- External tooling operational for drift detection
- Domain metadata updated to `maturity: declarative`

**Level 5 exit (Automated):**

- CI/CD pipeline generates, deploys, and monitors physical artifacts from MD-DDL
- Automated drift detection with remediation triggers operational
- Baseline files may be `status: archived` or removed entirely
- External tooling operational for deployment and remediation
- Domain metadata updated to `maturity: automated`

#### Regression Rules

A domain cannot regress to a lower maturity level. If structural changes invalidate a level (e.g., new entities added without governance), the domain stays at its current level but is flagged as "incomplete at current level" until gaps are resolved.

#### Staleness Rule

If a domain's `target_date` has passed and `maturity` has not reached `target_maturity`, agents flag the domain as "adoption stalled." The adoption-planning skill prompts a review: reassess timeline, identify blockers, or adjust target. This prevents Level 1 sprawl where teams document legacy but never progress.

---

### **Baselines**

The `baselines/` folder captures existing state documentation within a domain. Baseline files are reference documentation only — they are never used as inputs for physical artifact generation. Agent Artifact generates exclusively from canonical entities in `entities/`.

**Baselines are agent-generated, not human-authored.** Users provide raw input — DDL, dbt models, catalog exports, pipeline descriptions, natural-language notes — and the agent produces the baseline file. The human effort is providing the raw material; the structuring is the agent's job.

#### Folder Structure

```text
<domain>/
  domain.md
  baselines/                    # Existing state documentation
    dimensional/                # Existing dimensional models
      fact_transaction.md       # Star schema fact table documented
      dim_customer.md           # Dimension table documented
    canonical/                  # Existing enterprise/canonical models
      enterprise_customer.md    # Existing canonical entity documented
    etl/                        # Existing ETL/ELT pipeline inventory
      customer_load.md          # Pipeline documented
    catalog/                    # Governance catalog imports
      customer_governance.md    # Collibra/Purview metadata captured
  entities/
  sources/
  ...
```

#### Baseline File Format

Each baseline file has two parts: a short YAML metadata header and a free-form body. There are no type-specific YAML templates — the body holds whatever content best describes the existing asset.

##### Metadata Header

Every baseline file must include this metadata block:

```yaml
baseline:
  type: dimensional | canonical | etl | catalog
  source_system: "Snowflake DW" | "Informatica" | "Collibra" | etc.
  captured_date: 2024-01-15
  captured_by: "Jane Smith"
  status: active | superseded | archived
  superseded_by: "entities/customer.md"  # populated at Level 4+
```

- `type` identifies the baseline category and determines the subfolder
- `source_system` names the platform or tool where the existing asset lives
- `captured_date` is the date the baseline was documented (ISO 8601)
- `captured_by` identifies who documented the baseline (person or agent)
- `status` tracks the baseline's lifecycle: `active` (in use), `superseded` (replaced by canonical entity), or `archived` (retained for history)
- `superseded_by` links to the canonical entity file that replaced this baseline (populated at Level 4+)

##### Free-Form Body

Below the metadata header, the body may contain any combination of:

- Verbatim DDL in fenced code blocks (CREATE TABLE, ALTER TABLE, etc.)
- dbt model SQL or schema.yml excerpts
- Column listings (as Markdown tables, YAML, or plain text)
- Catalog export data (classification, ownership, quality scores, lineage)
- ETL/pipeline descriptions (schedule, dependencies, transformation logic)
- Known data quality issues
- Business context, historical notes, ERD fragments

The format is deliberately flexible. Agents parse the body to extract structured information when needed — humans should not be required to structure it manually. Paste what you have; the agent handles the rest.

##### What Baselines Do NOT Contain

- **No type-specific YAML templates.** Earlier versions of this spec defined `dimensional:`, `canonical:`, `etl:`, and `catalog:` YAML blocks. These are no longer required. If an agent generates structured YAML from raw input, it appears in the free-form body as documentation — not as a required schema.
- **No mapping blocks.** Baseline-to-canonical mappings are derived from source transforms (see below). Baselines do not carry `mapping:` blocks.

---

### **Mapping: Auto-Generated from Source Transforms**

When a domain advances from Level 1 (Documented) to Level 2 (Mapped), the intellectual translation from existing assets to canonical entities is captured in **source transform files** ([Section 8 — Transformations](./8-Transformations.md)), not in baseline mapping blocks.

This means mappings are derived from operational data flow definitions — the same transforms that will eventually generate ETL/ELT code. There is no separate "mapping" artifact to maintain.

#### How Mappings Are Derived

Source transform files in `sources/*/transforms/` define how source system fields map to canonical entity attributes. Each transform's `target` field points to a canonical attribute; each transform's `source` field points to a source system field. Together, these define the complete lineage from source to canonical model.

For brownfield adoption, agents parse existing ETL logic to **propose** transform files:

Input format | What the agent parses | Output
--- | --- | ---
SQL (SELECT, INSERT, MERGE) | Column aliases, JOIN conditions, WHERE filters, CASE expressions | `direct`, `derived`, `lookup`, `conditional` transforms
dbt models (SQL + schema.yml) | ref() calls, column descriptions, tests, source() macros | Transforms + source declarations
Stored procedures | Parameter mappings, cursor logic, conditional branches | Transforms with `derived` and `conditional` types
Informatica / SSIS mappings | Source-to-target field maps, expression transforms, lookup transforms | Transforms matching the ETL tool's logic
Natural-language descriptions | Entity and field references, business rules | Draft transforms marked with `# INFERRED` comments

The agent produces draft transform files from existing ETL code. The human reviews and refines. This replaces the manual `mapping:` block — the transform file *is* the mapping, and it is also the specification for generating new ETL code.

#### Reconciling Baseline Fields to Canonical Attributes

To understand how a baseline's columns relate to canonical attributes, agents read the transform files and produce a **mapping view** on demand. This is a generated report, not a stored artifact:

```text
Baseline: baselines/dimensional/fact_transaction.md
Canonical Entity: Transaction

Baseline Column     | Transform Type | Canonical Attribute     | Transform File
---                 | ---            | ---                     | ---
transaction_id      | direct         | Transaction Identifier  | sources/cbs/transforms/table_transactions.md
customer_key        | lookup         | Customer                | sources/cbs/transforms/table_transactions.md
amount              | direct         | Amount                  | sources/cbs/transforms/table_transactions.md
risk_score          | conditional    | Risk Rating             | sources/cbs/transforms/table_transactions.md
etl_batch_id        | —              | (unmapped: technical)   | —
dw_load_timestamp   | —              | (unmapped: technical)   | —
```

This view is generated by cross-referencing baseline column names against transform source fields. It is not stored in baseline files — it is computed when needed.

---

### **Adoption Journey Patterns**

Four starting-point patterns cover the most common brownfield scenarios. **Pattern A is the recommended default** — most brownfield adoptions start with existing schemas.

#### Pattern A: Starting from Existing Schemas (Primary Path)

1. Provide existing DDL, dbt models, or schema descriptions to the **schema-import** skill
2. Agent infers canonical entities, relationships, and enums — asks 2-3 clarifying questions
3. Review and refine the draft canonical model
4. Provide existing ETL code (SQL, dbt, stored procedures) — agent generates draft transform files
5. Review transforms; agent produces a mapping view showing baseline-to-canonical coverage
6. Establish governance metadata
7. Use Agent Artifact to generate new physical artifacts from canonical model
8. Reconcile generated vs existing — iterate until equivalent
9. Cut over to MD-DDL-generated artifacts

#### Pattern B: Starting from Existing Canonical/Enterprise Models

1. Document existing canonical model as `baselines/canonical/` files
2. Translate canonical entities to MD-DDL entity files (may be 1:1 or require restructuring)
3. Validate against MD-DDL rules (attribute types, constraints, relationships)
4. Map source systems via transform files
5. Establish governance metadata
6. Generate physical artifacts and reconcile with existing

#### Pattern C: Starting from ETL/ELT Pipelines

1. Document existing pipelines as `baselines/etl/` files
2. Agent parses pipeline logic to extract entity patterns and propose transform files
3. Create canonical entities from the target patterns
4. Review and refine generated transforms
5. Map source systems from pipeline sources
6. Generate physical artifacts from canonical model

#### Pattern D: Starting from Governance Catalog

1. Export governance metadata as `baselines/catalog/` files
2. Use classification, PII, ownership as seed data for domain and entity governance blocks
3. Create canonical entities using catalog entity/table definitions
4. Map source systems using catalog lineage; create transform files
5. Generate physical artifacts from canonical model

---

### **Coexistence and Cutover**

- **Coexistence is transitional** — the goal is always to reach Declarative or Automated maturity
- While at maturity levels 1–3, both baseline files and canonical entities may coexist
- At level 4 (Declarative), baseline files should be marked `status: superseded` with `superseded_by:` pointing to the canonical entity
- At level 5 (Automated), baseline files may be `status: archived` or removed entirely
- **No generation from baselines** — baselines are documentation only; Agent Artifact only generates from canonical entities in `entities/`
- **Reconciliation** — at the level 3→4 transition, generated artifacts must be compared against existing state; differences must be intentional

---

### **Drift Detection**

Drift detection becomes relevant at Level 4 (Declarative) when MD-DDL becomes the source of truth.

#### Level 4 — Basic Drift Detection

At Declarative maturity, the domain must have a mechanism to detect divergence between MD-DDL declarations and deployed physical state. The spec defines *what* drift means; the *mechanism* (CI/CD hooks, database introspection scripts, scheduled agent runs) is left to implementers since MD-DDL has no runtime.

Drift exists when:

- A deployed schema contains columns, tables, or constraints not declared in the MD-DDL model
- The MD-DDL model declares attributes, entities, or constraints not present in the deployed schema
- Data types, nullability, or constraint definitions differ between declaration and deployment

When drift is detected, it should be flagged with:

- The entity or attribute where drift occurred
- The nature of the divergence (added, removed, modified)
- A timestamp of when drift was detected

#### Level 5 — Automated Drift Enforcement

At Automated maturity, drift detection is integrated into CI/CD with remediation triggers:

- Drift detection runs automatically on deployment and on a schedule
- Detected drift blocks deployment or triggers automated remediation
- Drift history is retained for audit

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

### **Portfolio-Level Adoption**

Large enterprises may adopt MD-DDL domain-by-domain over months or years. Each domain tracks its own maturity independently. A portfolio-level adoption view can be assembled by reading all `domain.md` files and aggregating their `adoption` blocks. No portfolio-level metadata structure is defined in this version of the spec — this is deferred to a future version if demand warrants it.

---

### **Adoption Rules**

1. **Maturity is domain-level.** Entities do not individually track maturity. The domain advances as a whole. Domain maturity equals the lowest level all entities have reached.

2. **Baselines are documentation, not generation inputs.** Agent Artifact never generates from baselines. They are reference material for humans and for the reconciliation skill.

3. **Baselines are agent-generated.** Users provide raw input (DDL, dbt models, catalog exports, descriptions). Agents produce the structured baseline file. Humans should not be expected to author YAML templates manually.

4. **Coexistence is transitional.** Baselines exist to be superseded. The goal is always Declarative or Automated. Baseline files progress through `active` → `superseded` → `archived`.

5. **No regression.** A domain cannot move to a lower maturity level. New entities or structural changes that create gaps are flagged as "incomplete at current level."

6. **Mappings are derived from transforms.** Baseline-to-canonical mappings are not manually authored. They are derived from source transform files ([Section 8](./8-Transformations.md)) which define the operational data flow. The transform file *is* the mapping.

7. **Schema-import is the primary brownfield path.** For organisations with existing schemas (DDL, dbt, catalog exports), schema-import produces a draft canonical model directly. Baseline-capture is an optional secondary path for audit, history, or when no schema is available.

8. **Staleness prevents adoption decay.** Domains with a `target_date` that has passed without reaching `target_maturity` are flagged as "adoption stalled."

9. **Drift detection starts at Level 4.** When MD-DDL becomes the source of truth, basic drift detection is required to maintain that status. Level 5 upgrades to automated enforcement.

10. **Levels 4–5 require external tooling.** MD-DDL has no runtime. Drift detection, CI/CD integration, and automated deployment require tooling outside the spec. The spec defines what these levels mean; implementers build the infrastructure.

---

...next: [Foundation](1-Foundation.md)
