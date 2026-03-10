# MD-DDL Agent & Standard Effectiveness Evaluation

You are conducting a structured evaluation of the MD-DDL standard and its AI agents
by simulating realistic stakeholder interactions. Your goal is to assess whether each
agent effectively serves its intended audience and whether the standard itself supports
the data management lifecycle end to end.

This is Layer 3 of a multi-layer review process. Layer 1 (Structural Review) and
Layer 2 (Adversarial Review) should have been run first. Reference their findings
where relevant — this layer evaluates fitness for purpose, not structural correctness.

**Evaluation discipline:** You will be assessed on the quality of your criticisms,
not your supportiveness. Scores of 5/5 require specific evidence of excellence.
Scores of 4/5 or below are expected for most dimensions — a standard at Draft 0.9.0
should have meaningful gaps. An evaluation that produces mostly 4s and 5s across
the board is suspect. If you cannot identify genuine weaknesses in a scenario,
state what you lack the expertise to evaluate.

This is not a structural review of the repository (that is `md-ddl-review-prompt.md`).
This evaluation tests whether the agents and standard **work for real people doing
real work**.

Write the findings to the `review.md` file.

---

## Before you begin — load the standard and agents

Read these files in order. You need the full context to simulate authentic interactions.

### Specification (read all)

1. `md-ddl-specification/1-Foundation.md` — core principles
2. `md-ddl-specification/2-Domains.md` — domain file format
3. `md-ddl-specification/3-Entities.md` — entity and attribute definitions
4. `md-ddl-specification/4-Enumerations.md` — enum structure
5. `md-ddl-specification/5-Relationships.md` — relationship semantics
6. `md-ddl-specification/6-Events.md` — event structure and temporal rules
7. `md-ddl-specification/7-Sources.md` — source system declarations
8. `md-ddl-specification/8-Transformations.md` — transformation vocabulary
9. `md-ddl-specification/9-Data-Products.md` — data product classes and declarations

### Agents (read AGENT.md and each skill's SKILL.md)

1. `agents/agent-ontology/AGENT.md` — discovery and design agent
2. `agents/agent-ontology/skills/domain-scoping/SKILL.md`
3. `agents/agent-ontology/skills/entity-modelling/SKILL.md`
4. `agents/agent-ontology/skills/relationship-events/SKILL.md`
5. `agents/agent-ontology/skills/standards-alignment/SKILL.md`
6. `agents/agent-ontology/skills/domain-review/SKILL.md`
7. `agents/agent-artifact/AGENT.md` — physical artifact generation agent
8. `agents/agent-artifact/skills/dimensional/SKILL.md`
9. `agents/agent-artifact/skills/normalized/SKILL.md`
10. `agents/agent-artifact/skills/wide-column/SKILL.md`
11. `agents/agent-artifact/skills/knowledge-graph/SKILL.md`
12. `agents/agent-architect/AGENT.md` — strategic design and data product publication agent
13. `agents/agent-architect/skills/product-design/SKILL.md`
14. `agents/agent-architect/skills/odps-alignment/SKILL.md`
15. `agents/agent-governance/AGENT.md` — standards conformance and compliance assurance agent
16. `agents/agent-governance/skills/standards-conformance/SKILL.md`
17. `agents/agent-governance/skills/compliance-audit/SKILL.md`
18. `agents/agent-governance/skills/regulatory-compliance/SKILL.md`

### Reference examples (read domain + at least 3 entity files + 1 source + 1 product)

1. `examples/Financial Crime/domain.md`
2. `examples/Financial Crime/entities/party.md`
3. `examples/Financial Crime/entities/transaction.md`
4. `examples/Financial Crime/entities/account.md`
5. `examples/Financial Crime/products/analytics.md`
6. `examples/Financial Crime/sources/salesforce-crm/source.md`

---

## Stakeholder Personas

Each persona represents a real person who would interact with MD-DDL agents in their
daily work. Use these personas to simulate interactions and evaluate whether the agents
meet their needs.

The personas are drawn from different industries and organisational roles to test the
standard's breadth. When evaluating, consider whether the standard and agents are
industry-neutral or implicitly biased toward any one sector.

---

### Persona 1 — The Data Modeller

**Name:** Sarah Chen
**Role:** Senior Data Modeller, Enterprise Data Architecture
**Background:** 12 years modelling experience. Fluent in ER diagrams, UML, and 3NF.
Has used Erwin, PowerDesigner, and dbt. New to MD-DDL but experienced with
Markdown-native tooling. Works in a large insurance company.

**Goals:**

- Model a new Claims domain from scratch using MD-DDL
- Understand how MD-DDL handles inheritance (Person → Employee → Adjuster)
- Decide when to use an entity vs an enum vs an attribute
- Produce a domain file and entity detail files that pass peer review

**Pain points:**

- Frustrated by tools that force GUI workflows — prefers text-native
- Needs to understand the *why* behind modelling decisions, not just the syntax
- Has strong opinions about normalisation and will push back on denormalised suggestions
- Wants to know how MD-DDL compares to what she already knows (ER, UML class diagrams)

**Primary agent:** Agent Ontology
**Secondary agents:** Agent Artifact (to validate her model produces clean physical output)

---

### Persona 2 — The Data Steward

**Name:** Marcus Okafor
**Role:** Data Steward, Customer Data Domain
**Background:** 8 years in data governance. Responsible for data quality, lineage,
and metadata management. Uses a data catalogue tool (Collibra/Alation). Not a
developer but reads YAML comfortably. Works at a mid-size bank.

**Goals:**

- Review an existing MD-DDL domain for governance completeness
- Ensure PII is correctly identified and classified across all entities
- Add retention policies that satisfy both GDPR (EU customers) and APRA (AU parent company)
- Publish data products to an internal catalogue with clear ownership and SLA

**Pain points:**

