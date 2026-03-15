# Plan: Architecture Skill for Agent Architect

## TL;DR

Add an "architecture" skill to Agent Architect that enables architectural discussion about the philosophy underpinning MD-DDL — Data Autonomy, model-driven generation, canonical data models, data products as architecture quantum, and the 13 tenets distilled from the blog series. The skill operates in two modes: **Teach** (for users learning the concepts) and **Discuss** (for architects who want to explore, challenge, position, and present the ideas in their organisational context). Architects preparing material for governance councils or CIOs get presentation-ready outputs — talking points, comparison tables, adaptable Mermaid diagrams, and executive summaries. The blog source material is intentionally opinionated; the skill should make the agent an informed discussion partner, not dogmatic. Also embed the architectural philosophy into copilot-instructions, CLAUDE.md, and the review process so the thinking is discoverable and reviewable.

---

## Context: The Blog Series

17 blog posts (2018–2024) articulate an architectural philosophy that directly informs every design decision in MD-DDL. The posts evolve through four phases:

Phase | Period | Key ideas
--- | --- | ---
Problem definition | 2018–2019 | Vestigial technology, dependency as anti-pattern, Data Autonomy concept
Core architecture | 2020 | Data Mesh, semantic hubs, event-driven + RESTful, polyglot persistence, case study proof
Anti-patterns and principles | 2021 | Stop versioning, model-driven generation, systems of record critique, Tikanga Data ethics, data convergence
Standards and operationalisation | 2022–2024 | Standards as superpower, enterprise anarchy, data products ($150M savings), canonical data model + key mapping

The posts are in `references/architecture/` as markdown files (17 files, ~50K words total). PNG diagrams are missing — 20 diagram references in the posts point to external URLs.

---

## Phase 1: Create the Skill

### Step 1: Create skill folder and SKILL.md

Create `agents/agent-architect/skills/architecture/SKILL.md` with:
- Frontmatter trigger: questions about "architecture", "data autonomy", "why does MD-DDL work this way", "what's the philosophy behind", "canonical data model", "data products architecture", "model-driven generation", "why not [alternative approach]", "what problems does MD-DDL solve", "compare to Data Mesh/Data Fabric/TOGAF", "position for governance council", "CIO presentation", "architecture decision record"
- Two interaction modes: **Teach** (for concept learners — follows concept-explorer Step 1–5 pattern) and **Discuss** (for architects — follows the Discussion Protocol in Step 1b)
- Mode selection: If the user is asking "what is..." or "explain...", use Teach mode. If the user is positioning, comparing, debating, preparing material, or framing for a specific audience, use Discuss mode. When in doubt, ask.
- 13 architectural tenets as the discussion core — each with rationale, counter-position, and context dependency (see tenet table below)
- Reference loading table pointing to blog posts in `references/`
- Archetype-specific entry points (see Step 4) including governance council / CIO scenarios
- Presentation output formats for architects (see Step 4b)
- Comparison framework for alternative architectures (see Step 4c)

#### Tone guidance

The blog source material is intentionally opinionated — it takes strong positions. The skill must **not** make the agent dogmatic. Instead:

- Present tenets as *informed positions with rationale*, not as rules or axioms
- Always acknowledge the counter-position: "The Data Autonomy approach argues X because Y. The alternative view is Z, and organisations choose Z when [conditions]."
- Adapt to organisational context: not every tenet applies equally everywhere. Help the user identify which tenets matter most for their situation.
- When an architect pushes back on a tenet, engage with the objection. Explore why it doesn't fit. The tenets are design heuristics earned from experience, not dogma.
- When helping create presentation material, present both the position and the trade-offs honestly. A governance council respects candour; it distrusts sales pitches.

### Step 1b: Define the Discussion Protocol

The Discussion Protocol governs Discuss mode — used when an architect (or experienced practitioner) wants to explore, position, challenge, or present architectural concepts. This is distinct from the concept-explorer Teaching Protocol.

#### Discussion Step 1 — Explore Context

Understand the user's situation before positioning anything:

