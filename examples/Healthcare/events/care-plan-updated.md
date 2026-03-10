# [Healthcare](../domain.md)

## Events

### Care Plan Updated

Emitted when a care plan is created or revised. Care plan revisions are clinically significant — they reflect changed treatment strategies, new evidence, or patient response to treatment.

```yaml
actor: Practitioner
entity: Care Plan
emitted_on:
  - create
  - update
business_meaning: A care plan has been created or revised to reflect updated clinical decisions
downstream_impact:
  - Care coordination team is notified of the revised plan
  - Medication orders may be updated to reflect new treatment strategy
  - Patient education materials are regenerated for the new plan
  - Quality and outcomes tracking is updated
attributes:
  event_timestamp:
    type: datetime
    description: Time the care plan was created or revised
  previous_status:
    type: string
    description: Status of the care plan before this change (null for new plans)
  new_status:
    type: string
    description: Status of the care plan after this change
  revision_reason:
    type: string
    description: Clinical reason for the care plan revision
  conditions_addressed:
    type: string[]
    description: List of condition identifiers addressed by the updated plan
```
