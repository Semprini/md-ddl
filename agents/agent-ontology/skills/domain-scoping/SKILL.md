---
name: domain-scoping
description: Use this skill when starting a new domain model, when the user says "model this domain" or describes a business area from scratch, when scoping or boundary questions arise, or when choosing between canonical and domain-driven modelling strategies. Also use when the user asks who should own a concept or whether two concepts are the same thing across different domains.
---

# Skill: Domain Scoping

Covers the interview protocol for new domains, the MD-DDL domain file structure,
and the modelling strategy decision (Canonical vs. Domain-Driven).

## MD-DDL Reference

Load the full Domains specification from `md-ddl-specification/2-Domains.md`
(reference stub: `references/domains-spec.md`) before drafting any domain file.
Key sections to apply:

- **Domain Declaration and Description** — H1 heading, free-text before H2
- **Domain Metadata** — YAML block under `## Metadata`, fields and categories
- **Domain Overview Diagram** — required Mermaid graph, ELK engine, rules for what to include and exclude
- **Domain Structure** — the four summary tables (Entities, Enums, Relationships, Events) and the rules that govern them

For canonical-vs-bounded-context boundary decisions, also load `domain-boundaries.md`.

---

## Interview Protocol

Run this protocol before drafting. Do not skip steps; each one surfaces a different
class of modelling error.

### Step 1 — Business Purpose
Understand *why* this domain exists before modelling *what* it contains.

Ask:
- What decisions or operations does this domain support?
- Who consumes the data from this domain, and what do they do with it?
- What goes wrong if this domain is missing or wrong?

