# [Temenos Payment](./source.md)

## AccountRef

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | AccountNumber | Text | 34 | | | no | Account reference number | Account.Account Identifier
2 | AccountState | Text | 20 | | | yes | Lifecycle/account servicing state | [Map Account Status](#map-account-status)
3 | ProductCode | Text | 30 | | | yes | Linked product code | Account.Product Identifier

### Map Account Status

Maps account servicing status from Temenos account state.

```yaml
type: conditional
target: Account · Account Status
source:
  field: AccountRef.AccountState
cases:
  Active: "AccountState == 'ACTIVE'"
  Frozen: "AccountState == 'FROZEN'"
  Closed: "AccountState == 'CLOSED'"
fallback: Active
```
