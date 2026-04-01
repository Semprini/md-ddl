# Financial Crime Domain Review — 2026-03-31
**Scope:** Full domain review of `examples/Financial Crime/` covering structural conformance, decision quality, and dimensional model readiness.
**Trigger:** User request to verify entity, enum, and relationship completeness with sufficient attribute depth to support dimensional model data product generation.
**Verdict: Conditionally Ready** — zero Critical structural breakages; several Major issues resolved in the same session. See remediation log below.
---
## Pass Summary
What is already correct:
- Domain metadata complete: `classification`, `pii`, `regulatory_scope`, `default_retention`, `status`, `version`
- Party and Party Role have full bitemporal tracking declarations with regulatory rationale
- Contact Address has explicit valid-time handling with strong constraint blocks
- Address entity correctly separates location reference data from party-address association
- Governance blocks on high-PII entities (Party, Person, Contact Address) are thorough with `compliance_relevance` and `access_role`
- Enum definitions for Party Status, Financial Crime Risk Rating, Sanctions Screen Status, Due Diligence Status, PEP Status, Address Type/Purpose/Verification Status, Verification Method, Currency Code are well-formed
- Constraint blocks on Party, Party Role, Person, Contact Address are specific and regulatory-referenced
- Self-referential `Party Related To Party` relationship is correctly modelled with `relationship_attributes`
- `Customer Holds Account` correctly uses many-to-many with `relationship_attributes`
- `Exchange Rate` correctly uses `append_only` + dependent existence
- BIAN BOM references throughout are plausible
---
## Findings
### Critical
None.
---
### Major — Resolved in This Session
**M1 — Transaction entity is under-specified for dimensional fact modelling**
- Path: `entities/transaction.md`
- Issue: Transaction has only 4 attributes (Identifier, Date Time, Amount, Reference). Missing: Transaction Type, Channel, Status, Settlement Date Time, and crucially no currency or account references. A `fact_transaction` table cannot be built without these dimension keys.
- Fix: Added Transaction Type (enum), Transaction Channel (enum), Transaction Status (enum), Settlement Date Time, Transaction Denomination Currency relationship, Debit Account relationship, Credit Account relationship.
**M2 — Account entity is under-specified for dimensional dimension modelling**
- Path: `entities/account.md`
- Issue: Account has 4 attributes with no status, no type/product category link, and no currency denomination. A `dim_account` table is analytically useless without status and type.
- Fix: Added Account Status (enum), Account Type (enum), and Account Denominated In Currency relationship.
**M3 — FK attributes present on Teller and Merchant (spec violation)**
- Paths: `entities/teller.md`, `entities/merchant.md`
- Issue: `Assigned Branch Identifier` on Teller and `Settlement Account Identifier` on Merchant are foreign-key string attributes. MD-DDL spec: "Never add foreign key attributes to entities. Relationships handle links."
- Fix: Removed both FK attributes. `Teller Assigned To Branch` relationship already existed. Added `Merchant Has Settlement Account` relationship.
**M4 — Party Role At Point In Time relationship has wrong target entity**
- Path: `entities/party_role.md`
- Issue: `target: Customer` on a period-granularity snapshot relationship. Customer is a specialisation of Party Role — targeting it here is semantically incorrect and implies Customer-specific snapshots only.
- Fix: Changed target to `Party Role` with `self_referential: true`.
**M5 — Domain.md overview diagram is significantly incomplete**
- Path: `domain.md`
- Issue: Diagram shows only ~10 entities; Transaction, Account, Product, Agreement, Branch, Currency, Exchange Rate, Loan Agreement, Term Deposit Agreement are absent. A reader cannot understand the domain from the diagram alone.
- Fix: Rebuilt diagram to include all entities and key relationships.
**M6 — Domain.md Relationships table missing entries**
- Path: `domain.md`
- Issue: `Teller Assigned To Branch`, `Exchange Rate References Base Currency`, `Exchange Rate References Quote Currency` all exist in entity detail files but are absent from the domain summary table. Navigability broken.
- Fix: Added all missing relationships to domain summary.
**M7 — Duplicate reverse relationships on Payer, Payee, Payment Initiator**
- Paths: `entities/payer.md`, `entities/payee.md`, `entities/payment_initiator.md`
- Issue: Each file declares a reverse relationship (Payer→Transaction, Payee→Transaction, PaymentInitiator→Transaction) that duplicates the canonical Transaction-owned relationships (`Transaction Has Debtor`, `Transaction Has Creditor`, `Transaction Initiated By Instructing Agent`). Creates navigability confusion and potential physical generation conflicts.
- Fix: Removed the three reverse relationships from the role files.
---
### Major — Dimensional Readiness Only (Resolved)
**M8 — Missing enums required for dimensional modelling**
- Path: `enums.md`
- Issue: Transaction Type, Transaction Status, Transaction Channel, Account Status, Account Type, Agreement Status, Contact Preference, Company Legal Structure, Association Type, and Account Holder Type were all free-form strings or absent. Without enums, dimensional model attributes cannot be reliably used as dimension keys or filter predicates.
- Fix: All ten enums added to `enums.md` and to domain.md Enums summary table.
**M9 — Agreement entity missing status attribute**
- Path: `entities/agreement.md`
- Issue: Agreement has no lifecycle status. You cannot determine whether an agreement is Active, Expired, or Terminated. This is a required dimensional attribute for agreement-based analysis.
- Fix: Added Agreement Status (enum) attribute.
**M10 — Company entity thin for AML purposes**
- Path: `entities/company.md`
- Issue: Only 3 attributes. Missing: Legal Structure (critical for distinguishing shell companies, trusts, SPVs from operating entities), Tax Identifier (ABN/NZBN/EIN for identity verification), and Ultimate Beneficial Owner flag. Company Legal Structure is directly relevant to AML risk rating decisions.
- Fix: Added Company Legal Structure (enum) and Tax Identifier attributes.
**M11 — Customer Preferences Contact Preference is a free-form string**
- Path: `entities/customer-preferences.md`
- Issue: `Contact Preference: string` cannot be used reliably as a dimensional attribute or filter. Should be an enum.
- Fix: Changed to `enum:Contact Preference`.
---
### Minor
**m1 — Branch has no Address link**
- Branch is a physical location but has no reference to the Address entity. For network analysis (e.g., transactions at branches co-located with high-risk addresses), this link is useful.
- Observation only — out of scope for this session. Note for future modelling.
**m2 — Exchange Rate has no Rate Source attribute**
- For regulatory audit, knowing which rate provider was used for FX conversion is useful.
- Observation only.
**m3 — Loan Agreement and Term Deposit Agreement diagrams do not show inherited Agreement Identifier**
- Minor diagram completeness issue. Inherited attributes are not shown in specialisation diagrams by convention — acceptable.
**m4 — `Product Category` remains a free-form string on Product**
- Suggested as an enum (Savings, Current, Loan, Term Deposit, etc.) but Product Category is institution-specific. Left as string pending SME confirmation of standard values.
---
## Decision Summary
| Dimension | Assessment |
| --- | --- |
| Relationship granularity | `atomic` appropriate for all instance-level pairings. `group` on Branch Transaction Summary is correct. `period` on Party Role At Point In Time target corrected. |
| Temporal tracking | Party and Party Role: bitemporal — correct for AML audit. Contact Address: explicit valid-time — correct. Transaction: append_only — correct. Account: `frequently_changing` but no temporal declaration — advisory for future consideration. |
| Existence | Independent/dependent/associative correctly applied. Contact Address as `associative` is correct. Exchange Rate as `dependent` is correct. |
| Mutability | Reference data (Address, Currency, Branch) correctly `reference`. Transaction correctly `append_only`. Party/Party Role/Account correctly `slowly_changing` or `frequently_changing`. |
| Conceptual → logical | Specialisation hierarchies (Party→Person/Company, Party Role→Customer/Merchant/etc., Agreement→subtypes) are coherent. Ownership directions are consistent. M:N Customer Holds Account is intentional and correctly declared. |
| Standards alignment | BIAN BOM references are plausible and consistently applied. Not independently verified — see SME checklist. |
| Regulatory posture | AUSTRAC, RBNZ, FATF references are well-applied on high-PII entities. Transaction and Account governance blocks inherit domain defaults — appropriate for those entities. |
---
## Pending SME Review
- [ ] Entity completeness — are all real-world concepts represented? (e.g., Correspondent Bank, Alert/Case entities for SAR workflow may be missing)
- [ ] Relationship accuracy — do the modelled relationships match actual business rules?
- [ ] Business process coverage — do events capture the full lifecycle? (e.g., no SAR Filed event, no Account Frozen event)
- [ ] Governance correctness — are retention periods, classifications, and PII flags verified by legal/compliance?
- [ ] Standards alignment — are BIAN BOM Reference column mappings substantively correct for this organisation's use?
- [ ] Enum completeness — do enum values cover all real-world cases for Transaction Type, Account Type, etc.?
---
## Remediation Log
All Major findings were remediated in this session. Files modified:
- `enums.md` — added 10 enums
- `entities/transaction.md` — added attributes and relationships
- `entities/account.md` — added attributes and relationships
- `entities/agreement.md` — added Agreement Status attribute
- `entities/company.md` — added Legal Structure and Tax Identifier
- `entities/teller.md` — removed FK attribute
- `entities/merchant.md` — removed FK attribute; added relationship
- `entities/customer-preferences.md` — changed Contact Preference to enum type
- `entities/payer.md` — removed duplicate reverse relationship
- `entities/payee.md` — removed duplicate reverse relationship
- `entities/payment_initiator.md` — removed duplicate reverse relationship
- `entities/party_role.md` — fixed Party Role At Point In Time target
- `domain.md` — rebuilt diagram; completed Relationships and Enums summary tables
---
## Handoff
This domain is now **Conditionally Ready** for dimensional data product design. The `Transaction Risk Summary` and `Canonical Party` products can proceed. Recommend:
> "Design a dimensional star schema for the Financial Crime domain targeting the Transaction Risk Summary data product." — Agent Artifact
