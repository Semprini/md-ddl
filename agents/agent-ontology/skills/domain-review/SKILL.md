---
name: domain-review
description: Use this skill when the user asks to review, audit, validate, or quality-check an existing MD-DDL domain and its detail files. Also use before declaring a domain “complete” or production-ready. This skill performs both structural conformance checks and decision-quality checks for relationship granularity, temporal tracking, existence, mutability, conceptual-to-logical realization, standards alignment, and regulatory posture.
---

# Skill: Domain Review

Covers full-domain review of MD-DDL artifacts with two goals:
1) structural correctness against the MD-DDL specification, and
2) modelling decision quality against cross-skill guidance and standards/regulatory expectations.

**This is a contextual quality review, not a lint pass.** The review protocol below identifies structural breakages and decision-quality issues — it does not reject files for convention deviations, vocabulary differences, or organisational adaptations. See `md-ddl-specification/1-Foundation.md` "Validation Model" for the normative definition of what is and is not mechanically enforced.

**On vocabulary deviations:** If the domain uses non-standard field names or vocabulary (e.g., `phi` instead of `pii`, `data_class` instead of `classification`), note this as an **observation** with the flag "potential spec vocabulary gap" — do not flag it as a structural error or non-conformance. The deviation is signal about how the spec should evolve.

## References to Load

Load these references before performing the review:

- Domains spec: `md-ddl-specification/2-Domains.md`
	(reference stub: `../domain-scoping/references/domains-spec.md`)
- Entities spec: `md-ddl-specification/3-Entities.md`
	(reference stub: `../entity-modelling/references/entities-spec.md`)
- Enumerations spec: `md-ddl-specification/4-Enumerations.md`
	(reference stub: `../entity-modelling/references/enumerations-spec.md`)
- Relationships spec: `md-ddl-specification/5-Relationships.md`
	(reference stub: `../relationship-events/references/relationships-spec.md`)
- Events spec: `md-ddl-specification/6-Events.md`
	(reference stub: `../relationship-events/references/events-spec.md`)
- Sources spec: `md-ddl-specification/7-Sources.md`
	(reference stub: `../source-mapping/references/sources-spec.md`)
- Transformations spec: `md-ddl-specification/8-Transformations.md`
	(reference stub: `../source-mapping/references/transformations-spec.md`)
- Conceptual/physical realization: `../entity-modelling/conceptual-to-physical-realisation.md`
- Standards alignment: `../standards-alignment/SKILL.md`
- Regulatory compliance benchmark: `../../../agent-governance/skills/regulatory-compliance/SKILL.md`

If the domain is in a recognized industry (banking, payments, insurance, healthcare, telecom), standards and regulatory checks are mandatory, not optional.

---

## Review Protocol

Run the sections in order. Each catches a different class of problem.

### 0) Pre-Flight

If `md-ddl lint` is available, run it on the domain folder first (`md-ddl lint <folder>`,
or `python scripts/md_ddl_lint.py <folder>` in the MD-DDL repo). Its errors are the
mechanical tier: syntax, links, references, and representation agreement. Don't
re-derive them by eye. Classify them by what they break:

- **Critical:** errors that stop the YAML being read or resolved: `yaml-syntax`,
  `entity-references`, `domain-version`, `link-resolve` on a detail or type reference,
  `transform-target-resolve`, and `transform-case-values` (the last two break pipeline
  generation, not DDL).
- **Major:** errors where a representation disagrees with the YAML:
  `domain-diagram-coverage`, `domain-link-consistency`, `entity-heading-link`,
  `entity-diagram-links`, `entity-enum-in-diagram`, `entity-attribute-consistency`, and
  `mermaid-syntax`. The YAML is authoritative for generation, so these block promotion to
  Active but not generation from the YAML.

Warnings and observations feed the sections below.

Findings the linter can't see are classified by effect. **Critical:** the model contradicts
itself or the spec so that no correct artifact can be generated. **Major:** generation would
be non-deterministic or wrong for some artifact type (for example, pipelines but not DDL).
**Minor:** clarity and consistency.

