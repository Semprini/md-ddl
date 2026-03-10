# [Healthcare](../domain.md)

## Data Products

### Clinical Patient Record

The governed canonical representation of Patient, Encounter, Condition,
and related clinical entities for consumption by downstream domains and
cross-facility integration points. This product provides the standardized
clinical data model for any system that needs the full-fidelity patient
care record.

```yaml
class: domain-aligned
owner: clinical.data@hospital.org
consumers:
  - Cross-facility Integration
  - Health Information Exchange
  - Regulatory Reporting
status: Production
version: "1.0.0"

entities:
  - Patient
  - Encounter
  - Observation
  - Condition
  - Procedure
  - Medication Request
  - Care Plan
  - Practitioner
  - Practitioner Role

sla:
  freshness: "< 30 minutes"
  availability: "99.95%"

refresh: real-time
```
