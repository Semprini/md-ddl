# **Domains**

In MD-DDL, the Domain file acts as the router for the Knowledge Graph. While detail files provide the DNA (Attributes/Constraints), the Domain file provides the Anatomy (How entities, events, and relationships sit together).

## **Domain Declaration**

A domain is declared using a **level‑1 Markdown heading**:

```markdown
# Customer
```

## **Domain Description**

All free‑text Markdown under the H1 heading and before the next H2 heading is considered the domain description.

## **Domain Metadata**

Metadata is appears under a level‑2 heading:

```markdown
## Metadata
```
Domain Metadata sets the default posture for all contained objects unless overridden. Metadata is:

Category|Metadata Keys|Purpose
--------|-------------|-------
Accountability|owners, stewards, technical_leads|Who is responsible for the business vs. technical health.
Governance & Security|classification, confidentiality, pii|The default security posture for the entire domain.
Compliance|sox_scope, gdpr_relevant, retention_policy|Legal and regulatory frameworks governing this data.
Lifecycle|status (Draft/Live), version, source_systems|The maturity and origin of the data domain.
Discovery|tags|Searchability

### **Metadata Format**

Metadata is expressed as YAML or JSON inside a fenced code block:

````markdown
## Metadata

```yaml
# Accountability
owners:
  - data.customer@example.com
stewards:
  - jane.doe@example.com
technical_leads:
  - architecture.team@example.com

# Governance & Security
classification: "Highly Confidential"
pii: true
regulatory_scope:
  - GDPR
  - CCPA
default_retention: "7 years"

# Lifecycle & Discovery
status: "Production"
version: "2.1.0"
tags:
  - Core
  - MasterData
  - B2C
source_systems:
  - "Salesforce CRM"
  - "SAP ERP"
```
````

### **Diagrams**

Diagrams appear under level‑3 headings inside the Metadata section to separate Data about the Domain from Visuals of the Domain.:

````markdown
### Domain Overview Diagram
High-level view of how Customer data flows into downstream analytics.
```mermaid
flowchart LR
    Customer --> Customer Preference
```
````

---
## **Domain Structure**

Below the metadata section there are several sections, each with a level‑2 heading. The sections are: 

```markdown
## Entities

### <entity name>
Conceptual definition.
[detail](link to details)

## Enums
...
## Relationships
...
## Events
...
```

The order of these sections is not important. See the specification details of each for more information.

### Sample Structure

Below is an example of how a domain file is structured.

```markdown
# Domain Name

Domain description...

## Metadata
Formal JSON/YAML block and diagrams...

### Domain Overview Diagram
- [Domain Overview](diagrams/overview.md)

## Entities

### Customer
The primary representation of a customer in the organisation.
[detail](entities/customer.md)

### Customer Preference
Represents customer‑specific settings and preferences.
[detail](entities/customer-preference.md) 

## Enums

### Loyalty Tier
A structured level within a loyalty program that offers different benefits and rewards based on engagement or spending.
[detail](enums/loyalty-tier.md) 

## Relationships

### Customer Has Preferences
A customer can have 0 to many preferences which are used for interactions with our business.
[detail](relationships/customer-has-preferences.md) 

## Events
Emited when any system updates a field which is used to configure customer interactions.
[detail](events/customer-preference-updated.md) 

```

## Rules for Summary Definitions

- The summary must include a short natural‑language description.
- The summary must include a [detail]\(link to the full definition file.)
- The summary should not include YAML or formal attributes. It is a conceptual definition.
- The summary must be below the entity's level‑3 heading.
- The summary is authoritative but high level for the entity name.
- The summary is intentionally brief, designed for AI agents to load upfront and humans to scan quickly.

This allows the domain file to act as a semantic index of the domain.

---

...next: [Entities](3-Entities.md)
