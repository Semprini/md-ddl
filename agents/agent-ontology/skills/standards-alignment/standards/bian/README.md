# BIAN (Banking Industry Architecture Network) — Standard Guidance

## Overview

BIAN v13.0.0 provides a standardized framework for banking with:

- **330+ Service Domains** — functional capabilities (e.g., "Customer Agreement", "Current Account")
- **1,500+ Business Object (BO) Classes** — semantic entities (e.g., Party, Account, Agreement)
- **550+ BO Enumerations** — standardized value sets (e.g., `Partytypevalues`, `Accounttypevalues`)
- **Semantic APIs** — REST APIs for each service domain

**For MD-DDL modelling, reference the BO Classes (Business Objects), NOT Service Domains.**

## Local Reference Files

This directory contains pre-extracted reference data from BIAN v13.0.0.
Use these files for local lookup before falling back to the API.

File | Contents | Use for
--- | --- | ---
[bo-classes.md](bo-classes.md) | All ~1,528 BO classes (name, description, status) | Finding candidate BIAN class names
[bo-classes-detail.md](bo-classes-detail.md) | ~45 core classes with inheritance and full attributes | Attribute-level mapping and inheritance trees
[hierarchy.md](hierarchy.md) | Business Areas → Domains → Service Domains | Understanding where a concept sits in BIAN's taxonomy
[enumerations.md](enumerations.md) | All ~550 BO enumerations (name, description) | Mapping MD-DDL enums to BIAN counterparts

## BIAN BOM Structure

BIAN BOM organises business objects hierarchically:

```text
Party (abstract)
├─ Person
└─ Legal Entity

Party Role (abstract — involvement in business activity)
├─ Customer
├─ Merchant
└─ etc.

Agreement (abstract)
├─ Customer Agreement
├─ Loan Agreement
└─ etc.
```

## Finding BIAN Business Objects

### Deterministic Lookup Process (No Guessing)

Use this tiered approach — local reference files first, API fallback second.

#### Step 1 — Search the local BO class index

Open [bo-classes.md](bo-classes.md) and search for the entity name or close variants.
This replaces the API call to `BOClassesBasicByNameLike`.

Build a short candidate list (max 3–5) based on:

- Exact or close name match
- Description alignment with user intent
- Whether the concept is an abstract base vs a specialisation

#### Step 2 — Check the core class detail

If the candidate is in [bo-classes-detail.md](bo-classes-detail.md), use the local
data for inheritance (`Extends`), abstraction flag, and attribute tables.
This replaces the API call to `BOClassByName` for the ~45 most common classes.

#### Step 3 — Check the taxonomy hierarchy

Open [hierarchy.md](hierarchy.md) to understand which Business Area and Business Domain
own the concept. This provides context for whether the class is in the right
functional area.

#### Step 4 — API fallback for non-cached classes

For classes NOT in the detail cache, resolve via the API:

- `GET https://bian-modelapi-v4.azurewebsites.net/BOClassByName/{ExactBianName}/BIAN/13.0.0`

#### Step 5 — Resolve enumerations

For enum mapping, first search [enumerations.md](enumerations.md) for a name match.
If found, decide whether the BIAN enumeration aligns with the MD-DDL enum values.

For enumeration values/literals not covered in the local file, resolve by exact name:

- `GET https://bian-modelapi-v4.azurewebsites.net/BOEnumerationByName/{name}/BIAN/13.0.0`

Do not begin from bulk enumeration endpoints — always derive enum names from
resolved class attributes first.

### Query Expansion Heuristics

If Step 1 returns weak results, retry search with variants before concluding no match:

- Singular/plural: `Customer` / `Customers`
- Role vs subject: `Customer` / `PartyRole`
- Synonyms: `Person`, `Individual`, `LegalEntity`, `Organisation`, `Company`
- Finance terms: `Payment`, `Transaction`, `Agreement`, `Account`, `Location`

Record which variant produced the selected match.

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

> "In BIAN BOM, '[BIAN Class]' means [BIAN meaning]. In this model, '[Model Concept]' also includes [extension or constraint]."

Do not hide semantic drift by using an unqualified reference.

### Required Output for Ambiguous Matches

When more than one candidate remains plausible, provide a short disambiguation set before finalising:

- Search term used
- Candidate options (2–3 max)
- Why each may fit
- Proposed selection and rationale

If user confirmation is needed, pause and ask.

## Common BIAN BOM Mappings

Business Term | BIAN BOM Object | URL Pattern
--- | --- | ---
Customer, Merchant, Creditor | PartyRole | /BOClassByName/PartyRole
Individual, Person | Person | /BOClassByName/Person
Company, Organisation | LegalEntity (see `LegalEntityDirectoryEntry` in BO classes) | /BOClassByName/LegalEntity
Party (abstract) | Party | /BOClassByName/Party
Account | Account | /BOClassByName/Account
Loan | LoanAgreement | /BOClassByName/LoanAgreement
Payment, Transaction | Transaction | /BOClassByName/Transaction
Branch, Location | Location | /BOClassByName/Location

Treat this table as a starting hypothesis only. Always confirm against the local
[bo-classes.md](bo-classes.md) index and then resolve by exact class name.

## BIAN vs Business Terminology

