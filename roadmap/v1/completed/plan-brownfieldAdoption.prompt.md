# Plan: Brownfield Adoption for MD-DDL

## Implementation Status

**Status: COMPLETE** — All 16 steps implemented as of 2026-03-15. Implementation evolved from the original plan in several areas (documented below as design evolutions). One cleanup item remains.

### Step Completion Summary

Step | Phase | Status | Notes
--- | --- | --- | ---
1 | Phase 1 | ✅ Complete | `10-Adoption.md` created with maturity model, advancement criteria, regression/staleness rules
2 | Phase 1 | ✅ Complete (evolved) | `baselines/` folder structure defined. **Evolution:** Type-specific YAML templates (`dimensional:`, `canonical:`, `etl:`, `catalog:`) removed — baselines now use a minimal `baseline:` metadata header + free-form body. Baselines are described as agent-generated, not human-authored.
2b | Phase 1 | ✅ Complete (evolved) | **Evolution:** `mapping:` blocks on baselines removed entirely. Mappings are now derived from source transform files (Section 8). The transform file *is* the mapping. See "Mapping: Auto-Generated from Source Transforms" in 10-Adoption.md.
3 | Phase 1 | ✅ Complete (evolved) | `adoption` block added to domain metadata in 2-Domains.md. **Evolution:** `progress` field changed from free-text to structured `{ at_level, total }` for agent-parseable counts.
4 | Phase 1 | ✅ Complete (evolved) | Four journey patterns defined. **Evolution:** Pattern A redesigned from "Starting from Dimensional Models" to "Starting from Existing Schemas (Primary Path)" centered on schema-import skill.
5 | Phase 1 | ✅ Complete | Coexistence and cutover rules defined. Drift detection section added (Level 4 basic, Level 5 automated). "Levels 4–5 require external tooling" rule added.
6 | Phase 2 | ✅ Complete | Principle 7 "Adoption is Incremental" added to 1-Foundation.md. Layer 0 baselines paragraph added to Document Structure.
7 | Phase 2 | ✅ Complete | Brownfield adoption notes added to both 7-Sources.md and 8-Transformations.md.
8 | Phase 2 | ✅ Complete | Brownfield adoption note added to 9-Data-Products.md.
9 | Phase 3 | ✅ Complete | `agents/agent-guide/skills/adoption-planning/SKILL.md` created. Skill indexed in Agent Guide AGENT.md.
10 | Phase 3 | ✅ Complete | `agents/agent-ontology/skills/baseline-capture/SKILL.md` created. Skill indexed in Agent Ontology AGENT.md.
10b | Phase 3 | ✅ Complete | `agents/agent-ontology/skills/schema-import/SKILL.md` created with all four parts (export guidance, inference protocol, draft output, ETL parsing). Skill indexed in Agent Ontology AGENT.md.
11 | Phase 3 | ✅ Complete | Brownfield Step 5 added to `agents/agent-ontology/skills/domain-scoping/SKILL.md`. **⚠️ Cleanup needed:** Step 6 in that section still references `mapping` blocks and `unmapped_fields`, which contradicts 10-Adoption.md's "No mapping blocks" rule. Remove Step 6 or rewrite it to reference source transforms.
12 | Phase 3 | ✅ Complete | `agents/agent-artifact/skills/reconciliation/SKILL.md` created with lifecycle-aware gap report. Skill indexed in Agent Artifact AGENT.md.
13 | Phase 3 | ✅ Complete | Brownfield Adoption Walkthrough added to `agents/agent-guide/skills/worked-examples/SKILL.md` as Track narrative using Brownfield Retail example.
14 | Phase 4 | ✅ Complete | `examples/Brownfield Retail/` created with 10 files: domain.md, 3 baselines, 3 entities, 1 ETL baseline, 1 catalog baseline, 1 source. Example at Level 2 (Mapped) with source transforms.
15 | Phase 5 | ✅ Complete | `10-Adoption.md` added to `$sectionFiles` array in `.github/scripts/concat-md-ddl-specs.ps1`.
16 | Phase 5 | ✅ Complete | `.github/copilot-instructions.md` updated with 10-Adoption.md in repo layout, section ownership table, and example references. Review prompt files have been restructured (original `.prompts/md-ddl-review-prompt.md` deleted; review process lives in `.prompts/md-ddl-layered-review-process.md`).

### Design Evolutions from Original Plan

The implementation intentionally diverged from the original plan in five areas:

