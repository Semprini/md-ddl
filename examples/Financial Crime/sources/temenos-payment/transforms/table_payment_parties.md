# [Financial Crime](../../../domain.md)

## Sources

### [Temenos Payment](../source.md#temenos-payment)

#### PaymentParties

The debtor and creditor of a payment. One row produces both roles.

##### Entity Fan-Out

```yaml
produces:
  - entity: Payer
    cardinality: 1
    identity:
      field: PaymentParties.DebtorRoleId
      maps_to: Payer · Role Identifier
    references:
      Transaction: PaymentParties.PaymentId

  - entity: Payee
    cardinality: 1
    identity:
      field: PaymentParties.CreditorRoleId
      maps_to: Payee · Role Identifier
    references:
      Transaction: PaymentParties.PaymentId
```

##### Source Schema

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Description | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | PaymentId | Text | 64 | | | no | Payment the parties belong to | Transaction.Transaction Identifier
2 | DebtorRoleId | Text | 64 | | | no | Debtor role identifier in payment context | Payer.Role Identifier
3 | CreditorRoleId | Text | 64 | | | no | Creditor role identifier in payment context | Payee.Role Identifier

##### Worked Examples

```yaml
example: One row yields the debtor and creditor of a payment
given:
  PaymentId: "PAY-900001"
  DebtorRoleId: "PAYER-5501"
  CreditorRoleId: "PAYEE-7702"
produces:
  - entity: Payer
    Role Identifier: "PAYER-5501"
  - entity: Payee
    Role Identifier: "PAYEE-7702"
notes: >
  Each role references PAY-900001, which has exactly one Payer and one Payee (Transaction
  Has Debtor and Transaction Has Creditor are many-to-one from Transaction).
```
