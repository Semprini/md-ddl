# [Financial Crime](../domain.md)

## Entities

### Merchant

A Merchant is a Party Role that accepts payments for goods or services through institution channels.

```mermaid
---
config:
  layout: elk
---
classDiagram
  class Merchant{
    * Merchant Identifier : string
    Merchant Category Code : string
    Settlement Account Identifier : string
  }

  Merchant --|> PartyRole
  Merchant "1" --> "0..*" Transaction : processes

  class PartyRole["<a href='party_role.md'>Party Role</a>"]
  class Transaction["<a href='transaction.md'>Transaction</a>"]
```

```yaml
extends: Party Role
existence: independent
mutability: slowly_changing
attributes:
  Merchant Identifier:
    type: string
    identifier: primary
    description: Unique identifier for the merchant role instance.

  Merchant Category Code:
    type: string
    description: Industry code representing the merchant business type.

  Settlement Account Identifier:
    type: string
    description: Account identifier used for merchant settlement.
```

```yaml
governance:
  retention_basis: Inherited from domain default retention of 10 years post relationship end for AML/CTF record-keeping
```

## Relationships

### Merchant Receives Payment

A Merchant receives funds through one or more Transactions.

```yaml
source: Merchant
type: associates_with
target: Transaction
cardinality: one-to-many
granularity: atomic
ownership: Merchant
```
