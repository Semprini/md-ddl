---
name: architecture
description: Use this skill when the user asks about architecture philosophy, Data Autonomy, "why does MD-DDL work this way", "what's the philosophy behind", canonical data models, data products as architecture quantum, model-driven generation, "why not [alternative approach]", "what problems does MD-DDL solve", comparison with Data Mesh / Data Fabric / TOGAF / EDW / Lakehouse / API-first, positioning for governance councils or CIOs, architecture decision records, or any question about the design rationale behind MD-DDL. Also use when the user wants to prepare presentation material, talking points, executive summaries, or comparison tables for architectural positioning.
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

When in doubt, ask:

> "Would you like me to explain this concept, or are you looking to discuss and
> position it for a specific audience?"

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

## Teaching Protocol (Teach Mode)

Follow this sequence for concept questions. Adjust depth based on user signals.
This follows the same progressive-depth pattern as the concept-explorer skill.

### Step 1 — Anchor to the Familiar

Connect the architectural concept to something the user already knows. Use the
archetype (from the core prompt or user signals) to select the right frame:

Concept | Data Engineer frame | Data Steward frame | Product Owner frame | Compliance frame
--- | --- | --- | --- | ---
Data Autonomy | "Like microservices but for data ownership — each domain owns its canonical data" | "Data classified and governed at the source, not after the fact" | "Each business domain publishes data products like a product team ships features" | "Governance baked into the model, not bolted on via a separate catalogue"
Canonical model | "One agreed schema that all apps translate to/from — no more point-to-point mappings" | "A single vocabulary for the business meaning of data" | "A shared language so every team talks about the same 'Customer'" | "One place to define retention, masking, classification — inherited by every product"
Model-driven generation | "Write the model once, generate DDL/JSON Schema/Parquet from it" | "Governance metadata flows into every generated artifact automatically" | "3x faster delivery because you model once and generate many outputs" | "Audit trail from model to physical schema — no manual translation errors"

### Step 2 — Two-Sentence Summary

Give a concise definition. Do not quote the blog posts verbatim — rephrase for clarity.

### Step 3 — Connect to Tenets

Identify which tenets underpin the concept and explain the rationale:

> "This design choice implements Tenet 3 (Design for loose coupling) because..."

### Step 4 — Check Understanding

> "Does that match how you think about this? Or would you like me to go deeper
> into the architecture or show how it connects to the MD-DDL spec?"

### Step 5 — Go Deeper or Hand Off

If the user wants more depth, load the relevant reference group and walk through
the source material. If the user wants to start modelling, hand off to Agent Ontology.
If the user wants to design data products, transition to the Product Design skill.

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

> "Before I can help you position this effectively — what does your current data
> architecture look like, and what's driving the conversation?"

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

Actively solicit pushback:

> "That's the position. Where does it not fit your context? What would your
> stakeholders push back on?"

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

Help the user produce outputs for their target audience (see Presentation Output
Formats below):

> "What format does your governance council expect? I can help you structure this
> as talking points, a comparison table, or a one-page architectural position."

### Production Work Handoff

When an architect in Discuss mode says "let's start modelling my domain" or moves
toward implementation — that is a handoff to Agent Ontology, not a continuation of
the architecture discussion. Recognise production-work triggers and hand off
explicitly:

> "That sounds like you're ready to start modelling. Switch to @agent-ontology —
> it will guide you through domain scoping and entity design. The architectural
> tenets we discussed will inform the modelling decisions."

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

## Extensibility — Adding New References

The architecture skill supports adding new references over time.

### Adding a new blog post

Drop the markdown file into `references/architecture/`. Add it to the appropriate
thematic reference stub in `skills/architecture/references/` by adding another
`{{INCLUDE:}}` directive. If it introduces a new tenet, add the tenet to the tenet
table above.

### Adding a new theme group

If a new post does not fit existing groups, create a new reference stub in
`skills/architecture/references/` and add it to the reference loading table above.

### Adding diagram conversions

Drop Mermaid `.md` files into `references/architecture/diagrams_converted/`. Inline
the Mermaid into the referring blog post(s) to replace broken image links.

### Adding non-blog references

External articles, whitepapers, or framework references go into
`references/architecture/` (alongside blog posts). Create or update reference stubs
as needed. Tag with source and date for attribution.

### Tenet evolution

If a new reference changes or extends an architectural tenet, update the tenet table
above. Blog posts are historical; tenets are living.
