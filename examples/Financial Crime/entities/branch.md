# [Financial Crime](../domain.md)

## Entities

### Branch

A Branch is an operational location responsible for servicing accounts and branch-mediated transactions.

```mermaid
---
config:
  layout: elk
---
classDiagram
  class Branch{
    * Branch Identifier : string
    Branch Code : string
    Branch Name : string
  }

  Branch "1" --> "0..*" Account : services

  class Account["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/entities/account.md'>Account</a>"]
```

```yaml
existence: independent
mutability: reference
attributes:
  Branch Identifier:
    type: string
    identifier: primary
    description: Unique identifier for the branch location.

  Branch Code:
    type: string
    description: Operational code used to identify the branch.

  Branch Name:
    type: string
    description: Human-readable branch name.
```

```yaml
governance:
  retention_basis: Inherited from domain default retention of 10 years post relationship end for AML/CTF record-keeping
```

## Relationships

### Branch Services Account

A Branch services one or more Accounts.

```yaml
source: Branch
type: has
target: Account
cardinality: one-to-many
granularity: atomic
ownership: Branch
```

### Branch Transaction Summary

A Branch has a grouped relationship to Transactions processed through its serviced Accounts. This supports branch-level aggregated reporting for fraud pattern analysis.

```yaml
source: Branch
type: associates_with
target: Transaction
cardinality: one-to-many
granularity: group
ownership: Branch
```
