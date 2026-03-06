# MD‑DDL Specification (Draft 0.8.0)

*A Markdown‑native Data Definition Language for human-AI collaboration.*

---

## **Overview**

MD‑DDL is a **Markdown‑first**, **AI‑friendly** standard for defining domains, entities, attributes, enums, relationships, events, source mappings, and data products. It is designed to be readable by humans, generatable by AI, and transformable into:

- Data catalogs
- Knowledge graphs
- Data product definitions
- Schemas and technical artifacts (DDL, JSON Schema, Parquet contracts)
- ETL/ELT logic and source-to-domain lineage

MD‑DDL uses Markdown structure as its primary syntax, with YAML or JSON blocks for structured definitions and Mermaid or PlantUML for diagramming. Structural consistency is enforced by AI agents that validate, generate, and maintain model artifacts.

---

## **Core Principles**

1. **Source of Truth**  
   Every concept is defined once in the domain, in one canonical location. A design choice is whether to follow Domain Driven Design (DDD) and allow domain concepts to be mutually exclusive or not.

   This principle extends to source mappings. Source definitions and transform files are self-contained within each domain under `sources/<system>/`. Canonical entities contain no source references — they define meaning, not origin. Canonical data products replace the concept of Systems of Record: source systems are systems of change whose outputs are governed by the canonical model.

2. **Markdown‑Native**  
   Headings define structure; prose defines meaning.

3. **AI‑Friendly**  
   No redundant fields. No manually maintained lists. Minimal boilerplate.

4. **Agent‑Driven**  
   AI agents infer domain membership, index entities, validate relationships, and generate physical artifacts from the model.

5. **Graph‑Powered**  
   The knowledge graph acts as the semantic runtime for reasoning, lineage, and governance.

6. **Natural‑Language Naming**  
   Entities, attributes, and relationships use human‑readable names rather than code‑style casing.

---

## **Document Structure**

MD‑DDL is composed of several logical components:

- [Domains](./2-Domains.md)
- [Entities](./3-Entities.md)
- [Enumerations](./4-Enumerations.md)
- [Relationships](./5-Relationships.md)
- [Events](./6-Events.md)
- [Sources](./7-Sources.md)
- [Transformations](./8-Transformations.md)
- [Data Products](./9-Data-Products.md)

MD‑DDL uses a **two‑layer structure** for Entities, Enums, Relationships, Events, and Data Products:

1. A **summary definition** in the domain file  
2. A **detailed definition** in a separate file  

This structure supports both human readability and AI context management.

Example domain layout:

```shell
domains/customer/domain.md
domains/customer/entities/customer.md
domains/customer/entities/customer-preference.md
domains/customer/relationships/customer-has-preferences.md
domains/customer/products/analytics.md
domains/customer/diagrams/overview.md
```

Example source layout:

```shell
Financial Crime/sources/salesforce-crm/source.md
Financial Crime/sources/salesforce-crm/transforms/table_account.md
Financial Crime/sources/salesforce-crm/transforms/table_contact_point.md
Financial Crime/sources/sap-fraud-management/source.md
Financial Crime/sources/temenos-payment/source.md
```

Domain files and source files are co-located at the domain level. Domain files define meaning. Source folders define operational origin and mapping logic for that specific domain context.

---

### **Two‑Layer Structure**

#### **AI Context Management**

- The domain file provides a compact summary of all conceptual objects.  
- AI agents load only the summaries initially.  
- When deeper context is needed, they follow the `detail:` link to load the full definition.

This mirrors Anthropic’s "skills" concept but improves on it by:

- Centralising summaries
- Avoiding duplication
- Ensuring humans can browse the domain easily

#### **Human Readability**

- The domain file becomes a clean, navigable table of contents.  
- Detail files remain focused, concise, and free from clutter.

#### **Structural Predictability**

- AI agents know exactly where to find summaries and details.  
- Both layers are merged into a unified conceptual, logical, and physical model.

#### Detail File Flexibility

