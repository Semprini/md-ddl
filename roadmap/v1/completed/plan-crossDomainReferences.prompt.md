# Plan: Cross-Domain References

## TL;DR

Validate and demonstrate the existing cross-domain reference system defined in `9-Data-Products.md` by building a consumer-aligned product that spans Financial Crime and Healthcare domains. Example-driven approach: build the cross-domain product first, document any spec gaps or ambiguities encountered, then fix the spec to close those gaps. Scope is minimal — product-level `cross_domain:` block only, no cross-domain entity ownership or inheritance.

---

## Phase 1: Build Cross-Domain Example

### Step 1: Create a cross-domain consumer-aligned product in Financial Crime

Add a new product to `examples/Financial Crime/products/` that references entities from both Financial Crime and Healthcare domains. Natural use case: **Patient Financial Fraud Detection** — combining healthcare patient identity with financial transaction risk.

Product declaration should exercise:
- `class: consumer-aligned` with `cross_domain:` block
- Entity references from Financial Crime (Transaction, Party, Party Role, Account)
- Entity references from Healthcare (Patient, Encounter, Practitioner)
- Governance metadata conflict resolution (Financial Crime: Highly Confidential / AML / 10yr retention vs Healthcare: Confidential / HIPAA / 7yr retention)
- Masking strategy for PHI attributes from Healthcare + PII attributes from Financial Crime
- SLA declaration

```yaml
cross_domain:
  - domain: Healthcare
    entities:
      - Patient
      - Encounter
      - Practitioner
```

**Relevant file:** New file `examples/Financial Crime/products/patient-fraud-detection.md`

### Step 2: Create a cross-domain consumer-aligned product in Healthcare

Add a reciprocal product to `examples/Healthcare/products/` that pulls from Financial Crime. Natural use case: **Clinical Billing Fraud Detection** — combining clinical encounter data with financial transaction patterns to detect billing fraud.

This product exercises the same `cross_domain:` syntax but from the opposite direction, demonstrating that cross-domain references are bidirectional (either domain can reference the other).

```yaml
cross_domain:
  - domain: Financial Crime
    entities:
      - Transaction
      - Party
      - Account
```

**Relevant file:** New file `examples/Healthcare/products/billing-fraud-detection.md`

### Step 3: Verify governance conflict resolution rules

For each cross-domain product, explicitly work through the governance conflict resolution rules defined in `9-Data-Products.md`:

Check | Financial Crime Product | Healthcare Product
--- | --- | ---
Classification — highest wins | MAX(Highly Confidential, Confidential) = Highly Confidential | MAX(Confidential, Highly Confidential) = Highly Confidential
Retention — longest wins | MAX(10yr, 7yr) = 10yr | MAX(7yr, 10yr) = 10yr
PII — union | Both have PII; union masking | Both have PII; union masking
Regulatory scope — union | AML + HIPAA | HIPAA + AML

Document the resolution explicitly in each product's governance block with `justification:` comments.

---

## Phase 2: Document Gaps Found During Example Work

### Step 4: Log ambiguities encountered

As the products are authored, log every question or ambiguity where the spec doesn't give a clear answer. Expected issues based on research:

Known gap | Description | Expected resolution
--- | --- | ---
Domain path syntax | `cross_domain:` uses `domain: Healthcare` — is this the domain name from the domain.md H1, the folder name, or a qualified path? | Clarify in spec: domain name as declared in domain.md H1 heading
Entity name resolution | When `entities: [Patient]` is listed under a cross-domain reference, how does the consuming agent locate the entity file? | Clarify: resolved via `examples/{domain}/entities/{entity-slug}.md` convention or explicit path
Masking precedence | If Financial Crime masks `Date of Birth` as `year-only` and Healthcare masks it as `redact`, which wins in the cross-domain product? | Clarify in spec: product-level masking declaration is authoritative; product author must explicitly declare strategy per attribute
SLA mismatch | Financial Crime product has `freshness: < 15 minutes`; Healthcare entities may have batch-only sources with daily refresh. How is this declared? | Clarify: per-entity freshness not currently supported; product SLA is a contract, not derived from source freshness
Inverse relationship across domains | If the cross-domain product references Patient, does the Patient entity page in Healthcare show an inverse reference back? | Clarify: no — cross-domain products are one-directional references, not mutual relationships

### Step 5: Write spec clarifications