- Doesn't write code — needs the agent to explain and draft, not just generate
- Cares deeply about governance metadata accuracy — incorrect retention periods are audit findings
- Needs to reconcile multi-jurisdiction requirements without legal expertise
- Wants a single view of "what is published and for whom" across the domain

**Primary agents:** Agent Governance, Agent Architect
**Secondary agent:** Agent Ontology (for governance metadata during entity review)

---

### Persona 3 — The Data Risk Manager

**Name:** Priya Sharma
**Role:** Head of Data Risk, Group Risk Function
**Background:** 15 years in risk management and regulatory compliance. Reports to
CRO. Responsible for ensuring the organisation's data assets comply with prudential
standards. Not hands-on with data modelling but reviews and approves governance postures.
Works at a large Australian bank with NZ subsidiary.

**Goals:**

- Audit the Financial Crime domain's compliance posture against APRA CPS 234, RBNZ, and FATF
- Identify gaps where entities contain PII without adequate governance metadata
- Assess whether data products expose sensitive data with insufficient masking
- Get a board-ready summary of compliance gaps and remediation priorities

**Pain points:**

- Time-poor — needs findings in priority order, not a raw list
- Expects the agent to cite specific regulatory requirements, not general best practice
- Will reject vague findings like "consider adding governance" — needs specific references
- Wants to understand cross-jurisdiction conflicts (where AU and NZ requirements diverge)

**Primary agent:** Agent Governance
**Secondary agent:** Agent Architect (to review product-level governance)

---

### Persona 4 — The Data Engineer

**Name:** James Reeves
**Role:** Senior Data Engineer, Analytics Platform Team
**Background:** 10 years building data pipelines. Expert in SQL, Spark, dbt, and
Parquet. Responsible for translating logical models into physical schemas on
Snowflake and Databricks. Evaluates MD-DDL as a replacement for ad-hoc ERDs
shared via Confluence.

**Goals:**

- Generate a dimensional star schema from the Financial Crime domain for Snowflake
- Produce JSON Schema contracts for API validation
- Create a wide-column denormalised table for a real-time transaction monitoring dashboard
- Understand how MD-DDL data products control what gets generated and what doesn't

**Pain points:**

- Impatient with "chatty" agents — wants to get to generation quickly
- Cares about dialect-specific details (Snowflake VARIANT columns, Databricks DELTA)
- Will test edge cases: what happens with many-to-many relationships, multi-table inheritance, temporal attributes?
- Wants deterministic output — running the same request twice should produce the same DDL

**Primary agent:** Agent Artifact
**Secondary agent:** Agent Architect (to understand product-scoped generation)

---

### Persona 5 — The Data Product Owner

**Name:** Aisha Rahman
**Role:** Data Product Owner, Retail Banking Analytics
**Background:** 6 years in product management, transitioned to data products 2 years
ago. Responsible for defining what data is published, for whom, and under what terms.
Works with data engineers, consumers, and governance to produce catalogued data products.
Familiar with Data Mesh concepts.

**Goals:**

- Design data products for the Financial Crime domain serving three distinct consumer groups
- Choose the right product class and schema type for each consumer
- Define masking strategies for PII attributes in consumer-facing products
- Generate an ODPS manifest for publishing to an external data marketplace
- Understand how MD-DDL data products connect to physical generation

**Pain points:**

- Needs to balance consumer needs against governance constraints
- Wants to understand the full lifecycle: design → declare → generate → publish
- Expects clear handoff guidance between agents (when to use which)
- Wants the ODPS manifest to be as complete as possible, with clear gaps flagged

**Primary agent:** Agent Architect
**Secondary agents:** Agent Artifact (for generation), Agent Governance (for governance review)

---

### Persona 6 — The Healthcare Data Architect

**Name:** Dr. Lena Kowalski
**Role:** Chief Data Architect, Regional Health Network
**Background:** 10 years in health informatics. Expert in FHIR R4, HL7v2, and
SNOMED CT. Responsible for a data platform that integrates EMR, claims, and
clinical trial data across 12 hospitals. Evaluating MD-DDL as a semantic layer
above her existing FHIR-based data lake.

**Goals:**

- Model a Patient Care domain covering patients, encounters, diagnoses, procedures,
  and medications
- Align entity definitions with FHIR resources (Patient, Encounter, Condition)
- Handle healthcare-specific complexity: coded concepts (ICD-10, SNOMED), temporal
  clinical events, patient consent under HIPAA
- Understand whether MD-DDL adds value on top of FHIR or duplicates it

**Pain points:**

- Healthcare data is inherently hierarchical and coded — needs rich enum/reference support
- HIPAA consent and de-identification rules are non-negotiable
- Temporal precision matters: encounter start/end, medication administration timestamps
- Will push back if MD-DDL can't express FHIR's polymorphic reference types

**Primary agent:** Agent Ontology
**Secondary agents:** Agent Governance (HIPAA compliance), Agent Artifact (clinical data warehouse)

---

### Persona 7 — The Integration Engineer

**Name:** Tomás Rivera
**Role:** Senior Integration Engineer, Enterprise Data Platform
**Background:** 8 years building integration pipelines. Expert in Kafka, dbt, and
source system reverse engineering. Responsible for onboarding new source systems
into the canonical data model. Works at a large retailer with 6 source systems
feeding a single Customer domain.

**Goals:**

- Declare a new source system (Shopify POS) and map its tables to existing
  canonical entities
- Write transformation rules for non-trivial mappings (concatenation, lookup,
  conditional logic)
- Understand how MD-DDL source files relate to the canonical domain model
- Validate that source mappings cover all required canonical attributes

**Pain points:**

- Source systems have messy schemas — needs flexible mapping vocabulary
- Wants the source file to be the contract between his team and the modelling team
- Needs to handle source-specific quirks (NULL semantics, date formats, composite keys)
- Expects the agent to understand the separation between source layer and canonical layer

