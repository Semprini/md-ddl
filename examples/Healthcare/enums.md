# [Healthcare](domain.md)

## Enums

### Encounter Status

Lifecycle status of a clinical encounter. Aligned to FHIR R4 EncounterStatus value set.

Standard: [FHIR R4 EncounterStatus](http://hl7.org/fhir/R4/valueset-encounter-status.html)

```yaml
values:
  Planned:
    description: The encounter is planned but has not yet started
  Arrived:
    description: The patient has arrived and is waiting to be seen
  Triaged:
    description: The patient has been assessed for urgency and priority
  In Progress:
    description: The encounter is currently active and the patient is receiving care
  On Leave:
    description: The encounter has been paused (patient temporarily away from care setting)
  Finished:
    description: The encounter has ended normally after care completion
  Cancelled:
    description: The encounter was cancelled before it started
```

---

### Encounter Class

Classification of the type of patient encounter. Aligned to FHIR R4 ActEncounterCode value set.

Standard: [FHIR R4 ActEncounterCode](http://hl7.org/fhir/R4/v3/ActEncounterCode/vs.html)

```yaml
values:
  Inpatient:
    description: Patient is admitted to a hospital bed for overnight or multi-day stay
  Outpatient:
    description: Patient visits a clinic or facility without overnight admission
  Emergency:
    description: Patient presents to the emergency department
  Virtual:
    description: Remote consultation via telehealth platform
  Home Health:
    description: Care delivered at the patient's home
```

---

### Condition Clinical Status

Clinical status of a condition, problem, or diagnosis. Aligned to FHIR R4 ConditionClinicalStatusCodes value set.

Standard: [FHIR R4 ConditionClinicalStatus](http://hl7.org/fhir/R4/valueset-condition-clinical.html)

```yaml
values:
  Active:
    description: The condition is currently active and clinically relevant
  Recurrence:
    description: The condition has returned after a period of remission or resolution
  Relapse:
    description: The condition has worsened after a period of improvement
  Inactive:
    description: The condition is no longer clinically active but has not formally resolved
  Remission:
    description: The condition is in remission — symptoms have diminished or disappeared
  Resolved:
    description: The condition is considered resolved and no longer a clinical concern
```

---

### Observation Status

Status of an observation result. Aligned to FHIR R4 ObservationStatus value set.

Standard: [FHIR R4 ObservationStatus](http://hl7.org/fhir/R4/valueset-observation-status.html)

```yaml
values:
  Registered:
    description: Observation has been recorded but no result is yet available
  Preliminary:
    description: Initial result available but may be subject to change
  Final:
    description: Result is complete and verified — no further changes expected
  Amended:
    description: A subsequent update correcting a previously final result
  Cancelled:
    description: The observation was cancelled and should not be considered
  Entered In Error:
    description: The observation was entered in error and is withdrawn
```

---

### Medication Request Status

Lifecycle status of a medication request. Aligned to FHIR R4 MedicationRequestStatus value set.

Standard: [FHIR R4 MedicationRequestStatus](http://hl7.org/fhir/R4/valueset-medicationrequest-status.html)

```yaml
values:
  Active:
    description: The medication request is active and the medication should be administered
  On Hold:
    description: The medication request has been temporarily suspended
  Cancelled:
    description: The medication request has been cancelled
  Completed:
    description: All administrations of the medication have been completed
  Entered In Error:
    description: The medication request was entered in error and is withdrawn
  Stopped:
    description: The medication request was stopped — not taken as directed
  Draft:
    description: The medication request is not yet active and is being prepared
```

---

### Care Plan Status

Lifecycle status of a care plan. Aligned to FHIR R4 RequestStatus value set.

Standard: [FHIR R4 RequestStatus](http://hl7.org/fhir/R4/valueset-request-status.html)

```yaml
values:
  Draft:
    description: The care plan is in preparation and not yet active
  Active:
    description: The care plan is active and guiding current clinical decisions
  On Hold:
    description: The care plan has been temporarily suspended
  Revoked:
    description: The care plan has been withdrawn and is no longer in effect
  Completed:
    description: All planned activities have been completed
  Entered In Error:
    description: The care plan was entered in error and is withdrawn
```

---

### Appointment Status

Lifecycle status of a scheduled appointment. Aligned to FHIR R4 AppointmentStatus value set.

Standard: [FHIR R4 AppointmentStatus](http://hl7.org/fhir/R4/valueset-appointmentstatus.html)

```yaml
values:
  Proposed:
    description: Appointment has been proposed but not yet confirmed
  Pending:
    description: Appointment has been requested and is awaiting confirmation
  Booked:
    description: Appointment has been confirmed by all participants
  Arrived:
    description: Patient has arrived for the appointment
  Fulfilled:
    description: Appointment has been completed and resulted in an encounter
  Cancelled:
    description: Appointment has been cancelled before it occurred
  No Show:
    description: Patient did not arrive for the scheduled appointment
```

---

### Procedure Status

Lifecycle status of a clinical procedure. Aligned to FHIR R4 EventStatus value set.

Standard: [FHIR R4 EventStatus](http://hl7.org/fhir/R4/valueset-event-status.html)

```yaml
values:
  Preparation:
    description: Procedure is being prepared but has not started
  In Progress:
    description: Procedure is currently being performed
  Not Done:
    description: Procedure was not performed as planned
  On Hold:
    description: Procedure has been paused
  Stopped:
    description: Procedure was halted before completion
  Completed:
    description: Procedure has been completed successfully
  Entered In Error:
    description: Procedure record was entered in error and is withdrawn
```

---

### Administrative Gender

Administrative gender of a person. Aligned to FHIR R4 AdministrativeGender value set.

Standard: [FHIR R4 AdministrativeGender](http://hl7.org/fhir/R4/valueset-administrative-gender.html)

```yaml
values:
  Male:
    description: Male administrative gender
  Female:
    description: Female administrative gender
  Other:
    description: Administrative gender other than male or female
  Unknown:
    description: Administrative gender is not known
```

---

### LOINC Observation Code

Logical Observation Identifiers Names and Codes used for laboratory and clinical observations. This is a representative subset of commonly used codes — the full LOINC code system is the normative reference.

Standard: [LOINC](https://loinc.org/)

```yaml
values:
  8867-4:
    description: Heart rate (beats per minute)
  8310-5:
    description: Body temperature (degrees Celsius)
  8480-6:
    description: Systolic blood pressure (mmHg)
  8462-4:
    description: Diastolic blood pressure (mmHg)
  9279-1:
    description: Respiratory rate (breaths per minute)
  2708-6:
    description: Oxygen saturation (%)
  2345-7:
    description: Glucose (mg/dL)
  718-7:
    description: Hemoglobin (g/dL)
  4548-4:
    description: Hemoglobin A1c (%)
  2160-0:
    description: Creatinine (mg/dL)
```

---

### ICD-10 Condition Code

International Classification of Diseases, 10th Revision codes for conditions and diagnoses. This is a representative subset — the full ICD-10 code system is the normative reference.

Standard: [ICD-10](https://icd.who.int/browse10/)

```yaml
values:
  E11:
    description: Type 2 diabetes mellitus
  I10:
    description: Essential (primary) hypertension
  J18.9:
    description: Pneumonia, unspecified organism
  I21:
    description: Acute myocardial infarction
  J44.1:
    description: Chronic obstructive pulmonary disease with acute exacerbation
  K21.0:
    description: Gastro-oesophageal reflux disease with oesophagitis
  N18.3:
    description: Chronic kidney disease, stage 3
  F32.1:
    description: Major depressive disorder, single episode, moderate
  M54.5:
    description: Low back pain
  C34.9:
    description: Malignant neoplasm of unspecified part of bronchus or lung
```

---

### SNOMED CT Procedure Code

SNOMED Clinical Terms codes for clinical procedures. This is a representative subset — the full SNOMED CT code system is the normative reference.

Standard: [SNOMED CT](https://www.snomed.org/)

```yaml
values:
  80146002:
    description: Appendectomy
  27737000:
    description: Total hip replacement
  387713003:
    description: Surgical procedure (general)
  232717009:
    description: Coronary artery bypass graft
  18286008:
    description: Catheterization of urinary bladder
  174041007:
    description: Open cholecystectomy
  40701008:
    description: Echocardiography
  71388002:
    description: Colonoscopy
  76164006:
    description: Biopsy of skin
  312681000:
    description: Computerized tomography of chest
```
