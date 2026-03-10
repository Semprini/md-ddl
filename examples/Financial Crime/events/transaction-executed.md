# [Financial Crime](../domain.md)

## Events

### Transaction Executed

Emitted when a financial transaction is successfully executed.

```yaml
actor: Payment Initiator
entity: Transaction
emitted_on:
  - create
business_meaning: Funds movement has been executed and committed as a business transaction
downstream_impact:
  - Ledger and balance updates are triggered
  - Transaction monitoring and screening pipelines are triggered
attributes:
  event_timestamp:
    type: datetime
    description: Time the transaction was executed
  amount:
    type: decimal
    description: Monetary value moved by the transaction
  currency_code:
    type: string
    description: ISO 4217 currency code of the transaction amount
  payer_role_identifier:
    type: string
    description: Role identifier of the payer party
  payee_role_identifier:
    type: string
    description: Role identifier of the payee party
  channel:
    type: string
    description: Channel through which the transaction was initiated (e.g. branch, online, mobile)
```
