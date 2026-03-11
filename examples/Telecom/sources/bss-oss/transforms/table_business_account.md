# [BSS/OSS Platform](../source.md)

## BusinessAccount

Business account records represent corporate and SME subscribers. Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | BusinessAccountId | Text | 64 | | | no | System-assigned business account identifier | Party.Party Identifier
2 | LegalName | Text | 255 | | | no | Registered legal name of the organisation | Organization.Legal Name
3 | TradingName | Text | 255 | | | yes | Trading or brand name if different from legal name | Organization.Trading Name
4 | RegistrationNo | Text | 50 | | | yes | Company registration number | Organization.Registration Number
5 | IndustrySectorCode | Text | 20 | | | yes | Industry classification code (ANZSIC or SIC) | Organization.Industry Sector Code
6 | VATNo | Text | 30 | | | yes | VAT or GST registration number | Organization.VAT Number
7 | PartyTypeCode | Text | 20 | | | no | Discriminator: always 'ORG' for business accounts | [Map Party Type](#map-party-type)

### Map Party Type

Maps the BSS party type discriminator to the canonical Party Type value.

```yaml
type: conditional
target: Party · Party Type
source:
  field: BusinessAccount.PartyTypeCode
cases:
  Organization: "PartyTypeCode == 'ORG'"
fallback: Organization
```
