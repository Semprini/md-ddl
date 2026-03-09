# Plan: Brownfield Adoption for MD-DDL

## TL;DR

Extend the MD-DDL standard with a formal adoption maturity model, a `baselines/` folder structure for documenting existing state (dimensional models, ETL/ELT, canonical models, catalog metadata), and domain-level maturity tracking that guides organisations from "documented existing state" to "fully declarative." Add a new spec section (10-Adoption.md), extend domain metadata, and create new agent skills for baseline capture and adoption planning. Coexistence is transitional — the goal is always full conversion, but the timeline may span months/years.

---

## Phase 1: Spec — New Section 10-Adoption.md

This is the foundational spec work. Everything else builds on top of it.

### Step 1: Write 10-Adoption.md — Adoption Maturity Model

Create `md-ddl-specification/10-Adoption.md` defining:

**1.1 Adoption Maturity Levels (domain-level)**

Level | Name | Description | Characteristics
--- | --- | --- | ---
1 | Documented | Existing state captured as MD-DDL baseline files | `baselines/` folder populated; no canonical entities yet; existing schemas, ETLs, catalog entries recorded as-is
2 | Mapped | Canonical entities defined, structured mappings from baseline → canonical established | `entities/` folder populated; `sources/` may exist; baseline files carry a `mapping` block linking baseline columns/fields to canonical entity attributes
3 | Governed | Governance metadata complete on all canonical entities | Classification, PII, retention, regulatory scope, compliance relevance all populated; domain review passed
4 | Declarative | MD-DDL is the source of truth; physical artifacts generated and drift-monitored | Agent Artifact generates DDL/schemas from MD-DDL; existing physical artifacts replaced or reconciled; baselines superseded; basic drift detection flags divergence between declarations and deployed state
5 | Automated | CI/CD generates, deploys, and enforces from MD-DDL | Pipeline generates, deploys, and monitors physical artifacts; automated drift detection with remediation triggers; baseline folder can be removed

**1.2 Advancement criteria** — each level has explicit "exit criteria" that must be satisfied before advancing. These are structural checks (verifiable by agents) plus SME attestations.

**1.3 Regression rules** — a domain cannot regress to a lower maturity level. If structural changes invalidate a level (e.g., new entities added without governance), the domain stays at its current level but is flagged as "incomplete at current level" until gaps are resolved.

### Step 2: Define the baselines/ folder structure

Within 10-Adoption.md, define the `baselines/` construct:

```
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

**Baseline file format rules:**

- Each baseline file uses a simplified Markdown structure (not full MD-DDL entity YAML) because the goal is documentation, not generation
- Required metadata per baseline file:

```yaml
baseline:
  type: dimensional | canonical | etl | catalog
  source_system: "Snowflake DW" | "Informatica" | "Collibra" | etc.
  captured_date: 2024-01-15
  captured_by: "Jane Smith"
  status: active | superseded | archived
  superseded_by: "entities/customer.md"  # link to canonical entity once translated
```

- Body contains: schema documentation (CREATE TABLE or natural-language description), column/attribute listing, known quality issues, transformation logic (for ETL baselines), governance metadata (for catalog baselines)
- Baseline files are NOT used for generation — they are reference documentation only
- Format should be flexible enough to capture DDL verbatim (in fenced code blocks), metadata from catalogs, or natural-language descriptions of pipelines

**Baseline type templates:**

Each baseline type has a **required YAML block** that agents and reviewers can parse reliably, plus free-form Markdown documentation below it. The YAML block ensures consistency across teams; the Markdown body allows capturing context that doesn't fit a schema.

**Dimensional baseline:**

Required YAML:
```yaml
dimensional:
  table: fact_transaction
  schema: analytics
  database: snowflake_dw
  grain: "One row per transaction line item"
  columns:
    - name: transaction_id
      type: bigint
      nullable: false
    - name: customer_key
      type: bigint
      nullable: false
    - name: amount
      type: decimal(18,2)
      nullable: true
  dimensions:
    - dim_customer (customer_key)
    - dim_date (transaction_date_key)
  load_frequency: daily
  sla: "Available by 06:00 UTC"
