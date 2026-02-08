# Customer

## Entities

### Customer
The primary representation of a customer in the organisation.

```yaml
attributes:
  - name: Customer Id
    type: string
    identifier: true
  - name: Email
    type: string
    pii: true
  - name: Loyalty Tier
    type: enum:LoyaltyTier
```
