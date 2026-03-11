# [BSS/OSS Platform](../source.md)

## Customer

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | CustomerId | Text | 64 | | | no | System-assigned customer identifier | Customer.Customer Identifier
2 | SubscriberId | Text | 64 | | | no | Identifies which Party this Customer belongs to | Party.Party Identifier
3 | StatusCode | Text | 20 | | | no | Customer lifecycle status code | [Map Customer Status](#map-customer-status)
4 | CustomerSinceDate | Date | | | | yes | Date the customer relationship was established | Customer.Customer Since Date
5 | Segment | Text | 50 | | | yes | Commercial segment (Consumer, SME, Enterprise, Wholesale) | Customer.Segment
6 | AccountManagerId | Text | 64 | | | yes | Identifier of assigned account manager | Customer.Account Manager

### Map Customer Status

Maps BSS status codes to canonical Customer Status enum values.

```yaml
type: conditional
target: Customer · Status
source:
  field: Customer.StatusCode
cases:
  Prospect: "StatusCode == 'PROSPECT'"
  Active: "StatusCode == 'ACTIVE'"
  Suspended: "StatusCode == 'SUSPENDED'"
  Closed: "StatusCode == 'CLOSED'"
fallback: Active
```
