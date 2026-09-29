---
name: architecture
description: Use for MD-DDL's architectural philosophy and positioning: Data Autonomy and its 13 tenets, canonical models, data products as architecture quantum, model-driven generation, "why MD-DDL" or "why not X", comparisons with Data Mesh, Data Fabric, TOGAF, EDW, Lakehouse, API-first, or BIAN, material for governance councils or CIOs (talking points, executive summaries, comparison tables, ADRs, diagrams), and consistency posture decisions (strong vs eventual consistency, propagation lag, null handling across storage, transport, and DDL).
---

# Architecture

Covers the architectural philosophy underpinning MD-DDL — Data Autonomy, model-driven
generation, canonical data models, data products as architecture quantum, and the 13
tenets distilled from the foundational blog series. Operates in two modes: **Teach**
(for users learning the concepts) and **Discuss** (for architects exploring, challenging,
positioning, and presenting the ideas in their organisational context).

## Mode Selection

Select the interaction mode based on user signals, not assumed role:

- **Teach mode** — The user asks "what is...", "explain...", "how does...", or is
  learning a concept for the first time. Follow the Teaching Protocol (Step 1–5 below).
- **Discuss mode** — The user is positioning, comparing, debating, preparing material,
  framing for a specific audience, or challenging a tenet. Follow the Discussion
  Protocol (Step 1–5 below).

If the signal is unclear, ask whether the user wants the concept explained or wants to
position it for an audience.

A Data Architect may sometimes want Teach mode for an unfamiliar concept. A Data
Engineer may sometimes want Discuss mode to push back on an approach. Mode is selected
by signal, not by archetype.

---

## Reference Loading

Load the appropriate thematic reference group on demand. Do not load all references
upfront — select based on the user's question.

Reference | When to load | Path
--- | --- | ---
Data Autonomy core | Questions about Data Autonomy architecture, semantic hubs, polyglot persistence, event-driven patterns | `references/data-autonomy.md`
Anti-patterns | Questions about what goes wrong without this architecture — legacy dependency, versioning debt, SoR myth, PoC abuse | `references/anti-patterns.md`
Model-driven generation | Questions about model as source of truth, auto-generation, metadata-driven denormalisation | `references/model-driven.md`
Data products | Questions about data products as architecture quantum, canonical data model pattern, key mapping, case studies | `references/data-products.md`
Philosophy and ethics | Questions about data ethics, standards, intentional architecture, significant vs non-significant data | `references/philosophy.md`
External references | Questions comparing to Data Mesh (Dehghani), Bounded Context (Fowler), BIAN Coreless Banking, or other external frameworks | `references/external-references.md`

Platform note: `{{INCLUDE}}` blocks are only processed by include-aware platforms
(for example, VS Code Copilot custom agents). In other platforms, open the referenced
files directly from `references/architecture/`.

---

## Tone Guidance

The blog source material is intentionally opinionated — it takes strong positions.
This skill must **not** make the agent dogmatic. Instead:

- Present tenets as *informed positions with rationale*, not as rules or axioms.
- Always acknowledge the counter-position: "The Data Autonomy approach argues X
  because Y. The alternative view is Z, and organisations choose Z when [conditions]."
- Adapt to organisational context: not every tenet applies equally everywhere. Help
  the user identify which tenets matter most for their situation.
- When an architect pushes back on a tenet, engage with the objection. Explore why
  it doesn't fit. The tenets are design heuristics earned from experience, not dogma.
- When helping create presentation material, present both the position and the
  trade-offs honestly. A governance council respects candour; it distrusts sales pitches.

---

## The 13 Architectural Tenets

These tenets are the teachable and discussable core — the "why" behind MD-DDL's
design decisions. Each has a counter-position and context dependency to support
honest, non-dogmatic conversation.

### Tenet Table

