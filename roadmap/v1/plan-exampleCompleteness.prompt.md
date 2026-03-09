# Plan: Example Completeness

## TL;DR

Bring the MD-DDL examples to v1.0 quality by fixing spec drift in Simple Customer, filling feature-coverage gaps in Financial Crime, and adding a new Healthcare (FHIR-aligned) domain that exercises spec features Financial Crime does not. Simple Customer stays minimal (2-file intro). Financial Crime adds missing high-value patterns. Healthcare is a contrasting full-quality domain that demonstrates FHIR standards alignment and features absent from Financial Crime.

---

## Phase 1: Audit & Fix Existing Examples

Fix what exists before adding anything new.

### Step 1: Audit Simple Customer for spec drift

Compare `examples/Simple Customer/domain.md` and `details.md` against the current spec (v0.9.0). Check:
- Domain metadata schema matches `2-Domains.md` (version, owner, steward, tags, governance defaults)
- Entity YAML matches `3-Entities.md` (mutability, temporal, existence, constraints)
- Enum format matches `4-Enumerations.md` (dictionary vs simple list)
- Relationship YAML matches `5-Relationships.md` (granularity, constraints)
- Event YAML matches `6-Events.md` (actor, entity, emitted_on, governance)
- Governance metadata keys match spec vocabulary

Fix any drift in-place. Do not expand scope — Simple Customer stays as a 2-file intro. Its purpose is "hello world for MD-DDL."

### Step 2: Audit Financial Crime for spec drift

Same checks as Step 1, applied to all 20+ files in `examples/Financial Crime/`. Priority files:
- `domain.md` — domain metadata schema
- `entities/*.md` — entity YAML, classDiagram, attributes
- `events/*.md` — event YAML structure
- `products/*.md` — product YAML (governance, SLA, masking)

Fix any drift in-place. Do not add new features in this step — that's Phase 2.

---

## Phase 2: Fill Financial Crime Feature Gaps

These are spec features that exist but are not demonstrated anywhere. Add them to Financial Crime where they fit naturally.

### Step 3: Add group and period relationship granularity

Currently all 16+ relationships use `granularity: atomic`. Add at least:
- One `group` relationship — e.g., Account → Transaction (monthly summary) or Branch → Transaction (grouped by branch)
- One `period` relationship — e.g., Party Role → Customer (point-in-time role assignment with effective dates)

Update the relevant entity detail files and the domain diagram.

**Relevant files:**
- `examples/Financial Crime/domain.md` — domain diagram relationships table
- Entity files that receive the new relationships

### Step 4: Add bitemporal and diverse mutability patterns

Currently only `valid_time` and implied `slowly_changing` are shown. Add:
- `bitemporal` temporal tracking on at least one entity — Party Role is a natural fit (role assignment valid in business time + recorded in system time)
- `append_only` mutability on Transaction (transactions are immutable once recorded)
- `reference` mutability on Currency, Exchange Rate (externally managed reference data)
- `frequently_changing` mutability on Account (balance updates)

**Relevant files:**
- `examples/Financial Crime/entities/party_role.md` — add bitemporal
- `examples/Financial Crime/entities/transaction.md` — set append_only
- `examples/Financial Crime/entities/currency.md` — set reference
- `examples/Financial Crime/entities/account.md` — set frequently_changing

### Step 5: Add SLA declarations and lifecycle state to products

Currently products declare `status: Production` but don't show lifecycle transitions or SLA. Add:
- SLA block to `products/analytics.md` (already has it — ✓ verify it matches spec format)
- SLA block to `products/canonical.md` and `products/source-feeds.md`
- Add a `Deprecated` product to demonstrate lifecycle transitions — e.g., a legacy "Party Risk Report" product marked Deprecated with deprecation metadata

**Relevant files:**
- `examples/Financial Crime/products/canonical.md`
- `examples/Financial Crime/products/source-feeds.md`
- New file: `examples/Financial Crime/products/party-risk-report-legacy.md` (Deprecated product)

### Step 6: Add event payload structure detail

Currently events declare actor/entity/trigger but payload schemas are minimal. Flesh out at least 2 events with full payload attributes matching `6-Events.md` format:
- `events/transaction-executed.md` — add payload with amount, currency, timestamp, risk_score fields
- `events/high-risk-transaction-detected.md` — add payload with alert_type, severity, detection_method, threshold_breached