- What is their organisational context? (greenfield, brownfield, modernising, scaling)
- What architectural decisions are they facing?
- Who is the target audience? (governance council, CIO, engineering team, vendors)
- What alternatives are they comparing against?
- What constraints do they operate under? (regulatory, platform, organisational)

> "Before I can help you position this effectively — what does your current data architecture look like, and what's driving the conversation with your governance council?"

#### Discussion Step 2 — Position with Rationale

Present the relevant tenets as positions, not facts. For each:

- State what the Data Autonomy approach argues
- Explain why — the problem it solves, the evidence behind it
- Cite specific blog posts or case study numbers where relevant (load the appropriate reference stub)
- Connect to the user's context: "In your situation, this matters because..."

Do not dump all 13 tenets. Select the 3–5 most relevant to the user's question and go deep.

#### Discussion Step 3 — Invite Challenge

Actively solicit pushback:

> "That's the position. Where does it not fit your context? What would your stakeholders push back on?"

When the user raises objections:
- Engage honestly — some objections are valid and the tenet has limits
- Distinguish between "this tenet doesn't apply here" (legitimate) and "this is hard to implement" (different problem)
- Help the user think through trade-offs rather than defending a position

#### Discussion Step 4 — Contextualise

Adapt the architecture to the user's specific situation:

- Which tenets are critical for their context? Which are aspirational?
- What does a realistic adoption path look like for their organisation?
- How does this coexist with their existing architecture? (reference brownfield plan tenets if relevant)
- What are the risks of the approach in their specific context?

#### Discussion Step 5 — Present

Help the user produce outputs for their target audience (see Step 4b for format details):

- Talking points for a governance council
- Comparison table for a CIO
- Architecture overview diagram they can adapt
- Executive summary or ADR

> "What format does your governance council expect? I can help you structure this as talking points, a comparison table, or a one-page architectural position."

### Step 2: Create reference stubs

Create `agents/agent-architect/skills/architecture/references/` with reference stubs pointing to the blog posts. Group posts thematically rather than one stub per post to keep context loading manageable:

Reference | Posts included | Teaches
--- | --- | ---
`references/data-autonomy.md` | 2019 overview, 2020 holistic data mesh, 2020 resource-oriented, 2020 BI analytics | Core Data Autonomy architecture, semantic hubs, polyglot persistence, event-driven patterns
`references/anti-patterns.md` | 2018 vestigial technology, 2021 stop versioning, 2021 systems of record bollocks, 2021 PoC PoC PoC | What goes wrong without this architecture — legacy dependency, versioning debt, SoR myth, PoC abuse
`references/model-driven.md` | 2021 model-driven generation, 2021 automated op-to-analytics transform | Model as source of truth, auto-generation of schemas/infrastructure, metadata-driven denormalisation
`references/data-products.md` | 2024 data products $150M, 2024 architecting data autonomy, 2020 case study | Data products as architecture quantum, canonical data model pattern, key mapping, proven case studies
`references/philosophy.md` | 2021 Tikanga Data, 2022 standards, 2024 enterprise anarchy, 2021 data convergence, 2022 forgotten question mark | Ethics, standards as pit of success, intentional architecture, significant vs non-significant data

Each stub uses `{{INCLUDE:}}` with relative paths to the blog posts in `references/architecture/`.

### Step 2b: Fix broken image links in blog posts

The blog posts contain ~20 broken `![](https://s3...semprini.me/...)` image references. Mermaid replacements exist in `references/architecture/diagrams_converted/`. For each blog post with a broken image link where a converted diagram exists:

- Replace the `![alt](https://s3...semprini.me/...)` line with a Mermaid include or inline reference to the corresponding file in `diagrams_converted/`
- Use the pattern: remove the broken image link and add a note pointing to the converted diagram, e.g., `<!-- Diagram: see diagrams_converted/Bounded Context.md -->`
- Alternatively, inline the Mermaid block directly from the converted file into the blog post (preferred — keeps content self-contained when loaded via `{{INCLUDE:}}`)

Mapping of converted diagrams to blog posts:

