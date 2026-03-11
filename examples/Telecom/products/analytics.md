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
status: Production
version: "1.0.0"

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
  - attribute: "Individual.Given Name"
    strategy: null
  - attribute: "Individual.Family Name"
    strategy: null
  - attribute: "Individual.Date of Birth"
    strategy: year-only
  - attribute: "Usage Record.Destination Number"
    strategy: truncate

sla:
  freshness: "< 1 hour"
  availability: "99.5%"

refresh: hourly
```
