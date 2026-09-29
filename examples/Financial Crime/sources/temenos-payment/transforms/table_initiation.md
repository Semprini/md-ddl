# [Financial Crime](../../../domain.md)

## Sources

### [Temenos Payment](../source.md#temenos-payment)

#### Initiation

Who initiated a payment, and through which channel.

##### Entity Fan-Out

```yaml
produces:
  - entity: Payment Initiator
    cardinality: 1
    identity:
      field: Initiation.ActorRoleId
      maps_to: Payment Initiator · Role Identifier
    references:
      Transaction: Initiation.PaymentId
```

##### Source Schema

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Description | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | PaymentId | Text | 64 | | | no | Payment the initiation belongs to | Transaction.Transaction Identifier
2 | ActorRoleId | Text | 64 | | | no | Role identifier of the initiator | Payment Initiator.Role Identifier
3 | ChannelCode | Text | 20 | | | yes | Channel where initiation occurred | [Transform: Map Initiation Channel](#transform-map-initiation-channel)

##### Transform: Map Initiation Channel

API initiations come from third-party providers, so they map to Third Party in the domain's channel vocabulary.

```yaml
type: conditional
target: Payment Initiator · Initiation Channel
evaluation: exclusive
source:
  field: Initiation.ChannelCode
cases:
  Branch: "ChannelCode == 'BRANCH'"
  Mobile Banking: "ChannelCode == 'MOBILE'"
  Online Banking: "ChannelCode == 'ONLINE'"
  Third Party: "ChannelCode == 'API'"
fallback: null
```

##### Worked Examples

```yaml
example: Payment initiated through a third-party API
given:
  PaymentId: "PAY-900001"
  ActorRoleId: "INIT-3301"
  ChannelCode: "API"
produces:
  - entity: Payment Initiator
    Role Identifier: "INIT-3301"
    Initiation Channel: Third Party
```