Converted diagram | Blog post(s) that reference it
--- | ---
`Bounded Context.md` | `2019-02-17_data-autonomy-overview.md`, `2020-07-18_data-autonomy-holistic-data-mesh.md`
`SH Integration.md` | `2020-07-18_data-autonomy-holistic-data-mesh.md`
`Canonical Data Model Pattern.md` | `2024-08-07_architecting_data_autonomy.md`
`Data Products E2E.md` | `2024-08-07_architecting_data_autonomy.md`
`Key Mapping.md` | `2024-08-07_architecting_data_autonomy.md`
`OP2ANL.md` | `2021-04-05_automated-operational-analytics-transform.md`
`Flatten.md` | `2021-04-05_automated-operational-analytics-transform.md`

Remaining broken image references (title/hero graphics, metaphorical images) that have no converted diagram can be removed or replaced with a text description of what the image showed.

### Step 2c: Establish extensibility pattern for new references

The architecture skill must support adding new references over time (new blog posts, articles, third-party material, community contributions). Define in SKILL.md:

- **Adding a new blog post:** Drop the markdown file into `references/architecture/`. Add it to the appropriate thematic reference stub in `skills/architecture/references/` by adding another `{{INCLUDE:}}` directive. If it introduces a new tenet, add the tenet to the tenet table in SKILL.md.
- **Adding a new theme group:** If a new post doesn't fit existing groups, create a new reference stub in `skills/architecture/references/` and add it to the reference loading table in SKILL.md.
- **Adding diagram conversions:** Drop Mermaid `.md` files into `references/architecture/diagrams_converted/`. Inline the Mermaid into the referring blog post(s) to replace broken image links.
- **Adding non-blog references:** External articles, whitepapers, or framework references go into `references/architecture/external/` (new subfolder). Create reference stubs as needed. Tag with source and date for attribution.
- **Tenet evolution:** If a new reference changes or extends an architectural tenet, update the tenet table in SKILL.md. Blog posts are historical; tenets are living.

### Step 3: Define the 13 architectural tenets

The skill should present these tenets as the teachable core — the "why" behind MD-DDL's design decisions:

Tenet | One-line summary | MD-DDL connection | Counter-position | Context dependency
--- | --- | --- | --- | ---
1. Master data where change is least | Own data where it's easiest to manage, not where apps store it | Domain-aligned entity ownership | "Let apps own their data" (microservices orthodoxy) | Strong when you have many apps sharing core concepts; weaker when apps are truly isolated
2. Separate data from logic ownership | Data governance and business logic evolve on different timescales | Two-layer model, domain scoping | "Data and logic should be co-located" (DDD aggregate boundaries) | Critical in regulated industries; less important in single-team startups
3. Design for loose coupling | Depend on stable canonical semantics, not app-specific formats | Source abstraction, transformations | "Tight coupling is simpler and faster" (pragmatic integration) | Always beneficial at scale; overhead may not be justified for 2–3 systems
4. Model for business semantics | Models represent the business view, not implementation | Entity/relationship design, naming | "Model for performance" (physical-first design) | Strongest when multiple consumers interpret the same data; less critical for single-purpose pipelines
5. Encode governance as metadata | Classification, masking, retention live in the model | Entity governance blocks, data products | "Governance is a catalogue/tool concern" (external governance) | Essential for shift-left compliance; may overlap with existing catalogue investments
6. Use polyglot persistence | Same data in multiple forms for different workloads | Agent Artifact multi-schema generation | "One platform, one format" (platform consolidation) | Valuable when workloads are genuinely diverse; overhead if everything is analytical SQL
7. Embrace small, regular change | Versioning is a false economy; upgrade as you go | Spec evolution, domain versioning | "Version everything for stability" (contract-first API design) | Strong for internal data models; versioning may still be needed at organisation boundaries
8. Ask "what does good look like?" | Agree on success criteria before solutioning | Domain scoping interview protocol | "Just start building and iterate" (lean/agile bias) | Critical for expensive shared infrastructure; less necessary for exploratory work
9. Standardise 80%, differentiate 20% | Standards accelerate commodity; reserve flexibility for differentiation | MD-DDL as standard, validation philosophy | "Standards stifle innovation" (autonomy-first) | Best at enterprise scale; small orgs may not need formal standardisation yet
10. Data products are architecture quantum | Independently deployable, governed, business-owned data assets | Data product classes and generation | "Data products add unnecessary complexity" (centralised team model) | Compelling when data has multiple consumers; less so with a single BI team
11. Canonical models + key mapping | Translate app-specific → canonical form; track IDs across systems | Source mapping, transformations | "Point-to-point mapping is simpler" (integration pragmatism) | Scales much better; point-to-point may be fine for < 5 systems
12. Event-driven = real-time semantics | Events and resources are semantically aligned | Events spec, temporal tracking | "Batch is simpler and cheaper" (batch-first pragmatism) | Essential for real-time use cases; batch may be perfectly adequate for daily reporting
13. Data ethics as relational philosophy | Treat data with respect; trust flows from ethical stewardship | Governance metadata, Tikanga Data | "Ethics is a compliance checkbox" (minimal compliance) | Differentiator for organisations that want trust as a competitive advantage; harder to justify in pure cost-reduction framing

