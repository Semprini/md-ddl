---
name: domain-discovery
description: Research and scope a new MD-DDL domain by identifying business concepts and applicable standards. Use when starting a new domain model or when user says "model this domain" or "create a data model for X"
---

# Domain Discovery Process

## Step 1: Understand Context

Ask user:
1. **What business problem are we solving?**
2. **What industry/domain are you in?** (Banking, Insurance, Telecom, Healthcare, etc.)
3. **What regulatory jurisdictions apply?** (Australia, NZ, EU, US, etc.)
4. **Are there specific industry standards to align with?**

## Step 2: Load Relevant Standards

Based on user's industry, load ONLY the applicable standards guidance:

Industry | Load Standards
---------|---------------
Banking/Financial Services | [BIAN](../external-standard-mapping/standards/bian.md), [ISO 20022](../external-standard-mapping/standards/iso20022.md)
Insurance | [ACORD](../external-standard-mapping/standards/acord.md)
Telecommunications | [TM Forum](../external-standard-mapping/standards/tm-forum.md)
Healthcare | [FHIR](../external-standard-mapping/standards/fhir.md)

**Example**:
```
User: "We're building a financial crime model for a bank in New Zealand"
AI: Loading BIAN and ISO 20022 standards...
```

## Step 3: Load Relevant Regulators

Based on user's jurisdiction, load ONLY the applicable regulatory guidance:

Jurisdiction | Load Regulators
-------------|----------------
Australia/NZ Banking | [APRA](../regulatory-compliance/regulators/apra.md), [RBNZ](../regulatory-compliance/regulators/rbnz.md), [Basel](../regulatory-compliance/regulators/basel.md), [FATF](../regulatory-compliance/regulators/fatf.md)
EU | [GDPR](../regulatory-compliance/regulators/gdpr.md), [Basel](../regulatory-compliance/regulators/basel.md)
US Banking | [FDIC](../regulatory-compliance/regulators/fdic.md), [OCC](../regulatory-compliance/regulators/occ.md), [Basel](../regulatory-compliance/regulators/basel.md)
Global AML | [FATF](../regulatory-compliance/regulators/fatf.md)

**Example**:
```
User: "We need to comply with APRA and RBNZ requirements"
AI: Loading APRA, RBNZ, Basel, and FATF regulatory guidance...
```

## Step 4: Identify Core Concepts

Ask user about key business concepts to model.

Use loaded standards to find mappings:
- If BIAN loaded → Search for BIAN Business Objects
- If ACORD loaded → Search for ACORD data models
- If TM Forum loaded → Search for SID entities

## Step 5: Propose Domain Structure

Create domain.md with:
- Metadata block (include regulatory scope from loaded regulators)
- Entity summaries with standard references
- Governance metadata aligned with regulatory requirements

## Step 6: Validate with User

Present domain summary and ask:
"Does this capture the right concepts and scope for your {industry} domain in {jurisdiction}?"

Wait for approval before creating detail files.