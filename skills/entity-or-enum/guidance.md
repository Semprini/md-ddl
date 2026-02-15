# Entity or Enum Classification - Detailed Guidance

## Overview

The entity-or-enum decision is one of the most fundamental in data modeling. Getting it wrong leads to:
- Inflexible models that can't accommodate business changes
- Ownership confusion (who maintains this?)
- Governance gaps (who ensures data quality?)
- Integration complexity (how do systems share this?)

This guidance provides deep patterns across industries to help AI make informed classification decisions.

---

## Core Principles

### Principle 1: Business Ownership Signals Entity

If different business teams own or are accountable for a concept, it should be an entity.

**Why**: Different teams mean:
- Different governance processes
- Different approval workflows for changes
- Different compliance requirements
- Different data quality metrics
- Different lifecycle management

**Example - Banking**:
- **Customer** (owned by Customer Management team)
- **Merchant** (owned by Merchant Services team)
- Even though both are "party roles," they're managed completely differently

**Example - Insurance**:
- **Policy Holder** (owned by Underwriting team)
- **Claimant** (owned by Claims team)
- Different teams, different processes, different entities

**Example - Telecommunications**:
- **Customer** (owned by Customer Care)
- **Subscriber** (owned by Network Operations)
- Customer pays bills, Subscriber uses network - different concepts

### Principle 2: Unique Attributes Signal Entity

If a concept has >3 attributes that don't apply to other similar concepts, it's an entity.

**Why**: Unique attributes mean unique business semantics that need to be modeled explicitly.

**Example - Banking**:
**Customer** has unique attributes:
- KYC Status
- Customer Segment
- Relationship Manager
- Marketing Preferences
- Credit Score

**Merchant** has completely different attributes:
- Merchant Category Code (MCC)
- Payment Service Provider
- Settlement Account
- Chargeback Rate
- Merchant Agreement Reference

**These can't share the same entity** - they're fundamentally different.

### Principle 3: Distinct Governance Signals Entity

If a concept has different compliance, retention, or security requirements, it's an entity.

**Why**: Governance is applied at the entity level in most systems.

**Example - Healthcare**:
- **Patient** (HIPAA protected, 7-year retention after last visit)
- **Practitioner** (different credentialing requirements, different retention)
- Can't use same governance rules, must be separate entities

**Example - Banking**:
- **Customer** (KYC/AML requirements, GDPR right to erasure)
- **Teller** (employee data, different privacy rules, different retention)
- Different regulatory frameworks, separate entities

### Principle 4: Simple Classification Signals Enum

If a concept is just a controlled list of values with minimal metadata, it's an enum.

**Why**: Enums are simpler to manage, easier to validate, and don't need separate governance.

**Characteristics of enums**:
- ≤10 values typically
- Values rarely change
- No unique attributes per value (or just 1-2 simple ones)
- Single owner/maintainer
- Applied uniformly across the domain

**Examples**:
- Account Status: Active, Dormant, Frozen, Closed
- Risk Rating: Low, Medium, High, Very High
- Currency Code: USD, EUR, GBP, JPY
- Transaction Type: Wire, ACH, Card, Cash

### Principle 5: Contextual Meaning Signals Relationship Attribute

If a concept only makes sense in the context of a relationship, it's a relationship attribute.

**Why**: It's not a standalone concept - it describes HOW two entities relate.

**Examples**:
- "Role in Transaction" (Debtor, Creditor, Instructing Agent) - only meaningful in context of specific transaction
- "Coverage Level" (Primary, Secondary) - only meaningful in context of specific policy-patient relationship
- "Authorization Type" (Read, Write, Admin) - only meaningful in context of user-resource relationship

---

## Industry Pattern Library

### Banking / Financial Services (BIAN Standard)

**Party Role Pattern**:

In BIAN, Party Role is an abstract concept representing involvement of a party in a business context.

**Decision**: Should Customer, Merchant, Creditor, Debtor be entities or just enum values?

**Analysis**:
- **Customer**: Customer Management team owns, has KYC attributes, GDPR compliance → **Entity**
- **Merchant**: Merchant Services team owns, has MCC codes, settlement rules → **Entity**
- **Creditor**: Just a role in a transaction, no unique attributes → **Relationship Attribute**
- **Debtor**: Just a role in a transaction, no unique attributes → **Relationship Attribute**

**Result**:
```markdown
# Entities
### Party Role
Abstract representation of a party's involvement.

### Customer
Party that holds accounts or uses products/services.
- specializes: [Party Role](entities/party-role.md)

### Merchant
Party that accepts payments for goods or services.
- specializes: [Party Role](entities/party-role.md)

# Relationships
### Transaction Involves Parties
- attributes:
    Role in Transaction:
      type: enum:Transaction Role Type  # Debtor, Creditor, Instructing Agent
```

