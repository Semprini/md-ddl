# [Financial Crime](../domain.md)

## Data Products

### Party Risk Report (Legacy)

Legacy denormalized party risk view that combined party identity with
risk rating and due diligence status. Superseded by the Transaction Risk
Summary product which provides richer transaction-level context.

```yaml
class: consumer-aligned
schema_type: wide-column
owner: fincrime.analytics@bank.com
consumers:
  - Financial Crime Analytics (migrating)
status: Deprecated
deprecated_date: "2025-01-15"
successor: "Transaction Risk Summary"
version: "1.0.0"

entities:
  - Party
  - Party Role
  - Customer

governance:
  classification: Highly Confidential
  pii: true
  retention: "10 years"
```