```

Free-form body: known data quality issues, business context, historical notes, verbatim DDL in fenced code blocks.

**Canonical baseline:**

Required YAML:
```yaml
canonical:
  entity: Customer
  model: "Enterprise Data Model v3.2"
  attributes:
    - name: Customer ID
      type: string
      identifier: true
    - name: Full Name
      type: string
    - name: Date of Birth
      type: date
      pii: true
  relationships:
    - "Customer has many Accounts"
    - "Customer belongs to one Segment"
```

Free-form body: business rules, derivation logic, known governance metadata, ERD fragments.

**ETL baseline:**

Required YAML:
```yaml
etl:
  pipeline: daily_customer_load
  tool: dbt
  source: salesforce_crm.account
  target: analytics.dim_customer
  schedule: "daily 02:00 UTC"
  sla: "Complete by 04:00 UTC"
  dependencies:
    - staging_account_extract
```

Free-form body: transformation logic (verbatim SQL/dbt model or natural-language description), known issues, technical debt.

**Catalog baseline:**

Required YAML:
```yaml
catalog:
  tool: Collibra
  asset: Customer
  classification: Confidential
  pii: true
  data_owner: "Jane Smith"
  data_steward: "Bob Jones"
  quality_score: 0.87
  lineage:
    - "Salesforce CRM → Staging → DW → Customer dimension"
```

Free-form body: data quality rules, additional lineage detail, certification history.

### Step 2b: Define the mapping block for Level 1→2 transition

When a domain advances from Level 1 (Documented) to Level 2 (Mapped), each baseline file gains a `mapping` block that structurally links baseline columns/fields to canonical entity attributes. This replaces the unstructured "mapping notes" concept with a traceable, agent-parseable record of the intellectual translation.

Add a `mapping` block to the baseline metadata:

```yaml
baseline:
  type: dimensional
  source_system: "Snowflake DW"
  captured_date: 2024-01-15
  captured_by: "Jane Smith"
  status: active | superseded | archived
  superseded_by: "entities/customer.md"

mapping:                            # Added at Level 2 (Mapped)
  target_entity: Customer
  field_mappings:
    - baseline_field: customer_key
      canonical_attribute: Customer Identifier
      notes: "Surrogate key; natural key is customer_id"
    - baseline_field: full_name
      canonical_attribute: Full Name
    - baseline_field: dob
      canonical_attribute: Date of Birth
      notes: "Format differs: source uses MM/DD/YYYY"
  unmapped_fields:
    - etl_batch_id               # Technical field, no canonical equivalent
    - dw_load_timestamp          # Technical field
  coverage: "12/14 fields mapped"
```

Rules:
- `mapping` is optional at Level 1, required at Level 2+
- `target_entity` links to the canonical entity file this baseline translates to
- `field_mappings` is an array of baseline→canonical attribute pairs with optional notes
- `unmapped_fields` lists baseline fields that have no canonical equivalent (technical columns, audit fields, etc.) — this makes intentional exclusions explicit
- `coverage` is a human-readable summary of mapping completeness
- This is distinct from source→canonical transforms (Section 8) — those define the operational data flow; the mapping block documents the design translation from existing artifact to canonical model

### Step 3: Extend domain metadata in 2-Domains.md

Add `adoption` block to domain metadata schema:

```yaml
adoption:
  maturity: documented | mapped | governed | declarative | automated
  adoption_started: 2024-01-15
  target_maturity: declarative
  target_date: 2025-06-30
  progress: "12/15 entities governed"
  notes: "Phase 1 capturing existing DW star schema. Target Q2 2025 for declarative."
