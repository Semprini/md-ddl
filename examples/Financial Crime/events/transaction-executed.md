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
  Event Timestamp:
    type: datetime
    description: Time the transaction was executed
  Amount:
    type: decimal
    description: Monetary value moved by the transaction
  Currency Code:
    type: string
    description: ISO 4217 currency code of the transaction amount
  Payer Role Identifier:
    type: string
    description: Role identifier of the payer party
  Payee Role Identifier:
    type: string
    description: Role identifier of the payee party
  Channel:
    type: string
    description: Channel through which the transaction was initiated (e.g. branch, online, mobile)
```
