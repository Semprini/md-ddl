# **Entities**
Each file must declare which domain it is part of by starting with a Level 1 heading with the domain name. 


## **Entity Declaration**

The Entities section appear under a level‑2 heading:

```markdown
## Entities
```

Each entity is introduced with a **level‑3 heading**:

```markdown
### Customer
```

## **Entity Description**

Free‑text Markdown under the heading describes the entity in more detail than was found in the domain summary.

## **Entity Definition**

A structured block defines the entity's attributes and logic. MD‑DDL follows a Key-as-Name philosophy to eliminate redundancy and ensure that the human-readable label used in the documentation is the exact same identifier used in the Knowledge Graph.:

````markdown
```yaml
extends: Party Role
attributes:
  - Customer Identifier:
      type: string
      identifier: true
  - Email Address:
      type: string
      pii: true
  - Balance:
      type: Decimal
```
```yaml
constraints:
  - Valid Date Range:
      logic: "End Date > Start Date"
  - Positive Liquidity:
      logic: "Balance > 0"
```
```yaml
governance:
  pii: true
  retention: 7 years
  access_role: HR_ADMIN
  classification: Confidential
```
````

**The "Key-as-Name" Principle**

By using the business term (e.g., Positive Liquidity) as the YAML key rather than a nested property (e.g., name: Positive Liquidity), we achieve:

- Semantic Uniqueness: Every constraint and attribute is forced to have a distinct, meaningful identity within its context.
- Reduced Friction: There is no "translation layer" between the documentation and the database schema. What you see in the heading or key is what appears in the Graph node.
- Logical Referencing: Sub-entities that inherit from this entity can specifically override or reference a constraint by its key name, allowing for a cleaner "Logic Lineage."

## Rules

**Inheritance:**
- Attribute Inheritance: Customer gets all attributes of Party Role
- Constraint Inheritance: If Party Role has a constraint, Customer must follow it.

**Identifiers:**

Every Entity should have at least one attribute marked identifier: true. If missing, the Knowledge Graph treats the entity as a "Logic Object" rather than a "Data Object."

**Parser:**

The parser will merge all YAML/JSON blocks found under a single L3 heading into a single Entity node.

**No Relationship Attributes:**

Explicitly forbid Customer Id appearing inside a Preference entity YAML. Instead, the Relationships section handles the link. This prevents "Foreign Key Drift."

### **Naming Rules**

- Natural Language Priority: Entity and attribute names must use natural language (e.g., Email Address, not email_addr).
- Case & Spaces: Names are case-sensitive and support spaces.
- No Redundancy: Do not include a name: field inside the YAML block. The Markdown heading serves as the Entity name, and the YAML keys serve as Attribute/Constraint names.
- Machine Normalisation: While the Knowledge Graph preserves these natural labels for navigability, the MD‑DDL compiler automatically handles the normalisation (e.g., conversion to snake_case) for physical system generation.

---

...next: [Enums](MD-DDL-4-Enumerations.md)
