# Plan: BIAN v13 to v14 Migration

## TL;DR

Migrate MD-DDL BIAN alignment from v13 to v14 using a controlled dual-track approach:

- Keep v13 operational for production safety.
- Add v14 snapshots and generated references side-by-side.
- Gate cutover on successful access to the official v14 API and data completeness checks.

Your role is the critical dependency: secure official v14 API access credentials and access method. Engineering then executes ingestion, generation, agent updates, and cutover validation.

---

## Current State

- Extractor is version-aware and supports v13/v14 source/output paths.
- Standards guidance is already version-aware and defaults to v14 for new work.
- Snapshot downloader exists: `references/industry_standards/bian/download-snapshots.ps1`.
- v8 endpoint (`https://bian-modelapi-v8.azurewebsites.net`) is reachable but returns `401 Unauthorized` without credentials.
- v4 endpoint provides empty/insufficient v14 list data.

This means the migration is technically prepared, but blocked on official API access.

---

## Migration Strategy

Use a staged migration with explicit exit criteria:

1. Access enablement
2. Data acquisition
3. Reference generation
4. Agent behavior hardening
5. Validation and pilot
6. Controlled cutover
7. v13 deprecation decision

No hard cutover until validation gates pass.

---

## Phase 1: Access Enablement (Owner: You)

### Step 1: Obtain official API access

Acquire from BIAN:

- Authentication mechanism (Bearer token, API key, OAuth flow, tenant binding)
- Required headers and token lifetime/refresh expectations
- Allowed endpoint base URL(s) for v14 model access
- Rate limits and usage constraints

### Step 2: Confirm endpoint contract for required datasets

Confirm these list datasets are available and authorized for v14:

- `BOClassesLite` or equivalent list endpoint
- `BOEnumerationsLite` or equivalent list endpoint
- `BusinessAreas`
- `BusinessDomains` or `BusinessDomainsBasic`
- `ServiceDomainsBasic`

### Step 3: Deliver access package to engineering

Provide:

- Auth details (securely)
- Any endpoint path differences from v4 assumptions
- A short "how to authenticate" runbook

**Exit criteria:** Engineering can execute authenticated requests and retrieve non-empty v14 payloads for required datasets.

---

## Phase 2: Snapshot Acquisition (Owner: Engineering)

### Step 4: Wire authenticated downloader execution

Use:

- `references/industry_standards/bian/download-snapshots.ps1`

Run with authenticated context against v8 (preferred), fallback only if explicitly approved:

```powershell
$env:BIAN_BEARER_TOKEN = "<token>"
powershell -ExecutionPolicy Bypass -File .\references\industry_standards\bian\download-snapshots.ps1 -Version 14.0.0
```

### Step 5: Persist v14 raw snapshots

Write required files under:

- `references/industry_standards/bian/v14/`

Files expected:

- `BOClassesLite.json`
- `BOEnumerationsLite.json`
- `BusinessAreas.json`
- `BusinessDomains.json`
- `ServiceDomainsBasic.json`

### Step 6: Record provenance and integrity

Update:

- `references/industry_standards/bian/source-manifest.md`

Add for each file:

- Exact source URL
- Retrieval date/time (UTC)
- SHA256 checksum
- Notes on auth scope/version

**Exit criteria:** All five v14 source files exist, are non-empty, and have manifest provenance entries with checksums.

---

## Phase 3: Generate v14 Reference Artifacts (Owner: Engineering)

### Step 7: Generate versioned standards references

Run:

```powershell
python references/industry_standards/bian/extract-references.py --version 14.0.0
python references/industry_standards/bian/extract-references.py --version 14.0.0 --fetch-classes
```

Expected output in:

- `agents/agent-ontology/skills/standards-alignment/standards/bian/v14/`

Expected files:

- `bo-classes.md`
- `bo-classes-detail.md`
- `enumerations.md`
- `hierarchy.md`

### Step 8: Keep v13 regenerated for baseline comparison

Run:

```powershell
python references/industry_standards/bian/extract-references.py --version 13.0.0
```

Use v13 as baseline for count/delta sanity checks.

**Exit criteria:** v14 artifacts are generated successfully and structurally valid.

---

## Phase 4: Agent and Guidance Alignment (Owner: Engineering)

### Step 9: Confirm standards guidance matches runtime reality

Verify/update:

- `agents/agent-ontology/skills/standards-alignment/standards/bian/README.md`
- `references/industry_standards/bian/v14/README.md`

