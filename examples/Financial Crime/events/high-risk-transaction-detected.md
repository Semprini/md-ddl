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
  - event timestamp:
      type: datetime
      description: Time the high-risk detection decision was produced
```
