---
name: orientation
description: Use on first contact, when the user asks "what is MD-DDL", "where do I start", or "what can I do here", describes their role and goals, or wants an overview of the standard, the agents, or the workflow.
---

# Skill: Orientation

Find out who the user is, give them an overview of MD-DDL in their own terms, and
suggest a concrete next step.

Load `md-ddl-specification/1-Foundation.md` (stub: `references/foundation-spec.md`) if
the user asks *why* MD-DDL is designed as it is. For an overview, this skill is enough.

---

## Profile in One or Two Questions

If the opening message doesn't already say, ask the user's role and what they're trying
to do. Then ask one calibrating question that tells you which analogies will work:

Role | Calibrating question
--- | ---
Modeller or architect | ER, UML, or dbt background?
Steward or compliance | Which catalogue or governance framework today?
Engineer | Current stack (Snowflake, Databricks, Spark, dbt)?
Product owner | Familiar with Data Mesh or data contracts?
Healthcare architect | Using FHIR, HL7, or SNOMED?
Integration engineer | How many source systems, and how is mapping done today?

Match the answers to the User Archetypes table in the core prompt. Returning users,
those who use MD-DDL vocabulary or name agents, skip profiling entirely.

## Tailor the Overview

Say in a few sentences what MD-DDL gives *this* person. Don't recite the spec. What to
emphasise for each archetype:

Archetype | What MD-DDL means for them
--- | ---
Data Modeller | ER-style modelling in version-controlled Markdown with YAML, readable by people and AI agents alike
Data Steward | Classification, PII, retention, ownership, and regulatory scope live inside the model, so Agent Governance can audit everything in one pass
Data Engineer | Model the domain once; Agent Artifact generates DDL, JSON Schema, Parquet contracts, and dbt projects, scoped by data products; Agent Test turns worked examples into tests
Compliance Manager | Regulatory scope and data sensitivity live in the model; Agent Governance audits against frameworks such as APRA CPS 234, GDPR, HIPAA, and FATF and produces prioritised gap reports
Data Product Owner | Products are declared in the model: consumers, schema type, governance, masking, SLA. Agent Architect designs them and publishes ODPS manifests
Healthcare Architect | A semantic layer above FHIR: entities align to resources, enums to ValueSets, plus governance, temporal tracking, and generation that FHIR alone doesn't give
Integration Engineer | A source layer declares each system and table, how columns map to the canonical model, and worked examples that pin the expected output and become tests
Domain Review Lead | Agent Ontology's domain-review skill checks structure, decision quality, and standards alignment, and returns findings by severity

Then show the workflow from the core prompt, highlighting the step closest to the
user's goal. Most people start with Discover and Model in Agent Ontology.

## Suggest Next Steps

Offer two or three of these, whichever fit the user's archetype and goal:

- Explain a concept by comparing it with a tool they know (Concept Explorer)
- Walk through an example domain (Worked Examples)
- Set up MD-DDL in their environment (Platform Setup)
- Plan adoption around their existing systems (Adoption Planning)
- Go straight to modelling, with a drafted opening request for Agent Ontology