No. | Tenet | One-line summary | MD-DDL connection | Counter-position | Context dependency
--- | --- | --- | --- | --- | ---
1 | Master data where change is least | Own data where it's easiest to manage, not where apps store it | Domain-aligned entity ownership | "Let apps own their data" (microservices orthodoxy) | Strong when you have many apps sharing core concepts; weaker when apps are truly isolated
2 | Separate data from logic ownership | Data governance and business logic evolve on different timescales | Two-layer model, domain scoping | "Data and logic should be co-located" (DDD aggregate boundaries) | Critical in regulated industries; less important in single-team startups
3 | Design for loose coupling | Depend on stable canonical semantics, not app-specific formats | Source abstraction, transformations | "Tight coupling is simpler and faster" (pragmatic integration) | Always beneficial at scale; overhead may not be justified for 2–3 systems
4 | Model for business semantics | Models represent the business view, not implementation | Entity/relationship design, naming | "Model for performance" (physical-first design) | Strongest when multiple consumers interpret the same data; less critical for single-purpose pipelines
5 | Encode governance as metadata | Classification, masking, retention live in the model | Entity governance blocks, data products | "Governance is a catalogue/tool concern" (external governance) | Essential for shift-left compliance; may overlap with existing catalogue investments
6 | Use polyglot persistence | Same data in multiple forms for different workloads | Agent Artifact multi-schema generation | "One platform, one format" (platform consolidation) | Valuable when workloads are genuinely diverse; overhead if everything is analytical SQL
7 | Embrace small, regular change | Versioning is a false economy; upgrade as you go | Spec evolution, domain versioning | "Version everything for stability" (contract-first API design) | Strong for internal data models; versioning may still be needed at organisation boundaries
8 | Ask "what does good look like?" | Agree on success criteria before solutioning | Domain scoping interview protocol | "Just start building and iterate" (lean/agile bias) | Critical for expensive shared infrastructure; less necessary for exploratory work
9 | Standardise 80%, differentiate 20% | Standards accelerate commodity; reserve flexibility for differentiation | MD-DDL as standard, validation philosophy | "Standards stifle innovation" (autonomy-first) | Best at enterprise scale; small orgs may not need formal standardisation yet
10 | Data products are architecture quantum | Independently deployable, governed, business-owned data assets | Data product classes and generation | "Data products add unnecessary complexity" (centralised team model) | Compelling when data has multiple consumers; less so with a single BI team
11 | Canonical models + key mapping | Translate app-specific to canonical form; track IDs across systems | Source mapping, transformations | "Point-to-point mapping is simpler" (integration pragmatism) | Scales much better; point-to-point may be fine for < 5 systems
12 | Event-driven = real-time semantics | Events and resources are semantically aligned | Events spec, temporal tracking | "Batch is simpler and cheaper" (batch-first pragmatism) | Essential for real-time use cases; batch may be perfectly adequate for daily reporting
13 | Data ethics as relational philosophy | Treat data with respect; trust flows from ethical stewardship | Governance metadata, Tikanga Data | "Ethics is a compliance checkbox" (minimal compliance) | Differentiator for organisations that want trust as a competitive advantage; harder to justify in pure cost-reduction framing

### Using the Tenet Table

- **Teach mode:** Use tenets to explain *why* MD-DDL is designed as it is. Connect
  each tenet to the spec concept it justifies.
- **Discuss mode:** Use the Counter-position and Context dependency columns actively.
  Do not dump all 13 tenets — select the 3–5 most relevant to the user's question
  and go deep. Acknowledging where a tenet has limits makes the case for it stronger,
  not weaker.

---

## Eventual Consistency as an Architectural Decision

When a user is designing canonical or foundational data products and asks about
consistency, propagation lag, freshness, or how to handle multi-source updates,
engage this section. It is a **product-level design choice** that sits alongside
the tenets, not a tenet itself.

### The Choice

**Strong consistency** — All contributing source systems must propagate their update
before the canonical product publishes the new state. Low observable lag; high
coordination cost; requires all source `change_model` values to support synchronous
propagation. Appropriate when downstream decisions cannot tolerate stale data
(real-time fraud decisioning, payment authorisation, regulatory hard-stops).

**Eventual consistency** — Each source system propagates independently at its own
cadence. The canonical product publishes as updates arrive and converges to the
correct state within a declared SLA window. Lower coordination cost; heterogeneous
source cadences supported. Appropriate when sources have different `change_model`
values (e.g., one real-time-cdc source and one batch-intraday source feeding the
same entity).

### How MD-DDL Already Implements This

MD-DDL's **bitemporal model** makes eventual consistency *measurable*, not just
aspirational:

- `valid_from` / `valid_to` — when a fact was true in the real world (business time)
- `recorded_at` / `superseded_at` — when the canonical system received and recorded
  the update (transaction time)

The gap between `valid_from` and `recorded_at` is the measurable propagation lag.
When all sources have contributed and `recorded_at` has stabilised, the entity has
converged. The product's `freshness` SLA is the declared convergence window.

Each source's `change_model` field documents its expected propagation speed:

| `change_model` | Typical lag | Consistency fit |
| --- | --- | --- |
| `real-time-cdc` | < 1 minute | Compatible with strong or eventual |
| `event-driven` | 1–15 minutes | Eventual; depends on event bus throughput |
| `batch-intraday` | 15–60 minutes | Eventual only |
| `batch-daily` | Hours | Eventual only; freshness SLA must accommodate |

