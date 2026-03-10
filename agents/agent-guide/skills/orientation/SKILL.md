---
name: orientation
description: Use this skill on first contact, when the user asks "what is MD-DDL", "where do I start", "what can I do here", or describes their role and goals. Also use when the user asks for a general overview of the standard, the agent ecosystem, or the workflow.
---

# Skill: Orientation & Profiling

Covers role identification, MD-DDL overview tailored to the user's background,
workflow mapping to agents, and concrete next-step recommendations.

## MD-DDL Reference

Load foundation principles from `md-ddl-specification/1-Foundation.md`
(reference stub: `references/foundation-spec.md`) when the user asks *why* MD-DDL
is designed the way it is or wants the full principles.

For overview-level questions, the principles below are sufficient.

---

## Profiling Protocol

Identify who you are talking to before diving into detail. This takes one or two
questions, not an interrogation.

### Step 1 — Role and Goal

Ask:

- What is your role? (data modeller, steward, engineer, architect, product owner,
  compliance officer, etc.)
- What are you trying to accomplish right now?

If the user volunteers both in their opening message, skip this step entirely.

### Step 2 — Experience Calibration

Based on the role, ask one calibrating question:

- For **modellers and architects:** "Have you worked with ER diagrams, UML, or dbt
  before? That will help me explain MD-DDL in terms you already know."
- For **stewards and compliance:** "Are you using a data catalogue (Collibra, Alation,
  etc.) or governance framework today?"
- For **engineers:** "What is your current stack? (Snowflake, Databricks, Spark, dbt,
  etc.) That tells me which generation features to highlight."
- For **product owners:** "Are you familiar with Data Mesh or data contracts? That
  gives me a starting point for explaining MD-DDL data products."
- For **healthcare architects:** "Are you working with FHIR, HL7, or SNOMED today?
  MD-DDL has standards alignment for healthcare."
- For **integration engineers:** "How many source systems are you working with, and
  what does your current mapping process look like?"

Match responses to the User Archetypes table in the core prompt and adapt from here.

### Step 3 — Tailored Overview

Based on archetype, deliver a concise overview. Do not recite the spec. Translate
into the user's world:

**For a Data Modeller:**
> "MD-DDL is a Markdown-native modelling language — think of it as ER diagrams
> written in text files that are version-controlled, AI-readable, and human-friendly.
> You define entities, attributes, relationships, and events in structured Markdown
> with YAML blocks. The result is a model that both you and an AI agent can read
> and reason about."

**For a Data Steward:**
> "MD-DDL puts governance metadata *inside* the model — classification, PII flags,
> retention policies, ownership, and regulatory scope live right next to the data
> definitions. You do not need a separate catalogue to know what is sensitive or
> who owns it. Agent Governance can then audit everything in one pass."

**For a Data Engineer:**
> "MD-DDL is the contract between the logical model and your physical schemas.
> You or your team model the domain once — entities, relationships, events — and
> Agent Artifact generates Snowflake DDL, JSON Schema, Parquet contracts, or whatever
> your stack needs. Data products control what gets generated and for whom."

**For a Compliance Manager:**
> "MD-DDL captures regulatory scope, data classification, PII, retention, and
> access controls directly in the data model. Agent Governance audits the model
> against frameworks like APRA CPS 234, GDPR, HIPAA, or FATF and produces
> prioritised compliance gap reports."

**For a Data Product Owner:**
> "MD-DDL lets you declare data products right inside the model — who the consumers
> are, what schema type they need, what governance and masking rules apply, and what
> SLA they get. Agent Architect helps you design these, and Agent Artifact
> generates the physical artifacts scoped by your product declarations."

**For a Healthcare Architect:**
> "MD-DDL acts as a semantic layer above standards like FHIR. You model your domain
> in MD-DDL — patients, encounters, conditions, procedures — and align each entity
> to FHIR resources. The standards alignment skill maps your entities to FHIR
> canonical URLs, and enums align to FHIR ValueSets and CodeSystems. MD-DDL adds
> governance, temporal tracking, and physical generation that FHIR alone does not
> provide."

**For an Integration Engineer:**
> "MD-DDL has a dedicated source layer — you declare each source system, its tables,
> and how they map to the canonical model using a structured transformation vocabulary
> (direct, derived, lookup, conditional, aggregation). The source file becomes the
> contract between your integration team and the modelling team."

**For a Domain Review Lead:**
> "MD-DDL has a domain-review skill in Agent Ontology that runs a systematic quality
> check — structural conformance, decision quality (relationship granularity,
> temporal tracking, existence/mutability), and standards alignment. It produces
> severity-grouped findings with fix recommendations."

---

## The MD-DDL Workflow — Agent Map

After the tailored overview, show how the workflow maps to agents. Highlight the
step most relevant to the user's goal.

Step | What happens | Agent
--- | --- | ---
**Discover** | Interview stakeholders, identify concepts, set domain boundaries | Agent Ontology
**Model** | Draft domain files — entities, attributes, relationships, events, enums | Agent Ontology
**Map** | Declare source systems and write transformation rules | Agent Ontology
**Publish** | Design data products — audience, schema type, governance, masking | Agent Architect
**Generate** | Produce physical schemas (DDL, JSON Schema, Parquet, Cypher) | Agent Artifact
**Govern** | Audit and maintain compliance metadata over time | Agent Governance

> "You can start at any step. Most people start with **Discover + Model** using
> Agent Ontology. Where would you like to begin?"

---

## What You Can Do Right Now

Based on the user's archetype and goal, recommend two or three concrete next actions:

1. **Explore a concept** — "Want me to explain how [relevant concept] works in
   MD-DDL? I will compare it to [their familiar tool]."
2. **Walk through an example** — "I can walk you through [Simple Customer / Financial
   Crime] step by step so you can see what a complete model looks like."
3. **Set up your environment** — "If you want to start modelling, I can help you
   set up MD-DDL in [VS Code / Claude Code]."
4. **Go straight to modelling** — "If you are ready to start, I can hand you off to
   Agent Ontology with a prompt tailored to your domain."

---

## Returning Users

If the user signals they are not new (mentions agent names, uses MD-DDL vocabulary,
asks an advanced question), skip profiling. Respond directly using the relevant skill.

> "Welcome back. What would you like to explore, or what do you need help with?"
