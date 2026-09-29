# [Financial Crime](../../../domain.md)

## Sources

### [Salesforce CRM](../source.md#salesforce-crm)

#### Preference

A customer's communication and consent preferences, delivered as a platform event whenever they change.

##### Entity Fan-Out

```yaml
produces:
  - entity: Customer Preferences
    cardinality: 1
    identity:
      field: Preference.Id
      maps_to: Customer Preferences · Preference Identifier
    references:
      Customer: Derive Customer Role Identifier
```

##### Source Schema

Pos | Column Name | Data Type | Max Len | Precision | Scale | Nulls | Description | Destination
--- | --- | --- | --- | --- | --- | --- | --- | ---
1 | Id | Text | 18 | | | no | Salesforce record identifier | Customer Preferences.Preference Identifier
2 | PartyExternalId | Text | 40 | | | no | Enterprise party identifier of the customer | Reference: Customer
3 | PreferredChannelCode | Text | 10 | | | yes | Preferred communication channel code | [Transform: Map Contact Preference](#transform-map-contact-preference)
4 | MarketingOptInFlag | Text | 1 | | | yes | Opt-in indicator for marketing messages (Y/N) | [Transform: Map Marketing Consent](#transform-map-marketing-consent)
5 | EffectiveDate | Date | | | | no | Date the preferences took effect | Customer Preferences.Effective From

##### Transform: Derive Customer Role Identifier

Computes the key of the existing Customer role these preferences belong to, exactly as the Account table derives it. It's used only in `references`: it identifies the Customer, and never creates or updates one.

```yaml
type: derived
target: Customer · Role Identifier
expression: "'CUST-' + Party External Id"
inputs:
  Party External Id:
    field: Preference.PartyExternalId
```

##### Transform: Map Contact Preference

```yaml
type: lookup
target: Customer Preferences · Contact Preference
source:
  field: Preference.PreferredChannelCode
lookup:
  inline:
    EMAIL: Email
    SMS: SMS
    POST: Post
    PHONE: Phone
    APP: In App
    NONE: No Contact
fallback: null
```

##### Transform: Map Marketing Consent

Consent is only recorded when the customer answered. A missing flag stays null rather than being read as a refusal, so consent is never inferred.

```yaml
type: conditional
target: Customer Preferences · Marketing Consent
evaluation: exclusive
source:
  field: Preference.MarketingOptInFlag
cases:
  true: "MarketingOptInFlag == 'Y'"
  false: "MarketingOptInFlag == 'N'"
fallback: null
```

##### Worked Examples

```yaml
example: Opted in, prefers email
given:
  Id: "a0P000000000001"
  PartyExternalId: "P-1001"
  PreferredChannelCode: "EMAIL"
  MarketingOptInFlag: "Y"
  EffectiveDate: "2024-02-15"
produces:
  - entity: Customer Preferences
    Preference Identifier: "a0P000000000001"
    Contact Preference: Email
    Marketing Consent: true
    Effective From: "2024-02-15"
notes: The preferences attach to the Customer role CUST-P-1001.
```

```yaml
example: No consent answer recorded
given:
  Id: "a0P000000000002"
  PartyExternalId: "P-1003"
  PreferredChannelCode: "NONE"
  MarketingOptInFlag: null
  EffectiveDate: "2024-05-20"
produces:
  - entity: Customer Preferences
    Preference Identifier: "a0P000000000002"
    Contact Preference: No Contact
    Marketing Consent: null
```