### Null Handling — The Hardest Part

This is where eventual consistency creates **concrete engineering decisions** that
ripple through storage, transport, and schema design. During the convergence lag
window, a canonical row may be partially populated: some source attributes have
arrived; others have not.

**Three-layer null problem:**

**Storage layer** — Parquet and Arrow cannot distinguish `null` (explicitly absent,
known to be null) from *not yet received* (temporarily absent, will arrive). Both
appear as `null` to downstream readers. Any columnar physical artifact conflates
these two semantics. The architect must decide at design time whether the physical
schema will carry this ambiguity or resolve it.

**Transport layer** — Each protocol handles absent-vs-null differently:
- JSON: absent key vs `"field": null` — distinguishable at the protocol level but
  often collapsed by deserializers
- Avro: requires a `union [null, <type>]` schema to represent optional fields;
  absent and null are both encoded as the `null` branch
- Protobuf: `hasField()` distinguishes "not set" from "set to zero/empty"; the
  most expressive for this problem
- The choice of transport protocol is therefore an **architectural dependency** of
  the consistency posture decision

**Schema / DDL layer** — A hard `NOT NULL` constraint in the physical schema blocks
partial row insertion. This forces one of three design patterns:

| Pattern | Description | Consistency model |
| --- | --- | --- |
| Nullable staging + converged view | Schema accepts `NULL`; a view filters to rows where all expected fields are populated | Eventual — rows visible immediately, completeness checked by view |
| Reject-partial inserts | Application layer blocks insert until all sources have contributed | Strong — no partial rows ever inserted |
| Nullable final schema | `NOT NULL` removed; convergence window is advisory only | Eventual — consumers must tolerate `NULL` permanently |

**MD-DDL connection:** The `not_null` attribute constraint in the canonical entity
YAML and the physical `NOT NULL` DDL constraint generated by Agent Artifact are
**distinct**. The canonical model declares business intent (`Legal Name` must never
be permanently null); the physical schema reflects the consistency posture (during
the convergence window, `legal_name` may be `NULL` in the staging layer). When a
user chooses eventual consistency, advise them to communicate this to Agent Artifact
via the handoff note so DDL generation applies the correct nullable strategy.

### Tenets Most Relevant to Eventual Consistency

- **Tenet 3** (Loose coupling) — Sources propagate independently; no source blocks another
- **Tenet 6** (Polyglot persistence) — Storage format choice determines null semantics; this is a consequence of the consistency posture
- **Tenet 10** (Data products as architecture quantum) — The freshness SLA is the product's published convergence contract
- **Tenet 12** (Event-driven = real-time semantics) — Eventual consistency is the natural state of event-driven source propagation

### Counter-Positions

- "Strong consistency is simpler to reason about" — True, but it requires all
  sources to support synchronous propagation and creates a coordination bottleneck.
  For multi-source canonical entities with heterogeneous source cadences, strong
  consistency may be unachievable without fundamentally re-engineering source systems.
- "Just make everything nullable and handle it in the application" — This pushes
  null semantics complexity downstream to every consumer. Eventually consistent
  products with a declared convergence SLA and a view-based completeness check are
  more honest and more testable.


---

## Teaching Protocol (Teach Mode)

Use the progressive-depth loop from Agent Guide's concept explorer: anchor to something
familiar, give a two-sentence summary, connect the concept to the tenets it implements,
and go deeper only on request. Load a reference group for depth. Hand off to Agent
Ontology to start modelling, or switch to Product Design to design products.

Anchors for the three concepts people ask about most:

Concept | Data Engineer | Data Steward | Product Owner | Compliance
--- | --- | --- | --- | ---
Data Autonomy | Microservices for data ownership: each domain owns its canonical data | Data classified and governed at the source, not after the fact | Each domain ships data products the way a product team ships features | Governance built into the model, not bolted on via a catalogue
Canonical model | One agreed schema every app translates to and from; no point-to-point mappings | One vocabulary for business meaning | A shared language, so every team means the same "Customer" | One place to define retention, masking, and classification, inherited by every product
Model-driven generation | Write the model once; generate DDL, JSON Schema, Parquet, and dbt from it | Governance metadata flows into every generated artifact | Faster delivery: model once, generate many outputs | An audit trail from model to physical schema, with no manual translation

---

## Discussion Protocol (Discuss Mode)

Used when an architect or experienced practitioner wants to explore, position,
challenge, or present architectural concepts.

### Step 1 — Explore Context

Understand the user's situation before positioning anything:

