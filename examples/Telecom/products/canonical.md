# [Telecom](../domain.md)

## Data Products

### Canonical Subscriber

The authoritative domain-aligned view of subscriber identity, commercial status, and active subscriptions. This product is the primary integration surface for other domains that need subscriber context — it exposes the canonical Telecom domain model without denormalization or product-specific shaping.

```yaml
class: domain-aligned
schema_type: normalized
owner: domain.telecom@telco.com
consumers:
  - Cross-domain Integration
  - Identity Resolution Platform
  - Financial Crime Analytics
status: Active
version: "1.0.0"

entities:
  - Party
  - Individual
  - Organization
  - Customer
  - Subscription
  - Product Offering

lineage:
  - source: bss-oss
    tables:
      - table_subscriber
      - table_business_account
      - table_customer
      - table_product_catalog
      - table_subscription

governance:
  classification: Confidential
  pii: true
  retention: "7 years post contract end"

masking:
  - attribute: "Individual.Date of Birth"
    strategy: year-only
  - attribute: "Individual.Identity Document Number"
    strategy: hash

sla:
  freshness: "< 5 minutes"
  availability: "99.9%"

refresh: real-time
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
    Party Type : enum~PartyType~
  }

  class Individual{
    Given Name : string
    Family Name : string
    Date of Birth : date
    Email Address : string
    Mobile Number : string
    Identity Document Type : string
    Identity Document Number : string
  }

  class Organization{
    Legal Name : string
    Trading Name : string
    Registration Number : string
    Industry Sector Code : string
    VAT Number : string
  }

  class Customer{
    * Customer Identifier : string
    Status : enum~CustomerStatus~
    Customer Since Date : date
    Segment : string
    Account Manager : string
  }

  class Subscription{
    * Subscription Identifier : string
    Status : enum~SubscriptionStatus~
    Agreed Monthly Charge : decimal
    Start Date : date
    Commitment End Date : date
    Auto Renew : boolean
  }

  class ProductOffering{
    * Product Offering Identifier : string
    Name : string
    Offering Type : enum~ProductOfferingType~
    Monthly Charge : decimal
    Currency Code : string
    Data Allowance GB : decimal
    Voice Allowance Minutes : integer
    Commitment Period Months : integer
    Valid From Date : date
    Valid To Date : date
  }

  Individual --|> Party
  Organization --|> Party
  Party "1" --> "0..*" Customer : has
  Customer "1" --> "0..*" Subscription : has
  Subscription "0..*" --> "1" ProductOffering : activates

  class Party["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Telecom/entities/party.md'>Party</a>"]
  class Individual["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Telecom/entities/individual.md'>Individual</a>"]
  class Organization["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Telecom/entities/organization.md'>Organization</a>"]
  class Customer["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Telecom/entities/customer.md'>Customer</a>"]
  class Subscription["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Telecom/entities/subscription.md'>Subscription</a>"]
  class ProductOffering["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Telecom/entities/product_offering.md'>Product Offering</a>"]
```
