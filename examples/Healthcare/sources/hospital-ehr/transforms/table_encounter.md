# [Hospital EHR](../source.md)

## Encounter

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | EncounterId | Text | 64 | | | no | System-assigned encounter identifier | Encounter.Encounter Identifier
2 | PatientId | Text | 64 | | | no | Identifies which Patient this Encounter belongs to | Patient.Patient Identifier
3 | StatusCode | Text | 20 | | | no | Encounter lifecycle status code | [Map Encounter Status](#map-encounter-status)
4 | ClassCode | Text | 20 | | | no | Encounter classification code | [Map Encounter Class](#map-encounter-class)
5 | AdmissionDttm | DateTime | | | | yes | Admission or arrival date and time | Encounter.Admission Date Time
6 | DischargeDttm | DateTime | | | | yes | Discharge or departure date and time | Encounter.Discharge Date Time
7 | ReasonText | Text | 500 | | | yes | Free-text clinical reason for visit | Encounter.Reason

### Map Encounter Status

Maps EHR status codes to canonical Encounter Status enum values.

```yaml
type: conditional
target: Encounter · Status
source:
  field: Encounter.StatusCode
cases:
  Planned: "StatusCode == 'PLANNED'"
  Arrived: "StatusCode == 'ARRIVED'"
  Triaged: "StatusCode == 'TRIAGED'"
  In Progress: "StatusCode == 'INPROGRESS'"
  On Leave: "StatusCode == 'ONLEAVE'"
  Finished: "StatusCode == 'FINISHED'"
  Cancelled: "StatusCode == 'CANCELLED'"
fallback: In Progress
```

### Map Encounter Class

Maps EHR class codes to canonical Encounter Class enum values.

```yaml
type: conditional
target: Encounter · Class
source:
  field: Encounter.ClassCode
cases:
  Inpatient: "ClassCode == 'IMP'"
  Outpatient: "ClassCode == 'AMB'"
  Emergency: "ClassCode == 'EMER'"
  Virtual: "ClassCode == 'VR'"
  Home Health: "ClassCode == 'HH'"
fallback: Outpatient
```
