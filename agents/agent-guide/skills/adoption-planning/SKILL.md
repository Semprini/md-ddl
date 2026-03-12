---
name: adoption-planning
description: Use this skill when the user mentions existing systems, legacy, migration, brownfield, "we already have", "starting from", "current state", or asks how to adopt MD-DDL into an environment with existing data assets. Also use when the user asks about maturity levels, adoption timelines, or how to plan an MD-DDL rollout.
---

# Skill: Adoption Planning

Guides users through assessing their current data landscape and creating an
adoption roadmap for MD-DDL. This skill teaches the adoption maturity model
and helps users understand which starting-point pattern applies to them.

## MD-DDL Reference

Load the Adoption specification from `md-ddl-specification/10-Adoption.md`
before responding. Key sections to apply:

- **Adoption Maturity Model** — the five levels and advancement criteria
- **Adoption Journey Patterns** — the four starting-point patterns (A/B/C/D)
- **Baselines** — folder structure and file format
- **Domain Adoption Metadata** — the `adoption` block in domain metadata

---

## Process

### Step 1 — Assess Current State

Understand what existing data assets the user has. Ask:

- What existing data assets do you have? (dimensional models/star schemas,
  enterprise/canonical models, ETL/ELT pipelines, governance catalog metadata)
- What platforms are these on? (Snowflake, Databricks, SQL Server, dbt,
  Informatica, Collibra, Purview, etc.)
- How many business domains are involved?

Listen for signals that indicate which adoption pattern applies:

Signal | Pattern
--- | ---
Star schemas, fact/dimension tables, data warehouse | Pattern A (Dimensional)
Enterprise data model, canonical model, CDM | Pattern B (Canonical)
dbt models, ETL pipelines, SSIS, Informatica | Pattern C (ETL/ELT)
Collibra, Purview, Alation, data catalog | Pattern D (Catalog)

Multiple patterns may apply — most organisations have a mix.

### Step 2 — Assess Target State

Ask:

- What maturity level are you aiming for? (Explain the levels if needed)
- What is your timeline?
- Is this a single-domain pilot or a multi-domain rollout?

Recommend starting with **Declarative** (Level 4) as a realistic initial
target for most organisations. **Automated** (Level 5) requires CI/CD
integration that is typically a later investment.

### Step 3 — Identify Starting Domains

Ask:

- Which business domain should we start with?
- Which domain is best understood, has the clearest ownership, and has the
  most willing stakeholders?

Recommend starting with a single, well-understood domain. Success with one
domain creates the template and organisational confidence for the next.

### Step 4 — Create Adoption Roadmap

Based on Steps 1–3, outline a per-domain adoption roadmap:

1. **Domain name** and starting pattern (A/B/C/D)
2. **Current assets** to baseline
3. **Target maturity** and estimated timeline
4. **Key milestones** mapped to maturity levels
5. **Risks and dependencies** (stakeholder availability, platform access, etc.)

Present this as a Markdown table or structured outline the user can save.

### Step 5 — Hand Off

Direct the user to the appropriate next step:

- For baseline documentation → Agent Ontology with baseline-capture skill
- For fast-track DDL import → Agent Ontology with schema-import skill
- For greenfield modelling → Agent Ontology with domain-scoping skill

Offer to formulate the opening prompt for the target agent.

---

## Teaching Points

When explaining the adoption model, emphasise:

- **You do not need to start from scratch.** MD-DDL meets you where you are.
- **Baselines are temporary.** They exist to be superseded by canonical entities.
- **Maturity is domain-level.** You do not need the whole organisation at the
  same level — progress domain by domain.
- **The schema-import skill is the fastest path.** Paste DDL, answer 2–3
  questions, get a draft domain in minutes.
- **Coexistence is expected.** During transition, baselines and canonical
  entities coexist. This is normal and designed for.

---

## Handoff Prompts

**To Agent Ontology (baseline-capture):**
> "I would like to document my existing [dimensional models / ETL pipelines /
> catalog metadata] as MD-DDL baselines for the [domain name] domain."

**To Agent Ontology (schema-import):**
> "I have existing DDL from [platform]. I would like to import it into a
> draft MD-DDL domain."

**To Agent Ontology (domain-scoping):**
> "I would like to model the [domain name] domain from scratch."