**Primary agent:** Agent Ontology (source mapping falls under domain scoping)
**Secondary agents:** Agent Artifact (to generate transformation artifacts)

---

### Persona 8 — The Domain Review Lead

**Name:** Kenji Nakamura
**Role:** Lead Data Architect, Data Governance Office
**Background:** 15 years in enterprise architecture. Responsible for reviewing and
approving domain models before they enter production. Peer-reviews other modellers'
work. Uses MD-DDL daily and knows the spec well. Works at a large telco.

**Goals:**

- Run a full quality review of a completed domain before signing it off
- Check structural conformance, decision quality, and standards alignment
- Verify that the domain model is ready for downstream consumption by Agent Artifact
  and Agent Architect
- Identify modelling anti-patterns (over-entity-ing, missing temporal tracking,
  inconsistent granularity)

**Pain points:**

- Has seen too many domains approved with hidden quality issues
- Wants a systematic checklist, not ad-hoc review
- Needs to verify standards alignment for the telecom industry (TM Forum SID)
- Expects the review to surface issues the original modeller missed

**Primary agent:** Agent Ontology (Domain Review skill)
**Secondary agents:** Agent Governance (governance review)

---

## Evaluation Method

For each agent, simulate **the assigned interactions** using the personas specified
in each scenario. Each interaction represents a realistic task the persona would
bring to the agent.

### How to simulate

1. **State the persona and task** — describe what the persona is asking for as if
   they were typing into a chat with the agent
2. **Evaluate the agent prompt** — based on what the AGENT.md, skills, and loaded
   references contain, assess how the agent would respond
3. **Score the interaction** using the rubric below
4. **Record standard feedback** — note any point where the MD-DDL specification
   itself is the limiting factor, not the agent

### What you are evaluating

You are not running the agents live. You are reading their prompt architecture
(AGENT.md, skills, references) and assessing whether they are structured to handle
each scenario effectively. Consider:

- Would the agent load the right skill for this request?
- Would the behaviour mode transitions work naturally for this persona's workflow?
- Does the agent have access to the information needed to respond correctly?
- Would the output follow the spec accurately?
- Would the agent know when to defer to another agent, and would the handoff be clear?
- Would the persona find the interaction helpful, or would they be frustrated?

---

## Evaluation Scenarios

### Agent Ontology — Discovery and Design

**Scenario O1 — New domain from scratch (Sarah, Data Modeller)**
> "I need to model our Claims domain. We have claims, policies, claimants,
> adjusters, and service providers. Claims go through stages — lodged, assessed,
> approved, paid, closed. Adjusters are employees who can be internal or external
> contractors. How do I start?"

Evaluate: Does the agent enter Interview mode? Does it ask focused questions about
scope and boundaries before drafting? Does it correctly trigger Domain Scoping and
Entity Modelling skills? Does it handle the inheritance question (adjuster types)
with appropriate trade-off discussion? Does it propose events for claim lifecycle
stages?

**Scenario O2 — Entity vs enum vs attribute decision (Sarah, Data Modeller)**
> "In our claims model, we have 'Claim Type' — it's things like Motor, Property,
> Liability, Workers Comp. Each type has different required fields. Motor claims need
> vehicle registration, property claims need address, liability has coverage limits.
> Should this be an entity, an enum, or an attribute?"

Evaluate: Does the agent load Entity Modelling skill? Does it explain the decision
framework (static list → enum, behavioural differences → entity, single value → attribute)?
Does it correctly identify that type-specific required fields signal entity-level
modelling (inheritance or composition), not a simple enum? Does it present trade-offs?

**Scenario O3 — Standards alignment challenge (Marcus, Data Steward)**
> "We're modelling our customer data domain. We need to align with BIAN Service
> Domains for banking and ISO 20022 for party identification. But our internal
> model doesn't match BIAN's Party concept cleanly — we have Customer, Account
> Holder, and Beneficial Owner as separate things. How should we reconcile?"

Evaluate: Does the agent load Standards Alignment skill? Does it use the
reconciliation protocol (comparison table, option evaluation, resolution proposal)?
Does it avoid blindly copying BIAN structure and instead help the user map their
concepts? Does it stay in Interview mode long enough, or does it rush to draft?

**Scenario O4 — Healthcare domain with FHIR alignment (Dr. Kowalski, Healthcare Data Architect)**
> "I need to model a Patient Care domain. Core concepts are Patient, Encounter,
> Condition (diagnosis), Procedure, and Medication Administration. These map to
> FHIR R4 resources. Encounters have start and end timestamps. Conditions reference
> ICD-10 and SNOMED codes. How should I structure this in MD-DDL?"

Evaluate: Does the agent enter Interview mode and explore healthcare-specific
complexity? Does it load Standards Alignment skill for FHIR? Does it recognise
that ICD-10 and SNOMED code sets are enums (or reference entities if they carry
metadata)? Does it handle temporal precision for clinical events? Does it help
Dr. Kowalski understand how MD-DDL's entity/enum model maps to FHIR's resource
model? Does the standards reference material cover FHIR, or is this a gap?

**Scenario O5 — Domain review and quality gate (Kenji, Domain Review Lead)**
> "Review the Financial Crime domain. Check structural conformance, decision
> quality, and standards alignment. I want to know if this domain is ready for
> production — flag any anti-patterns, missing temporal tracking, inconsistent
> granularity, or governance gaps."

Evaluate: Does the agent load Domain Review skill? Does it follow the systematic
review protocol (Inventory & Coverage → Structural Conformance → Decision Quality
→ Standards & Regulatory)? Does it cross-reference entity-modelling and
relationship-events guidance for decision quality checks? Can it identify
anti-patterns like over-entity-ing, missing events for lifecycle transitions, or
inconsistent `existence`/`mutability` choices? Does the review output give Kenji
a clear pass/fail with specific findings?

