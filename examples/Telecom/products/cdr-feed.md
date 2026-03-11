# [Telecom](../domain.md)

## Data Products

### CDR Raw Feed

Source-aligned product exposing the raw call detail records from the BSS/OSS mediation layer with minimal transformation. Intended for the Data Engineering team to load into the data lake for downstream processing, archival, and ad-hoc analysis.

```yaml
class: source-aligned
source: bss-oss
owner: platform.engineering@telco.com
consumers:
  - Data Engineering
  - Revenue Assurance
status: Production
version: "1.0.0"

governance:
  classification: Highly Confidential
  pii: true
  retention: "7 years"

sla:
  freshness: "< 2 minutes"
  availability: "99.9%"

refresh: real-time
```
