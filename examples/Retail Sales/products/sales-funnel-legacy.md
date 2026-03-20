# [Retail Sales](../domain.md)

## Data Products

### Sales Funnel Report (Legacy)

Legacy wide-column funnel view that combined customer acquisition data with first-order metrics. Superseded by the Customer 360 product which provides richer cross-domain context and correct separation of buyer and contact identities.

```yaml
class: consumer-aligned
schema_type: wide-column
owner: domain.sales@retailer.com
consumers:
  - Marketing Analytics (migrating)
status: Deprecated
deprecated_date: "2025-09-01"
successor: "Customer 360"
version: "1.0.0"

entities:
  - Customer
  - Order

lineage:
  - domain: Retail Sales
    entities:
      - Customer
      - Order

governance:
  classification: Internal
  pii: true
```
