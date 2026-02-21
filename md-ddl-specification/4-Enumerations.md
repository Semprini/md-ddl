# MD-DDL

## **Enumerations**

Each file must declare which domain it is part of by starting with a Level 1 heading with the domain name.

### **Enum Declaration**

Enums appear under:

```markdown
## Enums
```

Enums can be defined as a simple list of values or a dictionary if the values require additional metadata.

Simple Format:

```yaml
values:
  - Bronze
  - Silver
  - Gold
```

Each enum uses a level‑3 heading with metadata:

````markdown
### Loyalty Tier
Categorizes customers by their annual spend and engagement levels.

```yaml
values:
  Bronze:
    description: Entry level tier
    score: 1
  Silver:
    description: Standard tier
    score: 2
  Gold:
    description: Premium tier
    score: 3
```
````

### Naming Rules

- Natural Language: Values should use business-friendly names (e.g., Part Time, not PT).
- Normalization: The compiler will handle the translation of these values into machine-readable codes (e.g., PART_TIME) if required by the target physical system.
- Global Reference: Once defined in a Domain, an Enum can be referenced by any Entity or Event using the enum:Enum Name type syntax.

---

...next: [Relationships](5-Relationships.md)
