# [Telecom](../domain.md)

## Data Products

### Telecom Fraud Intelligence

Consumer-aligned product combining subscriber identity, usage patterns, and subscription activity with financial transaction data from the Financial Crime domain to detect cross-channel fraud — SIM swap attacks, subscription fraud, account takeover, and synthetic identity schemes that span both telecom and financial systems.

Governance note: This product combines PCI-DSS-regulated telecom data with AML/GDPR-regulated financial crime data. The effective classification is Highly Confidential and the regulatory scope is the union of both contributing domains. The strictest retention obligation (10 years, from Financial Crime) applies.

```yaml
class: consumer-aligned
schema_type: normalized
owner: telecom.fraud@telco.com
consumers:
  - Financial Crime Analytics
  - Telecom Fraud Operations
  - Enterprise Fraud Operations
status: Production
version: "1.0.0"

entities:
  - Customer
  - Individual
  - Subscription
  - Service
  - Usage Record

cross_domain:
  - domain: Financial Crime
    entities:
      - Party
      - Transaction
      - Account

governance:
  classification: Highly Confidential
  pii: true
  retention: "10 years"
  regulatory_scope:
    - PCI-DSS (Payment Card Industry Data Security Standard)
    - GDPR (General Data Protection Regulation)
    - AML (Anti-Money Laundering)
    - KYC (Know Your Customer)
    - CPNI (Customer Proprietary Network Information)

masking:
  - attribute: "Individual.Given Name"
    strategy: tokenize
  - attribute: "Individual.Family Name"
    strategy: tokenize
  - attribute: "Individual.Date of Birth"
    strategy: year-only
  - attribute: "Individual.Identity Document Number"
    strategy: hash
  - attribute: "Usage Record.Destination Number"
    strategy: hash
  - attribute: "Billing Account.Payment Method Token"
    strategy: redact

sla:
  freshness: "< 15 minutes"
  availability: "99.9%"
  latency_p99: "< 500ms"

refresh: real-time
```
