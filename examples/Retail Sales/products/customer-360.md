# [Retail Sales](../domain.md)

## Data Products

### Customer 360

Consumer-aligned product combining the Retail Sales Customer (buyer identity) with the Retail Service Customer (contact identity) to produce a unified view of the customer across both domains. Designed for customer experience teams who need to see a customer's purchase history alongside their service interactions in a single view.

This product demonstrates the Bounded Context integration pattern: because the two domains define Customer differently (Sales = buyer; Service = contact), they cannot share a canonical entity. Instead, each domain publishes its own domain-aligned product and this consumer-aligned product joins them at the product layer, under explicit governance.

```yaml
class: consumer-aligned
schema_type: normalized
owner: customer.experience@retailer.com
consumers:
  - Customer Experience
  - Marketing
  - Customer Service
status: Production
version: "1.0.0"

entities:
  - Customer
  - Order
  - Order Line

cross_domain:
  - domain: Retail Service
    entities:
      - Customer
      - Service Request
      - Service Case

governance:
  classification: Internal
  pii: true
  retention: "5 years post last interaction"

masking:
  - attribute: "Retail Sales Customer.Email Address"
    strategy: hash
  - attribute: "Retail Sales Customer.Given Name"
    strategy: redact
  - attribute: "Retail Sales Customer.Family Name"
    strategy: redact
  - attribute: "Retail Service Customer.Email Address"
    strategy: hash

sla:
  freshness: "< 30 minutes"
  availability: "99.5%"

refresh: hourly
```
