---
name: schema-import
description: Use this skill when the user wants to get from an existing database schema to a draft MD-DDL domain. This is the PRIMARY brownfield adoption path. Triggers include "import schema", "reverse engineer", "I have a database", "here's my DDL", "start from existing tables", "convert my schema", "paste DDL", "brownfield", "existing schema", or when the user provides CREATE TABLE statements, dbt schema.yml, or similar structured schema definitions expecting a canonical domain as output.
---

# Skill: Schema Import

The **primary brownfield path**. Takes an existing database schema and produces
a draft MD-DDL domain with canonical entities, relationships, and enums —
asking only the questions the schema cannot answer. Also parses existing ETL
logic (SQL, dbt models, stored procedures) to generate draft source transform
files.

## MD-DDL Reference

Load before responding:

- `md-ddl-specification/10-Adoption.md` — Adoption maturity model
- `md-ddl-specification/2-Domains.md` — Domain file structure
- `md-ddl-specification/3-Entities.md` — Entity detail file structure

Also reference (do not load unless needed for detailed decisions):

- `skills/entity-modelling/SKILL.md` — for attribute type mapping
- `skills/domain-scoping/SKILL.md` — for domain file checklist

---

## Part 1 — Schema Export Guidance

Before the agent can infer anything, the user needs to get their schema out of
their platform. Present the relevant platform's commands when the user says
what database they are using. If they do not know, ask — do not guess.

### Snowflake

```sql
-- Export all tables and views in a schema
SELECT GET_DDL('SCHEMA', 'MY_DATABASE.MY_SCHEMA');

-- Or export a single table
SELECT GET_DDL('TABLE', 'MY_DATABASE.MY_SCHEMA.MY_TABLE');

-- Include foreign keys and constraints
SHOW IMPORTED KEYS IN SCHEMA MY_DATABASE.MY_SCHEMA;
SHOW PRIMARY KEYS IN SCHEMA MY_DATABASE.MY_SCHEMA;
```

### PostgreSQL

```bash
# Export schema DDL (tables, constraints, indexes)
pg_dump --schema-only --schema=my_schema -d my_database > schema.sql

# Or use psql for a single table
\d+ my_table
```

### SQL Server

```sql
-- Using SSMS: right-click database > Tasks > Generate Scripts
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

### Databricks / Unity Catalog

```sql
-- List tables in a schema
SHOW TABLES IN my_catalog.my_schema;

-- Describe table structure
DESCRIBE EXTENDED my_catalog.my_schema.my_table;

-- Show create statement
SHOW CREATE TABLE my_catalog.my_schema.my_table;
```

### Other Input Formats

The agent also accepts:

- Raw DDL pasted directly (any SQL dialect)
- dbt `schema.yml` or model SQL files
- ERD descriptions in natural language
- CSV/table descriptions (column name, type, nullable, description)

---

## Part 2 — Schema Inference Protocol

Once the user provides their schema, infer as much as possible before asking
anything.

### What the Agent Infers (No Questions Needed)

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

### What the Agent MUST Ask

This is the minimal interview — the smallest set of questions that unlocks
what the schema does not tell you.

**Question 1 — Domain identity and purpose:**

> "What business area does this schema serve? Who uses this data and for
> what decisions?"

This gives the domain name, description, and data owner context.

**Question 2 — Concept refinement (asked per ambiguous table, not globally):**

> "I see tables X, Y, Z that look like [interpretation]. Is that right, or
> are some of these [alternative]?"

Show inferences and ask for corrections. Examples:

- "I see `customer` and `customer_type` — is `customer_type` an enum (fixed
  list of types) or does it have its own lifecycle?"
- "I see `order_line` with FKs to `order` and `product` — is this a dependent
  entity of Order, or is it a relationship between Order and Product?"
- "I see `dim_customer` and `fact_transaction` — this looks like a star schema.
  Are you looking to model the business concepts behind it (Customer,
  Transaction) or document the star schema as-is?"

Only ask about genuinely ambiguous structures. If the schema is clear, skip.

**Question 3 — Governance posture:**

> "Does this data have regulatory or compliance requirements? (e.g., PII,
> retention rules, specific regulations like GDPR/APRA/HIPAA)"

Governance cannot be inferred from DDL. One question covers it.

That is it — three questions (sometimes two if governance is not relevant).
Everything else comes from the schema.

---

## Part 3 — Draft Output

From the schema plus minimal interview answers, produce:

1. **Draft `domain.md`** — domain name, description, metadata (with
   `adoption.maturity: mapped`), overview diagram (Mermaid), and all four
   summary tables (Entities, Enums, Relationships, Events) inferred from
   the schema

2. **Draft entity detail files** — one per inferred entity, with attributes,
   types, constraints, and identifier. Attributes use MD-DDL naming
   (de-snake-cased, business-semantic). Technical/audit columns are noted
   but excluded from canonical attributes.

3. **Draft enum files** — for any identified lookup tables or low-cardinality
   columns

4. **Inferred relationships** — from foreign keys, with cardinality, direction,
   and whether identifying

5. **Uncertainty markers** — anything inferred with medium confidence gets a
   `# INFERRED: [rationale] — confirm or correct` comment so the user can
   review

