# [Retail Sales](domain.md)

## Enums

### Order Status

Lifecycle status of a purchase order.

```yaml
type: enum
values:
  - Pending Payment
  - Confirmed
  - Processing
  - Shipped
  - Delivered
  - Cancelled
  - Returned
```

### Customer Tier

Loyalty tier of the customer based on cumulative spend.

```yaml
type: enum
values:
  - Standard
  - Silver
  - Gold
  - Platinum
```
