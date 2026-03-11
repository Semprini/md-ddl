# [Telecom](../domain.md)

## Events

### Usage Recorded

Emitted when a Usage Record is committed to the billing system following mediation. This event triggers downstream rating, allowance deduction, and fraud screening pipelines.

```yaml
actor: Network
entity: Usage Record
emitted_on:
  - create
business_meaning: A metered call detail record has been received from the network, validated by the mediation layer, and committed to the billing system. Rating and allowance deduction are triggered. This event is the primary input for real-time fraud detection.
downstream_impact:
  - Rating engine applies charges or deducts from included allowances
  - Real-time fraud screening evaluates the CDR for anomalous patterns
  - Revenue assurance pipeline checks for duplicate or missing CDRs
  - Usage summary aggregations are updated for analytics
attributes:
  event_timestamp:
    type: datetime
    description: Time the usage record was committed by the mediation system
  usage_record_identifier:
    type: string
    description: Unique CDR identifier
  service_identifier:
    type: string
    description: Identifier of the service that generated the usage
  usage_type:
    type: string
    description: Category of usage (Voice, SMS, Data, MMS, Roaming Voice, Roaming Data)
  volume:
    type: decimal
    description: Quantity of usage consumed
  volume_unit:
    type: string
    description: Unit of measurement for the volume
  session_start:
    type: datetime
    description: UTC timestamp when the usage session began
  roaming_indicator:
    type: boolean
    description: True if the usage occurred while roaming on a partner network
  rated_amount:
    type: decimal
    description: Charge applied after allowance deduction and rating
```
