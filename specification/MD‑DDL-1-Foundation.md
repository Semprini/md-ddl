# **MD‑DDL Specification (Draft 0.2)**  
*A Markdown‑native Data Definition Language for human‑AI collaboration.*

---

# **Overview**

MD‑DDL is a **Markdown‑first**, **AI‑friendly** standard for defining logical data models, domains, entities, attributes, enums, and relationships. It is designed to be readable by humans, generatable by AI, and compilable into:

- Data Catalog
- Knowledge graphs
- Data product definitions
- Schemas & Technical Artifacts

MD‑DDL uses Markdown structure as the primary syntax, YAML or JSON blocks for structured definitions and Mermaid, PlantUML for diagramming. Consistency checks of the structure is provided by the compiler and companion AI.

---

# **Core Principles**

1. **Single Source of Truth**
   Every concept is defined once, in one place.

2. **Markdown‑Native**
   Headings define structure; prose defines meaning.

3. **AI‑Friendly**
   No redundant fields, no lists that must be maintained manually.

4. **Compiler‑Driven**
   The compiler infers domain membership, indexes entities, and validates relationships.

5. **Graph‑Powered**
   The knowledge graph is the semantic runtime for reasoning, lineage, and governance.

6. **Natural‑Language Naming**  
   Entity names, attribute names, and relationship names use human language, not code casing.

---

# **Document Structure**

MD‑DDL is composed of several logical components: 
- [Domains](MD-DDL-2-Domains.md)
- [Entities](MD-DDL-3-Entities.md)
- [Enumerations](MD-DDL-4-Enumerations.md)
- [Relationships](MD-DDL-5-Relationships.md)
- [Events](MD-DDL-6-Events.md)

These components may be defined together or separately across multiple files and include diagrams in Mermaid or PLantUML format to give context and useful views. This separation is intentional: it supports both human readability and AI context management. Similar to Anthropic's concept of "skills" MD‑DDL allows AI systems to load only the relevant parts of the model rather than the entire knowledge base at once.

## Multi‑File Domains
A domain is a logical construct, not a single file.
A domain may be defined across one or more Markdown files, and the compiler assembles the complete domain model by merging all files that begin with the same level‑1 heading.

For example, the following files all contribute to the Customer domain:

```Code
domains/customer/domain.md
domains/customer/entities/customer.md
domains/customer/entities/customer-preference.md
domains/customer/relationships/customer-has-preferences.md
domains/customer/diagrams/overview.md
```

Each file begins with:
```markdown
# Customer
```

## Sample Structure

Below is an example of how a domain file is structured.
A domain file can either:

- contain some or all of the section data directly
and/or
- contain links to separate files that hold detailed definitions.

This flexibility is intentional. It allows both humans and AI data modeling agents to browse the domain at a high level and then "click through" to the specific topics (entities, relationships, enums, diagrams, etc.) that are currently relevant.

```markdown
# Domain Name

Domain description...

## Metadata
Formal JSON/YAML block and diagrams...

### Domain Overview Diagram
- [Domain Overview](diagrams/overview.md)

## Entities
  - [Customer](entities/customer.md) 
  - [Customer Preference](entities/customer-preference.md) 

## Enums
  - [Loyalty Tier](enums/loyalty-tier.md) 

## Relationships
  - [Customer Has Preferences](relationships/customer-has-preferences.md) 

## Events
  - [Customer Preference Updated](events/customer-preference-updated.md) 

```
---

# **Type System**

MD‑DDL supports:

- string  
- integer  
- decimal  
- boolean  
- date  
- datetime  
- enum: Enum Name  
- array  
- object  

---