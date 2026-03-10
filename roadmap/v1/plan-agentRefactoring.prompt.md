# Plan: Agent Refactoring

## TL;DR

Intentionally restructure the 5-agent architecture before executing any v1.0 roadmap plans. Rename `agent-dataproduct` → `agent-architect` (absorbing the architecture skill and keeping product-design + ODPS). Rename `agent-regulation` → `agent-governance` (broadening scope to include standards conformance assurance). Rebalance Ontology's skill load by confirming the 9-skill modelling lifecycle is coherent rather than splitting it further. Add a `standards-conformance` skill to Governance for post-hoc standards auditing. Update all cross-references: AGENT.md files, wrapper files, copilot-instructions.md, CLAUDE.md, and roadmap plans.

---

## Rationale

### Why refactor now

Six roadmap plans are about to add 6+ new skills across the agents. Without intentional design, the agent architecture would grow by accretion — skills piling onto whichever agent seemed closest at the time. This refactoring establishes the target agent architecture before any plans execute, so each skill lands in the right agent from the start.

### What's wrong with the current state

Problem | Symptom
--- | ---
**Data Product is underweight and misnamed** | 2 skills (product-design, odps-alignment). The name "Data Product" is too narrow for a standalone agent. Meanwhile, the architecture skill (a major planned addition) has no natural home.
**Regulation is underweight and too narrow** | 2 skills (regulatory-compliance, compliance-audit). The name "Regulation" implies legal compliance only, but governance assurance also covers standards conformance (BIAN alignment, FHIR mapping quality) — work that straddles Ontology's design-time standards-alignment and a missing assurance-time counterpart.
**Ontology is overloaded post-plans** | 9 skills covering domain scoping, entity modelling, relationship and event design, standards alignment, source mapping, domain review, preflight, plus planned baseline-capture and schema-import. The count is high, but the skills form a coherent modelling lifecycle — the issue is whether they are correctly grouped, not whether there are too many.
**Architecture skill has no natural home** | The architecture skill plan targets Agent Guide, but Guide is a learning agent — architecture discussion is strategic design work for architects, not onboarding.
**Agent names don't match target personas** | "Data Product" and "Regulation" are activity labels, not persona labels. An architect thinks in terms of architecture, products, and strategic alignment. A governance lead thinks in terms of standards conformance and regulatory compliance.

### Design principles for the refactoring

1. **Each agent owns a lifecycle phase.** The phase determines what goes in, what stays out.
2. **Agent names should be persona-intuitive.** A user should know which agent to invoke without reading documentation.
3. **Skills group by concern.** Strategic vs. tactical, design-time vs. assurance-time, conceptual vs. physical.
4. **Minimize handoffs for common workflows.** Two agents touching the same artifact in sequence is acceptable; three is a design smell.
5. **Shared references are normal; shared ownership is not.** Multiple agents may read the same reference files. Only one agent owns each skill.

---

## Proposed Agent Architecture

### Lifecycle mapping

```
Guide → Architect → Ontology → Artifact → Governance
(learn)  (strategy)  (model)    (generate)  (assure)
```

Agent Architect appears at two lifecycle points: before modelling (architecture discussion, strategic positioning) and after modelling (data product design and publication). This is intentional — strategic design bookends the modelling process.

### Agent summary (after refactoring)

Agent | Lifecycle phase | Skills | Modes
--- | --- | --- | ---
**Guide** | Learning and navigation | orientation, concept-explorer, worked-examples, platform-setup, adoption-planning† | Welcome, Teach, Navigate
**Architect** | Strategic design and data products | architecture†, product-design, odps-alignment | Discussion, Assessment, Design, Publication
**Ontology** | Domain discovery and modelling | domain-scoping, schema-import†, baseline-capture†, entity-modelling, relationship-events, standards-alignment, source-mapping, domain-review, preflight | Interview, Drafting, Refinement
**Artifact** | Physical artifact generation | dimensional, normalized, wide-column, knowledge-graph, reconciliation† | Assessment, Generation
**Governance** | Standards conformance and compliance assurance | regulatory-compliance (shared), compliance-audit, standards-conformance† | Conformance Audit, Compliance Audit, Regulatory Monitoring, Remediation

