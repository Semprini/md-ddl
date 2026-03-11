# [Retail Sales](../domain.md)

## Events

### Order Placed

Emitted when a customer submits a new purchase order. Triggers inventory reservation, payment processing, and fulfilment pipeline initiation.

```yaml
actor: Customer
entity: Order
emitted_on:
  - create
business_meaning: Customer has committed to purchasing one or more products. Inventory must be reserved, payment initiated, and the order routed to fulfilment.
downstream_impact:
  - Inventory system reserves stock for each order line
  - Payment gateway initiates charge against the customer's payment method
  - Fulfilment system receives the order for picking and packing
  - Customer receives order confirmation notification
attributes:
  event_timestamp:
    type: datetime
    description: Time the order was placed
  order_identifier:
    type: string
    description: Identifier of the placed order
  customer_identifier:
    type: string
    description: Identifier of the customer who placed the order
  total_amount:
    type: decimal
    description: Total value of the order
  currency_code:
    type: string
    description: ISO 4217 currency code for the order amount
  channel:
    type: string
    description: Sales channel through which the order was placed
  line_count:
    type: integer
    description: Number of distinct order lines
```
