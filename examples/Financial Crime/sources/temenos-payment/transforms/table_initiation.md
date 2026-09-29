# [Financial Crime](../../../domain.md)

## Sources

### [Temenos Payment](../source.md#temenos-payment)

#### Initiation

Who initiated a payment, and through which channel. The channel is a fact about this payment, so it lands on the Transaction. The initiator is a Party Role of the initiating party, keyed on that party like every other role.

##### Entity Fan-Out

```yaml
produces:
  - entity: Payment Initiator
    cardinality: 1
    identity: Derive Initiator Role Identifier
    references:
      Party: Initiation.ActorPartyId

  - entity: Transaction
    cardinality: 1
    contributes: true
    identity:
      field: Initiation.PaymentId
      maps_to: Transaction · Transaction Identifier
    references:
      Payment Initiator: Derive Initiator Role Identifier
```

##### Source Schema

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Description | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | PaymentId | Text | 64 | | | no | Payment the initiation belongs to | Transaction.Transaction Identifier
2 | ActorPartyId | Text | 40 | | | no | Enterprise party identifier of the initiator | [Transform: Derive Initiator Role Identifier](#transform-derive-initiator-role-identifier)
3 | ChannelCode | Text | 20 | | | yes | Channel where initiation occurred | [Transform: Map Transaction Channel](#transform-map-transaction-channel)

##### Transform: Derive Initiator Role Identifier

Initiator roles are keyed on the initiating party, like Customer, so the same party always has the same initiator role.

```yaml
type: derived
target: Payment Initiator · Role Identifier
expression: "'INIT-' + Actor Party Id"
inputs:
  Actor Party Id:
    field: Initiation.ActorPartyId
```

##### Transform: Map Transaction Channel

API initiations come from third-party providers, so they map to Third Party.

```yaml
type: conditional
target: Transaction · Transaction Channel
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
  ActorPartyId: "P-1001"
  ChannelCode: "API"
produces:
  - entity: Payment Initiator
    Role Identifier: "INIT-P-1001"
  - entity: Transaction
    Transaction Identifier: "PAY-900001"
    Transaction Channel: Third Party
notes: >
  The Transaction already exists from PaymentEvent; this row contributes its channel and links
  it to INIT-P-1001 through Transaction Initiated By Instructing Agent.
```