1. **Simplified baseline format** — Type-specific YAML templates (dimensional, canonical, ETL, catalog blocks) were removed. Baselines now use a minimal metadata header + free-form body. Rationale: reduces human effort; agents parse free-form content to extract structure when needed.

2. **Mappings derived from transforms** — The `mapping:` block on baseline files was replaced by deriving mappings from source transform files (Section 8). Rationale: eliminates a separate artifact to maintain; the transform file *is* the mapping and also the specification for generating ETL code.

3. **Structured progress tracking** — Free-text `progress` changed to `{ at_level, total }`. Rationale: enables agents to compute percentage and detect stalls programmatically.

4. **Schema-import as primary path** — Pattern A redesigned around schema-import rather than dimensional model documentation. Rationale: faster time-to-value; paste DDL → get a draft domain in minutes.

5. **Agent-generated baselines** — Added the principle that baselines are agent-generated from raw input, not human-authored YAML templates. Rationale: reduces adoption friction.

### Cleanup Items

- **domain-scoping Brownfield Step 6** (`agents/agent-ontology/skills/domain-scoping/SKILL.md` lines 186-192): Still references `mapping` blocks and `unmapped_fields` on baseline files. This contradicts 10-Adoption.md line 149: "No mapping blocks." Should be removed or rewritten to reference source transforms.

---

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

**Key rule:** The baseline-capture skill documents existing state; it does NOT create canonical entity files. That's the domain-scoping/entity-modelling skill's job (or the schema-import skill for the fast-track path). Clear handoff.

### Step 10b: New skill — Agent Ontology "schema-import"

Create `agents/agent-ontology/skills/schema-import/SKILL.md`

This is the fast-track brownfield path — the skill that makes adopting MD-DDL feel immediate and guided. A user pastes (or describes) their existing database schema and the agent produces a draft domain with canonical entities, relationships, and enums, asking only the questions the schema can't answer.

**Trigger:** User wants to quickly get from an existing database to a draft MD-DDL domain; user mentions "import schema," "reverse engineer," "I have a database," "here's my DDL," "start from existing tables," "convert my schema"

#### Part 1 — Schema Export Guidance

Before the agent can infer anything, the user needs to get their schema out of their platform. The skill includes practical, copy-paste-ready extraction commands for each supported platform:

**Snowflake:**
```sql
-- Export all tables and views in a schema
SELECT GET_DDL('SCHEMA', 'MY_DATABASE.MY_SCHEMA');

-- Or export a single table
SELECT GET_DDL('TABLE', 'MY_DATABASE.MY_SCHEMA.MY_TABLE');

-- Include foreign keys and constraints
SHOW IMPORTED KEYS IN SCHEMA MY_DATABASE.MY_SCHEMA;
SHOW PRIMARY KEYS IN SCHEMA MY_DATABASE.MY_SCHEMA;
```

**PostgreSQL:**
```bash
# Export schema DDL (tables, constraints, indexes)
pg_dump --schema-only --schema=my_schema -d my_database > schema.sql

# Or use psql for a single table
\d+ my_table
```

**SQL Server:**
```sql
-- Using SSMS: right-click database → Tasks → Generate Scripts
-- Or programmatically:
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE,
       CHARACTER_MAXIMUM_LENGTH, COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
ORDER BY TABLE_NAME, ORDINAL_POSITION;

-- Foreign keys
SELECT fk.name, tp.name AS parent_table, cp.name AS parent_column,
       tr.name AS referenced_table, cr.name AS referenced_column
FROM sys.foreign_keys fk
JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
JOIN sys.tables tp ON fkc.parent_object_id = tp.object_id
JOIN sys.columns cp ON fkc.parent_object_id = cp.object_id AND fkc.parent_column_id = cp.column_id
JOIN sys.tables tr ON fkc.referenced_object_id = tr.object_id
JOIN sys.columns cr ON fkc.referenced_object_id = cr.object_id AND fkc.referenced_column_id = cr.column_id;
```

**Databricks / Unity Catalog:**
```sql
-- List tables in a schema
SHOW TABLES IN my_catalog.my_schema;

-- Describe table structure
DESCRIBE EXTENDED my_catalog.my_schema.my_table;

-- Show create statement
SHOW CREATE TABLE my_catalog.my_schema.my_table;
```

The agent presents the relevant platform's commands when the user says what database they're using. If the user doesn't know, ask — don't guess.

