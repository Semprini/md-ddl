# SAP Fraud Management

SAP Fraud Management is the analytical source for fraud and suspicious activity detection signals. It contributes risk outcomes and case-oriented enrichment used by AML, KYC, and transaction monitoring controls.

## Metadata

```yaml
id: sap-fraud-management
owner: fraud.operations@bank.com
steward: compliance.officer@bank.com

change_model: event-driven
change_events:
  - Fraud Alert Raised
  - Fraud Alert Closed
  - Transaction Risk Scored
  - Case Escalated

update_frequency: real-time
data_quality_tier: 2
status: Production
version: "1.0.0"

tags:
  - Fraud
  - AML
  - Financial Crime
```

## [Financial Crime](../../domain.md) Feeds

Canonical Entity | Transform File | Attributes Contributed | Change Model
--- | --- | --- | ---
[Transaction](../../entities/transaction.md#transaction) | [table_alert_case](transforms/table_alert_case.md) | Financial Crime Risk Score, Monitoring Outcome, Alert Reference | event-driven
[Party](../../entities/party.md#party) | [table_sanctions_screening](transforms/table_sanctions_screening.md) | Sanctions Screen Status, Watchlist Match Indicator | batch-intraday
[Customer](../../entities/customer.md#customer) | [table_customer_risk_profile](transforms/table_customer_risk_profile.md) | Risk Review Flag, Enhanced Due Diligence Trigger | event-driven
