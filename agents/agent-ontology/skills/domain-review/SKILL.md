---
name: domain-review
description: Use this skill when the user asks to review, audit, validate, or quality-check an existing MD-DDL domain and its detail files. Also use before declaring a domain “complete” or production-ready. This skill performs both structural conformance checks and decision-quality checks for relationship granularity, temporal tracking, existence, mutability, conceptual-to-logical realization, standards alignment, and regulatory posture.
---

# Skill: Domain Review

Covers full-domain review of MD-DDL artifacts with two goals:
1) structural correctness against the MD-DDL specification, and
2) modelling decision quality against cross-skill guidance and standards/regulatory expectations.

## References to Load

Load these references before performing the review:

- Domains spec: `../domain-scoping/references/domains-spec.md`
- Entities spec: `../entity-modelling/references/entities-spec.md`
- Enumerations spec: `../entity-modelling/references/enumerations-spec.md`
- Relationships spec: `../relationship-events/references/relationships-spec.md`
- Events spec: `../relationship-events/references/events-spec.md`
- Sources spec: `../source-mapping/references/sources-spec.md`
- Transformations spec: `../source-mapping/references/transformations-spec.md`
- Conceptual/physical realization: `../entity-modelling/conceptual-to-physical-realisation.md`
- Standards alignment: `../standards-alignment/SKILL.md`
- Regulatory compliance benchmark: `../../../agent-regulation/skills/regulatory-compliance/SKILL.md`

If the domain is in a recognized industry (banking, payments, insurance, healthcare, telecom), standards and regulatory checks are mandatory, not optional.

---

## Review Protocol

Run this protocol in order. Do not skip sections.

### 1) Inventory and Coverage

Confirm all modeled artifacts are present and navigable:

- Domain file exists and includes Metadata, Diagram, and all four summary tables
- Every summary table Name link resolves to an existing detail file anchor
- Every referenced entity/enum/relationship/event appears exactly once in the expected section
- No orphaned detail files that are not represented in summary tables (unless explicitly marked draft)

### 2) Structural Conformance Review

Validate structure and formatting against MD-DDL spec:

- Heading hierarchy and section placement
- Mermaid syntax and ELK usage in all required diagrams
- Entity YAML completeness (identifier, attributes, no FK attributes)
- Enum declaration correctness (simple list vs dictionary usage)
- Relationship YAML completeness (`source`, `type`, `target`, `cardinality`, `granularity`, `ownership`)
- Event YAML completeness (`actor`, `entity`, `emitted_on`, `business_meaning`, temporal priority)
- Link integrity and anchor correctness

### 3) Decision-Quality Review (Non-Structural)

Assess modelling choices and explain *why* each is acceptable or needs revision.

#### Relationship Granularity

For each relationship, verify chosen `granularity` matches business meaning:

- `atomic` only when instance-level pairing is true
- `group` when one side is aggregate/collection semantics
- `period` when state-at-time semantics are intended

Flag cases where default `atomic` appears unexamined.

#### Entity Temporal Tracking

For each temporal entity, confirm tracking mode matches lifecycle and audit need:

- `valid_time`, `transaction_time`, `bitemporal`, or explicit none-by-design
- temporal attributes and constraints are coherent with narrative and governance

Flag missing or contradictory temporal strategy.

#### Existence

Validate `existence` (`independent` / `dependent` / `associative`) against conceptual meaning and expected physical realization.

Flag misuse driven by implementation shortcuts.

#### Mutability

Validate `mutability` choice against expected change behavior and lineage/audit requirements:

- `immutable`, `append_only`, `slowly_changing`, `frequently_changing`, `reference`

Flag choices that conflict with temporal requirements or event semantics.

#### Conceptual → Logical Realization

Using `conceptual-to-physical-realisation.md`, verify:

- source/ownership direction is coherent
- cardinality in detail files matches conceptual statements in domain file
- M:N patterns are modelled intentionally and not collapsed accidentally
- logical choices do not imply contradictory physical targets

Flag ownership/existence conflation and cardinality mismatches.

### 4) Standards Alignment Review

For each domain concept claiming a standard mapping:

- mapping is plausible and specific (not superficial name matching)
- reference links are valid and point to intended standard object
- material deviations from the standard are acknowledged in descriptions where needed

Flag fabricated, weak, or ambiguous mappings.

### 5) Regulatory Review

Assess domain and entity governance posture against stated jurisdictional scope:

- `regulatory_scope` matches domain geography and business context
- domain-level defaults are present and sensible
- entity-level governance overrides are used only where stricter or exceptional
- retention, classification, and access controls are not contradictory
- AML/CTF, privacy, and jurisdiction-specific obligations are represented where applicable

Flag under-specified regulatory posture and unsupported claims.

### 6) Source and Transform Review

If the domain declares source systems in `## Source Systems`, review the source layer:

#### Source File Conformance

- Each source system in the domain summary has a corresponding `sources/<system>/source.md` file
- Source files include platform, capability, and change model metadata
- Domain feed tables map every source table to a canonical entity
- Source schema tables are present with column-level detail
- `Destination` column uses correct formats (`Entity.Attribute` for direct, `[Name](#anchor)` for transforms)

#### Transform File Conformance

- Transform files follow `table_<source-table>.md` naming pattern
- Each transform has a level-3 heading, prose description, and YAML block
- YAML blocks declare `type`, `source_field`, `target_entity`, `target_attribute`
- Transformation types use the vocabulary from the Transformations spec (Section 8)
- Destination column in source schema tables links correctly to transform anchors

#### Source-Domain Consistency

- Every canonical entity that is claimed to receive data from a source has at least one mapping (domain feed table entry or transform destination)
- Source fields that map to PII attributes are flagged if entity governance does not already declare `pii: true`
- No source references appear in entity detail files (source-agnostic canonical layer is maintained)

If no source systems are declared, skip this step but note the absence as advisory — most production domains should declare at least one source.

---

## Output Format for Reviews

Return findings grouped by severity with explicit remediation:

- **Critical**: structural breakages or compliance risks
- **Major**: high-impact modelling decision issues
- **Minor**: consistency, naming, or clarity improvements

Each finding must include:

- Artifact path
- Section heading
- What is wrong
- Why it matters (spec/decision impact)
- Concrete fix recommendation

Also include:

- **Pass Summary**: what is already correct
- **Decision Summary**: per requested dimension (granularity, temporal, existence, mutability, conceptual→logical, standards, regulations)
- **Readiness Verdict**: `Not Ready`, `Conditionally Ready`, or `Ready`

---

## Review Guardrails

- Do not fabricate standards/regulatory facts.
- If uncertainty exists, mark as a question and request specific evidence.
- Prefer smallest corrective change that restores consistency.
- Keep structural findings and decision-quality findings distinct.
- When proposing fixes, preserve existing domain intent unless the user requests redesign.
