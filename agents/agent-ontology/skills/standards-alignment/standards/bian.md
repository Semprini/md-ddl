# BIAN (Banking Industry Architecture Network) - Standard Guidance

## Overview

BIAN provides a standardized framework for banking with:

- **300+ Service Domains** (functional capabilities like "Customer Agreement", "Current Account")
- **Business Object Model (BOM)** (semantic entities like Party, Account, Payment)
- **Semantic APIs** (REST APIs for each service domain)

**For MD-DDL modeling, reference the BOM (Business Objects), NOT Service Domains.**

## BIAN BOM Structure

BIAN BOM organizes business objects hierarchically:

```text
Party (abstract)
├─ Person (or Individual in older versions)
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

### Deterministic Lookup Process (No Guessing)

Use this process whenever the business term may not exactly match BIAN naming.

1. Start with candidate search (small payload):
   - `GET /BOClassesBasicByNameLike/{nameLike}/{organisation}/{version}`
   - Use: `organisation=BIAN`, `version=13.0.0`
   - Example:
     `https://bian-modelapi-v4.azurewebsites.net/BOClassesBasicByNameLike/Cust/BIAN/13.0.0`
2. Build a short candidate list (max 3-5) based on semantic fit:
   - exact or close name match
   - description alignment with user intent
   - whether concept is abstract base vs specialization
3. Resolve each shortlisted candidate to full details:
   - `GET /BOClassByName/{ExactBianName}/BIAN/13.0.0`
4. Select mapping outcome:
   - exact match
   - parent/specialisation match
   - partial match (document the difference)
   - no match
5. Only after confirmation, add reference URL in MD-DDL:
   - `https://bian-modelapi-v4.azurewebsites.net/BOClassByName/{ExactBianName}`

If no strong match exists, do not fabricate a BIAN URL. Leave the reference empty or
use `# TODO:` with candidate options for user confirmation.

### Query Expansion Heuristics

If step 1 returns weak results, retry `nameLike` with variants before concluding no match:

- singular/plural: `Customer` / `Customers`
- role vs subject: `Customer` / `PartyRole`
- synonyms: `Person`, `Individual`, `LegalEntity`, `Organisation`, `Company`
- finance terms: `Payment`, `Transaction`, `Agreement`, `Account`, `Location`

Record which variant produced the selected match.

### Finding BIAN Enumerations for Attributes

Do not begin from bulk enumeration endpoints (`/BOEnumerationsBasic`) because payload size is too large.

Use this sequence instead:

1. Resolve the class first:
   - `GET /BOClassByName/{ExactBianName}/BIAN/13.0.0`
2. Inspect class attributes in the response (`attributeList`) and identify enum-backed attributes
   (for example attributes referencing `boEnumeration`, enumeration names, or enum-type markers).
3. Resolve each required enumeration by exact name:
   - `GET /BOEnumerationByName/{name}/BIAN/13.0.0`
4. Use the returned enumeration details to validate MD-DDL enum naming and allowed values.

If an attribute appears enum-like but no enumeration name can be resolved confidently,
record `# TODO:` and ask the user to confirm instead of guessing.

### Mapping Quality Decision

Use this decision table after candidate resolution:

Signal | Action
--- | ---
Concept name and definition match closely | Reference directly; no qualification required
Concept is a specialisation of a BIAN object | Reference the parent and note the specialisation in description
Concept partially overlaps a BIAN object | Reference with explicit qualification (`Partial alignment`) and state the gap
No convincing BIAN counterpart | Do not force a reference; leave reference empty or add `# TODO:`

### Material Difference Note (Required for Partial Fit)

If the selected BIAN class is not an exact fit, explicitly note the semantic difference:

"In BIAN BOM, '[BIAN Class]' means [BIAN meaning]. In this model, '[Model Concept]' also includes [extension or constraint]."

Do not hide semantic drift by using an unqualified reference.

### Required Output for Ambiguous Matches

When more than one candidate remains plausible, provide a short disambiguation set before finalizing:

- Search term used
- Candidate options (2-3 max)
- Why each may fit
- Proposed selection and rationale

If user confirmation is needed, pause and ask.

### Common BIAN BOM Mappings

Business Term | BIAN BOM Object | URL Pattern
------------- | --------------- | -----------
Customer, Merchant, Creditor | PartyRole | /BOClassByName/PartyRole
Individual, Person | Person (or Individual in older versions) | /BOClassByName/{ExactBianName}
Company, Organization | LegalEntity | /BOClassByName/LegalEntity
Party (abstract) | Party | /BOClassByName/Party
Account | Account | /BOClassByName/Account
Loan | LoanAgreement | /BOClassByName/LoanAgreement
Payment, Transaction | Payment | /BOClassByName/Payment
Branch, Location | Location | /BOClassByName/Location
Currency | Currency | /BOClassByName/Currency

Important: treat this table as a starting hypothesis only. Always confirm with
`BOClassesBasicByNameLike` and then resolve by exact class name.

### BIAN vs Business Terminology

BIAN Term | Common Business Term | Notes
--------- | ------------------- | -----
Legal Entity | Company, Organization | Use business term in MD-DDL, note BIAN term
Agreement | Contract | Use business term, reference BIAN
Payment | Transaction | Context dependent
Party Role | Customer Role, User Role | BIAN abstraction pattern

## BIAN Party / Party Role Pattern

**Critical Pattern**: BIAN uses an abstract Party and Party Role pattern.

**Party** = The who (Person or Legal Entity)
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
-------------- | ------- | --------------
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
- Use version-scoped lookup endpoints during discovery: `/.../BIAN/13.0.0`
- If version-specific behavior matters, note in references: `BIAN 13.0 - Party Role`

## Execution and Output Rules

Use these rules and templates when writing MD-DDL references.

- Never output a BIAN URL that was not resolved from an API result.
- Never select the first fuzzy hit without checking semantic fit.
- When 2 or more plausible classes remain, show 2-3 options and ask the user to confirm.
- For unresolved mappings, use explicit `# TODO: No BIAN BOM mapping confirmed yet`.
- Never call bulk BO enumeration listing endpoints as a first step for mapping; derive enum names from resolved class attributes, then resolve by `/BOEnumerationByName/{name}`.

### Reference Formatting in MD-DDL

Use these patterns in domain summary tables and entity detail descriptions.

### Exact Match

```markdown
| [Customer](entities/customer.md#customer) | [Party Role](entities/party-role.md#party-role) | A Party with an active product relationship. | [BIAN BOM - PartyRole](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/PartyRole) |
```

### Partial Alignment

```markdown
| [Payment Transaction](entities/payment-transaction.md#payment-transaction) |  | A movement of funds between parties. Partial alignment to BIAN Payment: this model includes internal fraud-case enrichment fields not in BIAN. | [BIAN BOM - Payment](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/Payment) |
```

### No Confirmed Mapping

```markdown
| [Internal Risk Flag](entities/internal-risk-flag.md#internal-risk-flag) |  | Internal concept used for institution-specific monitoring thresholds. | # TODO: No BIAN BOM mapping confirmed yet |
```

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

### Person
- specializes: [Party](entities/party.md)
- references: [BIAN BOM - Person](url)

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

- [BIAN Website](https://bian.org)
- [BIAN Model API](https://bian-modelapi-v4.azurewebsites.net/)
- [BIAN Documentation](https://bian.org/deliverables/)
