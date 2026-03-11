# MD-DDL Examples

This directory contains reference examples that demonstrate the MD-DDL
specification across increasing levels of complexity. Use these as
patterns when modelling your own domains.

## Examples

Example | Description | Complexity
--- | --- | ---
[Simple Customer](Simple%20Customer/domain.md) | Minimal 2-file example — one domain, three entities, one enum, one event | Starter
[Financial Crime](Financial%20Crime/domain.md) | Comprehensive AML/fraud domain — 15+ entities, sources, products, BIAN alignment | Intermediate
[Healthcare](Healthcare/domain.md) | FHIR-aligned clinical domain — 12 entities, HIPAA governance, source transforms, knowledge-graph product | Intermediate
[Telecom](Telecom/domain.md) | TM Forum-aligned telecom domain — 10 entities, PCI-DSS, associative entity, new relationship types, dimensional product | Advanced
[Retail Sales](Retail%20Sales/domain.md) | Greenfield sales domain — 4 entities, Bounded Context strategy, cross-domain Customer 360 | Advanced
[Retail Service](Retail%20Service/domain.md) | Greenfield service domain — 4 entities, Bounded Context strategy, pairs with Retail Sales | Advanced

## Feature Coverage Matrix

This matrix shows which spec features each example exercises. Use it to
find the right example when learning a specific part of the specification.

### Core Structure (Spec §1–§4)

Feature | Simple Customer | Financial Crime | Healthcare | Telecom | Retail Sales | Retail Service
--- | --- | --- | --- | --- | --- | ---
Domain file with metadata | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Entity summary table | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Mermaid entity diagram | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Entity detail file(s) | ✓ (single file) | ✓ (per-entity) | ✓ (per-entity) | ✓ (per-entity) | ✓ (per-entity) | ✓ (per-entity)
Inheritance (`extends`) | ✓ | ✓ | — | ✓ | — | —
`existence: independent` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
`existence: dependent` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
`existence: associative` | — | — | — | ✓ (Subscription) | ✓ (Order Line) | —
Attribute constraints | ✓ | ✓ | ✓ | ✓ | ✓ | —
Governance block | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
PII marking | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Enums (dictionary style) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Enums (simple list) | — | ✓ | ✓ | ✓ | ✓ | ✓
External standard enums | — | ✓ (ISO 4217) | ✓ (LOINC, ICD-10, SNOMED CT) | — | — | —

### Temporal & Mutability (Spec §3)

Feature | Simple Customer | Financial Crime | Healthcare | Telecom | Retail Sales | Retail Service
--- | --- | --- | --- | --- | --- | ---
`mutability: immutable` | — | — | — | ✓ (Usage Record) | — | —
`mutability: append_only` | — | ✓ | ✓ | ✓ | ✓ (Order) | ✓ (Service Request)
`mutability: slowly_changing` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
`mutability: frequently_changing` | — | ✓ | ✓ | ✓ (Billing Account) | — | —
`mutability: reference` | — | ✓ | ✓ | ✓ | ✓ | ✓
`temporal: valid_time` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
`temporal: transaction_time` | — | — | ✓ | ✓ (Service Order) | ✓ (Order) | ✓ (Service Request)
`temporal: bitemporal` | — | ✓ | ✓ | ✓ (Customer, Usage Record) | — | —

### Relationships (Spec §5)

Feature | Simple Customer | Financial Crime | Healthcare | Telecom | Retail Sales | Retail Service
--- | --- | --- | --- | --- | --- | ---
`type: has` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
`type: owns` | ✓ | ✓ | — | ✓ (Customer owns Billing Account) | — | —
`type: references` | — | ✓ | ✓ | ✓ | ✓ | ✓
`type: assigned_to` | — | — | — | ✓ (Billing Account assigned_to Customer) | — | —
`type: triggers` | — | — | — | ✓ (Subscription triggers Service Order) | — | —
`type: supersedes` | — | — | — | ✓ (Product Offering supersedes itself) | — | —
`type: produces` | — | — | ✓ | ✓ | — | ✓
Relationship constraints | ✓ | ✓ | — | ✓ | ✓ | —
`granularity: atomic` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
`granularity: group` | — | ✓ | ✓ | — | — | —
`granularity: period` | — | ✓ | ✓ | ✓ (Customer Has Subscriptions) | — | —
Self-referencing relationship | — | — | ✓ | ✓ (Product Offering supersedes) | — | —

