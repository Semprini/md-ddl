# [Hospital EHR](../source.md)

## Appointment

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | AppointmentId | Text | 64 | | | no | System-assigned appointment identifier | Appointment.Appointment Identifier
2 | PatientId | Text | 64 | | | no | Identifies which Patient this Appointment belongs to | Patient.Patient Identifier
3 | StatusCode | Text | 20 | | | no | Appointment lifecycle status | [Map Appointment Status](#map-appointment-status)
4 | StartDttm | DateTime | | | | no | Scheduled start date and time | Appointment.Scheduled Start
5 | EndDttm | DateTime | | | | yes | Scheduled end date and time | Appointment.Scheduled End
6 | ServiceTypeCode | Text | 50 | | | yes | Type of clinical service being scheduled | Appointment.Service Type

### Map Appointment Status

Maps EHR status codes to canonical Appointment Status enum values.

```yaml
type: conditional
target: Appointment · Status
source:
  field: Appointment.StatusCode
cases:
  Proposed: "StatusCode == 'PROPOSED'"
  Pending: "StatusCode == 'PENDING'"
  Booked: "StatusCode == 'BOOKED'"
  Arrived: "StatusCode == 'ARRIVED'"
  Fulfilled: "StatusCode == 'FULFILLED'"
  Cancelled: "StatusCode == 'CANCELLED'"
  No Show: "StatusCode == 'NOSHOW'"
fallback: Booked
```
