---
name: source-mapping
description: Use this skill when the user wants to declare source systems, author source summaries and feed tables, define field-level transformations, or map source fields to canonical entities. Also use when one source table splits into several domain entities, when instance identity or deduplication must be derived, when a source column needs conditional or lookup logic, or when the user asks "where does this data come from?", "how do we map source fields?", or "will an agent generate the same thing twice from this?"
---

# Skill: Source Mapping

Covers the interview protocol for source system SMEs, source summary authoring, feed tables, and transform detail with field-level mappings using the transformation vocabulary from the MD-DDL specification.

## MD-DDL Reference

- Full sources specification: `md-ddl-specification/7-Sources.md`
  (reference stub: `references/sources-spec.md`)
- Full transformations specification: `md-ddl-specification/8-Transformations.md`
  (reference stub: `references/transformations-spec.md`)

Read the relevant reference before drafting any source or transform file. Key sections: Entity Fan-Out, the transformation type vocabulary, Worked Examples, and Open Decisions.

### Load-bearing concepts

- **Sources are not owners.** Sources generate operational change. The canonical model absorbs that change. There is no "system of record" — only canonical data products.
- **Separation of concerns.** Domain entity files contain no source references. Source files contain no governance metadata. Source idiosyncrasies — null representations, format quirks, legacy codes — stay in transform detail and never leak into the canonical model.
- **Domain-rooted hierarchy.** `## Sources` is a domain section like `## Entities`. Every source file, summary or detail, is rooted at the domain.
- **Determinism is the deliverable.** Transform detail exists so a generating agent produces the same output twice. Anything a reader has to infer, an agent will guess — and two runs will guess differently.

---

## The Determinism Test

Apply this before declaring transform detail complete. It is the single most useful check in this skill, and most defects it catches are invisible to a human reader who already knows the answer.

For each source table, ask:

1. **How many instances does one row produce?** If the answer is anything other than "exactly one, of one entity", an `Entity Fan-Out` section is required.
2. **Where does each instance's identifier come from?** If it is not a direct map from a source column, a `deduplication` transformation must derive it.
3. **When two rows describe the same thing, which one wins?** If merging is possible, a `survivorship` rule is required. Without it, output is order-dependent.
4. **When two case predicates both match, which fires?** If cases can overlap, `evaluation` must be declared.
5. **Does every referenced field exist in the declaration?** A predicate reading an undeclared field breaks lineage tracing.
6. **Does every `target` resolve?** Entity and attribute must exist in the domain model, spelled as the model spells them. This is the most common defect in hand-authored transform detail — an attribute the author assumed existed.
7. **Is every blank `Destination` a decision?** Blank means deliberately not mapped. Undecided belongs in `Open Decisions`.

Anything that fails is either fixed or recorded in `Open Decisions`. Never leave it to inference.

---

## Interview Protocol

Run this protocol when a user wants to connect a source system to an existing domain model. The domain file and entity detail files should already exist — if they don't, defer to Domain Scoping first.

### Step 1 — Source System Identity

- What is the system's name and platform?
- What business capability does it serve?
- Who owns it operationally, and who stewards its data?

### Step 2 — Change Model

How does the system signal change? Use the spec's declared values:

Value | Meaning
--- | ---
`real-time-cdc` | Row-level changes streamed in real time
`event-driven` | Publishes business events, not raw CDC
`batch-daily` | Full or incremental extract, daily
`batch-intraday` | Multiple batch extracts within a day
`api-poll` | Changes retrieved by polling an API
`manual` | Human-loaded; no automated feed

Also capture `data_quality_tier` — 1 (high trust), 2 (standard), 3 (legacy, requires validation). This is a governance signal about how much trust to extend, not a technical score.

### Step 3 — Source Tables and Canonical Targets

For each source table:

- Which canonical entities does it feed?
- **Does one row produce one instance, or several?** Ask this explicitly. Source systems routinely combine concepts the domain model separates — an address table that also carries the owner's name is producing at least three instances per row.
- Are joins required before mapping?

### Step 4 — Identity and Deduplication

Skip only if every instance's identifier is a direct map from a source column.