**If the user describes downstream product requirements** (e.g., "this canonical
model will feed financial crime screening, transaction monitoring, and fraud
analytics"), extract canonical model constraints *before* beginning the entity
interview. Product consumer needs drive existence, mutability, and granularity
decisions — do not discover them after the fact:

- Real-time screening / sub-second query → `append_only` or `immutable`; SLA signal
- Historical state reconstruction (audit, replay) → temporal tracking required
- Cross-entity context in a single query (e.g., transaction + customer + account) → relationship granularity and entity scope decisions
- Regulatory re-presentation at a point in time → bi-temporal tracking

Note these as modelling constraints and carry them into Steps 2–4. Use the user
story mapping table in `../entity-modelling/SKILL.md § User Story to Modelling
Signals` to formalise the derivation if user stories are available.

### Step 2 — Candidate Concepts
Surface the nouns and verbs of the domain without committing to a structure yet.

Ask the user to describe the domain in plain language. Listen for:
- **Nouns** → candidate entities or enums
- **Verbs** → candidate relationships or events
- **Adjectives describing nouns** → candidate attributes or subtypes
- **Rules and conditions** → candidate constraints

Do not label these as entities/relationships/events during this step. Just capture
the vocabulary. Reflect it back to the user to confirm.

### Step 3 — Boundaries
Determine what is inside and outside this domain.

Ask:
- Are there concepts that *feel* like they belong here but might be owned elsewhere?
- Are there other teams or systems that model similar concepts?
- Should this domain be able to exist independently, or does it depend on concepts
  from another domain?

This surfaces the canonical vs. bounded context decision (see Modelling Strategy).

### Step 4 — Governance and Platform Posture
Capture the metadata inputs. These cannot be inferred.

Ask:
- Who is accountable for the business health of this data?
- Who is accountable for the technical health?
- Are there regulatory frameworks that apply (GDPR, AML, APRA, SOX, etc.)?
- How long does data in this domain need to be retained?
- What source systems feed this domain?
- How does the organisation relate data products to platforms? (single-platform, polyglot, or selective — see Section 9, Platform Posture)

If the user does not know, mark the relevant YAML fields with `# TODO:` and proceed.

Platform posture is typically an organisation-wide decision that shapes
downstream data product design. Recording it early in domain scoping ensures
Agent Architect has the context it needs.

### Step 5 — Standards Check
Before drafting, check whether Standards Alignment applies.

If the domain maps to an industry (banking, insurance, healthcare, payments, telecom):
load `skills/standards-alignment/SKILL.md` and run the standards check in parallel
with drafting.

---

## Requirements Intake Path

Use this path when the user brings **structured artefacts** rather than starting
from a blank conversation — business requirements documents, spreadsheets of
concepts, user stories, regulatory obligation lists, or process maps. This
complements (and feeds into) the standard interview protocol; it does not replace it.

**Triggers:**

- "I have a spreadsheet / requirements doc / BRD with concepts"
- "Here are our user stories"
- "Our regulatory team gave us a list of obligations"
- "We have a business requirements document for this domain"
- User pastes or uploads a structured list of concepts, rules, or stories

### Requirements Step 1 — Extract Vocabulary

Ask the user to share the document or its key contents. Parse it for:

- **Nouns** → candidate entities or enums
- **Verbs and processes** → candidate relationships or events
- **Rules and conditions** → candidate constraints
- **Regulatory obligations** → governance metadata and temporal tracking signals
- **Consumer roles and access patterns** → data product requirements; existence and mutability signals

Reflect the extracted vocabulary back to the user before categorising it:

> "I can see these key concepts: [list]. Before I classify them, does this capture
> the vocabulary you work with, or are there important terms missing?"

### Requirements Step 2 — Map Requirements to Modelling Decisions

For each extracted item, apply this mapping:

Requirement type | Modelling signal
--- | ---
Business concept with its own identity and lifecycle | Candidate entity
Classification or controlled vocabulary | Candidate enum
Rule applying only when two things are connected | Candidate relationship attribute
"Must be able to reconstruct [X] at any point in time" | Temporal tracking on X; consider bi-temporal
"Must retain [X] for [period] for [regulation]" | `retention` override on entity; `regulatory_reporting` field
"[Role] must be able to query [X] in real time" | Consumer-aligned product; SLA signal; mutability → `append_only` or `immutable`
"[X] changes frequently; current value is what matters" | mutability → `frequently_changing`
"[X] is created once and never modified" | mutability → `immutable`; existence → `independent`
"[X] only makes sense in the context of [Y]" | existence → `dependent`; candidate fact entity
"[X] connects [A] to [B] and carries its own attributes" | existence → `associative`

### Requirements Step 3 — Map User Stories to Model Signals

If the user provides user stories in `as an X I want Y so that Z` format, parse each
story for modelling signals:

Story element | Modelling signal
--- | ---
**X** (the role) | Consumer archetype; informs data product `consumers` field and access controls
**Y** (the capability) | Access pattern → schema type; entity and relationship scope; product class
**Z** (the outcome / "so that") | Non-functional requirement → SLA, mutability, temporal tracking, retention

Apply the full mapping table in the entity-modelling skill: `../entity-modelling/SKILL.md § User Story to Modelling Signals`.

> "You have [N] user stories. I am reading each one for entity scope, access patterns,
> and non-functional requirements that drive modelling decisions. Let me summarise
> what I found before we proceed."

### Requirements Step 4 — Identify Gaps

After extracting and mapping, identify what the requirements document does *not* answer
and flag them before starting the interview:

- Governance posture (classification, PII, retention basis) unless stated
- Domain ownership (steward, technical owner)
- Source systems that feed the domain
- Boundaries — concepts that may belong to a neighbouring domain
- Modelling strategy (Canonical vs. BoundedContext) if not implied

> "I have mapped the requirements to candidate modelling decisions. Before I start
> drafting, I still need to confirm: [gaps list]. I will ask about these in the
> interview, or you can tell me now if you know the answers."

### Requirements Step 5 — Transition to Interview

Continue with the standard interview protocol (Steps 1–5 above) to fill the gaps.
Skip any interview question already answered by the requirements artefact.

---

## Brownfield Interview Path

Use this path when the user wants to extend, modify, or integrate with an
**existing** domain model rather than starting from scratch. Triggers include:

- "Add an entity to [domain]"
- "We have a new source system to connect"
- "We need to add governance for [regulation]"
- "Model this new concept in the existing [domain]"
- Any request where a domain file already exists

### Brownfield Step 1 — Understand the Existing Model

Read the domain file and build context:

- What entities, relationships, events, and products already exist?
- What governance posture is declared?
- What source systems are connected?
- What modelling strategy is in use (Canonical vs. BoundedContext)?

Do not re-interview the domain's purpose or boundaries unless the user is
questioning them.

### Brownfield Step 2 — Scope the Change

Ask:
- What specifically are you adding or changing?
- Is this a new concept, an extension to an existing concept, or a correction?
- Does this change affect existing entities, relationships, or events?

Classify the change using the Domain Evolution rules from the Domains spec:

- **Breaking**: changes meaning or removes concepts → major version bump
- **Additive**: extends the model without altering existing meaning → minor bump
- **Corrective**: fixes errors without changing intended meaning → patch bump

### Brownfield Step 3 — Impact Assessment

Before modifying anything, assess impact:

- Which existing detail files are affected?
- Do any data products reference the affected entities?
- Will this change require updates to source mappings?
- Does the change affect the domain's governance posture?

Flag cross-cutting impacts to the user before proceeding to drafting.

### Brownfield Step 4 — Targeted Drafting

Apply the relevant specialist skill (Entity Modelling, Relationship & Events,
Source Mapping, etc.) for just the change in question. Update:

1. The affected detail files
2. The relevant summary tables in the domain file
3. The domain `version` field per version-bump rules
4. The domain overview diagram if entities or relationships changed

### Brownfield Step 5 — Baseline-to-Canonical Translation

Use this step when the user has baseline files (in `baselines/`) and wants to
create canonical entities from them. This extends the brownfield path for
adoption scenarios. See `md-ddl-specification/10-Adoption.md` for the full
adoption maturity model.

**Triggers:**

- "Translate baseline to canonical"
- "Create entities from baselines"
- "We have documented our existing state, now we want to model it"
- User has baselines and wants to advance from Level 1 (Documented) to
  Level 2 (Mapped)

**Process:**

1. **Read baseline files** as input context. Load the relevant `baselines/`
   files to understand what existing assets have been documented.

2. **Propose entity structure** derived from baselines:
   - From dimensional baselines: facts → business process entities,
     dimensions → business entities
   - From canonical baselines: existing entities → MD-DDL entities (may be
     1:1 or require restructuring)
   - From ETL baselines: pipeline targets → candidate entities
   - From catalog baselines: catalog assets → candidate entities

3. **Apply entity-modelling skill** for each proposed entity. Use the
   standard Entity Modelling skill for attribute decisions, type choices,
   and structural patterns.

4. **Create source transform files.** For each canonical entity, create
   transform files in `sources/*/transforms/` that define how source fields
   map to canonical attributes. If existing ETL code is available, parse it
   to generate draft transforms (see schema-import skill, Part 4). The
   transform file *is* the mapping — no separate mapping block is needed.

5. **Update domain adoption maturity.** When all identified entities have
   been created and transform files exist, update the domain metadata:
   `adoption.maturity: mapped`

**Boundary:** This step creates canonical entities and source transform files.
It does not create baseline files (that is the baseline-capture skill's job)
and does not generate physical artifacts (that is Agent Artifact's job).
Baseline-to-canonical mappings are derived from the transform files — no
separate mapping block is stored on baseline files (see
[10-Adoption.md](../../../../md-ddl-specification/10-Adoption.md)).

**Relationship to schema-import:** The schema-import skill provides a
fast-track path for users who have DDL and want to jump straight to a draft
domain. This brownfield step is the deeper, interview-driven route for
translating baselines that are not raw DDL (ETL pipelines, catalog metadata,
natural-language descriptions). Both paths converge at Level 2 (Mapped).

---

## Modelling Strategy

Determine and state the strategy explicitly in the domain description and in the
metadata `tags` field. Present both options to the user if it is not obvious.

### Canonical
**Use when:** the concept is universal across the organisation — reference data,
foundational objects (Party, Currency, Location), or data that must mean exactly
the same thing everywhere.

**Implications:**
- Strict governance; one domain owns it
- Other domains reference but do not redefine
- Changes require cross-domain impact assessment
- Tag: `Canonical`

### Domain-Driven (Bounded Context)
**Use when:** the concept has meaningfully different attributes or rules in different
business contexts, or teams need autonomous ownership.

**Implications:**
- The same real-world thing may appear as different entities in different domains
- They are mapped at integration time; each domain owns its version
- Lower governance overhead; higher integration complexity
- Tag: `BoundedContext`

**Decision prompt for the user:**

> "Does [concept] need to mean exactly the same thing everywhere in the organisation,
> or does [Team A]'s version of it differ meaningfully from [Team B]'s? If the answer
> is 'it's slightly different but close enough', that's often a signal for Canonical
> with a well-governed specialisation pattern."

---

## Domain File Checklist

Before handing a domain file to the user for review, confirm:

- [ ] H1 heading matches the agreed domain name
- [ ] Description explains business purpose, not technical implementation
- [ ] All required metadata fields present (or flagged `# TODO:`)
- [ ] `regulatory_scope` lists all frameworks identified in Step 4
- [ ] Domain Overview Diagram uses `graph TD` or `graph LR` with ELK engine
- [ ] Diagram includes all entities, inheritance arrows, and labelled relationship edges
- [ ] Diagram hyperlinks are on the 3–5 most central entities only
- [ ] All four summary tables present (Entities, Enums, Relationships, Events)
- [ ] Every Name cell contains a Markdown link to the detail file anchor
- [ ] `Specializes` column populated for all subtypes
- [ ] No H3 headings in the domain file (H3 is reserved for detail files)
- [ ] Modelling strategy stated in description and tags

---

## Domain Authoring Checklist

When creating a complete domain from scratch, follow this sequence. Each step
references the skill that owns detailed guidance.

1. **Domain file** - `domain.md`
  - Metadata, governance, overview diagram, summary tables
  - Guidance: this skill (Domain File Checklist)
  - Standards: load standards-alignment when industry standards apply

2. **Entity detail files** - `entities/*.md` (one per entity)
  - Attributes, existence, mutability, temporal, governance, diagrams
  - Guidance: `../entity-modelling/SKILL.md` (Entity and Enum checklists)
  - Decisions: concept realisation framework and inheritance reasoning

3. **Enumerations file** - `enums.md`
  - Domain enum declarations (or co-located enum sections where appropriate)
  - Guidance: `../entity-modelling/SKILL.md` (Enum checklist)
  - External standards: representative subset (5 to 15 values) plus standard reference

4. **Relationship YAML** - co-located in entity files
  - Type, cardinality, granularity, constraints
  - Guidance: `../relationship-events/SKILL.md` (Relationship checklist)

5. **Event files** - `events/*.md` (one per event)
  - Actor, entity, emitted_on, payload, governance
  - Guidance: `../relationship-events/SKILL.md` (Event checklist)

6. **Source system files** - `sources/*/source.md`
  - Change model, feeds table, data quality tier
  - Guidance: `../source-mapping/SKILL.md` (Source File checklist)

7. **Data product files** - `products/*.md`
  - Class, entities, SLA, governance overrides, masking
  - Guidance: `../../agent-architect/skills/product-design/SKILL.md`

8. **Update `domain.md` summary tables**
  - Ensure Entities, Enums, Relationships, Events, and Data Products reflect
    all created detail files