† = new skill from roadmap plans or this refactoring

### What changed

Change | Rationale
--- | ---
`agent-dataproduct` → `agent-architect` | Architect persona handles both strategic architecture discussion and data product design. "Architect" is persona-intuitive; "Data Product" was activity-scoped.
Architecture skill moves from Guide → Architect | Architecture discussion is strategic design work. Guide teaches concepts and onboards; Architect engages in strategic positioning, comparison, and presentation preparation.
`agent-regulation` → `agent-governance` | "Governance" encompasses both regulatory compliance AND standards conformance. The broader name matches the broader assurance mandate.
New `standards-conformance` skill on Governance | Post-hoc standards auditing (is this model aligned with BIAN/FHIR/ISO 20022?) is assurance-time work, distinct from Ontology's design-time standards-alignment.
`adoption-planning` skill stays on Guide | Adoption planning is advisory/consultative — assessing organisational readiness and recommending a path. The actual modelling work (baseline-capture, schema-import) happens on Ontology.
Ontology keeps 9 skills | They form a coherent modelling lifecycle sequence. The count is high but the concern set is unified: all skills produce or validate MD-DDL domain/entity content.

### What did NOT change

- **Agent Guide**: Same scope. Gains `adoption-planning` from the brownfield plan as originally designed.
- **Agent Ontology**: Same scope. Gains `baseline-capture` and `schema-import` from the brownfield plan as originally designed. `standards-alignment` stays (design-time).
- **Agent Artifact**: Same scope. Gains `reconciliation` from the brownfield plan as originally designed.
- **Review agent**: Unchanged. Needs awareness of renamed agents in its review protocols.

---

## Phase 1: Rename agent-dataproduct → agent-architect

### Step 1: Rename the canonical folder

Rename `agents/agent-dataproduct/` → `agents/agent-architect/`.

All files within move unchanged. Skill folders (`product-design/`, `odps-alignment/`) remain as-is — their names describe their function, not the parent agent's name.

### Step 2: Update AGENT.md identity and purpose

Rewrite the identity section of `agents/agent-architect/AGENT.md`:

Old identity | New identity
--- | ---
"Agent Data Product" | "Agent Architect"
"Data product design and publication agent" | "Strategic design and data product publication agent"
Lifecycle: product design and publication | Lifecycle: strategic architecture discussion, data product design, and ODPS publication

Update the skill index table to include the future `architecture` skill slot (marked as planned — will be populated when plan-architectureSkill executes):

Skill | Trigger | Path
--- | --- | ---
**Architecture** | Architecture philosophy; "why MD-DDL"; "compare to Data Mesh/TOGAF"; "position for governance council"; "CIO presentation"; data autonomy tenets; canonical data model rationale | `skills/architecture/SKILL.md` *(planned)*
**Product Design** | *(unchanged trigger)* | `skills/product-design/SKILL.md`
**ODPS Alignment** | *(unchanged trigger)* | `skills/odps-alignment/SKILL.md`

Update behaviour modes:

Mode | Description
--- | ---
**Discussion** | Active when discussing architecture philosophy, positioning tenets, comparing approaches, or preparing presentation material. *(New — activated by architecture skill)*
**Assessment** | *(unchanged — product context discovery)*
**Design** | *(unchanged — product declaration creation)*
**Publication** | *(unchanged — ODPS manifest generation)*

Update "What you are not":

- Keep: "Not a domain modeller" (defer to Ontology), "Not a physical artifact generator" (defer to Artifact), "Not a compliance auditor" (defer to Governance — updated name), "Not a runtime platform"
- Add: "Not a learning agent. You do not teach MD-DDL concepts or walk through tutorials. That is Agent Guide's responsibility."

Update cross-agent handoff rules:

- Handoff to Artifact — keep, same content
- Handoff to Ontology — keep, same content
- Handoff to Governance — update name from "Agent Regulation" to "Agent Governance"
- Handoff from Governance — update name, keep content
- Add handoff from Guide: "When Agent Guide identifies a user who wants to discuss architecture philosophy, compare MD-DDL to alternative approaches, or prepare strategic positioning material, it hands off to Agent Architect."

