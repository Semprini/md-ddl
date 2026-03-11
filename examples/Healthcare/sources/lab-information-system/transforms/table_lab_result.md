# [Lab Information System](../source.md)

## LabResult

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | ResultId | Text | 64 | | | no | System-assigned lab result identifier | Observation.Observation Identifier
2 | PatientId | Text | 64 | | | no | Identifies which Patient this Observation belongs to | Patient.Patient Identifier
3 | EncounterId | Text | 64 | | | yes | Identifies which Encounter this Observation was recorded in | Encounter.Encounter Identifier
4 | LOINCCode | Text | 20 | | | no | LOINC code — source already uses canonical codes | Observation.Code
5 | NumericValue | Decimal | | 18 | 6 | yes | Numeric measurement value | Observation.Value Quantity
6 | ValueUnits | Text | 50 | | | yes | Unit of measurement (e.g. mg/dL, bpm) | Observation.Value Unit
7 | TextValue | Text | 1000 | | | yes | Free-text result where numeric is not applicable | Observation.Value Text
8 | StatusCode | Text | 20 | | | no | Result status code | [Map Result Status](#map-result-status)
9 | SpecimenDttm | DateTime | | | | yes | Date and time specimen was collected | Observation.Effective Date Time
10 | ReportedDttm | DateTime | | | | no | Date and time result was released to the EHR | Observation.Issued Date Time

### Map Result Status

Maps LIS result status codes to canonical Observation Status enum values.

```yaml
type: conditional
target: Observation · Status
source:
  field: LabResult.StatusCode
cases:
  Registered: "StatusCode == 'R'"
  Preliminary: "StatusCode == 'P'"
  Final: "StatusCode == 'F'"
  Amended: "StatusCode == 'C'"
  Cancelled: "StatusCode == 'X'"
  Entered In Error: "StatusCode == 'W'"
fallback: Final
```
