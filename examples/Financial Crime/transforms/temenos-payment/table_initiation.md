# [Temenos Payment](./source.md)

## Initiation

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Comment | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | ActorRoleId | Text | 64 | | | no | Role identifier that initiated payment | Payment Initiator.Initiator Role Identifier
2 | ChannelCode | Text | 20 | | | yes | Channel where initiation occurred | [Map Initiation Channel](#map-initiation-channel)

### Map Initiation Channel

Maps channel used to initiate payment to canonical channel.

```yaml
type: conditional
target: Payment Initiator · Initiation Channel
source:
  field: Initiation.ChannelCode
cases:
  Branch: "ChannelCode == 'BRANCH'"
  Mobile: "ChannelCode == 'MOBILE'"
  Internet Banking: "ChannelCode == 'ONLINE'"
  API: "ChannelCode == 'API'"
fallback: API
```
