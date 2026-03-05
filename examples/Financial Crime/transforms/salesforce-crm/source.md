# Salesforce CRM

Salesforce CRM is the customer relationship source for onboarding, profile maintenance, and communication preferences. It contributes party identity, customer profile, and contact data used by KYC and due diligence workflows.

## Metadata

```yaml
id: salesforce-crm
owner: crm.platform@bank.com
steward: data.governance@bank.com

change_model: real-time-cdc
change_events:
  - Customer Created
  - Customer Updated
  - Contact Address Updated
  - Customer Preference Updated

update_frequency: real-time
data_quality_tier: 1
status: Production
version: "1.0.0"
```

## [Financial Crime](../../domain.md) Feeds

Canonical Entity | Transform File | Attributes Contributed | Change Model
--- | --- | --- | ---
[Party](../../entities/party.md#party) | [table_account](table_account.md) | Party Identifier, Party Status | real-time-cdc
[Person](../../entities/person.md#person) | [table_contact](table_contact.md) | Given Name, Family Name, Date of Birth, PEP Status | real-time-cdc
[Company](../../entities/company.md#company) | [table_account](table_account.md) | Legal Name, Registration Identifier | real-time-cdc
[Customer](../../entities/customer.md#customer) | [table_account](table_account.md) | Customer Number, Onboarding Date, Segment | real-time-cdc
[Contact Address](../../entities/contact_address.md#contact-address) | [table_contact_point](table_contact_point.md) | Address Purpose, Verification Status, Effective Dates | real-time-cdc
[Customer Preferences](../../entities/customer-preferences.md#customer-preferences) | [table_preference](table_preference.md) | Preferred Contact Channel, Marketing Consent | event-driven
