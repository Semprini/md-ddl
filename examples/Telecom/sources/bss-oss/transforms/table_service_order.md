# [BSS/OSS Platform](../source.md)

## ServiceOrder

Service order records are emitted event-driven from the provisioning system. Each status change appends a new record — the source table is itself append-only.

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | ServiceOrderId | Text | 64 | | | no | System-assigned service order identifier | Service Order.Service Order Identifier
2 | SubscriptionId | Text | 64 | | | no | Identifies which Subscription triggered this Service Order | Subscription.Subscription Identifier
3 | OrderTypeCode | Text | 20 | | | no | Type of provisioning action requested | [Map Order Type](#map-order-type)
4 | StatusCode | Text | 20 | | | no | Current processing status of the service order | [Map Order Status](#map-order-status)
5 | RequestedDate | Date | | | | no | Date the service order was submitted | Service Order.Requested Date
6 | CompletionDate | Date | | | | yes | Date the order was completed (null if in progress) | Service Order.Completion Date
7 | FailureReason | Text | 500 | | | yes | Failure description when status is Failed | Service Order.Failure Reason

### Map Order Type

Maps BSS order type codes to canonical Service Order Type enum values.

```yaml
type: conditional
target: Service Order · Order Type
source:
  field: ServiceOrder.OrderTypeCode
cases:
  Provision: "OrderTypeCode == 'PROVISION'"
  Modify: "OrderTypeCode == 'MODIFY'"
  Suspend: "OrderTypeCode == 'SUSPEND'"
  Resume: "OrderTypeCode == 'RESUME'"
  Terminate: "OrderTypeCode == 'TERMINATE'"
fallback: Provision
```

### Map Order Status

Maps BSS service order status codes to canonical Service Order Status enum values.

```yaml
type: conditional
target: Service Order · Status
source:
  field: ServiceOrder.StatusCode
cases:
  Acknowledged: "StatusCode == 'ACK'"
  In Progress: "StatusCode == 'INPROG'"
  Completed: "StatusCode == 'COMPLETED'"
  Failed: "StatusCode == 'FAILED'"
  Cancelled: "StatusCode == 'CANCELLED'"
fallback: Acknowledged
```
