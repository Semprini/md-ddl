# [Healthcare](../domain.md)

## Entities

### Appointment

A booking of a healthcare event among patients, practitioners, related persons, and/or devices for a specific date/time. Aligned to the FHIR R4 Appointment resource, this entity represents scheduled future healthcare interactions that may or may not result in an Encounter.

Appointments use a period-granularity relationship to Encounters — the appointment captures scheduled time (when the visit is planned) while the encounter captures actual time (when the visit occurred). Comparing scheduled versus actual enables wait time analysis and scheduling efficiency reporting.

Appointment records change frequently throughout their lifecycle. In high-volume outpatient departments, a single appointment may be rescheduled multiple times, confirmed, cancelled, and re-booked before reaching a terminal state (Fulfilled or No Show). This high-churn pattern — driven by patient availability, practitioner schedules, and urgent clinical reprioritisation — makes Appointment a `frequently_changing` entity, distinct from clinical records like Patient or Condition which change infrequently.

```mermaid
---
config:
  layout: elk
---
classDiagram
  class Appointment{
    * Appointment Identifier : string
    Status : enum~AppointmentStatus~
    Service Type : string
    Scheduled Start : datetime
    Scheduled End : datetime
    Description : string
    Priority : integer
  }

  Patient "1" --> "0..*" Appointment : has
  Appointment "0..*" --> "0..1" Encounter : results in

  class AppointmentStatus["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Healthcare/enums.md#appointment-status'>Appointment Status</a>"]{<<enumeration>>}

  class Patient["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Healthcare/entities/patient.md'>Patient</a>"]
  class Encounter["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Healthcare/entities/encounter.md'>Encounter</a>"]
```

```yaml
existence: dependent
mutability: frequently_changing
temporal:
  tracking: valid_time
  description: >
    Valid time tracks the scheduled appointment window from Scheduled Start
    to Scheduled End. Appointments are frequently rescheduled — each reschedule
    changes the valid time window. Full history of reschedules is retained for
    scheduling variance analysis and no-show pattern detection.
attributes:
  Appointment Identifier:
    type: string
    identifier: primary
    description: Unique identifier for this appointment.

  Status:
    type: enum:Appointment Status
    description: Lifecycle status of the appointment (proposed, pending, booked, arrived, fulfilled, cancelled, noshow).

  Service Type:
    type: string
    description: Type of healthcare service scheduled (e.g. consultation, follow-up, imaging).

  Scheduled Start:
    type: datetime
    description: Planned start date and time of the appointment.

  Scheduled End:
    type: datetime
    description: Planned end date and time of the appointment.

  Description:
    type: string
    description: Brief description or reason for the appointment.

  Priority:
    type: integer
    description: Relative priority of the appointment (lower numbers are higher priority).
```

```yaml
constraints:
  Scheduled End After Start:
    check: "Scheduled End IS NULL OR Scheduled End > Scheduled Start"
    description: Appointment end must be after start.
```

```yaml
governance:
  pii: true
  classification: Confidential
  retention_basis: >
    Appointment scheduling data is PHI containing patient visit timing.
    Retained per domain default.
  access_role:
    - CLINICAL_STAFF
    - SCHEDULING
    - REGISTRATION
```

## Relationships

### Appointment Results In Encounter

A fulfilled Appointment results in an Encounter. This is a period-granularity relationship — the appointment captures the scheduled time window while the encounter captures the actual clinical interaction period. Comparing the two enables scheduling variance analysis.

```yaml
source: Appointment
type: produces
target: Encounter
cardinality: many-to-one
granularity: period
ownership: Appointment
```
