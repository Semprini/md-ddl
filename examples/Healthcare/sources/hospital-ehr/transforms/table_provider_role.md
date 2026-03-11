# [Hospital EHR](../source.md)

## ProviderRole

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | ProviderRoleId | Text | 64 | | | no | System-assigned provider role identifier | Practitioner Role.Practitioner Role Identifier
2 | ProviderId | Text | 64 | | | no | Reference to provider (practitioner) record | Practitioner Role.Practitioner Identifier
3 | OrgId | Text | 64 | | | yes | Organisation where this role is held | Practitioner Role.Organization Identifier
4 | Specialty | Text | 100 | | | yes | Clinical specialty for this role | Practitioner Role.Specialty
5 | IsActive | Boolean | | | | no | Whether this role is currently active | Practitioner Role.Active
6 | RoleStartDate | Date | | | | yes | Date this role became effective | Practitioner Role.Role Period Start
7 | RoleEndDate | Date | | | | yes | Date this role ceased (null if still active) | Practitioner Role.Role Period End
