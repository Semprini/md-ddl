# [Healthcare](../domain.md)

## Events

### Patient Admitted

Emitted when a patient is admitted and a new encounter begins. This event triggers downstream clinical workflows including bed assignment, care team notification, and medication reconciliation.

```yaml
actor: Registration Clerk
entity: Encounter
emitted_on:
  - create
business_meaning: A patient has been admitted to the facility and a clinical encounter has begun
downstream_impact:
  - Bed management and ward assignment workflows are triggered
  - Care team is notified of the new admission
  - Medication reconciliation process is initiated
  - Billing and insurance verification begins
attributes:
  event_timestamp:
    type: datetime
    description: Time the admission was recorded
  encounter_class:
    type: string
    description: Type of encounter (inpatient, outpatient, emergency)
  admitting_location:
    type: string
    description: Ward or department where the patient is admitted
  admitting_practitioner_id:
    type: string
    description: Identifier of the practitioner responsible for the admission
  reason_for_admission:
    type: string
    description: Primary reason for the clinical encounter
```