**Scenario O6 — Model evolution: adding entities to an existing domain (Sarah, Data Modeller)**
> "Our Claims domain has been in production for 6 months. Now we need to add
> Reinsurance entities — Treaty, Facultative Placement, and Recovery. These
> relate to existing Claim and Policy entities. How do I extend the domain without
> breaking what's already published?"

Evaluate: Does the agent handle incremental modelling (extending an existing domain
vs. greenfield)? Does it check for impacts on existing relationships, data products,
and physical artifacts? Does it advise on versioning the domain file? Does the
standard's domain metadata support version tracking for evolution? Does the agent
reference the domain-boundaries guidance for deciding whether Reinsurance belongs
in the Claims domain or warrants its own domain?

---

### Agent Artifact — Physical Generation

**Scenario A1 — Dimensional star schema for Snowflake (James, Data Engineer)**
> "Generate a dimensional star schema from the Financial Crime domain targeting
> Snowflake. I need fact tables for transactions and events, with dimensions for
> party, account, branch, and currency. Use Snowflake-specific syntax — VARIANT
> columns for semi-structured attributes, CLUSTER BY for large tables."

Evaluate: Does the agent enter Assessment mode first? Does it load the Dimensional
skill and the Snowflake dialect reference? Does it correctly map MD-DDL entity
existence/mutability to dimension vs fact? Does it handle Snowflake dialect
correctly (VARIANT, CLUSTER BY, transient tables, object tagging)? Does it produce
a mapping summary justifying fact/dimension/bridge decisions?

**Scenario A2 — Product-scoped generation (James, Data Engineer)**
> "I want to generate physical artifacts for the Transaction Risk Summary data
> product only — not the whole domain. The product is in
> `examples/Financial Crime/products/analytics.md`. It declares
> `schema_type: wide-column`. Generate it for Databricks."

Evaluate: Does the agent recognise the product reference and scope generation to
the product's entity list? Does it load the Wide Column skill and the Databricks
dialect reference? Does it apply the product's governance and masking metadata?
Does it respect the `schema_type` rather than defaulting to its own preference?
Does it use Delta Lake features (TBLPROPERTIES, change data feed, Unity Catalog)?

**Scenario A3 — Edge case: multi-table inheritance (Sarah, Data Modeller)**
> "My Claim entity uses table-per-subtype inheritance. MotorClaim, PropertyClaim,
> and LiabilityClaim each have different attributes. Generate normalised DDL that
> handles this — I need proper foreign keys back to the base Claim table and I
> don't want NULLable columns for type-specific fields."

Evaluate: Does the agent handle the inheritance pattern correctly? Does it load
Normalized skill and apply the inheritance DDL templates (class-table pattern)?
Does it produce separate tables with FK back to base using the documented templates?
Does the inheritance strategy decision table help select the right approach?

**Scenario A4 — Knowledge graph generation (James, Data Engineer)**
> "Generate a Neo4j knowledge graph schema from the Financial Crime domain. I want
> node labels for all entities, relationship types with properties, and uniqueness
> constraints. Show me how inheritance (Party → Person/Company) maps to graph labels.
> Include Cypher DDL I can run directly."

Evaluate: Does the agent load the Knowledge Graph skill? Does it correctly map
entities to nodes, relationships to graph relationships, and inheritance to
multi-label nodes? Does it generate valid Cypher DDL (CREATE CONSTRAINT, CREATE
INDEX)? Does it handle enums (as labels, properties, or separate nodes)? Does it
produce seed data for reference entities? Would James find the output directly
executable?

**Scenario A5 — JSON Schema contracts for API validation (James, Data Engineer)**
> "Generate JSON Schema contracts for the Party, Account, and Transaction entities
> from the Financial Crime domain. These will be used for API request/response
> validation. I need proper `$ref` for relationships, enum validation, and
> required/optional field handling based on constraints."

Evaluate: Does the agent handle JSON Schema generation? Which skill covers this
(Normalized)? Does it correctly map MD-DDL types to JSON Schema types? Does it
handle relationships as `$ref` references? Does it map `not_null` constraints to
`required` arrays? Does it handle enums as `enum` values in JSON Schema? Is there
a gap in the skills for non-DDL output formats?

---

### Agent Architect — Design and Publication

**Scenario D1 — Design products for multiple consumers (Aisha, Data Product Owner)**
> "The Financial Crime domain needs to serve three consumer groups: (1) the
> transaction monitoring team who need real-time wide-column access, (2) the
> regulatory reporting system that needs normalised SAR data, and (3) our data
> science team who want a dimensional model for pattern analysis. Help me design
> the right data products."

Evaluate: Does the agent enter Assessment mode and read the domain? Does it load the
Product Design skill? Does it propose three distinct products with appropriate class
and schema_type? Does it guide the user through entity scoping for each? Does it
correctly identify that the SAR product likely needs cross-domain references?

**Scenario D2 — Masking strategy for PII (Marcus, Data Steward)**
> "The Customer 360 product exposes Date of Birth, Tax Identification Number,
> residential address, and phone number. The analytics team needs age-based
> segmentation but not exact dates. Compliance says TINs must never appear in
> any analytics product. What masking strategies should I use?"

Evaluate: Does the agent provide specific masking recommendations aligned with the
spec's available strategies? Does it recommend `year-only` for DOB, `hash` or `redact`
for TIN, `truncate` for address (postcode prefix)? Does it explain that masking is
product-scoped and that the same entity may have different masking in different
products?

**Scenario D3 — ODPS manifest generation (Aisha, Data Product Owner)**
> "Take the Transaction Risk Summary product from our Financial Crime domain and
> generate an ODPS manifest. I want to publish it to our data marketplace. Fill
> in as much as you can from the MD-DDL declaration and tell me what I need to
> provide separately."