The agent should use the Counter-position and Context dependency columns actively when in Discuss mode — acknowledging where a tenet has limits makes the case for it stronger, not weaker.

### Step 4: Write archetype-specific approaches

Different users need different entry points and interaction modes:

Archetype | Default mode | Entry point | Emphasise | De-emphasise
--- | --- | --- | --- | ---
Data Engineer | Teach | "How does this replace my ETL?" | Model-driven generation, polyglot persistence, source transforms | Organisational philosophy
Data Steward | Teach | "How does governance actually work?" | Governance as metadata, standards, data ethics | Technical event patterns
Data Architect | **Discuss** | "How do I position this for my governance council?" | Positioning, comparison tables, tenets with counter-positions, adaptable diagrams, case study evidence | Step-by-step syntax tutorials
Enterprise Architect | **Discuss** | "How does this fit our enterprise architecture?" | TOGAF/Zachman mapping, canonical model justification, platform implications, anti-patterns | Detailed YAML structure
Product Owner | Teach | "What business value does this deliver?" | Data products, $150M case study, 3x cadence | Technical implementation detail
Compliance Manager | Teach | "How does this help me audit?" | Governance metadata, data ethics, shift-left compliance | Event-driven architecture detail
Integration Engineer | Teach/Discuss | "How does this change my integration patterns?" | Source mapping, event-driven, canonical model, key mapping | Business ownership

#### Data Architect and Enterprise Architect — expanded guidance

These archetypes are the primary users of Discuss mode. They are not learning MD-DDL — they are evaluating and positioning an architectural approach. Common scenarios:

Scenario | What they need | Key tenets | Output format
--- | --- | --- | ---
Governance council presentation | Position Data Autonomy as the target architecture; honest about trade-offs; comparison with current state | 1, 3, 9, 10, 11 | Talking points + comparison table + overview diagram
CIO briefing | Business case with evidence; risk/benefit; what changes and what doesn't | 8, 9, 10 + $150M case study | Executive summary + key metrics + risk table
Architecture review board | Technical depth on canonical models, key mapping, polyglot persistence; how this integrates with existing platforms | 3, 6, 11, 12 | Adaptable Mermaid diagrams + ADR format
Vendor/platform evaluation | How MD-DDL approach works with Snowflake/Databricks/Fabric; what's platform-agnostic vs platform-specific | 6, 9 + dialect references | Comparison matrix
Team onboarding | Architects onboarding their own teams to the approach | All tenets, graduated | Workshop structure + worked examples

### Step 4b: Define presentation output formats

The skill should support producing these structured outputs for architects:

**Talking Points** — Numbered list of key messages for a specific audience, each with: the claim, the evidence, the expected pushback, and the response. Structured for someone presenting live, not reading a document.

**Comparison Table** — Side-by-side comparison of Data Autonomy with alternatives the architect's organisation is considering. Columns: Approach | Core idea | Strengths | Weaknesses | When to choose | MD-DDL alignment. The agent should be honest about alternatives' strengths — a governance council will test whether the comparison is fair.

**Executive Summary** — One-page structure: Context (what problem), Position (what we recommend), Evidence (why — case study, industry support), Trade-offs (what we give up), Next steps (how to start). Written for a CIO who reads the first paragraph and skims the rest.

