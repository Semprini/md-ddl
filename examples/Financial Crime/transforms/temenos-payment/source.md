# Temenos Payment

Temenos Payment is the operational source for payment initiation and execution records. It emits high-volume transaction changes used for financial crime monitoring and downstream payment analytics.

## Metadata

```yaml
id: temenos-payment
owner: payments.platform@bank.com
steward: data.governance@bank.com

change_model: real-time-cdc
change_events:
  - Payment Initiated
  - Payment Executed
  - Payment Reversed
  - Payment Rejected

update_frequency: real-time
data_quality_tier: 1
status: Production
version: "1.0.0"

tags:
  - Payments
  - Core Banking
  - Financial Crime
```

## [Financial Crime](../../domain.md) Feeds

Canonical Entity | Transform File | Attributes Contributed | Change Model
--- | --- | --- | ---
[Transaction](../../entities/transaction.md#transaction) | [table_payment_event](table_payment_event.md) | Transaction Identifier, Amount, Currency, Execution Timestamp, Status | real-time-cdc
[Account](../../entities/account.md#account) | [table_account_ref](table_account_ref.md) | Account Identifier, Account Status, Product Identifier | real-time-cdc
[Payment Initiator](../../entities/payment_initiator.md#payment-initiator) | [table_initiation](table_initiation.md) | Initiator Role Identifier, Initiation Channel | event-driven
[Payer](../../entities/payer.md#payer) | [table_payment_parties](table_payment_parties.md) | Payer Role Identifier | event-driven
[Payee](../../entities/payee.md#payee) | [table_payment_parties](table_payment_parties.md) | Payee Role Identifier | event-driven