**Key Insight**: Customer and Merchant are first-class because different teams manage them. Debtor/Creditor are contextual roles in transactions.

**BIAN Reference**: [Party Role Business Object](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/PartyRole)

---

### Insurance (ACORD Standard)

**Party Involvement Pattern**:

In ACORD, parties can be involved in policies and claims in various ways.

**Decision**: Should Policy Holder, Insured, Claimant, Beneficiary be entities or enum values?

**Analysis**:
- **Policy Holder**: Policy Administration team owns, has payment history, billing address → **Entity**
- **Insured**: Often same as Policy Holder, but can be different (e.g., parent insures child) → **Entity** (can reference Policy Holder)
- **Claimant**: Claims team owns, has claim history, fraud scores → **Entity**
- **Beneficiary**: Life insurance context, estate planning requirements → **Entity**

**Result**:
```markdown
# Entities
### Policy Holder
Party that owns and is financially responsible for an insurance policy.

### Insured Party
Party whose life, health, or property is covered by the insurance policy.

### Claimant
Party who submits a claim for benefits under an insurance policy.

### Beneficiary
Party who receives benefits from an insurance policy.
```

**Key Insight**: In insurance, different roles have very different attributes and processes. All are entities.

**ACORD Reference**: Search "ACORD party roles" for standard definitions

---

### Telecommunications (TM Forum SID)

**Customer vs Subscriber Pattern**:

In TM Forum, there's an important distinction between Customer and Subscriber.

**Decision**: Should Customer, Subscriber, Account Holder be entities or the same entity?

**Analysis**:
- **Customer**: The business relationship (billing, payments, customer care) → **Entity**
- **Subscriber**: The service user (network access, usage, technical profile) → **Entity**
- **Account Holder**: Often same as Customer, but not always (corporate scenarios) → **Entity** or reference to Customer

**Real-world scenario**:
- Company X is the **Customer** (signs contract, pays bills)
- Employee Y is the **Subscriber** (uses the mobile service, has SIM card)
- Different teams, different attributes, different entities

**Result**:
```markdown
# Entities
### Customer
The party that has a commercial relationship with the service provider.
- references: [TM Forum SID - Customer](url)

### Subscriber
The party that uses the services and has access to the network.
- references: [TM Forum SID - Subscriber](url)

# Relationships
### Customer Has Subscribers
A corporate customer can have many individual subscribers (employees).
```

**Key Insight**: Telecom separates commercial relationship from service usage. Two entities.

**TM Forum Reference**: Search "TM Forum SID Customer Subscriber" for standard definitions

---

### Healthcare (FHIR Standard)

**Person vs Patient vs Practitioner Pattern**:

In FHIR, Person is a general concept, but Patient and Practitioner are specific roles.

**Decision**: Should Patient, Practitioner, RelatedPerson be entities or specializations?

**Analysis**:
- **Patient**: Subject of care, EMR team owns, HIPAA protected → **Entity**
- **Practitioner**: Provides care, credentialing team owns, licensing requirements → **Entity**
- **RelatedPerson**: Associated with patient (family, guardian), different privacy → **Entity**

**Result**:
```markdown
# Entities
### Party
Abstract representation of a person or organization in healthcare context.

### Patient
A person receiving or registered to receive healthcare services.
- specializes: [Party](entities/party.md)
- references: [FHIR - Patient](https://hl7.org/fhir/patient.html)

### Practitioner
A person who is directly or indirectly involved in provisioning healthcare.
- specializes: [Party](entities/party.md)
- references: [FHIR - Practitioner](https://hl7.org/fhir/practitioner.html)

### Related Person
A person related to a patient (family member, guardian, caregiver).
- specializes: [Party](entities/party.md)
- references: [FHIR - RelatedPerson](https://hl7.org/fhir/relatedperson.html)
```

**Key Insight**: Healthcare roles have distinct regulatory requirements and ownership. All entities.

