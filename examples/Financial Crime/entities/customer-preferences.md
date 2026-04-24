# [Financial Crime](../domain.md)

## Entities

### Customer Preferences

Customer Preferences captures communication and consent preferences that apply to a specific customer relationship.

```mermaid
---
config:
  layout: elk
---
classDiagram
  class CustomerPreferences{
    * Preference Identifier : string
    Contact Preference : enum~ContactPreference~
    Marketing Consent : boolean
    Effective From : date
  }

  Customer "1" --> "0..1" CustomerPreferences : has

    class ContactPreference["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/enums.md#contact-preference'>Contact Preference</a>"]{<<enumeration>>}
    class Customer["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Financial%20Crime/entities/customer.md'>Customer</a>"]
```

```yaml
existence: dependent
mutability: slowly_changing
attributes:
  Preference Identifier:
    type: string
    identifier: primary
    description: Unique identifier for the customer preference profile.

  Contact Preference:
    type: enum:Contact Preference
    description: >
      The customer's preferred channel for outbound communication from the institution.
      Must be respected in all non-mandatory communications and drives CRM system routing.

  Marketing Consent:
    type: boolean
    description: Indicates whether the customer has consented to marketing communications.

  Effective From:
    type: date
    description: Date from which the current preference set applies.
```

```yaml
governance:
  retention_basis: Inherited from domain default retention of 10 years post relationship end for AML/CTF record-keeping
```

## Relationships

No relationships are sourced directly from Customer Preferences in the current domain model.