Ensure:

- v14 default guidance remains correct
- auth requirements are accurately documented
- snapshot acquisition commands are current

### Step 10: Confirm cross-agent references remain valid

Spot-check references in regulation and ontology skills to canonical BIAN guidance entrypoint.

**Exit criteria:** No stale v13-only assumptions in active guidance where v14 should be primary.

---

## Phase 5: Validation and Pilot (Owner: Engineering + Modelling Leads)

### Step 11: Data quality and schema checks

Validate:

- JSON parseability
- Non-empty arrays
- Required key presence (`name`, `description`, identifiers)
- No malformed markdown output tables

### Step 12: Mapping smoke tests

Run at least these mappings using v14 references:

- Party
- PartyRole
- CustomerRole
- Account
- Transaction or AccountEntry mapping rationale

### Step 13: Pilot a real workflow

Run one full standards-alignment pass on a known domain (Financial Crime) using v14 references only.

**Exit criteria:** Pilot produces coherent mappings with no blocker defects.

---

## Phase 6: Controlled Cutover (Owner: Team)

### Step 14: Adopt v14 as operational default

Operational policy:

- New modelling uses v14 references.
- Existing v13 artifacts stay valid and unchanged unless intentionally upgraded.

### Step 15: Track migration progress for existing assets

Maintain a lightweight register:

- Not started / In progress / Upgraded to v14 / Intentionally retained on v13.

**Exit criteria:** Team uses v14 by default for all new BIAN-aligned work.

---

## Phase 7: v13 Deprecation Decision (Owner: Governance)

### Step 16: Decide deprecation timeline

Only consider v13 deprecation after:

- v14 stable operation over agreed observation window
- no unresolved critical mapping regressions
- downstream consumers notified

Until then, keep v13 references side-by-side.

---

## Roles and Responsibilities

Role | Responsibility
--- | ---
You (API Access Owner) | Obtain and validate official v14 API access, auth method, and endpoint contract
Engineering | Run authenticated snapshot acquisition, generate artifacts, update docs and guidance
Modelling Leads | Validate mapping quality in real domain scenarios
Governance/Architecture | Approve cutover and future v13 deprecation

---

## Relevant Files

- `references/industry_standards/bian/download-snapshots.ps1`
- `references/industry_standards/bian/source-manifest.md`
- `references/industry_standards/bian/v14/README.md`
- `references/industry_standards/bian/v14/`
- `references/industry_standards/bian/extract-references.py`
- `agents/agent-ontology/skills/standards-alignment/standards/bian/README.md`
- `agents/agent-ontology/skills/standards-alignment/standards/bian/v14/`
- `agents/agent-ontology/skills/standards-alignment/standards/bian/v13/`

---

## Verification Checklist

1. Authenticated request to v8 succeeds (`200`) for all required list datasets.
2. All five v14 source JSON files are present and non-empty under `references/industry_standards/bian/v14/`.
3. `source-manifest.md` has URL, timestamp, checksum for each file.
4. v14 reference generation runs without errors.
5. Generated v14 markdown files render correctly and contain expected record volumes.
6. Smoke mappings (Party, PartyRole, CustomerRole, Account, Transaction/AccountEntry) pass review.
7. Team confirms v14 default policy and communicates v13 compatibility posture.

---

## Decisions

- Migration mode: side-by-side (v13 retained, v14 introduced safely).
- Access dependency: official authenticated v8 access is mandatory for reliable v14 onboarding.
- Cutover policy: default new work to v14 only after validation gates pass.
- Risk posture: no silent fallback to empty datasets; fail fast on incomplete snapshots.

---

## Risks and Mitigations

Risk | Impact | Mitigation
--- | --- | ---
Auth delays or unclear onboarding | Migration blocked | Escalate via BIAN support; request sample curl and scope confirmation
Endpoint contract drift | Downloader breaks | Keep downloader configurable (`-BaseUrl`, token support); update manifest notes
Partial dataset availability | Broken references | Enforce non-empty snapshot checks and gate generation
Semantic differences v13→v14 | Mapping regressions | Run smoke tests + pilot before cutover

---

## Further Considerations

1. If BIAN provides bulk export files, prefer those over per-endpoint pull for reproducibility.
2. Add CI check that rejects empty v14 snapshot files when version is marked active.
3. After stable cutover, consider adding an automated delta report (v13 vs v14 class/enumeration count and renamed concepts).