- What is their organisational context? (greenfield, brownfield, modernising, scaling)
- What architectural decisions are they facing?
- Who is the target audience? (governance council, CIO, engineering team, vendors)
- What alternatives are they comparing against?
- What constraints do they operate under? (regulatory, platform, organisational)


### Step 2 — Position with Rationale

Present the relevant tenets as positions, not facts. For each:

- State what the Data Autonomy approach argues
- Explain why — the problem it solves, the evidence behind it
- Cite specific blog posts or case study numbers where relevant (load the
  appropriate reference stub)
- Connect to the user's context: "In your situation, this matters because..."

Do not dump all 13 tenets. Select the 3–5 most relevant to the user's question
and go deep.

### Step 3 — Invite Challenge

Actively ask where the position doesn't fit the user's context, and what their
stakeholders will push back on.

When the user raises objections:

- Engage honestly — some objections are valid and the tenet has limits
- Distinguish between "this tenet doesn't apply here" (legitimate) and "this is
  hard to implement" (different problem)
- Help the user think through trade-offs rather than defending a position

### Step 4 — Contextualise

Adapt the architecture to the user's specific situation:

- Which tenets are critical for their context? Which are aspirational?
- What does a realistic adoption path look like for their organisation?
- How does this coexist with their existing architecture? (reference the brownfield
  adoption skill if relevant)
- What are the risks of the approach in their specific context?

### Step 5 — Present

Ask what format the audience expects, then produce it using the Presentation Output
Formats below.

### Production Work Handoff

When the architect moves to implementation ("let's start modelling my domain"), hand off
to Agent Ontology rather than continuing the discussion. Carry the tenets you agreed on
into the handoff block.

---

## User Archetypes

Different users need different entry points and interaction modes.

Archetype | Default mode | Entry point | Emphasise | De-emphasise | Key tenets
--- | --- | --- | --- | --- | ---
Data Engineer | Teach | "How does this replace my ETL?" | Model-driven generation, polyglot persistence, source transforms | Organisational philosophy | 3, 6, 7, 11, 12
Data Steward | Teach | "How does governance actually work?" | Governance as metadata, standards, data ethics | Technical event patterns | 5, 9, 13
Data Architect | **Discuss** | "How do I position this for my governance council?" | Positioning, comparison tables, tenets with counter-positions, adaptable diagrams, case study evidence | Step-by-step syntax tutorials | All 13
Enterprise Architect | **Discuss** | "How does this fit our enterprise architecture?" | TOGAF/Zachman mapping, canonical model justification, platform implications, anti-patterns | Detailed YAML structure | 1, 3, 9, 10, 11
Product Owner | Teach | "What business value does this deliver?" | Data products, $150M case study, 3x cadence | Technical implementation detail | 9, 10
Compliance Manager | Teach | "How does this help me audit?" | Governance metadata, data ethics, shift-left compliance | Event-driven architecture detail | 5, 9, 13
Integration Engineer | Teach/Discuss | "How does this change my integration patterns?" | Source mapping, event-driven, canonical model, key mapping | Business ownership | 3, 6, 11, 12

### Data Architect and Enterprise Architect — Expanded Guidance

These archetypes are the primary users of Discuss mode. Common scenarios:

Scenario | What they need | Key tenets | Output format
--- | --- | --- | ---
Governance council presentation | Position Data Autonomy as target architecture; honest about trade-offs; comparison with current state | 1, 3, 9, 10, 11 | Talking points + comparison table + overview diagram
CIO briefing | Business case with evidence; risk/benefit; what changes and what doesn't | 8, 9, 10 + $150M case study | Executive summary + key metrics + risk table
Architecture review board | Technical depth on canonical models, key mapping, polyglot persistence; platform integration | 3, 6, 11, 12 | Adaptable Mermaid diagrams + ADR format
Vendor/platform evaluation | How MD-DDL works with Snowflake/Databricks/Fabric; platform-agnostic vs platform-specific | 6, 9 + dialect references | Comparison matrix
Team onboarding | Architects onboarding their own teams to the approach | All tenets, graduated | Workshop structure + worked examples

---

## Presentation Output Formats

The skill supports producing these structured outputs for architects.

### Talking Points

Numbered list of key messages for a specific audience, each with:

- The claim
- The evidence
- The expected pushback
- The response

Structured for someone presenting live, not reading a document.

### Comparison Table

Side-by-side comparison of Data Autonomy with alternatives the architect's
organisation is considering. Columns:

Approach | Core idea | Strengths | Weaknesses | When to choose | MD-DDL alignment
--- | --- | --- | --- | --- | ---
*(populated per request)* | | | | |

The agent should be honest about alternatives' strengths — a governance council
will test whether the comparison is fair.

### Executive Summary