The agent should also accept:
- Raw DDL pasted directly (any SQL dialect)
- dbt `schema.yml` or model SQL files
- ERD descriptions in natural language
- CSV/table descriptions (column name, type, nullable, description)

#### Part 2 — Schema Inference Protocol

Once the user provides their schema, the agent infers as much as possible before asking anything:

**What the agent infers from the schema (no questions needed):**

Schema signal | MD-DDL inference | Confidence
--- | --- | ---
Table name | Candidate entity name (de-snake-cased, singularised) | High
Column names + types | Candidate attributes with MD-DDL types | High
Primary key | `identifier: true` attribute | High
Foreign keys | Candidate relationships (direction, cardinality from constraint type) | Medium-High
Nullability | `required: true/false` | High
Unique constraints | Candidate identifier or alternate key | Medium
Enum-like columns (low cardinality, varchar, FK to lookup table) | Candidate enums | Medium
Junction/bridge tables (composite PK of two FKs) | Many-to-many relationship | High
Timestamp columns (`created_at`, `updated_at`, `deleted_at`) | Mutability signal (mutable if `updated_at` exists), soft-delete pattern | Medium
Audit columns (`created_by`, `modified_by`) | Governance signal but not canonical attributes | Medium
Naming patterns (`dim_*`, `fact_*`, `stg_*`) | Dimensional vs staging vs operational classification | High
Column prefixes matching table names (`customer_id`, `customer_name`) | Table-scoped naming convention (strip prefix in canonical) | Medium

**What the agent CANNOT infer (must ask):**

This is the minimal interview — the smallest set of questions that unlocks what the schema doesn't tell you:

**Question 1 — Domain identity and purpose:**
> "What business area does this schema serve? Who uses this data and for what decisions?"

This gives the domain name, description, and data owner context. A schema of tables tells you structure but never *why* it exists.

**Question 2 — Concept refinement (asked per ambiguous table, not globally):**
> "I see tables X, Y, Z that look like [interpretation]. Is that right, or are some of these [alternative]?"

The agent shows its inferences and asks for corrections. Examples:
- "I see `customer` and `customer_type` — is `customer_type` an enum (fixed list of types) or does it have its own lifecycle?"
- "I see `order_line` with FKs to `order` and `product` — is this a dependent entity of Order, or is it a relationship between Order and Product?"
- "I see `dim_customer` and `fact_transaction` — this looks like a star schema. Are you looking to model the business concepts behind it (Customer, Transaction) or document the star schema as-is?"

Only ask about genuinely ambiguous structures. If the schema is clear, don't ask.

**Question 3 — Governance posture:**
> "Does this data have regulatory or compliance requirements? (e.g., PII, retention rules, specific regulations like GDPR/APRA/HIPAA)"

Governance cannot be inferred from DDL. One question covers it.

That's it — three questions (sometimes two if governance isn't relevant). Everything else comes from the schema.

#### Part 3 — Draft Output

From the schema + minimal interview answers, the agent produces:

1. **Draft `domain.md`** — domain name, description, metadata (with `adoption.maturity: mapped`), overview diagram (Mermaid), and all four summary tables (Entities, Enums, Relationships, Events) inferred from the schema
2. **Draft entity detail files** — one per inferred entity, with attributes, types, constraints, and identifier. Attributes use MD-DDL naming (de-snake-cased, business-semantic). Technical/audit columns are noted but excluded from canonical attributes.
3. **Draft enum files** — for any identified lookup tables or low-cardinality columns
4. **Inferred relationships** — from foreign keys, with cardinality, direction, and whether identifying
5. **Uncertainty markers** — anything the agent inferred with medium confidence gets a `# INFERRED: [rationale] — confirm or correct` comment so the user can review

The draft is explicitly marked as a starting point:
> "This is a draft inferred from your schema. Review it — the structure should be close, but the business meaning is yours to confirm. Tell me what to change, and I'll refine."

#### Part 4 — Refinement Loop

After producing the draft, the agent enters a conversational refinement loop:
- User reviews, corrects, adds business context
- Agent applies changes, re-explains trade-offs when relevant
- When the user is satisfied, the agent sets `adoption.maturity: mapped` and hands off to domain-review or entity-modelling for deeper work

This loop should feel collaborative, not interrogative. The agent has already done the heavy lifting; the user is steering, not answering a questionnaire.

#### Relationship to other skills

