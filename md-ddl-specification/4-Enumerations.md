# MD‑DDL Specification (Draft 0.9.2)

## **Enumerations**

Each file must declare which domain it is part of by starting with a Level 1 heading with the domain name.

### **Enum Declaration**

Enums appear under:

```markdown
## Enums
```

Enums can be defined as a simple list of values or a dictionary if the values require additional metadata. Enums should be named as a plural - E.g. Customer Types.

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
- Normalization: Physical artifact generation handles the translation of these values into machine-readable codes (e.g., PART_TIME) if required by the target system.
- Global Reference: Once defined in a Domain, an Enum can be referenced by any Entity or Event using the enum:Enum Name type syntax.

### External Standard Enumerations

When an enum's values are defined by an external standard (for example ISO 4217
currencies, HL7 FHIR value sets, or BIAN enumerations), include a representative
subset of 5 to 15 values sufficient to demonstrate the pattern. Reference the
authoritative source using a `standard` metadata field.

```yaml
values:
  AUD:
    description: Australian Dollar
  USD:
    description: United States Dollar
  EUR:
    description: Euro
standard:
  name: ISO 4217
  version: "2024"
  url: https://www.iso.org/iso-4217-currency-codes.html
  note: Representative subset - full standard defines 180+ active currency codes
```

Physical artifact generation should support loading the full external value set
when the representative subset is insufficient for the target use case.

---

...next: [Relationships](5-Relationships.md)
