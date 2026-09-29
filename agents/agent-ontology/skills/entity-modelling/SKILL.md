---
name: entity-modelling
description: Use when modelling entities or attributes, when the user says "types of" or "kinds of", when inheritance questions arise, when deciding whether a concept is an entity, enum, attribute, or relationship attribute, when two similar concepts might be the same thing, when choosing existence, mutability, or temporal tracking, or when user stories should drive those choices.
---

# Skill: Entity Modelling

Covers concept classification, inheritance, existence and mutability, governance while
authoring, and the entity and enum detail files.

## MD-DDL Reference

- `md-ddl-specification/3-Entities.md` (stub: `references/entities-spec.md`): YAML,
  attributes, types, constraints, temporal tracking, existence, mutability, governance schema
- `md-ddl-specification/4-Enumerations.md` (stub: `references/enumerations-spec.md`)
- `guides/diagram-style.md`: classDiagram conventions (non-normative)
- `guidance.md`: industry patterns, hard cases, and inheritance, for ambiguous
  classification
- `conceptual-to-physical-realisation.md`: ownership vs existence, and how many-to-many
  and roles realise physically. Use it before finalising `existence`.
- `../standards-alignment/SKILL.md`: in industry domains, load before settling entity
  boundaries, `existence`, `mutability`, or temporal tracking

---

## Classifying a Concept

When the user is unsure what a concept is, reason it through with them before drafting.

Make it | When
--- | ---
**Entity** | It has its own identity and lifecycle, relates to several other entities, will gather attributes, needs its own audit or governance, and can exist before or after what it relates to
**Enum** | It's a controlled vocabulary that classifies something, with nothing beyond a label and light metadata. Nobody will ask "tell me everything about this value".
**Relationship attribute** | It only means something while two particular entities are connected (an effective date on a role assignment, a limit on a facility link)
**Attribute** | It's a simple property with no lifecycle, only ever reached through its parent, and not shared

When it's genuinely ambiguous, show the trade-off: an entity gives governance, audit, and
room to grow, at the cost of more relationships; an attribute is simpler but has no
lifecycle or audit; an enum costs nothing while stable, but can't carry attributes
without a refactor. `guidance.md` has the industry patterns and hard cases.

## Inheritance

Work through these questions with the user rather than choosing silently:

1. **Do subtypes share real attributes and constraints,** or just a label? A label calls
   for an enum discriminator on a single entity.
2. **Is the parent ever instantiated directly?** If not, mark it `<<abstract>>`.
3. **Do subtypes add meaningful attributes or constraints** (roughly three or more, or
   different rules)? If so, use `extends:`. If they're identical apart from a label,
   use a discriminator.
4. **Will they diverge?** If divergence is expected, separate them now even if they look
   alike today.

Roles are not subtypes. If an instance can hold several at once, or change between them,
model them as Party Roles (`guidance.md § Inheritance`).

## Existence and Mutability

Decide both for every entity. They drive physical generation directly, and a wrong
`existence` produces a wrong dimensional model. Ask when they aren't obvious.

`existence` | Meaning | Typical physical form
--- | --- | ---
`independent` | Meaningful on its own | Dimension
`dependent` | Only meaningful in the context of other entities | Fact
`associative` | Resolves a many-to-many and carries its own attributes | Bridge

`mutability` | Meaning | Typical physical form
--- | --- | ---
`immutable` | Never changes once written | Ledger, event store
`append_only` | New rows only | Log, transaction table
`slowly_changing` | Changes occasionally; history may matter | SCD Type 2
`frequently_changing` | Changes often; the current value matters | Overwrite
`reference` | Essentially static, admin-managed | Small lookup

Ownership of a relationship doesn't decide existence. An entity can be `independent`
and still be owned by another entity's relationship (`conceptual-to-physical-realisation.md`).

## User Stories as Evidence

User stories hold the *why* behind existence, mutability, and temporal choices. Before
deciding, gather every story that mentions the entity:

Story pattern | Signal
--- | ---
"…see all X for a Y over time" | X `dependent` on Y; `append_only`; temporal tracking
"…reconstruct what X looked like at a date" | `append_only` or bitemporal; flag for compliance review
"…query X with Y and Z context in real time" | X likely `dependent`, `append_only`; consumer-aligned product with an SLA; relationship granularity matters
"…analyse trends in X over a period" | `append_only`; analytical product (wide-column or dimensional)
"…manage X" (create, update, delete) | X `independent`; slowly or frequently changing; normalized operational product
"…look up X by an identifier" | X `independent`; `reference` or `slowly_changing`
"…flag X when a condition holds" | A constraint, or an event rather than polling
"…see the current X for Y" | X `dependent`; `frequently_changing`; no temporal tracking
"…audit who changed X and when" | Audit stereotype; `compliance_relevance`

When stories conflict (one needs current state, another needs history), say so. It
usually means one canonical entity feeds two products, for example an `append_only`
entity with a current-state view and a history view. Note the implied product
access patterns for Agent Architect.

## Governance While Authoring

Apply governance as you draft; don't leave it for a later pass. The schema and
inheritance rules are in `3-Entities.md § Governance Metadata Schema`.

- **Domain defaults** (`classification`, `pii`, `regulatory_scope`,
  `default_retention`) are set once in `domain.md` during domain scoping, and every
  entity inherits them.
- **Entity `governance:` blocks hold overrides only.** Include `pii`, `classification`,
  `retention`, or `access_role` only where they differ from the domain. Entities
  directly involved in regulatory reporting add `compliance_relevance` and
  `regulatory_reporting`. A weaker posture than the domain's needs a justification in
  `description` or `retention_basis`.
- **Inheriting entities** need no block. A block containing only `retention_basis` may
  optionally record *why* the default fits.
- **Unknowns** get `# TODO: confirm with data steward` rather than a guess. Leave
  jurisdiction-specific compliance questions to Agent Governance.

---

## Entity Detail File Checklist

- H1 is the domain name linked to `domain.md`. The entity is an H3 under `## Entities`.
- The classDiagram comes after the description and before the YAML, using the ELK layout.
  The subject class lists its own attributes only (not inherited ones), with the primary
  identifier prefixed `*`. Abstract entities are `<<abstract>>`. Reference classes are
  linked, not defined.
- The YAML has an `identifier: primary` attribute (or a deliberate Logic Object), plus
  `existence` and `mutability`, and no foreign-key attributes.
- Governance follows the rules above.
- Constraint keys are natural language (Key-as-Name).

## Enum Checklist

- An H3 under `## Enums`, in a file rooted at the domain H1.
- Values are natural language (`Politically Exposed`, not `PT` or `HI_CONF`).
- Use dictionary format when values carry metadata (description, sort order, score),
  and a simple list when they're labels only.
- For external standards, include a representative subset (5 to 15 values) plus a
  reference to the full standard.