### Step 3: Update the wrapper file

Rename `.github/agents/agent-dataproduct.agent.md` → `.github/agents/agent-architect.agent.md`.

Update frontmatter:

```yaml
---
name: agent-architect
description: >-
  Specialist MD-DDL strategic design and data product publication agent for
  architecture philosophy discussion, data product declaration, product class
  and schema type selection, governance and masking strategies, and
  ODPS-aligned manifest generation.
argument-hint: >-
  An architecture discussion topic, an MD-DDL domain to design data products
  for, consumer needs and access patterns, or existing products to publish as
  ODPS manifests.
---
```

Update the include path to reference `agents/agent-architect/AGENT.md`.

### Step 4: Update all references to agent-dataproduct across the repo

Files that reference `agent-dataproduct` or "Agent Data Product" (exhaustive list):

File | What to update
--- | ---
`.github/copilot-instructions.md` | Agent responsibilities table, 3 boundary rules (Ontology vs Data Product, Data Product vs Artifact, Regulation vs Data Product), repository layout, adding new agent section
`CLAUDE.md` | Agent list
`agents/agent-guide/AGENT.md` | Agent directory / handoff table
`agents/agent-ontology/AGENT.md` | Handoff to Agent Data Product section
`agents/agent-regulation/AGENT.md` | Product governance handoff
`agents/agent-artifact/AGENT.md` | Check for any Data Product references
`roadmap/v1/plan-architectureSkill.prompt.md` | Architecture skill target agent (change from Guide to Architect)
`roadmap/v1/plan-brownfieldAdoption.prompt.md` | Any agent references
`roadmap/v1/plan-exampleCompleteness.prompt.md` | Any agent references
`roadmap/v1/plan-crossDomainReferences.prompt.md` | Any agent references

Search for: `agent-dataproduct`, `Agent Data Product`, `agent_dataproduct`, `@agent-dataproduct`, `DataProduct`.

---

## Phase 2: Absorb architecture skill into Agent Architect

### Step 5: Update plan-architectureSkill.prompt.md

The architecture skill plan currently targets Agent Guide. Update the plan to target Agent Architect instead:

- Change all references from "Agent Guide" to "Agent Architect" as the target agent
- Change skill path from `agents/agent-guide/skills/architecture/` to `agents/agent-architect/skills/architecture/`
- Remove the step that embeds architecture awareness in Guide's orientation skill — instead, add a handoff rule in Guide: "When a user asks about architecture philosophy, data autonomy tenets, or strategic positioning, hand off to Agent Architect"
- Keep the step that adds architecture references to copilot-instructions.md and CLAUDE.md
- Add a note that Guide may still reference architecture *concepts* when teaching (Teach mode), but strategic discussion and positioning belong to Architect (Discuss mode)

### Step 6: Add architecture awareness to Agent Guide's handoffs

In `agents/agent-guide/AGENT.md`, add Agent Architect to the agent directory / handoff table:

Agent | When to use | What it expects
--- | --- | ---
**Agent Architect** | Discuss architecture philosophy; compare MD-DDL to Data Mesh/TOGAF/other approaches; prepare material for governance councils or CIOs; design data products; generate ODPS manifests | An architecture topic to discuss, a domain to design products for, or products to publish

Update the existing Agent Data Product row to Agent Architect. Do not add a separate row — replace the existing one.

---

## Phase 3: Rename agent-regulation → agent-governance

### Step 7: Rename the canonical folder

Rename `agents/agent-regulation/` → `agents/agent-governance/`.

All files within move unchanged. Skill folders (`regulatory-compliance/`, `compliance-audit/`) remain as-is.

### Step 8: Update AGENT.md identity and purpose

Rewrite the identity section of `agents/agent-governance/AGENT.md`:

Old identity | New identity
--- | ---
"Agent Regulation" | "Agent Governance"
"Regulatory compliance and audit agent" | "Standards conformance and compliance assurance agent"
Lifecycle: governance assurance | Lifecycle: standards conformance auditing, regulatory compliance, and governance remediation

Update the skill index table to add the new `standards-conformance` skill:

