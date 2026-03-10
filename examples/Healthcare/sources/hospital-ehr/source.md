# Hospital EHR

Hospital EHR is the primary electronic health record system for patient demographics, encounter management, clinical documentation, and care planning. It serves as the system of record for all inpatient and outpatient clinical activities.

## Metadata

```yaml
id: hospital-ehr
owner: health.it@hospital.org
steward: clinical.informatics@hospital.org

change_model: real-time-cdc
change_events:
  - Patient Registered
  - Patient Updated
  - Encounter Created
  - Encounter Updated
  - Encounter Discharged
  - Condition Recorded
  - Medication Ordered
  - Care Plan Created
  - Care Plan Updated
  - Appointment Scheduled
  - Appointment Updated

update_frequency: real-time
data_quality_tier: 1
status: Production
version: "1.0.0"

tags:
  - Clinical
  - EHR
  - Patient Care
```

## [Healthcare](../../domain.md) Feeds

Canonical Entity | Transform File | Attributes Contributed | Change Model
--- | --- | --- | ---
[Patient](../../entities/patient.md#patient) | [table_patient_demographics](transforms/table_patient_demographics.md) | Patient Identifier, MRN, Given Name, Family Name, Date of Birth, Gender, Active | real-time-cdc
[Encounter](../../entities/encounter.md#encounter) | [table_encounter](transforms/table_encounter.md) | Encounter Identifier, Status, Class, Admission Date Time, Discharge Date Time, Reason | real-time-cdc
[Condition](../../entities/condition.md#condition) | [table_diagnosis](transforms/table_diagnosis.md) | Condition Identifier, Clinical Status, ICD-10 Code, Onset, Severity | real-time-cdc
[Medication Request](../../entities/medication_request.md#medication-request) | [table_medication_order](transforms/table_medication_order.md) | Medication Request Identifier, Status, Medication Name, Dosage, Authored On | real-time-cdc
[Care Plan](../../entities/care_plan.md#care-plan) | [table_care_plan](transforms/table_care_plan.md) | Care Plan Identifier, Status, Title, Period Start, Period End | real-time-cdc
[Appointment](../../entities/appointment.md#appointment) | [table_appointment](transforms/table_appointment.md) | Appointment Identifier, Status, Scheduled Start, Scheduled End, Service Type | real-time-cdc
[Practitioner](../../entities/practitioner.md#practitioner) | [table_provider](transforms/table_provider.md) | Practitioner Identifier, NPI, Given Name, Family Name, Active | batch
[Practitioner Role](../../entities/practitioner_role.md#practitioner-role) | [table_provider_role](transforms/table_provider_role.md) | Practitioner Role Identifier, Specialty, Active, Role Period | batch
[Organization](../../entities/organization.md#organization) | [table_organization](transforms/table_organization.md) | Organization Identifier, Name, Type, Active | batch
[Location](../../entities/location.md#location) | [table_location](transforms/table_location.md) | Location Identifier, Name, Type, Status | batch
