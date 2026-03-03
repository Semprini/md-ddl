# [Financial Crime](../domain.md)

## Events

### Agreement Activated

Emitted when an agreement becomes active and enforceable.

```yaml
actor: Party Role
entity: Agreement
emitted_on:
  - update
business_meaning: Contractual terms are now active and govern in-scope roles and products
downstream_impact:
  - Product and servicing rules can be applied under the active agreement
  - Contract lifecycle and compliance timelines are started
attributes:
  - event timestamp:
      type: datetime
      description: Time the agreement became active
```
