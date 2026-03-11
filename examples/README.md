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

## Feature Coverage Matrix

This matrix shows which spec features each example exercises. Use it to
find the right example when learning a specific part of the specification.

### Core Structure (Spec §1–§4)

Feature | Simple Customer | Financial Crime | Healthcare
--- | --- | --- | ---
Domain file with metadata | ✓ | ✓ | ✓
Entity summary table | ✓ | ✓ | ✓
Mermaid entity diagram | ✓ | ✓ | ✓
Entity detail file(s) | ✓ (single file) | ✓ (per-entity) | ✓ (per-entity)
Inheritance (`extends`) | ✓ | ✓ | —
`existence: independent` | ✓ | ✓ | ✓
`existence: dependent` | ✓ | ✓ | ✓
Attribute constraints | ✓ | ✓ | ✓
Governance block | ✓ | ✓ | ✓
PII marking | ✓ | ✓ | ✓
Enums (dictionary style) | ✓ | ✓ | ✓
Enums (simple list) | — | ✓ | ✓
External standard enums | — | ✓ (ISO 4217) | ✓ (LOINC, ICD-10, SNOMED CT)

### Temporal & Mutability (Spec §3)

Feature | Simple Customer | Financial Crime | Healthcare
--- | --- | --- | ---
`mutability: slowly_changing` | ✓ | ✓ | ✓
`mutability: append_only` | — | ✓ | ✓
`mutability: reference` | — | ✓ | ✓
`mutability: frequently_changing` | — | ✓ | ✓
`temporal: valid_time` | ✓ | ✓ | ✓
`temporal: transaction_time` | — | — | ✓
`temporal: bitemporal` | — | ✓ | ✓

### Relationships (Spec §5)

Feature | Simple Customer | Financial Crime | Healthcare
--- | --- | --- | ---
`type: has` | ✓ | ✓ | ✓
`type: owns` | ✓ | ✓ | —
`type: references` | — | ✓ | ✓
Relationship constraints | ✓ | ✓ | —
`granularity: atomic` | ✓ | ✓ | ✓
`granularity: group` | — | ✓ | ✓
`granularity: period` | — | ✓ | ✓
Self-referencing relationship | — | — | ✓

### Events (Spec §6)

Feature | Simple Customer | Financial Crime | Healthcare
--- | --- | --- | ---
Event with `emitted_on: create` | — | ✓ | ✓
Event with `emitted_on: update` | ✓ | ✓ | ✓
Event with multiple triggers | ✓ | — | ✓
Event payload attributes | ✓ | ✓ | ✓

### Sources & Transformations (Spec §7–§8)

Feature | Simple Customer | Financial Crime | Healthcare
--- | --- | --- | ---
Source system declaration | — | ✓ | ✓
`change_model: real-time-cdc` | — | ✓ | ✓
`change_model: event-driven` | — | — | ✓
`change_model: batch` | — | ✓ | ✓
Domain feeds table | — | ✓ | ✓
Multiple source systems | — | ✓ | ✓
Transform files (column-level mapping) | — | ✓ | ✓
Transform type: `conditional` | — | ✓ | ✓
Transform type: `direct` | — | ✓ | ✓

### Data Products (Spec §9)

Feature | Simple Customer | Financial Crime | Healthcare
--- | --- | --- | ---
`class: domain-aligned` | — | ✓ | ✓
`class: consumer-aligned` | — | ✓ | ✓
`class: source-aligned` | — | ✓ | ✓
Cross-domain product | — | ✓ (patient-financial-fraud-detection) | ✓ (clinical-billing-fraud-detection)
SLA block (freshness, availability) | — | ✓ | ✓
Masking rules | — | ✓ | ✓
`schema_type: knowledge-graph` | — | — | ✓
Product lifecycle (`status: Deprecated`) | — | ✓ | —

### Standards & Governance

Feature | Simple Customer | Financial Crime | Healthcare
--- | --- | --- | ---
Industry standard alignment | — | BIAN | FHIR R4
Regulatory scope | — | AML/GDPR | HIPAA/HITECH
Generated physical artifacts | — | ✓ (3NF JSON, Dimensional SQL) | —
