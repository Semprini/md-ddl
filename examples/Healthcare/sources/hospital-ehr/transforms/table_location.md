# [Hospital EHR](../source.md)

## Location

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | LocationId | Text | 64 | | | no | System-assigned location identifier | Location.Location Identifier
2 | LocationName | Text | 255 | | | no | Descriptive name of the location | Location.Name
3 | LocationTypeCode | Text | 20 | | | yes | Physical type of location | [Map Location Type](#map-location-type)
4 | StatusCode | Text | 20 | | | no | Operational status of the location | [Map Location Status](#map-location-status)

### Map Location Type

Maps EHR location type codes to canonical Location Type values.

```yaml
type: conditional
target: Location · Type
source:
  field: Location.LocationTypeCode
cases:
  Ward: "LocationTypeCode == 'WARD'"
  Bed: "LocationTypeCode == 'BED'"
  Clinic: "LocationTypeCode == 'CLINIC'"
  Theatre: "LocationTypeCode == 'THEATRE'"
  ICU: "LocationTypeCode == 'ICU'"
fallback: Ward
```

### Map Location Status

Maps EHR status codes to canonical Location Status values.

```yaml
type: conditional
target: Location · Status
source:
  field: Location.StatusCode
cases:
  Active: "StatusCode == 'ACTIVE'"
  Suspended: "StatusCode == 'SUSPENDED'"
  Inactive: "StatusCode == 'INACTIVE'"
fallback: Active
```