**FHIR Reference**: [FHIR Resource Index](https://hl7.org/fhir/resourcelist.html)

---

## Complex Scenarios

### Scenario 1: "What if we add attributes later?"

**Question**: "Right now it's just a type, but we might add attributes later. Should it be an entity now?"

**Answer**: 
- If you're **certain** attributes will be added within 6 months → Entity
- If it's **hypothetical** ("maybe someday") → Enum (can refactor later)
- If different teams are **already discussing** ownership → Entity

**Refactoring from Enum to Entity is acceptable** in MD-DDL - the two-layer structure makes this easier than in traditional modeling.

### Scenario 2: "What about entities with only 2 attributes?"

**Question**: "Customer only has Customer ID and Name. Does it need to be an entity?"

**Answer**:
- Check ownership: Who maintains customer data? If distinct team → Entity
- Check future: Will KYC, preferences, relationships be added? → Entity
- Check governance: Different compliance rules? → Entity
- If truly minimal and no plans to expand → Consider if this is really just a reference

**Most "minimal" entities in early modeling become rich entities as the model matures.**

### Scenario 3: "What about enums with 50+ values?"

**Question**: "We have 50+ product types. Should this still be an enum?"

**Answer**:
- If all 50+ types share the same attributes → Enum (large but still classification)
- If different product types have different attributes → Entity hierarchy
- If product types are actively managed by a Product team → Entity

**Example - Telecom**:
- 50+ service plan names → **Enum** (just names, all plans have same structure)
- 5 product categories (Mobile, Broadband, TV, Landline, IoT) where each has unique technical attributes → **Entity hierarchy**

### Scenario 4: "What about temporal enums?"

**Question**: "Our status values change over time (we add new statuses). Should it be an entity to track changes?"

**Answer**:
- Enum values changing over time (adding/removing values) is normal → Still Enum
- Need to track **when** values were added/removed → Use enum with metadata in detail file
- Need to track **which instances** had which values **when** → Entity with temporal tracking

**Most enums don't need temporal tracking** - it's the entity that has the status that needs temporal tracking, not the enum itself.

---

## Anti-Patterns

### ❌ Anti-Pattern 1: "Everything is an Entity"

**Problem**: Making every concept an entity "just in case"

**Why it's wrong**:
- Overcomplicated model
- Governance burden (who owns Status as an entity?)
- Integration complexity (50 entity types for simple classifications)

**Solution**: Use enums liberally for simple classifications

---

### ❌ Anti-Pattern 2: "Everything is an Enum"

**Problem**: Using enums for concepts that clearly have business ownership

**Why it's wrong**:
- Can't model unique attributes
- Can't apply distinct governance
- Forces artificial constraints

**Example - Wrong**:
```yaml
attributes:
  Party Role Type:
    type: enum:Party Role Type  # Customer, Merchant, Teller, etc.
```

**Example - Right**:
```markdown
### Customer
First-class entity with KYC attributes
- specializes: [Party Role](entities/party-role.md)
```

---

### ❌ Anti-Pattern 3: "When in Doubt, Make it Both"

**Problem**: Creating both an entity AND an enum for the same concept

**Example - Wrong**:
```markdown
# Entity
### Customer Type
An entity representing types of customers...

# Enum  
### Customer Type Values
Retail, Corporate, Government...
```

**Why it's wrong**: Confusing, duplicate maintenance, unclear which to use

**Solution**: Pick one based on the decision framework

---

## Decision Examples by Attribute Count

### 0-1 Attributes → Enum
```yaml
# Account Status - just the value
values:
  - Active
  - Dormant
  - Frozen
  - Closed
```

### 2-3 Attributes → Probably Enum (with metadata)
```yaml
# Risk Rating - value plus score
values:
  Low:
    score: 1
    description: Minimal risk
  Medium:
    score: 2
    description: Moderate risk
  High:
    score: 3
    description: Significant risk
```

### 4+ Attributes → Probably Entity
```yaml
# Customer - many unique attributes
attributes:
  Customer ID:
    type: string
    identifier: primary
  KYC Status:
    type: enum:KYC Status
  Customer Segment:
    type: enum:Customer Segment
  Risk Rating:
    type: enum:Risk Rating
  Relationship Manager:
    type: string
  Onboarding Date:
    type: date
```

---

## Refactoring Guide

### Enum → Entity Migration

When to refactor:
- Business asks to add 4+ attributes
- Different team takes ownership
- Distinct governance requirements emerge

**Process**:
1. Create new entity detail file
2. Add specialized attributes
3. Update summary to declare as entity (not enum)
4. Keep old enum for backward compatibility (deprecated)
5. Create migration guide for consumers

### Entity → Enum Simplification

When to refactor (rare):
- Entity proves to be over-engineered
- No team claims ownership
- No unique attributes emerged
- Just a classification after all

**Process**:
1. Create enum detail file
2. Mark entity as deprecated
3. Provide migration path for consumers

---

## Summary Decision Matrix

Ask | Entity | Enum | Relationship Attribute
----|--------|------|----------------------
Different owner? | ✅ Yes | ❌ No | ❌ No
>3 unique attributes? | ✅ Yes | ❌ No | ❌ No
Distinct governance? | ✅ Yes | ❌ No | ❌ No
Just classification? | ❌ No | ✅ Yes | ❌ No
Only in relationship context? | ❌ No | ❌ No | ✅ Yes
Has own lifecycle? | ✅ Yes | ❌ No | ❌ No
Managed by team? | ✅ Yes | Maybe | ❌ No

---

## Related Guidance

- [inheritance/guidance.md](../inheritance/guidance.md) - Once classified as entity, design hierarchy
- [relationship-design/guidance.md](../relationship-design/guidance.md) - When classified as relationship attribute
- [constraint-logic/guidance.md](../constraint-logic/guidance.md) - Constraints differ for entities vs enums
