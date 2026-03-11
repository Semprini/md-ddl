# [BSS/OSS Platform](../source.md)

## Subscription

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | SubscriptionId | Text | 64 | | | no | System-assigned subscription identifier | Subscription.Subscription Identifier
2 | CustomerId | Text | 64 | | | no | Identifies which Customer holds this Subscription | Customer.Customer Identifier
3 | OfferingId | Text | 64 | | | no | Identifies which Product Offering this Subscription activates | Product Offering.Product Offering Identifier
4 | StatusCode | Text | 20 | | | no | Subscription lifecycle status code | [Map Subscription Status](#map-subscription-status)
5 | AgreedMonthlyCharge | Decimal | | 10 | 2 | no | Monthly recurring charge agreed at point of sale | Subscription.Agreed Monthly Charge
6 | StartDate | Date | | | | no | Date the subscription became active | Subscription.Start Date
7 | CommitmentEndDate | Date | | | | yes | Commitment end date (null for month-to-month) | Subscription.Commitment End Date
8 | AutoRenew | Boolean | | | | no | Whether the subscription auto-renews at term end | Subscription.Auto Renew

### Map Subscription Status

Maps BSS subscription status codes to canonical Subscription Status enum values.

```yaml
type: conditional
target: Subscription · Status
source:
  field: Subscription.StatusCode
cases:
  Pending: "StatusCode == 'PENDING'"
  Active: "StatusCode == 'ACTIVE'"
  Suspended: "StatusCode == 'SUSPENDED'"
  Cancelled: "StatusCode == 'CANCELLED'"
  Expired: "StatusCode == 'EXPIRED'"
fallback: Active
```
