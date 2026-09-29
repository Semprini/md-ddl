---
name: relationship-events
description: Use when connecting entities with relationships; choosing relationship type, cardinality, granularity, or ownership; modelling hierarchies or networks within one entity; deciding between a relationship attribute and an entity attribute; or modelling business events ("what happens when X", "who initiates Y"), their payloads, and downstream impact.
---

# Skill: Relationships and Events

## MD-DDL Reference

- `md-ddl-specification/5-Relationships.md` (stub: `references/relationships-spec.md`):
  types, granularity, self-referential relationships, rules
- `md-ddl-specification/6-Events.md` (stub: `references/events-spec.md`): definition,
  rules, contextual payloads, temporal priority
- `../entity-modelling/conceptual-to-physical-realisation.md`: when cardinality or
  ownership affects physical realisation or `existence`
- `../standards-alignment/SKILL.md`: in industry domains, load it before settling
  granularity, ownership semantics, or event timing

---

## Relationships

**Type.** Use the vocabulary in `5-Relationships.md § Relationship Types`: `owns`,
`has`, `references`, `related_to`, `assigned_to`, `triggers`, `produces`, `supersedes`,
`governs`, `masks`. The list is extensible, and a new verb is a possible spec
contribution. For `owns` vs `has`, ask: "If the source is permanently deleted, should
the target go with it?" If it should, use `owns`; if it survives, use `has`.

**Granularity** matters for generation and is easy to miss, so ask rather than
defaulting when the domain has temporal or aggregation patterns:

- `atomic` (the default): direct join at full grain
- `group`: one side summarises the other; generates aggregation
- `period`: state as it stood at a point in time; generates a snapshot join

**Self-referential relationships** (ownership networks, hierarchies, family ties): the same
entity is both source and target, with `self_referential: true` and usually
`type: related_to`. Attributes of the link itself go under `relationship_attributes`.

**No foreign keys.** If the user asks for `Customer ID` on Order, explain that the
relationship `Customer Places Order` is the link. That keeps it visible and stops FK
drift. Offer to draft the relationship.

**Constraints spanning both ends** belong on the relationship, using `Entity.Attribute`
syntax (`check: "Customer.Status == 'Active'"`). Suggest them whenever the user
describes a rule that involves both entities.

For many-to-many or unclear ownership, use `conceptual-to-physical-realisation.md`
before fixing the ownership wording and the related `existence` values.

## Events

**Business, not mechanics.** "Order Placed", not "row inserted into orders". "Customer
Profile Updated", not "CDC delta on customer". If the user describes a technical trigger,
ask what it means for the business and which decision or process it enables.

**Actor vs entity.** The actor is *who caused* the event (a role, system, or person); the
entity is *what changed*. For "Loan Agreement Activated", the Credit Committee is the
actor and the Loan Agreement the entity.

**Payload** is the delta and the context, not a copy of the entity. Ask:

- what changed?
- what triggered it?
- who needs to know, and what do they do with it?

The last answer fills `downstream_impact`, which is high-value for governance. Payload
attributes use the same dictionary format as entity attributes, not a list of
single-key maps.

**Temporal priority** (Events Rule 9). Every event needs a timestamp or a sequence
attribute, or the timeline can't be reconstructed. Add one if the user doesn't:

```yaml
attributes:
  Event Timestamp:
    type: datetime
    description: When this event occurred in business time
```

---

## Relationship Checklist

- The heading hierarchy is rooted at the domain H1. The relationship is an H3 under
  `## Relationships`, with a description of *why* the connection exists.
- The YAML has `source`, `type`, `target`, `cardinality`, `granularity`, and `ownership`.
  Granularity is a decision, not a silent default.
- Cross-entity rules are constraints on the relationship. Neither entity gains an FK
  attribute.
- Self-referential links declare `self_referential: true`.

## Event Checklist

- An H3 under `## Events`, named in natural language ("Customer Preference Updated").
  The name appears only in the heading.
- The description gives the business trigger and meaning, with no CDC, SQL, or ETL.
- The YAML has `actor`, `entity`, `emitted_on`, `business_meaning`, and `downstream_impact`.
- Payload attributes are in dictionary format and include a timestamp or sequence.
- There's a `governance:` block only for overrides, and constraints only where actor or
  state must be validated.