Skill | When to load | Path
--- | --- | ---
**Standards Conformance** | User asks to check model alignment with industry standards (BIAN, FHIR, ISO 20022, TM Forum); post-modelling standards audit; "is this model aligned with [standard]?"; "check BIAN conformance" | `skills/standards-conformance/SKILL.md` *(planned — created in Phase 4)*
**Regulatory Compliance** | *(unchanged trigger)* | `skills/regulatory-compliance/SKILL.md`
**Compliance Audit** | *(unchanged trigger)* | `skills/compliance-audit/SKILL.md`

Update behaviour modes:

Mode | Description
--- | ---
**Conformance Audit** | *(New)* User provides a domain or asks "does this follow BIAN/FHIR/[standard]?"; load standards-conformance skill; evaluate entity naming, attribute alignment, relationship patterns against the target standard; produce a conformance report.
**Compliance Audit** | *(unchanged)*
**Regulatory Monitoring** | *(unchanged)*
**Remediation** | *(unchanged — expanded to include standards conformance remediation suggestions)*

Update "What you are not":

- Keep all existing rules
- Add: "Not a standards mapper during design. Design-time standards alignment (choosing entity names, applying standard attribute patterns during modelling) is Agent Ontology's responsibility via the standards-alignment skill. You audit conformance after the model exists."

Update cross-agent handoffs:

- All existing handoff rules stay, with "Agent Regulation" → "Agent Governance" name change
- Add handoff from Ontology for standards conformance: "When a user has completed domain modelling and wants to verify conformance with industry standards, Agent Ontology hands off to Agent Governance."
- Add handoff to Ontology for conformance gaps: "When standards conformance audit identifies structural alignment gaps (entity renaming, missing attributes to match a standard), flag the gap and defer structural changes to Agent Ontology."

### Step 9: Update the wrapper file

Rename `.github/agents/agent-regulation.agent.md` → `.github/agents/agent-governance.agent.md`.

Update frontmatter:

```yaml
---
name: agent-governance
description: >-
  Specialist MD-DDL standards conformance and compliance assurance agent for
  auditing standards alignment, regulatory compliance, governance metadata
  completeness, and guiding remediation across domain portfolios.
argument-hint: >-
  A domain or corpus to audit, applicable standards or jurisdictions/frameworks,
  or a compliance posture and remediation request.
---
```

Update the include path to reference `agents/agent-governance/AGENT.md`.

### Step 10: Update all references to agent-regulation across the repo

Files that reference `agent-regulation` or "Agent Regulation" (exhaustive list):

File | What to update
--- | ---
`.github/copilot-instructions.md` | Agent responsibilities table, 3 boundary rules (Ontology vs Regulation, Regulation vs Data Product → Governance vs Architect, adding new agent section), shared skills section, repository layout
`CLAUDE.md` | Agent list
`agents/agent-guide/AGENT.md` | Agent directory / handoff table
`agents/agent-ontology/AGENT.md` | Handoff to Agent Regulation section, shared skill reference
`agents/agent-architect/AGENT.md` | Handoff to/from Governance (already updated in Phase 1 if Phase 1 runs first)
`agents/agent-artifact/AGENT.md` | Check for any Regulation references
`roadmap/v1/plan-brownfieldAdoption.prompt.md` | Any agent references
`roadmap/v1/plan-validationPhilosophy.prompt.md` | Any agent references

Search for: `agent-regulation`, `Agent Regulation`, `agent_regulation`, `@agent-regulation`.

---

## Phase 4: Create standards-conformance skill

### Step 11: Create the skill folder and SKILL.md stub

Create `agents/agent-governance/skills/standards-conformance/SKILL.md` with:

**Trigger description:**
- "Is this model aligned with [standard]?"
- "Check BIAN conformance"
- "FHIR alignment audit"
- "Standards conformance report"
- "Does this follow [industry standard]?"
- Post-modelling standards quality check

**Skill purpose:**

Audit an existing MD-DDL domain model against one or more industry standards (BIAN, FHIR, ISO 20022, TM Forum, ACORD) and produce a structured conformance report. This is assurance-time work — the model already exists and the auditor checks alignment quality.

**Distinction from standards-alignment (Ontology):**

