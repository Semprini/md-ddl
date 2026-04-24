# [Healthcare](../domain.md)

## Data Products

### Clinical Patient Record

The governed canonical representation of Patient, Encounter, Condition,
and related clinical entities for consumption by downstream domains and
cross-facility integration points. This product provides the standardized
clinical data model for any system that needs the full-fidelity patient
care record.

```yaml
class: domain-aligned
schema_type: normalized
owner: clinical.data@hospital.org
consumers:
  - Cross-facility Integration
  - Health Information Exchange
  - Regulatory Reporting
status: Active
version: "1.0.0"

entities:
  - Patient
  - Encounter
  - Observation
  - Condition
  - Procedure
  - Medication Request
  - Care Plan
  - Practitioner
  - Practitioner Role

lineage:
  - source: hospital-ehr
    tables:
      - table_patient_demographics
      - table_encounter
      - table_diagnosis
      - table_medication_order
      - table_care_plan
      - table_provider
      - table_provider_role
  - source: lab-information-system
    tables:
      - table_lab_result
      - table_lab_procedure

sla:
  freshness: "< 30 minutes"
  availability: "99.95%"

refresh: real-time
```

#### Logical Model

```mermaid
---
config:
  layout: elk
---
classDiagram
  class Patient{
    * Patient Identifier : string
    Medical Record Number : string
    Given Name : string
    Family Name : string
    Date of Birth : date
    Administrative Gender : enum~AdministrativeGender~
    Deceased : boolean
    Active : boolean
  }

  class Encounter{
    * Encounter Identifier : string
    Status : enum~EncounterStatus~
    Class : enum~EncounterClass~
    Admission Date Time : datetime
    Discharge Date Time : datetime
    Reason : string
    Length Of Stay : integer
  }

  class Observation{
    * Observation Identifier : string
    Status : enum~ObservationStatus~
    Code : enum~LOINCObservationCode~
    Effective Date Time : datetime
    Issued Date Time : datetime
    Value Quantity : decimal
    Value Unit : string
    Value Text : string
    Interpretation : string
  }

  class Condition{
    * Condition Identifier : string
    Clinical Status : enum~ConditionClinicalStatus~
    Code : enum~ICD10ConditionCode~
    Onset Date Time : datetime
    Abatement Date Time : datetime
    Recorded Date : datetime
    Severity : string
  }

  class Procedure{
    * Procedure Identifier : string
    Status : enum~ProcedureStatus~
    Code : enum~SNOMEDCTProcedureCode~
    Performed Date Time : datetime
    Outcome : string
  }

  class MedicationRequest{
    * Medication Request Identifier : string
    Status : enum~MedicationRequestStatus~
    Intent : string
    Medication Name : string
    Dosage Instructions : string
    Authored On : datetime
    Priority : string
  }

  class CarePlan{
    * Care Plan Identifier : string
    Status : enum~CarePlanStatus~
    Intent : string
    Title : string
    Description : string
    Period Start : date
    Period End : date
    Created : datetime
  }

  class Practitioner{
    * Practitioner Identifier : string
    National Provider Identifier : string
    Given Name : string
    Family Name : string
    Gender : enum~AdministrativeGender~
    Active : boolean
  }

  class PractitionerRole{
    * Practitioner Role Identifier : string
    Specialty : string
    Active : boolean
    Role Start Date : date
    Role End Date : date
  }

  Patient "1" --> "0..*" Encounter : has
  Patient "1" --> "0..*" Condition : has
  Patient "1" --> "0..*" CarePlan : has
  Encounter "1" --> "0..*" Observation : has
  Encounter "1" --> "0..*" Procedure : has
  Encounter "1" --> "0..*" MedicationRequest : has
  CarePlan "0..*" --> "0..*" Condition : addresses
  CarePlan "0..*" --> "0..*" MedicationRequest : includes
  Practitioner "1" --> "0..*" PractitionerRole : assumes
  PractitionerRole "0..*" --> "0..*" Encounter : provides

  class Patient["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Healthcare/entities/patient.md'>Patient</a>"]
  class Encounter["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Healthcare/entities/encounter.md'>Encounter</a>"]
  class Observation["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Healthcare/entities/observation.md'>Observation</a>"]
  class Condition["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Healthcare/entities/condition.md'>Condition</a>"]
  class Procedure["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Healthcare/entities/procedure.md'>Procedure</a>"]
  class MedicationRequest["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Healthcare/entities/medication_request.md'>Medication Request</a>"]
  class CarePlan["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Healthcare/entities/care_plan.md'>Care Plan</a>"]
  class Practitioner["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Healthcare/entities/practitioner.md'>Practitioner</a>"]
  class PractitionerRole["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Healthcare/entities/practitioner_role.md'>Practitioner Role</a>"]
```
