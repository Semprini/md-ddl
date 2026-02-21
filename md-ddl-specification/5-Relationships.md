# MD-DDL

## **Relationships**

Each file must declare which domain it is part of by starting with a Level 1 heading with the domain name.

Relationships are **first‑class citizens**.

### **Relationship Declaration**

```markdown
## Relationships
```

Each relationship uses a level‑3 heading:

```markdown
### Customer Has Preferences
```

#### **Relationship Description**

Free‑text Markdown describes the semantics.

### **Relationship Definition**

Relationships define the semantic and structural connection between two entities.

````markdown
```yaml
source: Customer
type: owns
target: Customer Preference
cardinality: one-to-many
granularity: atomic | group | period
ownership: Customer
```
```yaml
constraints:
  Active Customer Preference Only:
    check: "Customer.Status == 'Active' OR Customer Preference.EffectiveStatus == 'Inactive'"
    description: "A customer cannot have active preferences if their account is not active."
```
````

### Relationship Types

- `owns`: Strongest link. The target entity's life is bound to the source. Example: Customer owns Account. (If the customer is deleted, the account must be too).
- `has` / `associates_with`: A loose connection where both entities can exist independently. Example: Contact has Location.
- `references`: Used when one entity points to another for lookup purposes. Example: Transaction references Currency.
- `assigned_to`: Denotes a functional link or responsibility. Example: Claim assigned_to Adjuster.
- `triggers`: Used when one entity or event initiates another. Example: Application Submitted triggers Credit Check.
- `produces` / `results_in`: Describes the outcome of a process. Example: Assessment produces Risk Score.
- `supersedes` / `replaces`: Versioning or correction logic. Example: New Policy supersedes Old Policy.
- `governs`: A set of rules or a domain controlling an entity. Example: GDPR Policy governs Customer PII.
- `masks` / `protects`: Security-specific relationships. Example: Vault Service masks Credit Card Number.

### Granularity

Describes the resolution at which a relationship operates relative to the entities it connects.

Type|Description|Compiler Behavior
----|-----------|-----------------
atomic|The relationship holds at the finest level of detail — one instance on each side participates individually.|The compiler treats this as a direct join at full grain.
group|the related entity represents a collection or summary of instances on the other side (e.g. a monthly budget linked to individual daily transactions).|The compiler will generate aggregation logic to bridge the difference.
period|the relationship captures the state of one entity as it stood at a specific point in time rather than recording an event|The compiler will emit snapshot or point-in-time join logic accordingly.

If not specified, the compiler defaults to atomic.

### Relationship Rules

- First-Class Identity: Every relationship is a distinct node in the graph. It can hold its own metadata, constraints, and versioning.
- Directional Logic: The source is the origin of the relationship, and the target is the destination.
- Inverse Inference: The compiler automatically generates the inverse (e.g., if "Customer Has Preferences," it infers "Preferences Belong To Customer").
- Constraint Awareness: Constraints in a relationship can reference attributes from both the source and the target entities using the Entity.Attribute syntax.

#### **Relationship Naming Rules**

- Action-Oriented: Use natural language that describes the interaction (e.g., Account Holds Balance or Customer Places Order).
- Avoid Key Redundancy: Do not define Foreign Keys (e.g., Customer ID) inside the Entity attributes. The Relationship definition handles this link automatically.

---

...next: [Events](6-Events.md)
