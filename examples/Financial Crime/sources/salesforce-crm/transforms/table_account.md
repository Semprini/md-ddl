# [Salesforce CRM](../source.md)

## Account

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | ExternalPartyId | Text | 40 | | | no | Account-scoped party identifier | Party.Party Identifier
2 | RecordStatus | Text | 20 | | | yes | Account lifecycle status from CRM | [Map Party Status](#map-party-status)
3 | LegalEntityName | Text | 200 | | | yes | Registered legal entity name | Company.Legal Name
4 | CompanyRegistrationNumber | Text | 80 | | | yes | Jurisdictional registration number | Company.Registration Identifier
5 | CustomerNumber | Text | 100 | | | yes | CRM customer reference | Customer.Customer Number
6 | OnboardingCompletedDate | Date | | | | yes | Date onboarding completed | Customer.Onboarding Date
7 | CustomerSegmentCode | Text | 30 | | | yes | Commercial segment classification code | Customer.Segment

### Map Party Status

Translates CRM lifecycle status values into canonical party status.

```yaml
type: conditional
target: Party · Party Status
source:
  field: Account.RecordStatus
cases:
  Active: "RecordStatus == 'Active'"
  Inactive: "RecordStatus == 'Inactive'"
  Suspended: "RecordStatus == 'Suspended'"
  Closed: "RecordStatus == 'Closed'"
fallback: Inactive
```
