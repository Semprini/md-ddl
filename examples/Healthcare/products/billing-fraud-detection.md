# [Healthcare](../domain.md)

## Data Products

### Clinical Billing Fraud Detection

Consumer-aligned product combining encounter and patient context with
financial transaction behavior to detect billing anomalies, duplicated
claims, and suspicious reimbursement patterns.

```yaml
class: consumer-aligned
schema_type: normalized
owner: revenue.integrity@hospital.org
consumers:
  - Revenue Integrity
  - Clinical Compliance
  - Financial Crime Operations
status: Production
version: "1.0.0"

entities:
  - Patient
  - Encounter
  - Practitioner
  - Observation

cross_domain:
  - domain: Financial Crime
    entities:
      - Transaction
      - Party
      - Account

governance:
  # Classification conflict: Healthcare (Highly Confidential) vs Financial
  # Crime (Highly Confidential). Highest wins.
  classification: Highly Confidential
  # Retention conflict: Healthcare 7 years vs Financial Crime 10 years.
  # Longest wins.
  retention: "10 years"
  # PII/PHI union across both contributing domains.
  pii: true
  # Regulatory scope union across both contributing domains.
  regulatory_scope:
    - HIPAA (Health Insurance Portability and Accountability Act)
    - HITECH Act
    - 21st Century Cures Act
    - AML (Anti-Money Laundering)
    - KYC (Know Your Customer)
    - CTF (Counter-Terrorist Financing)
    - FATF Recommendations
    - BSA (Bank Secrecy Act)
    - EU 5AMLD / 6AMLD
    - USA PATRIOT Act

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
    strategy: null
  - attribute: "Account.Account Number"
    strategy: hash

sla:
  freshness: "< 4 hours"
  availability: "99.9%"
  latency_p99: "< 800ms"

refresh: hourly
```
