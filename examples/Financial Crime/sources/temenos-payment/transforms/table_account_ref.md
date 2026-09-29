# [Financial Crime](../../../domain.md)

## Sources

### [Temenos Payment](../source.md#temenos-payment)

#### AccountRef

Account reference data used by payments.

##### Entity Fan-Out

```yaml
produces:
  - entity: Account
    cardinality: 1
    identity:
      field: AccountRef.AccountNumber
      maps_to: Account · Account Identifier
    references:
      Product: AccountRef.ProductCode
```

##### Source Schema

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Description | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | AccountNumber | Text | 34 | | | no | Account reference number | Account.Account Identifier, Account.Account Number
2 | AccountState | Text | 20 | | | yes | Account servicing state | [Transform: Map Account Status](#transform-map-account-status)
3 | ProductCode | Text | 30 | | | yes | Product the account is an instance of | Reference: Product

##### Transform: Map Account Status

Unrecognised states load as null and fail the quality check. Guessing Active would let a blocked account look usable.

```yaml
type: conditional
target: Account · Account Status
evaluation: exclusive
source:
  field: AccountRef.AccountState
cases:
  Active: "AccountState == 'ACTIVE'"
  Dormant: "AccountState == 'DORMANT'"
  Frozen: "AccountState == 'FROZEN'"
  Closed: "AccountState == 'CLOSED'"
fallback: null
```

##### Worked Examples

```yaml
example: Frozen account
given:
  AccountNumber: "062-000-12345678"
  AccountState: "FROZEN"
  ProductCode: "TXN-EVERYDAY"
produces:
  - entity: Account
    Account Identifier: "062-000-12345678"
    Account Number: "062-000-12345678"
    Account Status: Frozen
notes: The account is linked to product TXN-EVERYDAY through Account Holds Product.
```

```yaml
example: Unrecognised state is not guessed
given:
  AccountNumber: "062-000-87654321"
  AccountState: "MIGRATING"
produces:
  - entity: Account
    Account Identifier: "062-000-87654321"
    Account Status: null
```
