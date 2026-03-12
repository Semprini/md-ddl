# MD‑DDL Specification (Draft 0.9.0)

*A Markdown‑native Data Definition Language for human-AI collaboration.*

---

## **Overview**

MD‑DDL is a **Markdown‑first**, **AI‑friendly** standard for defining domains, entities, attributes, enums, relationships, events, source mappings, and data products. It is designed to be readable by humans, generatable by AI, and transformable into:

- Data catalogs
- Knowledge graphs
- Data product definitions
- Schemas and technical artifacts (DDL, JSON Schema, Parquet contracts)
- ETL/ELT logic and source-to-domain lineage

MD‑DDL uses Markdown structure as its primary syntax, with YAML or JSON blocks for structured definitions and Mermaid or PlantUML for diagramming. Structural consistency is enforced by AI agents that validate, generate, and maintain model artifacts.

---

## **Core Principles**

1. **Source of Truth**  
   Every concept is defined once in the domain, in one canonical location. A design choice is whether to follow Domain Driven Design (DDD) and allow domain concepts to be mutually exclusive or not.

   This principle extends to source mappings. Source definitions and transform files are self-contained within each domain under `sources/<system>/`. Canonical entities contain no source references — they define meaning, not origin. Canonical data products replace the concept of Systems of Record: source systems are systems of change whose outputs are governed by the canonical model.

2. **Markdown‑Native**  
   Headings define structure; prose defines meaning.

3. **AI‑Friendly**  
   No redundant fields. No manually maintained lists. Minimal boilerplate.

4. **Agent‑Driven**  
   AI agents infer domain membership, index entities, validate relationships, and generate physical artifacts from the model.

5. **Graph‑Powered**  
   The knowledge graph acts as the semantic runtime for reasoning, lineage, and governance.

6. **Natural‑Language Naming**
   Entities, attributes, and relationships use human‑readable names rather than code‑style casing.

7. **Adoption is Incremental**
   MD-DDL supports incremental adoption. Organisations can begin by documenting their existing data landscape — dimensional models, canonical models, ETL pipelines, governance metadata — and progressively evolve toward declarative, AI-generated artifacts. The `baselines/` folder captures existing state; the adoption maturity model tracks the journey; the canonical model is the destination. See [Section 10 — Adoption](./10-Adoption.md) for the full maturity model and adoption workflow.

---

## **Document Structure**

MD‑DDL is composed of several logical components:

- [Domains](./2-Domains.md)
- [Entities](./3-Entities.md)
- [Enumerations](./4-Enumerations.md)
- [Relationships](./5-Relationships.md)
- [Events](./6-Events.md)
- [Sources](./7-Sources.md)
- [Transformations](./8-Transformations.md)
- [Data Products](./9-Data-Products.md)
- [Adoption](./10-Adoption.md)

MD‑DDL uses a **two‑layer structure** for Entities, Enums, Relationships, Events, and Data Products:

1. A **summary definition** in the domain file
2. A **detailed definition** in a separate file

During adoption (see [Section 10](./10-Adoption.md)), a transitional layer may also exist:

- **Layer 0 — Baselines** (existing state documentation) — transitional; captured in `baselines/` subfolders within the domain

Baselines document what exists today. They are not part of the canonical model and are never used for generation. They are superseded as the domain advances through adoption maturity levels.

This structure supports both human readability and AI context management.

Example domain layout:

```shell
domains/customer/domain.md
domains/customer/entities/customer.md
domains/customer/entities/customer-preference.md
domains/customer/relationships/customer-has-preferences.md
domains/customer/products/analytics.md
domains/customer/diagrams/overview.md
```

Example source layout:

```shell
Financial Crime/sources/salesforce-crm/source.md
Financial Crime/sources/salesforce-crm/transforms/table_account.md
Financial Crime/sources/salesforce-crm/transforms/table_contact_point.md
Financial Crime/sources/sap-fraud-management/source.md
Financial Crime/sources/temenos-payment/source.md
```

Domain files and source files are co-located at the domain level. Domain files define meaning. Source folders define operational origin and mapping logic for that specific domain context.

---

### **Two‑Layer Structure**

#### **AI Context Management**

- The domain file provides a compact summary of all conceptual objects.  
- AI agents load only the summaries initially.  
- When deeper context is needed, they follow the `detail:` link to load the full definition.

This mirrors Anthropic’s "skills" concept but improves on it by:

- Centralising summaries
- Avoiding duplication
- Ensuring humans can browse the domain easily

#### **Human Readability**

- The domain file becomes a clean, navigable table of contents.  
- Detail files remain focused, concise, and free from clutter.

#### **Structural Predictability**

- AI agents know exactly where to find summaries and details.  
- Both layers are merged into a unified conceptual, logical, and physical model.

#### Detail File Flexibility

