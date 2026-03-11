# [Telecom](../domain.md)

## Events

### Service Provisioned

Emitted when a Service Order completes successfully and the service is live on the network. This event confirms that the subscriber's service is active and usage recording can begin.

```yaml
actor: Service Order
entity: Service
emitted_on:
  - create
  - update
business_meaning: A service order has completed and the subscriber's network service is now active. Usage recording, allowance tracking, and SLA monitoring begin from this point.
downstream_impact:
  - Usage recording pipeline activates for the service
  - SLA monitoring registers the service activation
  - Customer portal is updated to show service as Active
attributes:
  event_timestamp:
    type: datetime
    description: Time the service was confirmed as provisioned on the network
  service_identifier:
    type: string
    description: Identifier of the provisioned service
  service_number:
    type: string
    description: Subscriber-facing service identifier (MSISDN or circuit ID)
  service_order_identifier:
    type: string
    description: Identifier of the service order that triggered provisioning
  service_type:
    type: string
    description: Category of service that was provisioned
  activation_date:
    type: date
    description: Date the service became active on the network
```
