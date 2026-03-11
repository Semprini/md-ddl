# [BSS/OSS Platform](../source.md)

## ProductCatalog

Product catalog records are loaded via batch from the product management system. Each row represents a versioned product offering.

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | OfferingId | Text | 64 | | | no | System-assigned product offering identifier | Product Offering.Product Offering Identifier
2 | OfferingName | Text | 255 | | | no | Commercial name of the offering | Product Offering.Name
3 | Description | Text | 2000 | | | yes | Full offering description | Product Offering.Description
4 | OfferingTypeCode | Text | 20 | | | no | Commercial classification code | [Map Offering Type](#map-offering-type)
5 | MonthlyCharge | Decimal | | 10 | 2 | no | Recurring monthly charge | Product Offering.Monthly Charge
6 | CurrencyCode | Text | 3 | | | no | ISO 4217 currency code | Product Offering.Currency Code
7 | DataAllowanceGB | Decimal | | 10 | 3 | yes | Included data allowance in GB (null = unlimited) | Product Offering.Data Allowance GB
8 | VoiceAllowanceMins | Integer | | | | yes | Included voice minutes (null = unlimited) | Product Offering.Voice Allowance Minutes
9 | SMSAllowance | Integer | | | | yes | Included SMS count (null = unlimited) | Product Offering.SMS Allowance
10 | CommitmentMonths | Integer | | | | no | Minimum contract period in months | Product Offering.Commitment Period Months
11 | ValidFromDate | Date | | | | no | Catalog availability start date | Product Offering.Valid From Date
12 | ValidToDate | Date | | | | yes | Catalog availability end date (null = active) | Product Offering.Valid To Date

### Map Offering Type

Maps BSS offering type codes to canonical Product Offering Type enum values.

```yaml
type: conditional
target: Product Offering · Offering Type
source:
  field: ProductCatalog.OfferingTypeCode
cases:
  Prepaid: "OfferingTypeCode == 'PREPAID'"
  Postpaid: "OfferingTypeCode == 'POSTPAID'"
  Hybrid: "OfferingTypeCode == 'HYBRID'"
  Business: "OfferingTypeCode == 'BUSINESS'"
  Wholesale: "OfferingTypeCode == 'WHOLESALE'"
fallback: Postpaid
```