BIAN Term | Common Business Term | Notes
--- | --- | ---
Legal Entity | Company, Organisation | Use business term in MD-DDL, note BIAN term
Agreement | Contract | Use business term, reference BIAN
Party Role | Customer Role, User Role | BIAN abstraction pattern

## BIAN Party / Party Role Pattern

**Critical Pattern**: BIAN uses an abstract Party and Party Role pattern.

**Party** = The who (Person or Legal Entity)
**Party Role** = The what they do (Customer, Merchant, Creditor, etc.)

### When to Use BIAN Party Role Pattern

Ask user: "Are Customer, Merchant, etc. managed by different teams with different requirements?"

**If YES**: Make each a first-class entity specialising Party Role

```markdown
### Customer
A party that holds accounts or uses products/services.
- specializes: [Party Role](entities/party-role.md)
- references: [BIAN BOM - PartyRole](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/PartyRole)
```

**If NO**: Use a single Party Role entity with Role Type enum

## BIAN Service Domains vs BOM

**Don't confuse these**:

BIAN Component | Purpose | Use in MD-DDL
--- | --- | ---
Service Domain | Functional capability (e.g., "Party Reference Data Directory") | Do not reference in MD-DDL
Business Object Model (BOM) | Semantic entities (e.g., "Party", "PartyRole") | Reference in MD-DDL
Semantic API | REST API for service domain | Do not reference in MD-DDL

**Example — WRONG**:

```markdown
- references: [BIAN - Party Reference Data Directory](https://bian.org/semantic-apis/party-reference-data-directory/)
```

**Example — RIGHT**:

```markdown
- references: [BIAN BOM - Party](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/Party)
```

## BIAN Versions

Current release: **v13.0.0**

When referencing:

- Use version-agnostic URL in MD-DDL output: `/BOClassByName/{Object}`
- Use version-scoped lookup endpoints during discovery: `/.../BIAN/13.0.0`
- If version-specific behaviour matters, note in references: `BIAN 13.0 — Party Role`

## Execution and Output Rules

- Never output a BIAN URL that was not resolved from the local index or an API result.
- Never select the first fuzzy hit without checking semantic fit.
- When 2 or more plausible classes remain, show 2–3 options and ask the user to confirm.
- For unresolved mappings, use explicit `# TODO: No BIAN BOM mapping confirmed yet`.

### Reference Formatting in MD-DDL

### Exact Match

```markdown
| [Customer](entities/customer.md#customer) | [Party Role](entities/party-role.md#party-role) | A Party with an active product relationship. | [BIAN BOM - PartyRole](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/PartyRole) |
```

### Partial Alignment

```markdown
| [Payment Transaction](entities/payment-transaction.md#payment-transaction) |  | A movement of funds between parties. Partial alignment to BIAN Transaction: this model includes internal fraud-case enrichment fields not in BIAN. | [BIAN BOM - Transaction](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/Transaction) |
```

### No Confirmed Mapping

```markdown
| [Internal Risk Flag](entities/internal-risk-flag.md#internal-risk-flag) |  | Internal concept used for institution-specific monitoring thresholds. | # TODO: No BIAN BOM mapping confirmed yet |
```

## BIAN + ISO 20022

For payment/transaction entities, reference both standards where applicable:

```markdown
### Payment Transaction
A financial transaction involving movement of funds.
- references: [BIAN BOM - Transaction](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/Transaction)
- references: [ISO 20022 - Payment](url)
```

BIAN provides the business object model, ISO 20022 provides the message format.

## Common BIAN Patterns in MD-DDL

### Pattern 1: Party Abstraction

```markdown
### Party
- detail: [Party](entities/party.md)
- references: [BIAN BOM - Party](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/Party)

### Person
- specializes: [Party](entities/party.md)
- references: [BIAN BOM - Person](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/Person)
```

### Pattern 2: Party Role Specialisation

```markdown
### Party Role
- detail: [Party Role](entities/party-role.md)
- references: [BIAN BOM - PartyRole](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/PartyRole)

### Customer
- specializes: [Party Role](entities/party-role.md)
- references: [BIAN BOM - PartyRole](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/PartyRole)
```

### Pattern 3: Agreement / Contract

```markdown
### Contract
- detail: [Contract](entities/contract.md)
- references: [BIAN BOM - Agreement](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/Agreement)

### Loan Contract
- specializes: [Contract](entities/contract.md)
- references: [BIAN BOM - LoanAgreement](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/LoanAgreement)
```

## When BIAN Doesn't Have a Concept

If modelling a concept not in BIAN (e.g., domain-specific internal concept):

- Omit BIAN reference
- Note in detail file: "No BIAN BOM mapping identified — internal business concept"
- Reference other standards if applicable (ISO 20022, Basel, etc.)

## Regenerating Reference Files

The reference files in this directory are generated from the raw BIAN v13 JSON
data stored in `industry_standards/bian/v13/`. To regenerate after a BIAN version update:

```shell
python industry_standards/bian/extract-references.py                  # local JSON only
python industry_standards/bian/extract-references.py --fetch-classes   # also fetch core class attributes via API
```

Cached class data is stored in `industry_standards/bian/v13/cached-classes/` and will be reused on
subsequent runs. Delete the cache directory to force re-fetch.

## Resources

- [BIAN Website](https://bian.org)
- [BIAN Model API](https://bian-modelapi-v4.azurewebsites.net/)
- [BIAN Documentation](https://bian.org/deliverables/)
