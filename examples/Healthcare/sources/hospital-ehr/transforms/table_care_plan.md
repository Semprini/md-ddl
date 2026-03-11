# [Hospital EHR](../source.md)

## CarePlan

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | CarePlanId | Text | 64 | | | no | System-assigned care plan identifier | Care Plan.Care Plan Identifier
2 | PatientId | Text | 64 | | | no | Identifies which Patient this Care Plan belongs to | Patient.Patient Identifier
3 | StatusCode | Text | 20 | | | no | Care plan lifecycle status | [Map Care Plan Status](#map-care-plan-status)
4 | PlanTitle | Text | 255 | | | no | Descriptive title of the care plan | Care Plan.Title
5 | PeriodStartDate | Date | | | | yes | Date the care plan becomes or became active | Care Plan.Period Start
6 | PeriodEndDate | Date | | | | yes | Planned or actual end date of the care plan | Care Plan.Period End

### Map Care Plan Status

Maps EHR status codes to canonical Care Plan Status enum values.

```yaml
type: conditional
target: Care Plan · Status
source:
  field: CarePlan.StatusCode
cases:
  Draft: "StatusCode == 'DRAFT'"
  Active: "StatusCode == 'ACTIVE'"
  On Hold: "StatusCode == 'HOLD'"
  Revoked: "StatusCode == 'REVOKED'"
  Completed: "StatusCode == 'COMPLETED'"
  Entered In Error: "StatusCode == 'ERROR'"
fallback: Active
```
