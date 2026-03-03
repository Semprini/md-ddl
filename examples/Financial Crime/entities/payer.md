# [Financial Crime](../domain.md)

## Entities

### Payer

A Payer is a Party Role representing the party from whom funds are debited in a transaction.

```mermaid
---
config:
  layout: elk
---
classDiagram
  class Payer{
    Payer Identifier : string
    Funding Source Reference : string
  }

  Payer --|> PartyRole
  Payer "1" --> "0..*" Transaction : funds

  class PartyRole["<a href='party_role.md'>Party Role</a>"]
  class Transaction["<a href='transaction.md'>Transaction</a>"]
```

```yaml
extends: Party Role
existence: independent
mutability: slowly_changing
attributes:
  Payer Identifier:
    type: string
    identifier: primary
    description: Unique identifier for the payer role instance.

  Funding Source Reference:
    type: string
    description: Reference to the source account or instrument used to fund payments.
```

```yaml
governance:
  retention_basis: Inherited from domain default retention of 10 years post relationship end for AML/CTF record-keeping
```

## Relationships

### Payer Funds Transaction

A Payer can be associated with one or more Transactions as the funding party.

```yaml
source: Payer
type: associates_with
target: Transaction
cardinality: one-to-many
granularity: atomic
ownership: Payer
```