```

Rules:
- `maturity` is required once any baseline file exists in the domain
- `adoption_started` is when the first baseline was captured
- `target_maturity` and `target_date` are optional planning fields
- `progress` is an optional free-text indicator showing advancement within the current level (e.g., "12/15 entities governed" at level 3, or "8/10 baselines mapped" at level 2). Keeps domain maturity = lowest level all entities have reached while showing forward momentum.
- `notes` is free-text for migration context
- **Staleness rule:** if `target_date` has passed and `maturity` has not reached `target_maturity`, agents flag the domain as "adoption stalled." The adoption-planning skill prompts a review: reassess timeline, identify blockers, or adjust target.

### Step 4: Define the adoption journey patterns

Within 10-Adoption.md, define the four starting-point patterns:

**Pattern A: Starting from Dimensional Models**
1. Document existing star schema as `baselines/dimensional/` files
2. Identify business entities behind facts and dimensions → create `entities/`
3. Map dimensional columns back to canonical attributes
4. Document existing ETL as `baselines/etl/` (what populates the star schema)
5. Create source declarations for operational systems feeding the ETL
6. Establish governance metadata
7. Use Agent Artifact to generate new physical artifacts from canonical model
8. Reconcile generated vs existing dimensional model — iterate until equivalent
9. Cut over to MD-DDL-generated artifacts

**Pattern B: Starting from Existing Canonical/Enterprise Models**
1. Document existing canonical model as `baselines/canonical/` files
2. Translate canonical entities to MD-DDL entity files (may be 1:1 or require restructuring)
3. Validate against MD-DDL rules (attribute types, constraints, relationships)
4. Map source systems
5. Establish governance metadata
6. Generate physical artifacts and reconcile with existing

**Pattern C: Starting from ETL/ELT Pipelines**
1. Document existing pipelines as `baselines/etl/` files
2. Extract entity patterns from pipeline targets (what tables do the pipelines populate?)
3. Create canonical entities from the target patterns
4. Convert ETL logic to MD-DDL transformation YAML
5. Map source systems from pipeline sources
6. Generate physical artifacts from canonical model

**Pattern D: Starting from Governance Catalog**
1. Export governance metadata as `baselines/catalog/` files
2. Use classification, PII, ownership as seed data for domain and entity governance blocks
3. Create canonical entities using catalog entity/table definitions
4. Map source systems using catalog lineage
5. Generate physical artifacts from canonical model

### Step 5: Define coexistence and cutover rules

Within 10-Adoption.md:

- **Coexistence is transitional** — the goal is always to reach Declarative or Automated maturity
- While at maturity levels 1-3, both baseline files and canonical entities may coexist
- At level 4 (Declarative), baseline files should be marked `status: superseded` with `superseded_by:` pointing to the canonical entity
- At level 5 (Automated), baseline files may be `status: archived` or removed entirely
- **No generation from baselines** — baselines are documentation only; Agent Artifact only generates from canonical entities in `entities/`
- **Reconciliation** — at level 3→4 transition, generated artifacts must be compared against existing state; differences must be intentional

---

## Phase 2: Spec — Update Existing Sections

*Depends on Phase 1 (10-Adoption.md defines the concepts referenced here)*

### Step 6: Update 1-Foundation.md

Add a new principle (or extend existing ones):

**Principle: Adoption is Incremental**
> MD-DDL supports incremental adoption. Organisations can begin by documenting their existing data landscape — dimensional models, canonical models, ETL pipelines, governance metadata — and progressively evolve toward declarative, AI-generated artifacts. The `baselines/` folder captures existing state; the adoption maturity model tracks the journey; the canonical model is the destination.

Update the two-layer model section to acknowledge the existence of a third layer during adoption:
- Layer 0: Baselines (existing state documentation) — transitional
- Layer 1: Domain file (summary and discovery)
- Layer 2: Detail files (entities, sources, events, etc.)

### Step 7: Update 7-Sources.md and 8-Transformations.md

- In Sources, add a note that source system declarations can reference baseline ETL documentation:
  > "When adopting MD-DDL into an existing environment, source declarations may initially reference baseline ETL documentation in `baselines/etl/` to capture the current transformation logic before formalising it as MD-DDL transform files."

- In Transformations, add a note about the baseline → transform migration path:
  > "Existing ETL/ELT logic documented in `baselines/etl/` serves as the reference for creating MD-DDL transformation YAML. The transformation spec defines the target state; the baseline documents the current state. Reconciliation between the two is part of the adoption journey."

### Step 8: Update 9-Data-Products.md

Add a note about product lifecycle in brownfield contexts:
- At maturity level 1-2, data products may reference existing physical artifacts that are not yet MD-DDL-generated
- At maturity level 4+, all data products should be generated from MD-DDL declarations
- Products can begin their lifecycle at Draft even when based on existing physical artifacts

---

## Phase 3: Agent Skills — Brownfield Adoption Support

*Parallel with Phase 2; depends on Phase 1 for terminology*

### Step 9: New skill — Agent Guide "adoption-planning"

Create `agents/agent-guide/skills/adoption-planning/SKILL.md`

**Trigger:** User mentions existing systems, legacy, migration, brownfield, "we already have," "starting from," "current state"

**Process:**
1. **Assess current state** — What existing assets do you have? (dimensional models, canonical models, ETL, catalog metadata). Which of the four patterns (A/B/C/D) from 10-Adoption.md apply?
2. **Assess target state** — What maturity level are you aiming for? What timeline?
3. **Identify domains** — Which business domains should be tackled first? (recommend starting with a single well-understood domain)
4. **Create adoption roadmap** — Per-domain maturity targets with milestones
5. **Hand off** — Direct user to Agent Ontology with baseline-capture skill for first domain

**Output:** Adoption roadmap document (can be placed in domain folder or project root)

### Step 10: New skill — Agent Ontology "baseline-capture"

Create `agents/agent-ontology/skills/baseline-capture/SKILL.md`

**Trigger:** User wants to document existing schemas, models, ETLs, or catalog metadata; user mentions "capture," "import," "document existing," "baseline"

**Process:**
1. **Identify baseline type** — dimensional, canonical, ETL, or catalog?
2. **Gather existing artifacts** — User provides DDL, dbt models, catalog exports, ERDs, or descriptions
3. **Create baseline files** — Document in `baselines/<type>/` using the templates from 10-Adoption.md
4. **Extract candidate entities** — Identify business concepts from the baseline (facts → business processes, dimensions → entities, ETL targets → entities)
5. **Propose canonical structure** — Suggest which canonical entities could be created from the baseline, with mapping notes
6. **Set domain adoption metadata** — Set `adoption.maturity: documented` in domain.md

**Key rule:** The baseline-capture skill documents existing state; it does NOT create canonical entity files. That's the domain-scoping/entity-modelling skill's job. Clear handoff.

### Step 11: Enhanced skill — Agent Ontology "domain-scoping" brownfield path

Enhance existing brownfield interview path in `agents/agent-ontology/skills/domain-scoping/SKILL.md`:

Currently the brownfield path handles "add entity to existing domain." Extend it to handle:
- **"Translate baseline to canonical"** — User has baselines and wants to create canonical entities from them
- Read baseline files as input context
- Propose entity structure derived from baseline
- Track which baseline files each entity maps to
- Update domain adoption maturity as entities are created (documented → mapped)

### Step 12: New skill — Agent Artifact "reconciliation"

Create `agents/agent-artifact/skills/reconciliation/SKILL.md`

**Trigger:** User wants to compare generated artifacts with existing state; user mentions "reconcile," "compare," "diff," "gap analysis"

**Process:**
1. **Generate physical artifacts** from canonical MD-DDL model (using existing dimensional/normalized/etc. skills)
2. **Compare against baselines** — Load relevant `baselines/dimensional/` or `baselines/canonical/` files
3. **Produce gap report:**
   - Columns/attributes in baseline but not in generated (potential missing entities/attributes)
   - Columns/attributes in generated but not in baseline (new additions from canonical model)
   - Type mismatches, constraint differences
   - Transformation logic differences (baseline ETL vs. MD-DDL transform YAML)
4. **Recommend resolution** — For each gap, suggest whether to update the canonical model, accept the difference as intentional, or flag for SME review

### Step 13: Enhanced skill — Agent Guide "worked-examples"

Extend worked examples to include a brownfield walkthrough:
- Start with an existing star schema (dimensional model)
- Document it as baselines
- Extract canonical entities
- Map source systems
- Generate new physical artifacts
- Reconcile with original
- Show the full adoption journey from Documented → Declarative

---

## Phase 4: Examples

*Depends on Phases 1-3*

### Step 14: Create a brownfield example

Create `examples/Brownfield Adoption/` (or extend Financial Crime with a brownfield narrative):

Option A (preferred): New standalone example showing a realistic brownfield scenario:
```
examples/Brownfield Retail/
  domain.md                     # with adoption metadata
  baselines/
    dimensional/
      fact_sales.md             # existing star schema fact
      dim_product.md            # existing dimension
      dim_store.md
    etl/
      daily_sales_load.md       # existing SSIS/dbt pipeline
    catalog/
      collibra_product.md       # existing governance metadata
  entities/
    sale.md                     # canonical entity derived from fact_sales
    product.md                  # canonical entity derived from dim_product
    store.md                    # canonical entity derived from dim_store
  sources/
    pos-system/
      source.md                 # operational source feeding the ETL