### 1) Inventory and Coverage

Confirm all modeled artifacts are present and navigable:

- Domain file exists and includes Metadata, the overview diagram, and the Entities, Enums, Relationships, and Events tables (plus Data Products where declared)
- Every summary table Name link resolves to an existing detail file anchor
- Every referenced entity/enum/relationship/event appears exactly once in the expected section
- No orphaned detail files that are not represented in summary tables (unless explicitly marked draft)

### 2) Structural Conformance Review

Validate structure and formatting against MD-DDL spec:

- Heading hierarchy and section placement
- Mermaid syntax in diagrams; style conventions per `guides/diagram-style.md` (deviations are observations, not errors)
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

#### Source Summary Conformance

- Each source system in the domain summary has a corresponding `### <System>` summary under `## Sources` (conventionally in `sources/sources.md`, split out only once large)
- Source files are domain-rooted: level-1 heading names the domain and links back to it
- Metadata declares `id`, `owner`, `steward`, `change_model`, `data_quality_tier`, `status`, `version`
- `change_model` uses a declared value (`real-time-cdc`, `event-driven`, `batch-daily`, `batch-intraday`, `api-poll`, `manual`)
- A Source Overview Diagram is present, with edges labelled by change model
- The Feeds table declares Canonical Entity, Transform, Attributes Contributed, and Change Model
- Feeds list concrete subtypes actually instantiated, not abstract parents
- Domain-level `## Source Systems` links resolve to the source's summary anchor

#### Transform Detail Conformance

- Transform files are named for the source table, matching the source system's casing
- Hierarchy is repeated from the domain down; the source heading links back to its summary
- Source schema table uses the `Description` column and covers every source column
- `Destination` uses `Entity.Attribute` for direct maps and a rule-section link for non-direct; a column feeding several targets uses a comma-separated list
- Each non-direct mapping has a `Transform: ` heading, prose description, and YAML block
- YAML declares `type:` and `target: Entity · Attribute`; `system:` is omitted (implicit from the owning source)
- Transformation types come from the Section 8 vocabulary: `direct`, `derived`, `lookup`, `conditional`, `reconciliation`, `deduplication`, `aggregation`

#### Determinism Review

This is the part a structural check misses. Ask whether a generating agent would produce the same output twice:

- **Fan-out declared** — wherever one source row produces more than one canonical instance, an `Entity Fan-Out` section with a `produces:` block exists
- **Abstract targets bound** — any transform targeting an attribute on an abstract entity has a fan-out entry binding it to a concrete subtype
- **Identity derived** — wherever an instance identifier is not a direct map from a source column, a transform declares how it is derived: `derived` when it comes deterministically from the row, `deduplication` when rows must collapse into one instance
- **Survivorship declared** — wherever rows can merge, a `survivorship` rule exists; without one, output is order-dependent
- **Key branches exhaustive** — a `deduplication` key has a branch covering the case where the external identifier is absent
- **Evaluation order declared** — wherever `conditional` cases can overlap, `evaluation` is stated
- **Inputs complete** — every field a case predicate references is declared in `inputs:` or `source:`
- **Case keys valid** — for `enum:` targets, every case key is a real enum value
- **Predicate types match** — predicates compare columns against values of the source column's actual type
- **Blanks are decisions** — blank `Destination` cells mean deliberately unmapped, and the file states this convention
- **Unresolved is recorded** — undecided mappings, unknown code values, and contradictory source metadata appear in `Open Decisions`, not as blanks or guesses
- **Worked examples present** — anything beyond direct maps has examples covering each fan-out branch and each key branch, and every entity they produce is declared in the fan-out; entities fed by more than one source have a fan-in example

#### Source-Domain Consistency

