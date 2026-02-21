---
name: domain-discovery
description: Research and scope a MD-DDL domain by identifying business concepts, applicable standards, and the semantic modeling strategy (Canonical vs. Domain-Driven). Use when starting a new domain model or when user says "model this domain".
---

# Domain Discovery Process

## Step 1: Understand Context
Ask user:
1. **What business problem are we solving?**
2. **What industry/domain are you in?** (Banking, Insurance, Telecom, Healthcare, etc.)
3. **What regulatory jurisdictions apply?** (Australia, NZ, EU, US, etc.)
4. **Are there specific industry standards to align with?**

## Step 2: Determine Modeling Strategy
Before modeling, determine the boundary strategy to manage semantic complexity.

**Summarized Strategy Options:**
- **Single Canonical**: One definition (e.g., "Customer") for the whole enterprise. Best for small orgs or universal concepts where consensus is easy.
- **Domain-Driven**: Context-specific definitions (e.g., "Customer" in Sales vs. "Customer" in Support). Best for independent evolution and complex data flows.
- **Hybrid (Recommended)**: Canonical for reference data (Currencies, Countries); Domain-Driven for core entities (Orders, Products).

**Ask user:** "Should we aim for a single enterprise-wide canonical definition for core entities, or allow for domain-specific definitions to support independent evolution?"
- *For deeper logic on this choice, refer to: [Domain Boundaries Details](./domain-boundaries.md)*

## Step 3: Load Relevant Standards
Based on user's industry, load ONLY the applicable standards guidance:

Industry | Load Standards
---------|---------------
Banking/Financial Services | [BIAN](../external-standard-mapping/standards/bian.md), [ISO 20022](../external-standard-mapping/standards/iso20022.md)
Insurance | ACORD TBD
Telecommunications | TM Forum TBD
Healthcare | FHIR TBD

## Step 4: Load Relevant Regulators
Based on user's jurisdiction, load ONLY the applicable regulatory guidance:

Jurisdiction | Load Regulators
-------------|----------------
Australia/NZ Banking | [APRA](../regulatory-compliance/regulators/apra.md), [RBNZ](../regulatory-compliance/regulators/rbnz.md), [Basel](../regulatory-compliance/regulators/basel.md), FATF TBD
EU | GDPR TBD, [Basel](../regulatory-compliance/regulators/basel.md)
US Banking | FDIC TBD, OCC TBD, [Basel](../regulatory-compliance/regulators/basel.md)

## Step 5: Identify Core Concepts
Identify key business concepts. If **Domain-Driven** was chosen in Step 2, explicitly define the **Context Boundaries** (e.g., "Customer as defined within the Lending Domain").

- If BIAN loaded → Search for BIAN Business Objects
- If ACORD loaded → Search for ACORD data models

## Step 6: Propose Domain Structure
Create `domain.md` with:
- Metadata block (include regulatory scope and **Modeling Strategy**).
- Entity summaries with standard references.
- **Boundary Map**: If using Domain-Driven, describe how this domain interacts with others (Cross-domain lineage).

## Step 7: Validate with User

"Does this capture the right concepts, scope, and **boundary strategy** for your {industry} domain?"