- What makes two rows "the same thing" in the real world?
- Is there an external identifier (a DPID, an ISIN, an LEI)? Is it always populated?
- When it is absent, what combination of columns identifies the row instead?
- When two rows merge and disagree on a value, which wins — the most recent, the highest-priority source, or only where they agree?

### Step 5 — Field-Level Mapping

- Do you have the source schema — column names, types, lengths, nullability?
- Which columns need logic beyond a rename? Look for legacy code tables, split or combined names, flags that encode status, and type discriminators.
- **Which columns are not needed at all?** Get this stated rather than left blank by accident.
- Are there columns whose meaning nobody can confirm? Those go straight to `Open Decisions`.

### Step 6 — Worked Examples

Ask the SME to walk through two or three real rows and state what should come out. This is the highest-value part of the interview: it surfaces disagreements that field-level questioning misses, and it converts directly into the `Worked Examples` section and into test fixtures.

Prioritise: each branch of a fan-out condition, each branch of a deduplication key, and any case whose evaluation order matters.

### Step 7 — Source Governance Context

- Any PII in this source not already declared on the canonical entity?
- Known data quality issues worth recording as `quality_note`?

Flag governance findings for the domain owner. Do not modify entity governance metadata from within source mapping.

---

## Authoring: Source Summary

Source summaries are small. Collect them in a single `sources/sources.md` and split a source into its own file only once it grows large enough to warrant it.

```markdown
# [Domain Name](../domain.md)

## Sources

### System Name

One or two sentences: what this system does and why it feeds this domain.

#### Metadata

​```yaml
id: system-id
owner: team@bank.com
steward: data.governance@bank.com
change_model: real-time-cdc
change_events:
  - Customer Created
  - Customer Updated
update_frequency: real-time
data_quality_tier: 1
status: Production
version: "1.0.0"
​```

#### Source Overview Diagram

A Mermaid `graph LR` showing which canonical entities this source feeds, edges labelled with the change model, nodes linked to entity detail.

#### Feeds

Canonical Entity | Transform | Attributes Contributed | Change Model
--- | --- | --- | ---
[Entity](../entities/entity.md#anchor) | [table_NAME](system-id/table_NAME.md#name) | Attribute One, Attribute Two | real-time-cdc
```

Because the file is rooted at the domain, the domain name is not repeated in the Feeds heading.

Where a source row produces the concrete subtypes of an abstract entity, list the subtypes actually instantiated — not the abstract parent — and note that their attributes are inherited.

---

## Authoring: Transform Detail

One file per source table, named for the table and matching the source system's casing: `sources/<system-id>/table_ADDRESS.md`. No `transforms/` subfolder is required — parsers locate content by heading hierarchy, not path.

```markdown
# [Domain Name](../../domain.md)

## Sources

### [System Name](../sources.md#system-name)

#### SourceTableName
```

Under the source table heading, use these level-5 sections. Only the source schema is mandatory:

Section | When
--- | ---
`##### Entity Fan-Out` | One row produces more than one instance
`##### Source Schema` | Always
`##### Transform: <Name>` | Once per non-direct mapping rule
`##### Worked Examples` | Anything beyond direct maps
`##### Open Decisions` | Anything unresolved

The `Transform: ` prefix separates mapping rules from the fixed sections. The transform's Knowledge Graph identity is the heading with the prefix removed.

### Source Schema table

Columns are `Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Description | Destination`.

- Direct mappings need only the `Destination` cell — no YAML.
- Non-direct mappings link to the rule anchor: `[Transform: Map Party Status](#transform-map-party-status)`.
- A column feeding several targets takes a comma-separated list. The one-path constraint is per *target attribute*: several rules may read one column; two rules must not write one attribute.
- **A blank `Destination` asserts the column is deliberately not mapped.** State this convention in the file so it reads as a decision, not an omission.

---

## Entity Fan-Out

Required whenever one source row produces more than one canonical instance. Without it, the number and identity of outputs is left to the generating agent to infer.

```yaml
produces:
  - entity: Address · Postal Address
    cardinality: 0..1
    deduplicated: true
    identity: Address Uniqueness Merge

  - entity: Location Involvement
    cardinality: 1
    identity: Location Involvement Mapping
    references:
      Address: Address Uniqueness Merge

  - entity: Individual
    cardinality: 0..1
    condition: "OWNER_TYPE_ENUM == 1"
    identity:
      field: ADDRESS.OWNER_ID
      maps_to: Party · Party Identifier
```

