# [Financial Crime](../../../domain.md)

## Sources

### [Salesforce CRM](../source.md#salesforce-crm)

#### Account

One Account row describes a party and, where it has one, its customer relationship. Business accounts carry a legal entity name; person accounts don't.

##### Entity Fan-Out

```yaml
produces:
  - entity: Party · Company
    cardinality: 0..1
    condition: "LegalEntityName IS NOT NULL"
    identity:
      field: Account.ExternalPartyId
      maps_to: Party · Party Identifier

  - entity: Party · Person
    cardinality: 0..1
    condition: "LegalEntityName IS NULL"
    identity:
      field: Account.ExternalPartyId
      maps_to: Party · Party Identifier

  - entity: Customer
    cardinality: 0..1
    condition: "CustomerNumber IS NOT NULL"
    identity: Derive Customer Role Identifier
    references:
      Party: Account.ExternalPartyId
```

##### Source Schema

A blank Destination means the column is deliberately not mapped.

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Description | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | ExternalPartyId | Text | 40 | | | no | Enterprise party identifier held on the CRM account | Party.Party Identifier, [Transform: Derive Customer Role Identifier](#transform-derive-customer-role-identifier)
2 | RecordStatus | Text | 20 | | | yes | Account lifecycle status from CRM | [Transform: Map Party Status](#transform-map-party-status)
3 | LegalEntityName | Text | 200 | | | yes | Registered legal entity name; empty for person accounts | Company.Legal Name
4 | CompanyRegistrationNumber | Text | 80 | | | yes | Jurisdictional registration number | Company.Company Registration Number
5 | CustomerNumber | Text | 100 | | | yes | CRM customer reference | Customer.Customer Number
6 | OnboardingCompletedDate | Date | | | | yes | Date onboarding completed | Customer.Onboarding Date
7 | CustomerSegmentCode | Text | 30 | | | yes | Commercial segment classification code | [OD-1](#open-decisions)

##### Transform: Map Party Status

Translates CRM lifecycle status into canonical party status. CRM `Suspended` means services are restricted pending review, so it maps to Restricted. Unrecognised statuses fall back to Under Review, so an analyst looks at them rather than the pipeline guessing a benign value.

```yaml
type: conditional
target: Party · Party Status
evaluation: exclusive
source:
  field: Account.RecordStatus
cases:
  Active: "RecordStatus == 'Active'"
  Inactive: "RecordStatus == 'Inactive'"
  Restricted: "RecordStatus == 'Suspended'"
  Closed: "RecordStatus == 'Closed'"
fallback: Under Review
```

##### Transform: Derive Customer Role Identifier

The customer role is keyed on the enterprise party identifier, so every source that knows the party derives the same role identifier.

```yaml
type: derived
target: Customer · Role Identifier
expression: "'CUST-' + External Party Id"
inputs:
  External Party Id:
    field: Account.ExternalPartyId
```

##### Worked Examples

```yaml
example: Business account with a customer relationship
given:
  ExternalPartyId: "P-1001"
  RecordStatus: "Active"
  LegalEntityName: "Harbour Freight Pty Ltd"
  CompanyRegistrationNumber: "ACN 123 456 789"
  CustomerNumber: "C-20001"
  OnboardingCompletedDate: "2024-02-15"
produces:
  - entity: Party · Company
    Party Identifier: "P-1001"
    Party Status: Active
    Legal Name: "Harbour Freight Pty Ltd"
    Company Registration Number: "ACN 123 456 789"
  - entity: Customer
    Role Identifier: "CUST-P-1001"
    Customer Number: "C-20001"
    Onboarding Date: "2024-02-15"
notes: >
  LegalEntityName is present, so the Company branch fires and the Person branch doesn't.
  CustomerNumber is present, so a Customer role is produced for the same party.
```

```yaml
example: Suspended person account with no customer relationship yet
given:
  ExternalPartyId: "P-1002"
  RecordStatus: "Suspended"
  LegalEntityName: null
  CustomerNumber: null
produces:
  - entity: Party · Person
    Party Identifier: "P-1002"
    Party Status: Restricted
  - entity: Customer
    cardinality: 0
notes: >
  No legal entity name means a person account. CRM Suspended maps to Restricted. With no
  CustomerNumber, the Customer entry's condition fails and no role is produced.
```

```yaml
example: Unrecognised CRM status is routed to review
given:
  ExternalPartyId: "P-1004"
  RecordStatus: "Archived"
  LegalEntityName: "Old Mill Holdings Ltd"
produces:
  - entity: Party · Company
    Party Identifier: "P-1004"
    Party Status: Under Review
notes: >
  Archived matches no case, so the fallback applies. Under Review is deliberate: an unknown
  status on a compliance-relevant field is escalated, not guessed.
```

```yaml
example: CRM onboards a company; SAP screening and risk profile arrive later
given:
  - from: Salesforce CRM · Account
    row:
      ExternalPartyId: "P-1003"
      RecordStatus: "Active"
      LegalEntityName: "Coral Trading Ltd"
      CustomerNumber: "C-20003"
  - from: SAP Fraud Management · SanctionsScreening
    row:
      PartyExternalId: "P-1003"
      ResultCode: "POTENTIAL_MATCH"
  - from: SAP Fraud Management · CustomerRiskProfile
    row:
      PartyExternalId: "P-1003"
      ReviewRequiredFlag: true
      EddTriggerCode: "TRIGGERED"
produces:
  - entity: Party · Company
    Party Identifier: "P-1003"
    Party Status: Active
    Legal Name: "Coral Trading Ltd"
    Sanctions Screen Status: Potential Match
  - entity: Customer
    Role Identifier: "CUST-P-1003"
    Customer Number: "C-20003"
    Risk Review Required: true
    Enhanced Due Diligence Trigger: Triggered
interim:
  - after: 1
    produces:
      - entity: Party · Company
        Party Identifier: "P-1003"
        Party Status: Active
        Sanctions Screen Status: null
      - entity: Customer
        Role Identifier: "CUST-P-1003"
        Risk Review Required: null
        Enhanced Due Diligence Trigger: null
notes: >
  Fan-in: the three sources contribute disjoint attributes to the same Party and Customer,
  so no reconciliation is needed. SAP rows carry the enterprise party identifier, and the
  customer role identifier is derived from it the same way on both sides. Until SAP
  arrives, the screening and risk attributes are null. The Canonical Party product
  declares eventual consistency with a nullable-staging null strategy, so these interim
  rows are visible in staging but not in the converged view.
```

##### Open Decisions

Ref | Item | Impact
--- | --- | ---
OD-1 | `CustomerSegmentCode` values and meaning are undocumented, and the model has no customer segment attribute. | Not mapped until the domain owner decides whether Customer needs a Segment attribute and enum.
