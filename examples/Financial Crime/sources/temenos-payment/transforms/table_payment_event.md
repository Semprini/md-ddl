# [Financial Crime](../../../domain.md)

## Sources

### [Temenos Payment](../source.md#temenos-payment)

#### PaymentEvent

The payment record as it moves through execution. A status change creates a new transaction-time version of the Transaction; nothing is updated in place.

##### Entity Fan-Out

```yaml
produces:
  - entity: Transaction
    cardinality: 1
    identity:
      field: PaymentEvent.PaymentId
      maps_to: Transaction · Transaction Identifier
    references:
      Currency: PaymentEvent.SettlementCurrency
```

##### Source Schema

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Description | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | PaymentId | Text | 64 | | | no | Unique payment identifier | Transaction.Transaction Identifier
2 | SettlementAmount | Decimal | | 18 | 4 | no | Settled payment amount | Transaction.Amount
3 | SettlementCurrency | Text | 3 | | | no | ISO 4217 currency code | Reference: Currency
4 | ExecutionDateTime | DateTime | | | | yes | When the payment was executed | Transaction.Settlement Date Time
5 | PaymentStatus | Text | 20 | | | yes | Payment lifecycle status | [Transform: Map Transaction Status](#transform-map-transaction-status)

##### Transform: Map Transaction Status

Rejected payments failed, so they map to Failed. Unrecognised statuses go to Under Review, which suspends settlement for a monitoring analyst.

```yaml
type: conditional
target: Transaction · Transaction Status
evaluation: exclusive
source:
  field: PaymentEvent.PaymentStatus
cases:
  Pending: "PaymentStatus == 'PENDING'"
  Settled: "PaymentStatus == 'EXECUTED'"
  Reversed: "PaymentStatus == 'REVERSED'"
  Failed: "PaymentStatus == 'REJECTED'"
fallback: Under Review
```

##### Worked Examples

```yaml
example: Executed payment
given:
  PaymentId: "PAY-900001"
  SettlementAmount: 18250.00
  SettlementCurrency: "AUD"
  ExecutionDateTime: "2024-06-03T02:10:00Z"
  PaymentStatus: "EXECUTED"
produces:
  - entity: Transaction
    Transaction Identifier: "PAY-900001"
    Amount: 18250.00
    Settlement Date Time: "2024-06-03T02:10:00Z"
    Transaction Status: Settled
notes: The transaction is denominated in AUD through the reference to Currency.
```

```yaml
example: Rejected payment
given:
  PaymentId: "PAY-900003"
  SettlementAmount: 950.00
  SettlementCurrency: "NZD"
  PaymentStatus: "REJECTED"
produces:
  - entity: Transaction
    Transaction Identifier: "PAY-900003"
    Transaction Status: Failed
```
