# [Hospital EHR](../source.md)

## MedicationOrder

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | OrderId | Text | 64 | | | no | System-assigned medication order identifier | Medication Request.Medication Request Identifier
2 | PatientId | Text | 64 | | | no | Identifies which Patient this order belongs to | Patient.Patient Identifier
3 | EncounterId | Text | 64 | | | yes | Identifies which Encounter this order was created in | Encounter.Encounter Identifier
4 | StatusCode | Text | 20 | | | no | Medication order lifecycle status | [Map Medication Status](#map-medication-status)
5 | DrugName | Text | 255 | | | no | Generic or brand medication name | Medication Request.Medication Name
6 | DosageInstruction | Text | 500 | | | yes | Dosage and administration instructions | Medication Request.Dosage
7 | OrderedDate | Date | | | | no | Date the order was created | Medication Request.Authored On

### Map Medication Status

Maps EHR order status codes to canonical Medication Request Status enum values.

```yaml
type: conditional
target: Medication Request · Status
source:
  field: MedicationOrder.StatusCode
cases:
  Active: "StatusCode == 'ACTIVE'"
  On Hold: "StatusCode == 'HOLD'"
  Cancelled: "StatusCode == 'CANCELLED'"
  Completed: "StatusCode == 'COMPLETED'"
  Entered In Error: "StatusCode == 'ERROR'"
  Stopped: "StatusCode == 'STOPPED'"
  Draft: "StatusCode == 'DRAFT'"
fallback: Active
```
