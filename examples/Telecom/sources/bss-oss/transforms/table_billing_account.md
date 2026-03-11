# [BSS/OSS Platform](../source.md)

## BillingAccount

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | BillingAcctId | Text | 64 | | | no | System-assigned billing account identifier | Billing Account.Billing Account Identifier
2 | CustomerId | Text | 64 | | | no | Identifies which Customer this Billing Account belongs to | Customer.Customer Identifier
3 | StatusCode | Text | 20 | | | no | Billing account status code | [Map Billing Account Status](#map-billing-account-status)
4 | CreditLimit | Decimal | | 12 | 2 | no | Maximum outstanding balance permitted | Billing Account.Credit Limit
5 | OutstandingBalance | Decimal | | 12 | 2 | no | Current amount owed | Billing Account.Outstanding Balance
6 | CurrencyCode | Text | 3 | | | no | ISO 4217 currency code | Billing Account.Currency Code
7 | PaymentMethodCode | Text | 20 | | | yes | Payment method type code | Billing Account.Payment Method Code
8 | PaymentToken | Text | 255 | | | yes | Tokenized payment method reference | Billing Account.Payment Method Token
9 | BillingCycleDay | Integer | | | | no | Day of month for invoice generation | Billing Account.Billing Cycle Day

### Map Billing Account Status

Maps BSS billing account status codes to canonical Billing Account Status enum values.

```yaml
type: conditional
target: Billing Account · Status
source:
  field: BillingAccount.StatusCode
cases:
  Active: "StatusCode == 'ACTIVE'"
  Suspended: "StatusCode == 'SUSPENDED'"
  Closed: "StatusCode == 'CLOSED'"
  Overdue: "StatusCode == 'OVERDUE'"
fallback: Active
```