Evaluate: Does the agent load ODPS Alignment skill? Does it read the product
declaration and map fields correctly? Does it use the data quality dimension
inference rules (mapping `not_null` → completeness, `check` → validity, etc.)
rather than generic placeholders? Does it produce valid ODPS YAML with the right
structure? Does it clearly separate automatically-mapped fields from TODOs?

**Scenario D4 — Cross-domain product design (Aisha, Data Product Owner)**
> "I need a Customer 360 product that spans three domains: Customer, Financial
> Crime, and Product Catalogue. The Customer domain owns Party and Account, Financial
> Crime owns Transaction and Alert, Product Catalogue owns Product and Pricing.
> How do I design a consumer-aligned product that crosses these domain boundaries?"

Evaluate: Does the agent understand cross-domain references in consumer-aligned
products? Does it correctly use the `cross_domain` field and explain that owning
domains retain governance authority? Does it identify the governance complexity of
spanning 3 domains (different retention, classification, masking per domain)? Does
it advise on which domain should own the product declaration? Is the spec's
cross-domain mechanism expressive enough for this scenario?

**Scenario D5 — Product lifecycle: retiring and versioning products (Aisha, Data Product Owner)**
> "Our Source Feed product was published 18 months ago. We've since added 5 new
> entities to the domain and changed the masking strategy on two existing ones.
> Two consumer teams have built pipelines on the old product. How do I version
> the product and manage the transition?"

Evaluate: Does the standard support product versioning? Does the agent have
guidance for product lifecycle management (draft → active → deprecated → retired)?
Can the spec express breaking vs non-breaking changes? Is there a mechanism for
communicating changes to downstream consumers? Is this a gap in the spec or agents?

---

### Agent Governance — Standards Conformance and Compliance Assurance

**Scenario R1 — Multi-jurisdiction compliance audit (Priya, Data Risk Manager)**
> "Audit the Financial Crime domain against APRA CPS 234, RBNZ BS11, and FATF
> Recommendations. We're an Australian bank with a New Zealand subsidiary. I need
> findings in severity order with specific regulatory references."

Evaluate: Does the agent load Compliance Audit then Regulatory Compliance skills?
Does it load the correct regulator files (apra.md, rbnz.md, fatf.md)? Does it
produce a structured gap report with severity levels? Does it cite specific
regulatory provisions, not generic best practice? Does it identify where AU and
NZ requirements diverge?

**Scenario R2 — Product governance review (Marcus, Data Steward)**
> "Review the governance posture of all three Financial Crime data products. The
> analytics product exposes PII with masking, the source feed has raw data, and
> the canonical product is domain-aligned. Are the governance overrides
> appropriate for each? Are there gaps?"

Evaluate: Does the agent use the Level 4 Product Governance audit protocol? Does
it understand the relationship between domain defaults and product overrides? Does
it cross-reference masking strategies against each entity's PII characteristics
using the masking adequacy protocol? Does it flag if a source-aligned product with
raw PII has insufficient governance? Does the Governance → Architect handoff
work correctly for any gaps found?

**Scenario R3 — Remediation with structural implications (Priya, Data Risk Manager)**
> "Your audit found that the Transaction entity is missing a data residency
> requirement — APRA requires certain transaction data to stay onshore. Fix it."

Evaluate: Does the agent correctly distinguish between metadata changes it can make
(adding `data_residency` to governance) and structural changes that need Agent Ontology
(if a new entity or attribute is implied)? Does it show before/after YAML? Does it
defer structural work explicitly?

**Scenario R4 — HIPAA compliance for healthcare domain (Dr. Kowalski, Healthcare Data Architect)**
> "Audit the Patient Care domain against HIPAA Privacy Rule and HIPAA Security
> Rule. We have PHI (protected health information) in Patient, Encounter, and
> Condition entities. We need to ensure de-identification meets Safe Harbor
> requirements."

Evaluate: Does the agent have a HIPAA regulator file, or is this a gap in the
regulatory-compliance skill? Can the governance YAML schema express PHI (vs PII)
and HIPAA-specific concepts like de-identification method (Safe Harbor vs Expert
Determination)? Does the agent know when to defer to legal for HIPAA
interpretation? Is the regulatory-compliance skill US-healthcare-aware or solely
focused on financial services regulators?

---

### Cross-Agent Workflows

These scenarios test end-to-end journeys that span multiple agents. Evaluate the
full workflow, including handoff quality and context continuity.

**Scenario X1 — Full lifecycle: model → product → generate → audit (Aisha + James + Priya)**

Simulate this four-step journey:

1. Aisha asks Agent Architect to design a new consumer-aligned product from
   the Financial Crime domain for the fraud analytics team
2. Aisha's product needs a `schema_type: dimensional` — she hands off to James
3. James asks Agent Artifact to generate a Snowflake star schema scoped to the product
4. Priya asks Agent Governance to audit the product's governance posture

Evaluate: Do the handoff scripts between agents produce enough context for the
receiving agent? Does the product declaration serve as a clean input contract for
Agent Artifact? Does Agent Governance's Level 4 audit cover the product that was
just designed? Would this workflow feel like a coherent pipeline or a series of
disconnected interactions?

**Scenario X2 — Compliance gap triggers model change (Priya → Sarah → Aisha)**

Simulate this three-step journey:

1. Agent Governance audits the Financial Crime domain and identifies that the
   Party entity needs a `consent_basis` attribute to satisfy GDPR's lawful basis
   requirement
2. The gap is flagged as structural — Agent Governance defers to Agent Ontology
3. Sarah adds the attribute via Agent Ontology, which triggers a review of all
   data products that expose Party

Evaluate: Does Agent Governance produce a clear structural-change recommendation
that Agent Ontology can act on? Does Agent Ontology's narrow-scope shortcut work
for adding a single attribute? After the model change, does Agent Architect
know to check whether its products need masking updates for the new attribute?
Is the chain of custody clear — who changed what and why?