### Step 7: Add dictionary-style enum with external standard reference

Currently all enums use the dictionary format but none reference external standards. Add at least one enum that maps to an external standard:
- Currency Code enum aligned to ISO 4217
- Or Country Code enum aligned to ISO 3166

Update `examples/Financial Crime/enums.md` with the new enum.

---

## Phase 3: New Healthcare Domain (FHIR-aligned)

A second full-quality domain that exercises features Financial Crime does not, using the existing FHIR R4 reference data in `references/industry_standards/fhir/r4/`.

### Step 8: Create Healthcare domain structure

```
examples/Healthcare/
  domain.md
  enums.md
  entities/
  events/
  sources/
  products/
```

### Step 9: Write domain.md with FHIR standards alignment

Core entities to model (8–12 entities, contrasting with Financial Crime's party/transaction pattern):

Entity | FHIR Resource | Demonstrates
--- | --- | ---
Patient | Patient | Standards alignment mapping
Encounter | Encounter | Period-based entity (admission → discharge)
Observation | Observation | Append-only, high-volume
Condition | Condition | Clinical terminology alignment
Procedure | Procedure | Event-driven with actor model
Practitioner | Practitioner | Independent entity, reference mutability
PractitionerRole | PractitionerRole | Role pattern (parallels Party Role but from FHIR)
Organization | Organization | Hierarchical reference data
Location | Location | Spatial reference entity
MedicationRequest | MedicationRequest | Complex dependent entity with governance
CarePlan | CarePlan | Group-granularity relationships (plan → activities)
Appointment | Appointment | Period-granularity relationships (scheduled vs actual)

**Spec features to exercise that Financial Crime does not:**
- `transaction_time` temporal tracking (Observation — system time matters for clinical records)
- `bitemporal` on at least one entity (CarePlan — both clinical validity and system recording matter)
- More `period` and `group` granularity relationships
- Standards alignment skill demonstration (FHIR R4 mapping using `references/industry_standards/fhir/r4/profiles-resources.json`)
- Enum with external standard reference (ICD-10, SNOMED CT, LOINC codes)
- Different governance profile (HIPAA-driven vs AML-driven)

### Step 10: Write entity detail files

One `.md` per entity in `entities/`. Each must include:
- Full YAML block with mutability, temporal, existence, governance
- classDiagram with attributes and relationships
- Governance metadata relevant to healthcare (HIPAA classification, PHI marking, retention laws)

### Step 11: Write source systems

Add 1–2 source systems to demonstrate source mapping in a different domain context:
- An EHR system (e.g., Epic-like or generic "Hospital EHR") with transform files
- A lab system (e.g., "Lab Information System") for Observation feeds

This exercises the same source mapping patterns as Financial Crime but in a healthcare context, reinforcing that the pattern is domain-agnostic.

### Step 12: Write data products

At least 2 products:
- A domain-aligned canonical product (e.g., "Clinical Patient Record")
- A consumer-aligned product for analytics (e.g., "Clinical Outcomes Dashboard") — this will also serve the Cross-Domain References plan

### Step 13: Write events

At least 3–4 events exercising payload detail:
- Patient Admitted (Encounter-driven)
- Observation Recorded (high-volume, append-only)
- Medication Prescribed (clinical workflow trigger)
- Care Plan Updated (versioned update event)

### Step 14: Generate physical artifacts

Run Agent Artifact to generate at least:
- Knowledge-graph (Cypher) — Financial Crime only shows dimensional + 3NF
- Wide-column — Financial Crime only shows it in product declaration, not generated output

Place in `examples/Healthcare/generated/`.

---

## Phase 4: Verification

### Step 15: Feature coverage matrix

Create a coverage matrix (can be a markdown table in `examples/README.md`) showing which spec feature is exercised by which example:

Feature | Simple Customer | Financial Crime | Healthcare
--- | --- | --- | ---
Entity inheritance | ✓ | ✓ | ✓
Bitemporal | | ✓ (Phase 2) | ✓
Append-only | | ✓ (Phase 2) | ✓
Group granularity | | ✓ (Phase 2) | ✓
Period granularity | | ✓ (Phase 2) | ✓
Standards alignment | | | ✓
Knowledge graph gen | | | ✓
Wide-column gen | | | ✓
Cross-domain product | | ✓ (Cross-Domain plan) | ✓ (Cross-Domain plan)
SLA declarations | | ✓ (Phase 2) | ✓
Lifecycle transitions | | ✓ (Phase 2) |
Source transforms | | ✓ | ✓
Dictionary enums | ✓ | ✓ | ✓
External standard enum | | ✓ (Phase 2) | ✓

### Step 16: Agent walkthrough validation

Run each agent against the new Healthcare domain to validate:
- Agent Ontology can read and review the domain model
- Agent Artifact can generate physical artifacts from it
- Agent Data Product can work with the product declarations
- Agent Guide can use it as a teaching example

---

## Relevant Files

- `examples/Simple Customer/domain.md` — audit for spec drift (Step 1)
- `examples/Simple Customer/details.md` — audit for spec drift (Step 1)
- `examples/Financial Crime/domain.md` — audit + add relationships (Steps 2, 3)
- `examples/Financial Crime/entities/*.md` — add mutability/temporal patterns (Step 4)
- `examples/Financial Crime/products/*.md` — add SLA/lifecycle (Step 5)
- `examples/Financial Crime/events/*.md` — flesh out payloads (Step 6)
- `examples/Financial Crime/enums.md` — add external standard enum (Step 7)
- `examples/Healthcare/` — new domain (Steps 8–14, all new files)
- `examples/README.md` — new coverage matrix (Step 15)
- `references/industry_standards/fhir/r4/profiles-resources.json` — FHIR reference data for standards alignment
- `md-ddl-specification/3-Entities.md` — reference for mutability/temporal vocab
- `md-ddl-specification/5-Relationships.md` — reference for granularity vocab
- `md-ddl-specification/6-Events.md` — reference for event payload structure
- `md-ddl-specification/9-Data-Products.md` — reference for SLA/lifecycle/cross-domain

## Verification

1. Run diff of Simple Customer against spec section schemas — confirm all YAML keys are current vocabulary
2. Run diff of Financial Crime entity YAML against spec section 3 — confirm mutability + temporal values added correctly
3. Validate Healthcare domain.md Mermaid diagram renders correctly (paste into Mermaid live editor or use VS Code preview)
4. Validate all Healthcare entity classDiagrams render correctly
5. Confirm each row in the coverage matrix (Step 15) is exercised by at least one example file — grep for the YAML key in each cited example
6. Verify generated physical artifacts in `examples/Healthcare/generated/` are syntactically valid (Cypher syntax check, schema validation)
7. Confirm agent-guide worked-examples skill references are still accurate after example changes

## Decisions

- Simple Customer stays minimal (2 files) — its role is onboarding, not comprehensive feature demonstration
- Healthcare chosen as third domain because it contrasts with Financial Crime (clinical vs financial), has existing FHIR R4 reference data in the repo, and exercises different governance (HIPAA vs AML)
- Financial Crime fills gaps in-place rather than via a separate example — it's already 80% complete and is the established reference
- Knowledge graph and wide-column generation demonstrated in Healthcare since Financial Crime already covers dimensional + 3NF
- Deprecated product added to Financial Crime (not Healthcare) because lifecycle transitions are most meaningful when there's already an established product set

## Dependencies

- Steps 1–2 are independent and can run in parallel
- Steps 3–7 depend on Step 2 (audit first, then add features)
- Steps 3–7 are independent of each other and can run in parallel
- Steps 8–13 are independent of Phase 1 and 2 — can run in parallel with them
- Step 14 depends on Steps 8–13 (needs model to generate from)
- Steps 15–16 depend on all prior steps

## Further Considerations

1. **Healthcare governance profile:** Should we model HIPAA compliance metadata specifically, or keep governance generic with healthcare-flavoured values? Recommendation: Use HIPAA-specific values (`regulatory_scope: [HIPAA]`, `phi: true`) to contrast with Financial Crime's AML/GDPR profile — this strengthens the governance demonstration.

2. **FHIR mapping depth:** Should Healthcare entities include explicit FHIR resource URLs in metadata, or just conceptual alignment? Recommendation: Include a `standard_alignment` metadata field pointing to the FHIR resource type — this tests whether the standards-alignment skill works with real mappings.
