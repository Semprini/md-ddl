# [Financial Crime](../domain.md)

## Events

### Account Status Changed

Emitted when an account status changes in a way that affects operational behavior.

```yaml
actor: Customer
entity: Account
emitted_on:
  - update
business_meaning: The account lifecycle status has changed and associated controls may differ
downstream_impact:
  - Transaction permissions and servicing controls may be recalculated
  - Compliance and customer notification workflows may be initiated
attributes:
  event_timestamp:
    type: datetime
    description: Time the account status change was recorded
```