- **baseline-capture** is for documenting existing state faithfully (Level 1 — Documented). schema-import is for jumping straight to a draft canonical model (Level 2 — Mapped). They serve different purposes: baseline-capture preserves what exists; schema-import infers what should exist.
- **domain-scoping** is the full greenfield interview protocol. schema-import replaces most of it when a schema already exists — the schema answers Steps 2 (candidate concepts), 3 (boundaries — tables already in the schema are in scope), and partially Step 4 (governance — if catalog metadata is present). Only Step 1 (business purpose) and the remaining governance questions need asking.
- **entity-modelling** handles deeper modelling decisions (inheritance, type hierarchies, attribute trade-offs) that schema-import defers to once the draft exists.

### Step 11: Enhanced skill — Agent Ontology "domain-scoping" brownfield path

Enhance existing brownfield interview path in `agents/agent-ontology/skills/domain-scoping/SKILL.md`:

Currently the brownfield path handles "add entity to existing domain." Extend it to handle:
- **"Translate baseline to canonical"** — User has baselines and wants to create canonical entities from them
- Read baseline files as input context
- Propose entity structure derived from baseline
- Track which baseline files each entity maps to
- Update domain adoption maturity as entities are created (documented → mapped)

Note: the schema-import skill (Step 10b) provides the fast-track path for users who have DDL and want to jump straight to a draft domain. Domain-scoping's brownfield path remains the deeper, interview-driven route for translating baselines that aren't raw DDL (ETL pipelines, catalog metadata, natural-language descriptions).

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

- [md-ddl-specification/1-Foundation.md](../../md-ddl-specification/1-Foundation.md) — Add adoption principle, update two-layer model
- [md-ddl-specification/2-Domains.md](../../md-ddl-specification/2-Domains.md) — Add `adoption` metadata block to domain schema
- [md-ddl-specification/7-Sources.md](../../md-ddl-specification/7-Sources.md) — Add baseline→source migration note
- [md-ddl-specification/8-Transformations.md](../../md-ddl-specification/8-Transformations.md) — Add baseline→transform migration note
- [md-ddl-specification/9-Data-Products.md](../../md-ddl-specification/9-Data-Products.md) — Add brownfield product lifecycle note
- `md-ddl-specification/10-Adoption.md` — **NEW** — Core adoption spec
- [agents/agent-guide/AGENT.md](../../agents/agent-guide/AGENT.md) — Add adoption-planning skill to index
- [agents/agent-ontology/AGENT.md](../../agents/agent-ontology/AGENT.md) — Add baseline-capture and schema-import skills to index
- [agents/agent-ontology/skills/domain-scoping/SKILL.md](../../agents/agent-ontology/skills/domain-scoping/SKILL.md) — Enhance brownfield path
- [agents/agent-artifact/AGENT.md](../../agents/agent-artifact/AGENT.md) — Add reconciliation skill to index
- `agents/agent-guide/skills/adoption-planning/SKILL.md` — **NEW**
- `agents/agent-ontology/skills/baseline-capture/SKILL.md` — **NEW**
- `agents/agent-ontology/skills/schema-import/SKILL.md` — **NEW** — Fast-track schema-to-domain inference
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
8. **Agent boundary compliance** — Verify baseline-capture doesn't create canonical entities (that's domain-scoping's job), schema-import produces drafts (not baselines), reconciliation doesn't modify canonical model (that's ontology's job)
9. **Schema-import demo path** — Paste a Snowflake `GET_DDL` export of 8–12 tables with FKs into Agent Ontology. Verify: (a) agent asks ≤3 questions, (b) draft domain.md and entity files are produced, (c) inferred relationships match FK structure, (d) technical/audit columns are excluded from canonical attributes, (e) ambiguous structures are marked with `# INFERRED:` comments
10. **Platform coverage** — Verify schema export guidance exists and is correct for Snowflake, PostgreSQL, SQL Server, and Databricks

---

## Decisions

