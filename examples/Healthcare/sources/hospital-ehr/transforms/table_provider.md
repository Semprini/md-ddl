# [Hospital EHR](../source.md)

## Provider

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | ProviderId | Text | 64 | | | no | System-assigned provider identifier | Practitioner.Practitioner Identifier
2 | NPI | Text | 10 | | | yes | National Provider Identifier (10-digit) | Practitioner.NPI
3 | FirstName | Text | 100 | | | no | Provider given name | Practitioner.Given Name
4 | LastName | Text | 100 | | | no | Provider family name | Practitioner.Family Name
5 | IsActive | Boolean | | | | no | Whether provider record is active | Practitioner.Active
