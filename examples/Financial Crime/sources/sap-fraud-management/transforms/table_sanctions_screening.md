# [Financial Crime](../../../domain.md)

## Sources

### [SAP Fraud Management](../source.md#sap-fraud-management)

#### SanctionsScreening

The latest sanctions screening result for a party.

##### Entity Fan-Out

```yaml
produces:
  - entity: Party
    cardinality: 1
    contributes: true
    identity:
      field: SanctionsScreening.PartyExternalId
      maps_to: Party · Party Identifier
```

Screening updates an existing Party that Salesforce CRM has already established as a Person or a Company. The entry is `contributes: true`, so it names the abstract Party and never creates one. A screening row for an unknown party is held until the CRM establishes it.

##### Source Schema

A blank Destination means the column is deliberately not mapped.

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Description | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | PartyExternalId | Text | 40 | | | no | Enterprise party identifier | Party.Party Identifier
2 | ResultCode | Text | 32 | | | yes | Screening engine outcome code | [Transform: Map Sanctions Screen Status](#transform-map-sanctions-screen-status)
3 | MatchFlag | Boolean | | | | yes | Whether a watchlist match was detected | 

`MatchFlag` is deliberately unmapped: it's derivable from `ResultCode` and would duplicate Sanctions Screen Status.

##### Transform: Map Sanctions Screen Status

Unrecognised result codes fall back to Potential Match so that they're investigated. A new engine code must never silently clear a party.

```yaml
type: conditional
target: Party · Sanctions Screen Status
evaluation: exclusive
source:
  field: SanctionsScreening.ResultCode
cases:
  Clear: "ResultCode == 'CLEAR'"
  Potential Match: "ResultCode == 'POTENTIAL_MATCH'"
  Confirmed Match: "ResultCode == 'CONFIRMED_MATCH'"
  False Positive: "ResultCode == 'FALSE_POSITIVE'"
fallback: Potential Match
```

##### Worked Examples

```yaml
example: Confirmed match
given:
  PartyExternalId: "P-1003"
  ResultCode: "CONFIRMED_MATCH"
  MatchFlag: true
produces:
  - entity: Party
    Party Identifier: "P-1003"
    Sanctions Screen Status: Confirmed Match
```

```yaml
example: Unknown engine code is investigated, not cleared
given:
  PartyExternalId: "P-1002"
  ResultCode: "REVIEW_REQUIRED"
produces:
  - entity: Party
    Party Identifier: "P-1002"
    Sanctions Screen Status: Potential Match
```
