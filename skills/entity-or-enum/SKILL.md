---
name: entity-or-enum
description: Decide whether a concept should be a first-class entity, an enum, or a relationship attribute in MD-DDL. Use when discovering a new concept during modeling, or when user asks "should this be an entity?" or "is this just a type?"
---

# Entity or Enum Classification

## Quick Decision Framework

Ask these questions in order:

1. **Is it owned by a different business team with distinct requirements?**
   - YES → **Entity**
   - NO → Continue to question 2

2. **Does it have >3 unique attributes beyond just type/classification?**
   - YES → **Entity**
   - NO → Continue to question 3

3. **Does it have distinct governance, compliance, or lifecycle requirements?**
   - YES → **Entity**
   - NO → Continue to question 4

4. **Is it just a controlled vocabulary or classification?**
   - YES → **Enum**
   - NO → Continue to question 5

5. **Is it only meaningful in the context of a relationship?**
   - YES → **Relationship Attribute**
   - NO → **Entity** (when in doubt)

## Common Pattern: Party Role Specialization

This pattern appears across industries (banking, insurance, telecom, healthcare):

**Scenario**: Modeling Customer, Merchant, Subscriber, Policy Holder, Patient, etc.

**Ask user**: "Are these concepts managed by different business teams with different requirements?"

**If YES**:
- Make each a **first-class entity**
- Each specializes an abstract parent (Party Role, Coverage Type, etc.)
- Each team owns their entity with specific attributes and governance

**If NO**:
- Use **enum** for role type
- Single Party Role entity with Role Type enum attribute

## Questions to Ask User

- "Is **{concept}** owned by a different business team?"
- "Does **{concept}** have unique attributes beyond just its type or name?"
- "Does **{concept}** have separate compliance, retention, or security requirements?"
- "Does **{concept}** have its own lifecycle (created, activated, closed, etc.)?"

## Examples by Industry

**Banking** (using BIAN):
- ✅ **Customer** as entity (Customer team owns, KYC attributes, compliance requirements)
- ✅ **Merchant** as entity (Merchant Services owns, different agreements, different risk)
- ❌ **Account Status** as enum (simple classification: Active, Dormant, Closed)

**Insurance** (using ACORD):
- ✅ **Policy Holder** as entity (distinct from Claimant or Beneficiary, different ownership)
- ✅ **Claim** as entity (Claims team owns, complex lifecycle, distinct attributes)
- ❌ **Coverage Type** as enum (Auto, Property, Life - simple classification)

**Telecommunications** (using TM Forum):
- ✅ **Customer** as entity (Customer Care owns, distinct from Subscriber)
- ✅ **Subscriber** as entity (Network team owns, technical subscriptions)
- ❌ **Service Type** as enum (Mobile, Broadband, TV - simple classification)

**Healthcare** (using FHIR):
- ✅ **Patient** as entity (distinct from Practitioner, different attributes)
- ✅ **Practitioner** as entity (Provider team owns, credentialing requirements)
- ❌ **Encounter Type** as enum (Inpatient, Outpatient, Emergency - classification)

## Output Format

### Entity Summary (in domain.md)
```markdown
### Customer
A party that holds accounts, uses products/services, or has an active relationship with the institution. First-class business concept with distinct ownership and governance.
- specializes: [Party Role](entities/party-role.md)
- detail: [Customer](entities/customer.md)
- references: [BIAN BOM - Party Role](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/PartyRole)
```

### Enum Summary (in domain.md)
```markdown
### Account Status
Current operational status of an account (Active, Dormant, Frozen, Closed).
- detail: [Account Status](enums/account-status.md)
- references: [BIAN BOM - Account](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/Account)
```

### Relationship Attribute
```markdown
### Transaction Involves Parties
Transactions link to Parties in various roles (Debtor, Creditor, Instructing Agent).
- detail: [Transaction Involves Parties](relationships/transaction-involves-parties.md)

# In the relationship detail file:
attributes:
  Role in Transaction:
    type: enum:Party Role Type
    description: The role this party plays in this specific transaction
```

## When to Load Detailed Guidance

Load [guidance.md](guidance.md) when:
- User's domain doesn't fit standard banking/insurance/telecom patterns
- First time modeling party/role abstraction
- Dealing with concepts that seem to be "both" entity and enum
- User challenges the classification decision
- Need complete worked examples from multiple industries
- Handling edge cases (e.g., "what if attributes are added later?")

## Related Skills

- [inheritance](../inheritance/SKILL.md) - Once classified as entity, design hierarchy
- [external-standard-mapping](../external-standard-mapping/SKILL.md) - Find standard references
- [relationship-design](../relationship-design/SKILL.md) - If classified as relationship attribute