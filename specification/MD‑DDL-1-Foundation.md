# **MD‑DDL Specification (Draft 0.3)**  
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

MD‑DDL supports a two‑layer structure for Entities, Enums, Relationships, and Events:

1. A summary definition in the domain file
2. A detailed definition in a separate file

This structure enables both human readability and AI context management. For example, the following files all contribute to the Customer domain:

```Code
domains/customer/domain.md
domains/customer/entities/customer.md
domains/customer/entities/customer-preference.md
domains/customer/relationships/customer-has-preferences.md
domains/customer/diagrams/overview.md
```

## **Two-Layer Structure**

The two-layer structure supports:

**AI Context Management:**

- The domain file provides a compact summary of all conceptual objects.
- AI agents load only the summaries initially.
- When needed, they follow the [detail] link to load the full and logical definition.

This mirrors Anthropic's "skills" concept but improves on it by:
- Keeping summaries centralised
- Avoiding duplication
- Ensuring humans can browse the domain easily

**Human Readability**
- The domain file becomes a clean, navigable table of contents.
- Detail files remain focused and uncluttered.

**Compiler Simplicity**
- The compiler knows exactly where to find summaries and details.
- The compiler merges both layers into a single conceptual/logical and physical model.

---

...next: [Domains](MD-DDL-2-Domains.md)
