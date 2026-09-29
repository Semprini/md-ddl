# Lifecycle - Financial Crime

This file records the current lifecycle state of the Financial Crime domain and
its published products. It combines machine-readable change intent with a
human-readable history so lifecycle, reconciliation, and migration planning can
work from the same source.

## Current State

```yaml
domain_version: "2.0.0"
domain_status: Active

products:
  - name: Canonical Party
    status: Active
    version: "2.0.0"
  - name: Transaction Risk Summary
    status: Active
    version: "1.0.0"
  - name: Patient Financial Fraud Detection
    status: Active
    version: "1.0.0"
  - name: Salesforce CRM Raw Feed
    status: Active
    version: "1.0.0"
  - name: Party Risk Report (Legacy)
    status: Deprecated
    version: "1.0.0"
```

## Version History

### Domain 2.0.0 - 2026-09-29

A quality release. A domain review and the new transform lint rules found that the example
didn't meet its own standard: lint errors, transform targets naming attributes the model
didn't have, conditional cases outside their enums, conflicting keys, and a source layer
that wasn't deterministic. This release fixes the model and rebuilds the source layer.

#### Change Manifest

```yaml
changes:
  - type: breaking
    scope: attribute
    entity: Customer
    description: "Party Role subtypes no longer declare a second primary identifier. Customer Number, Merchant Identifier, Payer Identifier, Payee Identifier, Teller Identifier, and Payment Initiator Identifier are now identifier: alternate; Role Identifier is the only primary key."
  - type: breaking
    scope: relationship
    entity: Party Role
    description: "Removed Party Role Governed By Agreement, which duplicated Agreement Involves Party Roles. Agreement Involves Party Roles is now many-to-many with a Role In Agreement attribute, since a role can be party to several agreements."
  - type: breaking
    scope: relationship
    entity: Merchant
    description: "Removed Merchant Receives Payment. A merchant receiving a payment is the Payee on it."
  - type: breaking
    scope: relationship
    entity: Transaction
    description: "Transaction Has Debtor and Transaction Has Creditor are many-to-one from Transaction (exactly one debtor and one creditor per transaction), not one-to-many."
  - type: breaking
    scope: attribute
    entity: Merchant
    description: "Removed foreign-key attributes Merchant.Settlement Account Identifier and Teller.Assigned Branch Identifier; the existing relationships carry these links."
  - type: additive
    scope: entity
    entity: Transaction Alert
    description: "New entity for transaction monitoring alerts (risk score, disposition), separate from append-only Transaction because an alert's outcome changes during review. Related by Transaction Raises Alerts."
  - type: additive
    scope: attribute
    entity: Person
    description: "Added Given Name and Family Name, needed for identity verification and name screening."
  - type: additive
    scope: attribute
    entity: Customer
    description: "Added Risk Review Required and Enhanced Due Diligence Trigger (new EDD Trigger Status enum)."
  - type: additive
    scope: enum
    entity: Monitoring Outcome
    description: "New enum for Transaction Alert disposition."
  - type: corrective
    scope: attribute
    entity: Payment Initiator
    description: "Initiation Channel typed as enum:Transaction Channel instead of free text."
  - type: corrective
    scope: enum
    entity: Address Verification Status
    description: "Heading renamed from 'Address Verification Statuses' so the enum type reference resolves."
  - type: corrective
    scope: entity
    entity: Party
    description: "Governance aligned: retention values state their trigger, descriptions no longer contradict the 10-year retention, PII overrides are justified, and the domain regulatory scope matches the AU/NZ frameworks the entities cite."
  - type: corrective
    scope: entity
    entity: Company
    description: "BIAN references corrected to classes present in the v13 index (Organisation partial, PaymentTransaction, BankingProduct, AccessPreferenceArrangement partial); unverifiable references removed."

affected_products:
  - name: Canonical Party
    impact: breaking
    reason: "Customer is no longer keyed on Customer Number; Person and Customer gain attributes. Version 2.0.0, now declaring an eventual consistency posture."
  - name: Transaction Risk Summary
    impact: none
    reason: "Output columns are unchanged; lineage paths through Payer and Payee still resolve."
  - name: Patient Financial Fraud Detection
    impact: none
    reason: "Uses Transaction and Party attributes that are unchanged."
  - name: Salesforce CRM Raw Feed
    impact: additive
    reason: "The Salesforce extracts now carry the enterprise party identifier and key columns on every table."
  - name: Party Risk Report (Legacy)
    impact: none
    reason: "Deprecated; not updated."
```

#### Changelog

### Changed

- The source layer follows the spec's domain-rooted hierarchy, with Entity Fan-Out, `Transform:`
  rule headings, worked examples (including a fan-in example across Salesforce CRM and SAP
  Fraud Management, with interim states), and Open Decisions.
- Every transform target resolves to a declared attribute, and every conditional case is a valid
  value of its target. Unknown source codes now fall back to a review value or null, never a
  benign guess.
- The source extracts carry the keys needed for deterministic mapping: the enterprise party
  identifier on every Salesforce and SAP table, and the payment identifier on Temenos party and
  initiation tables.
- Event payload attributes use natural-language names.

### Removed

- Party Role Governed By Agreement, Merchant Receives Payment, and the Merchant and Teller
  foreign-key attributes.

### Open decisions

- OD-1 (Salesforce Account): customer segment codes and whether Customer needs a Segment attribute.
- OD-2 (Salesforce Contact): the source of PEP category for flagged persons.


### Domain 1.0.0 - 2026-03-15

#### Change Manifest

```yaml
changes:
  - type: additive
    scope: entity
    entity: Party
    description: "Established the Party, Party Role, Account, Agreement, and Transaction backbone for financial crime modelling."
  - type: additive
    scope: relationship
    entity: Party
    description: "Declared role, account, agreement, and self-referential relationship patterns needed for AML, KYC, and network analysis."
  - type: additive
    scope: event
    entity: Transaction
    description: "Added core lifecycle and detection events for onboarding, execution, account change, and suspicious activity workflows."
  - type: additive
    scope: entity
    entity: Exchange Rate
    description: "Included currency and exchange-rate concepts for cross-border and multi-currency monitoring."

affected_products:
  - name: Canonical Party
    impact: additive
    reason: "Initial domain-aligned publication of core identity and relationship entities."
  - name: Transaction Risk Summary
    impact: additive
    reason: "Initial consumer-aligned analytics product for transaction monitoring."
  - name: Patient Financial Fraud Detection
    impact: additive
    reason: "Initial cross-domain fraud product combining Financial Crime and Healthcare context."
  - name: Salesforce CRM Raw Feed
    impact: additive
    reason: "Initial source-aligned replay and audit feed for Salesforce CRM."
  - name: Party Risk Report (Legacy)
    impact: none
    reason: "Retained as a deprecated legacy product while consumers migrate to Transaction Risk Summary."
```

#### Changelog

### Added

- Initial Financial Crime domain release with party, account, agreement, transaction, branch, currency, and exchange-rate concepts.
- Relationship patterns for party role assignment, customer account holding, party association, and agreement governance.
- Events covering onboarding, transaction execution, account status change, agreement activation, KYC updates, and suspicious activity detection.
- Four active products: Canonical Party, Transaction Risk Summary, Patient Financial Fraud Detection, and Salesforce CRM Raw Feed.

### Deprecated

- Party Risk Report (Legacy) retained for migration support while downstream consumers move to Transaction Risk Summary.
