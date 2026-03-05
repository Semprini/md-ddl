# [Salesforce CRM](./source.md)

## Contact

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | FirstName | Text | 120 | | | yes | Contact given name | Person.Given Name
2 | LastName | Text | 120 | | | yes | Contact family name | Person.Family Name
3 | Birthdate | Date | | | | yes | Contact date of birth | Person.Date of Birth
4 | CompliancePepFlag | Text | 1 | | | yes | PEP indicator from compliance screening | [Derive PEP Status](#derive-pep-status)

### Derive PEP Status

Derives politically exposed person status from CRM compliance flag.

```yaml
type: conditional
target: Person · PEP Status
source:
  field: Contact.CompliancePepFlag
cases:
  Confirmed: "CompliancePepFlag == 'Y'"
  Not PEP: "CompliancePepFlag == 'N'"
  Unknown: "CompliancePepFlag == null"
fallback: Unknown
```
