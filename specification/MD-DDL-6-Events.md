# **Events**
Each file must declare which domain it is part of by starting with a Level 1 heading with the domain name. 

Events represent meaningful business‑level changes in state. They describe *what happened* in the domain, independent of how the underlying data systems record or transport those changes. Events allow MD‑DDL to map technical change (CDC, ETL deltas, logs) to **semantic business events**, ensuring that business processes react to meaning rather than database mechanics.

---

## **Event Declaration**

An event is declared using a **level‑3 Markdown heading** under the `## Events` section:

```markdown
## Events

### Customer Preference Updated
```

The heading is the authoritative name of the event.  
Event names use **natural language**, not camelCase, PascalCase, or snake_case.

---

## **Event Description**

Free‑text Markdown immediately following the heading provides a human‑readable description of the event. This describes the business meaning, not the technical implementation.

Example:

```markdown
Triggered when a customer changes one or more preferences.
```

The description may include:

- the business context  
- why the event matters  
- how it is used  
- any relevant domain rules  

---

## **Event Definition**

A structured YAML or JSON block defines the event’s formal properties:

````markdown
```yaml
actor: Customer
entity: Customer Preference
attributes:
  - name: updated fields
    type: array
  - name: timestamp
    type: datetime
```
````

### **Required fields**

| Field | Description |
|-------|-------------|
| `actor` | The entity or role that initiates or causes the event. |
| `entity` | The primary entity whose state has changed. |

### **Optional fields**

| Field | Description |
|-------|-------------|
| `attributes` | Additional data carried by the event (e.g., changed fields, metadata). |
| `relationships` | Optional references to related entities. |
| `classification` | Sensitivity, governance, or lineage metadata. |
| `conditions` | Optional rules describing when the event should be emitted. |

---

## **Event Rules**

1. **Natural‑language naming**  
   Event names must be written in natural language (e.g., “Customer Preference Updated”).

2. **No duplication**  
   The event name appears only in the heading, not inside the YAML block.

3. **Events are first‑class citizens**  
   Events are not embedded inside entities or relationships; they live in their own section.

4. **Events describe business meaning, not technical mechanics**  
   Events should not reference CDC, SQL operations, or ETL logic.

5. **Events may appear in any file**  
   As long as the file begins with the domain’s level‑1 heading, the compiler will assemble them.

6. **Events may be linked to entities and relationships**  
   Through `actor`, `entity`, and optional `relationships`.

7. **Events are optional**  
   Domains may define zero, one, or many events.

---

## **Example Event**

````markdown
### Customer Preference Updated
Triggered when a customer changes one or more preferences.

```yaml
actor: Customer
entity: Customer Preference
attributes:
  - name: updated fields
    type: array
  - name: timestamp
    type: datetime
```
````

---
