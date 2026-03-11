# [Retail Service](../domain.md)

## Events

### Service Request Received

Emitted when a new service request is received from a customer via any contact channel. Triggers routing, SLA timer initiation, and first-response workflows.

```yaml
actor: Customer
entity: Service Request
emitted_on:
  - create
business_meaning: A customer has contacted support with an issue or query. An SLA clock begins and the request must be routed to the appropriate team.
downstream_impact:
  - SLA timer is initiated for first-response measurement
  - Routing engine assigns the request to the appropriate team or agent
  - Customer receives an acknowledgement notification with a reference number
  - Case load metrics are updated for the receiving team
attributes:
  event_timestamp:
    type: datetime
    description: Time the service request was received
  service_request_identifier:
    type: string
    description: Identifier of the received service request
  customer_identifier:
    type: string
    description: Identifier of the customer who raised the request
  contact_channel:
    type: string
    description: Channel through which the request was received
  subject:
    type: string
    description: Brief description of the customer's issue
```