**Adaptable Mermaid Diagrams** — Start from the existing diagrams in `references/architecture/diagrams_converted/` but adapt them to the user's context:
- Replace generic labels with the user's domain names, platforms, and system names
- Highlight the components most relevant to the user's current question
- Provide the Mermaid source so the architect can paste it into their own tooling and edit further
- Suggest which diagrams to include for different audiences (governance council wants the E2E overview; architecture review board wants the key mapping detail)

**Architecture Decision Record (ADR)** — If the architect is documenting a decision, structure it as: Title, Status, Context, Decision, Consequences, Tenets applied. Reference the relevant Data Autonomy tenets as the rationale.

### Step 4c: Define comparison framework for alternative architectures

Architects will compare Data Autonomy to approaches their organisation is already invested in or their CIO has heard about. The skill should support honest, non-dismissive comparison with:

Alternative | Relationship to Data Autonomy | Where it overlaps | Where it diverges | Honest assessment
--- | --- | --- | --- | ---
Data Mesh (Dehghani) | Shares domain orientation and data-as-product; Data Autonomy predates and extends it | Domain ownership, data products, federated governance | Data Autonomy adds canonical models, key mapping, model-driven generation, polyglot persistence | Data Mesh is an organisational framework; Data Autonomy is an architectural pattern that can implement it
Data Fabric (Gartner) | Complementary — Data Fabric focuses on metadata-driven automation across platforms | Metadata-driven, governance, automation | Data Fabric is vendor/platform-oriented; Data Autonomy is model-first and platform-agnostic | They solve different problems; Data Autonomy models the semantics, Data Fabric automates the plumbing
Traditional EDW / centralised DW | Data Autonomy is partly a response to EDW limitations | Both want consistent enterprise semantics | EDW centralises ownership, storage, and logic; Data Autonomy distributes ownership and generates persistence | EDW works for small-scale analytics; breaks down with many source systems and multiple consumers
Data Lakehouse | Complementary — lakehouse is a platform pattern | Both support analytical + operational workloads | Lakehouse is a platform architecture; Data Autonomy is a modelling and design architecture that can target lakehouse platforms | Use both: model in MD-DDL, generate for lakehouse platforms
TOGAF / Zachman | Data Autonomy operates at the data architecture layer within these frameworks | Enterprise architecture governance, capability mapping | TOGAF is a methodology; Data Autonomy is a data architecture style | Data Autonomy fits within TOGAF's Technology Architecture or Data Architecture domains; they're not competing
Contract-first / API-first | Shares the emphasis on stable interfaces | Published contracts, consumer focus, governance | Data Autonomy generates contracts from models rather than hand-crafting them; emphasises canonical semantics over API design | Complementary — MD-DDL data products can be seen as declarative data contracts

The agent should:
- Never dismiss an alternative — acknowledge its strengths genuinely
- Help the architect articulate what Data Autonomy adds, not what it replaces
- Position combinations where appropriate ("you can use TOGAF for governance and Data Autonomy for data architecture")
- Be honest about where Data Autonomy requires organisational change that the alternative doesn't

---

## Phase 2: Handle Missing Diagrams

### Step 5: Identify high-value diagrams for Mermaid conversion

Of the 20 missing diagram references, these are the most valuable for teaching and should be recreated as Mermaid diagrams:

Priority | Diagram | Post | What it shows | Suggested Mermaid type
--- | --- | --- | --- | ---
1 | BoundedContext.png | Data Autonomy Overview / Holistic Data Mesh | Domain-aligned data mesh with semantic hubs and gateways | flowchart or C4
2 | SH Integration.png | Holistic Data Mesh | Application Abstraction Layers connecting to Semantic Hub | flowchart
3 | Canonical Data Model Pattern | Architecting Data Autonomy | Apps translating to/from canonical form | flowchart
4 | Data Products E2E | Architecting Data Autonomy | End-to-end: abstraction → canonical → platform services | flowchart
5 | Key Mapping | Architecting Data Autonomy | Source system IDs → canonical enterprise ID allocation | flowchart or ER
6 | OP2ANL.png | Automated Op-to-Analytics Transform | Recursive traversal from owner to source for events/entities | flowchart
7 | Flatten Example | Automated Op-to-Analytics Transform | Nested JSON → flattened wide-column | table or code block