Key | Purpose
--- | ---
`entity` | Canonical entity produced. `Parent · Subtype` where the target is a subtype.
`cardinality` | Instances per source row: `1`, `0..1`, `0..*`
`condition` | Selects when this instance is produced. Required when entries are alternatives.
`identity` | The transformation determining the identifier, or a source field and what it maps to.
`deduplicated` | `true` when instances collapse across rows. Requires a `deduplication` transform.
`references` | Which produced instance satisfies a relationship to another.

**Abstract targets.** A transform targeting an attribute on an abstract entity — `target: Party · Legal Name` — states which attribute is populated but not which instance receives it. The fan-out entry whose `condition` matched supplies that binding. A transform targeting an abstract entity with no fan-out declaration is a validation error.

---

## Transformation Type Selection

Use only these types. The envelope is always `type:` plus `target: Entity · Attribute`; `system:` is omitted because it is implicit from the owning source.

Type | Use when
--- | ---
`direct` | Field maps 1:1, possibly with a `cast`. Declared in the Destination cell; no YAML needed.
`derived` | Attribute computed from one or more fields via `expression:` and named `inputs:`
`lookup` | Source codes translate to canonical values, via a domain enum/entity (`reference:`) or an `inline:` code table
`conditional` | Value selected by predicate — ranges, compound tests, several codes collapsing to one value
`reconciliation` | Same attribute exists in multiple source *systems*; priority decides
`deduplication` | Instance identifier must be derived, and rows collapse into one instance
`aggregation` | Source is finer-grained than the entity; rows roll up to one value

### Choosing between the near-neighbours

- **`lookup` inline vs `conditional`** — `inline:` for an opaque code table with no logic in it. `conditional` when a case needs a predicate: a range, a compound test, or several codes mapping to one value.
- **`reconciliation` vs `deduplication`** — `reconciliation` resolves an attribute *across source systems*. `deduplication` collapses duplicate rows *within* one source table.
- **`derived` with `if()` vs `conditional`** — `if()` is for a single branch inside an otherwise computational expression. Multi-way value selection is `conditional`, which validates its case keys against the target's type.

### `conditional` — the two things that get missed

Declare multiple inputs rather than a single `source:` when cases test several columns, and declare evaluation order when cases can overlap:

```yaml
type: conditional
target: Location Involvement · Verification Status
evaluation: first_match
inputs:
  Is Validated:
    field: ADDRESS.IS_VALIDATED
  Retired Date:
    field: ADDRESS.DSS_END_DATE
cases:
  Expired:  "Retired Date IS NOT NULL AND Retired Date < today()"
  Verified: "Is Validated == 1"
fallback: Unverified
```

`evaluation` is `first_match` (declaration order wins) or `exclusive` (non-overlap asserted; generation emits a check). Every field a predicate references must be declared. Case keys must be valid values of the target's type — for an `enum:` target, valid enum values.

Watch source types: comparing a `NUMBER` column to `'true'` is a type error that generates SQL matching nothing.

### `deduplication` — identity and survivorship

```yaml
type: deduplication
target: Address · Address Identifier
key:
  - when: "DPID_N IS NOT NULL"
    using:
      - field: ADDRESS.DPID_N
    prefix: "DPID"
  - when: "DPID_N IS NULL"
    using:
      - field: ADDRESS.ADDRESS1
      - field: ADDRESS.POST_CODE
    normalise: [trim, uppercase, collapse_whitespace]
    prefix: "COMP"
survivorship:
  strategy: most_recent
  timestamp_field: ADDRESS.UPDATE_DATE
```

`key` branches are ordered; the first matching `when` supplies the key. Always author the fallback branch — an external identifier that is "always populated" rarely is. `prefix` stops a composite key colliding with an external-identifier key. `survivorship` reuses the reconciliation strategies (`priority_non_null`, `priority_always`, `most_recent`, `consensus`).

---

## Worked Examples

For anything beyond a direct map, this is the only device that pins behaviour. Declare a source row and the exact instances it must produce.

