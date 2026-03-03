---
name: relationship-events
description: Use this skill when connecting entities with relationships, when modelling what happens when something changes (business events), when cardinality or ownership questions arise, when the user asks "what happens when X" or "who initiates Y",  or when deciding whether something is a relationship attribute vs. an entity attribute. Also use when the user asks about event payloads, downstream impacts, or temporal sequencing of business state changes.
---

# Skill: Relationships & Events

Covers relationship semantics, cardinality, granularity, relationship constraints,
event structure, event payloads, temporal priority, and the distinction between
business events and technical mechanics.

## MD-DDL Reference

- Full relationships specification: `references/relationships-spec.md`
  (source: `md-ddl-specification/5-Relationships.md`)
- Full events specification: `references/events-spec.md`
  (source: `md-ddl-specification/6-Events.md`)
- Cross-skill conceptual/physical guidance: `../entity-modelling/conceptual-to-physical-realisation.md`
  (use when cardinality/ownership decisions affect dimensional realization and
  `existence` interpretation)
- Cross-skill standards guidance: `../standards-alignment/SKILL.md`
  (load before finalizing granularity and temporal choices in industry-standard domains)

Read the relevant reference before drafting. Key sections:

**Relationships spec:** Relationship Declaration, Definition (YAML), Relationship
Types, Granularity table, Relationship Rules, Naming Rules.

**Events spec:** Event Declaration, Event Description, Event Definition (YAML),
Event Rules, Contextual Payloads, Temporal Priority.

If modelling in a recognized industry domain (banking, payments, insurance,
healthcare, telecom), load `../standards-alignment/SKILL.md` before finalizing:
- relationship granularity
- relationship ownership semantics tied to standard abstractions
- event temporal tracking shape (timestamp/sequence expectations)

---

## Relationship Authoring Guide

### Choosing the Relationship Type

Present this table to the user when the relationship type is ambiguous:

| Type | Meaning | Example |
|---|---|---|
| `owns` | Target's life is bound to source. Source deletion cascades. | Customer owns Account |
| `has` / `associates_with` | Both entities exist independently | Contact has Location |
| `references` | One entity points to another for lookup only | Transaction references Currency |
| `assigned_to` | Functional link or responsibility | Claim assigned_to Adjuster |
| `triggers` | One entity/event initiates another | Application Submitted triggers Credit Check |
| `produces` / `results_in` | Outcome of a process | Assessment produces Risk Score |
| `supersedes` / `replaces` | Versioning or correction | New Policy supersedes Old Policy |
| `governs` | Rules or domain controlling an entity | GDPR Policy governs Customer PII |
| `masks` / `protects` | Security-specific | Vault Service masks Credit Card Number |

**Ownership test:** Ask the user — "If the [source] is permanently deleted, should
the [target] also be deleted, or should it survive?" If survive → `has`. If delete
cascade → `owns`.

### Granularity Decision

Granularity is easy to miss but critical for compiler output. Ask explicitly.

In industry-standard domains, confirm Standards Alignment has been loaded before
locking granularity, because standard definitions may constrain whether the
relationship is atomic, grouped, or period-based.

| Value | When to use | Compiler output |
|---|---|---|
| `atomic` | One instance on each side participates directly | Direct join at full grain |
| `group` | One side represents a collection or summary of the other | Aggregation logic |
| `period` | Captures state as it stood at a point in time | Point-in-time join / snapshot |

Default is `atomic` if not specified — but confirm this with the user rather than
silently defaulting when the domain has temporal or aggregation patterns.

When many-to-many relationships or ownership ambiguity is present, apply
`../entity-modelling/conceptual-to-physical-realisation.md` before finalizing
relationship ownership wording and associated entity-existence decisions.

### Foreign Key Rule

**Never add foreign key attributes to entities.** If the user requests one, redirect:

> "In MD-DDL, `Customer ID` doesn't appear inside the `Order` entity YAML. Instead,
> the relationship `Customer Places Order` creates that link. This prevents foreign
> key drift and keeps the relationship semantically visible in the model. Shall I
> draft that relationship?"

### Relationship Constraints

Relationships can carry their own constraints that reference attributes from
*both* the source and target. Use `Entity.Attribute` syntax:

```yaml
constraints:
  Active Customers Only:
    check: "Customer.Status == 'Active'"
    description: Orders can only be placed by active customers
```

This is a first-class modelling pattern — not just validation logic buried in code.
Proactively suggest relationship constraints when the user describes rules that
span two entities.

---

## Event Authoring Guide

### The Core Distinction

Events describe *what happened in the business*, not *how the database recorded it*.

| ❌ Technical (wrong) | ✅ Business (correct) |
|---|---|
| Row inserted into `orders` | Order Placed |
| CDC delta on `customer` table | Customer Profile Updated |
| ETL batch completed | Daily Position Snapshot Generated |

If the user describes a technical trigger, ask: "What does this mean for the
business? What decision or process does this change enable?"

### Payload Design

Event payloads should capture the **delta** (what changed) and the **context**
(why it changed) — not a full copy of the entity state.

Ask the user:
- What specific fields changed?
- What triggered the change (actor, system, or rule)?
- Who needs to know about this, and what do they do with it?
- Are there downstream systems or processes that must react?

The `downstream_impact` field in the event YAML is high-value for governance.
Populate it from the user's answer to the third question above.

### Temporal Priority — Non-Negotiable

Every event **must** carry either a timestamp or a sequence attribute. This is Rule 9
in the Events spec and is non-negotiable. Without it, the knowledge graph cannot
reconstruct the timeline of an entity's state.

If the user does not specify one, add it and explain why:

```yaml
attributes:
  - event timestamp:
      type: datetime
      description: When this event occurred in business time
```

### Actor vs. Entity

These are distinct and both required:

- **Actor** — who or what initiated the event (a role, a system, a person)
- **Entity** — the primary business object whose state changed

If the user conflates them, clarify:

> "In MD-DDL, the actor is *who caused* the event, and the entity is *what changed*.
> For 'Loan Agreement Activated', the actor might be the Credit Committee (who approved
> it) and the entity is the Loan Agreement (what changed state). Does that match
> your intent?"

---

## Relationship Detail File Checklist

- [ ] File begins with domain H1 heading and link back to domain.md
- [ ] Relationship under H3 heading within `## Relationships` section
- [ ] Business description explains *why* this connection exists
- [ ] YAML includes `source`, `type`, `target`, `cardinality`, `granularity`, `ownership`
- [ ] Relationship type chosen from the approved type list
- [ ] Granularity explicitly set (not silently defaulted)
- [ ] Constraints block present if any cross-entity rules apply
- [ ] No foreign key attributes added to either entity

## Event Detail File Checklist

- [ ] File begins with domain H1 heading and link back to domain.md
- [ ] Event under H3 heading within `## Events` section
- [ ] Business description explains the trigger and meaning (no technical mechanics)
- [ ] YAML includes `actor`, `entity`, `emitted_on`, `business_meaning`
- [ ] `downstream_impact` populated
- [ ] Domain-level governance defaults are confirmed for the event
- [ ] `governance` block is included only when the event needs an override
- [ ] At least one timestamp or sequence attribute present (temporal priority rule)
- [ ] Constraints block present if actor/ownership validation is needed
- [ ] Event name uses natural language (not camelCase, not past-tense verb only)
