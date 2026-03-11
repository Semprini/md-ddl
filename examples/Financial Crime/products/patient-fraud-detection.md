# [Financial Crime](../domain.md)

## Data Products

### Patient Financial Fraud Detection

Consumer-aligned product combining financial transaction activity with
healthcare patient and encounter context to detect cross-channel fraud,
synthetic identities, and abnormal billing or reimbursement patterns.

```yaml
class: consumer-aligned
schema_type: normalized
owner: financial.crime.analytics@bank.com
consumers:
  - Financial Crime Analytics
  - Enterprise Fraud Operations
  - Clinical Revenue Integrity
status: Production
version: "1.0.0"

entities:
  - Transaction
  - Party
  - Party Role
  - Account

cross_domain:
  - domain: Healthcare
    entities:
      - Patient
      - Encounter
      - Practitioner

governance:
  # Classification resolution: both contributing domains are
  # Highly Confidential at domain level. Effective classification remains
  # Highly Confidential.
  classification: Highly Confidential
  # Retention conflict: Financial Crime 10 years vs Healthcare 7 years.
  # Longest wins.
  retention: "10 years"
  # PII/PHI union across both contributing domains.
  pii: true
  # Regulatory scope union across both contributing domains.
  regulatory_scope:
    - AML (Anti-Money Laundering)
    - KYC (Know Your Customer)
    - CTF (Counter-Terrorist Financing)
    - FATF Recommendations
    - BSA (Bank Secrecy Act)
    - EU 5AMLD / 6AMLD
    - USA PATRIOT Act
    - HIPAA (Health Insurance Portability and Accountability Act)
    - HITECH Act
    - 21st Century Cures Act

masking:
  - attribute: "Patient.Given Name"
    strategy: redact
  - attribute: "Patient.Family Name"
    strategy: redact
  - attribute: "Patient.Date of Birth"
    strategy: year-only
  - attribute: "Practitioner.Given Name"
    strategy: tokenize
  - attribute: "Practitioner.Family Name"
    strategy: tokenize
  - attribute: "Party.Legal Name"
    strategy: hash
  - attribute: "Party.Also Known As"
    strategy: hash
  - attribute: "Transaction.Reference"
    strategy: truncate

sla:
  freshness: "< 4 hours"
  availability: "99.9%"
  latency_p99: "< 500ms"

refresh: hourly
```
