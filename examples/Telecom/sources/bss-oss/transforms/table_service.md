# [BSS/OSS Platform](../source.md)

## Service

Service records are emitted event-driven from the provisioning system when a service is created, modified, or terminated.

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | ServiceId | Text | 64 | | | no | System-assigned service identifier | Service.Service Identifier
2 | ServiceOrderId | Text | 64 | | | no | Identifies which Service Order provisioned this Service | Service Order.Service Order Identifier
3 | ServiceNumber | Text | 50 | | | yes | Subscriber-facing service identifier (MSISDN or circuit ID) | Service.Service Number
4 | ServiceType | Text | 50 | | | no | Service category (e.g. Mobile Voice, Fixed Broadband) | Service.Service Type
5 | StatusCode | Text | 20 | | | no | Service operational status code | [Map Service Status](#map-service-status)
6 | ActivationDate | Date | | | | yes | Date the service was activated on the network | Service.Activation Date
7 | DeactivationDate | Date | | | | yes | Date the service was deactivated (null if active) | Service.Deactivation Date

### Map Service Status

Maps BSS service status codes to canonical Service Status enum values.

```yaml
type: conditional
target: Service · Status
source:
  field: Service.StatusCode
cases:
  Pending: "StatusCode == 'PENDING'"
  Active: "StatusCode == 'ACTIVE'"
  Suspended: "StatusCode == 'SUSPENDED'"
  Terminated: "StatusCode == 'TERMINATED'"
fallback: Active
```