Lower priority (nice to have but not essential for teaching):
- Loyalty Overview / Data Product Overview (case study diagrams)
- customer_GET_Queue (REST/event parity example)
- Nomenclature / TestDomain (pyMDG diagrams — less relevant to MD-DDL)
- Title graphics and metaphorical images (Flying Ship)

**Action:** Ask user to provide Mermaid versions for the top 7 priority diagrams, or provide the PNGs for reference so the agent (or a contributor) can recreate them.

---

## Phase 3: Embed in Contributor Instructions and CLAUDE.md

### Step 6: Add architecture philosophy section to copilot-instructions.md

Add a new section to `.github/copilot-instructions.md` — "Architectural philosophy" — that:

- States that MD-DDL implements the Data Autonomy architectural style
- Lists the 13 tenets as the design principles behind spec decisions
- Points to `references/architecture/` as the source material
- Instructs contributors: when adding or changing spec rules, consider which tenet(s) the rule implements — if none, question whether the rule belongs
- Instructs contributors: when reviewing agent prompts, verify they teach the *why* (architecture) not just the *what* (syntax)

**Relevant file:** `.github/copilot-instructions.md`

### Step 7: Add architecture reference to CLAUDE.md

Add a brief entry to `CLAUDE.md`:

- MD-DDL implements the Data Autonomy architectural style. See `references/architecture/` for foundational blog posts and `agents/agent-architect/skills/architecture/SKILL.md` for the distilled tenets.

**Relevant file:** `CLAUDE.md`

---

## Phase 4: Embed in Review Process

### Step 8: Add tenet alignment check to structural review

Add to `.github/md-ddl-review-prompt.md`:

- Check: Do spec rules trace to at least one architectural tenet? Flag rules that appear to have no architectural justification — they may be correct but should have documented rationale.
- Check: Does the Agent Architect architecture skill's tenet list match the current architectural tenets? Flag drift.

**Relevant file:** `.github/md-ddl-review-prompt.md`

### Step 9: Add architecture probe to adversarial review

Add to `.github/md-ddl-adversarial-review-prompt.md`:

- Probe: "Does the standard actually implement the stated architectural philosophy, or does it subtly contradict it?"
- Probe: "Are there design decisions in the spec that serve implementation convenience but violate the tenets?"
- Probe: "Could the architectural philosophy be used to justify removing or simplifying existing spec rules?"

**Relevant file:** `.github/md-ddl-adversarial-review-prompt.md`

---

## Phase 5: Update Agent Architect AGENT.md

### Step 10: Add architecture skill to skill table

Add the architecture skill to the skill index in `agents/agent-architect/AGENT.md`:

Skill | Trigger | Path
--- | --- | ---
**Architecture** | "why does MD-DDL"; "what's the philosophy"; "architecture"; "data autonomy"; "canonical data model"; "what problems does this solve"; "why not [alternative]"; "how does this fit enterprise architecture"; "compare to Data Mesh / Data Fabric"; "governance council"; "CIO presentation"; "position for"; "architecture decision"; any question about design rationale, architectural positioning, or comparison with alternative approaches | `skills/architecture/SKILL.md`

**Relevant file:** `agents/agent-architect/AGENT.md`

### Step 11: Update archetype table with architecture entry points

Add an "Architecture entry point" column to the User Archetypes table, or add notes to existing entries pointing to the architecture skill for "why" questions:

- Data Architect archetype: primary user of architecture skill **in Discuss mode**; governance council and CIO scenarios; all 13 tenets relevant; produces talking points, comparison tables, adaptable diagrams
- Enterprise Architect archetype: **new archetype** — uses Discuss mode; needs TOGAF/Zachman positioning, enterprise-scale justification, platform implications
- Data Engineer: tenets 3, 6, 7, 11, 12 most relevant; typically Teach mode
- Data Steward: tenets 5, 9, 13 most relevant; typically Teach mode
- Product Owner: tenets 9, 10 most relevant; case study $150M; may use Discuss mode for business case framing