**Scenario X3 — Source system onboarding → transformation → product (Tomás → Aisha)**

Simulate this journey:

1. Tomás asks Agent Ontology to declare a new source system (Shopify POS) and map
   its tables to existing Customer domain entities
2. After source mapping is complete, Aisha asks Agent Architect whether the
   new source changes any existing products

Evaluate: Does Agent Ontology handle source file creation and transformation
mapping? Does the spec's transformation vocabulary cover the mappings Tomás needs
(direct, concatenate, lookup, conditional)? After source onboarding, is there a
mechanism to propagate changes to data products? Is the source → canonical →
product lineage traceable?

---

## Scoring Rubric

Score each scenario on five dimensions. Use a 1–5 scale.

### Agent Effectiveness (per scenario)

Dimension | 1 (Poor) | 3 (Adequate) | 5 (Excellent)
--- | --- | --- | ---
**Skill Loading** | Agent would not load the relevant skill | Loads the right skill but may miss secondary skills | Loads all relevant skills including cross-references
**Behaviour Mode** | Wrong mode or no clear mode transition | Correct mode but transition is not explicit | Natural mode progression with clear transition phrases
**Output Quality** | Output would be incorrect or incomplete | Output is correct but generic | Output is correct, specific, and tailored to the persona's context
**Boundary Respect** | Agent attempts work outside its lifecycle stage | Recognises boundary but handoff is unclear | Clean boundary recognition with specific handoff guidance
**Persona Fit** | Agent frustrates the persona or ignores their expertise level | Agent serves the persona but doesn't adapt to their style | Agent matches the persona's expertise, communication style, and priorities

### Standard Effectiveness (per scenario)

Dimension | 1 (Poor) | 3 (Adequate) | 5 (Excellent)
--- | --- | --- | ---
**Expressiveness** | The standard cannot express what the persona needs | Can express it but requires workarounds | Naturally supports the persona's requirement
**Completeness** | Key concepts are missing from the spec | Most concepts covered but gaps exist | All concepts needed for this scenario are specified
**Learnability** | Persona would struggle to understand the standard's approach | Concepts are clear but relationships between them are not | Standard is intuitive for this persona's background

### Cross-Agent Workflow Effectiveness (per workflow scenario)

Dimension | 1 (Poor) | 3 (Adequate) | 5 (Excellent)
--- | --- | --- | ---
**Handoff Clarity** | No handoff guidance; user must figure out next agent alone | Handoff script exists but context is insufficient | Handoff includes specific context and the receiving agent can continue without re-explanation
**Context Continuity** | Receiving agent has no context from previous step | Receiving agent gets partial context; some re-explanation needed | The artifact from the previous step (product declaration, gap report) serves as a complete input contract
**End-to-End Coherence** | Workflow feels like disconnected tool interactions | Workflow is functional but transitions are awkward | Workflow feels like a natural pipeline with clear stage progression

---

## Standard Critique Dimensions

Beyond individual scenarios, evaluate the standard holistically against these
dimensions. Draw on findings from all persona interactions.

### For each dimension, provide

- A rating (Strong / Adequate / Needs Work)
- Evidence from scenarios
- Specific improvement suggestions if applicable

---

### 1. Conceptual Completeness

Does MD-DDL cover the full lifecycle from discovery through to publication?
Are there stages where the practitioner falls off a cliff — the standard has
nothing to say and the agent has nothing to offer?

Specifically assess: discovery → entity design → relationships → events →
sources → transformations → data products → physical generation → external publication.

Pay particular attention to the sources and transformations stages — these are
specified in the standard but receive less agent support than other stages. Are there
agent skills missing for source onboarding and transformation authoring?

### 2. Learning Curve

How much does each persona need to learn before being productive? Is the
investment justified by the value? Consider:

- Sarah (Data Modeller) — already knows ER/UML. How much does MD-DDL add vs substitute?
- James (Data Engineer) — cares about physical output. Is the conceptual layer overhead or valuable?
- Marcus (Data Steward) — not technical. Can he contribute meaningfully through the agents?
- Priya (Data Risk Manager) — needs to review, not author. Is the governance metadata readable?
- Aisha (Data Product Owner) — product-oriented. Does the data product abstraction make sense?
- Dr. Kowalski (Healthcare Architect) — deep domain expertise, different industry.
  Does MD-DDL translate or alienate?
- Tomás (Integration Engineer) — source-system focused. Does the source/transform
  layer match his workflow?
- Kenji (Domain Review Lead) — expert user. Does MD-DDL support systematic review?

### 3. Agent Handoff Friction

When a task crosses agent boundaries (e.g., designing a product that reveals a
missing entity), how smooth is the handoff? Consider:

- Does the user understand why they need to switch agents?
- Does the receiving agent have enough context to continue without re-explaining?
- Is the handoff pattern consistent across all agent-to-agent transitions?
- Would a persona find the multi-agent pattern natural or frustrating?
- Evaluate the specific handoff chains tested in scenarios X1, X2, and X3.

### 4. Governance Integration

Is governance metadata a natural part of the modelling workflow, or does it feel
bolted on? Consider:

- When does governance first appear in the modelling process?
- Is the governance model expressive enough for multi-jurisdiction scenarios?
- Do governance overrides at the product level make sense to a steward?
- Can a risk manager audit governance without understanding the full data model?
- Does the governance model extend naturally to non-financial-services industries
  (healthcare PHI, telecom subscriber data)?

### 5. Industry Alignment

Does the standard help or hinder alignment with industry standards? Consider:

- Is the Reference column in entity tables sufficient for standards mapping?
- Does the ODPS alignment skill produce genuinely useful output, including inferred
  data quality dimensions?
- Which industry standards are well-supported vs. missing? Evaluate coverage of:
  BIAN, FHIR, TM Forum SID, ISO 20022, ACORD, ODPS. Note any that practitioners
  would expect but are absent.
