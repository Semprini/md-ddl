# [Financial Crime](../domain.md)

## Events

### Party Role Assigned

Emitted when a Party assumes a new Party Role in a business context.

```yaml
actor: Party
entity: Party Role
emitted_on:
  - create
business_meaning: A party has been assigned a role that changes participation context and controls
downstream_impact:
  - Access and entitlements can be updated for the new role
  - Role-based monitoring and due diligence workflows are triggered
attributes:
  - event timestamp:
      type: datetime
      description: Time the role assignment became effective
```
