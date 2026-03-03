# [Financial Crime](../domain.md)

## Entities

### Payee

A Payee is a Party Role representing the recipient of funds in a transaction.

```mermaid
---
config:
  layout: elk
---
classDiagram
  class Payee{
    Payee Identifier : string
    Beneficiary Reference : string
  }

  Payee --|> PartyRole
  Payee "1" --> "0..*" Transaction : receives

  class PartyRole["<a href='party_role.md'>Party Role</a>"]
  class Transaction["<a href='transaction.md'>Transaction</a>"]
```

```yaml
extends: Party Role
existence: independent
mutability: slowly_changing
attributes:
  Payee Identifier:
    type: string
    identifier: primary
    description: Unique identifier for the payee role instance.

  Beneficiary Reference:
    type: string
    description: Reference used to identify the beneficiary in payment instructions.
```

```yaml
governance:
  retention_basis: Inherited from domain default retention of 10 years post relationship end for AML/CTF record-keeping
```

## Relationships

### Payee Receives Transaction

A Payee can be associated with one or more Transactions as the receiving party.

```yaml
source: Payee
type: associates_with
target: Transaction
cardinality: one-to-many
granularity: atomic
ownership: Payee
```
