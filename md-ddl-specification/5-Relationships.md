# MD‑DDL Specification (Draft 0.9.1)

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

```yaml
# Optional governance override (include only when different from domain defaults)
governance:
  classification: Confidential
```
````

### Relationship Types

- `owns`: Strongest link. The target entity's life is bound to the source. Example: Customer owns Account. (If the customer is deleted, the account must be too).
- `has` / `associates_with`: A loose connection where both entities can exist independently. Example: Contact has Location.
- `references`: Used when one entity points to another for lookup purposes. Example: Transaction references Currency.
- `related_to`: A symmetric or near-symmetric association where neither entity owns or depends on the other. Used for peer-level connections and self-referential networks (e.g., Party related to Party for ownership structures, Account related to Account for parent/sub-account hierarchies). Most commonly paired with `self_referential: true`.
- `assigned_to`: Denotes a functional link or responsibility. Example: Claim assigned_to Adjuster.
- `triggers`: Used when one entity or event initiates another. Example: Application Submitted triggers Credit Check.
- `produces` / `results_in`: Describes the outcome of a process. Example: Assessment produces Risk Score.
- `supersedes` / `replaces`: Versioning or correction logic. Example: New Policy supersedes Old Policy.
- `governs`: A set of rules or a domain controlling an entity. Example: GDPR Policy governs Customer PII.
- `masks` / `protects`: Security-specific relationships. Example: Vault Service masks Credit Card Number.

### Granularity

Describes the resolution at which a relationship operates relative to the entities it connects.

Type|Description|Generation Guidance
----|-----------|--------------------
atomic|The relationship holds at the finest level of detail — one instance on each side participates individually.|Treated as a direct join at full grain.
group|the related entity represents a collection or summary of instances on the other side (e.g. a monthly budget linked to individual daily transactions).|Generates aggregation logic to bridge the difference.
period|the relationship captures the state of one entity as it stood at a specific point in time rather than recording an event|Emits snapshot or point-in-time join logic accordingly.

If not specified, the default is atomic.

### Self-Referential Relationships

A self-referential relationship connects instances of the same entity type to each other — `source` and `target` both name the same entity. Use this pattern for ownership networks, hierarchies, family or social ties, and any associative structure within a single entity population.

#### Declaration

Set `self_referential: true` in the relationship YAML:

```yaml
source: Party
type: related_to
target: Party
cardinality: many-to-many
granularity: atomic
ownership: Party
self_referential: true
```

#### Edge Attributes

When the relationship instance itself carries attributes — not the entities it connects — declare them under `relationship_attributes`. These become columns on the bridge table in physical generation:

```yaml
self_referential: true
relationship_attributes:
  - Association Type
  - Association Start Date
  - Association End Date
  - Verified
```

`relationship_attributes` names follow standard MD-DDL attribute naming (natural language, title case). They are attributes of the association instance, not of either participant entity.

#### Source and Target Semantics

When `self_referential: true`, directionality is preserved in the physical model by generating two FK columns pointing to the same entity table:

- `source_[entity_identifier]` — FK referencing the source instance
- `target_[entity_identifier]` — FK referencing the target instance

For a Party with identifier `Party Identifier`, the bridge table would contain `source_party_identifier` and `target_party_identifier`. For bidirectional relationships where direction is not meaningful (e.g., "sibling of"), the generating agent should document that either column may be treated as the source.

The `ownership` field names the entity that owns the relationship definition — typically the entity the relationship most naturally describes from. For self-referential relationships this is always the same entity as `source` and `target`.

#### Generation Guidance

Self-referential relationships always generate a bridge/association table — even at one-to-many cardinality — to avoid a self-referencing FK on the entity's own primary key column:

Cardinality | Physical pattern
--- | ---
`many-to-many` | Bridge table with `source_[pk]`, `target_[pk]`, and `relationship_attributes` columns
`one-to-many` (hierarchy) | Bridge table preferred; adjacency list (parent FK on entity) is acceptable for shallow hierarchies where generation skill supports it explicitly
Any | Unbounded recursion depth is the default; document when depth is bounded and recommend recursive CTE query patterns in platform-specific notes

### Relationship Rules

- First-Class Identity: Every relationship is a distinct node in the graph. It can hold its own metadata, constraints, and versioning.
- Directional Logic: The source is the origin of the relationship, and the target is the destination.
- Inverse Inference: The generating agent automatically produces the inverse (e.g., if "Customer Has Preferences," it infers "Preferences Belong To Customer").
- Constraint Awareness: Constraints in a relationship can reference attributes from both the source and the target entities using the Entity.Attribute syntax.
- Governance Inheritance: Relationships inherit governance/compliance metadata from the domain. Include `governance:` only when overriding inherited values.

#### **Relationship Naming Rules**

- Action-Oriented: Use natural language that describes the interaction (e.g., Account Holds Balance or Customer Places Order).
- Avoid Key Redundancy: Do not define Foreign Keys (e.g., Customer ID) inside the Entity attributes. The Relationship definition handles this link automatically.

---

...next: [Events](6-Events.md)
