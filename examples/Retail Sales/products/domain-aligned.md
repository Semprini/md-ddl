# [Retail Sales](../domain.md)

## Data Products

### Sales Domain Model

The authoritative domain-aligned view of the Retail Sales bounded context. Exposes the canonical Customer (sales definition), Product catalog, Order, and Order Line entities for integration with other domains. This product is the integration surface for the Customer 360 consumer product.

```yaml
class: domain-aligned
schema_type: normalized
owner: domain.sales@retailer.com
consumers:
  - Cross-domain Integration
  - Customer Experience Platform
status: Production
version: "1.0.0"

entities:
  - Customer
  - Product
  - Order
  - Order Line

# TODO: Add lineage once sources/ directory is populated for this domain.
# lineage:
#   - source: <pos-system or ecommerce-platform>
#     tables:
#       - <transform files>

governance:
  classification: Internal
  pii: true

masking:
  - attribute: "Customer.Email Address"
    strategy: hash

sla:
  freshness: "< 10 minutes"
  availability: "99.5%"

refresh: real-time
```

#### Logical Model

```mermaid
---
config:
  layout: elk
---
classDiagram
  class Customer{
    * Customer Identifier : string
    Email Address : string
    Given Name : string
    Family Name : string
    Loyalty Tier : enum~CustomerTier~
    Marketing Opt In : boolean
  }

  class Product{
    * Product Identifier : string
    SKU : string
    Name : string
    Category : string
    Unit Price : decimal
    Currency Code : string
    In Stock : boolean
  }

  class Order{
    * Order Identifier : string
    Status : enum~OrderStatus~
    Order Date : datetime
    Total Amount : decimal
    Currency Code : string
    Channel : string
  }

  class OrderLine{
    * Order Line Identifier : string
    Quantity : integer
    Agreed Unit Price : decimal
    Line Total : decimal
    Discount Amount : decimal
  }

  Customer "1" --> "0..*" Order : places
  Order "1" --> "1..*" OrderLine : contains
  OrderLine "0..*" --> "1" Product : references

  class Customer["<a href='../entities/customer.md'>Customer</a>"]
  class Product["<a href='../entities/product.md'>Product</a>"]
  class Order["<a href='../entities/order.md'>Order</a>"]
  class OrderLine["<a href='../entities/order_line.md'>Order Line</a>"]
```
