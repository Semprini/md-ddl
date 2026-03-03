# [Financial Crime](../domain.md)

## Events

### KYC Status Updated

Emitted when the KYC status of a Party is updated following review or remediation.

```yaml
actor: Compliance Officer
entity: Party
emitted_on:
  - update
business_meaning: The due diligence posture of a party has changed and risk treatment may be updated
downstream_impact:
  - Risk scoring and monitoring thresholds may be recalculated
  - Relationship restrictions or approvals may be adjusted
attributes:
  - event timestamp:
      type: datetime
      description: Time the KYC status update took effect
```
