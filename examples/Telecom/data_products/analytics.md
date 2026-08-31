# [Telecom](../domain.md)

## Data Products

### Subscriber Usage Analytics

A dimensional star schema combining subscriber identity, subscription terms, and usage volumes for network analytics and revenue assurance reporting. Designed for OLAP-style queries — slicing usage by customer segment, service type, geography, and time period.

The dimensional model places Usage Record at the centre as the fact table, with Customer, Subscription, Product Offering, and Service as surrounding dimension tables. This structure enables efficient query patterns for standard analytics use cases without requiring joins across the full normalized model.

```yaml
class: consumer-aligned
schema_type: dimensional
owner: revenue.assurance@telco.com
consumers:
  - Network Analytics
  - Revenue Assurance
  - Executive Reporting
status: Active
version: "1.0.0"

entities:
  - Usage Record Fact
  - Customer Dimension
  - Individual Dimension
  - Subscription Dimension
  - Product Offering Dimension
  - Service Dimension

lineage:
  - domain: Telecom
    entities:
      - Usage Record
      - Service
      - Subscription
      - Product Offering
      - Customer
      - Individual

governance:
  classification: Confidential
  pii: true
  retention: "7 years"
  masking:
    - attribute: "Individual Dimension.Given Name"
      strategy: null
    - attribute: "Individual Dimension.Family Name"
      strategy: null
    - attribute: "Individual Dimension.Date of Birth"
      strategy: year-only
    - attribute: "Usage Record Fact.Destination Number"
      strategy: truncate

sla:
  freshness: "< 1 hour"
  availability: "99.5%"

refresh: hourly
```

#### Logical Model

Dimensional model with Usage Record as the central fact and five surrounding
dimension tables. All measures and foreign keys live in the fact; descriptive
attributes live in the dimensions.

```mermaid
---
config:
  layout: elk
---
classDiagram
  class UsageRecordFact{
    <<fact>>
    * Usage Record Identifier : string
    Customer Key : string
    Subscription Key : string
    Product Offering Key : string
    Service Key : string
    Usage Type : enum~UsageType~
    Volume : decimal
    Volume Unit : string
    Duration Seconds : integer
    Session Start : datetime
    Session End : datetime
    Destination Number : string
    Roaming Indicator : boolean
    Rated Amount : decimal
    Currency Code : string
  }

  class CustomerDimension{
    <<dimension>>
    * Customer Key : string
    Customer Identifier : string
    Status : enum~CustomerStatus~
    Customer Since Date : date
    Segment : string
  }

  class IndividualDimension{
    <<dimension>>
    * Customer Key : string
    Given Name : string
    Family Name : string
    Date of Birth : date
    Mobile Number : string
  }

  class SubscriptionDimension{
    <<dimension>>
    * Subscription Key : string
    Subscription Identifier : string
    Status : enum~SubscriptionStatus~
    Agreed Monthly Charge : decimal
    Start Date : date
    Commitment End Date : date
  }

  class ProductOfferingDimension{
    <<dimension>>
    * Product Offering Key : string
    Product Offering Identifier : string
    Name : string
    Offering Type : enum~ProductOfferingType~
    Monthly Charge : decimal
    Data Allowance GB : decimal
    Voice Allowance Minutes : integer
  }

  class ServiceDimension{
    <<dimension>>
    * Service Key : string
    Service Identifier : string
    Service Number : string
    Service Type : string
    Status : enum~ServiceStatus~
    Activation Date : date
  }

  UsageRecordFact "0..*" --> "1" CustomerDimension : customer
  UsageRecordFact "0..*" --> "1" SubscriptionDimension : subscription
  UsageRecordFact "0..*" --> "1" ProductOfferingDimension : product offering
  UsageRecordFact "0..*" --> "1" ServiceDimension : service
  CustomerDimension "1" --> "0..1" IndividualDimension : identity
```

#### Attribute Mapping

##### Usage Record Fact

Product Attribute | Source | Path | Transform
--- | --- | --- | ---
Usage Record Identifier | Usage Record.Usage Record Identifier | — | —
Customer Key | Customer.Customer Identifier | Usage Record → Service → Subscription → Customer | —
Subscription Key | Subscription.Subscription Identifier | Usage Record → Service → Subscription | —
Product Offering Key | Product Offering.Product Offering Identifier | Usage Record → Service → Subscription → Product Offering | —
Service Key | Service.Service Identifier | Usage Record → Service | —
Usage Type | Usage Record.Usage Type | — | —
Volume | Usage Record.Volume | — | —
Volume Unit | Usage Record.Volume Unit | — | —
Duration Seconds | Usage Record.Duration Seconds | — | —
Session Start | Usage Record.Session Start | — | —
Session End | Usage Record.Session End | — | —
Destination Number | Usage Record.Destination Number | — | —
Roaming Indicator | Usage Record.Roaming Indicator | — | —
Rated Amount | Usage Record.Rated Amount | — | —
Currency Code | Usage Record.Currency Code | — | —

##### Customer Dimension

Product Attribute | Source | Path | Transform
--- | --- | --- | ---
Customer Key | Customer.Customer Identifier | — | —
Customer Identifier | Customer.Customer Identifier | — | —
Status | Customer.Status | — | —
Customer Since Date | Customer.Customer Since Date | — | —
Segment | Customer.Segment | — | —

##### Individual Dimension

Product Attribute | Source | Path | Transform
--- | --- | --- | ---
Customer Key | Customer.Customer Identifier | Individual → Party → Customer | —
Given Name | Individual.Given Name | — | —
Family Name | Individual.Family Name | — | —
Date of Birth | Individual.Date of Birth | — | —
Mobile Number | Individual.Mobile Number | — | —

##### Subscription Dimension

Product Attribute | Source | Path | Transform
--- | --- | --- | ---
Subscription Key | Subscription.Subscription Identifier | — | —
Subscription Identifier | Subscription.Subscription Identifier | — | —
Status | Subscription.Status | — | —
Agreed Monthly Charge | Subscription.Agreed Monthly Charge | — | —
Start Date | Subscription.Start Date | — | —
Commitment End Date | Subscription.Commitment End Date | — | —

##### Product Offering Dimension

Product Attribute | Source | Path | Transform
--- | --- | --- | ---
Product Offering Key | Product Offering.Product Offering Identifier | — | —
Product Offering Identifier | Product Offering.Product Offering Identifier | — | —
Name | Product Offering.Name | — | —
Offering Type | Product Offering.Offering Type | — | —
Monthly Charge | Product Offering.Monthly Charge | — | —
Data Allowance GB | Product Offering.Data Allowance GB | — | —
Voice Allowance Minutes | Product Offering.Voice Allowance Minutes | — | —

##### Service Dimension

Product Attribute | Source | Path | Transform
--- | --- | --- | ---
Service Key | Service.Service Identifier | — | —
Service Identifier | Service.Service Identifier | — | —
Service Number | Service.Service Number | — | —
Service Type | Service.Service Type | — | —
Status | Service.Status | — | —
Activation Date | Service.Activation Date | — | —
