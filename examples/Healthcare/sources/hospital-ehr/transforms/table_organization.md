# [Hospital EHR](../source.md)

## Organization

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | OrgId | Text | 64 | | | no | System-assigned organisation identifier | Organization.Organization Identifier
2 | OrgName | Text | 255 | | | no | Full organisation name | Organization.Name
3 | OrgTypeCode | Text | 20 | | | yes | Organisation type code | [Map Org Type](#map-org-type)
4 | IsActive | Boolean | | | | no | Whether organisation record is active | Organization.Active

### Map Org Type

Maps EHR organisation type codes to canonical Organisation Type values.

```yaml
type: conditional
target: Organization · Type
source:
  field: Organization.OrgTypeCode
cases:
  Hospital: "OrgTypeCode == 'HOSP'"
  Department: "OrgTypeCode == 'DEPT'"
  Clinic: "OrgTypeCode == 'CLIN'"
  Laboratory: "OrgTypeCode == 'LAB'"
  Pharmacy: "OrgTypeCode == 'PHARM'"
fallback: Department
```