Mark the draft explicitly:

> "This is a draft inferred from your schema. Review it — the structure
> should be close, but the business meaning is yours to confirm. Tell me
> what to change, and I will refine."

---

## Part 4 — ETL Parsing and Transform Generation

If the user has existing ETL logic, parse it to generate draft source
transform files. This replaces the manual mapping block approach — the
transform file *is* the mapping.

### Accepted ETL Inputs

- **SQL** — SELECT, INSERT INTO...SELECT, MERGE statements
- **dbt models** — model SQL with ref()/source() macros, schema.yml
- **Stored procedures** — T-SQL, PL/SQL, PL/pgSQL
- **Pipeline descriptions** — Informatica mappings, SSIS packages, ADF pipelines (described or pasted)
- **Natural-language descriptions** — "the pipeline joins customers with orders and calculates total spend"

### What the Agent Extracts

ETL pattern | Transform type | Example
--- | --- | ---
Column alias / direct select | `direct` | `SELECT acct_no AS account_number` → direct map
CONCAT, string operations | `derived` | `CONCAT(first_name, ' ', last_name)` → derived with expression
CASE / IF expressions | `conditional` | `CASE WHEN score > 70 THEN 'High'` → conditional with cases
JOIN to lookup/reference table | `lookup` | `LEFT JOIN country_codes ON ...` → lookup transform
Aggregation (SUM, COUNT, etc.) | `aggregation` | `SUM(amount) GROUP BY customer_id` → aggregation transform
COALESCE across sources | `reconciliation` | `COALESCE(crm.email, erp.email)` → reconciliation with priority

### Output

For each source system identified in the ETL, produce:

1. **Draft `source.md`** in `sources/<system>/` if it does not exist
2. **Draft transform files** in `sources/<system>/transforms/` with:
   - Source schema table mapping columns to destinations
   - Named transform sections for non-direct mappings
   - `# INFERRED: [rationale]` comments on medium-confidence transforms

Present transforms alongside the canonical entities so the user can see
the full picture: "here are your entities, and here is how your existing
ETL populates them."

---

## Part 5 — Refinement Loop

After producing the draft, enter a conversational refinement loop:

- User reviews, corrects, adds business context
- Agent applies changes, re-explains trade-offs when relevant
- When the user is satisfied, set `adoption.maturity: mapped` and hand off
  to domain-review or entity-modelling for deeper work

This loop should feel collaborative, not interrogative. The agent has already
done the heavy lifting; the user is steering, not answering a questionnaire.

---

## Relationship to Other Skills

- **baseline-capture** is the secondary brownfield path for documenting
  existing state (Level 1) when audit or history is needed. schema-import
  is the primary path — it jumps straight to a draft canonical model (Level 2).

- **domain-scoping** is the full greenfield interview protocol. schema-import
  replaces most of it when a schema already exists — the schema answers
  candidate concepts, boundaries (tables in the schema are in scope), and
  partially governance. Only business purpose and remaining governance
  questions need asking.

- **entity-modelling** handles deeper modelling decisions (inheritance, type
  hierarchies, attribute trade-offs) that schema-import defers to once the
  draft exists.

---

## Boundary Rules

- **This skill produces drafts, not baselines.** The output is canonical
  entity files (draft quality), not `baselines/` documentation files.
- **This skill does not generate physical artifacts.** That is Agent Artifact's
  responsibility.
- **This skill asks at most three questions.** Everything else is inferred.
  If the schema is genuinely too ambiguous to infer from, fall back to the
  domain-scoping interview protocol.
