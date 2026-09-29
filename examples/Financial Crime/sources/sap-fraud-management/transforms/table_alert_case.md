# [Financial Crime](../../../domain.md)

## Sources

### [SAP Fraud Management](../source.md#sap-fraud-management)

#### AlertCase

One AlertCase row is a transaction monitoring alert and its current disposition.

##### Entity Fan-Out

```yaml
produces:
  - entity: Transaction Alert
    cardinality: 1
    identity:
      field: AlertCase.CaseId
      maps_to: Transaction Alert · Alert Reference
    references:
      Transaction: AlertCase.PaymentId
```

##### Source Schema

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Description | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | CaseId | Text | 64 | | | no | Unique SAP alert case identifier | Transaction Alert.Alert Reference
2 | PaymentId | Text | 64 | | | no | Payment identifier of the alerted transaction | Transaction.Transaction Identifier
3 | TxRiskScore | Decimal | | 18 | 6 | yes | Computed transaction ML/TF risk score | Transaction Alert.Financial Crime Risk Score
4 | DecisionStatus | Text | 30 | | | yes | Alert workflow decision status | [Transform: Map Monitoring Outcome](#transform-map-monitoring-outcome)
5 | RaisedAt | DateTime | | | | no | When the alert was raised | Transaction Alert.Raised Date Time

##### Transform: Map Monitoring Outcome

Open alerts are Under Review. Any status SAP adds later is also treated as Under Review until it's mapped, so no alert is closed by default.

```yaml
type: conditional
target: Transaction Alert · Monitoring Outcome
evaluation: exclusive
source:
  field: AlertCase.DecisionStatus
cases:
  Escalated: "DecisionStatus == 'ESCALATED'"
  Cleared: "DecisionStatus == 'CLEARED'"
  Under Review: "DecisionStatus == 'OPEN' OR DecisionStatus IS NULL"
fallback: Under Review
```

##### Worked Examples

```yaml
example: Escalated alert on a payment
given:
  CaseId: "FM-77120"
  PaymentId: "PAY-900001"
  TxRiskScore: 0.914
  DecisionStatus: "ESCALATED"
  RaisedAt: "2024-06-03T02:14:00Z"
produces:
  - entity: Transaction Alert
    Alert Reference: "FM-77120"
    Financial Crime Risk Score: 0.914
    Monitoring Outcome: Escalated
    Raised Date Time: "2024-06-03T02:14:00Z"
notes: The alert belongs to transaction PAY-900001 through Transaction Raises Alerts.
```

```yaml
example: New workflow status defaults to review
given:
  CaseId: "FM-77121"
  PaymentId: "PAY-900002"
  DecisionStatus: "REOPENED"
  RaisedAt: "2024-06-04T10:00:00Z"
produces:
  - entity: Transaction Alert
    Alert Reference: "FM-77121"
    Monitoring Outcome: Under Review
```
