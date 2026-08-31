# [Financial Crime](../domain.md)

## Data Products

### Canonical Party

The governed canonical representation of Party, Party Role, and related
identity entities for consumption by downstream domains and cross-domain
integration points.

```yaml
class: domain-aligned
schema_type: normalized
owner: data.architecture@bank.com
consumers:
  - Cross-domain Integration
  - Customer Domain
  - Regulatory Reporting
status: Active
version: "1.0.0"

entities:
  - Party
  - Person
  - Company
  - Party Role
  - Customer
  - Contact Address
  - Address

lineage:
  - source: salesforce-crm
    tables:
      - table_account
      - table_contact
      - table_contact_point
  - source: sap-fraud-management
    tables:
      - table_sanctions_screening
      - table_customer_risk_profile

sla:
  freshness: "< 1 hour"
  availability: "99.95%"

refresh: hourly
```

#### Logical Model

```mermaid
---
config:
  layout: elk
---
classDiagram
  class Party{
    <<abstract>>
    * Party Identifier : string
    Legal Name : string
    Also Known As : string[]
    Party Status : enum~PartyStatus~
    Risk Rating : enum~FinancialCrimeRiskRating~
    Sanctions Screen Status : enum~SanctionsScreenStatus~
    Next Review Date : date
  }

  class Person{
    Date of Birth : date
    Country of Birth : string
    Nationality : string[]
    Country of Residence : string
    Politically Exposed Person Status : enum~PEPStatus~
  }

  class Company{
    Company Registration Number : string
    Incorporation Country : string
    Incorporation Date : date
  }

  class PartyRole{
    <<abstract>>
    * Role Identifier : string
    Role Status : enum~PartyRoleStatus~
    Role Start Date : date
    Role End Date : date
    Due Diligence Status : enum~DDStatus~
  }

  class Customer{
    * Customer Number : string
    Onboarding Date : date
    Relationship Start Date : date
  }

  class ContactAddress{
    * Contact Address Identifier : string
    Address Purpose : enum~AddressPurpose~
    Is Primary : boolean
    Verification Status : enum~AddressVerificationStatus~
    Verification Date : date
    Verification Method : enum~VerificationMethod~
    Valid From : date
    Valid To : date
  }

  class Address{
    * Address Identifier : string
    Address Type : enum~AddressType~
    Address Line 1 : string
    Address Line 2 : string
    Suburb : string
    City : string
    State Or Region : string
    Postcode : string
    Country : string
  }

  Person --|> Party
  Company --|> Party
  Customer --|> PartyRole
  Party "1" --> "0..*" PartyRole : assumes
  Party "1" --> "0..*" ContactAddress : has
  PartyRole "0..*" --> "0..*" ContactAddress : uses
  ContactAddress "0..*" --> "1" Address : references

  class Party["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/entities/party.md'>Party</a>"]
  class Person["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/entities/person.md'>Person</a>"]
  class Company["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/entities/company.md'>Company</a>"]
  class PartyRole["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/entities/party_role.md'>Party Role</a>"]
  class Customer["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/entities/customer.md'>Customer</a>"]
  class ContactAddress["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/entities/contact_address.md'>Contact Address</a>"]
  class Address["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/entities/address.md'>Address</a>"]
```