**Relevant file:** `agents/agent-architect/AGENT.md`

---

## Relevant Files

- `agents/agent-architect/skills/architecture/SKILL.md` — new skill (Steps 1, 1b, 3, 4, 4b, 4c)
- `agents/agent-architect/skills/architecture/references/` — new reference stubs (Step 2)
- `references/architecture/*.md` — 17 blog posts (source material, already in repo)
- `references/architecture/diagrams_converted/*.md` — 7 Mermaid diagram conversions (already in repo)
- `agents/agent-architect/AGENT.md` — skill table + archetype updates (Steps 10, 11)
- `.github/copilot-instructions.md` — architecture philosophy section (Step 6)
- `CLAUDE.md` — architecture reference (Step 7)
- `.github/md-ddl-review-prompt.md` — tenet alignment check (Step 8)
- `.github/md-ddl-adversarial-review-prompt.md` — architecture probes (Step 9)

## Verification

1. Confirm `agents/agent-architect/skills/architecture/SKILL.md` has both Teach and Discuss protocols — frontmatter, dual-mode selection guidance, tenet table with counter-positions, reference table, comparison framework, output formats
2. Confirm reference stubs use `{{INCLUDE:}}` with relative paths that resolve correctly from the skill's `references/` directory
3. Confirm all 13 tenets are present in SKILL.md with Counter-position and Context dependency columns, and each maps to at least one MD-DDL spec concept
4. Confirm skill table in AGENT.md includes architecture with appropriate triggers including "governance council", "CIO", "compare to Data Mesh"
5. Confirm `.github/copilot-instructions.md` architecture section references the tenets and `references/architecture/`
6. **Teach mode test:** Ask Agent Architect "why does MD-DDL use canonical models instead of application-specific schemas?" — verify it loads the architecture skill, selects Teach mode, and explains using tenets 1, 3, 4, 11
7. **Discuss mode test:** Ask Agent Architect "I need to position Data Autonomy for my governance council next week — we're currently running a centralised EDW and the CIO has heard about Data Mesh" — verify it selects Discuss mode, asks about organisational context, positions relevant tenets with counter-arguments, and offers to produce talking points or a comparison table
8. **Non-dogmatic test:** Ask Agent Architect "I don't think canonical models work for us — our domains are too small and too integrated" — verify it engages with the objection using the Context dependency column rather than re-asserting the tenet
9. **Presentation output test:** Ask Agent Architect "can you give me a CIO executive summary for adopting a model-driven approach?" — verify it produces a structured executive summary (Context, Position, Evidence, Trade-offs, Next steps)
10. **Comparison test:** Ask Agent Architect "how does Data Autonomy differ from Data Mesh?" — verify it gives an honest, non-dismissive comparison acknowledging Data Mesh's strengths
11. Run structural review — verify tenet alignment check is present and passes
12. Grep all blog posts for `semprini.me/media/images` — confirm zero broken external image links remain (all replaced with Mermaid inlines or text descriptions)
13. Confirm `references/architecture/diagrams_converted/` Mermaid files are referenced from the correct blog posts
14. Confirm SKILL.md documents the extensibility pattern — how to add new posts, new themes, new diagrams, and external references

## Decisions