For each gap logged in Step 4, draft a targeted clarification to the relevant spec section. All expected clarifications are minor additions to `9-Data-Products.md`:

- Add a "Domain Name Resolution" paragraph to the `cross_domain:` section specifying that `domain:` matches the H1 heading of the referenced domain's `domain.md`
- Add a "Masking Precedence" paragraph confirming product-level masking is authoritative for cross-domain products
- Add a "SLA Scope" note clarifying that SLA is a product-level contract and does not imply per-entity freshness guarantees
- Add an "Inverse References" note confirming cross-domain references are unidirectional (referenced domain is not modified)

**Relevant file:** `md-ddl-specification/9-Data-Products.md` — targeted additions only

---

## Phase 3: Verification

### Step 6: Validate cross-domain products parse correctly

Check both product files for:
- Valid YAML in code blocks
- `cross_domain:` entries match actual domain names and entity names in referenced domains
- Governance block explicitly resolves every conflict (classification, retention, PII, regulatory scope)
- Masking entries cover all sensitive attributes from both domains
- SLA block is present and uses spec-defined keys

### Step 7: Agent walkthrough validation

- Run Agent Architect against both cross-domain products to verify it can interpret the `cross_domain:` block
- Run Agent Artifact to verify it can generate physical artifacts from a cross-domain product (it should pull entity definitions from both domains)
- Run Agent Governance to verify governance conflict resolution is flagged as complete (no audit gaps)

### Step 8: Update coverage matrix

Add cross-domain product row to the coverage matrix created in the Example Completeness plan (Step 15):

Feature | Simple Customer | Financial Crime | Healthcare
--- | --- | --- | ---
Cross-domain product | | ✓ (patient-fraud-detection) | ✓ (billing-fraud-detection)

---

## Relevant Files

- `examples/Financial Crime/products/patient-fraud-detection.md` — new cross-domain product (Step 1)
- `examples/Healthcare/products/billing-fraud-detection.md` — new cross-domain product (Step 2)
- `examples/Financial Crime/domain.md` — reference for governance metadata values
- `examples/Healthcare/domain.md` — reference for governance metadata values (created in Example Completeness plan)
- `md-ddl-specification/9-Data-Products.md` — spec clarifications (Step 5)
- `examples/README.md` — coverage matrix update (Step 8)

## Verification

1. YAML lint both new product files — no syntax errors
2. Confirm `domain:` values in `cross_domain:` blocks match H1 headings in referenced domain.md files
3. Confirm all `entities:` listed in `cross_domain:` blocks have corresponding entity files in the referenced domain
4. Verify governance resolution is explicit (no silent inheritance) — each conflict must have a declared resolution
5. Verify masking covers all PII/PHI attributes from both contributing domains
6. Run Agent Architect interpretation check on both products
7. Confirm spec clarifications in `9-Data-Products.md` don't contradict existing rules

## Decisions

- **Scope: product-level only** — cross-domain references stay within the `cross_domain:` block on consumer-aligned products. No cross-domain entity ownership, inheritance, or shared entity definitions.
- **Example-driven** — build the products first, document gaps as encountered, then patch the spec. This avoids over-specifying rules that may not matter in practice.
- **Bidirectional demonstration** — two products (one per domain) show that either domain can reference the other, demonstrating the pattern is symmetric.
- **Governance conflict resolution is explicit** — every conflict documented and resolved in the product YAML, not left to implicit inheritance.
- **Spec changes are minimal** — clarifications only, no new syntax or features. The existing `cross_domain:` block and governance resolution rules in `9-Data-Products.md` are sufficient; they just need minor disambiguation.

## Dependencies

- **Depends on Example Completeness plan Phase 3** — Healthcare domain must exist before cross-domain products can reference it. Specifically, Steps 8–10 (domain structure, domain.md, entity files) must be complete.
- Steps 1 and 2 can run in parallel once Healthcare exists
- Step 3 depends on Steps 1 and 2
- Steps 4 and 5 are sequential (log gaps, then fix)
- Steps 6–8 depend on all prior steps

## Further Considerations

1. **Cross-domain product in Healthcare as part of Example Completeness?** The billing-fraud-detection product (Step 2) could be included as one of Healthcare's two required products in the Example Completeness plan (Step 12). This avoids creating Healthcare products twice. Recommendation: Yes — make billing-fraud-detection the consumer-aligned product for Healthcare, and create a separate domain-aligned canonical product. Two plans share the work on this file.
