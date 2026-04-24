# [Healthcare](../domain.md)

## Entities

### Procedure

An action that is or was performed on or for a patient. Aligned to the FHIR R4 Procedure resource, this entity captures surgical operations, diagnostic procedures, therapeutic interventions, and other clinical actions. Procedures are coded using SNOMED CT for international clinical terminology interoperability.

Procedures are event-driven with a clear actor model — every procedure is performed by one or more practitioners in specific roles.

```mermaid
---
config:
  layout: elk
---
classDiagram
  class Procedure{
    * Procedure Identifier : string
    Status : enum~ProcedureStatus~
    Code : enum~SNOMEDCTProcedureCode~
    Performed Date Time : datetime
    Outcome : string
  }

  Encounter "1" --> "0..*" Procedure : has

  class ProcedureStatus["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Healthcare/enums.md#procedure-status'>Procedure Status</a>"]{<<enumeration>>}
  class SNOMEDCTProcedureCode["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Healthcare/enums.md#snomed-ct-procedure-code'>SNOMED CT Procedure Code</a>"]{<<enumeration>>}

  class Encounter["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Healthcare/entities/encounter.md'>Encounter</a>"]
```

```yaml
existence: dependent
mutability: append_only
temporal:
  tracking: transaction_time
  description: >
    Transaction time tracks when the procedure record was entered into the
    system. Procedure records are append-only — once documented, corrections
    are issued as amendments rather than overwrites.
attributes:
  Procedure Identifier:
    type: string
    identifier: primary
    description: Unique identifier for this procedure record.

  Status:
    type: enum:Procedure Status
    description: Lifecycle status of the procedure (preparation, in-progress, completed, etc.).

  Code:
    type: enum:SNOMED CT Procedure Code
    description: >
      SNOMED CT code identifying the procedure performed. Uses SNOMED Clinical
      Terms for precise clinical procedure classification.

  Performed Date Time:
    type: datetime
    description: Date and time the procedure was performed.

  Outcome:
    type: string
    description: Outcome of the procedure (e.g. successful, complications noted).
```

```yaml
governance:
  pii: true
  classification: Highly Confidential
  retention_basis: Inherited from domain default retention of 7 years post last encounter
```
