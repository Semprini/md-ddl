# [SAP Fraud Management](../source.md)

## CustomerRiskProfile

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | ReviewRequiredFlag | Boolean | | | | yes | Indicates whether formal review is required | Customer.Risk Review Flag
2 | EddTriggerCode | Text | 20 | | | yes | Enhanced due diligence trigger status code | [Map Enhanced Due Diligence Trigger](#map-enhanced-due-diligence-trigger)

### Map Enhanced Due Diligence Trigger

Derives EDD trigger based on high-risk profile and unresolved alerts.

```yaml
type: conditional
target: Customer · Enhanced Due Diligence Trigger
source:
  field: CustomerRiskProfile.EddTriggerCode
cases:
  Triggered: "EddTriggerCode == 'TRIGGERED'"
  Not Triggered: "EddTriggerCode == 'NOT_TRIGGERED'"
  Pending: "EddTriggerCode == 'PENDING'"
fallback: Pending
```
