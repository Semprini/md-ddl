# [Telecom](../domain.md)

## Events

### Subscription Activated

Emitted when a new Subscription transitions to Active status, signalling that the customer's commercial commitment has been accepted and service provisioning should begin.

```yaml
actor: Subscriber Management System
entity: Subscription
emitted_on:
  - create
  - update
business_meaning: Customer has accepted a product offering and their subscription is now commercially active. A Service Order must be triggered to provision the underlying network service.
downstream_impact:
  - Service Order is triggered to provision the network service
  - Billing system registers the recurring charge schedule
  - Customer analytics pipeline receives a new active subscriber event
attributes:
  event_timestamp:
    type: datetime
    description: Time the subscription was activated
  subscription_identifier:
    type: string
    description: Identifier of the activated subscription
  customer_identifier:
    type: string
    description: Identifier of the customer who activated the subscription
  product_offering_identifier:
    type: string
    description: Identifier of the product offering subscribed to
  agreed_monthly_charge:
    type: decimal
    description: The monthly recurring charge agreed at point of sale
  commitment_end_date:
    type: date
    description: Commitment end date for the subscription (null for month-to-month)
```