- **Every `target` resolves** — the entity and attribute exist in the domain model, spelled as the model spells them, including inherited attributes. This is the most common defect in hand-authored transform detail; check it attribute by attribute rather than by eye
- Every canonical entity claimed to receive data from a source has at least one mapping (feed table entry or transform destination)
- Every entity in a `produces:` block appears in the source's Feeds table
- Source fields that map to PII attributes are flagged if entity governance does not already declare `pii: true`
- No source references appear in entity detail files (source-agnostic canonical layer is maintained)
- No source idiosyncrasies (null representations, legacy codes, format quirks) have leaked into entity definitions

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

- **Observations**: vocabulary deviations and convention differences, each noted as a possible spec contribution rather than a defect
- **Pass Summary**: what is already correct
- **Decision Summary**: per requested dimension (granularity, temporal, existence, mutability, conceptual→logical, standards, regulations)
- **Readiness Verdict**: `Not Ready`, `Conditionally Ready`, or `Ready`

---

## Semantic Validation

A review checks conformance, internal consistency, and declared metadata. It can't check
the following, which need people who know the domain. Mark them **Pending SME Review** in
the verdict unless the user confirmed them during the session.

### SME Review Checklist

Include this in every review output:

```markdown
### Pending SME Review
- [ ] Entity completeness — are all real-world concepts represented?
- [ ] Relationship accuracy — do the modelled relationships match actual business rules?
- [ ] Business process coverage — do events capture the full lifecycle?
- [ ] Governance correctness — are retention periods, classifications, and PII flags verified?
- [ ] Standards alignment — are Reference column mappings substantively correct?
- [ ] Enum completeness — do enum values cover all real-world cases?
```

---

## Model Readiness Definition

A domain model's readiness verdict determines whether it can proceed to physical artifact generation (Agent Artifact) or data product design (Agent Architect).

### Ready

All of the following must be true:

- Zero Critical findings
- Zero Major findings
- All entities have `existence` and `mutability` declared
- All entities have an `identifier: primary` attribute, or are deliberately Logic Objects
- All relationships have `cardinality`, `granularity`, and `ownership`
- Domain metadata includes `classification`, `pii`, `regulatory_scope`, and `default_retention`
- Governance blocks on entities with PII or elevated classification are present
- Mermaid diagrams are syntactically valid
- No unresolved `# TODO:` markers in production-status domains

### Conditionally Ready

- Zero Critical findings
- One or more Major findings that do not affect the specific physical target requested
- Example: missing `mutability` on a reference entity that is not part of the requested schema scope

When issuing a Conditionally Ready verdict, list the specific conditions under which generation can proceed and which artifacts would be affected if the Major findings are not resolved.

### Not Ready

- One or more Critical findings, OR
- Major findings that would produce incorrect physical artifacts (wrong dimensional grain, missing identifiers, contradictory temporal strategy)

**Which representation wins.** When the diagram, the summary tables, and the entity YAML
disagree, the YAML is authoritative for generation. The disagreement is still a finding,
because readers trust the diagram.

A Not Ready verdict must include a prioritised remediation plan.

### Handoff to Downstream Agents

**Ready:** tell the user the model can go to Agent Artifact (physical generation) and
Agent Architect (product design). **Conditionally Ready:** state which artifacts can proceed
now, and which conditions must be resolved first for the rest.

---

## Review Guardrails

- Do not fabricate standards/regulatory facts.
- If uncertainty exists, mark as a question and request specific evidence.
- Prefer smallest corrective change that restores consistency.
- Keep structural findings and decision-quality findings distinct.
- When proposing fixes, preserve existing domain intent unless the user requests redesign.
- **Do not use error/reject language for convention or quality issues.** Use `flag` / `note` / `observe` / `suggest` for Levels 3–5 concerns. Reserve `error` language for syntax-level failures (Level 1) only.
- **Treat vocabulary deviations as observations.** If an organisation uses non-standard terminology, note it as "potential spec vocabulary gap" rather than "non-conformance". Include it in the Observations section of the review output, not in Critical or Major findings.
