# [Telecom](domain.md)

## Enums

### Party Type

Discriminator identifying whether a Party is an Individual or Organization.

```yaml
type: enum
values:
  - Individual
  - Organization
```

### Customer Status

Lifecycle status of a customer record.

```yaml
type: enum
values:
  - Active
  - Suspended
  - Closed
  - Prospect
```

### Subscription Status

Lifecycle status of a subscription.

```yaml
type: enum
values:
  - Pending
  - Active
  - Suspended
  - Cancelled
  - Expired
```

### Service Status

Operational status of a provisioned service.

```yaml
type: enum
values:
  - Pending
  - Active
  - Suspended
  - Terminated
```

### Service Order Status

Processing status of a service order.

```yaml
type: enum
values:
  - Acknowledged
  - In Progress
  - Completed
  - Failed
  - Cancelled
```

### Service Order Type

Type of service order action requested.

```yaml
type: enum
values:
  - Provision
  - Modify
  - Suspend
  - Resume
  - Terminate
```

### Usage Type

Category of metered network usage.

```yaml
type: enum
values:
  - Voice
  - SMS
  - Data
  - MMS
  - Roaming Voice
  - Roaming Data
```

### Product Offering Type

Commercial classification of a product offering.

```yaml
type: enum
values:
  - Prepaid
  - Postpaid
  - Hybrid
  - Business
  - Wholesale
```

### Billing Account Status

Operational status of a billing account.

```yaml
type: enum
values:
  - Active
  - Suspended
  - Closed
  - Overdue
```
