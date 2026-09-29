# [Financial Crime](../../../domain.md)

## Sources

### [SAP Fraud Management](../source.md#sap-fraud-management)

#### CustomerRiskProfile

The fraud system's current risk assessment for a customer.

##### Entity Fan-Out

```yaml
produces:
  - entity: Customer
    cardinality: 1
    identity: Derive Customer Role Identifier
```

##### Source Schema

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Description | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | PartyExternalId | Text | 40 | | | no | Enterprise party identifier of the customer | [Transform: Derive Customer Role Identifier](#transform-derive-customer-role-identifier)
2 | ReviewRequiredFlag | Boolean | | | | yes | Whether a formal risk review is required | Customer.Risk Review Required
3 | EddTriggerCode | Text | 20 | | | yes | Enhanced due diligence trigger status code | [Transform: Map Enhanced Due Diligence Trigger](#transform-map-enhanced-due-diligence-trigger)

##### Transform: Derive Customer Role Identifier

The same derivation Salesforce CRM uses, so both sources address the same Customer.

```yaml
type: derived
target: Customer · Role Identifier
expression: "'CUST-' + Party External Id"
inputs:
  Party External Id:
    field: CustomerRiskProfile.PartyExternalId
```

##### Transform: Map Enhanced Due Diligence Trigger

```yaml
type: conditional
target: Customer · Enhanced Due Diligence Trigger
evaluation: exclusive
source:
  field: CustomerRiskProfile.EddTriggerCode
cases:
  Triggered: "EddTriggerCode == 'TRIGGERED'"
  Not Triggered: "EddTriggerCode == 'NOT_TRIGGERED'"
  Pending Assessment: "EddTriggerCode == 'PENDING'"
fallback: Pending Assessment
```

##### Worked Examples

```yaml
example: High-risk customer needs enhanced due diligence
given:
  PartyExternalId: "P-1001"
  ReviewRequiredFlag: true
  EddTriggerCode: "TRIGGERED"
produces:
  - entity: Customer
    Role Identifier: "CUST-P-1001"
    Risk Review Required: true
    Enhanced Due Diligence Trigger: Triggered
```
