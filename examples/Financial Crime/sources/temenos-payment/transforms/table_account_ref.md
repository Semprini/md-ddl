# [Financial Crime](../../../domain.md)

## Sources

### [Temenos Payment](../source.md#temenos-payment)

#### AccountRef

Account reference data used by payments. Currency is reference data (ISO 4217, mutability `reference`), so the reference resolves without any source creating it.

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
      Currency: AccountRef.CurrencyCode
```

##### Source Schema

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Description | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | AccountNumber | Text | 34 | | | no | Account reference number | Account.Account Identifier, Account.Account Number
2 | AccountState | Text | 20 | | | yes | Account servicing state | [Transform: Map Account Status](#transform-map-account-status)
3 | ProductCode | Text | 30 | | | no | Product the account is an instance of | Reference: Product
4 | CurrencyCode | Text | 3 | | | no | ISO 4217 currency the account is held in | Reference: Currency

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
  CurrencyCode: "AUD"
produces:
  - entity: Account
    Account Identifier: "062-000-12345678"
    Account Number: "062-000-12345678"
    Account Status: Frozen
notes: >
  The account is linked to product TXN-EVERYDAY through Account Holds Product, and to AUD
  through Account Denominated In Currency.
```

```yaml
example: Unrecognised state is not guessed
given:
  AccountNumber: "062-000-87654321"
  AccountState: "MIGRATING"
  ProductCode: "TXN-EVERYDAY"
  CurrencyCode: "AUD"
produces:
  - entity: Account
    Account Identifier: "062-000-87654321"
    Account Status: null
```

##### Open Decisions

Ref | Item | Impact
--- | --- | ---
OD-1 | No mapped source establishes Product instances; Product is slowly changing, not reference data. `ProductCode` references a product the model can't yet resolve. | Until a product catalogue source is mapped (or Product is reclassified as reference data), Account Holds Product links can't be tested.
