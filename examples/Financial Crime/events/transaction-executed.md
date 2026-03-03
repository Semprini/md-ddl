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
  - event timestamp:
      type: datetime
      description: Time the transaction was executed
```
