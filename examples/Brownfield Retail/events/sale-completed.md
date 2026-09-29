# [Retail Sales (Brownfield)](../domain.md)

## Events

### Sale Completed

Emitted when a sales transaction is finalised at the point of sale. The existing nightly pipeline loads these as completed POS transactions (see the [daily sales load baseline](../baselines/etl/daily_sales_load.md)).

```yaml
actor: POS System
entity: Sale
emitted_on:
  - create
business_meaning: A customer purchase has been completed at a store and the sale is final
downstream_impact:
  - Daily sales reporting includes the sale
  - Store and product performance measures are updated
attributes:
  Event Timestamp:
    type: datetime
    description: When the sale was finalised at the point of sale
```
