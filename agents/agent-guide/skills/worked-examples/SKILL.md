---
name: worked-examples
description: Use this skill when the user asks to see an example, says "walk me through", "show me how [concept] looks in practice", mentions the Simple Customer or Financial Crime example, or wants to understand how a complete MD-DDL model is structured. Also use when a user asks for a concrete demonstration of a concept after it has been explained.
---

# Skill: Worked Examples

Covers interactive walkthroughs of the three reference examples in this repository.
Teaches by exploring real artifacts — domain files, entity details, relationships,
events, governance metadata, and data products — with guided commentary.

---

## Example Tracks

### Track 1 — Simple Customer (Beginner)

**Location:** `examples/Simple Customer/`
**Scope:** 3 entities, 1 enum, 1 relationship, 1 event
**Best for:** First-time users, users who want the smallest complete example

**Files:**

- `domain.md` — Domain declaration, metadata, overview diagram, summary tables
- `details.md` — Entity detail YAML, enum values, relationship YAML, event YAML

### Track 2 — Financial Crime (Intermediate)

**Location:** `examples/Financial Crime/`
**Scope:** 21 entities (with inheritance hierarchies), 10 enums, 14 relationships,
7 events, 3 data products, 3 source systems
**Best for:** Users who want a production-quality reference; exploring advanced
features like inheritance, governance metadata, standards alignment, data products

**Files:**

- `domain.md` — Full domain with metadata, overview diagram, all summary tables
- `entities/` — One file per entity with full YAML, diagrams, and constraints
- `events/` — One file per event with YAML definitions
- `products/` — Data product declarations (canonical, analytics, source-feeds)
- `sources/` — Source system declarations with transformation mappings

### Track 3 — Healthcare (Intermediate)

**Location:** `examples/Healthcare/`
**Scope:** 12 entities, 11 enums, 14 relationships, 4 events, 2 data products,
2 source systems
**Best for:** Users exploring standards-aligned healthcare modelling (FHIR),
transaction_time and bitemporal temporal patterns, and knowledge-graph products

**Files:**

- `domain.md` — Full healthcare domain with metadata, overview diagram, and summary tables
- `entities/` — One file per clinical entity with full YAML, diagrams, and constraints
- `events/` — Clinical workflow events with payload attributes
- `products/` — Canonical and analytics product declarations
- `sources/` — EHR and LIS source declarations with transformation mappings

---

## Teaching Protocol

Follow this sequence when walking through an example. Adapt depth and pace to the
user's archetype and signals.

### Step 1 — Big Picture First

Open the domain file and present the overview:

> "This is the [Simple Customer / Financial Crime] domain. Let me show you the
> big picture before we dive into details."

Highlight:

- **Domain description** — What business area does this model represent?
- **Metadata block** — Who owns it, what governance applies, what regulations scope it
- **Overview diagram** — How the entities connect visually
- **Summary tables** — The four (or five) tables: Entities, Enums, Relationships, Events (and Data Products if present)

Explain that the domain file is a table of contents — summary-level. Detail lives
in linked files.

### Step 2 — Pick One Entity to Explore

Let the user choose, or suggest one based on their archetype:

- **For modellers:** Start with an entity that uses inheritance (e.g., `Party` →
  `Person` / `Company` in Financial Crime, or `Party Role` → `Customer` in Simple Customer)
- **For data stewards:** Start with an entity that has governance metadata
  (e.g., `Customer` with PII attributes)
- **For engineers:** Start with an entity that has complex attributes or
  constraints (e.g., `Transaction` in Financial Crime)
- **For compliance users:** Start with an entity that has regulatory scope
  (e.g., `Party` with AML/KYC references)

Walk through the entity detail file:

1. **Heading structure** — H1 links to domain, H2 is entity name, H3 is `### Attributes`
2. **YAML block** — Each attribute with name, type, required, identifier, description
3. **Metadata fields** — existence, mutability, governance annotations
4. **Diagram** — classDiagram showing the entity and its relationships

Explain each element's purpose and connect to the user's frame of reference.

### Step 3 — Highlight a Decision Point

Every model contains design decisions. Surfacing one teaches the user *how to
think* in MD-DDL, not just how to read it:

**Simple Customer decisions:**

- **Why is Party Role abstract?** — It exists only as a base for specialisation.
  Customer inherits from it. This avoids duplicating common attributes.
- **Why is Loyalty Tier an enum, not an entity?** — It has no attributes, no
  relationships, no lifecycle of its own. It is just a set of labels.
- **Why does Customer Preference have `existence: dependent`?** — A preference
  cannot exist without a customer. It is owned, not independent.

**Financial Crime decisions:**

- **Why is Party abstract with Person and Company as concrete subtypes?** —
  A party can be either a person or a company, but never just "a party". The
  subtypes add meaningfully different attributes (Date of Birth vs Registration Number).
- **Why is Transaction not dependent on Account?** — A transaction connects
  a payer, payee, and payment initiator. It has its own lifecycle and identifiers.
- **Why are there separate Payer, Payee, and Payment Initiator entities?** —
  They are specialisations of Party Role with distinct attributes and rules.

After presenting the decision, ask:

> "In your domain, do you have a similar situation? Something that could be
> modelled as either [option A] or [option B]?"

### Step 4 — Connect to the Lifecycle

Show how the example entity connects to other stages of the MD-DDL workflow:

- **Relationships** — How does this entity relate to others? Show the relationship
  YAML and explain cardinality and identifying vs non-identifying.
- **Events** — What happens to this entity over time? Show an event definition
  and explain the temporal tracking connection.
- **Data Products** (Financial Crime only) — How does this entity appear in data
  product declarations? Show how the product's `entities` list scopes generation.
- **Sources** (Financial Crime only) — Where does this entity's data come from?
  Show a source mapping and transformation rule.

> "So the model is not just entities in isolation — it captures how they connect,
> what happens to them, where their data comes from, and how they are published.
> This is the full lifecycle that MD-DDL supports."

### Step 5 — Build Your Own (Bridge to Agent Ontology)

After the walkthrough, invite the user to describe a concept from their own domain:

> "Now that you have seen how [example entity] is structured, think about a
> concept from your own domain. Describe it in a couple of sentences and I will
> sketch how it might look in MD-DDL."

Sketch it as a **demonstration** — mark it clearly as an illustration:

> "Here is how that might look — this is a sketch, not a production artifact.
> When you are ready to build the real thing, Agent Ontology will walk you through
> the full modelling process."

If the user is ready:

> "Would you like me to hand you off to Agent Ontology? I can formulate an opening
> prompt based on what you have described."

---

## Guided Exploration Patterns

If the user does not want a linear walkthrough, support exploration:

- **"Show me how inheritance works"** → Jump to Party → Person / Company in
  Financial Crime. Show the Specializes column in the entities table, then the
  entity detail files. Explain abstract vs concrete.
- **"Show me governance metadata"** → Jump to domain metadata block. Show
  classification, PII, retention, regulatory scope. Then show entity-level
  governance in an entity detail file.
- **"Show me a data product"** → Jump to `products/` in Financial Crime. Show
  the canonical product and the analytics product. Explain product class, entities
  list, schema type, masking.
- **"Show me source mapping"** → Jump to `sources/` in Financial Crime. Show
  a source declaration and a transformation file. Explain change models and
  mapping types.
- **"Show me an event"** → Jump to any event in `events/`. Show the YAML
  structure. Explain actor, entity, and temporal tracking.

Always connect back to the user's archetype and domain when exploring.
