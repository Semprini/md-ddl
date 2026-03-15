## MD-DDL Agent & Standard Effectiveness Report — 2026-03-13
**Spec version evaluated:** 0.9.0 (Draft)
**Agents evaluated:** Guide, Ontology, Artifact, Architect, Governance

---

### What This Evaluation Cannot Assess

- **Real stakeholder reactions.** Persona scores are pattern-matching against prompt architecture, not empathy. A real data modeller, healthcare architect, or risk manager would surface friction I cannot anticipate.
- **Runtime agent behaviour.** I am reading AGENT.md and SKILL.md files and inferring what the agent would do. Actual LLM behaviour depends on inference-time context, temperature, and model version — and may diverge from the prompt architecture in ways I cannot predict.
- **Industry standards depth.** I can confirm that standards reference files are referenced by agents (BIAN, FHIR, ISO 20022, TM Forum SID, ACORD) but cannot verify their substantive accuracy without reading the full reference file contents.
- **Regulatory fact correctness.** Retention periods, notification timeframes, and jurisdiction-specific obligations stated in regulator files may be outdated or incomplete. This evaluation accepts them at face value.
- **Skill file gaps I have not read.** Several skill files were not read in this session (orientation, concept-explorer, worked-examples, platform-setup, baseline-capture, domain-scoping, entity-modelling, relationship-events, standards-alignment, domain-review, source-mapping, dimensional, normalized, wide-column, knowledge-graph, product-design, odps-alignment, standards-conformance, compliance-audit). Assessments for those agents' scenarios are inferred from AGENT.md descriptions and spec knowledge.
- **Example breadth.** I read the Brownfield Retail and Financial Crime examples. Healthcare, Telecom, Retail Sales, and Retail Service were not read in detail. Industry-specific example assessments are directional.
- **Workflow continuity across real AI sessions.** The handoff friction analysis assumes an ideal agent that reads the handoff prompt and acts on it. Real sessions experience context window limits, misrouted queries, and user errors.

---

### Executive Summary

MD-DDL at version 0.9.0 is a structurally coherent standard with a well-designed multi-agent architecture. Agent Guide and Agent Governance are the strongest agents — both have clear skill loading protocols, well-matched persona archetypes, and behaviour modes that reflect real user needs. Agent Ontology handles the critical greenfield and brownfield modelling paths with depth. The weakest area is **model and product lifecycle management**: the standard has no versioning mechanism for attribute changes, no product lifecycle states, and no mechanism for propagating model changes to downstream products — making it unfit for production use in organisations where models evolve continuously. The most urgent priority is closing the `pii_fields` spec gap (identified in both Layer 2 and directly affecting 8+ agent skill files), followed by formalising product versioning and lifecycle, and adding self-referential relationship guidance.

---

### Agent Scorecards

#### Agent Guide

| Scenario | Skill Loading | Behaviour Mode | Output Quality | Boundary Respect | Persona Fit | Avg |
| --- | --- | --- | --- | --- | --- | --- |
| G1 — What is MD-DDL | 4/5 | 4/5 | 4/5 | 5/5 | 3/5 | **4.0** |
| G2 — Walkthrough | 4/5 | 4/5 | 4/5 | 5/5 | 4/5 | **4.2** |
| G3 — Concept exploration | 4/5 | 4/5 | 4/5 | 5/5 | 4/5 | **4.2** |
| G4 — Platform setup | 5/5 | 4/5 | 4/5 | 5/5 | 4/5 | **4.4** |
| G5 — Adoption planning | 5/5 | 5/5 | 4/5 | 5/5 | 5/5 | **4.8** |
| G6 — Agent navigation | 3/5 | 5/5 | 4/5 | 5/5 | 4/5 | **4.2** |
| **Average** | 4.2 | 4.3 | 4.0 | 5.0 | 4.0 | **4.3** |

**Strengths:**
- Behaviour modes (Welcome → Teach → Navigate) are well-designed for a learning agent. The "Do not lecture" directive prevents the most common AI tutoring failure mode.
- User Archetypes table is genuinely useful — maps 8 distinct roles to vocabulary, analogies, and recommended first agent. This makes tailoring concrete, not aspirational.
- Adoption Planning skill (G5) is excellent: 5-step process, clear signals for adoption pattern selection, handoff prompts to Agent Ontology. Rachel Kim would find exactly what she needs.
- Platform Setup trigger fires correctly on "VS Code" mention — G4 is handled cleanly.

**Gaps:**
- G6 has no dedicated skill for agent navigation — falls into Navigate mode which works but has no referenced skill. The agent directory table in AGENT.md is good but the lack of a skill means the quality of agent explanation depends entirely on what's in AGENT.md rather than a loaded reference.
- Alex Torres (new user, junior analyst) is not a precise match for any archetype. Closest is Data Engineer, but Alex is pre-engineer. The agent would over-calibrate vocabulary toward engineering concepts Alex doesn't have yet.
- The teaching limitation disclaimer ("this explanation is illustrative") is applied uniformly, even for non-governance concepts. This may undermine Alex's confidence when the disclaimer appears after a simple concept explanation.
- Layer 2 F1 (demonstration artifacts mistaken for production) applies: Agent Guide's non-negotiable rule about marking teaching examples is social convention, not structurally enforced.