Detail files are not restricted to a single entity. Authors may organise detail files to suit their modelling style — for example, one entity per file, one file per subdomain cluster, or a file combining an entity with its enumerations and originating relationships.
The only structural requirement is that every detail file begins with a level‑1 heading naming the domain (with a link back to the domain file), followed by one or more level‑2 section headings (## Entities, ## Enums, ## Relationships, ## Events, ## Data Products) containing the relevant definitions.

Source transform files follow the same two-layer pattern but are scoped to a source system within a domain context. They begin with a level-1 heading linking back to `./source.md` in the same source folder, followed by a level-2 heading for the source table and optional level-3 rule sections for non-direct mappings.

---

## **Domains**

In MD-DDL, the Domain file acts as the router for the Knowledge Graph. While detail files provide the DNA (Attributes/Constraints), the Domain file provides the Anatomy (How entities, events, and relationships sit together).

### **Domain Declaration**

A domain is declared using a **level‑1 Markdown heading**:

```markdown
# Customer
```

### **Domain Description**

All free‑text Markdown under the H1 heading and before the next H2 heading is considered the domain description.

### **Domain Metadata**

Metadata appears under a level‑2 heading:

```markdown
## Metadata
```

Domain Metadata sets the default posture for all contained objects unless overridden. Metadata is:

Governance and compliance metadata declared at the domain level is inherited by all contained entities, relationships, and events. Detail files should not repeat governance attributes when values are unchanged from the domain defaults.

Include a `governance:` block in detail files only when specifying an exception or stricter requirement than the domain default.

Category|Metadata Keys|Purpose
--------|-------------|-------
Accountability|owners, stewards, technical_leads|Who is responsible for the business vs. technical health.
Governance & Security|classification, confidentiality, pii|The default security posture for the entire domain.
Compliance|sox_scope, gdpr_relevant, retention_policy|Legal and regulatory frameworks governing this data.
Lifecycle|status (Draft/Live), version|The maturity of the data domain.
Discovery|tags|Searchability

#### **Metadata Format**

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
```
````

### **Source Systems**

Source systems are first-class domain summary objects and must be declared under a level‑2 heading immediately after `## Metadata`.

Use a Markdown table with the following columns:

Column | Purpose
--- | ---
**Business Application** | Source application or product name, expressed as a Markdown link to the source markdown file.
**Platform** | Technology platform or deployment model.
**Capability Domain** | Business capability or functional area served by the source.

Example:

````markdown
## Source Systems

Business Application | Platform | Capability Domain
--- | --- | ---
[Temenos Payment](sources/temenos-payment/source.md) | Temenos SaaS | Payment Execution
[SAP Fraud Management](sources/sap-fraud-management/source.md) | SAP | Fraud
````

#### **Diagrams**

Diagrams appear under level‑3 headings inside the Metadata section, after the YAML metadata block. This separates data *about* the domain from visuals *of* the domain.

A domain file should contain at least one **Domain Overview Diagram** that shows the full entity graph for the domain. This diagram is the primary navigational and communicative artefact of the domain file — it must give any reader an immediate understanding of how all concepts relate to each other.

The Domain Overview Diagram uses `graph TD` (top-down) or `graph LR` (left-right) Mermaid syntax with the ELK layout engine for consistent, readable positioning of complex graphs.

##### **What to include in the Domain Overview Diagram**

The diagram must show:

1. **All entities** defined in the domain
2. **Inheritance relationships** using `-->|is a|` notation
3. **All relationships** between entities using labelled edges whose verb matches the relationship name defined in the Relationships section
4. **Hyperlinks** on key navigable entities using `EntityName["<a href='path'>Display Name</a>"]` syntax. Not every node needs a link — prioritise the abstract and most-referenced entities.

The diagram must not show:

- Attributes (these belong in entity detail files)
- Cardinality notation (this belongs in relationship detail files)
- Enumeration values (these belong in enum detail files)

##### **Diagram Syntax Rules**

- Use `graph TD` for domains with deep inheritance hierarchies
- Use the ELK layout engine (`layout: elk`) with `mergeEdges: false` for complex graphs to prevent edge crossings
- Relationship edge labels must use the verb form from the Relationships
  section: `-->|assumes|`, `-->|references|`, `-->|governed by|`
- Inheritance is always expressed as `Child -->|is a|Parent`
- Bidirectional relationships use `<-->|label|`
- Entity hyperlinks use plain anchor tags: `<a href='path'>Display Name</a>`
  with no additional CSS class attributes
- Node identifiers in the graph use PascalCase for readability
  (e.g., `PartyRole`, `ContactAddress`) but the display label uses
  natural language where a hyperlink is defined

##### **Example: Financial Crime Domain Overview Diagram**

````markdown
### Domain Overview Diagram

```mermaid
---
config:
  layout: elk
  elk:
    mergeEdges: false
    nodePlacementStrategy: LINEAR_SEGMENTS
  look: classic
  theme: dark
---
graph TD

  Individual --> |is a|Party
  Company --> |is a|Party
  TermDepositAgreement --> |is a|Agreement
  LoanAgreement --> |is a|Agreement

  Party <--> |related to|Party
  Party --> |assumes|PartyRole

  Customer --> |is a|PartyRole
  Merchant --> |is a|PartyRole
  Payee --> |is a|PartyRole
  Payer --> |is a|PartyRole
  Teller --> |is a|PartyRole
  PaymentInitiator --> |is a|PartyRole

  Party --> |has|ContactAddress
  PartyRole --> |uses|ContactAddress
  ContactAddress --> |references|Address

  Customer --> |holds|Account
  Customer --> |has|CustomerPreferences
  PartyRole --> |governed by|Agreement
  PaymentTransaction --> |has|Payer
  PaymentTransaction --> |has|Payee
  PaymentTransaction --> |initiated by|PaymentInitiator
  PaymentTransactionAccount --> |involved in|PaymentTransaction
  PaymentTransactionAccount --> |debits|Account
  PaymentTransactionAccount --> |credits|Account
  Teller --> |processes|PaymentTransaction
  Merchant --> |processes|PaymentTransaction

  Account --> |holds|Product
  Branch --> |services|Account
  Product --> |in terms of|Agreement

  Party["<a href='entities/party.md'>Party</a>"]
  PartyRole["<a href='entities/party_role.md'>Party Role</a>"]
  ContactAddress["<a href='entities/contact_address.md'>Contact Address</a>"]
  Address["<a href='entities/address.md'>Address</a>"]
```
````

##### **Why the Domain Overview Diagram matters**

The domain diagram is the first artefact an AI agent or a new team member loads when working with a domain. It establishes:

- **Scope**: what concepts are owned by this domain
- **Structure**: how inheritance hierarchies are organised
- **Connectivity**: which entities are central vs peripheral
- **Navigation**: hyperlinks on key entities provide one-click access to detail files from the diagram itself

A well-maintained domain diagram makes the two-layer structure of MD‑DDL work in practice — the domain file is the map, and the diagram is the visual index of that map.

##### **Additional Diagrams**

Beyond the overview, a domain file may contain additional level‑3 diagrams focusing on a specific sub-area. For example:

````markdown
### Transaction Flow Diagram
Shows how payment transactions move through party roles.

```mermaid
graph LR
  Payer --> |initiates|PaymentTransaction
  PaymentTransaction --> |credits|Payee
```
````

Additional diagrams are optional. The Domain Overview Diagram is required.

#### Conceptual vs Logical Diagrams

MD-DDL uses two distinct diagram types for different purposes:

Diagram|Location|Purpose|Relationship Labels
-------|--------|-------|-------------------
`graph TD/LR`|Domain file|Conceptual model — business meaning and named relationships|Required — must match Relationships section
`classDiagram`|Entity detail file|Logical model — structural realization of the entity|Optional — structural intent only

The classDiagram is not required to mirror the domain graph one-for-one. Modellers have freedom to realize conceptual relationships as they see fit at the logical level.

---

### **Domain Structure**

Below the metadata section, the Domain file organizes concepts into six primary sections using level‑2 headings: `## Source Systems`, `## Entities`, `## Enums`, `## Relationships`, `## Events`, and `## Data Products`.

In the Domain file, these sections **must use Markdown tables** for high-level summaries. This ensures the domain file acts as a compact "Router" for the knowledge graph.

#### Sample File Structure

```shell
domain.md
entities/party.md        ← Party entity + Party Has Role + Party Has Contact Address
entities/party-role.md   ← Party Role entity + Party Role Uses Contact Address
entities/address.md      ← Address entity (no outbound relationships)
products/analytics.md    ← Consumer-aligned data products
products/canonical.md    ← Domain-aligned data products
sources/temenos-payment/source.md
sources/sap-fraud-management/source.md
```

#### **Source Systems Table**

Summarizes operational source applications relevant to the domain.

Column | Purpose
--- | ---
**Application** | Markdown link to the source markdown file.
**Platform** | Technology platform or deployment model.
**Capability Domain** | Business capability or functional area served by the source.

---

#### **Entities Table**

The Entities table summarizes the core concepts of the domain.

 Column | Purpose
 --- | ---
**Name** | The natural language name of the entity, linked to its anchor in a detail file.
**Specializes** | If applicable, a link to the parent entity being specialized.
**Description** | A brief conceptual definition (1–2 sentences).
**Reference** | Optional URL to external industry standards (e.g., BIAN, FIBO, ISO).

---

#### **Enums Table**

Summarizes the discrete value sets used within the domain. Enums should be named as a plural - E.g. Customer Types.

Column | Purpose
--- | ---
**Name** | The name of the enumeration, linked to the detail file.
**Description** | What this set of values represents.
**Reference** | Optional external reference for standardized codes.

---

#### **Relationships Table**

Summarizes the semantic connections between entities.

Column | Purpose
--- | ---
**Name** | The action-oriented name (e.g., Customer Has Preferences), linked to details.
**Description** | The business meaning of the connection.
**Reference** | Optional link to relationship patterns or external schemas.

---

#### **Events Table**

Summarizes the meaningful business changes that occur within the domain.

Column | Purpose
--- | ---
**Name** | The natural language name of the event, linked to details.
**Actor** | The primary entity or role that initiates the event.
**Entity** | The primary entity affected by the event.
**Description** | The business trigger for this event.

---

#### **Data Products Table**

Summarizes the data products published by the domain.

Column | Purpose
--- | ---
**Name** | The product name, linked to its detail definition.
**Class** | `source-aligned`, `domain-aligned`, or `consumer-aligned`.
**Consumers** | Primary consumers of this product.
**Status** | Lifecycle state: `Draft`, `Production`, `Deprecated`.

---

### **Rules for Summary Definitions**

- **Tabular Authority:** The Domain file summary **must** use the table formats defined above. H3 headings are reserved for **Detail Files**.
- **Linking Strategy:** The `Name` column must contain a Markdown link pointing to the specific H3 anchor in the detail file (e.g., `[Entity Name](./path/to/file.md#entity-name)`).
- **AI Scoping:** AI agents should ingest these tables first to understand the "Anatomy" of the domain before requesting the "DNA" (YAML blocks) from the detail files.
- **No Boilerplate:** If a column like `Specializes` or `Reference` is empty for all entries in a section, it may be omitted from the table, but the `Name` and `Description` columns are mandatory.
- The description must include a short natural‑language description. A longer description will be included in the detail file.

This allows the domain file to act as a semantic index of the domain.

---

#### **Domain Structure Example**

Below is an example of how a domain file is structured.

````markdown
# Domain Name

Domain description...

## Metadata
Formal JSON/YAML block and diagrams...

## Source Systems

Business Application | Platform | Capability Domain
--- | --- | ---
[Customer CRM](sources/salesforce-crm/source.md) | Salesforce SaaS | Customer Relationship Management

### Domain Overview Diagram

```mermaid
graph TD

  Individual --> |is a|Party
  Company --> |is a|Party...
```

## Entities

Name | Specializes | Description | Reference
--- | --- | --- | ---
[Customer](./details.md#customer) | [Party Role](./details.md#party-role) | An individual or legal entity that has a relationship with the organization. | [BIAN: Party Role](https://...) |
[Individual](./details.md#individual) | [Party](./details.md#party) | A natural person as opposed to a legal entity. | |

When an entity specializes (inherits from) another entity, declare this in the specializes column with a link to the parent.

## Enums

Name | Description | Reference
--- | --- | ---
[Loyalty Tier](./details.md#loyalty-tier) | Categorizes customers by annual spend and engagement. | |

## Relationships

Name | Description | Reference
--- | --- | ---
[Customer Has Preferences](./details.md#customer-has-preferences) | Maps a customer to their specific interaction settings. |

## Events

Name | Actor | Entity | Description
--- | --- | --- | ---
[Preference Updated](./details.md#preference-updated) | Customer | Customer Preference | Emitted when interaction settings are modified.

## Data Products

Name | Class | Consumers | Status
--- | --- | --- | ---
[Customer 360 Profile](products/analytics.md#customer-360-profile) | consumer-aligned | Retail Analytics Team | Production

````

---

...next: [Entities](3-Entities.md)

## **Entities**

Each file must declare which domain it is part of by starting with a Level 1 heading with the domain name. The domain name should provide a link back to the domain file like:

```markdown
# [My Domain](../domain.md)
```

### **Entity Declaration**

A detail file may contain any combination of ## Entities, ## Enums, and ## Relationships sections. Authors are free to co-locate an entity with its directly originating relationships and any enumerations it references — this is the recommended pattern when a single entity is the clear owner of those concepts.
The Entities section appear under a level‑2 heading:

```markdown
## Entities
```

Each entity is introduced with a **level‑3 heading**:

```markdown
### Customer
```

### **Entity Description**

Free‑text Markdown under the heading describes the entity in more detail than was found in the domain summary.

### **Entity Diagram**

Every entity detail file must include a `classDiagram` immediately after the entity description and before the YAML definition blocks. The diagram is the visual contract for the entity — it shows the entity's own attributes, its position in the inheritance hierarchy, and all of its immediate relationships to other entities.

#### **Diagram Configuration**

All entity diagrams use the ELK layout engine for consistent rendering:

````markdown
```mermaid
---
config:
  layout: elk
---
classDiagram
  ...
```
````

#### **The Subject Class**

The entity being defined is the **subject class**. It is always written as a full class block with its attributes listed inside:

```text
  class Party{
    <<abstract>>
    * Party Identifier : string
    Legal Name : string
    Party Status : enum~PartyStatus~
  }
```

**Rules for the subject class:**

- The class name uses PascalCase matching the entity heading (e.g., `Party`, `ContactAddress`, `PartyRole`)
- If the entity is abstract — never instantiated directly, only specialised - add `<<abstract>>` as the first line inside the class block
- The primary identifier attribute is prefixed with `*` to mark it as the key
- All attributes defined in the entity's YAML block must appear in the diagram
- Attribute types use the Mermaid classifier syntax:
  - Primitives: `string`, `integer`, `decimal`, `boolean`, `date`, `datetime`
  - Enumerations: `enum~EnumName~` (e.g., `enum~PartyStatus~`, `enum~CountryCode~`)
  - Arrays: append `[]` to the type (e.g., `enum~CountryCode~[]`, `string[]`)
- Inherited attributes from parent entities are **not** repeated in the subject class — only attributes defined in this entity's own YAML block are shown
- Attribute format is `AttributeName : Type` with a space either side of the colon

#### **Related Classes**

All other classes that appear in the diagram — parents, children, related entities, and referenced enums — are **reference classes** unless they are enums detailed in the same file. Reference classes are never defined with attribute blocks. Instead they use the linked class syntax:

```text
  class Party["<a href='party.md'>Party</a>"]
```

**Rules for reference classes:**

- Use plain anchor tags: `<a href='path'>Display Name</a>`
- No CSS class attributes on the anchor tag
- The `href` path is relative to the current file's location and uses snake_case filenames (e.g., `party.md`, `party_role.md`, `contact_address.md`)
- Display Name uses natural language with spaces matching the entity heading (e.g., `Party Role`, `Contact Address`)
- All reference class definitions are grouped at the bottom of the diagram, after all relationship lines
- If a specialisation child has no detail file yet, it may appear as a bare unlinked class: `class Customer` — without a block or link

#### **Enum Classes in Entity Diagrams**

Any enum used by the subject class attributes must appear in the class diagram.

Use one of two patterns:

1. **Referenced enum (detail in another file)** — show as a linked reference class:

```text
  class PartyStatus["<a href='../enums/party_status.md'>Party Status</a>"]
```

1. **Co-located enum (detail in the same file)** — show as an expanded enum class with values:

```text
  class PartyStatus{
    <<enumeration>>
    Active
    Inactive
    Under Review
  }
```

**Rules for enum classes:**

- Every enum type referenced in the subject class (for example `enum~PartyStatus~`) must appear exactly once in the diagram
- If the enum is defined in the same detail file under `## Enums`, render it as an expanded enum class with its values and include `<<enumeration>>`
- If the enum is defined elsewhere, render it as a linked reference class to its enum detail file and include only the `<<enumeration>>` tag in the class detail.
- Use PascalCase class names for enum class identifiers (for example `PartyStatus`, `CountryCode`)
- Display names in links use natural language (for example `Party Status`, `Country Code`)

#### **Inheritance**

Inheritance uses the Mermaid `--|>` arrow with the child on the left:

```text
  Individual --|> Party
  Company --|> Party
```

This reads as "Individual is a specialisation of Party." The direction matches the domain overview diagram convention of `Child -->|is a|Parent`.

When an entity **is** a specialisation, show the parent as a reference class:

```text
  Individual --|> Party
  class Party["<a href='party.md'>Party</a>"]
```

When an entity **has** specialisations, show each child as a reference class (or bare class if not yet defined):

```text
  Individual --|> Party
  Company --|> Party
  class Individual["<a href='individual.md'>Individual</a>"]
  class Company["<a href='company.md'>Company</a>"]
```

#### **Entity Relationships**

All immediate relationships to and from the entity are shown with labelled arrows and cardinality. The classDiagram is a logical realization of the entity — relationship labels here describe the structural link (e.g., has, references) and do not need to match the conceptual relationship names defined in the domain Relationships section. A single conceptual relationship may realize as multiple logical associations, and some logical associations may have no direct conceptual counterpart.

```text
  Party "1" --> "0..*" PartyRole
  PartyRole "0..*" --> "0..*" ContactAddress
  ContactAddress "0..*" --> "1" Address
```

Relationship labels on classDiagram arrows are optional. When included, they describe the structural navigation intent, not the conceptual relationship name.

**Rules for relationships:**

- Cardinality is always shown on both ends using quoted strings: `"1"`, `"0..1"`, `"0..*"`, `"1..*"`
- In class diagrams the relationship label is optional. We are realizing the concepts from the domain in a logical model so there may not be a direct relationship.
- The arrow direction reflects the ownership or navigational direction: the entity that *holds the reference* is the source (`-->`)
- Bidirectional relationships use `<-->`
- Every entity in a relationship line must have a corresponding reference class definition at the bottom of the diagram

#### **Ordering Within the Diagram**

To keep diagrams readable and consistent, follow this ordering:

1. The subject class block (with attributes)
2. Specialisation child classes (bare or linked, one per line)
3. Inheritance arrows (`--|>`)
4. Relationship lines (`-->` with cardinality and label)
5. Enum classes (expanded if co-located; linked reference if external)
6. All remaining reference class definitions (`class Foo["<a href='...'>...</a>"]`)

#### **Example**

**Abstract entity with specialisations and outbound relationships (Party):**

````markdown
```mermaid
---
config:
  layout: elk
---
classDiagram
  class Party{
    <<abstract>>
    * Party Identifier : string
    Legal Name : string
    Risk Rating : enum~FinancialCrimeRiskRating~
  }

  Individual --|> Party
  Company --|> Party
  Party "1" --> "0..*" PartyRole
  Party "1" --> "0..*" ContactAddress

  class FinancialCrimeRiskRating["<a href='../enums/financial_crime_risk_rating.md'>Financial Crime Risk Rating</a>"]

  class Individual["<a href='individual.md'>Individual</a>"]
  class Company["<a href='company.md'>Company</a>"]
  class PartyRole["<a href='party_role.md'>Party Role</a>"]
  class ContactAddress["<a href='contact_address.md'>Contact Address</a>"]
```
````

**Entity with co-located enum values (example):**

````markdown
```mermaid
---
config:
  layout: elk
---
classDiagram
  class CustomerPreferences{
    * Preference Identifier : string
    Contact Method Preference : enum~ContactMethodPreference~
  }

  class ContactMethodPreference{
    <<enumeration>>
    Email
    SMS
    Phone
  }
```
````

### **Entity Definition**

A structured block defines the entity's attributes and logic. MD‑DDL follows a Key-as-Name philosophy to eliminate redundancy and ensure that the human-readable label used in the documentation is the exact same identifier used in the Knowledge Graph.:

````markdown
```yaml
extends: Party Role
mutability: immutable | append_only | slowly_changing | frequently_changing | reference
existence: independent | dependent | associative
temporal:
  tracking: valid_time
  description: Preferences are valid for specific time periods and can be future-dated
attributes:
  Customer Number:
    type: string
    identifier: true
  Email Address:
    type: string
    pii: true
  Full Name:
    type: string
  Balance:
    type: Decimal
```

```yaml
constraints:
  Valid Date Range:
    check: "End Date > Start Date"
  Positive Liquidity:
    check: "Balance > 0"
```

```yaml
governance:
  pii: true
  retention: 7 years
  access_role: HR_ADMIN
  classification: Confidential
```
````

### The "Key-as-Name" Principle

By using the business term (e.g., Positive Liquidity) as the YAML key rather than a nested property (e.g., name: Positive Liquidity), we achieve:

- Semantic Uniqueness: Every constraint and attribute is forced to have a distinct, meaningful identity within its context.
- Reduced Friction: There is no "translation layer" between the documentation and the database schema. What you see in the heading or key is what appears in the Graph node.
- Logical Referencing: Sub-entities that inherit from this entity can specifically override or reference a constraint by its key name, allowing for a cleaner "Logic Lineage."

### Temporal Tracking Types

This optional section defines how temporal tracking is applied to the entity. This is optional and will default to current state tracking if not specified or inherit from parent entities if they have temporal tracking defined.

Type|Description|Generation Guidance
----|-----------|-------------------
`valid_time`|Business time - when is this true in the real world?|Adds effective/expiration date columns, supports point-in-time queries
`transaction_time`|System time - when was this recorded?|Adds created/superseded timestamps, immutable records
`bitemporal`|Both valid and transaction time|Adds both sets of columns, full temporal reconstruction
`point_in_time`|Event timestamp only|For events - single timestamp, immutable

### Existence

This optional section defines if this entity can exist independently.

- independent — meaningful on its own; doesn't require another entity to give it purpose (Customer, Product, Location)
- dependent — only meaningful in the context of other entities; its reason for existing is to record a relationship between them (Payment Transaction, Order Line, Enrolment)
- associative — resolves a many-to-many; carries attributes about the relationship itself (Party Agreement, Student Course Enrolment)

The generating agent uses this to decide whether to create a candidate dimension or candidate fact. Associative signals a bridge in dimensional models.

### Mutability

This optional section defines how the data changes over time.

- immutable — once written, never changes (event records, ledger entries)
- append_only — new rows added, existing rows never updated (logs, transactions)
- slowly_changing — changes occasionally, history may matter (customer address, product category)
- frequently_changing — changes often, current value is what matters (account balance, inventory level)
- reference — essentially static, managed by a small number of administrators (country codes, currency codes)

The generating agent sees immutable or append_only and knows this belongs at the centre of a star. It sees slowly_changing and knows to apply SCD logic. It sees reference and knows to generate a small lookup table.

---

### Attribute Definition

#### Attribute Properties

Property|Required|Description|Example
--------|--------|-----------|-------
`type`|Yes|The data type of the attribute|`string`, `integer`, `decimal`, `boolean`, `date`, `datetime`, `timestamp`, `string[]`, `enum:Loyalty Tier`
`description`|No|Human-readable explanation of the attribute's purpose|"The primary email address for customer communication"
`identifier`|No|Marks this attribute as an identifier (default: `false`). Values: `primary`, `alternate`, `natural`, `surrogate`|`primary`, `alternate`
`unique`|No|Whether values must be unique across all instances (default: `false`)|`true` or `false`
`default`|No|Default value when not explicitly provided|`0`, `"Unknown"`, `false`

#### Type System

Type|Description|Examples
----|-----------|--------
`string`|Text data.|"John Doe", "abc123"
`integer`|Whole numbers without decimals|42, -17, 0
`decimal`|Numeric values with decimal precision|99.99, -0.001, 3.14159
`boolean`|True or false values|`true`, `false`
`date`|Calendar date without time|2024-03-15
`datetime`|Date with time (timezone-aware)|2024-03-15T14:30:00Z
`enum:<Enum Name>`|Reference to a defined enumeration|`enum:Loyalty Tier`, `enum:Country Code`

#### Arrays

All types above support arrays by appending `[]` to the type name. For example, `string[]` or `decimal[]`

Array constraints can be specified in the square brackets. For example, `string[1..5]` means 1 to 5 strings. `decimal[0..*]` means 0 or more decimals. `enum:Country Code[2]` means exactly 2 country codes.

- Valid cardinality syntax: `[n]`, `[n..m]`, `[n..*]`, or `[*]`
- If no cardinality is provided, `[*]` is assumed.

### Constraint Definition

Constraints define validation rules and business logic that span one or more attributes. They appear under a `constraints:` section in the entity or relationship YAML.

#### Constraint Properties

Property|Purpose|Example
--------|-------|-------
`unique`|Enforce uniqueness of one or more attributes|`unique: Email Address` or `unique: [Country, State, Postal Code]`
`not_null`|Require attribute to have a value|`not_null: Email Address` or `not_null: [First Name, Last Name]`
`check`|Boolean expression that must be true|`check: "Age >= 18"`
`derived`|Define computed/calculated attributes|`derived: {attribute: Full Name, expression: "First Name + ' ' + Last Name"}`
`lifecycle_stage`|Enforce completeness at specific lifecycle stages|`lifecycle_stage: [Registration, KYC Complete]`
`description`|Human-readable explanation|"Customer must be 18 or older"

One of unique, not_null, check, or derived must be present.

Example:

```yaml
constraints:
  Contact Information Required:
    not_null: [Email Address, Phone Number]
    lifecycle_stage: Activation
    description: At least one contact method must be provided at activation
```

---

### Rules

**Inheritance:**

- Attribute Inheritance: Customer gets all attributes of Party Role
- Constraint Inheritance: If Party Role has a constraint, Customer must follow it.
- Governance Inheritance: Entities inherit governance/compliance metadata from the domain. Do not repeat identical governance attributes in entity detail files; include a `governance:` block only for overrides.

**Identifiers:**

Every Entity should have at least one attribute marked identifier: true. If missing, the Knowledge Graph treats the entity as a "Logic Object" rather than a "Data Object."

**No Relationship Attributes:**

Explicitly forbid Customer Id appearing inside a Preference entity YAML. Instead, the Relationships section handles the link. This prevents "Foreign Key Drift."

**No Source References in Entity Files:**

Entity YAML contains no `source:` keys, no source field names, and no references to source systems. The canonical model defines meaning and governance; source systems define operational reality. This separation is enforced structurally — source mappings are declared under domain-local source folders (for example `sources/salesforce-crm/source.md` and related transform files). See [Section 7 — Sources](./7-Sources.md).

#### **Naming Rules**

- Natural Language Priority: Entity and attribute names must use natural language (e.g., Email Address, not email_addr).
- Case & Spaces: Names are case-sensitive and support spaces.
- No Redundancy: Do not include a name: field inside the YAML block. The Markdown heading serves as the Entity name, and the YAML keys serve as Attribute/Constraint names.
- Machine Normalisation: While the Knowledge Graph preserves these natural labels for navigability, physical artifact generation automatically handles the normalisation (e.g., conversion to snake_case) for target systems.
- Source Field Names are the one place in MD-DDL where non-natural-language identifiers appear. They are declared in source-folder transform files under `sources/<system>/transforms/`, not in entity definitions. They are owned by the source system and are not subject to MD-DDL's naming rules.

---

...next: [Enums](4-Enumerations.md)

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

---

...next: [Relationships](5-Relationships.md)

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

## **Events**

Each file must declare which domain it is part of by starting with a Level 1 heading with the domain name.

Events represent meaningful business-level changes in state. They describe *what happened* in the domain, independent of how the underlying data systems record or transport those changes. Events allow MD‑DDL to map technical change (CDC, ETL deltas, logs) to **semantic business events**, ensuring that business processes react to meaning rather than database mechanics.

---

### **Event Declaration**

An event is declared using a **level‑3 Markdown heading** under the `## Events` section:

```markdown
## Events

### Customer Preference Updated
```

The heading is the authoritative name of the event.  
Event names use **natural language**, not camelCase, PascalCase, or snake_case.

---

### **Event Description**

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

### **Event Definition**

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
   classification: Confidential
```
````

---

### **Event Rules**

1. **Natural‑language naming**  
   Event names must be written in natural language (e.g., “Customer Preference Updated”).

2. **No duplication**  
   The event name appears only in the heading, not inside the YAML block.

3. **Events are first‑class citizens**  
   Events are not embedded inside entities or relationships; they live in their own section.

4. **Events describe business meaning, not technical mechanics**  
   Events should not reference CDC, SQL operations, or ETL logic.

5. **Events may appear in any file**  
   As long as the file begins with the domain's level‑1 heading, they will be discovered and assembled.

6. **Events may be linked to entities and relationships**  
   Through `actor`, `entity`, and optional `relationships`.

7. **Events are optional**  
   Domains may define zero, one, or many events.

8. **Contextual Payloads**

   The attributes block should focus on the delta (what changed) and the context (why it changed), rather than a full copy of the entity.

9. **Temporal Priority**
   Every event MUST have a timestamp or a sequence attribute to ensure the Knowledge Graph can reconstruct the timeline of an entity's life.

10. **Governance Inheritance**
   Events inherit governance/compliance metadata from the domain. Include a `governance:` block only when an event requires an override.

---

### **Example Event**

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

*Part of the MD‑DDL Specification. See [1-Foundation.md](./1-Foundation.md) for core principles and document structure.*

---

## **Sources**

A Source in MD-DDL represents a system that generates operational change — a CRM, a core banking system, a payment platform, an ERP. Sources are not owners of data. They are systems of change whose outputs feed canonical data products.

The canonical domain model defines meaning. Sources define operational reality. The Source File is the contract that translates between them.

This separation is deliberate and load-bearing:

- Domain modellers define canonical entities, attributes, and governance without knowing or caring which source systems produce the underlying data.
- Source system SMEs define field-level mappings and encode source idiosyncrasies without needing to understand the canonical model's governance posture.
- Integration engineers own transform files that connect the two worlds.

**Canonical data products replace the concept of Systems of Record.** There is no attribute in a domain entity that is "owned" by Salesforce or SAP. Those systems generate change events. The canonical model absorbs those changes according to rules declared in source-folder transform files.

---

### **Source Structure**

Sources are self-contained within each domain. Each source system has a folder under `sources/` containing a `source.md` router file and a `transforms/` subfolder for optional transform detail files.

```text
Financial Crime/
  domain.md
  entities/
  sources/
    salesforce-crm/
      source.md             ← source metadata + domain feed table
      transforms/
        table_account.md
        table_contact_point.md
    sap-fraud-management/
      source.md
      transforms/
        table_alert_case.md
    temenos-payment/
      source.md
      transforms/
        table_account_ref.md
```

The source file is the router — it declares what the source system is, how it generates change, and how it contributes to the current domain. Transform files remain the optional detail layer for field-level mappings using the transformation types defined in Section 8.

Transform file names are based on the source table and must follow this pattern:

`table_<source-table>.md`

Examples: `table_account.md`, `table_contact_point.md`, `table_payment_event.md`.

If multiple canonical entities map from the same source table, they should be grouped in the same transform file under separate level-2 entity headings.

#### File Organisation

A source may split transform definitions across as many files as needed. The natural split is one transform file per source table. For large, complex source systems, transform files may be further subdivided by functional area. If used, transform files are stored under the source folder's `transforms/` subfolder and every transform file must begin with a level-1 heading linking back to `../source.md`.

```text
Financial Crime/
  sources/
    salesforce-crm/
      source.md
      transforms/
        table_account.md       ← Account table mappings for Party/Company/Customer
        table_contact_point.md
    sap-fraud-management/
      source.md
      transforms/
        table_alert_case.md
```

---

### **Source File**

#### Declaration

A source file is declared using a level-1 Markdown heading:

```markdown
# Salesforce CRM
```

The heading is the source's display name. The stable machine identifier lives in the metadata block.

#### Description

Free-text Markdown under the H1 and before the first H2 describes the source system's business role — what it does, who operates it, and why it is a source for the canonical model. This is written for domain modellers and data stewards, not for engineers.

#### Metadata

Metadata appears under a level-2 heading:

```markdown
## Metadata
```

```yaml
id: salesforce
owner: crm-platform@bank.com
steward: data.governance@bank.com

# How this system generates change
change_model: real-time-cdc
change_events:
  - Customer Updated
  - Contact Created
  - Account Merged
  - Account Deactivated

# Operational characteristics
update_frequency: real-time
data_quality_tier: 1          # 1 = high trust, 2 = standard, 3 = requires validation
status: Production
version: "2.1.0"

tags:
  - CRM
  - CustomerData
  - Core
```

##### Change Models

The `change_model` field declares how change flows out of the source system.
This guides the pipeline pattern to generate.

Value | Description | Generated pipeline pattern
--- | --- | ---
`real-time-cdc` | Change Data Capture — row-level changes streamed in real time | Streaming pipeline
`event-driven` | Source publishes business events (not raw CDC) | Event consumer
`batch-daily` | Full or incremental extract on a daily schedule | Scheduled ETL
`batch-intraday` | Multiple batch extracts within a day | Scheduled ETL with frequency
`api-poll` | Changes retrieved by polling a source API | API ingestion job
`manual` | Data loaded by human intervention; no automated feed | Manual load template

##### Change Events

`change_events` lists the business-level change events this source emits. These are natural-language names that may correspond to Events declared in the canonical domain. They can be used to generate event subscription logic and to link source changes to downstream domain Events.

##### Data Quality Tier

`data_quality_tier` is a governance signal, not a technical score. It tells the canonical model how much trust to extend to values from this source:

Tier | Meaning
--- | ---
`1` | High trust — well-governed source, low null rates, consistent formats
`2` | Standard — typical operational system; some nulls, occasional quirks
`3` | Low trust — legacy system, known quality issues; requires validation rules

The tier does not prevent a source from contributing to canonical entities. It signals to downstream consumers and data quality rules how to treat values originating from this source.

---

#### Domain Feed Sections

Below the metadata block, a source file declares the feed table for its owning domain using this heading pattern:

```markdown
## [<Domain Name>](../../domain.md) Feeds
```

Example domain feed section:

```markdown
## [Financial Crime](../../domain.md) Feeds

Canonical Entity | Transform File | Attributes Contributed | Change Model
--- | --- | --- | ---
[Party](../../entities/party.md#party) | [table_account](transforms/table_account.md) | Party Identifier, Party Status | real-time-cdc
[Customer](../../entities/customer.md#customer) | [table_account](transforms/table_account.md) | Customer Number, Onboarding Date, Segment | real-time-cdc
```

**Domain feed table columns:**

Column | Purpose
--- | ---
**Canonical Entity** | Link to the entity in the target domain this source contributes to.
**Transform File** | Link to a `transforms/table_<source-table>.md` transform file in the same source folder, or `TBD` if not yet defined.
**Attributes Contributed** | Comma-separated list of the canonical attributes this source populates. Not every attribute needs to come from this source.
**Change Model** | How changes to this entity flow from this source. May differ per entity if the source uses different mechanisms for different record types.

---

#### Source Overview Diagram

A source file should include a Mermaid diagram showing which canonical entities the source feeds and what kind of change model applies to each.

````markdown
### Source Overview Diagram

```mermaid
---
config:
  layout: elk
---
graph LR
  Salesforce --> |real-time-cdc| Customer
  Salesforce --> |real-time-cdc| ContactAddress
  Salesforce --> |event-driven| CustomerPreferences

  Customer["<a href='../../domains/customer/entities/customer.md'>Customer</a>"]
  ContactAddress["<a href='../../domains/customer/entities/contact_address.md'>Contact Address</a>"]
  CustomerPreferences["<a href='../../domains/customer/entities/customer_preferences.md'>Customer Preferences</a>"]
```
````

---

### **Transform Files**

#### Transform Files Declaration

Every transform file begins with a level-1 heading that names the source system and links back to `../source.md`:

```markdown
# [Salesforce CRM](../source.md)
```

#### Structure

Transform files are source-table documents. Each file begins with a level-2 heading naming the source table (for example `## Account`, `## ContactPoint`) followed by a source schema table.

Required source schema table columns:

Column | Purpose
--- | ---
**Pos** | Column ordinal from the source table.
**Column Name** | Physical source column name.
**Data Type** | Source system type.
**Max Len** | Maximum length for string-like columns.
**Precision** | Numeric precision when applicable.
**Scale** | Numeric scale when applicable.
**Nulls** | Whether source column allows nulls.
**Comment** | Source-system context or business notes.
**Destination** | Canonical destination mapping (`Entity.Attribute`) or a same-file link to a rule section for non-direct mappings.

When mapping is direct, the `Destination` cell is sufficient and no additional YAML rule is required. Use a level-3 rule section only for non-direct mappings such as `conditional`, `derived`, `lookup`, `reconciliation`, or `aggregation`.

Rules are still expressed with level-3 headings and YAML blocks. Rule links in the `Destination` column must point to anchors in the same file (for example `[Map Party Status](#map-party-status)`).

Transform files may include multiple canonical entities when mappings originate from the same source table.

Example level-2 heading:

```markdown
## Account
```

For non-direct mappings, use a level-3 rule heading following the Key-as-Name principle. The heading is the transformation's identity in the Knowledge Graph and must be unique within the transform file.

#### Source field references

Within a transform file, all field references are scoped to the owning source system. The `system:` key is **not** required — it is implicit. Only the field path within the source is needed:

```yaml
source:
  field: Contact.Email
```

This keeps transform files clean and makes them portable if a source system is renamed. The source file's `id` field is the authoritative system identifier.

#### Target notation

The `target` field uses `Entity · Attribute` notation to identify the canonical destination unambiguously:

```yaml
target: Customer · Email Address
```

The entity name must match an entity declared in the canonical domain model. The attribute name must match an attribute declared in that entity's YAML block. Both are validated during generation.

#### Transformation types

Transform files use the transformation types defined in [Section 8 — Transformations](./8-Transformations.md). All type-specific YAML
syntax is unchanged. The only differences from Section 8's syntax are:

- `system:` is omitted from all `source:` blocks (implicit from file location)
- `target:` uses `Entity · Attribute` notation instead of bare attribute name
- The H3 heading is the transformation identity (Key-as-Name, as elsewhere)

---

#### **Source Idiosyncrasies**

Transform files are the right place to encode source-specific data quality characteristics that the canonical model should never need to know about.

##### Null representations

Many source systems represent null as a non-null value (`"N/A"`, `"0"`, `"UNKNOWN"`). Declare this on the source block so that appropriate null normalisation logic is generated:

```yaml
source:
  field: Contact.Email
  null_as: "N/A"
```

##### Quality flags

Attribute-level quality signals that should be carried into the canonical model:

```yaml
source:
  field: Customer.DateOfBirth
  quality: nullable           # may legitimately be absent
  quality_note: "DOB not collected pre-2015; backfill in progress"
```

##### Format normalisation

Source-specific format variations that require standardisation:

```yaml
source:
  field: Customer.PhoneNumber
  normalise: e164             # normalise to E.164 international format
```

```yaml
source:
  field: Account.OpenDate
  format: "DD/MM/YYYY"        # source uses non-ISO date format
  cast: date                  # generates format-aware cast
```

These annotations belong in the transform file, not in the canonical entity definition. The canonical model defines what the attribute means; the transform file handles the operational reality of getting clean data there.

---

### **Complete Example**

#### Source file

````markdown
# Salesforce CRM

The primary CRM system used by Retail Banking. Salesforce is the operational system for all customer relationship management — onboarding, contact management, preference capture, and relationship history. It generates real-time CDC events for all customer record changes.

## Metadata

```yaml
id: salesforce
owner: crm-platform@bank.com
steward: data.governance@bank.com
change_model: real-time-cdc
change_events:
  - Customer Created
  - Customer Updated
  - Contact Updated
  - Account Deactivated
data_quality_tier: 1
status: Production
version: "2.1.0"
tags:
  - CRM
  - CustomerData
  - Core
```

### Source Overview Diagram

```mermaid
---
config:
  layout: elk
---
graph LR
  Salesforce --> |real-time-cdc| Customer
  Salesforce --> |real-time-cdc| ContactAddress
  Salesforce --> |event-driven| CustomerPreferences

  Customer["<a href='../../domains/customer/entities/customer.md'>Customer</a>"]
  ContactAddress["<a href='../../domains/customer/entities/contact_address.md'>Contact Address</a>"]
  CustomerPreferences["<a href='../../domains/customer/entities/customer_preferences.md'>Customer Preferences</a>"]
```

## [Financial Crime](../../domain.md) Feeds

Canonical Entity | Transform File | Attributes Contributed | Change Model
--- | --- | --- | ---
[Party](../../entities/party.md#party) | [table_account](transforms/table_account.md) | Party Identifier, Party Status | real-time-cdc
[Customer](../../entities/customer.md#customer) | [table_account](transforms/table_account.md) | Customer Number, Email Address, Full Name, Date of Birth | real-time-cdc
[Contact Address](../../entities/contact_address.md#contact-address) | [table_contact_point](transforms/table_contact_point.md) | Street, City, Postal Code, Country Code | real-time-cdc
````

#### Transform file — `sources/salesforce-crm/transforms/table_contact.md`

````markdown
# [Salesforce CRM](../source.md)

## Customer

Salesforce is the primary contributor to the Customer canonical entity for all contact and identity attributes. Financial attributes (balance, credit limit) are contributed by the Core Banking System.

### Map Customer Number
Direct map from the Salesforce Account identifier.

```yaml
type: direct
target: Customer · Customer Number
source:
  field: Account.AccountNumber
```

### Concatenate Full Name
Salesforce stores given and family name separately. The canonical model uses a single Full Name attribute.

```yaml
type: derived
target: Customer · Full Name
expression: "trim(First Name) + ' ' + trim(Last Name)"
inputs:
  First Name:
    field: Contact.FirstName
  Last Name:
    field: Contact.LastName
```

### Map Email Address
Salesforce uses "N/A" as a null representation for missing email addresses.

```yaml
type: direct
target: Customer · Email Address
source:
  field: Contact.Email
  null_as: "N/A"
  quality: nullable
```

### Resolve Country Code
Salesforce stores legacy two-character country codes. The canonical model uses ISO 3166-1 alpha-3.

```yaml
type: lookup
target: Customer · Country Code
source:
  field: Contact.MailingCountry
lookup:
  reference: Country Code
  match_on: Abbreviation
  return: ISO Code
fallback: null
```

### Map Date of Birth
Salesforce uses DD/MM/YYYY format for dates. Generation produces a format-aware cast to the canonical date type.

```yaml
type: direct
target: Customer · Date of Birth
source:
  field: Contact.Birthdate
  format: "DD/MM/YYYY"
  cast: date
```
````

---

### **Source Rules**

1. **Source identity is stable.** The `id` in `source.md` metadata is a breaking-change identifier. Renaming requires a coordinated update across the source folder and references in the domain file.

2. **Canonical entities stay pure.** Entity detail files in the domain model contain no source references. The canonical model defines meaning; sources define operational reality. This separation is non-negotiable.

3. **Transform files are source-folder scoped.** A transform file belongs to exactly one source folder and one domain context. Cross-source reconciliation (where multiple sources contribute to the same attribute) is expressed using the `reconciliation` transformation type within a transform file, listing the contributing sources explicitly.

4. **Source idiosyncrasies stay in transform files.** Null representations, format quirks, quality notes, and encoding variations belong in the `source:` block of the relevant transform. They do not propagate into the canonical entity definition.

5. **Domain feed section is authoritative.** If an attribute is listed in a feed table but has no corresponding transformation in the same source folder, this is a validation error. If a transformation exists in the source folder but the entity is not listed in the feed table, this is a warning.

6. **Change events may link to domain Events.** When a source's `change_events` list contains an event whose name matches a domain Event, event subscription logic can be generated. This linkage is by name — no explicit reference key is required.

*Part of the MD‑DDL Specification. See [1-Foundation.md](./1-Foundation.md) for core principles and document structure.*

---

## **Transformations**

Each file must declare which domain it is part of by starting with a Level 1 heading with the domain name.

Transformations define how source system data is shaped and mapped into domain entities. They make the lineage from raw source field to governed domain attribute explicit, human-readable, and actionable by AI agents.

Transformations are **first-class citizens** of the Source layer. They are declared in source folders under `sources/<system>/transforms/` (see [Section 7 — Sources](./7-Sources.md)), not in domain entity files. The canonical domain model contains no source references — it defines meaning, not origin.

**This section defines the transformation type vocabulary** — the available types, their YAML syntax, and the expression language. Where transformations are declared and how they are organised is defined in Section 7.

---

### **What Transformations are not**

- **Not constraints.** A constraint defines what valid data looks like once it arrives in the domain. A transformation defines how data gets there. Keep them separate.
- **Not orchestration.** When a transformation runs, in what order, triggered by which event — that is a pipeline concern. MD-DDL declares the logic; the generating agent produces the pipeline artefact.
- **Not documentation of existing pipelines.** Transformations define the *intended* mapping as the source of truth. Existing pipelines should be aligned to the model, not the other way around.

---

### **Transformation Declaration**

Transformations are declared in source-table transform files. Each file uses a level-2 heading for the source table and a source schema table that maps columns to destinations:

```markdown
## Account

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | ExternalPartyId | Text | 40 | | | no | Account-scoped party id | Party.Party Identifier
2 | RecordStatus | Text | 20 | | | yes | Record lifecycle status | [Map Party Status](#map-party-status)
```

Each non-direct transformation in that file uses a **level-3 heading** following the Key-as-Name principle — the heading is the transformation's identity in the Knowledge Graph:

```markdown
### Concatenate Name Parts
```

A short prose description of the business intent follows the heading, before the YAML block. See [Section 7 — Sources](./7-Sources.md) for the full transform file structure.

Transform files must be named for the source table using the `table_<source-table>.md` pattern. If multiple canonical entities are mapped from the same source table, they can coexist in one file.

The `Destination` column controls rule verbosity:

- Direct mapping: use `Entity.Attribute` directly in the `Destination` cell.
- Non-direct mapping: link to a same-file rule section (for example `[Map Party Status](#map-party-status)`) and define the YAML rule under that heading.

---

### **Transformation Definition**

All transformations share a common envelope:

```yaml
type: <transformation type>
target: Entity · Attribute
```

`type` and `target` are always required. Everything else depends on the type.

`target` uses `Entity · Attribute` notation. The entity name must match an entity in the canonical domain model. The attribute name must match an attribute declared in that entity's YAML block. Both are validated during generation.

Within a transform file, `source.system` is **omitted** — it is implicit from the file's location under `sources/<system>/transforms/`. Only the field path within the source system is declared:

```yaml
source:
  field: Contact.Email
```

See [Section 7 — Sources](./7-Sources.md) for the source idiosyncrasy annotations (`null_as`, `quality`, `format`, `normalise`) available on `source:` blocks.

---

### **Transformation Types**

#### `direct`

A one-to-one field map with an optional type cast. Use when the source field and domain attribute are semantically identical but may differ in name or type.

````yaml
### Account Number
Maps the legacy account identifier from the core banking system.

```yaml
type: direct
target: Account Number
source:
  system: cbs
  field: ACCT_MASTER.ACCT_NO
  cast: string
```
````

`cast` is optional. Valid values match the MD-DDL type system:
`string`, `integer`, `decimal`, `boolean`, `date`, `datetime`.

---

#### `derived`

Computes a domain attribute from one or more source fields using an expression.
Inputs are named and declared separately from the expression so they can be
individually traced.

````markdown
### Full Name
Combines given and family names from CRM into a single display name.

```yaml
type: derived
target: Full Name
expression: "trim(First Name) + ' ' + trim(Last Name)"
inputs:
  First Name:
    system: salesforce
    field: Contact.FirstName
  Last Name:
    system: salesforce
    field: Contact.LastName
```
````

**Expression syntax** uses natural-language input names as operands, matching
the keys declared in `inputs:`. Supported operations:

Operation | Syntax | Example
--- | --- | ---
Concatenation | `+` | `"First Name + ' ' + Last Name"`
Arithmetic | `+` `-` `*` `/` | `"Amount * Exchange Rate"`
String functions | `trim()`, `uppercase()`, `lowercase()`, `substring(n, m)` | `"trim(Email Address)"`
Date functions | `today()`, `date_diff(a, b, unit)`, `date_add(d, n, unit)` | `"date_diff(End Date, Start Date, 'days')"`
Null handling | `coalesce(a, b)` | `"coalesce(Preferred Name, First Name)"`

The generating agent is responsible for translating these expressions into the target physical syntax (SQL, Spark, dbt). Authors write expressions against domain attribute names, not physical column names.

---

#### `reconciliation`

Resolves a domain attribute when the same data exists in multiple source systems and a priority rule determines which value to use.

````markdown
### Preferred Email Address
CRM is the master for contact data. The ERP value is used only when CRM has no email on record.

```yaml
type: reconciliation
target: Email Address
strategy: priority_non_null
sources:
  - priority: 1
    system: salesforce
    field: Contact.Email
  - priority: 2
    system: sap
    field: Customer.EmailAddress
```
````

**Reconciliation strategies:**

Strategy | Behaviour
--- | ---
`priority_non_null` | Take the highest-priority non-null value
`priority_always` | Always take the highest-priority value, even if null
`most_recent` | Take the value with the most recent timestamp; requires `timestamp_field` on each source
`consensus` | Take a value only when all sources agree; otherwise null

For `most_recent`, declare the timestamp field on each source:

```yaml
sources:
  - priority: 1
    system: salesforce
    field: Contact.Email
    timestamp_field: Contact.LastModifiedDate
```

---

#### `lookup`

Enriches a source value by joining to a domain enum or reference entity.
Use when the source system uses codes, abbreviations, or legacy identifiers
that the domain model has standardised.

````markdown
### Resolve Country Code
Translates two-character legacy country abbreviations from the core banking system into ISO 3166-1 alpha-3 codes used in the domain model.

```yaml
type: lookup
target: Country Code
source:
  system: cbs
  field: Customer.CountryAbbrev
lookup:
  reference: Country Code
  match_on: Abbreviation
  return: ISO Code
fallback: null
```
````

`reference` must name a domain Enum or Entity defined in the same model. `match_on` and `return` must be valid attribute or value names within that reference. `fallback` declares what to do when no match is found: `null`, `reject` (fail the record), or a literal default value.

---

#### `conditional`

Maps a source value to domain values using explicit threshold or rule cases.
Each case key is a valid domain attribute value or enum value.

````markdown
### Classify Customer Risk
Derives the domain risk tier from the raw numeric risk score produced by
the transaction monitoring system.

```yaml
type: conditional
target: Risk Rating
source:
  system: tms
  field: Customer.RiskScore
cases:
  Low:        "RiskScore < 30"
  Medium:     "RiskScore >= 30 AND RiskScore < 70"
  High:       "RiskScore >= 70 AND RiskScore < 90"
  Prohibited: "RiskScore >= 90"
fallback: null
```
````

Case keys must be valid values of the attribute's declared type. If `target` is an `enum:` type, case keys must be valid enum values. `fallback` behaves identically to the lookup type.

---

#### `aggregation`

Collapses multiple source rows into a single domain attribute value. Use when the source system operates at a finer grain than the domain entity.

````markdown
### Total Outstanding Balance
Sums all active loan disbursement records from the core banking system
to produce the entity-level balance figure.

```yaml
type: aggregation
target: Outstanding Balance
function: sum
source:
  system: cbs
  field: Loan_Disbursements.DisbursedAmount
filter: "Loan_Disbursements.Status == 'Active'"
grain:
  entity: Loan Agreement
  join_on: Loan Agreement Number
```
````

`function` supports: `sum`, `count`, `count_distinct`, `min`, `max`, `average`, `first`, `last`.

`grain` declares which entity this aggregation rolls up to and the join key. The `entity` value must match an entity name in the domain model. The `join_on` value must match an attribute name on that entity.

`filter` is optional. It applies before aggregation.

---

### **Transformation Rules**

1. **Key-as-Name:** The H3 heading is the transformation's identity in the Knowledge Graph. It must be unique within the file and is the authoritative name used in lineage tracing and generated output.

2. **Target must exist:** The entity and attribute in `target` must be declared in the canonical domain model. Both the entity name and the attribute name are validated during generation.

3. **Source system is implicit:** Within a transform file, the source system is not declared on individual transformations — it is inherited from the file's location. Source idiosyncrasies (`null_as`, `quality`, `format`) are declared on the `source:` block within the transformation.

4. **One mapping path per canonical attribute per source table:** Use exactly one `Destination` entry per target attribute from a given source table. If mapping is non-direct, the `Destination` entry must link to a single rule section that defines the logic.

5. **No transformation logic in constraints:** Constraints validate; they do not transform. The transformation defines the inbound mapping; the constraint defines the validation rule on the result.

6. **Expression operands use domain attribute names:** In `derived` expressions, operands match the keys declared in `inputs:`, not raw source field names. This keeps expressions readable and decoupled from physical source schema.

7. **Transformations are optional:** A `source.md` file may exist without additional transform files if the source is declared but mappings have not yet been authored. Transform files are added when integration lineage is needed.

---

### **Generation Behaviour**

AI agents use transformation definitions to generate:

- **ETL / ELT logic** — SQL `SELECT` statements, dbt models, or Spark transformations depending on the target platform
- **Lineage graph edges** — source field → transformation → domain attribute nodes in the Knowledge Graph
- **Data quality test stubs** — one test per transformation, asserting the target attribute is non-null after the transformation runs (override with `quality_check: false` on the transformation if the null case is valid)
- **Source-to-domain mapping documentation** — a human-readable crosswalk table per entity, generated from all inline and named source mappings

---

### **Example — Transform file excerpt**

See [Section 7 — Sources](./7-Sources.md) for the complete transform file example. The following shows the transformation type syntax in context:

````markdown
# [Salesforce CRM](../source.md)

## Customer

### Concatenate Full Name
```yaml
type: derived
target: Customer · Full Name
expression: "trim(First Name) + ' ' + trim(Last Name)"
inputs:
  First Name:
    field: Contact.FirstName
  Last Name:
    field: Contact.LastName
```

### Resolve Country Code
```yaml
type: lookup
target: Customer · Country Code
source:
  field: Contact.MailingCountry
  null_as: null
lookup:
  reference: Country Code
  match_on: Abbreviation
  return: ISO Code
fallback: null
```
````

*Part of the MD‑DDL Specification. See [1-Foundation.md](./1-Foundation.md) for core principles and document structure.*

---

## **Data Products**

A Data Product in MD-DDL is a governed, publishable unit of data that serves a specific audience. Data products are the bridge between the canonical domain model and the consumers of that model — analytics teams, downstream systems, regulatory reports, and operational dashboards.

Data products do not duplicate the domain model. They declare what subset of the model is published, in what shape, for whom, and under what governance. The canonical entities, relationships, and events remain the single source of truth; data products are curated projections of that truth.

---

### **Why Data Products Are First-Class**

Without data products, the gap between a well-modelled domain and a usable output is filled by undocumented views, ad-hoc queries, and shadow pipelines. Data products close that gap by making the publication contract explicit:

- **What** is published (which entities, attributes, relationships)
- **How** it is shaped (normalized, denormalized, aggregated)
- **Who** consumes it (team, system, or regulatory body)
- **Why** it exists (business purpose and SLA)

By declaring data products in the same Markdown-native format as the rest of the model, MD-DDL ensures that publication intent is version-controlled, reviewable, and traceable from source through canonical model to consumer.

---

### **Data Product Classes**

MD-DDL defines three classes of data product, each serving a distinct purpose in the data lifecycle. These classes are not tiers or layers — they are independent publication intents that may coexist within a single domain.

#### Source-Aligned

A source-aligned product publishes raw or lightly cleansed data from a single source system. It preserves the source schema and change model, making operational data available for audit, replay, and debugging without interpretation.

- **Scope:** Single source system within the domain
- **Shape:** Mirrors source structure; no joins across sources
- **Governance:** Inherits domain defaults; typically lower classification than domain-aligned products
- **Consumers:** Data engineers, audit teams, integration debugging
- **Cross-domain dependencies:** None — source-aligned products are self-contained within a domain

Source-aligned products reference a source system declared in the domain's `## Source Systems` section. Their schema corresponds to the source table structure defined in `sources/<system>/source.md`.

#### Domain-Aligned

A domain-aligned product publishes the canonical model itself — governed entities, relationships, and events in their modelled form. It is the standard representation of the domain's truth, ready for consumption by systems that understand the canonical schema.

- **Scope:** One or more canonical entities within the owning domain
- **Shape:** Matches the canonical model structure (normalized or as-modelled)
- **Governance:** Inherits domain defaults; represents the highest-fidelity view
- **Consumers:** Domain services, master data consumers, cross-domain integration
- **Cross-domain dependencies:** None — domain-aligned products publish only concepts owned by the declaring domain

Domain-aligned products reference entities from the domain's `## Entities` section. Their schema corresponds directly to the entity YAML definitions and relationship structure.

#### Consumer-Aligned

A consumer-aligned product reshapes domain data for a specific audience or use case. It may denormalize, aggregate, filter, or combine entities to suit the consumer's query patterns and performance needs.

- **Scope:** One or more canonical entities, potentially from multiple domains
- **Shape:** Tailored to consumer needs — wide tables, star schemas, aggregated summaries
- **Governance:** Inherits domain defaults with possible overrides (e.g., PII masking, restricted retention)
- **Consumers:** Named team, application, report, or regulatory body
- **Cross-domain dependencies:** Permitted — consumer-aligned products may reference entities from other domains when the consumer's use case spans domain boundaries

Consumer-aligned products are the primary trigger for physical artifact generation. The `schema_type` declared on a consumer-aligned product determines which Agent Artifact skill produces the output.

---

### **Data Product Declaration**

A data product is declared using a **level-3 Markdown heading** inside a detail file stored in the `products/` subfolder of the domain:

```markdown
### Customer 360 Profile
```

The heading is the product's name — its identity in the Knowledge Graph.

#### Data Product Metadata

Product metadata is expressed as YAML inside a fenced code block immediately after the heading:

````markdown
### Customer 360 Profile

A denormalized wide-column view combining customer identity, preferences,
account summary, and risk indicators for the retail analytics team.

```yaml
class: consumer-aligned
schema_type: wide-column
owner: retail.analytics@example.com
consumers:
  - Retail Analytics Team
  - Customer Insights Dashboard
status: Production
version: "1.0.0"

entities:
  - Customer
  - Customer Preferences
  - Account
  - Party

governance:
  classification: Confidential
  pii: true
  retention: "5 years"
  masking:
    - attribute: "Date of Birth"
      strategy: year-only
    - attribute: "Tax Identification Number"
      strategy: hash
```
````

#### Required Metadata Fields

Field | Purpose
--- | ---
`class` | One of `source-aligned`, `domain-aligned`, `consumer-aligned`.
`owner` | The team or individual accountable for this product's correctness and availability.
`consumers` | List of named consumers — teams, systems, reports, or regulatory bodies.
`status` | Lifecycle state: `Draft`, `Production`, `Deprecated`.
`entities` | List of canonical entity names included in this product.

#### Optional Metadata Fields

Field | Purpose
--- | ---
`schema_type` | Physical output style: `normalized`, `dimensional`, `wide-column`, `knowledge-graph`. When declared, this drives Agent Artifact's skill selection for generation.
`version` | Semantic version of the product definition.
`governance` | Governance overrides that differ from domain defaults. Only declare fields that differ.
`masking` | Attribute-level masking rules for sensitive data. Each entry names the canonical attribute and a masking strategy.
`sla` | Service-level attributes (freshness, availability, latency).
`refresh` | Refresh cadence: `real-time`, `hourly`, `daily`, `weekly`, `on-demand`.
`cross_domain` | List of external domain references for consumer-aligned products that span domains. Each entry names the domain and entities consumed.

#### Source-Aligned Metadata

Source-aligned products include a `source` field instead of an `entities` field:

````markdown
### Salesforce CRM Raw Feed

Raw audit feed from Salesforce CRM preserving source schema and change events
for replay and integration debugging.

```yaml
class: source-aligned
source: salesforce-crm
owner: data.engineering@example.com
consumers:
  - Data Engineering
  - Audit & Compliance
status: Production

governance:
  classification: Internal
  retention: "3 years"
```
````

Field | Purpose
--- | ---
`source` | The source system identifier matching a folder under `sources/`. Used instead of `entities` for source-aligned products.

#### Cross-Domain References

Consumer-aligned products that span domain boundaries must declare their external dependencies explicitly using the `cross_domain` field:

````markdown
### Suspicious Activity Report

Combines financial crime transaction data with customer identity from the
Customer domain for SAR filing.

```yaml
class: consumer-aligned
schema_type: normalized
owner: compliance.team@example.com
consumers:
  - Regulatory Reporting System
  - FATF Compliance
status: Production

entities:
  - Transaction
  - Party
  - Party Role

cross_domain:
  - domain: Customer
    entities:
      - Customer
      - Customer Preferences
  - domain: Geography
    entities:
      - Country
      - Jurisdiction

governance:
  classification: Highly Confidential
  pii: true
  retention: "10 years"
```
````

Cross-domain references create edges in the Knowledge Graph linking the data product to entities it does not own. The owning domain retains governance authority over those entities — the consuming product inherits their governance posture unless explicit overrides are declared.

---

### **Masking Strategies**

When a data product exposes PII or sensitive attributes, `masking` entries define how those attributes are protected in the published output.

Strategy | Behaviour
--- | ---
`hash` | One-way hash of the value; preserves joinability across products using the same salt.
`redact` | Replace with a fixed placeholder (e.g., `***REDACTED***`).
`year-only` | For date attributes: retain the year, zero out month and day.
`truncate` | Retain a prefix of the value (e.g., first 3 characters of a postcode).
`tokenize` | Replace with a reversible token managed by a tokenization service.
`null` | Replace the value with null in the published output.

Masking is declared at the product level, not the entity level. The same entity may appear in multiple products with different masking rules depending on the consumer's access level.

---

### **Product-Driven Generation**

The `schema_type` field on a data product is the entry point for physical artifact generation. When an AI agent encounters a data product with a `schema_type`, it selects the corresponding Agent Artifact skill:

`schema_type` value | Agent Artifact skill | Output
--- | --- | ---
`normalized` | Normalized | DDL, JSON Schema, Parquet contract
`dimensional` | Dimensional | Star schema DDL
`wide-column` | Wide Column | Denormalized table DDL
`knowledge-graph` | Knowledge Graph | Cypher DDL

The product's `entities` list scopes the generation — only the declared entities and their relationships are included in the physical output. The product's `governance` and `masking` metadata are applied as constraints on the generated artifacts.

If no `schema_type` is declared, the product is a logical declaration only. It documents what is published but does not trigger physical generation.

---

### **SLA Declaration**

Products that serve operational consumers may declare service-level attributes:

```yaml
sla:
  freshness: "< 15 minutes"
  availability: "99.9%"
  latency_p99: "< 200ms"
```

SLA fields are informational — they document expectations but do not generate runtime enforcement. Monitoring and alerting are orchestration concerns outside MD-DDL's scope.

---

### **Two-Layer Structure**

Data products follow the same two-layer pattern as entities, relationships, and events:

1. **Summary** — A `## Data Products` table in the domain file listing all products with class, consumers, and status
2. **Detail** — Individual product definitions in `products/` detail files using level-3 headings and YAML blocks

This allows the domain file to act as a complete index of what the domain publishes, while detail files contain the full product specification.

#### Domain File Summary Table

The domain file includes a `## Data Products` section with a summary table:

Column | Purpose
--- | ---
**Name** | The product name, linked to its detail definition.
**Class** | `source-aligned`, `domain-aligned`, or `consumer-aligned`.
**Consumers** | Primary consumers of this product.
**Status** | Lifecycle state.

Example:

```markdown
## Data Products

Name | Class | Consumers | Status
--- | --- | --- | ---
[Customer 360 Profile](products/analytics.md#customer-360-profile) | consumer-aligned | Retail Analytics Team | Production
[Salesforce CRM Raw Feed](products/source-feeds.md#salesforce-crm-raw-feed) | source-aligned | Data Engineering | Production
[Canonical Party](products/canonical.md#canonical-party) | domain-aligned | Cross-domain Integration | Production
```

#### Detail File Structure

Product detail files follow the same structural rules as entity detail files:

- Begin with a level-1 heading naming the domain, linked back to the domain file
- Use level-2 heading `## Data Products`
- Define individual products under level-3 headings with YAML metadata blocks

```markdown
# [Financial Crime](../domain.md)

## Data Products

### Customer 360 Profile
...product definition...

### Transaction Risk Summary
...product definition...
```

---

### **Rules for Data Products**

1. **Class determines scope.** Source-aligned products reference a single source system. Domain-aligned products reference canonical entities within the owning domain. Consumer-aligned products may span domains.

2. **Cross-domain only for consumer-aligned.** Only consumer-aligned products may declare `cross_domain` references. Source-aligned and domain-aligned products are self-contained within their domain.

3. **Entities must exist.** Every entity listed in `entities` must be declared in the domain's `## Entities` table (or in a referenced domain for `cross_domain` entries).

4. **Governance inheritance.** Products inherit governance metadata from the domain by default. Only declare `governance` overrides when the product requires stricter or different controls than the domain default.

5. **Masking is product-scoped.** Masking rules are declared per product, not per entity. The same attribute may be masked differently in different products.

6. **Schema type drives generation.** When `schema_type` is declared, the product definition is the input contract for Agent Artifact. The agent generates physical artifacts scoped to the product's entity list and constrained by its governance and masking rules.

7. **Products do not define structure.** Products reference canonical entities — they do not redefine attributes, types, or constraints. If a consumer needs a derived attribute, it should be modelled as a canonical attribute or transformation first.

8. **Source field for source-aligned.** Source-aligned products use `source` instead of `entities`. The value must match a source system folder under `sources/`.

9. **Two-layer compliance.** Every data product must appear in both the domain file summary table and a detail file. The domain file is the index; the detail file is the contract.

10. **Name uniqueness.** Data product names must be unique within a domain. The level-3 heading is the product's identity in the Knowledge Graph.