Detail files are not restricted to a single entity. Authors may organise detail files to suit their modelling style — for example, one entity per file, one file per subdomain cluster, or a file combining an entity with its enumerations and originating relationships.
The only structural requirement is that every detail file begins with a level‑1 heading naming the domain (with a link back to the domain file), followed by one or more level‑2 section headings (## Entities, ## Enums, ## Relationships, ## Events, ## Data Products) containing the relevant definitions.

Source transform files follow the same two-layer pattern but are scoped to a source system within a domain context. They begin with a level-1 heading linking back to `./source.md` in the same source folder, followed by a level-2 heading for the source table and optional level-3 rule sections for non-direct mappings.

### Include Directive

Agent prompt files and skill reference stubs use an `{{INCLUDE: <path>}}` directive to inject content from other files at prompt-load time. This is processed by the AI platform (e.g. VS Code Copilot custom agents, Claude Code) before the prompt reaches the model — it is not part of the MD-DDL modelling language itself.

The directive appears on its own line and takes a file-relative path:

```text
{{INCLUDE: ../../../md-ddl-specification/3-Entities.md}}
```

Paths must be relative to the file containing the directive. Do not use workspace-root paths, as MD-DDL repositories are commonly consumed as submodules where absolute paths break.

This mechanism enables the spec reference stub pattern: skill reference files contain a brief description and an `{{INCLUDE}}` pointing to the canonical spec section, so that spec updates propagate automatically without duplicating content across agent files.

---

## **Validation Model**

MD-DDL uses a two-tier validation model: **mechanical pre-flight checks** and **agent-driven quality review**. These tiers are deliberately separate because different categories of problem require different kinds of intelligence to detect.

### Why Not a Traditional Linter

MD-DDL is an AI-native standard. The primary consumer of an MD-DDL model is an AI agent that already understands intent, domain context, and organisational conventions — capabilities that no rule-based linter can match. Applying rigid pass/fail enforcement above the syntax level would:

- Reject legitimate organisational vocabulary differences (e.g., `phi` instead of `pii`) that agents understand and can work with
- Suppress feedback that drives spec evolution — when organisations adapt MD-DDL to their context, that signal is valuable
- Produce false positives for intentional exceptions (governance inheritance, minimal reference domains) that require domain context to evaluate correctly

Traditional linters assume the checker is smarter than the thing being checked. For MD-DDL, the inverse is true.

### Validation Levels

Five categories of check exist across the MD-DDL model. Only Level 1 benefits from mechanical tooling:

Level | Category | Example | Mechanically checked?
--- | --- | --- | ---
1 | Syntax | YAML parses, Mermaid renders, markdown links resolve | Yes — broken syntax silently corrupts agent interpretation with no wiggle room
2 | Structure | Required sections present, required YAML keys present | Partially — legitimate exceptions exist; structural checks need domain context to avoid false positives
3 | Convention | Naming patterns, column order, heading hierarchy | No — organisational vocabulary differences are signal, not errors
4 | Quality | Governance completeness, relationship coverage, event payloads | No — this is judgment; agents handle it through domain-review and compliance-audit
5 | Domain fitness | Is this the right model for the business? | Never — requires human domain expertise by definition

**The split:** Level 1 gets mechanical pre-flight checks. Levels 2–5 stay with agents and humans, where context and judgment live.

### Pre-Flight Check Scope

The following checks are the complete set of mechanical validation that MD-DDL endorses. No additional checks should be added without a spec version bump.

Check | What it validates | Why it is mechanical
--- | --- | ---
YAML syntax | All YAML code blocks parse without syntax errors | A YAML parse error silently corrupts agent interpretation of every attribute in the block
Mermaid syntax | All Mermaid code blocks use valid diagram syntax | A Mermaid syntax error breaks every rendering of the domain or entity diagram
Internal link integrity | All markdown links (`[text](path)`) resolve to existing files or headings | Dead links break navigation for both humans and agents
Entity reference consistency | Entity names in relationships, events, products, and source mappings match an entity defined in the domain | A typo in an entity name creates a silent reference to nothing
Domain version field | The `version:` key exists in domain metadata | Versionless domains cannot participate in maturity tracking or change management

**What is explicitly not checked mechanically:**

- Presence or absence of optional YAML keys (mutability, temporal, governance fields)
- Naming conventions or vocabulary choices
- Governance metadata completeness or correctness
- Relationship granularity or cardinality appropriateness
- Event payload structure completeness
- Standards alignment accuracy
- Any modelling judgment

### Pre-Flight Check Tool Interface

Any tool implementing pre-flight checks must conform to this interface:

- **Input:** a domain folder path
- **Output:** a list of findings, each with file path, line number, check name, and message
- **Exit behaviour:** report all findings; do not stop on first error
- **Severity:** all findings are a single severity ("pre-flight failure") — there is no warning/error distinction because all checks are binary
- **Configuration:** none — the checks are fixed and minimal; there are no rules to enable or disable

### Agent-Driven Quality Review

Everything above Level 1 is the responsibility of agents. Agent Ontology's domain-review skill, Agent Governance's compliance-audit skill, and the structured review prompts in `.github/` handle structural, convention, quality, and domain-fitness concerns. They understand context and intent. They flag deviations as observations, not errors.

When an agent encounters an organisational vocabulary deviation — a field named `phi` instead of `pii`, `data_class` instead of `classification` — the correct response is to note it as a **potential spec vocabulary gap** and work with it, not reject the file.

---

...next: [Domains](2-Domains.md)