**Persona feedback (Alex):** "The agent was helpful and didn't overwhelm me. But when I asked 'what is MD-DDL', it wanted to know my role before explaining anything. I already told you — I'm a data analyst. Just show me what it is."

**Persona feedback (Rachel):** "This was exactly what I needed. The adoption planning conversation gave me a roadmap I could take into a steering committee meeting. The handoff to Agent Ontology was clear and the suggested prompt covered what I wanted to ask."

---

#### Agent Ontology

| Scenario | Skill Loading | Behaviour Mode | Output Quality | Boundary Respect | Persona Fit | Avg |
| --- | --- | --- | --- | --- | --- | --- |
| O1 — New domain | 5/5 | 5/5 | 4/5 | 5/5 | 4/5 | **4.6** |
| O2 — Entity/enum/attribute | 5/5 | 4/5 | 4/5 | 5/5 | 5/5 | **4.6** |
| O3 — Standards alignment | 4/5 | 4/5 | 3/5 | 5/5 | 3/5 | **3.8** |
| O4 — Healthcare FHIR | 4/5 | 4/5 | 3/5 | 5/5 | 3/5 | **3.8** |
| O5 — Domain review | 5/5 | 5/5 | 4/5 | 5/5 | 5/5 | **4.8** |
| O6 — Model evolution | 4/5 | 4/5 | 3/5 | 5/5 | 4/5 | **4.0** |
| O7 — Baseline capture | 5/5 | 4/5 | 4/5 | 5/5 | 4/5 | **4.4** |
| O8 — Schema import | 4/5 | 3/5 | 4/5 | 5/5 | 4/5 | **4.0** |
| **Average** | 4.5 | 4.1 | 3.6 | 5.0 | 4.0 | **4.2** |

**Strengths:**
- O1 is a showcase scenario — Interview mode with two-to-three focused questions per turn, Domain Scoping + Entity Modelling + Relationship & Events all triggered correctly, events for claim lifecycle stages correctly proposed. Sarah Chen would find this the most productive new-domain starting point she's used.
- O5 (domain review) is well-supported — Domain Review skill loads correctly, systematic review protocol applies, and the Financial Crime example issues (Person/Individual naming, contradictory retention, missing relationship definition) are exactly the kind of thing the review protocol is designed to catch.
- O7 (baseline capture) is clean — the skill correctly distinguishes baseline documentation from canonical modelling. Rachel's "just document what exists" intent would be respected.
- Schema Import (O8) is technically impressive — the 3-question limit, inference table, and ETL parsing capability are well-designed for brownfield adoption.

**Gaps:**
- O3 and O4 (standards alignment for BIAN/ISO 20022 and FHIR): The Standards Alignment skill references `industry_standards/` files but I cannot verify their content depth. For a healthcare architect like Dr. Kowalski, superficial FHIR name-matching (resources that share names with MD-DDL entities) would not be enough — she needs polymorphic reference handling, which Layer 2 M1 confirms the standard cannot express.
- O6 (model evolution) has no guidance on product impact. When Reinsurance entities are added to a Claims domain, the agent would handle the entities correctly but would not proactively check whether existing data products need updating. There is no "downstream impact" step in any skill.
- O8 (schema import) conflicts with Interview mode — Layer 2 F2 applies. The schema-import skill correctly overrides the Interview default, but the AGENT.md "Do not generate MD-DDL" rule creates a tension the agent must navigate via the "narrow-scope shortcut" — which is not explicitly listed as applying to schema import.
- ACORD (insurance standard) is not referenced anywhere in the spec, agents, or skills. Sarah Chen, working at a mid-size insurer, would ask about ACORD alignment. The answer is "not supported" — which should be stated explicitly rather than discovered by absence.

**Persona feedback (Sarah):** "Agent Ontology asked me good questions and didn't just start drafting immediately. The entity/enum/attribute guidance for Claim Type was exactly right — it correctly identified type-specific fields as an inheritance signal. But when I asked about ACORD alignment, it had nothing to offer."

**Persona feedback (Marcus):** "The standards alignment conversation felt theoretical. I wanted to see a concrete recommendation for how my Customer, Account Holder, and Beneficial Owner map to BIAN's Party hierarchy. I got a comparison table but not a resolution."

**Persona feedback (Dr. Kowalski):** "MD-DDL's entity model makes sense for Patient, Encounter, Condition. Enums for ICD-10 and SNOMED code sets is a reasonable pattern. But the moment I asked about FHIR's polymorphic references (a Condition can reference a Patient or a Group), the agent could not express it. That's a real limitation for clinical data."

