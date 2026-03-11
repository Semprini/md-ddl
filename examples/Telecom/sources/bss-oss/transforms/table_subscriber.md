# [BSS/OSS Platform](../source.md)

## Subscriber

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | SubscriberId | Text | 64 | | | no | System-assigned subscriber identifier | Party.Party Identifier
2 | FirstName | Text | 100 | | | no | Subscriber's given name | Individual.Given Name
3 | LastName | Text | 100 | | | no | Subscriber's family name | Individual.Family Name
4 | DOB | Date | | | | yes | Date of birth | Individual.Date of Birth
5 | EmailAddr | Text | 255 | | | yes | Primary email address | Individual.Email Address
6 | MobileNo | Text | 20 | | | yes | Mobile number in E.164 format | Individual.Mobile Number
7 | IdDocType | Text | 50 | | | yes | Identity document type | Individual.Identity Document Type
8 | IdDocNo | Text | 50 | | | yes | Identity document number | Individual.Identity Document Number
9 | PartyTypeCode | Text | 20 | | | no | Discriminator: always 'IND' for individual subscribers | [Map Party Type](#map-party-type)

### Map Party Type

Maps the BSS party type discriminator to the canonical Party Type value.

```yaml
type: conditional
target: Party · Party Type
source:
  field: Subscriber.PartyTypeCode
cases:
  Individual: "PartyTypeCode == 'IND'"
fallback: Individual
```
