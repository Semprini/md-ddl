# Lab Information System

Lab Information System (LIS) manages laboratory specimen processing, test execution, and result reporting. It is the authoritative source for laboratory observations including blood chemistry, hematology, microbiology, and pathology results.

## Metadata

```yaml
id: lab-information-system
owner: laboratory.services@hospital.org
steward: laboratory.director@hospital.org

change_model: event-driven
change_events:
  - Specimen Received
  - Test Completed
  - Result Released
  - Result Amended

update_frequency: near-real-time
data_quality_tier: 1
status: Production
version: "1.0.0"

tags:
  - Laboratory
  - Diagnostics
  - Clinical
```

## [Healthcare](../../domain.md) Feeds

Canonical Entity | Transform File | Attributes Contributed | Change Model
--- | --- | --- | ---
[Observation](../../entities/observation.md#observation) | [table_lab_result](transforms/table_lab_result.md) | Observation Identifier, LOINC Code, Value, Unit, Status, Effective Date Time, Issued Date Time | event-driven
[Procedure](../../entities/procedure.md#procedure) | [table_lab_procedure](transforms/table_lab_procedure.md) | Procedure Identifier, SNOMED Code, Status, Performed Date Time | event-driven
