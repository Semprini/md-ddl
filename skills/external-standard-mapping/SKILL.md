---
name: external-standard-mapping
description: Find and reference external industry standards when modeling a domain. Use when user mentions a specific standard or when modeling an industry domain (banking, telecom, insurance, healthcare).
---

# External Standard Mapping

## Identify Relevant Standards

Ask user: "What industry are you in and are there specific standards we should align to?"

Common standards by industry:

Industry | Standards | Standard Files to Load
---------|-----------|----------------------
Banking/Financial Services | BIAN BOM, ISO 20022, FIBO | [bian.md](standards/bian.md), [iso20022.md](standards/iso20022.md), [fibo.md](standards/fibo.md)
Insurance | ACORD, IAA | [acord.md](standards/acord.md)
Telecommunications | TM Forum (SID, Frameworx) | [tm-forum.md](standards/tm-forum.md)
Healthcare | FHIR, HL7 | [fhir.md](standards/fhir.md)
Retail | GS1 | [gs1.md](standards/gs1.md)
Supply Chain | GS1, DCSA | [gs1.md](standards/gs1.md), [dcsa.md](standards/dcsa.md)

## Load Only Relevant Standards

**Critical**: Only load standard guidance files that apply to the user's industry.

**Example**:
```
User: "We're modeling financial crime for a bank using BIAN"
AI: Loading standards/bian.md...
AI: (Does NOT load acord.md, tm-forum.md, fhir.md, etc.)
```

**If user mentions multiple standards**:
```
User: "We need BIAN for business objects and ISO 20022 for payment messages"
AI: Loading standards/bian.md and standards/iso20022.md...
```

## Search Process

Once relevant standard(s) loaded:

1. User mentions concept: "We need to model Customer"
2. Consult loaded standard guidance for mapping
3. Find concept definition URL from standard guidance
4. Validate URL exists
5. Add to references in summary

**Example with BIAN loaded**:
```
User: "Model Customer entity"
AI: Checks standards/bian.md → finds PartyRole mapping
AI: Uses URL: https://bian-modelapi-v4.azurewebsites.net/BOClassByName/PartyRole
AI: Validates URL
AI: Adds reference to summary
```

## Reference Syntax

Generic pattern:
```markdown
- references: [{Standard Name} - {Concept}](url)
```

Examples:
```markdown
- references: [BIAN BOM - Party Role](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/PartyRole)
- references: [ACORD - Policy](https://www.acord.org/standards/...)
- references: [TM Forum SID - Customer](https://www.tmforum.org/resources/standard/...)
- references: [FHIR - Patient](https://hl7.org/fhir/patient.html)
```

## When Standard Uses Different Terminology

Note in summary:
```markdown
### Policy Holder
An individual or organization that owns an insurance policy. Also referred to as Insured Party in ACORD.
- references: [ACORD - Insured Party](url)
```

## Multiple Standards for Same Concept

A single concept can reference multiple standards:

```markdown
### Payment Transaction
A financial transaction involving movement of funds.
- references: [BIAN BOM - Payment](https://bian-modelapi-v4.azurewebsites.net/BOClassByName/Payment)
- references: [ISO 20022 - Payment](https://www.iso20022.org/payment-initiation)
```

This is common when:
- BIAN provides business object semantics
- ISO 20022 provides message format
- FIBO provides ontological definitions

## When No Standard Exists

If concept is domain-specific with no standard mapping:
- Omit references line
- Focus on clear business description
- Document in detail file why no standard applies

## Loading Additional Standards Mid-Modeling

If during modeling you discover need for another standard:

**Ask user**:
"I notice you're modeling {concept}. Should we also align with {additional standard}?"

**Example**:
```
User modeling payments in banking domain (BIAN loaded)
AI: "I notice you're modeling payment messages. Should we also align with ISO 20022?"
User: "Yes"
AI: Loading standards/iso20022.md...
```

**Only load when**:
- User explicitly requests
- Concept clearly belongs to that standard's domain
- User confirms the additional standard is relevant

## Finding Concept URLs

**Do NOT manually search** - use the loaded standard guidance files.

Each standard guidance file (e.g., standards/bian.md) contains:
- URL patterns for that standard
- Common concept mappings
- How to construct URLs
- Examples

**Process**:
1. Load relevant standard guidance file(s)
2. Consult guidance for concept mapping
3. Use URL pattern from guidance
4. Validate URL exists

**Example**:
```
AI loads standards/bian.md
User: "Model Customer"
AI consults bian.md → finds Customer maps to PartyRole
AI uses URL pattern from bian.md: /BOClassByName/PartyRole
AI validates URL
```

## Validation

Before including reference:
1. Fetch URL to confirm it exists
2. Verify concept name matches
3. If URL returns error, search for updated location
4. If no URL found, note in detail file: "No standard mapping identified"