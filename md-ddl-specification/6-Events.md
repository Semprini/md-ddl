# **Events**
Each file must declare which domain it is part of by starting with a Level 1 heading with the domain name. 

Events represent meaningful business-level changes in state. They describe *what happened* in the domain, independent of how the underlying data systems record or transport those changes. Events allow MD‑DDL to map technical change (CDC, ETL deltas, logs) to **semantic business events**, ensuring that business processes react to meaning rather than database mechanics.

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

A structured YAML or JSON block defines the event's formal properties:

````markdown
### Customer Preference Updated

Emitted when a customer modifies their communication or interaction preferences.
```yaml
actor: Customer
entity: Customer Preference
emitted_on: 
  - create
  - update
business_meaning: Customer has expressed a change in how they wish to interact with the business
downstream_impact:
  - Marketing campaigns must respect updated preferences
  - Communication systems must apply new settings
  - Compliance audit trail is maintained

constraints:
  Ownership Validation:
    check: "Customer.ID == Customer Preference.Customer ID"
    description: Preference change must be for the acting customer
  
  Active Customer Only:
    check: "Customer.Status == 'Active'"
    description: Only active customers can update preferences

governance:
  retention: 7 years
  access_role: CUSTOMER_SERVICE
  classification: Confidential
  pii: true
  compliance_relevance:
    - GDPR Right to Object
    - CCPA Opt-Out
```
````

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
   As long as the file begins with the domain's level‑1 heading, the compiler will assemble them.

6. **Events may be linked to entities and relationships**  
   Through `actor`, `entity`, and optional `relationships`.

7. **Events are optional**  
   Domains may define zero, one, or many events.

8. **Contextual Payloads**

   The attributes block should focus on the delta (what changed) and the context (why it changed), rather than a full copy of the entity.

9: **Temporal Priority** 
   Every event MUST have a timestamp or a sequence attribute to ensure the Knowledge Graph can reconstruct the timeline of an entity's life.

---

## **Example Event**

````markdown
### Customer Preference Updated
Triggered when a customer changes one or more preferences.

```yaml
actor: Customer
entity: Customer Preference
attributes:
  - updated fields:
      type: array
  - timestamp:
      type: datetime
```
````

---