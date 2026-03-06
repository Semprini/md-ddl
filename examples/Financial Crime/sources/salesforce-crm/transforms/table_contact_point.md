# [Salesforce CRM](../source.md)

## ContactPoint

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | PurposeCode | Text | 40 | | | yes | Purpose classification for contact point | Contact Address.Address Purpose
2 | VerificationResult | Text | 20 | | | yes | Verification workflow result | [Map Verification Status](#map-verification-status)
3 | ValidFromDate | Date | | | | yes | Effective-from date | [Derive Effective Dates](#derive-effective-dates)
4 | ValidToDate | Date | | | | yes | Effective-to date | [Derive Effective Dates](#derive-effective-dates)

### Map Verification Status

Maps verification outcome from CRM verification workflow.

```yaml
type: conditional
target: Contact Address · Verification Status
source:
  field: ContactPoint.VerificationResult
cases:
  Verified: "VerificationResult == 'PASS'"
  Pending: "VerificationResult == 'PENDING'"
  Failed: "VerificationResult == 'FAIL'"
fallback: Pending
```

### Derive Effective Dates

Builds effective date range token from valid-from and valid-to values.

```yaml
type: derived
target: Contact Address · Effective Dates
expression: "coalesce(Valid From, '') + '|' + coalesce(Valid To, '')"
inputs:
  Valid From:
    field: ContactPoint.ValidFromDate
  Valid To:
    field: ContactPoint.ValidToDate
```
