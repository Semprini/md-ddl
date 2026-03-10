# [Financial Crime](../domain.md)

## Events

### Customer Onboarded

Emitted when a new Customer relationship is established and approved for service.

```yaml
actor: Party
entity: Customer
emitted_on:
  - create
business_meaning: A party has completed onboarding and is now recognized as a customer
downstream_impact:
  - Customer profile is activated for product and service interactions
  - Ongoing due diligence schedule is initialized
attributes:
  event_timestamp:
    type: datetime
    description: Time the customer onboarding status became active
```
