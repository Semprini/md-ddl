# Lifecycle - Financial Crime

This file records the current lifecycle state of the Financial Crime domain and
its published products. It combines machine-readable change intent with a
human-readable history so lifecycle, reconciliation, and migration planning can
work from the same source.

## Current State

```yaml
domain_version: "1.0.0"
domain_status: Active

products:
  - name: Canonical Party
    status: Active
    version: "1.0.0"
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
