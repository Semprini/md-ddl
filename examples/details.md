# Customer Domain

*Note this simple example uses a single file for the details of entities, enums, relationships and events. This is for brevity and to show how linking works. Decide on your file structure based on it's readability for humans and context management for AI.*

## Entities

### Customer

The primary representation of a customer in the organisation.
Any role that is responsible for authority or access to customer data is a Customer.

```yaml
extends: Party Role
attributes:
  - name: Customer Id
    type: string
    identifier: true
  - name: Email
    type: string
    pii: true
  - name: Loyalty Tier
    type: enum:LoyaltyTier
  - name: Balance 
    type: Decimal
```

```yaml
constraints:
  - name: Valid Date Range
    logic: "End Date > Start Date"
  - name: Positive Liquidity
    logic: "Balance > 0"
```

```yaml
governance:
  pii: true
  retention: 7 years
  access_role: HR_ADMIN
```

### Customer Preference

Represents customer‑specific settings and preferences.

```yaml
attributes:
  - name: Preference Name
    type: string
  - name: Value
    type: string
```

## Enums

### Loyalty Tier

A structured level within a loyalty program that offers different benefits and rewards based on engagement or spending.

```yaml
values:
  - Bronze
  - Silver
  - Gold
  - Platinum
```

## Relationships

### Customer Has Preferences

Customers can have zero or more preferences, and preferences are owned by a customer. A preference cannot exist without a customer, and a customer can exist without preferences.

```yaml
source: Customer
target: Customer Preference
cardinality: one-to-many
ownership: Customer
```

```yaml
constraints:
  - name: Active Customer Preference Only
    logic: "Customer.Status == 'Active' OR Customer Preference.EffectiveStatus == 'Inactive'"
    description: "A customer cannot have active preferences if their account is not active."
```
