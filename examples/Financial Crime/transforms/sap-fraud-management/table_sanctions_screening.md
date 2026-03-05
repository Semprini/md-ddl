# [SAP Fraud Management](./source.md)

## SanctionsScreening

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | ResultCode | Text | 32 | | | yes | Screening engine outcome code | [Map Sanctions Screen Status](#map-sanctions-screen-status)
2 | MatchFlag | Boolean | | | | yes | Whether a watchlist match was detected | Party.Watchlist Match Indicator

### Map Sanctions Screen Status

Maps sanctions screening outcome from SAP sanctions service.

```yaml
type: conditional
target: Party · Sanctions Screen Status
source:
  field: SanctionsScreening.ResultCode
cases:
  Clear: "ResultCode == 'CLEAR'"
  Potential Match: "ResultCode == 'POTENTIAL_MATCH'"
  Confirmed Match: "ResultCode == 'CONFIRMED_MATCH'"
fallback: Clear
```
