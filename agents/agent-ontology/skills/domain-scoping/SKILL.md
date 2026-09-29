---
name: domain-scoping
description: Use when starting a new domain model ("model this domain", a business area described from scratch), when the user brings requirements documents, user stories, or concept spreadsheets, when extending an existing domain, when translating baselines into canonical entities, or when scoping, ownership, or canonical-vs-bounded-context questions arise.
---

# Skill: Domain Scoping

Covers the interview before drafting (greenfield, from requirements, or brownfield), the
modelling strategy decision, and the domain file itself.

## MD-DDL Reference

Load `md-ddl-specification/2-Domains.md` (stub: `references/domains-spec.md`) before
drafting a domain file. Diagram conventions (ELK layout, hyperlinks) are in
`guides/diagram-style.md`. For canonical-vs-bounded-context decisions, also load
`domain-boundaries.md`.

---

## Greenfield Interview

Each area surfaces a different kind of modelling error, so cover all of them. Skip
anything the user has already answered.

1. **Purpose.** What decisions or operations does the domain support? Who consumes its
   data, and what goes wrong if it's missing or wrong? When the user describes downstream
   consumers (screening, monitoring, analytics), extract their needs as modelling
   constraints *now*, before the entity interview:
   - real-time or sub-second queries → `append_only` or `immutable`, plus an SLA signal
   - reconstructing past state for audit or replay → temporal tracking
   - point-in-time regulatory re-presentation → bitemporal tracking
   - cross-entity context in one query → relationship granularity and entity scope
2. **Candidate concepts.** Have the user describe the domain in plain language. Capture
   nouns (entities, enums), verbs (relationships, events), qualifiers (attributes,
   subtypes), and rules (constraints) without committing to a structure yet. Reflect the
   vocabulary back and confirm it.
3. **Boundaries.** Which concepts feel as if they belong here but may be owned elsewhere?
   Which other teams model similar things? Can the domain stand alone? This leads to
   the modelling strategy decision.
4. **Governance and platform.** Business and technical owners, regulatory frameworks,
   retention, feeding source systems, and platform posture (single-platform, polyglot, or
   selective; `9-Data-Products.md § Platform Posture`). These can't be inferred. Mark
   unknowns `# TODO:` and continue.
5. **Standards.** In an industry domain (banking, payments, insurance, healthcare,
   telecom), load Standards Alignment before settling structural decisions.

## From Requirements Artefacts

When the user brings requirements documents, concept spreadsheets, user stories, obligation
lists, or process maps, extract the vocabulary from them first, then run the interview
only for what they leave unanswered.

Requirement | Modelling signal
--- | ---
A concept with its own identity and lifecycle | Candidate entity
A classification or controlled vocabulary | Candidate enum
A rule that applies only when two things are connected | Relationship attribute
"Must reconstruct X at any point in time" | Temporal tracking on X; consider bitemporal
"Must retain X for a period under regulation R" | `retention` override; regulatory reporting
"Role must query X in real time" | Consumer-aligned product; SLA; `append_only` or `immutable`
"X changes often; only the current value matters" | `frequently_changing`
"X is created once and never modified" | `immutable`
"X only makes sense in the context of Y" | `existence: dependent`
"X connects A and B and has its own attributes" | `existence: associative`

For user stories, use the mapping in `../entity-modelling/SKILL.md § User Story to
Modelling Signals`. Then list what the artefacts don't answer (governance posture,
ownership, sources, boundaries, strategy) and cover those in the interview.

## Brownfield: Changing an Existing Domain

Read the domain file first: its entities, relationships, events, products, governance,
sources, and strategy. Don't re-interview purpose or boundaries unless the user is
questioning them.

1. **Scope the change.** Is it new, an extension, or a correction? Classify it as
   breaking, additive, or corrective for the version bump (see the Lifecycle skill).
2. **Assess impact** before editing: affected detail files, data products that use the
   affected entities, source mappings, and the governance posture. Raise cross-cutting
   impacts with the user.
3. **Draft only the change** with the relevant skill, then update the summary tables, the
   overview diagram (if entities or relationships changed), and `version`.

### Baselines to Canonical Entities

When `baselines/` exist and the user wants to move from Documented to Mapped
(`guides/adoption-playbook.md`), follow these steps:

1. Read the baselines.
2. Propose entities from them. From dimensional baselines, facts become business
   process entities and dimensions become business entities. From canonical
   baselines, map existing entities to MD-DDL entities, one-to-one or restructured.
   From ETL, pipeline targets are candidates; from catalogues, catalogue assets are.
3. Model each entity with Entity Modelling.
4. Write source transform detail for each source table
   (`sources/<system-id>/table_<TABLE>.md`), with an `Entity Fan-Out` wherever a legacy
   row combines concepts the canonical model separates. Existing ETL code can seed the
   transforms (schema-import skill). The transform file *is* the mapping; baselines
   carry no separate mapping block.
5. When every identified entity and its transforms exist, set `adoption.maturity: mapped`.

Creating baselines is the Baseline Capture skill's job. For raw DDL, Schema Import is
the faster route to the same point.

---

## Modelling Strategy

State the strategy in the domain description and in `tags`. If it isn't obvious, put
both options to the user.

- **Canonical** (tag `Canonical`) suits concepts that must mean exactly the same
  everywhere: reference data and foundational objects (Party, Currency, Location). One
  domain owns the concept and others reference it without redefining it. Governance is
  strict and changes need cross-domain impact assessment.
- **Bounded context** (tag `BoundedContext`) suits concepts with meaningfully different
  attributes or rules per business context, or teams that need autonomy. Each domain
  owns its version, and the versions are mapped at integration time. Governance
  overhead is lower but integration is more complex.

A useful question: does the concept need to mean the same thing everywhere, or does one
team's version differ meaningfully from another's? "Slightly different but close enough"
usually points to Canonical with a governed specialisation.

---

## Domain File Checklist

- H1 is the agreed domain name. The description explains business purpose, not implementation.
- Every required metadata field is present or marked `# TODO:`. `regulatory_scope`
  lists every framework identified.
- The overview diagram is `graph TD` or `graph LR`, shows all entities, inheritance, and
  relationship edges whose labels match the Relationships section, and links the
  abstract and most-referenced entities.
- Summary tables: Entities, Enums, Relationships, Events, and Data Products when present.
  Each Name cell links to its detail anchor, and `Specializes` is filled for subtypes.
- No H3 headings in the domain file. H3 is reserved for detail definitions.
- The modelling strategy appears in both the description and `tags`.

After the domain file comes the rest of a new domain. Each part has its own skill and
checklist:

- entity files, then enums: Entity Modelling
- relationships (in the entity files), then events: Relationship & Events
- source summaries and transform detail: Source Mapping
- product files: Agent Architect

Finish by bringing the domain's summary tables into line with every detail file.
