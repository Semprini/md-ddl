---
name: source-mapping
description: Use this skill when the user wants to declare source systems, create source.md files, author domain feed tables, define field-level transformations, or map source fields to canonical entities. Also use when the user asks "where does this data come from?", "how do we map source fields?", or wants to connect an operational system to the domain model.
---

# Skill: Source Mapping

Covers the interview protocol for source system SMEs, source file creation,
domain feed table authoring, and transform file creation with field-level
mappings using the transformation vocabulary from the MD-DDL specification.

## MD-DDL References

Load these references before authoring any source or transform files:

- Sources spec: `references/sources-spec.md`
- Transformations spec: `references/transformations-spec.md`

Key concepts to apply:

- **Sources are not owners.** Sources generate operational change. The canonical
  model absorbs that change. There is no "system of record" — only canonical
  data products.
- **Two-layer structure.** The `source.md` file is the router (metadata + domain
  feed table). Transform files under `transforms/` are the detail layer for
  field-level mappings.
- **Separation of concerns.** Domain entity files contain no source references.
  Source files contain no governance metadata. Keep the layers clean.

---

## Interview Protocol

Run this protocol when a user wants to connect a source system to an existing
domain model. The domain file and entity detail files should already exist —
if they don't, defer to Domain Scoping first.

### Step 1 — Source System Identity

Understand what the source system is and what it does.

Ask:
- What is the system's name and platform? (e.g., "Salesforce CRM", "SAP S/4HANA")
- What business capability does it serve? (e.g., customer relationship management,
  payment processing, fraud detection)
- Is this a SaaS platform, on-premises system, or internal application?

### Step 2 — Change Model

Determine how the source system communicates change.

Ask:
- How does this system signal that something has changed? Options include:
  - **CDC** (Change Data Capture) — row-level change events
  - **Event** — the system publishes discrete business events
  - **Full Snapshot** — periodic full extracts
  - **Delta** — periodic incremental extracts
  - **API Poll** — data is fetched on-demand via API calls
- What is the typical change frequency? (real-time, hourly, daily, batch)

### Step 3 — Source Tables and Domain Mapping

Identify which source tables or feeds contribute to this domain.

Ask:
- What tables, feeds, or API endpoints from this system contribute data to
  this domain?
- For each source table:
  - What canonical entity does it map to?
  - Does it contribute to one entity or multiple entities?
  - Are there source tables that need to be joined before mapping?

Build the domain feed table from these answers (see Authoring section below).

### Step 4 — Field-Level Mapping Readiness

For each source table identified in Step 3, determine whether field-level
transforms are needed now.

Ask:
- Do you have the source schema available (column names, types, lengths)?
- Are there non-trivial transformations (lookups, concatenations, conditional
  mappings, cross-reference enrichments)?
- Or are the mappings mostly direct (source field → canonical attribute)?

**Decision rule:** If mappings are mostly direct, the domain feed table in
`source.md` is sufficient. If there are non-trivial transforms, create
individual transform files under `transforms/`.

### Step 5 — Source Governance Context

Capture source-specific governance context that affects the mapping.

Ask:
- Are there fields in this source that contain PII not already declared in
  the canonical entity?
- Does this source have specific retention or purge requirements?
- Are there data quality issues known in this source that need to be
  documented?

Flag governance findings for the domain owner but do not modify entity
governance metadata — that is the domain model's concern, not the source
layer's.

---

## Authoring: Source File (`source.md`)

Create the source file at `sources/<system-name>/source.md` following the
structure defined in the Sources specification.

### Source File Structure

```markdown
# [Domain Name](../../domain.md)

## Source Systems

### [System Name]

[One or two sentences: what this system does and why it feeds this domain.]

Platform | Capability | Change Model
--- | --- | ---
[Platform] | [Business Capability] | [CDC / Event / Full Snapshot / Delta / API Poll]

### Domain Feed Table

Source Table | Canonical Target | Granularity | Notes
--- | --- | --- | ---
[source_table_1] | [Entity Name] | row → instance | [any relevant notes]
[source_table_2] | [Entity Name] | row → instance | Requires join with [other_table]

### Source Schema Tables

For each source table in the domain feed table, include a schema table with
column-level detail:

#### [Source Table Name]

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | [col_name] | [type] | [len] | | | [yes/no] | [comment] | [Entity.Attribute or transform link]
```

