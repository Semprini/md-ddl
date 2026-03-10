# [Financial Crime](../domain.md)

## Events

### High Risk Transaction Detected

Emitted when transaction monitoring identifies a transaction with high financial crime risk indicators.

```yaml
actor: Transaction Monitoring System
entity: Transaction
emitted_on:
  - create
business_meaning: A transaction has been identified for enhanced investigation due to elevated risk
downstream_impact:
  - Alert and case management workflows are initiated
  - Potential reporting obligations may be triggered
attributes:
  event_timestamp:
    type: datetime
    description: Time the high-risk detection decision was produced
  alert_type:
    type: string
    description: Category of the detection rule that triggered (e.g. structuring, velocity, geographic)
  severity:
    type: string
    description: Assessed severity level of the alert (low, medium, high, critical)
  detection_method:
    type: string
    description: Name of the detection model or rule that produced the alert
  threshold_breached:
    type: string
    description: The specific threshold or limit that was exceeded
  risk_score:
    type: decimal
    description: Numeric risk score assigned by the detection engine
```
