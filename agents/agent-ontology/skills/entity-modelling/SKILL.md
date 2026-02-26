---
name: entity-modelling
description: Use this skill when modelling entities or their attributes, when the user says "types of" or "kinds of" something, when inheritance questions arise, or when deciding whether a concept should be a first-class entity, an enum, an attribute, or a relationship attribute. Also use when the user is unsure whether two similar concepts are the same entity or separate ones.
---

# Skill: Entity Modelling

Covers concept realisation decisions, inheritance hierarchies, entity YAML structure,
attribute definitions, constraints, and enumeration definitions.

## MD-DDL Reference

- Full entity specification: `references/entities-spec.md`
  (source: `md-ddl-specification/3-Entities.md`)
- Full enumeration specification: `references/enumerations-spec.md`
  (source: `md-ddl-specification/4-Enumerations.md`)
- Conceptual-to-physical realization guidance: `conceptual-to-physical-realisation.md`
  (use for ownership/cardinality decisions, dimensional implementation reasoning,
  and final `existence` value selection)

Read the relevant reference before drafting any entity or enum. Key sections:

**Entities spec:** Entity Declaration, Entity Diagram rules, Entity Definition (YAML),
Key-as-Name principle, Attribute Properties, Type System, Constraint Definition,
Temporal Tracking, Existence, Mutability, Naming Rules.

**Enumerations spec:** Enum Declaration, Simple vs. Dictionary format,
Naming Rules (natural language values).

---

## Concept Realisation Framework

When the user is uncertain what a concept *is*, apply this framework and explain
your reasoning before drafting anything.

### Make it an Entity if:
- It has its own identity and lifecycle independent of other entities
- It will have relationships to multiple other entities
- It will accumulate attributes over time
- It is auditable or requires its own governance posture
- It can exist before or after the things it relates to

### Make it an Enum if:
- It is a fixed or slowly-changing controlled vocabulary
- It classifies or categorises another entity
- It has no attributes beyond a label and optional metadata (description, sort order)
- No one will ever say "tell me everything about this [value]"

### Make it a Relationship Attribute if:
- The property only makes sense when two specific entities are connected
- It describes the terms or nature of a connection, not a standalone fact
- Examples: `effective_date` on a role assignment; `limit` on a credit facility link

### Make it an Attribute of an existing Entity if:
- It is a simple property with no independent lifecycle
- It is only ever referenced through its parent entity
- It cannot be shared across or re-used by other entities

**When it is genuinely ambiguous**, present the options to the user as a short
trade-off table:

| Option | Advantage | Disadvantage |
|---|---|---|
| Separate entity | Full governance, auditable, extensible | More relationships to manage |
| Attribute | Simpler model | No independent lifecycle or audit trail |
| Enum | Zero maintenance if stable | Can't evolve to carry attributes later without a refactor |

---

## Inheritance Reasoning

When a user describes "types of" something, or entities that share common properties,
walk through this logic explicitly before committing to a hierarchy.

**Step 1 — Is shared behaviour real?**
Do the candidate subtypes share actual attributes and constraints, or just a label?
If only a label → use an Enum discriminator on a single entity, not inheritance.

**Step 2 — Is the parent instantiated directly?**
Will anyone ever create a bare instance of the parent, or only ever a specific subtype?
If only subtypes → mark the parent `<<abstract>>` in the classDiagram.

**Step 3 — Do subtypes add meaningful attributes or constraints?**
If the subtypes are identical except for a type label → discriminator attribute is cleaner.
If subtypes add 3+ distinct attributes or meaningfully different constraints → separate entities with inheritance.

**Step 4 — Will subtypes diverge over time?**
High divergence expected → separate entities now, even if they look similar today.
Stable and similar → discriminator attribute with an enum.

Present this reasoning to the user before drafting. Do not silently choose a pattern.

---

## Existence and Mutability

These are required for every entity. They directly drive compiler output — do not
omit them or leave them as defaults without a conscious decision.

**Existence** (what is this entity's independence?)

| Value | Use when | Compiler hint |
|---|---|---|
| `independent` | Meaningful on its own | Candidate dimension |
| `dependent` | Only meaningful in context of other entities | Candidate fact |
| `associative` | Resolves a many-to-many; carries relationship attributes | Bridge table |

**Mutability** (how does this entity's data change?)

| Value | Use when | Compiler hint |
|---|---|---|
| `immutable` | Once written, never changes | Ledger / event store |
| `append_only` | New rows added; existing rows never updated | Log / transaction |
| `slowly_changing` | Changes occasionally; history may matter | SCD Type 2 |
| `frequently_changing` | Changes often; current value is what matters | Overwrite |
| `reference` | Essentially static; admin-managed | Small lookup table |

Ask the user explicitly if these are not obvious. A wrong existence value produces
a wrong dimensional model.

When relationship cardinality/ownership materially affects dimensional realization,
apply `conceptual-to-physical-realisation.md` before finalizing `existence`.

---

## Entity Detail File Checklist

Before presenting a drafted entity detail file:

- [ ] File begins with H1 heading with domain name as a link to domain.md
- [ ] Entity introduced with H3 heading under `## Entities`
- [ ] classDiagram present immediately after description, before YAML
- [ ] ELK layout engine declared in diagram config
- [ ] Subject class shows all attributes with correct Mermaid type syntax
- [ ] Inherited attributes are **not** repeated in the subject class
- [ ] Primary identifier prefixed with `*` in diagram
- [ ] Abstract entities marked `<<abstract>>`
- [ ] All reference classes defined at bottom of diagram with hyperlinks
- [ ] At least one attribute with `identifier: true` in YAML
- [ ] `existence` and `mutability` declared
- [ ] No foreign key attributes present
- [ ] Domain-level governance defaults are confirmed for the entity
- [ ] If a `governance:` block is present, it contains only override fields and `# TODO:` where required
- [ ] Constraint keys use natural language (Key-as-Name principle)

---

## Enum Detail File Checklist

- [ ] File begins with domain H1 heading and link back to domain.md
- [ ] Enum under H3 heading within `## Enums` section
- [ ] Values use natural language (not PT, ACTIVE, HI_CONF)
- [ ] Dictionary format used if values carry metadata (description, sort order, score)
- [ ] Simple list format used if values are labels only
