# Conceptual to Physical Realisation Guidance

## Purpose

Use this guidance when deciding how conceptual MD-DDL entities and relationships should be realised in a logical model and in a dimensional physical implementation.

This guidance is especially important for:

- role-based entities (for example, Customer as a Party Role)
- many-to-many relationships
- ownership vs lifecycle confusion
- `existence` value selection (`independent`, `dependent`, `associative`)

In recognized industry domains (banking, payments, insurance, healthcare, telecom),
apply this guidance alongside `../standards-alignment/SKILL.md` before finalizing
relationship granularity, `existence`, `mutability`, or temporal tracking choices.

---

## Three-Layer Thinking Pattern

Always reason in this order before finalising YAML:

1. **Conceptual meaning (domain summary)**
   - What does the concept mean in business language?
   - Is it a first-class concept or just a contextual role in another process?

2. **Logical realisation (entity detail + classDiagram)**
   - Which entity carries the relationship origin (`source`)?
   - What are the true cardinalities at business level?
   - Does the relationship need attributes or constraints?

3. **Physical realisation (dimensional target)**
   - Dimension, fact, or bridge?
   - SCD/temporal strategy based on `mutability` and `temporal.tracking`
   - Where many-to-many links materialise as effective-dated bridge structures

Do not choose `existence` from conceptual language alone.

---

## Relationship Ownership vs Entity Existence

These are different decisions and must not be conflated.

### Ownership (`relationships` YAML)

`ownership` answers: **which side originates and governs the relationship record?**

Example:

- `Customer Holds Account`
- `source: Customer`
- `ownership: Customer`

This means relationship detail belongs with Customer modelling artifacts.

### Existence (`entities` YAML)

`existence` answers: **can this entity stand as a meaningful business object independently?**

- `independent`: meaningful on its own; typically realised as a dimension candidate
- `dependent`: only meaningful in context of another entity; often fact-like
- `associative`: explicit many-to-many intersection carrying relationship semantics; bridge candidate

An entity can be `independent` even when it is relationship-owned by another entity.

---

## Many-to-Many Pattern (Customer ↔ Account)

When both sides can have multiple instances of the other:

- Conceptual: `Customer Holds Account`
- Logical: model M:N in classDiagram and relationship YAML from the origin side
- Physical dimensional realisation: materialise as an effective-dated bridge

Typical physical shape:

- `dim_customer`
- `dim_account`
- `bridge_customer_account` (with valid-from/valid-to and relationship role semantics where needed)

Do not force one side into `dependent` solely because a bridge is required.

---

## Existence Decision Heuristics for Dimensional Outcomes

### Mark as `independent` when

- The concept has stable identity and business meaning outside one specific link
- It is reused across multiple processes/facts
- It carries lifecycle/state tracked over time (often SCD)

Examples:

- Organisation
- Customer (role dimension with its own attributes/status)
- Account
- Product

### Mark as `dependent` when

- The record exists primarily to capture an event/measurement in context
- It is not commonly reused as a conformed dimension

Examples (domain-dependent):

- line-level transactional records
- process-stage snapshots tied to a parent process

### Mark as `associative` when

- The entity itself represents the M:N intersection and carries relationship attributes
- It is fundamentally a link object

Examples:

- Customer Account Relationship (if promoted to explicit entity)
- Party Agreement Relationship entity

---

## Authoring Rule for Relationship Details

If conceptual relationship is `A -> B`, relationship details belong with the origin modelling artifact for `A`.

In mixed detail-file styles, prefer co-locating the relationship section with the source entity file:

- `Customer Holds Account` in `customer.md`
- `Account Holds Product` in `account.md`

This keeps directional semantics, ownership rationale, and cross-entity constraints close to the source concept.

---

## Required Prompting Behaviour for Agent Ontology

When cardinality or ownership is discussed, the agent must explicitly ask or state:

1. Conceptual cardinality both directions
2. Logical source/ownership
3. Expected physical dimensional realisation (dimension/fact/bridge)
4. Whether `existence` still matches that physical target
5. Whether a standards constraint (if applicable) changes or narrows the preferred choice

If mismatch is found, explain and correct before finalising the entity YAML.