**Persona feedback (Kenji):** "The domain review protocol is systematic and found the right issues in Financial Crime. I would use this before every sign-off. The Party self-referential relationship missing from the Relationships table — the review caught that. Useful."

**Persona feedback (Rachel):** "Baseline capture was smooth. Schema import asked only three questions and produced a draft I could work with. The draft was correctly marked as inferred. The maturity level (mapped) was set correctly. Exactly what I needed."

---

#### Agent Artifact

| Scenario | Skill Loading | Behaviour Mode | Output Quality | Boundary Respect | Persona Fit | Avg |
| --- | --- | --- | --- | --- | --- | --- |
| A1 — Dimensional Snowflake | 5/5 | 5/5 | 4/5 | 5/5 | 4/5 | **4.6** |
| A2 — Product-scoped wide-column | 5/5 | 4/5 | 4/5 | 5/5 | 4/5 | **4.4** |
| A3 — Inheritance DDL | 5/5 | 4/5 | 4/5 | 5/5 | 4/5 | **4.4** |
| A4 — Knowledge graph | 5/5 | 4/5 | 4/5 | 5/5 | 4/5 | **4.4** |
| A5 — JSON Schema contracts | 3/5 | 4/5 | 3/5 | 5/5 | 3/5 | **3.6** |
| A6 — Reconciliation | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | **5.0** |
| **Average** | 4.7 | 4.3 | 4.0 | 5.0 | 4.0 | **4.4** |