- **Domain-level maturity only** — entities don't individually track maturity; the domain advances as a whole. Domain maturity = lowest level all entities have reached. The `progress` field shows forward momentum within a level (e.g., "48/50 entities governed") so stakeholders see advancement even when one lagging entity holds the domain at its current level.
- **Coexistence is transitional** — baselines exist to be superseded. The goal is always Declarative or Automated. Baseline files get marked `superseded` then `archived`.
- **Baselines are documentation, not generation inputs** — Agent Artifact never generates from baselines. They're reference material for humans and for the reconciliation skill.
- **Reverse engineering is secondary** — We support capturing and translating existing state, but the primary workflow remains top-down canonical modelling. Baseline capture is a structured way to document what exists; canonical entity creation is still a modelling activity guided by Agent Ontology.
- **Schema-import is the fast-track, not the only path** — schema-import gives the best demo experience (paste DDL → get a draft domain in minutes), but it's one of several brownfield routes. Baseline-capture + domain-scoping is the deeper route for ETL pipelines, catalog metadata, or situations where the schema doesn't represent the target canonical model. Both paths converge at Level 2 (Mapped).
- **Minimal interview, not no interview** — The schema-import skill infers everything it can from the DDL and asks only what it can't infer: business purpose, ambiguous structure clarification, and governance posture. Three questions or fewer for a typical schema. This keeps the interaction guided and efficient without pretending the agent can guess business meaning.
- **Four starting-point patterns** — Dimensional, Canonical, ETL, Catalog. Each has a defined journey in 10-Adoption.md.
- **Structured baseline bodies** — Each baseline type has a required YAML block (columns, grain, tool, etc.) ensuring agent-parseable consistency, plus free-form Markdown for context. This balances reliability with flexibility.
- **Mapping block at Level 2** — The baseline→canonical translation is captured as a structured `mapping` block on each baseline file, not as unstructured notes. This gives agents and reviewers a traceable record of which baseline fields became which canonical attributes, and which were intentionally excluded.
- **Drift detection starts at Level 4** — When MD-DDL becomes the source of truth (Declarative), basic drift detection is required to maintain that status. Level 5 (Automated) upgrades to CI/CD-enforced detection with remediation triggers.
- **Staleness prevents adoption decay** — Domains with a `target_date` that has passed without reaching `target_maturity` are flagged as "adoption stalled." This prevents Level 1 sprawl where teams document legacy but never progress.

## Further Considerations

1. **Baseline import tooling** — Should we define a machine-readable baseline format (e.g., paste DDL and have an agent create the baseline file)? Recommendation: The schema-import skill (Step 10b) now handles the fast-track DDL-to-domain path directly. The baseline-capture skill handles DDL-to-baseline for teams that want the documentation-first approach. Both accept pasted DDL, dbt YAML, and catalog exports.

2. **Multi-domain adoption** — Large enterprises might adopt MD-DDL domain-by-domain over years. Should there be a portfolio-level adoption tracker (across all domains)? Recommendation: Defer for now. Each domain has its own maturity. A portfolio view can be assembled by reading all domain.md files. Add this as a future consideration in 10-Adoption.md without specifying it.

3. **Drift detection implementation** — At Level 4, the spec should define what drift means (generated artifact hash vs deployed artifact hash? schema diff? column-level comparison?) and what metadata to capture (last verified date, drift status). Leave the mechanism (CI/CD hooks, database introspection scripts, scheduled agent runs) to implementers since MD-DDL has no runtime.

4. **Baseline→source transform alignment** — The mapping block on baselines documents the *design translation* (existing artifact → canonical model). Source transforms (Section 8) document the *operational data flow* (source system → canonical model). In some cases these overlap (e.g., an ETL baseline's source is the same system declared in `sources/`). The spec should clarify the relationship: mapping blocks are retrospective (what existed → what we designed); transforms are prospective (how data flows going forward).

5. **Schema-import for non-relational sources** — The current schema-import skill targets relational DDL. Future iterations could extend to: document databases (MongoDB schema inference from sample documents), event schemas (Avro/Protobuf → entity + event inference), API specs (OpenAPI → entity inference). Recommendation: defer until the relational path is proven.

## Review Attribution

Changes 1–5 below were incorporated based on external stakeholder review (Gemini multi-perspective analysis of the original plan):

1. **Staleness tracking** — CDO risk: Level 1 sprawl where teams document but never progress. Added `adoption_started`, staleness rule, and "adoption stalled" flag.
2. **Drift detection at Level 4** — Architect/Engineer insight: drift is the primary truth-degradation risk in brownfield. Moved basic drift detection from Level 5 to Level 4; Level 5 now covers automated enforcement.
3. **Structured baseline bodies** — Agent risk: inconsistent free-form baselines across teams. Added required YAML blocks per baseline type while preserving free-form Markdown for context.
4. **Mapping block** — Architect risk: unstructured "mapping notes" don't scale. Added structured `mapping` block to baseline files at Level 2 with field-level traceability and explicit unmapped field tracking.
5. **Progress indicator** — Addresses "partially mapped domains" challenge: domain maturity = lowest level reached, but `progress` field shows advancement within a level.
