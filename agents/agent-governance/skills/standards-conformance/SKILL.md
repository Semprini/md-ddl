---
name: standards-conformance
description: >-
  Audit an existing MD-DDL domain model against industry standards (BIAN, FHIR,
  ISO 20022, TM Forum, ACORD) and produce a structured conformance report. Use
  when the user asks "is this model aligned with [standard]?", "check BIAN
  conformance", "FHIR alignment audit", "standards conformance report", "does
  this follow [industry standard]?", or for any post-modelling standards quality
  check. Always load the relevant standard reference files before assessing
  conformance.
---

# Standards Conformance — Skill

## Purpose

Audit an existing MD-DDL domain model against one or more industry standards
(BIAN, FHIR, ISO 20022, TM Forum, ACORD) and produce a structured conformance
report. This is **assurance-time** work — the model already exists and the auditor
checks alignment quality.

### Distinction from Standards Alignment (Agent Ontology)

Activity | Agent | When
--- | --- | ---
Apply standard naming and patterns during design | Ontology (standards-alignment) | During modelling
Audit alignment quality after modelling | Governance (standards-conformance) | After modelling

Agent Ontology's `standards-alignment` skill helps users choose entity names,
attribute patterns, and structural conventions that align with a target standard
during the modelling process. This skill evaluates an already-modelled domain
against the standard and reports conformance findings.

---

## Process

### Step 1 — Identify Target Standard(s)

Ask the user which standard(s) they want to audit against. If the domain file
declares a `standards_reference` or `Reference` column in its Entities table,
use that as a starting point.

Supported standards:

Standard | Reference location
--- | ---
BIAN | `industry_standards/bian/`
FHIR R4 | `industry_standards/fhir/r4/`
TM Forum | `industry_standards/tmforum/v4/`
ISO 20022 | Load from standards-alignment references
ACORD | Load from standards-alignment references

### Step 2 — Load Standard References

Load the relevant industry standard reference files **before** assessing
conformance. Do not assess conformance from training knowledge alone.

For BIAN: Load business object definitions, service domain mappings, and
enumeration lists from `industry_standards/bian/`.

For FHIR: Load resource type definitions and profiles from
`industry_standards/fhir/r4/`.

For TM Forum: Load entity type definitions from `industry_standards/tmforum/v4/`.

### Step 3 — Read the Domain Model

Read the domain file and all entity detail files. For each entity, note:

- Entity name
- Attributes (names, types, constraints)
- Relationships (partners, cardinality)
- Reference column value (if present in domain file)
- Governance metadata

### Step 4 — Assess Conformance

For each entity, evaluate against the target standard:

Check | What to look for
--- | ---
**Naming alignment** | Does the entity name match or closely correspond to the standard's terminology?
**Attribute coverage** | Are the standard's expected attributes present? Are additional attributes justifiable extensions?
**Relationship patterns** | Do relationships match the standard's structural expectations (cardinality, ownership)?
**Enum alignment** | Do enum values map to the standard's code lists or value sets?
**Granularity match** | Does the entity's granularity (existence, mutability) align with the standard's concept?

Conformance is **graded**, not binary:

Grade | Meaning
--- | ---
**Full** | Entity name, attributes, and relationships closely match the standard's definition.
**Partial** | Entity is recognisably aligned but has naming differences, missing attributes, or structural deviations.
**Non-conformant** | Entity covers similar concepts but diverges significantly from the standard's structure or terminology.
**N/A** | Entity has no counterpart in the target standard (domain-specific extension).

### Step 5 — Produce Conformance Report

Use the report format below. Include specific findings and actionable
recommendations for each entity.

---

## Report Format

```markdown
## Standards Conformance Report: [Domain Name]

### Target Standard: [Standard Name and Version]
**Assessment date:** [date]
**Assessed by:** Agent Governance (standards-conformance skill)

### Summary

- Entities audited: N
- Full conformance: N
- Partial conformance: N
- Non-conformant: N
- Not applicable: N

### Entity-Level Findings

#### [Entity Name]
- **Conformance:** Full | Partial | Non-conformant | N/A
- **Standard reference:** [Standard entity/resource/service domain]
- **Findings:** [Specific alignment or misalignment notes]
- **Recommendation:** [If partial or non-conformant, what structural change
  would improve alignment — defer to Agent Ontology]

### Cross-Cutting Observations

[Patterns observed across multiple entities — systematic naming differences,
consistent attribute gaps, structural conventions that differ from the standard]

### Recommendations Summary

[Prioritised list of recommended changes, each tagged with the agent that
should implement it]

### What This Audit Cannot Assess

- Whether the standard version used is the correct target for the organisation
- Whether domain-specific extensions are justified by business requirements
- Whether conformance gaps are acceptable trade-offs or genuine deficiencies
- Whether the standard's reference files are current and complete
```

---

## Non-Negotiable Rules

- Never modify entity, relationship, or domain files. Produce findings and
  recommendations only.
- Always load the relevant standard reference files before stating conformance.
  Do not assess conformance from training knowledge alone.
- Structural changes (entity rename, attribute addition, relationship redesign)
  are recommendations that defer to Agent Ontology.
- Conformance is graded, not binary. "Partial" is a valid and common state —
  it means the entity is recognisably aligned but not fully conformant.
- When a domain uses different terminology from the standard but maps to the
  same concept, note it as a naming deviation, not a structural gap.
- Do not recommend changes that would break existing relationships, events, or
  data product declarations without flagging the downstream impact.
