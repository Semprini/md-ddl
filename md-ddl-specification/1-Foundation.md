# **MD‑DDL Specification (Draft 0.4)**  
*A Markdown‑native Data Definition Language for human-AI collaboration.*

---

# **Overview**

MD‑DDL is a **Markdown‑first**, **AI‑friendly** standard for **semantic data modeling** - defining what your data means in business terms, independent of how it's physically stored or processed.

It is designed to be readable by humans, generatable by AI, and compilable into:

- Data catalogs  
- Knowledge graphs  
- Data product definitions  
- Schemas and technical artifacts  

MD‑DDL uses Markdown structure as its primary syntax, with YAML or JSON blocks for structured definitions and Mermaid or PlantUML for diagramming. Structural consistency is enforced by the compiler and supported by companion AI agents.

---

# **Core Principles**

1. **Single Source of Truth**  
   Every concept is defined once, optionally per domain, in one location.

2. **Markdown‑Native**  
   Headings define structure; prose defines meaning.

3. **Semantic First**  
   Focus on business meaning and relationships, not technical implementation.

4. **AI‑Friendly**  
   No redundant fields. No manually maintained lists. Minimal boilerplate.

5. **Compiler‑Driven**  
   The compiler infers domain membership, indexes entities, and validates relationships.

6. **Graph‑Powered**  
   The knowledge graph acts as the semantic runtime for reasoning, lineage, and governance.

7. **Natural‑Language Naming**  
   Entities, attributes, and relationships use human‑readable names rather than code‑style casing.

8. **Eventual Consistency**  
   Designed for the full fifecycle of data in movement and at rest. All attributes (except primary identifiers) are nullable by default. Constraints define completeness requirements at specific lifecycle stages rather than enforcing rigid schemas.

---

# **Design Philosophy**

## **Semantic Modelling**

MD‑DDL is a **semantic modeling language** - it captures the **meaning** of your data, not the mechanics of how it's stored.

**What you define:**
- What is a Customer? (concept)
- What properties does a Customer have? (attributes)
- How does a Customer relate to other concepts? (relationships)
- What rules govern Customer data? (constraints)
- What happens when Customer data changes? (events)
- How does this concept evolve over time? (temporal patterns)

**What the compiler generates:**
- Database tables, columns, and foreign keys
- Graph nodes, edges, and properties
- Event schemas and message formats
- API definitions and validation logic
- Temporal tracking columns and versioning logic
- Governance metadata and lineage tracking

This separation means:
- Business stakeholders understand the model without technical knowledge
- The same semantic model compiles to multiple physical systems
- Physical optimizations don't require changing the business definition
- AI agents reason about business meaning, not database mechanics

A critical aspect of semantic modeling is **when data is true**, not just what it means. MD‑DDL treats temporal modeling as a **semantic concern**, not a physical implementation detail. This enables the knowledge graph to:
- **Reconstruct state at any point in time** - "What were this customer's preferences on January 1st?"
- **Track changes and lineage** - "When did this preference change and why?"
- **Support temporal reasoning** - "Which customers had active preferences during Q4?"
- **Maintain audit trails** - "Show me the history of changes to this entity"

## **Constraints as Business Rules**

Constraints in MD‑DDL express **business logic and data quality rules**, not just database constraints. They can be:
- Evaluated at different stages of the data lifecycle
- Applied selectively based on governance policies
- Used for data quality scoring rather than hard enforcement
- Documented for human understanding of business rules

## **Temporal by Design**

Data evolves over time. MD‑DDL supports temporal patterns as first-class metadata:
- Entities can track when data is valid in the business world (valid time)
- Entities can track when data was recorded or corrected (transaction time)
- Events are naturally point-in-time and immutable
- The compiler handles physical temporal implementation

## **Graph-Native Thinking**

While MD‑DDL can compile to relational schemas, it thinks in **relationships**, not foreign keys:

This means:
- Relationships are named and have business meaning ("owns", "references", "governs")
- Cross-domain connections are natural, not awkward joins
- The knowledge graph provides semantic navigation and discovery
- Lineage flows through relationships automatically

---

# **Document Structure**

MD‑DDL is composed of several logical components: 
- [Domains](2-Domains.md)
- [Entities](3-Entities.md)
- [Enumerations](4-Enumerations.md)
- [Relationships](5-Relationships.md)
- [Events](6-Events.md)

If providing the specification to an AI, you might get better results with the complete spec in a single file:

- [Complete Specification](MD-DDL-Complete.md)

MD‑DDL uses a **two‑layer structure** for Entities, Enums, Relationships, and Events:

1. A **summary definition** in the domain file
2. A **detailed definition** in a separate file

This structure supports both human readability and AI context management.

Example domain layout:

```
domains/customer/domain.md
domains/customer/entities/customer.md
domains/customer/entities/customer-preference.md
domains/customer/relationships/customer-has-preferences.md
domains/customer/diagrams/overview.md
```

---

## **Two‑Layer Structure**

The domain file provides **high-level concepts** - what exists and why.
- What concepts exist in this domain?
- What does each concept mean in business terms?
- How do concepts relate to each other?

### **AI Context Management**
  
AI agents follow this pattern naturally:

1. **Load the domain file** - Understand the conceptual landscape
2. **Browse summaries** - Get context on what exists without loading everything
3. **Load details on demand** - Pull specific entity/relationship definitions when needed for a task
4. **Reason semantically** - Work with business concepts, not technical schemas

This mirrors effective prompt engineering:
- Start broad (concepts)
- Narrow down (relevant details)
- Stay focused (only load what's needed)

### **Human Readability**

- The domain file becomes a clean, navigable table of contents.  
- Detail files remain focused, concise, and free from clutter.

### **Compiler Simplicity**

The compiler processes both layers:

1. **Discovers** domain files and follows `[detail]` links
2. **Merges** concept summaries and detailed definitions
3. **Validates** that summaries and details are consistent
4. **Generates** knowledge graph with full semantic model
5. **Compiles** to physical schemas, catalogs, and artifacts

The file structure is a convention, not a technical requirement - it's designed for **human and AI comprehension**, and the compiler handles the mechanics.

---

...next: [Domains](2-Domains.md)
