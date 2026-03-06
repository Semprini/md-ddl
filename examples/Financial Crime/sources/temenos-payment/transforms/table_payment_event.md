# [Temenos Payment](../source.md)

## PaymentEvent

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | PaymentId | Text | 64 | | | no | Unique payment event identifier | Transaction.Transaction Identifier
2 | SettlementAmount | Decimal | | 18 | 4 | no | Settled payment amount | Transaction.Amount
3 | SettlementCurrency | Text | 3 | | | no | ISO currency code | Transaction.Currency
4 | ExecutionDateTime | DateTime | | | | yes | Timestamp at execution | Transaction.Execution Timestamp
5 | PaymentStatus | Text | 20 | | | yes | Payment lifecycle status | [Map Status](#map-status)

### Map Status

Maps payment state into canonical transaction status.

```yaml
type: conditional
target: Transaction · Status
source:
  field: PaymentEvent.PaymentStatus
cases:
  Pending: "PaymentStatus == 'PENDING'"
  Completed: "PaymentStatus == 'EXECUTED'"
  Reversed: "PaymentStatus == 'REVERSED'"
  Rejected: "PaymentStatus == 'REJECTED'"
fallback: Pending
```