Activity | Agent | When
--- | --- | ---
Apply standard naming and patterns during design | Ontology (standards-alignment) | During modelling
Audit alignment quality after modelling | Governance (standards-conformance) | After modelling

**Conformance report format:**

The skill should produce a report structured as:

```markdown
## Standards Conformance Report: [Domain Name]

### Target Standard: [Standard Name and Version]

### Summary
- Entities audited: N
- Conformant: N
- Partial: N
- Non-conformant: N
- Not applicable: N

### Entity-Level Findings

#### [Entity Name]
- **Conformance:** Full | Partial | Non-conformant | N/A
- **Standard reference:** [Standard entity/resource/service domain]
- **Findings:** [Specific alignment or misalignment notes]
- **Recommendation:** [If partial or non-conformant, what structural change would improve alignment — defer to Agent Ontology]
```

**Shared references:**

This skill loads the same industry standard reference files as Ontology's standards-alignment skill:
- `industry_standards/bian/` — BIAN service domains, business objects, enumerations
- `industry_standards/fhir/` — FHIR resource types and profiles
- `industry_standards/tmforum/` — TM Forum entity types

The standard files are read-only shared references, not owned by either skill.

**Non-negotiable rules:**

- Never modify entity, relationship, or domain files. Produce findings and recommendations only.
- Always load the relevant standard reference files before stating conformance. Do not assess conformance from training knowledge alone.
- Structural changes (entity rename, attribute addition, relationship redesign) are recommendations that defer to Agent Ontology.
- Conformance is graded, not binary. "Partial" is a valid and common state — it means the entity is recognisably aligned but not fully conformant.

---

## Phase 5: Update boundary rules and cross-references

### Step 12: Update copilot-instructions.md

This is the most impactful file — it governs all contributor and agent behaviour.

**12a. Update repository layout section**

Replace `agent-dataproduct/` with `agent-architect/` and `agent-regulation/` with `agent-governance/` in the directory tree. Update the descriptions.

**12b. Update agent responsibilities table**

Agent | Lifecycle stage | Owns
--- | --- | ---
`agent-guide` | Learning and navigation | Standard explanation, user orientation, concept teaching, worked example walkthroughs, platform setup, adoption planning, agent navigation and handoff
`agent-architect` | Strategic design and data products | Architecture philosophy discussion, data product class selection, entity scoping, governance overrides, masking strategies, ODPS manifest generation, external catalogue alignment
`agent-ontology` | Discovery and design | Domain modelling, entity authoring, relationship and event design, source system mapping and field-level transformations, standards alignment during authoring, baseline capture, schema import
`agent-artifact` | Physical artifact generation | Dimensional star schemas, normalized 3NF designs, wide-column reporting schemas, knowledge graph schemas, SQL DDL, JSON Schema, Cypher, Parquet schema contracts, brownfield reconciliation
`agent-governance` | Standards conformance and compliance assurance | Standards conformance auditing, compliance metadata auditing, regulatory monitoring, governance remediation

**12c. Update boundary rules**

All 7 boundary rules need updating. The renamed agents change 5 of them. One new boundary rule is added.

**Boundary rule — Guide vs All Specialists:** Update to mention Agent Architect (not Agent Data Product) among the specialists that Guide hands off to. Add architecture discussion to the list of things Guide does not do.

**Boundary rule — Guide vs Ontology:** Unchanged.

**Boundary rule — Guide vs Architect (NEW):** Agent Guide may mention architecture concepts when teaching (Teach mode). Agent Architect engages in strategic architecture discussion, positioning, and comparison (Discuss mode). If Agent Guide identifies that a user wants to discuss architecture philosophy, compare approaches, or prepare strategic material, it hands off to Agent Architect. Do not add strategic discussion capability to Agent Guide, and do not add tutorial or onboarding capability to Agent Architect.

**Boundary rule — Ontology vs Artifact:** Unchanged.

**Boundary rule — Ontology vs Architect:** *(renamed from Ontology vs Data Product)* Agent Ontology creates the initial `## Data Products` summary table during domain drafting. Agent Architect takes over for detailed product design — choosing product class, scoping entities, setting governance overrides, masking strategies, and generating external manifests (ODPS). Agent Architect also handles architecture philosophy discussion. Do not add detailed product design, ODPS generation, or architecture discussion to Agent Ontology, and do not add entity modelling or relationship design to Agent Architect.

