# [Healthcare](../domain.md)

## Data Products

### Clinical Outcomes Dashboard

A consumer-aligned analytics product optimised for clinical outcomes
research, population health analysis, and quality-of-care metrics.
Exposes the relationships between patients, conditions, procedures, and
care plans as a knowledge graph for flexible traversal queries.

```yaml
class: consumer-aligned
owner: analytics.team@hospital.org
consumers:
  - Clinical Research
  - Quality Improvement
  - Population Health Management
status: Production
version: "1.0.0"
schema_type: knowledge-graph

entities:
  - Patient
  - Encounter
  - Observation
  - Condition
  - Procedure
  - Care Plan

governance:
  regulatory_scope:
    - HIPAA
    - HITECH
  classification: PHI
  retention: "7 years post last encounter"

masking:
  - entity: Patient
    attributes:
      - Given Name
      - Family Name
      - Date of Birth
    strategy: pseudonymise
  - entity: Observation
    attributes:
      - Value
    strategy: generalise

sla:
  freshness: "< 4 hours"
  availability: "99.9%"

refresh: hourly
```
