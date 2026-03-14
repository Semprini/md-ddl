# [Financial Crime](../domain.md)

## Data Products

### Transaction Risk Summary

A denormalized wide-column view combining transaction details with party
identity, account context, and risk indicators for the financial crime
analytics team. Designed for high-volume scan queries without joins.

```yaml
class: consumer-aligned
schema_type: wide-column
owner: fincrime.analytics@bank.com
consumers:
  - Financial Crime Analytics
  - Transaction Monitoring Dashboard
status: Active
version: "1.0.0"

entities:
  - Transaction
  - Party
  - Party Role
  - Account
  - Branch

governance:
  classification: Highly Confidential
  pii: true
  retention: "10 years"
  masking:
    - attribute: "Date of Birth"
      strategy: year-only
    - attribute: "Tax Identification Number"
      strategy: hash

sla:
  freshness: "< 15 minutes"
  availability: "99.9%"

refresh: real-time
```