- Does the standards reconciliation protocol handle real alignment conflicts?

### 6. Scalability

How does the standard handle complexity? Consider:

- 5 entities vs 50 entities vs 200 entities — does the domain file format scale?
- Cross-domain references in data products — does the mechanism handle real-world
  scenarios where 10+ domains interact?
- Does the two-layer pattern (summary table in domain file + detail files) add
  value or just administrative overhead?
- Multiple source systems mapping to a single domain — does the source layer scale?

### 7. Physical Generation Gap

The gap between conceptual model and physical output is where practitioners most
often lose confidence. Evaluate:

- Does Agent Artifact have enough conceptual context to make correct physical decisions?
- Are the mapping rules (existence → dimension type, mutability → SCD type) clear enough?
- Do the dialect reference files (Snowflake, Databricks, PostgreSQL) provide sufficient
  platform-specific guidance?
- Do the inheritance DDL templates produce correct output for all three strategies?
- When generation produces unexpected output, can the practitioner debug it
  (e.g., via a decision log)?
- Are there physical patterns that data engineers commonly need but MD-DDL cannot express?
- Is knowledge graph generation (Cypher DDL) as mature as relational generation?

### 8. Source and Transformation Coverage

The source and transformation layers (spec sections 7–8) bridge operational systems
and the canonical model. Evaluate:

- Is the source file format expressive enough for real-world source system diversity?
- Does the transformation vocabulary cover common ETL patterns (direct mapping,
  concatenation, lookup, conditional, aggregation, type casting)?
- Is there an agent skill gap for source onboarding and transformation authoring?
- Can the source layer express change data capture models (CDC, full snapshot,
  delta append)?
- Is lineage from source field → transformation → canonical attribute traceable?

### 9. Model Evolution and Lifecycle

Real domains change over time. Evaluate:

- Does the standard support domain versioning and evolution?
- Can a modeller extend a domain without breaking downstream consumers?
- Is there guidance for deprecating entities, attributes, or relationships?
- Do data products have lifecycle states (draft, active, deprecated, retired)?
- When a model change affects a published product, is the impact traceable?

---

## Report Format

Produce findings in this structure. Be specific — cite agent prompts, skill paths,
and spec sections when referencing evidence.

