# [Financial Crime](../../../domain.md)

## Sources

### [Temenos Payment](../source.md#temenos-payment)

#### PaymentParties

The debtor and creditor of a payment. One row produces both roles, each keyed on its party.

##### Entity Fan-Out

```yaml
produces:
  - entity: Payer
    cardinality: 1
    identity: Derive Payer Role Identifier
    references:
      Party: PaymentParties.DebtorPartyId
      Transaction: PaymentParties.PaymentId

  - entity: Payee
    cardinality: 1
    identity: Derive Payee Role Identifier
    references:
      Party: PaymentParties.CreditorPartyId
      Transaction: PaymentParties.PaymentId
```

##### Source Schema

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Description | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | PaymentId | Text | 64 | | | no | Payment the parties belong to | Reference: Transaction
2 | DebtorPartyId | Text | 40 | | | no | Enterprise party identifier of the debtor | [Transform: Derive Payer Role Identifier](#transform-derive-payer-role-identifier)
3 | CreditorPartyId | Text | 40 | | | no | Enterprise party identifier of the creditor | [Transform: Derive Payee Role Identifier](#transform-derive-payee-role-identifier)

##### Transform: Derive Payer Role Identifier

```yaml
type: derived
target: Payer · Role Identifier
expression: "'PAYER-' + Debtor Party Id"
inputs:
  Debtor Party Id:
    field: PaymentParties.DebtorPartyId
```

##### Transform: Derive Payee Role Identifier

```yaml
type: derived
target: Payee · Role Identifier
expression: "'PAYEE-' + Creditor Party Id"
inputs:
  Creditor Party Id:
    field: PaymentParties.CreditorPartyId
```

The prefixes keep each role type's identifiers apart in the shared Party Role key space.

##### Worked Examples

```yaml
example: One row yields the debtor and creditor of a payment
given:
  PaymentId: "PAY-900001"
  DebtorPartyId: "P-1001"
  CreditorPartyId: "P-1003"
produces:
  - entity: Payer
    Role Identifier: "PAYER-P-1001"
  - entity: Payee
    Role Identifier: "PAYEE-P-1003"
notes: >
  Each role belongs to its party and references PAY-900001, which has exactly one Payer and
  one Payee (Transaction Has Debtor and Transaction Has Creditor are many-to-one from
  Transaction).
```
