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
    Agreement Status : enum~AgreementStatus~
    Effective Date : date
    Maturity Date : date
  }

  TermDepositAgreement --|> Agreement
  LoanAgreement --|> Agreement
  Agreement "1" --> "0..*" PartyRole : governs

  class AgreementStatus["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/enums.md#agreement-status'>Agreement Status</a>"]{<<enumeration>>}
  class TermDepositAgreement["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/entities/term-deposit-agreement.md'>Term Deposit Agreement</a>"]
  class LoanAgreement["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/entities/loan-agreement.md'>Loan Agreement</a>"]
  class PartyRole["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/entities/party_role.md'>Party Role</a>"]
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

  Agreement Status:
    type: enum:Agreement Status
    description: >
      The current lifecycle state of the agreement. Active agreements govern current
      obligations; Terminated and Matured agreements must be retained for audit. Used
      as a dimension attribute in agreement-level analytics and regulatory reporting
      of active product holdings.

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

An Agreement involves the Party Roles that are party to it: a Customer as borrower, a
guarantor, joint holders. A role can be party to several agreements (a guarantor may
guarantee more than one loan), so the relationship is many-to-many, and the capacity in
which the role participates is an attribute of the link.

```yaml
source: Agreement
type: governs
target: Party Role
cardinality: many-to-many
granularity: atomic
ownership: Agreement
relationship_attributes:
  - Role In Agreement
```
