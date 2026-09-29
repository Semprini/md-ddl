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
    Merchant Identifier : string
    Merchant Category Code : string
  }

  Merchant --|> PartyRole
  Merchant "0..*" --> "0..1" Account : settles into

  class PartyRole["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/entities/party_role.md'>Party Role</a>"]
  class Account["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/entities/account.md'>Account</a>"]  
```

```yaml
extends: Party Role
existence: independent
mutability: slowly_changing
attributes:
  Merchant Identifier:
    type: string
    identifier: alternate
    description: Unique identifier for the merchant role instance.

  Merchant Category Code:
    type: string
    description: >
      ISO 18245 Merchant Category Code (MCC) representing the merchant's primary
      business type. Used in transaction monitoring rule segmentation — certain MCCs
      (e.g., cash-intensive businesses, money services) attract heightened scrutiny.
```

```yaml
governance:
  retention_basis: Inherited from domain default retention of 10 years post relationship end for AML/CTF record-keeping
```

## Relationships

### Merchant Has Settlement Account
A Merchant may have a designated Account into which settlement funds are credited by the institution.
```yaml
source: Merchant
type: references
target: Account
cardinality: many-to-one
granularity: atomic
ownership: Merchant
```