**Boundary rule — Architect vs Artifact:** *(renamed from Data Product vs Artifact)* Agent Architect produces MD-DDL data product declarations that serve as input contracts for Agent Artifact. Agent Artifact generates physical artifacts scoped by the product's metadata. Do not add physical artifact generation to Agent Architect, and do not add product design or ODPS alignment to Agent Artifact.

**Boundary rule — Ontology vs Governance:** *(renamed from Ontology vs Regulation)* Agent Ontology applies governance metadata and industry standards alignment during authoring (design-time). Agent Governance audits standards conformance and regulatory compliance after modelling (assurance-time). If a compliance or conformance gap requires a structural model change, Agent Governance flags it and defers the structural work to Agent Ontology. Do not add structural modelling capability to Agent Governance, and do not add post-hoc conformance auditing to Agent Ontology.

**Boundary rule — Governance vs Architect:** *(renamed from Regulation vs Data Product)* Agent Governance may audit data product governance and masking metadata and produce recommendations. Agent Architect owns all product declarations and applies approved changes. Agent Governance flags product governance gaps; Agent Architect fixes them. Do not add product declaration authoring to Agent Governance, and do not add compliance auditing to Agent Architect.

**12d. Update shared skills section**

Update the shared skills paragraph to reference Agent Governance instead of Agent Regulation. Also note that industry standard reference files (BIAN, FHIR, etc.) are shared read-only references used by both Ontology (standards-alignment) and Governance (standards-conformance).

**12e. Update adding-a-new-agent section**

Update any references to existing agent names.

### Step 13: Update CLAUDE.md

Update the agent list to use new names:

- **Agent Architect** — Strategic design and data product publication.
  Read: `.md-ddl/agents/agent-architect/AGENT.md`
- **Agent Governance** — Standards conformance and compliance assurance.
  Read: `.md-ddl/agents/agent-governance/AGENT.md`

### Step 14: Update review agent awareness

In `.github/agents/review-md-ddl.agent.md` — check for references to old agent names. The review agent reviews the standard, agents, and examples. It may reference agent names in its review criteria or examples. Update any found references.

Also check the review prompt files:
- `.github/md-ddl-review-prompt.md`
- `.github/md-ddl-adversarial-review-prompt.md`
- `.github/md-ddl-evaluation-prompt.md`
- `.github/md-ddl-layered-review-process.md`

---

## Phase 6: Update remaining roadmap plans

### Step 15: Update plan-architectureSkill.prompt.md

Critical change: the architecture skill now targets Agent Architect, not Agent Guide.

- Replace all "Agent Guide" references with "Agent Architect" in the context of skill placement
- Update skill path from `agents/agent-guide/skills/architecture/` to `agents/agent-architect/skills/architecture/`
- Add a step defining the Guide → Architect handoff for architecture discussions
- Keep the step for embedding architecture awareness in copilot-instructions.md and CLAUDE.md
- Note: the teaching protocol (Teach mode) in the architecture skill still works — Architect can teach architecture concepts to an architect persona. The distinction is that Guide teaches MD-DDL concepts to any persona, while Architect discusses architecture philosophy with architects.

### Step 16: Update plan-brownfieldAdoption.prompt.md

- Check all agent name references. The plan references Agent Ontology (baseline-capture, schema-import), Agent Guide (adoption-planning), and Agent Artifact (reconciliation). These placements are unchanged. Verify no references to "Agent Data Product" or "Agent Regulation" need updating.

### Step 17: Update other plans

Check and update any agent name references in:
- `plan-exampleCompleteness.prompt.md`
- `plan-crossDomainReferences.prompt.md`
- `plan-validationPhilosophy.prompt.md`
- `plan-bianV14Migration.prompt.md`

---

## Verification Checklist

After all phases complete:

