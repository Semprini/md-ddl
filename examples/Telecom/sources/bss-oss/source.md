# BSS/OSS Platform

The Business Support System and Operations Support System (BSS/OSS) is the operational source for all subscriber management, product catalog, and provisioning data. It emits changes via real-time CDC for commercial records and event-driven messages for service and usage events.

## Metadata

```yaml
id: bss-oss
owner: platform.engineering@telco.com
steward: data.governance@telco.com

change_model: real-time-cdc
change_events:
  - Customer Created
  - Customer Status Changed
  - Subscription Activated
  - Subscription Cancelled
  - Service Order Submitted
  - Service Order Completed
  - CDR Received

update_frequency: real-time
data_quality_tier: 1
status: Production
version: "2.3.0"

tags:
  - BSS
  - OSS
  - Subscriber Management
  - Provisioning
```

## [Telecom](../../domain.md) Feeds

Canonical Entity | Transform File | Attributes Contributed | Change Model
--- | --- | --- | ---
[Party / Individual](../../entities/individual.md#individual) | [table_subscriber](transforms/table_subscriber.md) | Party Identifier, Given Name, Family Name, Date of Birth, Email Address, Mobile Number, Identity Document Type, Identity Document Number | real-time-cdc
[Organization](../../entities/organization.md#organization) | [table_business_account](transforms/table_business_account.md) | Party Identifier, Legal Name, Trading Name, Registration Number, Industry Sector Code, VAT Number | real-time-cdc
[Customer](../../entities/customer.md#customer) | [table_customer](transforms/table_customer.md) | Customer Identifier, Status, Customer Since Date, Segment, Account Manager | real-time-cdc
[Billing Account](../../entities/billing_account.md#billing-account) | [table_billing_account](transforms/table_billing_account.md) | Billing Account Identifier, Status, Credit Limit, Outstanding Balance, Currency Code, Payment Method Code, Payment Method Token, Billing Cycle Day | real-time-cdc
[Product Offering](../../entities/product_offering.md#product-offering) | [table_product_catalog](transforms/table_product_catalog.md) | Product Offering Identifier, Name, Description, Offering Type, Monthly Charge, Currency Code, Data Allowance GB, Voice Allowance Minutes, SMS Allowance, Commitment Period Months, Valid From Date, Valid To Date | batch
[Subscription](../../entities/subscription.md#subscription) | [table_subscription](transforms/table_subscription.md) | Subscription Identifier, Status, Agreed Monthly Charge, Start Date, Commitment End Date, Auto Renew | real-time-cdc
[Service](../../entities/service.md#service) | [table_service](transforms/table_service.md) | Service Identifier, Service Number, Service Type, Status, Activation Date, Deactivation Date | event-driven
[Service Order](../../entities/service_order.md#service-order) | [table_service_order](transforms/table_service_order.md) | Service Order Identifier, Order Type, Status, Requested Date, Completion Date, Failure Reason | event-driven
[Usage Record](../../entities/usage_record.md#usage-record) | [table_cdr](transforms/table_cdr.md) | Usage Record Identifier, Usage Type, Volume, Volume Unit, Duration Seconds, Session Start, Session End, Destination Number, Roaming Indicator, Rated Amount, Currency Code | event-driven