- **Skill lives in Agent Architect.** Architecture discussion, strategic positioning, and comparison with alternative approaches are Agent Architect's responsibility. Agent Guide may teach basic concepts and hand off to Agent Architect for deeper architectural discussion. Production domain modelling is Agent Ontology's job. The boundary rule holds: Architect discusses and positions, Ontology builds.
- **Dual-mode: Teach + Discuss.** Teach mode follows concept-explorer's progressive-depth pattern for users learning the concepts. Discuss mode follows a peer-discussion protocol for architects who already understand the space and need to explore, challenge, contextualise, and present. Mode is selected by user signal, not role — a Data Architect may sometimes want Teach mode for an unfamiliar concept.
- **Informed positions, not dogma.** The blog source is intentionally opinionated. The skill should present tenets as positions with rationale and acknowledged counter-positions. An architect needs to make their own case to their organisation; the agent's job is to help them think, not to convert them.
- **13 tenets distilled, not 17 blog posts summarised.** Users need principles they can discuss and apply, not a reading list. The tenets are the discussion core; blog posts are the reference material loaded on demand.
- **Tenet table includes counter-positions and context dependency.** Every tenet has an honest "the other side argues" and "this matters most when" qualifier. This prevents the agent from treating tenets as axioms and supports honest governance-council conversations.
- **Presentation outputs for architects.** The skill produces structured artifacts — talking points, comparison tables, executive summaries, adaptable Mermaid diagrams, ADRs — not just explanations. These outputs are what architects actually bring to governance councils and CIO meetings.
- **Honest comparison with alternatives.** Data Mesh, Data Fabric, EDW, Lakehouse, TOGAF, API-first — the skill positions Data Autonomy relative to each without dismissing them. The comparison framework acknowledges strengths of alternatives and identifies complementary relationships.
- **Reference stubs group posts thematically (5 groups), not individually (17 stubs).** Loading one thematic group gives enough context without flooding the context window. A user asking about anti-patterns gets vestigial technology + versioning + SoR + PoC in one load.
- **Mermaid diagrams for the top 7 missing visuals.** The remaining 13 are title graphics, metaphorical images, or tool-specific diagrams (pyMDG) that add less teaching value. User to provide PNGs or Mermaid versions for priority diagrams.
- **Philosophy embedded in instructions and reviews, not just the skill.** If the architecture rationale only lives in the skill, contributors can change the spec without considering it. Embedding in copilot-instructions ensures every contributor sees the tenets; embedding in reviews ensures drift is caught.

## Dependencies

- Step 5 (diagram conversion) depends on user providing PNGs or Mermaid versions — this is a collaboration step
- Steps 1–4 are independent of diagram work and can proceed immediately
- Steps 6–9 are independent of skill creation and can run in parallel
- Steps 10–11 depend on Step 1 (skill must exist before referencing it in AGENT.md)
- No dependencies on other plans (brownfield, example completeness, cross-domain, validation)

## Further Considerations

1. **Should Agent Ontology also reference architectural tenets?** When Agent Ontology makes trade-off decisions (entity vs enum, relationship granularity, domain scoping), the architectural tenets could inform those decisions. Recommendation: Not in this plan — Agent Ontology already has its own decision frameworks. If overlap is needed, add a reference stub in domain-scoping or entity-modelling skills pointing to the architecture references in a future iteration.

2. **Blog post versioning.** The blog posts are a snapshot of thinking at a point in time. If the architectural philosophy evolves, should the tenets be updated? Recommendation: Yes — the tenets in SKILL.md are the living version; blog posts are historical references. When a tenet changes, update SKILL.md and add a note to the blog post reference explaining the evolution.

3. **Should tenets appear in 1-Foundation.md?** The spec's Foundation section describes core principles. The 13 tenets are more granular than the current principles but align with them. Recommendation: Defer for now — the tenets are teaching artefacts (Agent Architect territory), not normative spec rules. If the spec wants architectural rationale, a "Design Rationale" appendix or section could reference the tenets without making them normative.

4. **Discuss mode boundary with Agent Ontology.** When an architect in Discuss mode says "let's start modelling my domain" — that's a handoff to Agent Ontology, not a continuation of the architecture discussion. The Discussion Protocol should recognise production-work triggers and hand off explicitly, just as the Teaching Protocol does.

5. **Governance council materials vs production artifacts.** The presentation outputs (talking points, comparison tables, executive summaries) are Agent Architect territory — they're communication artifacts supporting architectural positioning, not MD-DDL modelling artifacts. If an architect wants to create actual domain files, entity details, or physical schemas, that's Agent Ontology / Agent Artifact. The boundary is: Architect helps you *think about, position, and communicate* the architecture; Ontology and Artifact help you *implement* it.

6. **Comparison framework maintenance.** The alternative architecture comparison table will need updating as the industry evolves (new patterns, new vendor claims). Treat it like the tenet table — living content in SKILL.md, updated when new references arrive or the landscape shifts.
