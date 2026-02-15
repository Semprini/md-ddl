# BIAN (Banking Industry Architecture Network) - Standard Guidance

## Overview

BIAN provides a standardized framework for banking with:
- **300+ Service Domains** (functional capabilities like "Customer Agreement", "Current Account")
- **Business Object Model (BOM)** (semantic entities like Party, Account, Payment)
- **Semantic APIs** (REST APIs for each service domain)

**For MD-DDL modeling, reference the BOM (Business Objects), NOT Service Domains.**

## BIAN BOM Structure

BIAN BOM organizes business objects hierarchically:
```
Party (abstract)
├─ Individual
└─ Legal Entity

Party Role (abstract - involvement in business activity)
├─ Customer
├─ Merchant
├─ etc.

Agreement (abstract)
├─ Customer Agreement
├─ Loan Agreement
└─ etc.
```

## Finding BIAN Business Objects

### Search Process

1. User mentions concept (e.g., "Customer")
2. Search: "BIAN Business Object {concept}"
3. Identify correct BOM name
4. Construct URL: `https://bian-modelapi-v4.azurewebsites.net/BOClassByName/{BusinessObject}`
5. Fetch URL to validate
6. Add to MD-DDL references

### Common BIAN BOM Mappings

Business Term | BIAN BOM Object | URL Pattern
--------------|-----------------|------------
Customer, Merchant, Creditor | PartyRole | /BOClassByName/PartyRole
Individual, Person | Individual | /BOClassByName/Individual
Company, Organization | LegalEntity | /BOClassByName/LegalEntity
Party (abstract) | Party | /BOClassByName/Party
Account | Account | /BOClassByName/Account
Loan | LoanAgreement | /BOClassByName/LoanAgreement
Payment, Transaction | Payment | /BOClassByName/Payment
Branch, Location | Location | /BOClassByName/Location
Currency | Currency | /BOClassByName/Currency

### BIAN vs Business Terminology

BIAN Term | Common Business Term | Notes
----------|---------------------|------
Legal Entity | Company, Organization | Use business term in MD-DDL, note BIAN term
Agreement | Contract | Use business term, reference BIAN
Payment | Transaction | Context dependent
Party Role | Customer Role, User Role | BIAN abstraction pattern

## BIAN Party / Party Role Pattern

**Critical Pattern**: BIAN uses an abstract Party and Party Role pattern.

**Party** = The who (Individual or Legal Entity)
**Party Role** = The what they do (Customer, Merchant, Creditor, etc.)

### When to Use BIAN Party Role Pattern

Ask user: "Are Customer, Merchant, etc. managed by different teams with different requirements?"

**If YES**: Make each a first-class entity specializing Party Role
```markdown
### Customer
A party that holds accounts or uses products/services.
- specializes: [Party Role](entities/party-role.md)
- references: [BIAN BOM - Party Role](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/PartyRole)
```

**If NO**: Use a single Party Role entity with Role Type enum

## BIAN Service Domains vs BOM

**Don't confuse these**:

BIAN Component | Purpose | Use in MD-DDL
---------------|---------|---------------
Service Domain | Functional capability (e.g., "Party Reference Data Directory") | ❌ Don't reference in MD-DDL
Business Object Model (BOM) | Semantic entities (e.g., "Party", "PartyRole") | ✅ Reference in MD-DDL
Semantic API | REST API for service domain | ❌ Don't reference in MD-DDL

**Example - WRONG**:
```markdown
- references: [BIAN - Party Reference Data Directory](https://bian.org/semantic-apis/party-reference-data-directory/)
```

**Example - RIGHT**:
```markdown
- references: [BIAN BOM - Party](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/Party)
```

## BIAN Versions

BIAN releases new versions periodically. Current version: **13.0**

When referencing:
- Use version-agnostic URL if possible: `/BOClassByName/{Object}`
- If version-specific, note in references: `BIAN 13.0 - Party Role`

## BIAN + ISO 20022

For payment/transaction entities, you may reference BOTH:
```markdown
### Payment Transaction
A financial transaction involving movement of funds.
- references: [BIAN BOM - Payment](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/Payment)
- references: [ISO 20022 - Payment](url)
```

BIAN provides the business object model, ISO 20022 provides the message format.

## Common BIAN Patterns in MD-DDL

### Pattern 1: Party Abstraction
```markdown
### Party
- detail: [Party](entities/party.md)
- references: [BIAN BOM - Party](url)

### Individual
- specializes: [Party](entities/party.md)
- references: [BIAN BOM - Individual](url)

### Legal Entity
- specializes: [Party](entities/party.md)
- references: [BIAN BOM - LegalEntity](url)
```

### Pattern 2: Party Role Specialization
```markdown
### Party Role
- detail: [Party Role](entities/party-role.md)
- references: [BIAN BOM - PartyRole](url)

### Customer
- specializes: [Party Role](entities/party-role.md)
- references: [BIAN BOM - PartyRole](url)
```

### Pattern 3: Agreement/Contract
```markdown
### Contract
- detail: [Contract](entities/contract.md)
- references: [BIAN BOM - Agreement](url)

### Loan Contract
- specializes: [Contract](entities/contract.md)
- references: [BIAN BOM - LoanAgreement](url)
```

## When BIAN Doesn't Have a Concept

If modeling a concept not in BIAN (e.g., domain-specific internal concept):
- Omit BIAN reference
- Note in detail file: "No BIAN BOM mapping identified - internal business concept"
- Reference other standards if applicable (ISO 20022, Basel, etc.)

## Resources

- BIAN Website: https://bian.org
- BIAN Model API: https://bian-modelapi-v4.azurewebsites.net/
- BIAN Documentation: https://bian.org/deliverables/