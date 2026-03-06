# [SAP Fraud Management](../source.md)

## AlertCase

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | TxRiskScore | Decimal | | 18 | 6 | yes | Computed transaction ML/TF risk score | Transaction.Financial Crime Risk Score
2 | DecisionStatus | Text | 30 | | | yes | Alert workflow decision status | [Map Monitoring Outcome](#map-monitoring-outcome)
3 | CaseId | Text | 64 | | | no | Unique SAP alert case identifier | Transaction.Alert Reference

### Map Monitoring Outcome

Maps alert decision outcome into canonical monitoring outcome.

```yaml
type: conditional
target: Transaction · Monitoring Outcome
source:
  field: AlertCase.DecisionStatus
cases:
  Escalated: "DecisionStatus == 'ESCALATED'"
  Cleared: "DecisionStatus == 'CLEARED'"
  Under Review: "DecisionStatus == 'OPEN'"
fallback: Under Review
```

### Map Alert Reference

Maps SAP alert case identifier for downstream investigations.

```yaml
type: direct
target: Transaction · Alert Reference
source:
  field: AlertCase.CaseId
  cast: string
```