```yaml
example: Individual with a DPID-matched, customer-confirmed residential address
given:
  ADDRESS_ID: "3f2b-aaa1"
  OWNER_ID: "8c14-p001"
  OWNER_TYPE_ENUM: 1
  DPID_N: "1234567"
produces:
  - entity: Address · Postal Address
    Address Identifier: "DPID:1234567"
  - entity: Individual
    Party Identifier: "8c14-p001"
    Legal Name: "Jane Whitcombe"
notes: >
  Party is abstract, so the concrete instance is an Individual, selected by the
  OWNER_TYPE_ENUM condition in Entity Fan-Out.
```

`given` accepts a list of rows where the example demonstrates cross-row behaviour such as deduplication. `produces` may declare `cardinality` where the count itself is the point. Only list what matters to the example — it is an assertion about behaviour, not a row dump.

An example producing an entity the fan-out does not declare is a validation error.

---

## Open Decisions

Real source systems have undocumented columns, contradictory type declarations, and codes nobody remembers. Recorded in prose, an unresolved question is invisible to generation; recorded here it is a declared blocker.

```markdown
Ref | Item | Impact
--- | --- | ---
OD-1 | `OWNER_TYPE_ENUM` typed `NUMBER` but documented with character codes. Values unknown. | Subtype routing in Entity Fan-Out cannot be generated.
```

Mark any placeholder inline and reference the decision:

```yaml
condition: "OWNER_TYPE_ENUM == <INDIVIDUAL_CODE>"   # UNRESOLVED — see OD-1
```

Surface open decisions when handing off. Do not guess past them.

---

## Updating the Domain File

Ensure the domain file's `## Source Systems` table links to the source's summary heading:

Business Application | Platform | Capability Domain
--- | --- | ---
System Name → `sources/sources.md#system-name` | Platform | Capability

If source tables carry PII not yet declared in entity governance, flag it for domain-level review — do not modify entity files from within source mapping.

---

## Checklists

### Source summary

- [ ] Level-1 heading names the domain, linked back to the domain file
- [ ] `### System Name` under `## Sources`
- [ ] Description explains business capability, not technical architecture
- [ ] Metadata declares `id`, `owner`, `steward`, `change_model`, `data_quality_tier`, `status`, `version`
- [ ] Source Overview Diagram present, edges labelled with change model
- [ ] Feeds table lists every entity the source contributes to, with attributes
- [ ] Concrete subtypes listed, not abstract parents
- [ ] Source appears in the domain file's `## Source Systems` table

### Transform detail

- [ ] File named for the source table, matching source casing
- [ ] Hierarchy repeated from the domain down; source heading links to its summary
- [ ] `Entity Fan-Out` present wherever a row produces more than one instance
- [ ] Source schema table uses the `Description` column and covers every column
- [ ] Every `target` resolves to a real entity and attribute — verified, not assumed
- [ ] Every non-direct mapping has a `Transform: ` heading and YAML block
- [ ] Identity derived by `deduplication` wherever it is not a direct map
- [ ] `survivorship` declared wherever rows can merge
- [ ] `evaluation` declared wherever cases can overlap
- [ ] Every field referenced by a predicate is declared in `inputs:`
- [ ] Blank `Destination` cells are decisions, and the convention is stated in the file
- [ ] Worked examples cover each fan-out branch and each key branch
- [ ] Unresolved items recorded in `Open Decisions`, not left blank

---

## Guardrails

- **Do not add source references to entity files.** The canonical model is source-agnostic.
- **Do not invent target attributes.** Read the entity file and confirm the attribute exists before writing a `Destination` or a `target`. If the domain model has no home for a source column, that is a modelling decision for the domain owner — record it in `Open Decisions`, do not map it to the nearest plausible name.
- **Do not invent source schemas.** If the user cannot provide column names and types, record what is known and put the rest in `Open Decisions`.
- **Do not resolve contradictions silently.** A column typed `NUMBER` but documented with letter codes cannot be mapped by guessing. Ask, or record it.
- **Do not modify governance metadata.** Source mapping reveals governance facts but does not own them.
- **One source per system.** Do not combine multiple source systems under one identity even if they share a platform.