Check | How to verify
--- | ---
No orphaned references to `agent-dataproduct` | Grep for `agent-dataproduct`, `Agent Data Product`, `@agent-dataproduct` across all files. Zero hits.
No orphaned references to `agent-regulation` | Grep for `agent-regulation`, `Agent Regulation`, `@agent-regulation` across all files. Zero hits.
All 5 agent folders exist with correct names | `agents/agent-guide/`, `agents/agent-architect/`, `agents/agent-ontology/`, `agents/agent-artifact/`, `agents/agent-governance/`
All 5 wrapper files exist with correct names | `.github/agents/agent-guide.agent.md`, `.github/agents/agent-architect.agent.md`, `.github/agents/agent-ontology.agent.md`, `.github/agents/agent-artifact.agent.md`, `.github/agents/agent-governance.agent.md`
Wrapper includes point to correct AGENT.md | Each wrapper's include path references the renamed canonical folder
Agent responsibilities table has 5 rows | copilot-instructions.md — guide, architect, ontology, artifact, governance
Boundary rules reference correct names | 8 boundary rules, all using current agent names
CLAUDE.md agent list matches | 5 agents with correct names and descriptions
Every AGENT.md cross-agent handoff uses current names | No agent mentions "Data Product" or "Regulation" when it means "Architect" or "Governance"
Shared skill ownership is declared | regulatory-compliance owned by Governance, loaded by Ontology — documented in copilot-instructions.md
Industry standard references are documented as shared | copilot-instructions.md notes that BIAN/FHIR/etc. references are used by both Ontology and Governance
Architecture skill plan targets Agent Architect | plan-architectureSkill.prompt.md references agent-architect, not agent-guide
Review agent knows the current names | review-md-ddl.agent.md and all review prompts use current agent names

---

## Execution Dependencies

This plan must execute BEFORE any other roadmap plans, because every other plan references agent names that this plan changes.

### Internal phase ordering

Phases may execute in any order with one constraint:

- **Phase 1 and Phase 2 are coupled** — rename agent-dataproduct first, then absorb architecture skill.
- **Phase 3 and Phase 4 are coupled** — rename agent-regulation first, then add standards-conformance skill.
- **Phase 5 depends on Phases 1–4** — cross-reference updates use the final agent names.
- **Phase 6 depends on Phase 5** — plan updates use the final cross-references.

### External plan ordering

After this plan completes, the remaining roadmap plans execute in their own dependency order:

Plan | Depends on
--- | ---
plan-architectureSkill | This plan (agent name + target changed)
plan-brownfieldAdoption | This plan (agent name verification)
plan-exampleCompleteness | Independent (but benefits from correct agent names in examples)
plan-crossDomainReferences | plan-exampleCompleteness (needs Healthcare domain)
plan-validationPhilosophy | Independent
plan-bianV14Migration | Independent

---

## Decisions for the Author

Decision | Options | Recommendation
--- | --- | ---
**Ontology skill count** | (A) Keep 9 skills as a coherent modelling lifecycle. (B) Split into two agents (e.g., separate source-mapping and brownfield skills into an "integration" agent). | **A — Keep 9 skills.** They form a clear sequence: scope → import → capture → model → connect → align → map sources → review → preflight. Splitting would create a new agent with no clear persona and add handoffs.
**Architecture Teach mode location** | (A) Architect can teach architecture concepts (dual Teach/Discuss). (B) Only Guide teaches; Architect only discusses. | **A — Architect can teach.** An architect asking "what is data autonomy?" should not be redirected to Guide. The distinction is persona: Guide teaches MD-DDL-the-standard to all personas; Architect teaches architecture-the-philosophy to architects.
**Standards-conformance skill depth** | (A) Full audit protocol with graded conformance, per-entity findings, structured report. (B) Lightweight check with pass/partial/fail per entity. | **A — Full audit.** Governance audits should match the depth of compliance-audit. Lightweight checks can be a subset mode, not a separate skill.
**Review agent updates** | (A) Update review prompts to reference new agent names. (B) Review prompts are agent-name-agnostic, no changes needed. | **Investigate — read the review prompts** to determine whether they reference specific agent names before deciding.
**Shared skill documentation** | (A) Document shared references in copilot-instructions.md only. (B) Also add a shared-references section to each consuming AGENT.md. | **A — copilot-instructions.md only.** Each AGENT.md already declares which external skills/references it loads. A separate shared-references section would duplicate that.
