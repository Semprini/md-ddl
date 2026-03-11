# [Retail Service](domain.md)

## Enums

### Service Request Status

Status of an initial service request.

```yaml
type: enum
values:
  - Open
  - Resolved
  - Escalated
  - Closed
```

### Service Case Status

Lifecycle status of a managed service case.

```yaml
type: enum
values:
  - Open
  - In Progress
  - Pending Customer
  - Resolved
  - Closed
```

### Contact Channel

Channel through which the customer contacted the service team.

```yaml
type: enum
values:
  - Phone
  - Email
  - Live Chat
  - Self Service
  - In Store
  - Social Media
```
