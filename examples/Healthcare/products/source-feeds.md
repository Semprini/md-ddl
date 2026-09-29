# [Healthcare](../domain.md)

## Data Products

### Lab Results Raw Feed

Raw event feed from the Lab Information System preserving source schema and
result events for pipeline replay, integration debugging, and regulatory
audit trails. Provides unmasked laboratory data for data engineering
pipelines upstream of canonical transformation.

```yaml
class: source-aligned
source: lab-information-system
owner: health.it@hospital.org
consumers:
  - Data Engineering
  - Clinical Informatics
status: Production
version: "1.0.0"

governance:
  classification: Highly Confidential
  pii: true
  retention: "7 years post last encounter"
  regulatory_scope:
    - HIPAA (Health Insurance Portability and Accountability Act)
    - HITECH Act
  access_role:
    - DATA_ENGINEERING
    - CLINICAL_INFORMATICS

sla:
  freshness: "< 2 minutes"
  availability: "99.9%"

refresh: near-real-time
```