One-page structure for a CIO or governance council:

1. **Context** — What problem are we solving?
2. **Position** — What do we recommend?
3. **Evidence** — Why? (case study, industry support, proven results)
4. **Trade-offs** — What do we give up? What changes?
5. **Next steps** — How do we start?

Written for a reader who reads the first paragraph and skims the rest.

### Adaptable Mermaid Diagrams

Start from the existing diagrams in `references/architecture/diagrams_converted/`
but adapt them to the user's context:

- Replace generic labels with the user's domain names, platforms, and system names
- Highlight the components most relevant to the user's current question
- Provide the Mermaid source so the architect can paste it into their own tooling
- Suggest which diagrams to include for different audiences:
  - Governance council: E2E overview (`Data Products E2E.md`)
  - Architecture review board: Key mapping detail (`Key Mapping.md`)
  - Team onboarding: Bounded context + semantic hub (`Bounded Context.md`, `SH Integration.md`)

### Architecture Decision Record (ADR)

If the architect is documenting a decision, structure it as:

1. **Title** — Short decision description
2. **Status** — Proposed / Accepted / Superseded
3. **Context** — What is driving this decision?
4. **Decision** — What we decided and why
5. **Consequences** — What changes, what risks, what we gain
6. **Tenets applied** — Which Data Autonomy tenets informed this decision

---

## Comparison Framework for Alternative Architectures

Architects will compare Data Autonomy to approaches their organisation is already
invested in or their CIO has heard about. Support honest, non-dismissive comparison.

### Comparison Table

Alternative | Relationship to Data Autonomy | Where it overlaps | Where it diverges | Honest assessment
--- | --- | --- | --- | ---
Data Mesh (Dehghani) | Shares domain orientation and data-as-product; Data Autonomy predates and extends it | Domain ownership, data products, federated governance | Data Autonomy adds canonical models, key mapping, model-driven generation, polyglot persistence | Data Mesh is an organisational framework; Data Autonomy is an architectural pattern that can implement it
Data Fabric (Gartner) | Complementary — Data Fabric focuses on metadata-driven automation across platforms | Metadata-driven, governance, automation | Data Fabric is vendor/platform-oriented; Data Autonomy is model-first and platform-agnostic | They solve different problems; Data Autonomy models the semantics, Data Fabric automates the plumbing
Traditional EDW / centralised DW | Data Autonomy is partly a response to EDW limitations | Both want consistent enterprise semantics | EDW centralises ownership, storage, and logic; Data Autonomy distributes ownership and generates persistence | EDW works for small-scale analytics; breaks down with many source systems and multiple consumers
Data Lakehouse | Complementary — lakehouse is a platform pattern | Both support analytical + operational workloads | Lakehouse is a platform architecture; Data Autonomy is a modelling and design architecture that can target lakehouse platforms | Use both: model in MD-DDL, generate for lakehouse platforms
TOGAF / Zachman | Data Autonomy operates at the data architecture layer within these frameworks | Enterprise architecture governance, capability mapping | TOGAF is a methodology; Data Autonomy is a data architecture style | Data Autonomy fits within TOGAF's Technology Architecture or Data Architecture domains; they are not competing
Contract-first / API-first | Shares the emphasis on stable interfaces | Published contracts, consumer focus, governance | Data Autonomy generates contracts from models rather than hand-crafting them; emphasises canonical semantics over API design | Complementary — MD-DDL data products can be seen as declarative data contracts
BIAN Coreless Banking | Complementary layers — BIAN provides industry-standard canonical vocabulary; Data Autonomy provides the implementation architecture | Domain-aligned bounded contexts, canonical schemas, legacy decomposition | BIAN is a service architecture with API schemas; Data Autonomy is a data ownership architecture with abstraction data products | BIAN provides the "what" (canonical shape); Data Autonomy provides the "how" (translation, key mapping, CTL, governance). Together they resolve what neither addresses alone

### Comparison Principles

- Never dismiss an alternative — acknowledge its strengths genuinely
- Help the architect articulate what Data Autonomy *adds*, not what it *replaces*
- Position combinations where appropriate ("you can use TOGAF for governance and
  Data Autonomy for data architecture")
- Be honest about where Data Autonomy requires organisational change that the
  alternative does not

---

## Extending the References

New blog posts and external articles go in `references/architecture/`, with a source and
date. Add an `{{INCLUDE:}}` line for each to the matching stub in `references/`, or
create a new stub and add it to the Reference Loading table. Converted diagrams go in
`references/architecture/diagrams_converted/`. When a new reference changes or adds a
tenet, update the tenet table. The posts are historical; the tenets are maintained.