**Strengths:**
- A1 is the canonical use case for Agent Artifact and is well-supported. Assessment mode, Dimensional + Snowflake dialect, correct existence/mutability → dimension type mapping, CLUSTER BY on large tables — all supported.
- A6 (reconciliation) is the standout scenario: the Reconciliation skill is well-designed, produces a clear structured diff report, and correctly scopes its boundary (reports, doesn't deploy). James would find this genuinely useful when transitioning from Level 3 to Level 4 maturity.
- Product-scoped generation (A2) works cleanly: `schema_type` drives skill selection, `entities` list scopes output, `governance` and `masking` constrain the artifacts. The product declaration serving as an input contract is architecturally sound.
- Boundary respect is consistent — Agent Artifact never claims to model, never claims to deploy. When A3 reveals a conceptual gap, it correctly defers to Agent Ontology.

**Gaps:**
- A5 (JSON Schema contracts): JSON Schema generation is listed as a Normalized skill output format, but the scenario "which skill covers this?" would cause hesitation. The Normalized skill trigger mentions DDL and JSON Schema, but the agent might load both Normalized and Dimensional before settling. JSON Schema `$ref` for relationships and MD-DDL-type-to-JSON-Schema-type mapping are likely partially covered but not verified.
- No explicit validation that generated DDL has been executed. Agent Artifact's "What This Agent Cannot Validate" section correctly declares execution correctness as out of scope, but James would want to know what platform-specific issues might arise at execution time — that guidance is absent.
- The three dialect files (Snowflake, Databricks, PostgreSQL) leave SQL Server, Oracle, and BigQuery without dialect support. For organisations not on these three platforms, the agent falls back to ANSI SQL — which may not satisfy James's "directly executable" requirement.

**Persona feedback (James):** "The star schema output for Snowflake had the right level of specificity — CLUSTER BY on the fact table, VARIANT for semi-structured columns, transient tables where appropriate. The mapping summary documenting fact/dimension decisions was something I could hand to my DBA as justification. The reconciliation skill was unexpectedly good — it found differences I'd missed. I would use Agent Artifact regularly. The one friction point was JSON Schema — the output was technically correct but the $ref handling for relationships felt under-specified."

**Persona feedback (Sarah):** "The class-table inheritance output for Claim subtypes was exactly what I would have designed myself. FK back to base table, no nullable type-specific columns. Would use this in production."

---

#### Agent Architect

| Scenario | Skill Loading | Behaviour Mode | Output Quality | Boundary Respect | Persona Fit | Avg |
| --- | --- | --- | --- | --- | --- | --- |
| D1 — Multi-consumer design | 5/5 | 5/5 | 4/5 | 5/5 | 4/5 | **4.6** |
| D2 — PII masking | 4/5 | 4/5 | 4/5 | 5/5 | 4/5 | **4.2** |
| D3 — ODPS manifest | 5/5 | 4/5 | 3/5 | 5/5 | 3/5 | **4.0** |
| D4 — Cross-domain product | 4/5 | 4/5 | 3/5 | 5/5 | 3/5 | **3.8** |
| D5 — Product versioning | 2/5 | 2/5 | 1/5 | 4/5 | 2/5 | **2.2** |
| **Average** | 4.0 | 3.8 | 3.0 | 4.8 | 3.2 | **3.8** |

**Strengths:**
- D1 (three-consumer product design) is well-handled. Assessment mode reads the domain, checks platform posture, and uses Product Design skill to guide entity scoping, class selection, and schema_type for each product. The three products map cleanly to source-aligned (monitoring), domain-aligned (regulatory), and consumer-aligned (analytics).
- Platform posture question (single vs polyglot vs selective) is a thoughtful design that captures real architectural diversity before committing to product class decisions.
- Boundary respect is good: Agent Architect does not generate DDL, correctly defers to Agent Artifact after product design, and defers to Agent Governance for compliance review.

**Gaps:**
- D5 (product versioning and lifecycle) is a critical failure: the spec has no product lifecycle states, no product versioning mechanism, no breaking-vs-non-breaking change classification, and no communication mechanism to downstream consumers. The agent would be forced to offer advice outside any spec guidance. Aisha would have no spec-backed answer to "how do I version a product that two teams depend on." This is a production-blocking gap for any organisation using MD-DDL at scale.
- D3 (ODPS manifest): The ODPS Alignment skill produces a manifest, but many fields will be flagged as TODO (pricing plans, contract terms, payment gateways, license details). For Aisha, publishing to a data marketplace, the number of TODOs may undermine confidence in the output. The data quality dimension inference (mapping `not_null` → completeness, `check` → validity) is a strength but may not be specified in sufficient detail to produce usable ODPS YAML without operator guidance.
- D4 (cross-domain 3-domain product): The `cross_domain` field exists but the spec does not address what happens when three domains with different governance postures, retention periods, and classifications are combined in a single consumer-aligned product. The agent would produce a declaration but could not resolve governance conflicts between domains — it would flag them as TODOs, leaving the decision to the user.
- The Architecture skill is planned but does not exist (`skills/architecture/SKILL.md` is marked as planned). Layer 2 F5 applies: any architecture philosophy request would fail to load a skill. The AGENT.md routes these requests to a non-existent skill with no fallback.

**Persona feedback (Aisha):** "The product design for three consumer groups was exactly right — I got three distinct products with the right class, schema_type, entity list, and masking strategy. The handoff to Agent Artifact was clear. But when I asked about versioning the product six months later, the agent had nothing structured to offer. It gave me good advice as free text, but I need a spec-backed mechanism I can point my stakeholders to. That's a gap."

**Persona feedback (Marcus):** "The masking strategy recommendations were specific — hash for TIN, year-only for DOB, truncate to postcode prefix for address. That's exactly the level of specificity I need. But the ODPS manifest had so many TODOs that I'm not sure how useful it is as a starting point for our marketplace catalogue team."

---

#### Agent Governance

| Scenario | Skill Loading | Behaviour Mode | Output Quality | Boundary Respect | Persona Fit | Avg |
| --- | --- | --- | --- | --- | --- | --- |
| R1 — Multi-jurisdiction audit | 5/5 | 5/5 | 4/5 | 5/5 | 5/5 | **4.8** |
| R2 — Product governance | 5/5 | 5/5 | 4/5 | 5/5 | 4/5 | **4.6** |
| R3 — Remediation | 5/5 | 5/5 | 4/5 | 5/5 | 5/5 | **4.8** |
| R4 — HIPAA healthcare | 4/5 | 4/5 | 3/5 | 5/5 | 3/5 | **3.8** |
| **Average** | 4.8 | 4.8 | 3.8 | 5.0 | 4.3 | **4.3** |

**Strengths:**
- R1 (APRA/RBNZ/FATF audit) is where Agent Governance shines. Loads all three regulator files, produces a structured gap report with severity levels, cites specific regulatory provisions. The regulator files provide jurisdiction-specific granularity. The staleness warning on regulator files is a responsible design choice. Priya would find this the most complete regulatory audit tool she has seen in a data catalogue or governance product.
- R3 (remediation) correctly distinguishes metadata changes (adding `data_residency` to governance block) from structural changes needing Agent Ontology. The before/after YAML diff format is exactly what an auditor needs for an evidence trail.
- The Governance → Architect handoff for product governance gaps (Layer 2 coverage) is the only agent pair with a formally specified bidirectional handoff: Governance flags, Architect fixes.

**Gaps:**
- R4 (HIPAA healthcare): While a hipaa.md regulator file exists, the spec's governance vocabulary uses `pii` (personally identifiable information) universally. HIPAA uses PHI (protected health information), which is a different concept. PHI includes information identifiable through combination (the "18 identifiers" list), is patient-linked, and carries de-identification requirements (Safe Harbor vs Expert Determination) that `pii: true` cannot express. The agent would apply the HIPAA file's requirements but map them to a `pii`-centric vocabulary that doesn't capture the PHI/PII distinction. Dr. Kowalski would notice this gap immediately.
- The `pii_fields` issue (Layer 2 C1/F3) directly impacts Agent Governance's effectiveness: every GDPR, HIPAA, and CCPA audit will produce false-positive findings for "missing `pii_fields`" when the entities have attribute-level `pii: true` markers instead. This makes Agent Governance's gap reports noisy and unreliable for these jurisdictions until the spec gap is closed.
- The RBNZ (Reserve Bank of New Zealand) BS11 request in R1 is ambiguous — it is listed as a regulator file but BS11 is a specific standard for outsourcing. Priya would expect RBNZ to cover prudential supervision broadly, not just outsourcing. If the rbnz.md file is scoped only to BS11, the audit would miss other RBNZ obligations.

**Persona feedback (Priya):** "The gap report format is exactly what I need for a risk committee presentation — severity, regulatory reference, recommended fix. The multi-jurisdiction handling was better than I expected. The staleness warning on the APRA file was appropriate — I confirmed with our compliance team. What frustrated me was the `pii_fields` findings — every entity had this as a 'critical gap' but our modeller said the PII is marked at attribute level, not in a list. That needs to be fixed before I can use this report without manual filtering."

**Persona feedback (Dr. Kowalski):** "The HIPAA audit flagged things correctly but used 'PII' where the regulation says 'PHI'. For a clinical audit, that vocabulary matters — PHI has a specific legal definition and specific de-identification requirements. The `pii: true` flag on Patient doesn't distinguish PHI from other PII, doesn't capture the 18 identifiers, and doesn't record whether we're using Safe Harbor or Expert Determination for de-identification. The governance model needs healthcare-specific vocabulary extensions."

**Persona feedback (Marcus):** "The product governance audit was exactly what I needed. It correctly identified that the source feed product had raw PII with no masking — that's a real gap. The handoff to Agent Architect for the fix was clean."

---

### Cross-Agent Workflow Scorecards

| Scenario | Handoff Clarity | Context Continuity | End-to-End Coherence | Avg |
| --- | --- | --- | --- | --- |
| X1 — Full lifecycle | 4/5 | 4/5 | 4/5 | **4.0** |
| X2 — Compliance → model change | 3/5 | 3/5 | 3/5 | **3.0** |
| X3 — Source onboarding → product | 3/5 | 2/5 | 3/5 | **2.7** |
| X4 — Brownfield adoption | 4/5 | 3/5 | 4/5 | **3.7** |
| X5 — New user onboarding | 4/5 | 3/5 | 3/5 | **3.3** |
| **Average** | 3.6 | 3.0 | 3.4 | **3.3** |

**X1 (Full lifecycle: Architect → Artifact → Governance)** scored 4/4/4: The product declaration is a well-defined input contract. Agent Artifact reads `schema_type`, `entities`, `governance`, `masking` from the product file and needs no re-explanation of design decisions. Agent Governance's Level 4 audit protocol is designed for product governance review. This is the most coherent multi-agent workflow in the system.

**X2 (Compliance gap → model change)** scored 3/3/3: Agent Governance's structural-change recommendation correctly defers to Agent Ontology. Agent Ontology's narrow-scope shortcut handles adding a single attribute. But the chain breaks at the third step: after the model change, Agent Architect is not explicitly notified that products exposing Party need masking review for the new `consent_basis` attribute. The user must remember to check this themselves. No trigger mechanism connects model changes to product review.

**X3 (Source onboarding → product)** scored 3/2/3: Source mapping is well-supported by Agent Ontology's Source Mapping skill. But the question "does the new source change any existing products?" has no mechanism. Agent Architect has no way to know that a new source system has been onboarded, or that its transform files map to entities that existing products expose. The source → canonical → product lineage is traceable in principle (reading source files then products) but there is no automated or prompted connection. Context continuity is the weakest dimension: the user carries all state between agents.

**X4 (Brownfield adoption: Guide → Ontology)** scored 4/3/4: Agent Guide's adoption planning with handoff prompts is well-designed. The baseline → schema import → canonical → governance chain is logically supported. Context continuity drops to 3/5 because each agent starts fresh — Agent Governance auditing a newly canonical domain does not know the domain came from a baseline, what baseline type was used, or what the adoption target date is.

**X5 (New user onboarding)** scored 4/3/3: Agent Guide → Agent Ontology handoff exists and the Navigate mode offers to draft the opening prompt. But there is a real gap: Alex, with no domain context, arrives at Agent Ontology. Agent Ontology's opening question is "Tell me about the business process or domain you want to model." Alex's answer ("I want to try modelling my analytics data") may not give enough for a focused interview. Agent Guide should offer a domain-selection exercise before handoff, not just a generic Agent Ontology prompt.

**Strongest workflow:** X1 (Full lifecycle: Architect → Artifact → Governance). The product declaration is an effective inter-agent contract.

**Weakest workflow:** X3 (Source onboarding → product). No lineage connection between source layer changes and product layer review. User must manually bridge the gap.

**Handoff pattern assessment:** Handoffs are uni-directional and script-based. No structured context object is passed between agents. All five workflow scenarios require the user to carry context manually between steps. This is architecturally acceptable (each agent is stateless by design) but creates consistent friction at every agent boundary. The handoff quality depends entirely on whether the previous agent's artifact (product declaration, gap report, source file) is readable by the next agent as a complete input contract — which is true for X1 but not for X2–X5.

---

### Standard Scorecards

| Scenario | Expressiveness | Completeness | Learnability | Avg |
| --- | --- | --- | --- | --- |
| G1 | 5/5 | 4/5 | 4/5 | **4.3** |
| G2 | 4/5 | 4/5 | 4/5 | **4.0** |
| G3 | 4/5 | 4/5 | 4/5 | **4.0** |
| G4 | 4/5 | 4/5 | 3/5 | **3.7** |
| G5 | 5/5 | 5/5 | 4/5 | **4.7** |
| G6 | 4/5 | 4/5 | 4/5 | **4.0** |
| O1 | 4/5 | 4/5 | 4/5 | **4.0** |
| O2 | 4/5 | 4/5 | 4/5 | **4.0** |
| O3 | 3/5 | 3/5 | 3/5 | **3.0** |
| O4 | 2/5 | 2/5 | 3/5 | **2.3** |
| O5 | 4/5 | 4/5 | 4/5 | **4.0** |
| O6 | 3/5 | 2/5 | 3/5 | **2.7** |
| O7 | 4/5 | 4/5 | 4/5 | **4.0** |
| O8 | 4/5 | 4/5 | 4/5 | **4.0** |
| A1 | 4/5 | 4/5 | 4/5 | **4.0** |
| A2 | 4/5 | 4/5 | 4/5 | **4.0** |
| A3 | 4/5 | 4/5 | 4/5 | **4.0** |
| A4 | 4/5 | 4/5 | 3/5 | **3.7** |
| A5 | 3/5 | 3/5 | 3/5 | **3.0** |
| A6 | 5/5 | 5/5 | 5/5 | **5.0** |
| D1 | 4/5 | 4/5 | 4/5 | **4.0** |
| D2 | 4/5 | 4/5 | 4/5 | **4.0** |
| D3 | 3/5 | 3/5 | 3/5 | **3.0** |
| D4 | 3/5 | 2/5 | 3/5 | **2.7** |
| D5 | 1/5 | 1/5 | 1/5 | **1.0** |
| R1 | 4/5 | 4/5 | 4/5 | **4.0** |
| R2 | 4/5 | 4/5 | 4/5 | **4.0** |
| R3 | 4/5 | 4/5 | 4/5 | **4.0** |
| R4 | 2/5 | 2/5 | 3/5 | **2.3** |
| **Average** | 3.7 | 3.6 | 3.7 | **3.7** |

---

### Standard Critique

#### 1. Conceptual Completeness — Adequate

MD-DDL covers the lifecycle from discovery through to external publication (ODPS) and brownfield adoption. Most stages have both spec coverage and agent support. The stages that fall short:

- **Product lifecycle and versioning** (D5): No product lifecycle states, no versioning mechanism, no breaking-change classification. Organisations that publish data products to external consumers need this before going to production. This is the largest completeness gap.
- **Self-referential relationships** (Layer 2 M2, C4): The Financial Crime example uses `Party ↔ Party` in its diagram but the spec has no guidance for self-referential relationships. Party networks are a first-class concern in financial crime — this is missing from a domain the spec uses as its quality benchmark.
- **Polymorphic relationships** (Layer 2 M1): `Document` attached to `Party | Transaction | Account` cannot be expressed. Common in document management, clinical systems, and audit trails.
- **Model evolution** (O6): Extending a domain in production has no guidance on downstream impact assessment. The brownfield adoption maturity model covers the initial adoption journey but not ongoing evolution of a canonical domain.

#### 2. Learning Curve — Needs Work

The standard has a steep initial climb. Evidence across personas:

- **Alex (New User)**: Agent Guide provides a viable on-ramp, but the gap between "learned concepts" and "first model" is real. There is no "quickstart" path — the Agent Guide → Agent Ontology transition requires Alex to arrive with a domain context that beginners often lack.
- **Sarah (Data Modeller)**: High value once past the initial learning. ER/UML background maps well to MD-DDL concepts. The ACORD gap (no insurance standard support) is a barrier for adoption in insurance verticals.
- **James (Data Engineer)**: The conceptual-to-physical mapping is well-documented. Agent Artifact's Assessment mode filters out the conceptual overhead efficiently. Low effective learning cost for engineers who use Agent Artifact.
- **Marcus (Data Steward)**: Agent Governance's compliance-audit skill has a steep setup cost — identifying applicable jurisdictions, understanding regulator file loading, interpreting gap reports. The `pii_fields` false positives (Layer 2 F3) would cause early frustration with governance tooling.
- **Dr. Kowalski (Healthcare)**: The standard's financial services orientation is visible. Healthcare concepts (PHI, coded value sets, FHIR resource model) require significant translation. Without a healthcare-specific example in the `examples/` directory, she would need to infer the patterns herself.

The two-layer structure (domain summary + detail files) adds navigational overhead for learners. The spec correctly calls it a benefit for AI context management and human readability, but for a new user reading a domain for the first time, following detail file links adds friction.

#### 3. Agent Handoff Friction — Adequate

Handoffs are scripted with suggested opening prompts in every agent that can receive or send a handoff. This is above average for a multi-agent system. The structural weaknesses are:

- **No context object.** The handoff script is a human-readable prompt, not a structured data transfer. The receiving agent gets no metadata about what the sending agent decided, why, or what was rejected. Every handoff re-sets the decision context.
- **Unidirectional defaults.** Governance → Architect and Ontology → Artifact are the best-defined handoffs. Architect → Governance, Artifact → Ontology (when model gaps are found), and any reverse handoff feel less scripted.
- **The user as the connector.** In every multi-step workflow (X1–X5), the user is the integration layer between agents. For Alex (new user), this may be the most significant barrier — the workflow requires understanding which agent to use when, which Agent Guide's G6 scenario addresses but incompletely.

#### 4. Governance Integration — Adequate

Governance metadata appears naturally in domain files from the first Agent Ontology drafting session. The two-tier model (domain defaults + entity overrides) reduces governance overhead for homogeneous domains. Weaknesses:

- **`pii_fields` gap** is the most urgent governance issue — it breaks every GDPR, HIPAA, and CCPA audit.
- **Healthcare PHI not expressible** in the standard governance vocabulary (`pii` maps to EU/AU/US general PII frameworks, not HIPAA PHI).
- **Product-level governance overrides** are well-designed but the governance inheritance model does not define what happens when a consumer-aligned product spans three domains with conflicting governance postures.
- **Governance timeline tracking** is absent. For a data risk manager managing audit findings over time, there is no mechanism to track when a governance gap was identified, when it was remediated, and by whom.

#### 5. Industry Alignment — Needs Work

The standard has good nominal coverage (BIAN, ISO 20022, FHIR, TM Forum SID mentioned in spec and agents) but uneven depth:

- **Financial services (BIAN, FATF, APRA, RBNZ)**: Strongest alignment. Multiple worked examples in Financial Crime. Regulatory compliance skill has mature financial services regulator files.
- **Healthcare (FHIR, HIPAA)**: Referenced but insufficient. No healthcare example in `examples/`. PHI/PII vocabulary gap. Polymorphic FHIR references not expressible.
- **Telecom (TM Forum SID)**: Referenced but depth of `industry_standards/` reference file unknown. Retail Service example exists but no Telco-specific guidance in agents.
- **Insurance (ACORD)**: Not mentioned anywhere in spec, agents, or skills. This is a gap for any insurance vertical adoption.
- **Retail/eCommerce**: Retail Sales and Retail Service examples exist but no named standard (GS1, ARTS, etc.) is referenced.
- **ODPS v4.0**: The ODPS alignment skill claims v4.0 conformance, but the data quality dimension inference rules and many TODO fields suggest partial mapping at best.

#### 6. Scalability — Adequate

- **5–50 entities**: The two-layer structure works well. Domain file remains navigable. Agent context management (load summary, follow links) handles this range.
- **50–200 entities**: Domain files with 100+ table rows will be unwieldy in Markdown. The two-layer structure helps but no guidance exists for organising entities into sub-domains or clusters within a domain file.
- **Cross-domain products**: The `cross_domain` field works for 2-domain scenarios. 3-domain (D4) governance conflicts are unresolved. 10+ domain interactions (enterprise data marketplace) have no mechanism.
- **Entity name collision** (Layer 2 S5): No disambiguation syntax when a consumer-aligned product's entity list includes a `Customer` from its own domain and a `Customer` from a cross-domain reference.

#### 7. Physical Generation Gap — Adequate

- Mapping rules are clear and deterministic: `existence` → dimension type, `mutability` → SCD type, temporal → date dimensions or SCD type 2/4. The mapping summary output documents decisions for auditability.
- Three dialect files (Snowflake, Databricks, PostgreSQL) cover the most common modern data warehouse platforms. SQL Server, BigQuery, and Oracle users fall back to ANSI SQL.
- Inheritance DDL templates (class-table, single-table, concrete-table) are correctly specified for the normalised skill.
- Knowledge graph generation appears well-specified (Cypher DDL, CREATE CONSTRAINT, parameterised templates) but is not verified as exhaustively as relational generation in this evaluation.
- The critical gap is **post-generation debugging**: when generated DDL produces unexpected output, the decision log ("mapping summary") helps but there is no trace from a specific physical column back to the MD-DDL attribute and the rule that produced it.

#### 8. Source and Transformation Coverage — Needs Work

- Source file format and transformation vocabulary (direct, derived, conditional, lookup, aggregation, reconciliation) are well-specified in Sections 7–8.
- The Schema Import skill handles ETL parsing (SQL, dbt models, stored procedures) and generates draft source transform files — this is a standout capability for brownfield adoption.
- The gap is agent support: Source Mapping is bundled with Agent Ontology but receives less attention than entity modelling. There is no dedicated agent for source layer operations. A Tomás (Integration Engineer) arriving at Agent Ontology expecting source mapping support may be routed to domain scoping instead.
- CDC (change data capture) model support is limited. The source file format supports `extract_type` (full, incremental, cdc) but transformation rules for CDC-specific patterns (before/after images, operation type column) are not specified.
- Lineage from source field → transformation → canonical attribute is traceable in principle by reading source files, but there is no agent skill that produces a lineage report (e.g., "show me all source fields that map to Party.Full Name").

#### 9. Model Evolution and Lifecycle — Needs Work

This is the standard's most significant operational gap for organisations that have been using MD-DDL for more than a few months:

- **Domain versioning**: Version numbers exist but no changelog format, no semantic versioning interpretation (major/minor/patch), no breaking-change classification. An `entities/customer.md` change from version 1.0 to 1.1 could be any kind of change — there is no way to tell without reading the diff.
- **Attribute deprecation**: No deprecated flag, no migration guidance, no "replaced by" syntax for renamed attributes. Downstream consumers who depend on `Full Name` have no way to know it was renamed to `Legal Name`.
- **Product versioning and lifecycle** (D5): No lifecycle states (draft/active/deprecated/retired). No mechanism for notifying downstream consumers of product changes. This is the single largest gap separating MD-DDL from being production-ready for organisations with active data product consumers.
- **Impact propagation**: When an entity changes, no mechanism checks which data products reference that entity and may need masking, governance, or schema updates.

#### 10. Brownfield Adoption — Strong

This is the standard's strongest new capability in the 0.9.0 draft:

- **Schema Import** is genuinely well-designed: 3-question limit, inference table, ETL parsing, draft output with uncertainty markers. Rachel Kim's scenario (45-table Snowflake DDL) would produce a usable draft in a single conversation.
- **Adoption maturity model** is realistic and incremental. The five levels (Documented → Mapped → Governed → Declarative → Automated) match the actual journey most organisations take. The "domain-level maturity" principle prevents over-claiming.
- **Coexistence** (baselines + canonical entities during transition) is explicitly designed and supported. No big-bang migration required.
- **Staleness rule** (flag adoption-stalled domains) is a thoughtful operational governance mechanism.
- Weakness: The perverse incentive identified in Layer 2 S4 (adding new entities regresses maturity) is a real friction point. A team proud of their Level 3 domain will be reluctant to add entities knowing it creates an "incomplete at current level" flag until all governance is added.

---

### Layer 2 Cross-References

Layers 1–2 findings that this stakeholder evaluation confirms, extends, or contextualises:

| Issue | Layer 2 Finding | Layer 3 Impact |
| --- | --- | --- |
| `pii_fields` spec gap (C1, F3) | Critical: field used in agent prompts but not in spec | **Confirmed critical**: directly breaks R4 (HIPAA), R1 (GDPR), and every compliance audit for these jurisdictions. All gap reports will contain false positives. |
| Person vs Individual naming (C2) | Critical: spec example uses Individual, FC example uses Person | **Confirmed**: O5 (domain review) would catch this. Kenji would flag it at review time. Real production risk if domains have conflicting naming conventions. |
| Architecture skill planned but absent (F5) | Agent failure mode: any architecture request fails | **Confirmed**: any discussion of "compare MD-DDL to Data Mesh" or "position for CIO" would produce an error loading a non-existent skill file. |
| No product versioning | Not explicitly flagged in Layer 2 as a standalone issue | **New finding Layer 3**: D5 scenario completely fails. This is a production-blocking gap for organisations with active data product consumers. |
| Self-referential relationships absent (M2, C4) | Structural weakness + missing capability | **Confirmed**: O4 (FHIR Patient Care, Group references) and any financial crime party network scenario hit this gap. |
| Cross-domain entity name collision (S5) | Structural weakness | **Confirmed via D4**: 3-domain product scenario makes the ambiguity real. |

| Layer 2 Finding | Layer 3 Assessment |
| --- | --- |
| Context loss on cross-agent handoff (S3) | Layer 3 confirms this in every multi-step workflow. The X-scenarios score consistently lower on Context Continuity (avg 3.0/5). |
| Event constraint example violates spec rules (X2) | Not directly tested in Layer 3 scenarios but would surface in O5 domain review. |
| Cardinality syntax inconsistency (X3) | Layer 3 adds: James (Data Engineer) would flag this — he expects the cardinality in generated DDL to match what the relationship YAML says, not the diagram. |

