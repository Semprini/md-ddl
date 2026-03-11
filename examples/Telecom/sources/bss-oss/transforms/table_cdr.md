# [BSS/OSS Platform](../source.md)

## CDR

Call Detail Records (CDRs) are emitted by the mediation layer after validation and enrichment. Each row represents one completed call, SMS, or data session.

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | CdrId | Text | 64 | | | no | Unique CDR identifier assigned by mediation | Usage Record.Usage Record Identifier
2 | ServiceId | Text | 64 | | | no | Identifies which Service generated this CDR | Service.Service Identifier
3 | UsageTypeCode | Text | 20 | | | no | Usage category code from the network element | [Map Usage Type](#map-usage-type)
4 | Volume | Decimal | | 18 | 6 | yes | Quantity consumed (null for SMS/MMS where count is 1) | Usage Record.Volume
5 | VolumeUnit | Text | 20 | | | yes | Unit of volume measurement | Usage Record.Volume Unit
6 | DurationSecs | Integer | | | | yes | Call or session duration in seconds | Usage Record.Duration Seconds
7 | SessionStartUtc | DateTime | | | | no | UTC start timestamp of the call or session | Usage Record.Session Start
8 | SessionEndUtc | DateTime | | | | no | UTC end timestamp of the call or session | Usage Record.Session End
9 | DestinationNo | Text | 20 | | | yes | E.164 destination number (null for data sessions) | Usage Record.Destination Number
10 | RoamingFlag | Boolean | | | | no | True if the CDR originated from a roaming partner | Usage Record.Roaming Indicator
11 | RatedAmount | Decimal | | 10 | 4 | no | Charge applied after rating and allowance deduction | Usage Record.Rated Amount
12 | CurrencyCode | Text | 3 | | | no | ISO 4217 currency code for the rated amount | Usage Record.Currency Code

### Map Usage Type

Maps mediation usage type codes to canonical Usage Type enum values.

```yaml
type: conditional
target: Usage Record · Usage Type
source:
  field: CDR.UsageTypeCode
cases:
  Voice: "UsageTypeCode == 'VOICE'"
  SMS: "UsageTypeCode == 'SMS'"
  Data: "UsageTypeCode == 'DATA'"
  MMS: "UsageTypeCode == 'MMS'"
  Roaming Voice: "UsageTypeCode == 'ROAM_VOICE'"
  Roaming Data: "UsageTypeCode == 'ROAM_DATA'"
fallback: Data
```
