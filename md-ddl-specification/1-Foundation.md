# **MD‑DDL Specification (Draft 0.7)**  

*A Markdown‑native Data Definition Language for human-AI collaboration.*

---

## **Overview**

MD‑DDL is a **Markdown‑first**, **AI‑friendly** standard for defining domains, entities, attributes, enums, relationships, events, and source mappings. It is designed to be readable by humans, generatable by AI, and compilable into:

- Data catalogs
- Knowledge graphs
- Data product definitions
- Schemas and technical artifacts
- ETL/ELT logic and source-to-domain lineage

MD‑DDL uses Markdown structure as its primary syntax, with YAML or JSON blocks for structured definitions and Mermaid or PlantUML for diagramming. Structural consistency is enforced by the compiler and supported by companion AI agents.

---

## **Core Principles**

1. **Source of Truth**  
   Every concept is defined once in the domain, in one canonical location. A design choice is whether to follow Domain Driven Design (DDD) and allow domain concepts to be mutually exclusive or not.

   This principle extends to source mappings. A source transform file is the single authoritative definition of how a source system's fields map to canonical domain attributes. Canonical entities contain no source references — they define meaning, not origin. Canonical data products replace the concept of Systems of Record: source systems are systems of change whose outputs are governed by the canonical model.

2. **Markdown‑Native**  
   Headings define structure; prose defines meaning.

3. **AI‑Friendly**  
   No redundant fields. No manually maintained lists. Minimal boilerplate.

4. **Compiler‑Driven**  
   The compiler infers domain membership, indexes entities, and validates relationships.

5. **Graph‑Powered**  
   The knowledge graph acts as the semantic runtime for reasoning, lineage, and governance.

6. **Natural‑Language Naming**  
   Entities, attributes, and relationships use human‑readable names rather than code‑style casing.

---

## **Document Structure**

MD‑DDL is composed of several logical components:

- [Domains](./2-Domains.md)
- [Entities](./3-Entities.md)
- [Enumerations](./4-Enumerations.md)
- [Relationships](./5.Relationships.md)
- [Events](./6.Events.md)
- [Sources](./7-Sources.md)
- [Transformations](./8-Transformations.md)

MD‑DDL uses a **two‑layer structure** for Entities, Enums, Relationships, and Events:

1. A **summary definition** in the domain file  
2. A **detailed definition** in a separate file  

This structure supports both human readability and AI context management.

Example domain layout:

```shell
domains/customer/domain.md
domains/customer/entities/customer.md
domains/customer/entities/customer-preference.md
domains/customer/relationships/customer-has-preferences.md
domains/customer/diagrams/overview.md
```

Example source layout:

```shell
sources/salesforce/manifest.md
sources/salesforce/transforms/customer.md
sources/salesforce/transforms/contact-address.md
sources/sap/manifest.md
sources/sap/transforms/customer.md
```

Domain files and source files are sibling structures at the project level. Domain files define meaning. Source files define origin and transformation logic. Neither references the other's internals — they are linked only through the `target: Entity · Attribute` notation in transform files and the Canonical Feeds table in the source manifest.

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

#### **Compiler Simplicity**

- The compiler knows exactly where to find summaries and details.  
- Both layers are merged into a unified conceptual, logical, and physical model.

#### Detail File Flexibility

Detail files are not restricted to a single entity. Authors may organise detail files to suit their modelling style — for example, one entity per file, one file per subdomain cluster, or a file combining an entity with its enumerations and originating relationships.
The only structural requirement is that every detail file begins with a level‑1 heading naming the domain (with a link back to the domain file), followed by one or more level‑2 section headings (## Entities, ## Enums, ## Relationships, ## Events) containing the relevant definitions.

Source transform files follow the same two-layer pattern but are scoped to a source system rather than a domain. They begin with a level-1 heading linking back to the source manifest, followed by level-2 headings for each canonical entity being populated.

---