### Source File Checklist

- [ ] Level-1 heading names the domain with link back to `../../domain.md`
- [ ] System description explains business capability, not technical architecture
- [ ] Platform, Capability, and Change Model are declared
- [ ] Domain feed table maps every source table to a canonical entity
- [ ] Source schema tables present for each source table in the feed table
- [ ] `Destination` column uses `Entity.Attribute` for direct mappings
- [ ] `Destination` column uses `[Transform Name](#anchor)` for non-direct mappings
- [ ] Source system appears in the domain file's `## Source Systems` table

---

## Authoring: Transform Files

Create transform files at `sources/<system-name>/transforms/table_<source-table>.md`
when field-level mappings require non-direct transformations.

### Transform File Structure

```markdown
# [Domain Name](../../../domain.md)

## [Source Table Name]

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | [col_name] | [type] | [len] | | | [yes/no] | [comment] | [Entity.Attribute or #transform-anchor]

### [Transform Name]

[One sentence: what this transform does and why.]

```yaml
type: [map | concatenate | split | lookup | conditional | derive | cross_reference | constant | coalesce | format]
source_field: [field name or list]
target_entity: [Entity Name]
target_attribute: [Attribute Name]
# ... type-specific fields per Section 8 vocabulary
```
```

### Transformation Types Quick Reference

Use the transformation vocabulary from the spec. The most common types:

Type | Use When
--- | ---
`direct` | Source field maps 1:1 to canonical attribute (declared in Destination column, no YAML needed)
`map` | Source value needs value-to-value mapping (e.g., status codes)
`concatenate` | Multiple source fields combine into one attribute
`split` | One source field becomes multiple attributes
`lookup` | Source value is enriched from a reference table
`conditional` | Mapping depends on a condition or business rule
`derive` | Target value is computed from source fields
`cross_reference` | Source value resolves against another entity
`constant` | Target attribute always receives a fixed value
`coalesce` | First non-null from a priority list of source fields
`format` | Value reformatting (date formats, case conversion, etc.)

### Transform File Checklist

- [ ] File named `table_<source-table>.md` (lowercase, underscores)
- [ ] Level-1 heading names the domain with link to `../../../domain.md`
- [ ] Level-2 heading names the source table
- [ ] Source schema table includes all columns from the source
- [ ] Every non-direct transform has a level-3 heading and YAML block
- [ ] Transform headings follow Key-as-Name principle
- [ ] Each transform YAML declares `type`, `source_field`, `target_entity`, `target_attribute`
- [ ] `Destination` column in schema table links to transform headings via anchors

---

## Updating the Domain File

After creating source files, ensure the domain file reflects the new source:

1. Add or update the `## Source Systems` table:

```markdown
## Source Systems

Business Application | Platform | Capability Domain
--- | --- | ---
[System Name](sources/<system-name>/source.md) | [Platform] | [Capability]
```

2. If the user identified source tables that carry PII not yet declared in
   entity governance, flag this for domain-level review — but do not modify
   entity files from within source mapping. That change belongs to Entity
   Modelling.

---

## Guardrails

- **Do not add source references to entity files.** The canonical model is
  source-agnostic. Source-to-entity mapping lives exclusively in source files.
- **Do not invent source schemas.** If the user cannot provide column names
  and types, mark them with `# TODO:` and proceed with what is known.
- **Do not modify governance metadata.** Source mapping reveals governance
  facts but does not own them. Flag findings for the domain owner.
- **One source folder per system.** Do not combine multiple source systems
  in a single folder even if they share a platform.
- **Transform file naming is strict.** Files must follow `table_<source-table>.md`
  pattern. The source table name drives the file name.
