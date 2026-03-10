# [Healthcare](../domain.md)

## Events

### Observation Recorded

Emitted when a clinical observation or laboratory result is recorded in the system. High-volume event — a single encounter can generate dozens of observations (vital signs, lab panels, imaging results).

```yaml
actor: Practitioner
entity: Observation
emitted_on:
  - create
business_meaning: A clinical measurement or laboratory result has been recorded for a patient
downstream_impact:
  - Clinical decision support rules are evaluated against the new result
  - Abnormal results trigger alert workflows to the responsible clinician
  - Quality measures and clinical dashboards are updated
attributes:
  event_timestamp:
    type: datetime
    description: Time the observation was recorded in the system
  observation_code:
    type: string
    description: LOINC code identifying the type of observation
  value_quantity:
    type: decimal
    description: Numeric result value
  value_unit:
    type: string
    description: Unit of measure for the result
  status:
    type: string
    description: Status of the observation (preliminary, final, amended)
  interpretation:
    type: string
    description: Clinical interpretation (normal, high, low, critical)
```