### Events (Spec §6)

Feature | Simple Customer | Financial Crime | Healthcare | Telecom | Retail Sales | Retail Service
--- | --- | --- | --- | --- | --- | ---
Event with `emitted_on: create` | — | ✓ | ✓ | ✓ | ✓ | ✓
Event with `emitted_on: update` | ✓ | ✓ | ✓ | ✓ | — | —
Event with multiple triggers | ✓ | — | ✓ | ✓ (create + update) | — | —
Event payload attributes | ✓ | ✓ | ✓ | ✓ | ✓ | ✓

### Sources & Transformations (Spec §7–§8)

Feature | Simple Customer | Financial Crime | Healthcare | Telecom | Retail Sales | Retail Service
--- | --- | --- | --- | --- | --- | ---
Source system declaration | — | ✓ | ✓ | ✓ | — | —
`change_model: real-time-cdc` | — | ✓ | ✓ | ✓ | — | —
`change_model: event-driven` | — | — | ✓ | ✓ | — | —
`change_model: batch` | — | ✓ | ✓ | ✓ (product catalog) | — | —
Domain feeds table | — | ✓ | ✓ | ✓ | — | —
Multiple source systems | — | ✓ | ✓ | — | — | —
Transform files (column-level mapping) | — | ✓ | ✓ | ✓ | — | —
Transform type: `conditional` | — | ✓ | ✓ | ✓ | — | —
Transform type: `direct` | — | ✓ | ✓ | ✓ | — | —

### Data Products (Spec §9)

Feature | Simple Customer | Financial Crime | Healthcare | Telecom | Retail Sales | Retail Service
--- | --- | --- | --- | --- | --- | ---
`class: domain-aligned` | — | ✓ | ✓ | ✓ | ✓ | ✓
`class: consumer-aligned` | — | ✓ | ✓ | ✓ | ✓ | —
`class: source-aligned` | — | ✓ | ✓ | ✓ | — | —
Cross-domain product | — | ✓ (patient-financial-fraud-detection) | ✓ (clinical-billing-fraud-detection) | ✓ (telecom-fraud-intelligence) | ✓ (customer-360) | —
SLA block (freshness, availability) | — | ✓ | ✓ | ✓ | ✓ | ✓
Masking rules | — | ✓ | ✓ | ✓ | ✓ | ✓
All 6 masking strategies | — | — | — | ✓ (across analytics + fraud products) | — | —
`schema_type: normalized` | — | ✓ | — | ✓ | ✓ | ✓
`schema_type: dimensional` | — | — | — | ✓ (Subscriber Usage Analytics) | — | —
`schema_type: wide-column` | — | ✓ | — | ✓ (legacy) | ✓ (legacy) | —
`schema_type: knowledge-graph` | — | — | ✓ | — | — | —
Product lifecycle (`status: Deprecated`) | — | ✓ | — | ✓ | ✓ | —

### Standards & Governance

Feature | Simple Customer | Financial Crime | Healthcare | Telecom | Retail Sales | Retail Service
--- | --- | --- | --- | --- | --- | ---
Industry standard alignment | — | BIAN | FHIR R4 | TM Forum ODA | — (no standard) | — (no standard)
Regulatory scope | — | AML/GDPR | HIPAA/HITECH | PCI-DSS/GDPR | GDPR | GDPR
`modelling_strategy: BoundedContext` | — | — | — | — | ✓ | ✓
Generated physical artifacts | — | ✓ (3NF JSON, Dimensional SQL) | — | — | — | —
