# [Healthcare](../domain.md)

## Events

### Medication Prescribed

Emitted when a new medication order is created for a patient. This event triggers pharmacy workflows, drug interaction checks, and formulary verification.

```yaml
actor: Practitioner
entity: Medication Request
emitted_on:
  - create
business_meaning: A clinician has prescribed a medication for a patient
downstream_impact:
  - Pharmacy receives the order for dispensing
  - Drug-drug interaction checks are performed automatically
  - Formulary compliance is verified against payer coverage
  - Medication administration schedule is generated
attributes:
  event_timestamp:
    type: datetime
    description: Time the medication request was authored
  medication_name:
    type: string
    description: Name of the medication prescribed
  dosage:
    type: string
    description: Dosage instructions for the medication
  priority:
    type: string
    description: Urgency of the medication request (routine, urgent, stat)
  prescribing_practitioner_id:
    type: string
    description: Identifier of the practitioner who authored the prescription
```
