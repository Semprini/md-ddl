# [Lab Information System](../source.md)

## LabProcedure

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | ProcedureId | Text | 64 | | | no | System-assigned lab procedure identifier | Procedure.Procedure Identifier
2 | PatientId | Text | 64 | | | no | Identifies which Patient this Procedure belongs to | Patient.Patient Identifier
3 | EncounterId | Text | 64 | | | yes | Identifies which Encounter this Procedure was performed in | Encounter.Encounter Identifier
4 | SNOMEDCode | Text | 20 | | | no | SNOMED CT code — source already uses canonical codes | Procedure.SNOMED Code
5 | StatusCode | Text | 20 | | | no | Procedure status code | [Map Procedure Status](#map-procedure-status)
6 | PerformedDttm | DateTime | | | | yes | Date and time procedure was performed | Procedure.Performed Date Time

### Map Procedure Status

Maps LIS status codes to canonical Procedure Status enum values.

```yaml
type: conditional
target: Procedure · Status
source:
  field: LabProcedure.StatusCode
cases:
  Preparation: "StatusCode == 'PREP'"
  In Progress: "StatusCode == 'INPROG'"
  Not Done: "StatusCode == 'NOTDONE'"
  On Hold: "StatusCode == 'HOLD'"
  Stopped: "StatusCode == 'STOPPED'"
  Completed: "StatusCode == 'COMPLETED'"
  Entered In Error: "StatusCode == 'ERROR'"
fallback: Completed
```
