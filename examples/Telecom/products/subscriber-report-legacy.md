# [Telecom](../domain.md)

## Data Products

### Subscriber Report (Legacy)

Legacy wide-column subscriber view combining party identity with customer status and subscription summary. Superseded by the Canonical Subscriber product which provides richer relational context and correct handling of multi-subscription customers.

```yaml
class: consumer-aligned
schema_type: wide-column
owner: domain.telecom@telco.com
consumers:
  - Customer Analytics (migrating)
status: Deprecated
deprecated_date: "2025-06-01"
successor: "Canonical Subscriber"
version: "1.0.0"

entities:
  - Party
  - Individual
  - Customer

governance:
  classification: Confidential
  pii: true
  retention: "7 years post contract end"
```