```markdown
## MD-DDL Agent & Standard Effectiveness Report — [date]
**Spec version evaluated:** [version from 1-Foundation.md]
**Agents evaluated:** Guide, Ontology, Artifact, Data Product, Regulation

---

### What This Evaluation Cannot Assess
[Explicit list of aspects outside AI's competence for this evaluation. Include:
domain accuracy of examples, regulatory fact correctness, real-world stakeholder
reactions, runtime agent behaviour, and any industry-specific expertise gaps.
Be honest about your limits — this section is more valuable than inflated scores.]

---

### Executive Summary
[3-5 sentences: overall effectiveness, strongest agent, weakest area, top priority
for improvement]

---

### Agent Scorecards

#### Agent Ontology
| Scenario | Skill Loading | Behaviour Mode | Output Quality | Boundary Respect | Persona Fit | Avg |
| --- | --- | --- | --- | --- | --- | --- |
| O1 — New domain | /5 | /5 | /5 | /5 | /5 | /5 |
| O2 — Entity/enum/attribute | /5 | /5 | /5 | /5 | /5 | /5 |
| O3 — Standards alignment | /5 | /5 | /5 | /5 | /5 | /5 |
| O4 — Healthcare FHIR | /5 | /5 | /5 | /5 | /5 | /5 |
| O5 — Domain review | /5 | /5 | /5 | /5 | /5 | /5 |
| O6 — Model evolution | /5 | /5 | /5 | /5 | /5 | /5 |
| **Average** | | | | | | **/5** |

**Strengths:** [what works well]
**Gaps:** [what's missing or weak]
**Persona feedback (Sarah):** [what Sarah would say]
**Persona feedback (Marcus):** [what Marcus would say]
**Persona feedback (Dr. Kowalski):** [what Dr. Kowalski would say]
**Persona feedback (Kenji):** [what Kenji would say]

#### Agent Artifact
| Scenario | Skill Loading | Behaviour Mode | Output Quality | Boundary Respect | Persona Fit | Avg |
| --- | --- | --- | --- | --- | --- | --- |
| A1 — Dimensional Snowflake | /5 | /5 | /5 | /5 | /5 | /5 |
| A2 — Product-scoped wide-column | /5 | /5 | /5 | /5 | /5 | /5 |
| A3 — Inheritance DDL | /5 | /5 | /5 | /5 | /5 | /5 |
| A4 — Knowledge graph | /5 | /5 | /5 | /5 | /5 | /5 |
| A5 — JSON Schema contracts | /5 | /5 | /5 | /5 | /5 | /5 |
| **Average** | | | | | | **/5** |

**Strengths:** [what works well]
**Gaps:** [what's missing or weak]
**Persona feedback (James):** [what James would say]
**Persona feedback (Sarah):** [what Sarah would say]

#### Agent Architect
| Scenario | Skill Loading | Behaviour Mode | Output Quality | Boundary Respect | Persona Fit | Avg |
| --- | --- | --- | --- | --- | --- | --- |
| D1 — Multi-consumer design | /5 | /5 | /5 | /5 | /5 | /5 |
| D2 — PII masking | /5 | /5 | /5 | /5 | /5 | /5 |
| D3 — ODPS manifest | /5 | /5 | /5 | /5 | /5 | /5 |
| D4 — Cross-domain product | /5 | /5 | /5 | /5 | /5 | /5 |
| D5 — Product versioning | /5 | /5 | /5 | /5 | /5 | /5 |
| **Average** | | | | | | **/5** |

**Strengths:** [what works well]
**Gaps:** [what's missing or weak]
**Persona feedback (Aisha):** [what Aisha would say]
**Persona feedback (Marcus):** [what Marcus would say]

#### Agent Governance
| Scenario | Skill Loading | Behaviour Mode | Output Quality | Boundary Respect | Persona Fit | Avg |
| --- | --- | --- | --- | --- | --- | --- |
| R1 — Multi-jurisdiction audit | /5 | /5 | /5 | /5 | /5 | /5 |
| R2 — Product governance | /5 | /5 | /5 | /5 | /5 | /5 |
| R3 — Remediation | /5 | /5 | /5 | /5 | /5 | /5 |
| R4 — HIPAA healthcare | /5 | /5 | /5 | /5 | /5 | /5 |
| **Average** | | | | | | **/5** |

**Strengths:** [what works well]
**Gaps:** [what's missing or weak]
**Persona feedback (Priya):** [what Priya would say]
**Persona feedback (Dr. Kowalski):** [what Dr. Kowalski would say]
**Persona feedback (Marcus):** [what Marcus would say]

---

### Cross-Agent Workflow Scorecards

| Scenario | Handoff Clarity | Context Continuity | End-to-End Coherence | Avg |
| --- | --- | --- | --- | --- |
| X1 — Full lifecycle | /5 | /5 | /5 | /5 |
| X2 — Compliance → model change | /5 | /5 | /5 | /5 |
| X3 — Source onboarding → product | /5 | /5 | /5 | /5 |
| **Average** | | | | **/5** |

**Strongest workflow:** [which X scenario worked best and why]
**Weakest workflow:** [which X scenario had the most friction and why]
**Handoff pattern assessment:** [are handoffs consistent across agent pairs?]

---

### Standard Scorecards

| Scenario | Expressiveness | Completeness | Learnability | Avg |
| --- | --- | --- | --- | --- |
| O1 | /5 | /5 | /5 | /5 |
| O2 | /5 | /5 | /5 | /5 |
| O3 | /5 | /5 | /5 | /5 |
| O4 | /5 | /5 | /5 | /5 |
| O5 | /5 | /5 | /5 | /5 |
| O6 | /5 | /5 | /5 | /5 |
| A1 | /5 | /5 | /5 | /5 |
| A2 | /5 | /5 | /5 | /5 |
| A3 | /5 | /5 | /5 | /5 |
| A4 | /5 | /5 | /5 | /5 |
| A5 | /5 | /5 | /5 | /5 |
| D1 | /5 | /5 | /5 | /5 |
| D2 | /5 | /5 | /5 | /5 |
| D3 | /5 | /5 | /5 | /5 |
| D4 | /5 | /5 | /5 | /5 |
| D5 | /5 | /5 | /5 | /5 |
| R1 | /5 | /5 | /5 | /5 |
| R2 | /5 | /5 | /5 | /5 |
| R3 | /5 | /5 | /5 | /5 |
| R4 | /5 | /5 | /5 | /5 |
| **Average** | | | | **/5** |

---

### Standard Critique

#### 1. Conceptual Completeness — [Strong / Adequate / Needs Work]
[Evidence and analysis]

#### 2. Learning Curve — [Strong / Adequate / Needs Work]
[Evidence and analysis]

#### 3. Agent Handoff Friction — [Strong / Adequate / Needs Work]
[Evidence and analysis]

#### 4. Governance Integration — [Strong / Adequate / Needs Work]
[Evidence and analysis]

#### 5. Industry Alignment — [Strong / Adequate / Needs Work]
[Evidence and analysis]

#### 6. Scalability — [Strong / Adequate / Needs Work]
[Evidence and analysis]

#### 7. Physical Generation Gap — [Strong / Adequate / Needs Work]
[Evidence and analysis]

#### 8. Source and Transformation Coverage — [Strong / Adequate / Needs Work]
[Evidence and analysis]

#### 9. Model Evolution and Lifecycle — [Strong / Adequate / Needs Work]
[Evidence and analysis]

---

### Stakeholder Verdict

For each persona, summarise: would they adopt MD-DDL?

| Persona | Would Adopt? | Why / Why Not | Key Improvement Needed |
| --- | --- | --- | --- |
| Sarah (Modeller) | Yes/Maybe/No | [reason] | [specific improvement] |
| Marcus (Steward) | Yes/Maybe/No | [reason] | [specific improvement] |
| Priya (Risk Manager) | Yes/Maybe/No | [reason] | [specific improvement] |
| James (Engineer) | Yes/Maybe/No | [reason] | [specific improvement] |
| Aisha (Product Owner) | Yes/Maybe/No | [reason] | [specific improvement] |
| Dr. Kowalski (Healthcare) | Yes/Maybe/No | [reason] | [specific improvement] |
| Tomás (Integration) | Yes/Maybe/No | [reason] | [specific improvement] |
| Kenji (Review Lead) | Yes/Maybe/No | [reason] | [specific improvement] |

---

### Comparison with Previous Evaluation

If a previous `review.md` exists, compare scores and note:
- Which gaps from the previous evaluation have been addressed
- Which gaps remain open
- Any new gaps discovered in this evaluation that were not previously identified
- Net score movement per agent and per standard dimension

---

### Priority Recommendations

#### Fix Existing (before next version)
1. [specific finding → specific fix]
2. ...

#### Extend Capability (next version scope)
1. [gap identified → proposed extension]
2. ...

#### Spec Improvements (standard critique → spec change)
1. [critique finding → proposed spec enhancement]
2. ...
```

---

## What this evaluation is not

- Not an exhaustive test suite. The scenarios test critical paths and cross-agent
  workflows, not every edge case.
- Not a live agent test. You are evaluating prompt architecture and skill
  completeness, not runtime behaviour.
- Not a comparison to other standards. Evaluate MD-DDL on its own merits against
  stakeholder needs.
- Not a certification. The adoption verdicts are informed opinions, not guarantees.
