# [Hospital EHR](../source.md)

## Diagnosis

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | DiagnosisId | Text | 64 | | | no | System-assigned diagnosis identifier | Condition.Condition Identifier
2 | PatientId | Text | 64 | | | no | Identifies which Patient this Condition belongs to | Patient.Patient Identifier
3 | EncounterId | Text | 64 | | | yes | Identifies which Encounter this Condition was recorded in | Encounter.Encounter Identifier
4 | ICD10Code | Text | 10 | | | no | ICD-10-CM diagnosis code — source already uses canonical codes | Condition.ICD-10 Code
5 | ClinicalStatusCode | Text | 20 | | | no | Clinical status of the condition | [Map Clinical Status](#map-clinical-status)
6 | OnsetDate | Date | | | | yes | Date condition was first identified | Condition.Onset
7 | SeverityText | Text | 50 | | | yes | Clinician-assigned severity description | Condition.Severity

### Map Clinical Status

Maps EHR clinical status codes to canonical Condition Clinical Status enum values.

```yaml
type: conditional
target: Condition · Clinical Status
source:
  field: Diagnosis.ClinicalStatusCode
cases:
  Active: "ClinicalStatusCode == 'ACTIVE'"
  Recurrence: "ClinicalStatusCode == 'RECURRENCE'"
  Relapse: "ClinicalStatusCode == 'RELAPSE'"
  Inactive: "ClinicalStatusCode == 'INACTIVE'"
  Remission: "ClinicalStatusCode == 'REMISSION'"
  Resolved: "ClinicalStatusCode == 'RESOLVED'"
fallback: Active
```
