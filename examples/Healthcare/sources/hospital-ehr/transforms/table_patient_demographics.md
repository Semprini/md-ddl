# [Hospital EHR](../source.md)

## PatientDemographics

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | PatientId | Text | 64 | | | no | System-assigned patient identifier | Patient.Patient Identifier
2 | MRN | Text | 20 | | | yes | Facility-assigned medical record number | Patient.Medical Record Number
3 | FirstName | Text | 100 | | | no | Patient given name | Patient.Given Name
4 | LastName | Text | 100 | | | no | Patient family name | Patient.Family Name
5 | DateOfBirth | Date | | | | yes | Patient date of birth | Patient.Date of Birth
6 | GenderCode | Text | 10 | | | yes | Administrative gender code from EHR | [Map Gender Code](#map-gender-code)
7 | IsDeceased | Boolean | | | | no | Whether patient is deceased | Patient.Deceased
8 | IsActive | Boolean | | | | no | Whether record is active | Patient.Active

### Map Gender Code

Maps EHR gender codes to canonical Administrative Gender enum values.

```yaml
type: conditional
target: Patient · Administrative Gender
source:
  field: PatientDemographics.GenderCode
cases:
  Male: "GenderCode == 'M'"
  Female: "GenderCode == 'F'"
  Other: "GenderCode == 'O'"
fallback: Unknown
```