```

This example shows:
- Baselines documented at maturity level 1
- Canonical entities created at maturity level 2
- Governance added at level 3
- Generated artifacts compared to baselines at level 3→4 transition

---

## Phase 5: Tooling & Integration

*Parallel with Phase 4; depends on Phase 1 for structure*

### Step 15: Concatenation script update

Update `.github/scripts/concat-md-ddl-specs.ps1` to include `10-Adoption.md` in the concatenated `MD-DDL-Complete.md`.

### Step 16: Review process update

Update `.github/md-ddl-review-prompt.md` to include adoption maturity validation:
- Does the domain have an `adoption` block if `baselines/` exists?
- Are baseline files using the required metadata format?
- Is `maturity` consistent with the actual state of the domain?

---

## Relevant Files

- [md-ddl-specification/1-Foundation.md](md-ddl-specification/1-Foundation.md) — Add adoption principle, update two-layer model
- [md-ddl-specification/2-Domains.md](md-ddl-specification/2-Domains.md) — Add `adoption` metadata block to domain schema
- [md-ddl-specification/7-Sources.md](md-ddl-specification/7-Sources.md) — Add baseline→source migration note
- [md-ddl-specification/8-Transformations.md](md-ddl-specification/8-Transformations.md) — Add baseline→transform migration note
- [md-ddl-specification/9-Data-Products.md](md-ddl-specification/9-Data-Products.md) — Add brownfield product lifecycle note
- `md-ddl-specification/10-Adoption.md` — **NEW** — Core adoption spec
- [agents/agent-guide/AGENT.md](agents/agent-guide/AGENT.md) — Add adoption-planning skill to index
- [agents/agent-ontology/AGENT.md](agents/agent-ontology/AGENT.md) — Add baseline-capture skill to index
- [agents/agent-ontology/skills/domain-scoping/SKILL.md](agents/agent-ontology/skills/domain-scoping/SKILL.md) — Enhance brownfield path
- [agents/agent-artifact/AGENT.md](agents/agent-artifact/AGENT.md) — Add reconciliation skill to index
- `agents/agent-guide/skills/adoption-planning/SKILL.md` — **NEW**
- `agents/agent-ontology/skills/baseline-capture/SKILL.md` — **NEW**
- `agents/agent-artifact/skills/reconciliation/SKILL.md` — **NEW**
- `.github/copilot-instructions.md` — Update repo layout, agent boundaries
- `.github/scripts/concat-md-ddl-specs.ps1` — Include section 10

---

## Verification

1. **Spec consistency** — Every concept in 10-Adoption.md is referenced correctly from 1-Foundation.md, 2-Domains.md, 7-Sources.md, 8-Transformations.md, 9-Data-Products.md
2. **Agent skill triggers** — Test that agent skill indexes trigger adoption-planning, baseline-capture, and reconciliation on appropriate user prompts
3. **Example validates spec** — The brownfield example uses all spec constructs correctly and passes the domain review skill
4. **Layered review** — Run Layer 1 structural review against 10-Adoption.md to verify spec quality
5. **Maturity model coherence** — Walk through each maturity level transition with the brownfield example and verify exit criteria are achievable
6. **No spec duplication** — Verify 10-Adoption.md doesn't duplicate rules from other sections; cross-references use file-relative paths
7. **Concatenation** — Regenerate MD-DDL-Complete.md and verify section 10 is included correctly
8. **Agent boundary compliance** — Verify baseline-capture doesn't create canonical entities (that's domain-scoping's job), reconciliation doesn't modify canonical model (that's ontology's job)

---

## Decisions

- **Domain-level maturity only** — entities don't individually track maturity; the domain advances as a whole. Domain maturity = lowest level all entities have reached. The `progress` field shows forward momentum within a level (e.g., "48/50 entities governed") so stakeholders see advancement even when one lagging entity holds the domain at its current level.
- **Coexistence is transitional** — baselines exist to be superseded. The goal is always Declarative or Automated. Baseline files get marked `superseded` then `archived`.
- **Baselines are documentation, not generation inputs** — Agent Artifact never generates from baselines. They're reference material for humans and for the reconciliation skill.
- **Reverse engineering is secondary** — We support capturing and translating existing state, but the primary workflow remains top-down canonical modelling. Baseline capture is a structured way to document what exists; canonical entity creation is still a modelling activity guided by Agent Ontology.
- **Four starting-point patterns** — Dimensional, Canonical, ETL, Catalog. Each has a defined journey in 10-Adoption.md.
- **Structured baseline bodies** — Each baseline type has a required YAML block (columns, grain, tool, etc.) ensuring agent-parseable consistency, plus free-form Markdown for context. This balances reliability with flexibility.
- **Mapping block at Level 2** — The baseline→canonical translation is captured as a structured `mapping` block on each baseline file, not as unstructured notes. This gives agents and reviewers a traceable record of which baseline fields became which canonical attributes, and which were intentionally excluded.
- **Drift detection starts at Level 4** — When MD-DDL becomes the source of truth (Declarative), basic drift detection is required to maintain that status. Level 5 (Automated) upgrades to CI/CD-enforced detection with remediation triggers.
- **Staleness prevents adoption decay** — Domains with a `target_date` that has passed without reaching `target_maturity` are flagged as "adoption stalled." This prevents Level 1 sprawl where teams document legacy but never progress.

## Further Considerations

1. **Baseline import tooling** — Should we define a machine-readable baseline format (e.g., paste DDL and have an agent create the baseline file)? Recommendation: Yes, the baseline-capture agent skill should accept DDL, dbt YAML, catalog API exports and create structured baseline files. This is agent behaviour, not spec — the spec defines the target format; the agent handles the translation.

2. **Multi-domain adoption** — Large enterprises might adopt MD-DDL domain-by-domain over years. Should there be a portfolio-level adoption tracker (across all domains)? Recommendation: Defer for now. Each domain has its own maturity. A portfolio view can be assembled by reading all domain.md files. Add this as a future consideration in 10-Adoption.md without specifying it.

3. **Drift detection implementation** — At Level 4, the spec should define what drift means (generated artifact hash vs deployed artifact hash? schema diff? column-level comparison?) and what metadata to capture (last verified date, drift status). Leave the mechanism (CI/CD hooks, database introspection scripts, scheduled agent runs) to implementers since MD-DDL has no runtime.

4. **Baseline→source transform alignment** — The mapping block on baselines documents the *design translation* (existing artifact → canonical model). Source transforms (Section 8) document the *operational data flow* (source system → canonical model). In some cases these overlap (e.g., an ETL baseline's source is the same system declared in `sources/`). The spec should clarify the relationship: mapping blocks are retrospective (what existed → what we designed); transforms are prospective (how data flows going forward).

## Review Attribution

Changes 1–5 below were incorporated based on external stakeholder review (Gemini multi-perspective analysis of the original plan):

1. **Staleness tracking** — CDO risk: Level 1 sprawl where teams document but never progress. Added `adoption_started`, staleness rule, and "adoption stalled" flag.
2. **Drift detection at Level 4** — Architect/Engineer insight: drift is the primary truth-degradation risk in brownfield. Moved basic drift detection from Level 5 to Level 4; Level 5 now covers automated enforcement.
3. **Structured baseline bodies** — Agent risk: inconsistent free-form baselines across teams. Added required YAML blocks per baseline type while preserving free-form Markdown for context.
4. **Mapping block** — Architect risk: unstructured "mapping notes" don't scale. Added structured `mapping` block to baseline files at Level 2 with field-level traceability and explicit unmapped field tracking.
5. **Progress indicator** — Addresses "partially mapped domains" challenge: domain maturity = lowest level reached, but `progress` field shows advancement within a level.
