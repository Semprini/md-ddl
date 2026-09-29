# [Financial Crime](../../../domain.md)

## Sources

### [Salesforce CRM](../source.md#salesforce-crm)

#### Contact

Personal details for the individual behind a person account. Each Contact row adds to the Person that the matching Account row establishes.

##### Entity Fan-Out

```yaml
produces:
  - entity: Party · Person
    cardinality: 1
    contributes: true
    identity:
      field: Contact.PartyExternalId
      maps_to: Party · Party Identifier
```

##### Source Schema

A blank Destination means the column is deliberately not mapped.

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Description | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | PartyExternalId | Text | 40 | | | no | Enterprise party identifier of the parent person account | Person.Party Identifier
2 | FirstName | Text | 120 | | | yes | Contact given name | Person.Given Name, [Transform: Derive Legal Name](#transform-derive-legal-name)
3 | LastName | Text | 120 | | | no | Contact family name | Person.Family Name, [Transform: Derive Legal Name](#transform-derive-legal-name)
4 | Birthdate | Date | | | | yes | Contact date of birth | Person.Date of Birth
5 | CompliancePepFlag | Text | 1 | | | yes | PEP indicator from compliance screening (Y/N) | [Transform: Map PEP Status](#transform-map-pep-status)

##### Transform: Derive Legal Name

A person's legal name is their given and family names as recorded on their identity document.

```yaml
type: derived
target: Person · Legal Name
expression: "trim(coalesce(Given Name, '') + ' ' + Family Name)"
inputs:
  Given Name:
    field: Contact.FirstName
  Family Name:
    field: Contact.LastName
```

##### Transform: Map PEP Status

The CRM flag records whether a person is a PEP but not which category, while the canonical status needs the category. `N` maps to Not PEP. `Y` can't be mapped until the category source is decided (OD-2), so it yields null, which downstream review treats as "confirm PEP category".

```yaml
type: conditional
target: Person · Politically Exposed Person Status
source:
  field: Contact.CompliancePepFlag
cases:
  Not PEP: "CompliancePepFlag == 'N'"
fallback: null   # UNRESOLVED for 'Y' — see OD-2
```

##### Worked Examples

```yaml
example: Non-PEP individual
given:
  PartyExternalId: "P-1002"
  FirstName: "Mere"
  LastName: "Tipene"
  Birthdate: "1986-04-11"
  CompliancePepFlag: "N"
produces:
  - entity: Party · Person
    Party Identifier: "P-1002"
    Given Name: "Mere"
    Family Name: "Tipene"
    Legal Name: "Mere Tipene"
    Date of Birth: "1986-04-11"
    Politically Exposed Person Status: Not PEP
```

```yaml
example: Flagged PEP awaits category
given:
  PartyExternalId: "P-1005"
  FirstName: null
  LastName: "Anand"
  CompliancePepFlag: "Y"
produces:
  - entity: Party · Person
    Party Identifier: "P-1005"
    Legal Name: "Anand"
    Politically Exposed Person Status: null
notes: >
  A missing given name still yields a legal name (coalesce and trim). Y has no case yet
  (OD-2), so the status is null rather than a guessed category.
```

##### Open Decisions

Ref | Item | Impact
--- | --- | ---
OD-2 | `CompliancePepFlag = 'Y'` doesn't say which PEP category applies (domestic, foreign, international organisation, family member, close associate). The category must come from the screening provider or a CRM field not in this extract. | Flagged PEPs load with a null status until the category source is decided.
