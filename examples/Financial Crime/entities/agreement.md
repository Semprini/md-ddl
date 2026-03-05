# [Financial Crime](../domain.md)

## Entities

### Agreement

An Agreement defines the formal contractual terms that govern relationships between party roles and financial products.

```mermaid
---
config:
  layout: elk
---
classDiagram
  class Agreement{
    * Agreement Identifier : string
    Agreement Number : string
    Effective Date : date
    Maturity Date : date
  }

  TermDepositAgreement --|> Agreement
  LoanAgreement --|> Agreement
  Agreement "1" --> "0..*" PartyRole : governs

  class TermDepositAgreement["<a href='term-deposit-agreement.md'>Term Deposit Agreement</a>"]
  class LoanAgreement["<a href='loan-agreement.md'>Loan Agreement</a>"]
  class PartyRole["<a href='party_role.md'>Party Role</a>"]
```

```yaml
existence: independent
mutability: slowly_changing
attributes:
  Agreement Identifier:
    type: string
    identifier: primary
    description: Unique identifier of the agreement record.

  Agreement Number:
    type: string
    description: Human-facing agreement reference number.

  Effective Date:
    type: date
    description: Date the agreement became enforceable.

  Maturity Date:
    type: date
    description: Date the agreement is scheduled to mature, if applicable.
```

```yaml
governance:
  retention_basis: Inherited from domain default retention of 10 years post relationship end for AML/CTF record-keeping
```

## Relationships

### Agreement Involves Party Roles

An Agreement governs and involves one or more Party Roles participating in the contract.

```yaml
source: Agreement
type: governs
target: Party Role
cardinality: one-to-many
granularity: atomic
ownership: Agreement
```
