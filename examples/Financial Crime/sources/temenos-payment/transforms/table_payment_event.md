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

Rejected payments failed, so they map to Failed. A REVERSED status on the original payment records a new version of that Transaction with status Reversed; any reversing movement Temenos sends arrives as its own payment. Unrecognised statuses go to Under Review, which suspends settlement for a monitoring analyst.

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

```yaml
example: A payment assembled from its event, initiation, and parties
given:
  - from: Temenos Payment · PaymentEvent
    row:
      PaymentId: "PAY-900001"
      SettlementAmount: 18250.00
      SettlementCurrency: "AUD"
      ExecutionDateTime: "2024-06-03T02:10:00Z"
      PaymentStatus: "EXECUTED"
  - from: Temenos Payment · Initiation
    row:
      PaymentId: "PAY-900001"
      ActorPartyId: "P-1001"
      ChannelCode: "API"
  - from: Temenos Payment · PaymentParties
    row:
      PaymentId: "PAY-900001"
      DebtorPartyId: "P-1001"
      CreditorPartyId: "P-1003"
produces:
  - entity: Transaction
    Transaction Identifier: "PAY-900001"
    Amount: 18250.00
    Settlement Date Time: "2024-06-03T02:10:00Z"
    Transaction Status: Settled
    Transaction Channel: Third Party
  - entity: Payment Initiator
    Role Identifier: "INIT-P-1001"
  - entity: Payer
    Role Identifier: "PAYER-P-1001"
  - entity: Payee
    Role Identifier: "PAYEE-P-1003"
interim:
  - after: 1
    produces:
      - entity: Transaction
        Transaction Identifier: "PAY-900001"
        Transaction Status: Settled
        Transaction Channel: null
  - after: 2
    produces:
      - entity: Transaction
        Transaction Identifier: "PAY-900001"
        Transaction Channel: Third Party
      - entity: Payment Initiator
        Role Identifier: "INIT-P-1001"
notes: >
  Fan-in within one source: PaymentEvent establishes the Transaction; Initiation and
  PaymentParties contribute to it. Transaction is append-only with transaction-time
  tracking, so each contribution records a new version carrying the earlier attributes
  forward. After step 2 the current version has the channel and is initiated by
  INIT-P-1001; after step 3 it also has its debtor (PAYER-P-1001) and creditor
  (PAYEE-P-1003). If Initiation or PaymentParties arrived first, its row would be held
  until PaymentEvent establishes PAY-900001 (`when_absent: hold`, the default).
```
