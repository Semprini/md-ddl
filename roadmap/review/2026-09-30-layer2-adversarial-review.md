# MD-DDL Adversarial Review — 2026-09-30 (Layer 2)

**Spec version:** Draft 0.10.0 (`md-ddl-specification/1-Foundation.md:1`)
**Package:** `md-ddl` 0.10.0
**Brief:** `.prompts/md-ddl-adversarial-review-prompt.md`, run under `.prompts/md-ddl-layered-review-process.md` (Layer 2). Agent Test (`agents/agent-test/`) and its skills are in scope although the brief predates them.
**Question asked by the owner:** what must be fixed before v1?

Severity scale (same as Layer 1): **Critical** = the standard or its flagship example produces incorrect or non-reproducible output, or silently defeats a governance control. **Major** = a rule contradicts another rule, an agent instruction contradicts the spec, or a core scenario cannot be expressed. **Minor** = local defect or friction. "Blocks v1?" means: should be settled before the 1.0 freeze, because it fixes grammar, vocabulary or normative behaviour that can only change by a major bump afterwards.

---

## How this review was run

Every finding cites text I read in this repository. Where a claim rests on a count or a search, I ran it (`grep`, a short Python script for enum membership and byte sizes). Nothing was executed from the agents; agent findings are predictions from reading prompts and are labelled as such.

I read in full: all ten spec sections; `agents/CONVENTIONS.md`; all six `AGENT.md` files; the Source Mapping, Test Strategy and Worked Example Compilation skills; `generation-semantics.md`; `guides/lifecycle-versioning.md`; the validation-tooling guide's pre-flight section. Financial Crime: `domain.md`, all eleven source files, `LIFECYCLE.md`, `handoff-to-artifact.md`, the Canonical Party, Source Feed, Patient Fraud and Transaction Risk Summary products (the Legacy product to line 80), and the `party`, `customer`, `address` and `transaction` entity files.

Read by excerpt or targeted search only: the Domain Review, Compliance Audit and Product Design skills; the dbt-project skill (lines 60-160); the dialect type tables; the Financial Crime `account`, `branch`, `company`, `exchange-rate`, `payer`, `person` and `party_role` entities; Financial Crime events (actor and timestamp attributes only); Financial Crime enums (values extracted by script); Healthcare and Telecom domain metadata, entity governance and mutability lines, and the cross-domain products; Brownfield Retail domain metadata and baseline headers. Not read: `consistency_example.py`, `factories.py`, Retail Sales, Retail Service, Simple Customer (except its abstract declaration), and the Healthcare and Telecom source layers (Readiness V1-06 covers those).

Checked by hand or script and found **consistent** (no finding): every `conditional` case key in the Financial Crime transforms is a member of its target enum (script-extracted enum values, compared by eye); the dedup key rendering in the ContactPoint worked example (`ADDR:12 HARBOUR ST|6011|NZ`) follows the composition rule at `8-Transformations.md:221`; the worked examples for `Map Party Status`, `Map Account Status`, `Map Transaction Status` and `Map Sanctions Screen Status` agree with their YAML.

---

## Cross-reference to earlier reviews

Layer 1 = `2026-09-30-layer1-structural-review.md`. Readiness = `2026-09-30-v1-readiness-review.md`.

Earlier finding | This review
--- | ---
Layer 1 S1 (`## Sources` vs `## Source Systems`) | **Confirms.** Financial Crime `domain.md:122` uses `## Source Systems`; every source file uses `## Sources`. Not re-reported.
Layer 1 S2 (source `status` vocabulary) | **Confirms** the gap. **Corrects one detail:** S2 says the domain/product lifecycle vocabulary is `Draft | Active | Deprecated | Retired` "used for domains (`2-Domains.md:244`)". Line 244 is the Data Products table. The domain status vocabulary (`2-Domains.md:268-274`) has five values including `Review`, and entities use the same five (`3-Entities.md:209`). Only products have four (`9-Data-Products.md:147`). Three status vocabularies exist. See L2-M9.
Layer 1 S17 (§9 lineage names entities in one place, products in another) | **Extends.** The flagship violates the "canonical products only" rule as written, and the lineage schema cannot name a product. See L2-09.
Layer 1 "Clean areas: lifecycle boundary audit, no undeclared overlaps; handoffs consistent" | **Disagrees.** The handoff protocol itself has defects (L2-18), and downstream agents do not implement the 0.10 source-layer semantics the boundaries assume (L2-19).
Layer 1 "Clean areas: Examples lint clean, none uses relationships without `type:`..." | **Consistent but not sufficient.** Lint-clean is true. Layer 1 explicitly did not assess semantics. The flagship has semantic defects that lint cannot see (L2-01, -04, -09, -10, -11, -13, -14).
Readiness V1-02 (conformance undefined; eight "validation error" statements unassigned) | **Confirms and extends.** Two of those statements collide with the flagship or with each other (L2-M8).
Readiness V1-05 (new features have not soaked) | **Confirms and extends.** The one exemplar that exercises the new constructs itself breaks spec rules (L2-10) and cannot express its own relationships (L2-01). A soak on this exemplar would not have surfaced the grammar gaps, because the exemplar routes around them silently.
Readiness V1-06 (Healthcare/Telecom non-conforming but lint clean) | **Extends.** Financial Crime, which V1-06 treats as the conforming exemplar, has the same class of defect.
Readiness V1-01 (no spec versioning policy) | **Extends.** The *model* versioning definition is also self-contradictory (L2-17), and there is no cross-domain pinning (L2-16).
Readiness S-16 (multi-domain conflict rules still normative) | **Extends.** The rules are also wrong or unsafe as written (L2-07, L2-08).
Readiness S-11 (no repeatable agent eval) | **Confirms.** L2-19 shows the kind of regression such a harness would catch.

---

## Summary

ID | Severity | Blocks v1? | Area | Finding
--- | --- | --- | --- | ---
L2-01 | Critical | Yes | Spec / flagship | Sources cannot populate a relationship unless the target entity name is unique; edge attributes have no mapping target. Financial Crime silently omits five relationships
L2-02 | Critical | Yes | Spec | Multi-source instance semantics are undefined: re-emission by the establishing source, default merge, hold granularity, absent `references` target
L2-03 | Critical | Yes | Spec | Relationship `cardinality` has no defined vocabulary and no optionality, so foreign-key nullability is undeterminable
L2-04 | Critical | Yes | Flagship / spec | A product's `masking` can name attributes that do not exist. Transaction Risk Summary publishes PII unmasked while declaring masking
L2-05 | Major | Yes | Spec / agents | The type system has no precision, scale or length, but dialect files "map from entity YAML"
L2-06 | Major | Yes | Spec | Domain `pii` is defined as "any entity" but inherited as "every entity"; subtype governance inheritance is unstated
L2-07 | Major | Yes | Spec / agents | "Longest retention wins" is the only conflict rule and cannot express a maximum-retention obligation. Governance agent contradicts itself
L2-08 | Major | Yes | Spec / flagship | Multi-domain conflict detection compares domain defaults only. Both cross-domain flagship products get the scope union wrong
L2-09 | Major | Yes | Spec / flagship | Consumer products "source only from canonical products" but no domain-aligned product publishes their entities, and lineage cannot name a product
L2-10 | Major | Yes | Flagship vs spec | Payer, Payee and Payment Initiator collapse many rows into one instance with no `deduplication`, violating Transformation Rule 8
L2-11 | Major | Yes | Spec / flagship | The dedup key can merge unrelated instances; the Address key omits city and merges on null postcode
L2-12 | Major | Yes | Spec / flagship | Bitemporal entities have no way to designate a valid-time source column; contribution rules cover 3 of 5 mutability values
L2-13 | Major | No | Spec / flagship | Consumer `Path` traversal has no multiplicity rule; the flagship path is invalid and multiplies the grain
L2-14 | Major | No | Flagship / spec | Constraints that encode process rules contradict worked examples; `check` language and `lifecycle_stage` are undefined
L2-15 | Major | Yes | Spec | The same source is identified three ways (`id`, folder, table casing) and the spec's own §7 and §9 examples disagree
L2-16 | Major | Yes | Scale / evolution | Relationships and `extends` cannot cross domains; lineage cannot pin a version; lineage is unidirectional so impact analysis is impossible
L2-17 | Major | Yes | Evolution | "Breaking" is defined as "different or incorrect output", which makes every additive change breaking. The guide contradicts it and itself
L2-18 | Major | Yes | Agents | Handoff protocol: file naming is ambiguous, one-pending rule discards unconsumed work, `consumed` is set on read
L2-19 | Major | Yes | Agents | No downstream agent implements `contributes`, `when_absent`, `earliest` or product `consistency` semantics; Agent Test cannot compile contributing-table examples
L2-20 | Major | No | Agents | Ontology's "every entity gets `identifier: primary`" rule reintroduces the defect Financial Crime 2.0.0 fixed
L2-21 | Major | No | Spec | `cardinality: 0..*` in Entity Fan-Out has no mechanism to enumerate the instances (repeating column groups, arrays)
L2-22 | Major | No | Spec / flagship | Default `when_absent: hold` is unbounded and silent; a confirmed sanctions match on an unknown party is invisible
L2-23 | Major | No | Spec / flagship | No way to declare an attribute or relationship as unsourced. Flagship has eight unsourced entities and attributes that consumer products map anyway
L2-M1 to L2-M12 | Minor | No (see table) | Various | Twelve minor findings (table below)

Critical: 4. Major: 19. Minor: 12 (numbered L2-M1 to L2-M12).

---

## What I Cannot Evaluate

- **Regulatory correctness.** I can read what a governance block cites and compare it with the domain's own `regulatory_scope`. I cannot judge whether AUSTRAC, NZ AML/CFT, HIPAA, PCI DSS or GDPR obligations are stated correctly. Statements about GDPR storage limitation, PCI DSS retention, HIPAA record retention and AML tipping-off (L2-07, L2-08, L2-M11) are flagged for a compliance specialist, not asserted.
- **Real source-system behaviour.** Whether Salesforce, Temenos or SAP emit rows in the orders and shapes I assume when constructing scenarios. The scenarios test what the spec permits, not what those vendors do.
- **Agent behaviour at runtime.** No agent was run. Every "agent would do X" statement is a prediction from the prompt text. Some of them may be handled by the model's own judgement in practice.
- **Whether a modelling choice is wrong for the business.** For example, whether Payer and Payee should be persistent Party Roles at all. I report where the modelling contradicts the spec's rules, not whether the business would prefer it.
- **Physical generation outcomes.** I did not generate DDL or dbt and did not run DuckLake or Snowflake. Effects on generated output are inferred from the skills and dialect tables.
- **Linter behaviour.** I did not rerun the linter. Its coverage is taken from Layer 1 and the readiness review. I did not read `src/md_ddl/lint.py`.
- **Retail Sales, Retail Service, Simple Customer and most of the Brownfield Retail sources.** I sampled Brownfield Retail's domain metadata and baseline headers only. Absence of findings there means not examined.
- **`standards-alignment/standards/**` and `references/industry_standards/**`** (BIAN, FHIR, ISO 20022, TM Forum reference files). Not read.
- **The `guides/` other than lifecycle-versioning, validation-tooling and diagram-style.** Not read in depth.
- **Usability.** Whether a human finds these rules learnable or the ambiguities significant in practice is Layer 3's question.
- **AI-evaluating-AI limits.** This review was produced by an AI reading a largely AI-authored repository. Shared blind spots are likely around YAML-heavy notations and around what a human data modeller would consider "obviously" implied (which is where I called ambiguity a defect).

---

## Critical findings

### L2-01. Sources cannot populate relationships that are not identified by a unique target entity name; edge attributes have no mapping target

**Evidence**

- `7-Sources.md:270`: `references` is "Which instance satisfies each relationship from this entry to another entity". Its shape in the example is `references: Address: Address Uniqueness Merge` (`:249-250`): the key is the **entity name**.
- `7-Sources.md:316-320`: a reference-only column's Destination is `Reference: <Entity>`, "naming the entity it identifies".
- `8-Transformations.md:41-52` and `7-Sources.md:363-371`: `target` is always `Entity · Attribute`. Nothing targets a relationship or a relationship attribute.
- `5-Relationships.md:99-110`: `relationship_attributes` are "columns on the bridge or association table". They appear in §5 only; §7 and §8 never mention them.
- Financial Crime has five relationship groups that the key shape cannot address:
  - `Transaction Has Debit Account` and `Transaction Has Credit Account`: both `many-to-one` to `Account` (`entities/transaction.md:231-250`, diagram `:31-32`).
  - `Exchange Rate References Base Currency` and `... Quote Currency`: both to `Currency` (`entities/exchange-rate.md:52,65`).
  - `Party Related To Party`, self-referential, with edge attributes (`entities/party.md:166-181`).
  - `Customer Holds Account`, many-to-many, with `Holder Type`, `Holder Start Date` (`entities/customer.md:73-90`).
- No transform in `sources/` populates any of them. `grep -i "debit\|holder\|association\|exchange"` over `sources/` returns only the word "Branch" in a channel code. The only Open Decisions about relationships are OD-1 (Product) and OD-1 (external counterparties). The gap is not declared.

**Failing scenario.** A payment table carries `DEBIT_ACCT_NO` and `CREDIT_ACCT_NO`. The author has to write `references: Account: ...` twice under one key. Two compliant resolutions exist: a generator that takes the first, or one that infers roles from column names. A m:n link with `Holder Type` has no entity instance to hang the attribute on, so `references` ("either side may declare it") has nowhere to put it. Party-to-party beneficial-ownership links, which the flagship calls "the structural basis for financial crime network analysis" (`party.md:168`), cannot be sourced at all. Because the spec says nothing, the flagship's authors omitted them without a record.

**Recommended fix.** Key `references` by **relationship name** (relationships already have Key-as-Name identity) and allow a list. Add a link entry type to `produces:` (for example `relationship: Customer Holds Account` with `source`, `target` identities and `attributes:`), and a Destination form for edge attributes (`Relationship Name · Edge Attribute`). Require unsourced relationships to appear in Open Decisions or a declared "not sourced" list (L2-23).

**Blocks v1?** Yes. The `references` key shape and the Destination grammar are frozen at 1.0. Changing a key from entity name to relationship name later is breaking.

**Why the standard evaluation misses this.** Lint and structural review check that `references` targets resolve to entities. They do not compare the model's relationship list with what the source layer populates.

---

### L2-02. Multi-source instance semantics are undefined where the 0.10 features are used

The five sub-issues below all concern what the pipeline does when one canonical instance is fed by several rows or tables. Each one has at least two readings that both comply with the text.

**(a) The establishing source's later rows.**
`7-Sources.md:278` says a *contribution* "records a new version that carries the earlier attributes forward". It says nothing about a later row from the *establishing* source. `8-Transformations.md:419` says "A source column not listed in `given` is null."
Financial Crime: `PaymentEvent` establishes `Transaction` (`table_payment_event.md`, fan-out entry without `contributes`). `Initiation` adds the channel; `PaymentParties` adds debtor and creditor (`transaction.md` temporal block: "a late-arriving contribution ... records a new version that carries the earlier attributes forward"). When `PaymentEvent` later re-emits the same `PaymentId` with `PaymentStatus = REVERSED` (which the transform explicitly expects: "A REVERSED status on the original payment records a new version"), that row carries no channel and no parties.
- Reading 1: the new version replaces the instance, so channel, debtor and creditor become null.
- Reading 2: the new version carries the contributed attributes forward.
Both comply. The spec's carry-forward sentence is limited to contributions.

**(b) Default merge of disjoint contributions.**
The Financial Crime fan-in examples say "no reconciliation is needed" because contributions are disjoint (`table_account.md:187-188`). `reconciliation` is the only merge device (`7-Sources.md:548`). The dbt skill says "Canonical model unioning the intermediate models on the entity identifier, applying `reconciliation` transformations per attribute" (`agents/agent-artifact/skills/dbt-project/SKILL.md:84`). With no reconciliation declared, a union yields one row per source per identifier (Reading 1); a merge yields one row with per-attribute coalescing (Reading 2). The worked examples assert the second, but nothing says a generator must produce it.

**(c) Hold granularity.**
`when_absent: hold` "keeps the row until the instance exists" (`7-Sources.md:272`). The `Initiation` row produces two entries: `Payment Initiator` (establishing) and `Transaction` (contributing) (`table_initiation.md:15-27`). If the `Transaction` does not exist yet:
- Reading 1: the whole row waits, so `INIT-P-1001` is not created either.
- Reading 2: only the contributing entry waits.
The `interim` example at `table_payment_event.md:117-133` assumes the second reading after step 2 but does not say so.

**(d) `hold` and `reject` cannot be asserted.**
`8-Transformations.md:419` says `cardinality: 0` asserts an entity is not produced. Held and rejected rows both produce zero instances now. No worked-example construct distinguishes them, and the spec calls worked examples "the only device in MD-DDL that pins behaviour" (`8-Transformations.md:376`).

**(e) A `references` target that does not exist.**
`7-Sources.md:270`: "A reference never creates the referenced instance." That is the only statement. `when_absent` is defined "For a contributing entry" only. No text (`grep -i "orphan\|dangling"` over the spec returns nothing) says what happens when the referenced instance is absent.
Financial Crime relies on this twice: `PaymentParties` references `Party: DebtorPartyId` while OD-1 records that external counterparties have no Party ("The roles reference a Party that no source creates", `table_payment_parties.md`, Open Decisions), and `Preference` references a `Customer` that exists only if the CRM row had a `CustomerNumber`. Possible behaviours: load with a dangling key; hold; reject; create a stub Party (which contradicts "never creates"). All four are compliant.

**(f) Subtype mismatch on a contribution.**
`table_contact.md:15-21` contributes to `Party · Person` and requires the identity to match. The spec (`:276`) says a row is held "if no instance with that identity exists". A CRM contact on a **business** account has an identity that exists, as a Company. The spec does not say whether the subtype is part of identity, so the row is held forever (Reading 1), rejected (Reading 2) or applied to the Company (Reading 3).

**Recommended fix.** State one rule for each: re-emission by an establishing entry is a per-attribute merge limited to the attributes that source maps (and say so in §7, not only for contributions); disjoint contributions merge per attribute by default and `reconciliation` overrides on conflict; `hold` applies per entry, not per row; add `when_absent` to `references` with the same vocabulary; define subtype mismatch as "no instance". Add a worked-example construct for held/rejected outcomes (for example `outcome: held`).

**Blocks v1?** Yes. These are the semantics of the features added on 29 September (`c1215a8`, `de08db5`, `0bbbcb9`), and the readiness review already flags that they have not soaked (V1-05).

**Why the standard evaluation misses this.** Each sentence in the spec is individually correct. The gap appears only when two of them are combined on one concrete table, which is what a structural review does not do.

---

### L2-03. Relationship `cardinality` has no defined vocabulary and no optionality; foreign-key nullability cannot be determined from the authoritative YAML

**Evidence**

- `5-Relationships.md:34` shows `cardinality: one-to-many` as the only example. The section never lists the permitted values. `grep "one-to-one\|many-to-one"` over the spec finds them only in `7-Sources.md:270` (and an unrelated use of "one-to-one field map" at `8-Transformations.md:71`). The examples use `one-to-one`, `one-to-many`, `many-to-one` and `many-to-many`.
- Nothing states whether a "one" end is mandatory or optional.
- Financial Crime:
  - `domain.md:196`: Transaction Has Debtor: "A Transaction has **exactly one** Debtor". YAML: `cardinality: many-to-one` (`transaction.md:175`). Diagram: `Transaction "0..*" --> "1" Payer` (`:27`).
  - `domain.md:212`: Transaction Has Debit Account: "Null for externally-held debit accounts". YAML: `cardinality: many-to-one` (`transaction.md:238`). Diagram: `"0..1" Account` (`:31`).
  The two YAML blocks are identical in the cardinality field. The difference lives only in prose and in the diagram.
- `3-Entities.md:34`: the diagram is "a rendering" and its associations "do not need to mirror" the semantic relationships. `agents/agent-artifact/AGENT.md:13-14`: "The YAML is authoritative for generation."
- No generation skill states an FK nullability rule: `grep -i "nullable\|NOT NULL\|optional"` over `normalized/SKILL.md` and `dimensional/SKILL.md` finds only discriminator and subtype columns.
- `Domain Review` treats "cardinality" as present or absent (`domain-review/SKILL.md:275`), never as correct.

**Failing scenario.** Generator A reads the YAML and makes both `debtor_id` and `debit_account_id` `NOT NULL`, so an inbound wire fails to load. Generator B reads the diagram and prose and makes only the debtor `NOT NULL`. Both follow the spec's precedence rule for A and its "diagram may realize differently" allowance for B.

The flagship also contradicts its own mandatory debtor: `table_payment_event.md:117-123` pins an interim Transaction that exists with no Payer, and `9-Data-Products.md:417` allows `not_null` attributes to be nullable under `nullable-staging`. That covers attributes, not relationships, so whether the debtor link may be null in the base structure is again undetermined.

**Recommended fix.** Define the vocabulary and put optionality in the YAML, for example `cardinality: many-to-one` plus `optional: source|target|both`, or explicit `min..max` per end. State that the YAML is authoritative and that the diagram must agree. Extend `consistency` to relationships.

**Blocks v1?** Yes. It changes the meaning of every existing relationship block and every generated FK.

**Why the standard evaluation misses this.** The Model Readiness check asks whether `cardinality` is present. Two well-formed blocks that differ only in prose look consistent.

---

### L2-04. A product's `masking` may name attributes that do not exist; the flagship consumer product publishes PII unmasked while declaring masking

**Evidence**

- `9-Data-Products.md:156`: masking entries each name "a product attribute". No rule requires the name to resolve. `:381`: "the product's `governance` and `masking` metadata are constraints on the generated artifacts."
- `examples/Financial Crime/products/analytics.md:41-45` (Transaction Risk Summary) masks `"Date of Birth"` (year-only) and `"Tax Identification Number"` (hash).
- The product's own logical model (`analytics.md`, `#### Logical Model`) contains `Payer Date of Birth` and no `Tax Identification Number` (checked by script: `'Tax Identification Number' in <model section>` is False). The same product publishes `Payer Legal Name` and `Payee Legal Name`, which `entities/party.md` marks `pii: true`, with no masking entry.
- The two masking names are the ones in the spec's own example (`9-Data-Products.md:132-135`, `Customer 360 Profile`), copied into a different product.
- `agents/agent-governance/skills/compliance-audit/SKILL.md:111` checks "A PII attribute ... has no `masking` entry". It has no check for a masking entry that resolves to nothing. It would flag Legal Name and Date of Birth as missing masks but would not flag the dangling entries, and an agent that treats the presence of a `masking` block as evidence of masking would pass the product.

**Failing scenario.** A generator that skips unresolvable entries produces a wide table with clear-text date of birth and names for a product whose declaration reads as masked. A generator that fails on them refuses to run. The spec permits either. Reviewers reading the YAML see masking and move on. This is "governance metadata that is technically valid but operationally meaningless", named in the brief.

**Recommended fix.** Add a rule: every `masking.attribute` must resolve to an attribute in the product's logical model (unqualified for single-entity products, `Entity.Attribute` for normalized ones), and every attribute marked PII upstream must have a masking entry or an explicit `unmasked` justification. Add it to the pre-flight set (it is reference integrity, not convention) or to Governance Level 4. Fix the example.

**Blocks v1?** Yes. Masking is the one control the standard promises to apply to generated artifacts, and the rule text is normative.

**Why the standard evaluation misses this.** The masking attribute strings look plausible and valid. Only a cross-file comparison of the masking block against the logical model catches it.

---

## Major findings

### L2-05. The type system has no precision, scale or length; the dialect files "map from entity YAML"

- `3-Entities.md:297-303`: the attribute property table has `type`, `description`, `identifier`, `unique`, `default`. `:307-315`: the type table has no precision, scale or length.
- `agents/agent-artifact/skills/dialects/snowflake.md:10`, `postgresql.md:10`, `databricks.md:10`: `decimal` maps to `NUMBER(p,s)` / `NUMERIC(p,s)` / `DECIMAL(p,s)`: "Map `precision` and `scale` from entity YAML". `snowflake.md:8`: `string` with `max_length` maps to `VARCHAR(n)`.
- `grep -rE "^\s+(precision|scale|max_length|length):" examples` returns nothing. No example declares them.
- The source schema does carry them: `table_payment_event.md` has `SettlementAmount | Decimal | | 18 | 4`. The canonical `Transaction.Amount` is `type: decimal` with no scale (`transaction.md`).
- `postgresql.md:98` shows `amount NUMERIC(18,2)` in its example.

**Failing scenario.** Generating the flagship `Amount` for PostgreSQL follows the dialect example and yields `NUMERIC(18,2)`. The source supplies four decimal places. Generating for Snowflake, "map precision and scale from entity YAML" finds none, so the agent picks `NUMBER(38,0)`, which truncates all decimals. Both follow the skill.

Also: `3-Entities.md:299` lists `timestamp` as an example type, but the Type System table has only `datetime`, and the `cast` list at `8-Transformations.md:89` has no `timestamp`. `3-Entities.md:83` uses `type: Decimal` (capitalised).

**Fix.** Add `precision`, `scale` and `max_length` to the attribute table, or delete the dialect language and state the default policy. Reconcile `timestamp`/`datetime` and the case of type names.
**Blocks v1?** Yes. Attribute properties are frozen grammar and the current text cannot generate lossless DDL.

### L2-06. Domain `pii` is defined as "any entity" but inherited as "every entity"; subtype inheritance is unstated

- `3-Entities.md:117`: domain `pii` = "Whether **any** entity in the domain contains personally identifiable information."
- `3-Entities.md:151`: "Every entity, relationship, and event inherits the domain's `classification`, `pii`, ... unless explicitly overridden."
- Healthcare shows the second reading: `Location` and `Organization` both declare `pii: false` (`examples/Healthcare/entities/location.md:58`, `organization.md:54`) to opt out of a `pii: true` domain.
- `2-Domains.md:192`: a specialization "inherits its attributes, constraints, and governance". `3-Entities.md:149-156` describes inheritance only from domain to entity. Telecom `Party` (abstract) declares `pii: false`, `classification: Internal` (`Telecom/entities/party.md:53-54`), while `Individual extends Party` declares `pii: true` (`individual.md:74`). Whether the parent's posture is a floor, a default or ignored is not stated, nor whether a `Party`-declared attribute is PII for an Individual instance.
- `pii` on an **attribute** (`3-Entities.md:79`) is used and relied on by `pii_fields` (`:128`) but is not in the attribute property table.

**Scenario.** A domain has `pii: true` and 60 entities. Under "any", the flag says nothing about which entities to mask. Under "default", 58 non-PII entities each need a `pii: false` override or they are treated as PII. A generator applying masking policies chooses one; an auditor reading the flag as "any" chooses the other.

**Fix.** Define domain `pii` as the default and add a separate derived summary if "any" is wanted. State the chain domain, parent entity, child entity with precedence. Add `pii` to the attribute table.
**Blocks v1?** Yes.

### L2-07. "Longest retention wins" is the only conflict rule and cannot express a maximum-retention obligation; the Governance agent contradicts itself

- `9-Data-Products.md:519`: "Retention: longest wins."
- `agents/agent-governance/skills/compliance-audit/SKILL.md:143`: conflict default "Retention | The longer period". `AGENT.md:92-93`: "apply the more conservative requirement by default". The same skill, `:148-149`, says "don't apply either side until the conflict has been reviewed", and its report template has a "Default applied" column (`:197`). Three instructions, two behaviours.
- `3-Entities.md:125-135`: entity governance has a single `retention` field. There is no field for a minimum, a maximum, an anchor event, or an erasure exemption.
- `agents/agent-governance/skills/regulatory-compliance/regulators/gdpr.md:25` says retention "depend[s] on the legal basis and purpose". Telecom lists GDPR in scope (`Telecom/domain.md`, `regulatory_scope`) and its fraud product settles on `retention: "10 years"` (`Telecom/products/fraud-intelligence.md:49`) by the longest-wins rule, because the Financial Crime side needs 10 years.
- `Compliance Audit` severities (`:153-162`) flag retention **below** the minimum. No severity exists for retention **above** a maximum.

**Scenario.** A product combines a domain bound by a minimum record-keeping period with one bound by a storage-limitation principle. Longest-wins retains personal data for the longer period. Whether that is lawful is a legal question I cannot answer (see "What I Cannot Evaluate"), but the standard gives a structural answer with no way to record the constraint that opposes it, and the Governance agent's own limits section concedes "'Most conservative wins' is a safe default, not always the legally correct answer" (`AGENT.md:112-113`).

**Fix.** Split `retention` into `retention_min` and `retention_max` (or a structured `retention:` with `minimum`, `maximum`, `anchor`, `erasure_exemption`). Make the conflict rule "surface, do not resolve" in both spec and agent, and reconcile the three Governance instructions.
**Blocks v1?** Yes. The rule is normative in §9 and would be frozen.

### L2-08. Multi-domain conflict detection compares domain defaults only; both cross-domain flagship products get the scope union wrong

- `9-Data-Products.md:506`: "compare the owning domain's governance defaults with the referenced domain's defaults". Entity-level overrides are never consulted.
  Concrete: Telecom's domain is `classification: "Confidential"` and its `Billing Account` entity is `Highly Confidential` (`Telecom/entities/billing_account.md:96`). A product owned by a Confidential domain that consumes Billing Account through lineage triggers no conflict.
- `9-Data-Products.md:523`: "Regulatory scope: union of frameworks. ... The owning domain's `regulatory_scope` does not shield the product from obligations in the referenced domains."
- Financial Crime `regulatory_scope`: AUSTRAC AML/CTF Act 2006, NZ AML/CFT Act 2009, APRA CPS 234, FATF (`domain.md:21-25`). Healthcare: HIPAA, HITECH, 21st Century Cures (`Healthcare/domain.md`).
- `Patient Financial Fraud Detection` (`products/patient-fraud-detection.md:55-64`) claims "Regulatory scope union across both contributing domains" and lists FATF plus generic AML, KYC, CTF, then **BSA, EU 5AMLD / 6AMLD, USA PATRIOT Act**. It omits AUSTRAC, NZ AML/CFT and APRA CPS 234 from Financial Crime, and BSA, EU AMLD and PATRIOT appear in neither domain.
- `Healthcare/products/billing-fraud-detection.md` carries the same list. The two products are copies with the same comment text ("Longest wins", "PII/PHI union").
- Retention: Financial Crime is "10 years post relationship end", Healthcare is "7 years post last encounter". The product writes `"10 years"`, dropping the anchor event (`patient-fraud-detection.md:51`). "Longest" is not comparable across anchors.
- Whether pushing Sanctions Screen Status and Risk Rating to a consumer team named "Clinical Revenue Integrity" (`patient-fraud-detection.md:18`) is acceptable under AML confidentiality rules needs a specialist. I flag it, I do not assert it.

**Fix.** Detect conflicts against entity effective governance, not domain defaults. Require retention to carry an anchor and define comparison only for equal anchors. Recompute the flagship scope union from the two domain blocks.
**Blocks v1?** Yes for the rule text. The example fix can follow.

### L2-09. Consumer products "source only from canonical products" but no domain-aligned product publishes their entities, and lineage cannot name a product

- `9-Data-Products.md:47`, `:229` and `:440`: consumer-aligned products source "exclusively from canonical (domain-aligned) products". `:210-229` declares lineage as `domain` plus `entities`. There is no way to name the product read. (Layer 1 S17 flagged the entity/product wording; this shows the consequence.)
- Financial Crime's only domain-aligned product, `Canonical Party` (`products/canonical.md:12-31`), publishes Party, Person, Company, Party Role, Customer, Contact Address, Address.
- `Transaction Risk Summary` lineage (`products/analytics.md:24-35`) draws on Transaction, Payer, Payee, Account and Branch. `Patient Financial Fraud Detection` draws on Transaction and Account (`patient-fraud-detection.md`). None of those five entities is in a domain-aligned product. The product's own text says "Financial Crime entities from Canonical Party" (`patient-fraud-detection.md:97`), which is false for Transaction and Account.
- `9-Data-Products.md:68` (`platform.product_scope`) lets a domain narrow which classes it recognises (Brownfield Retail excludes source-aligned, `domain.md`). A domain that declared `product_scope: [consumer-aligned]` would make "source only from canonical products" unsatisfiable.

**Fix.** Either lineage names a product (`product: Canonical Party`) and the rule is checkable, or the rule is restated as "from canonical entities", which is what the examples do. Add a rule that consumer lineage entities must be published by a domain-aligned product of the referenced domain, or drop the rule.
**Blocks v1?** Yes. It is a stated "never".

### L2-10. Payer, Payee and Payment Initiator collapse many rows into one instance with no `deduplication`

- `8-Transformations.md:501` (Rule 8): "A `derived` transformation suffices when the identifier comes deterministically from the row itself ... **and no two rows describe the same instance**. Where rows must collapse into one instance, a `deduplication` transformation is required."
- `7-Sources.md:269`: `deduplicated: true` "when instances collapse across source rows. Requires a `deduplication` transformation."
- `table_payment_parties.md:15-24`: `Payer` and `Payee` entries use `identity: Derive Payer Role Identifier` (a `derived` transformation) with no `deduplicated`. `:38`: "A Payer or Payee role is shared by every payment its party makes or receives." So every payment by party P-1001 produces the same `PAYER-P-1001`. `table_initiation.md:15-18` does the same for `Payment Initiator`.
- `LIFECYCLE.md` 2.0.0 confirms the design: roles "keyed on their parties (`PAYER-`, `PAYEE-`, `INIT-` prefixes)".

**Failing scenario.** Two payments from P-1001. Under Rule 8 as written, the pipeline must reject or flag two rows describing one instance, or the fan-out must declare `deduplicated: true` with a survivorship rule. As authored it does neither. Generator A upserts (Reading 1); generator B inserts twice and violates the primary key (Reading 2). Agent Test's Step 1 checks (`worked-example-compilation/SKILL.md:35-43`) have no check for this, so no agent catches it.

**Fix.** Either add `deduplicated: true` and a `deduplication` transformation with survivorship to those three entries, or relax Rule 8 to allow a `derived` key to repeat across rows when the entity has no row-level attributes. Decide, then make the flagship comply. (A modelling question sits behind this, whether a per-payment role should be a persistent Party Role at all, which needs the domain owner.)
**Blocks v1?** Yes. The flagship must pass its own normative rules before the standard freezes them.

### L2-11. The dedup key can merge unrelated instances; the Address key omits city and merges on null postcode

- `8-Transformations.md:221`: "A null value contributes an empty string." No rule says what happens when every component is null or when a branch's key is too weak to identify.
- `table_contact_point.md:56-69`: Address key = normalised `Street | PostalCode | Country`. `City` is nullable and not in the key. `PostalCode` is nullable (`:41`, Nulls "yes").
- `entities/address.md` (attributes) has `Suburb`, `City`, `State Or Region`, all outside the key.
- The address entity is described as the shared node for shared-address network detection (`domain.md:146`).

**Failing scenario.** Two unrelated parties both have `1 Main St`, no postcode, country `AU`, one in Sydney and one in Perth. Both normalise to `ADDR:1 MAIN ST||AU` and become one Address. Both Contact Addresses point at it, so the domain manufactures a shared-address link between unrelated parties, in an AML domain, and `earliest` keeps the first row's city. Nothing in the worked examples covers a null-postcode row.

Other underdetermined points in the same rule:
- Whether the order of `normalise` operations matters is not stated (`:218` lists them; the example at `:205` orders them). It can matter: `strip_punctuation` then `collapse_whitespace` turns `A - B` into `A B`, while the reverse leaves two spaces.
- `|` inside a value can create collisions (`"A|B","C"` and `"A","B|C"` compose the same key). No escaping rule.
- Numbers and dates in `using` (DPID_N is `NUMBER` in the spec example) have no defined string form (leading zeros, scale).
- Survivorship `earliest` on an entity the model calls `reference`/immutable: a late-arriving earlier-created row (out-of-order CDC) either rewrites the "first recorded" values (Reading 1) or is ignored (Reading 2). The text says "later rows never overwrite the first recorded values" (`:223`), which describes arrival order, while `earliest` describes timestamp order.

**Fix.** Add a "minimum identifying key" rule (a branch whose components are all null is unconditional-invalid and rejects), define normalisation order, delimiter escaping and scalar string forms, and say whether `earliest` is by timestamp or arrival. Add city (or a null-postcode branch) to the flagship key and a worked example for it.
**Blocks v1?** Yes for the key composition rules. The example fix can follow.

### L2-12. Bitemporal entities have no way to designate a valid-time source; contribution rules cover 3 of 5 mutability values

- `3-Entities.md:262-269` defines `valid_time`, `transaction_time`, `bitemporal`. Nothing in §7 or §8 lets a transform say which source column is the valid-time start of a version.
- Financial Crime `Party` is `bitemporal` and the description says "Valid time captures when the party information was true ... required to support ... Suspicious Matter Report evidence" (`entities/party.md`, temporal block). Yet `SanctionsScreening` has three columns: `PartyExternalId`, `ResultCode`, `MatchFlag` (`table_sanctions_screening.md:31-33`). No screening timestamp exists in the extract or the transform. A contributed `Sanctions Screen Status` version has a transaction time (ingest) and no source-derived valid time.
- `Contact Address` models its own `Valid From`/`Valid To` as ordinary attributes mapped from source columns (`table_contact_point.md:47-48`), which is a second way to express validity.
- `7-Sources.md:278` describes contributions for "transaction-time or bitemporal tracking, including an `append_only` one", `slowly_changing`/`frequently_changing`, and `immutable`. Not covered: `reference`, `append_only` with **no** temporal tracking, and `append_only` with `valid_time` only.
- A contribution to an abstract entity (`Party`) "follows the target entity's temporal tracking". Subtypes may differ (`Telecom/entities/party.md` is `reference`, its subtypes `slowly_changing`), and a contributor that "may not know its subtype" (`:276`) cannot know which rule applies. If a subtype were `immutable`, the contribution would be illegal, undetectably at design time.
- `8-Transformations.md:162` (`earliest`) says it "suits immutable reference data", while `7-Sources.md:278` says an `immutable` entity "accepts no contributions". A cross-source `earliest` reconciliation on an immutable entity, where the second source's row arrives second but is earlier, needs a rewrite.

**Fix.** Add `valid_from:`/`recorded_at:` mapping keys to transformation or fan-out entries for temporal entities. Complete the contribution table for all five mutabilities and both tracking axes. State whether subtypes may relax the parent's mutability.
**Blocks v1?** Yes for the valid-time mapping (it is a grammar addition); the rest is text.

### L2-13. Consumer `Path` traversal has no multiplicity rule; the flagship path is invalid and multiplies the grain

- `9-Data-Products.md:284`: "A Path column captures the relationship traversal". No text says what a to-many hop means for a wide-column row (one row per grain instance): first, aggregate, or multiply.
- `products/analytics.md:112-116`: `Account Identifier | Account.Account Identifier | Transaction → Payer → Customer → Account`. Payer and Customer are sibling subtypes of Party Role; `grep` of `payer.md`, `customer.md` finds no Payer-to-Customer relationship. `Customer Holds Account` is many-to-many (`customer.md:73-90`). Transaction already has a direct `Transaction Has Debit Account` (`transaction.md:231`).
- A customer with three accounts yields three rows per transaction (Reading 1) or an arbitrary one (Reading 2), on a product whose grain is the transaction.

**Fix.** Define traversal multiplicity (require `first|any|aggregate` on to-many hops, or forbid to-many hops). Fix the flagship path to use the declared debit-account relationship. Make path steps resolvable in pre-flight.
**Blocks v1?** No, if the spec adds a "to-many hops are undefined; do not use" note. Otherwise yes.

### L2-14. Constraints that encode process rules contradict worked examples; `check` language and `lifecycle_stage` are undefined

- `entities/party.md:108-110`: `Confirmed Sanctions Match Blocks Service` is `check: "Sanctions Screen Status != 'Confirmed Match'"` with `lifecycle_stage: Onboarding`. The SAP worked example produces exactly that status (`table_sanctions_screening.md`, "Confirmed match" example). `Agent Test` derives data tests from constraints "as declared" (`test-strategy/SKILL.md:54`). The resulting test fails on the instance the source contract creates.
- `party.md:103-104`: `Review Date Must Not Be Overdue` is `check: "Next Review Date >= Today OR Party Status == 'Under Review'"`. It changes truth with the clock and no data change. `Today` versus `today()` (`8-Transformations.md:123`): the expression language for `check` is not defined anywhere.
- `3-Entities.md:338`: `lifecycle_stage: [Registration, KYC Complete]` has no vocabulary and no way to declare which stage an instance is in.
- `party.md:98-99`: `Legal Name Required` is unconditional `not_null`. `table_account.md:108-124`, example "Suspended person account", produces a `Party · Person` with no Legal Name asserted, and the Account table has no source for a Person's Legal Name (it comes only from Contact). Under `nullable-staging` this is allowed. If the Contact row never arrives for a Person, the constraint is permanently violated.

**Fix.** Separate invariants from process rules (a `policy:` or `control:` block that generates no data test). Define the `check` expression language and reserve `lifecycle_stage` as a declared vocabulary or drop it. Note in Test Strategy how time-dependent checks are tested.
**Blocks v1?** No, but the expression language definition should ship with 1.0 since it is used in normative examples.

### L2-15. The same source is identified three ways and the spec's own examples disagree

- `7-Sources.md:86`: the stable identifier is `id: salesforce`.
- `9-Data-Products.md:173`: `source: salesforce-crm`. `:188`: "The source system identifier matching a folder under `sources/`". `:208`: "Each `source` value must match a declared source system." The folder name is a path, which contradicts `7-Sources.md:40` ("locate content by heading hierarchy, not by path").
- Table identifiers: `7-Sources.md:175` links `table_ACCOUNT` (source casing, as `:57` says). `9-Data-Products.md:200` lineage uses `table_account`. `:208`: each `tables` entry "must match a source table declared in that source system's feeds table". Which spelling is the key?
- Financial Crime works only because its ids equal its folder names and its file names are lowercase.
- `7-Sources.md:552` (Rule 5): an attribute in a feed table "but has no corresponding transformation for that source ... is a validation error". Direct mappings are declared in the Destination cell with no `Transform:` heading (`:302`), and Financial Crime Feeds rows list direct-mapped attributes. Literal reading makes every direct mapping an error (see also L2-M8).

**Fix.** Pick `id` as the only key for `source:` and lineage, and the transform heading text as the table key. Fix §9 examples and rule 9. Restate Rule 5 to say direct Destination mappings count.
**Blocks v1?** Yes. These are `must match` reference keys.

### L2-16. Relationships and `extends` cannot cross domains; lineage cannot pin a version; lineage is unidirectional

Scale and evolution stress: a 100-entity domain, split into several domains.

- Sizes. `examples/Financial Crime/domain.md` is 23,289 bytes for 22 entities, 25 enums, 28 relationships, 7 events and 5 products (entities table 5.9 KB, relationships table 6.4 KB, 60 BIAN URLs 4.1 KB). Linear extrapolation to 100 entities is about 100 to 115 KB, or on the order of 25,000 to 30,000 tokens for the summary file that `2-Domains.md:252` tells agents to ingest first ("AI Scoping"). There is no subject-area or package grouping inside a domain, so splitting into several domains is the only route. This is an estimate, not a measurement.
- `entity-references` requires `extends`, `source`, `target`, `entity` to name "an entity defined in the domain" (`guides/validation-tooling.md`, rule table). The spec provides cross-domain naming only in product attribute mapping (`9-Data-Products.md:281,352`: `Domain.Entity.Attribute`). So after a split, every relationship, inheritance link and event whose ends lie in different domains has no syntax: `Customer extends Party` where Party moved to a Party domain is inexpressible.
- Identity. `9-Data-Products.md:229`: `domain` in lineage must match the referenced domain's H1 text. Renaming a domain breaks every consumer silently. There is no domain id.
- Pinning. Lineage entries carry `domain` and `entities` only (`:212-227`). A consumer cannot record which domain version it was built against.
- Impact. `:231`: multi-domain lineage "does not create an inverse reference entry". The owning domain therefore cannot list its external consumers. The Financial Crime 2.0.0 `LIFECYCLE.md` `affected_products` lists only Financial Crime's own products. Healthcare's `Clinical Billing Fraud Detection` also consumes Financial Crime's Transaction, Party and Account (`Healthcare/products/billing-fraud-detection.md`), and is invisible to that analysis.
- Cycles. Financial Crime's `Patient Financial Fraud Detection` consumes Healthcare entities and Healthcare's `Clinical Billing Fraud Detection` consumes Financial Crime entities. There is no rule about cyclic cross-domain dependency, and each product's "unidirectional" statement is true while the domains depend on each other.

**Fix.** Define cross-domain entity reference syntax for `extends`, relationships and events. Add an optional `domain_id` and a `version` (range) on lineage entries. Make the inverse index a tooling requirement (generated, not authored) or add a `consumers` registry.
**Blocks v1?** Yes. The Data Autonomy claim depends on multi-domain federation, and reference syntax is frozen grammar.

### L2-17. "Breaking" is defined as "different or incorrect output", which makes every additive change breaking; the guide contradicts the definition and itself

- `2-Domains.md:278`: "A change is **breaking** if a correctly-authored downstream consumer ... would produce **different or incorrect** output after the change is applied."
- `guides/lifecycle-versioning.md:31`: adding "a new entity, attribute, relationship, event, enum value, or constraint" is Additive, a minor bump. Adding an attribute changes regenerated DDL, so by the spec's definition it is breaking.
- The guide restates the definition at `:36` ("different or incorrect") and then defines non-breaking at `:44` as "continue to produce correct output" (dropping "different"). `:31` lists "a constraint" as additive, `:42` says changing constraints is breaking if it narrows the valid domain. Adding a constraint narrows it.
- Financial Crime 2.0.0 classifies a corrected cardinality as breaking (correct by the guide) and the new `Person` attributes as additive (`LIFECYCLE.md`), which under the §2 definition would themselves be breaking.

**Fix.** Define breaking as "a correctly-authored consumer produces incorrect output or must change to keep working", matching the guide's own product rule (`:171`). Fix the constraint entry.
**Blocks v1?** Yes. It is the versioning contract that 1.0 promises.

### L2-18. Handoff protocol: file naming is ambiguous, the one-pending rule discards unconsumed work, and `consumed` is set on read

- `agents/CONVENTIONS.md:24`: look for `handoff-to-<your-id>.md`. `:64`: the name is `handoff-to-<agent-id>.md` with examples `handoff-to-artifact.md`, `handoff-to-test.md`. `:70-71`: the frontmatter `from`/`to` hold "agent ID (e.g. `agent-ontology`)". So an agent whose id is `agent-artifact` looks for `handoff-to-agent-artifact.md` and the file is named `handoff-to-artifact.md`. The flagship's own handoff file has `to: agent-artifact` in the frontmatter and the short name on disk (`examples/Financial Crime/handoff-to-artifact.md`).
- `:79`: "Only one `pending` file per destination may exist. Archive the previous one before writing a new one." Receiving rule 4 (`:28-29`): `archived` files are history, "don't act on their Task". If Governance and Ontology each need Architect in the same domain, the second sender must archive the first sender's unconsumed task, which the receiver is then told not to act on.
- `:24`: the receiver "set[s] it to `consumed`" on reading, before work is done. If the session ends, the task is history and is not picked up again.
- The archived example is also stale against the model: it says "Party Identifier is the natural primary key — no surrogate needed", while `entities/party.md` describes Party Identifier as a "Globally unique surrogate identifier".

**Failing scenario.** Governance finds a masking gap and writes `handoff-to-architect.md` (pending). Ontology finds a missing entity that changes a product and needs the same Architect handoff, so it archives Governance's. The Architect session opens, reads only Ontology's, and Governance's masking fix is silently dropped.

**Fix.** One id scheme (`artifact`, not `agent-artifact`) in both places, or filename `handoff-to-agent-artifact.md`. Allow several pending files distinguished by sender. Set `consumed` at completion, or add an `in-progress` state.
**Blocks v1?** Yes for the naming (file convention shipped to users). The rest can follow.

### L2-19. No downstream agent implements 0.10 source-layer semantics; Agent Test cannot compile contributing-table examples

- `grep -rniE "contributes|when_absent" agents/` finds only `source-mapping/SKILL.md` and an unrelated FHIR terminology file. Agent Artifact, Agent Test and Agent Architect never mention them. `grep -rni "earliest" agents/` returns **nothing**.
- `agents/agent-artifact/references/generation-semantics.md:88`: "`references` becomes the foreign key wiring between instances produced from the same row". It omits the other meaning (an existing instance; `Reference:` destinations). `:100`: "`survivorship` ... `most_recent` uses the declared `timestamp_field`". No `earliest`, no `contributes`, no `hold`/`reject`.
- `source-mapping/SKILL.md:255` lists survivorship strategies as `priority_non_null`, `priority_always`, `most_recent`, `consensus`, omitting `earliest`. `:168` lists the `produces:` keys without `contributes` or `when_absent`, then describes them a few lines later.
- `agent-test/skills/worked-example-compilation/SKILL.md:94-104` compiles `given` as only the listed source columns. `7-Sources.md:276` says an example for a contributing table "assumes the instance exists". The skill has no step for seeding that instance. Five Financial Crime tables are contributing (`table_contact.md`, `table_sanctions_screening.md`, `table_customer_risk_profile.md`, `table_initiation.md`, `table_payment_parties.md`). Their unit tests, compiled as written, feed one row into a model with no pre-existing instance: under `hold` (default) the expected rows are empty.
- Step 1 check `:43`: "a contributing source whose Entity Fan-Out does not declare the entity". The SAP fan-in example produces `Party · Company` (`table_account.md:164`) while SAP's fan-out declares `Party` (`table_sanctions_screening.md`, Fan-Out). Read literally, Agent Test reports a declaration defect on the flagship's own fan-in example and stops.
- Step 1 `Cardinality` check (`:42`) does not say "per source row". The multi-row example in `table_contact_point.md` ("Two parties at the same address") lists two `Contact Address` instances against a fan-out `cardinality: 1`.

**Failing scenario.** A user asks Agent Test to compile the Financial Crime examples. The unit tests for the five contributing tables either have empty expectations or are blocked by Step 1 findings; the model that implements the contribution (Agent Artifact) has no instruction that it should exist.

**Fix.** Add contribution, hold/reject, `earliest` and `references` semantics to `generation-semantics.md`, the dbt skill and Agent Test, and a seeding step for contributing examples. Make the Step 1 checks per-row and subtype-aware.
**Blocks v1?** Yes. These are the headline features of the release and the agents claim to consume them.

### L2-20. Ontology's "every entity gets `identifier: primary`" rule reintroduces the defect Financial Crime 2.0.0 fixed

- `agents/agent-ontology/AGENT.md:83`: "Give every entity an `identifier: primary` attribute." `domain-review/SKILL.md:274`: "All entities have an `identifier: primary` attribute, or are deliberately Logic Objects." `3-Entities.md:365`: "Every Entity should have at least one attribute marked as an identifier".
- `examples/Financial Crime/LIFECYCLE.md:48` (a breaking change in 2.0.0): "Party Role subtypes no longer declare a second primary identifier. Customer Number, ... are now `identifier: alternate`; Role Identifier is the only primary key." `customer.md:40`, `payer.md:32` are `alternate`; `party_role.md:71` holds the only `primary`.
- Nothing in the spec says whether an inherited `primary` satisfies the rule, or what two `primary` attributes on one entity mean (composite key, or an error). `grep composite` over §3 finds nothing.

**Failing scenario.** An agent following the Ontology rule adds `identifier: primary` to `Payer`, so Payer has two primaries. Or Domain Review checks each entity's own YAML and rates Customer, Merchant, Payer, Payee, Teller and Payment Initiator Not Ready. Both outcomes contradict the flagship.

**Fix.** State that a subtype inherits its primary identifier and must not declare another unless it deliberately redefines the key; define multiple `primary` (composite or error). Reword the two agent rules.
**Blocks v1?** No for the agent wording. Yes for the composite-key definition if the standard keeps `identifier: primary` on more than one attribute.

### L2-21. `cardinality: 0..*` in Entity Fan-Out has no mechanism to enumerate the instances

- `7-Sources.md:266`: `cardinality` is `1`, `0..1` or `0..*` ("Instances emitted per source row"). `identity` (`:268`) determines one instance's identifier.
- Nothing describes how one row yields N instances: no unpivot, no array element source, no index in the identity. `grep -i "unnest\|explode\|repeating\|foreach"` over the spec is empty. Array attributes exist (`3-Entities.md:317-324`) but no transformation builds one from columns.

**Failing scenario.** A legacy customer table has `PHONE1`, `PHONE2`, `PHONE3`. The model has a `Phone Number` entity. The author writes `cardinality: 0..3`-style intent as `0..*`. The identity for each instance cannot be derived from `identity` alone, so generators differ (three rows via unpivot, one row with an array, or only PHONE1).

**Fix.** Add a repeat construct (`for_each: [PHONE1, PHONE2, PHONE3]` with an index available to `identity`) or state `0..*` requires a child table. Add an array-building transform.
**Blocks v1?** No; document it as out of scope if not added. Repeating groups are common in exactly the brownfield sources the adoption model targets.

### L2-22. Default `when_absent: hold` is unbounded and silent; a confirmed sanctions match on an unknown party is invisible

- `7-Sources.md:272`: `hold` (default) "keeps the row until the instance exists". No timeout, maximum queue, alert, or dead-letter behaviour. `9-Data-Products.md:409`: `eventual` means "the product converges within `sla.freshness`". A held row never converges.
- `table_sanctions_screening.md:23`: "A screening row for an unknown party is held until the CRM establishes it." The same file maps `CONFIRMED_MATCH` to `Confirmed Match`, and its fallback comment says "A new engine code must never silently clear a party" (`Map Sanctions Screen Status`). A screening hit on a counterparty that the CRM never establishes (the flagship itself records this for wire counterparties: `table_payment_parties.md` OD-1) is neither in the canonical model nor reported.
- `Canonical Party` declares `sla.freshness: "< 1 hour"` (`canonical.md`), which cannot be met for held rows.
- A test agent cannot check any of it: see L2-02(d).

**Fix.** Give `hold` a bound (`hold_for: 24h` then `reject` or `escalate`) and require a declared destination for rejected/held rows (a quarantine entity or report). Add a governance note that compliance signals must not be silently held.
**Blocks v1?** No for the bound. Yes for the wording of the default if the standard keeps "default hold".

### L2-23. No way to declare an attribute or relationship as unsourced; the flagship has at least eight unsourced entities and consumer products map unsourced attributes

- `7-Sources.md:324`: "A blank `Destination` means the column is deliberately not mapped." That covers source columns. Nothing covers target attributes, entities or relationships with no source.
- Financial Crime: no source mentions `Transaction Date Time`, `Transaction Type`, `Opened Date`, `Risk Rating`, `Next Review Date`, `Role Status`, `Due Diligence Status` (each 0 hits under `sources/`), and none feeds Merchant, Teller, Branch, Agreement, Loan Agreement, Term Deposit Agreement, Exchange Rate or Product (`Product` has OD-1). `Transaction Date Time` is described as "the primary event time for transaction monitoring rule evaluation" (`transaction.md`).
- `Transaction Risk Summary` maps `Transaction.Transaction Date Time`, `Party.Risk Rating`, `Account.Opened Date`, `Branch.Branch Code` and `Branch.Branch Name` (`analytics.md`, Attribute Mapping). `Patient Financial Fraud Detection` maps `Transaction Date Time`, `Risk Rating`, `Opened Date`, `Closed Date`. Every one is lineage to a canonical attribute that no source populates.
- `Address Type` is unmapped, so the constraint `Street Address Requires Address Line 1` (`address.md`) can never fire, and a PO Box row (`table_contact_point.md`, example 2) lands in `Address Line 1`.

**Fix.** Add an attribute/entity-level coverage declaration (`sourced: false` with reason, or a coverage report generated by Agent Ontology) and a pre-flight or review check that consumer attribute mappings resolve to sourced attributes.
**Blocks v1?** No. It is a modelling-honesty gap, but the flagship should demonstrate the convention.

---

## Minor findings

ID | Where | Finding | Blocks v1?
--- | --- | --- | ---
L2-M1 | `5-Relationships.md:99-110`; `entities/party.md:180-181`, `customer.md:85` | `relationship_attributes` are untyped (a list of names). Financial Crime invented `Association Type (enum:Association Type)` inline in the string; date attributes such as `Holder Start Date` have no type at all. A generator cannot type them | No
L2-M2 | `8-Transformations.md:39-50` | Expression semantics are undefined for null propagation in `+` and `trim`. `table_contact.md:42` uses `coalesce(Given Name, '')` to survive a null; the spec's own `Full Name` example (`8-Transformations.md:106`) would yield null or "None Last" depending on the target platform. The dedup key defines null as empty (`:221`), so the two rules disagree | No
L2-M3 | `8-Transformations.md:360-362` | `aggregation` `grain.join_on: Loan Agreement Number` names an entity attribute but no source column that groups the rows. The group key is undeclared, and §7 forbids joins between source tables | No
L2-M4 | `6-Events.md:119,53-83,137` | Event Rule 9 says every event "MUST have a timestamp or a sequence attribute". The spec's full Event Definition example has no `attributes:` block. The Example Event uses the snake_case attribute `updated_fields` (against the natural-language naming rule at `3-Entities.md:377`) and `type: array` (not in the type system) | No
L2-M5 | Financial Crime `domain.md:223`, `entities/transaction.md:206`, `entities/party_role.md:11` | The old name "Instructing Agent" remains in the events summary table (actor), a relationship name and prose, while the event detail says `actor: Payment Initiator` and the entity is Payment Initiator. Summary and detail disagree, which the spec says must agree | No
L2-M6 | `entities/address.md:40`, `Healthcare/entities/practitioner.md`, `Telecom/entities/party.md:39` vs `3-Entities.md:287`, `generation-semantics.md:23` | `mutability: reference` ("essentially static, managed by a small number of administrators") is used for Address (loaded from CRM by deduplication), for Practitioner (people) and for an abstract Party whose subtypes are `slowly_changing`. Generation maps `reference` to "Small lookup table; seeded/managed data pattern". `7-Sources.md:270` also treats `reference` entities as needing no source. So a source-built Address is exempt from reference checks (see L2-02e) and is generated as a seeded lookup | No
L2-M7 | Financial Crime `Currency` | Currency is `reference` and "maintained outside the sources" (`table_account_ref.md`, intro). Nothing declares who loads it, so the references from `Account` and `Transaction` point at a table no source populates. Currencies are also modelled twice, as the `Currency Code` enum and the `Currency` entity (`domain.md:153,172`) | No
L2-M8 | `7-Sources.md:552`, `:302`, `:266`; `8-Transformations.md:419`; `7-Sources.md:190` vs `:276` | Four small rule collisions: Rule 5 vs direct-mapping shorthand (L2-15); fan-out `cardinality` means "per row" but the same key in an example means "count across all given rows" and adds a value `0` outside the fan-out vocabulary; the Feeds rule "list the subtypes actually instantiated, not the abstract parent" (`:190`) contradicts contributing entries that must name the abstract parent (`:276`) and Financial Crime's SAP Feeds row lists `Party` (`sap-fraud-management/source.md`). The source-mapping checklist (`SKILL.md:321`, "Concrete subtypes listed, not abstract parents") would flag it | No
L2-M9 | `2-Domains.md:244,268-274`; `3-Entities.md:209`; `9-Data-Products.md:147`; Layer 1 S2 | Three status vocabularies: domain and entity have five values with `Review`, product has four. A product in a domain under `Review` cannot itself be `Review`. Layer 1 S2 cites the four-value list for domains | No
L2-M10 | `5-Relationships.md:99-110` vs `3-Entities.md:277`; `entities/party_role.md:177-195` vs `entities/party_role.md` temporal block; `9-Data-Products.md:406-415` | Several constructs give two ways to say one thing. A many-to-many with attributes is either an `associative` entity or `relationship_attributes`, with no guidance. Point-in-time state is either `temporal: bitemporal` or a self-referential `snapshots` relationship, which `generation-semantics.md:36` would realise as a bridge table joining each role to itself. `strong` and `eventual`+`reject-partial` both hold rows until every source arrives (`product-design/SKILL.md:185` calls it "effectively strong"). `interim` states describe the canonical instance but are justified by a product's posture (`8-Transformations.md:471`), and a `strong` product with an `interim` example is contradictory across two agents' files | No
L2-M11 | `Healthcare/entities/patient.md` (retention_basis), `Telecom/entities/billing_account.md:96-101`, `Healthcare/entities/patient.md` | Regulatory citations needing SME confirmation: the Patient retention basis says "HIPAA requires retention of medical records for a minimum of 6 years"; Billing Account says records "are subject to PCI-DSS data retention requirements" and cites PCI Requirements 3 and 7, which are about protecting and restricting stored data. I cannot verify either and flag them because a reviewer could not tell from the file whether the cited provision supports the stated period. Governance regulator files for HIPAA and others carry `last_verified: 2025-03-08` (Layer 1 S9) | No
L2-M12 | Adoption: `10-Adoption.md:17,73`; `9-Data-Products.md:462`; Brownfield Retail `domain.md:45-55` | (a) `superseded_by: "entities/customer.md"` is a single file path, so a baseline that splits into several entities (the star-schema `fact_sales`) or several baselines that merge cannot be traced, and a file move orphans the link. It also contradicts "locate content by heading, not path". (b) "The domain advances as a whole" (`:17`) gives no rule for a domain with 5 of 60 entities canonical. (c) `progress.at_level: 3, total: 3` at `mapped` is ambiguous: complete at this level, or progress towards the next? (d) §9 refers to "maturity levels 1-2" and "4+", but §10 names levels without numbers | No

---

## Determinism exercise

Two realistic mappings from the flagship, each read two ways.

### Mapping A: Temenos payment (PaymentEvent, Initiation, PaymentParties into Transaction, Payer, Payee, Payment Initiator)

Decision point | Reading 1 | Reading 2 | Spec text | Finding
--- | --- | --- | --- | ---
A status update from PaymentEvent arrives after the channel and debtor were contributed | New version replaces attributes; contributed values become null | New version carries them forward | `7-Sources.md:278` covers contributions only | L2-02(a)
Initiation row arrives before PaymentEvent | Whole row held; INIT-P-1001 not created | Only the Transaction entry held | `:272` "keeps the row" | L2-02(c)
No `reconciliation` declared, three disjoint sources | Union: one row per source arrival | Per-attribute merge into one row | `8-Transformations.md`, Rule 3 in §7 | L2-02(b)
`PaymentParties` references `Party` that no source creates (OD-1) | Load with dangling key | Hold, reject or create stub | `:270` "never creates" | L2-02(e)
Debtor and debit account both `many-to-one` | Both NOT NULL | Debtor NOT NULL, account nullable | Relationship YAML identical | L2-03
Two payments by the same party | Upsert on `PAYER-<id>` | Insert twice, key violation | Rule 8 requires `deduplication` | L2-10
Sanctions row for an unknown party | Held forever | Rejected and reported | Default `hold`, no bound | L2-22
Contact row on a business account | Held forever | Applied to Company | `:276` "if no instance with that identity exists" | L2-02(f)

### Mapping B: Salesforce ContactPoint (Address deduplication, Contact Address)

Decision point | Reading 1 | Reading 2 | Spec text | Finding
--- | --- | --- | --- | ---
Null postcode, same street, different cities | One Address `ADDR:1 MAIN ST||AU` | Two Addresses (if city were in the key) | `:221` null is empty; key omits City | L2-11
`normalise: [trim, uppercase, collapse_whitespace]` on `" 12  harbour st "` | Applied in listed order | Applied in a fixed canonical order | `:218` lists, no order stated | L2-11
Earlier-created row arrives after a later one | Rewrites first-recorded values | Ignored (first arrival kept) | `:223` "later rows never overwrite" | L2-11
Two rows with equal `CreatedDate` | Tie broken by arrival | Tie broken by identifier | Not stated | L2-11
Row with `PurposeCode: SHIP` | Whole row rejected, no Address | Reject only the Contact Address, keep the Address | `:271` "rejects the source row" | Consistent with the spec; the example is explicit. Included to show that this point is well specified
`Party` referenced by `PartyExternalId` does not yet exist | Load with dangling key | Hold | Not stated | L2-02(e)
`Decimal(18,4)` amount in a related mapping | `NUMERIC(18,2)` | `NUMBER(38,0)` | Dialect files | L2-05

---

## Agent failure modes

Failure | Agent | Trigger | Expected | Predicted behaviour | Root cause | ID
--- | --- | --- | --- | --- | --- | ---
Second primary identifier | Ontology | "Add Payer and Merchant as party roles" | Inherits Role Identifier | Adds `identifier: primary` to each | `AGENT.md:83` | L2-20
False "Not Ready" | Ontology, then Artifact | Readiness check of Financial Crime | Ready | Customer, Payer, Payee, Merchant, Teller lack their own `primary`, so Not Ready | `domain-review/SKILL.md:274` | L2-20
Readiness demands a defaulted field | Ontology | Any relationship without `granularity` | Default `atomic` applies | Not Ready; `5-Relationships.md:77` says "If not specified, the default is atomic" but `domain-review/SKILL.md:275` requires it | Gate stricter than spec | See Validation philosophy
Conflict rule applied silently | Governance | Two frameworks, different retention | Report and stop | Applies longer period as default, per `AGENT.md:92-93`; the skill says do not apply | Contradictory instructions | L2-07
Dangling masking accepted | Governance / Architect | Audit of Transaction Risk Summary | Flag | Flags missing entries for Legal Name and Date of Birth but not the dangling ones | `compliance-audit/SKILL.md:111` | L2-04
Test compile blocked or empty | Test | "Compile the examples" on any contributing table | Runnable tests | Empty expectations under `hold`, or a Step 1 defect (SAP `Party` vs `Party · Company`) | No seeding step, no subtype rule | L2-19
Generator ignores contribution | Artifact | dbt generation for Canonical Party | Contribution models | Union of intermediate models, no hold/reject | No instruction | L2-19
Wrong survivorship taught | Ontology | "Address dedup, keep first" | `earliest` | Offers `most_recent` only, per the skill's list | `source-mapping/SKILL.md:255` | L2-19
Handoff not found | Any receiver | Domain with `handoff-to-artifact.md` | Reads it | Looks for `handoff-to-agent-artifact.md` | `CONVENTIONS.md:24` vs `:64` | L2-18
Lost governance task | Architect | Two agents hand off in one domain | Both tasks done | Only the later pending file read | `CONVENTIONS.md:79` | L2-18
Ambiguous routing | Router in `CLAUDE.md` | "Audit our customer domain" | One agent | "Review, evaluate, audit the standard itself" routes to the layered review prompts, "Compliance audit" to Governance, and Ontology's Domain Review also claims "audit". The routing table has no row for reviewing a domain model | `CLAUDE.md` routing table | Minor, not numbered

Two brief questions where I found no defect: the Agent Guide's onboarding routes users to the specialist agents consistently with the workflow list (`AGENT.md:71-81`), and I found no place where a Guide demonstration is instructed to be saved as a production file. The only Guide defect I found is the dead `review-md-ddl` route Layer 1 already reported (S12).

---

## Validation philosophy

- **`phi` instead of `pii`.** No agent prompt rejects it (`domain-review/SKILL.md:14,316`; `compliance-audit/SKILL.md:16-19`). However, the Governance Level 4 masking check is defined on `pii` markers and `pii_fields` (`compliance-audit/SKILL.md:111`). An organisation using `phi` gets its deviation logged as an observation, and whether its PHI attributes are treated as PII for the masking check depends on the agent noticing the equivalence. No synonym mapping exists. The philosophy is met in tone; the safety-relevant detection is not guaranteed.
- **Hidden rigidity.** The only place convention becomes a gate is Model Readiness (`domain-review/SKILL.md:267-281`): it requires `existence`, `mutability`, `granularity` and `ownership`, which the spec treats as optional sections or defaults (`3-Entities.md:271-273`, `5-Relationships.md:77`). It is an internal gate, not an error, but Agent Artifact refuses to generate a spec-conformant model that lacks them (`agent-artifact/AGENT.md:9-13`).
- **Scope creep of the closed set.** The set is called "fixed and closed" (`guides/validation-tooling.md:36,84`). What prevents a thirteenth rule is prose. There is no test that ties the linter's rule list to the guide (the readiness review, V1-03, found no tests at all). Two rules were added in 0.10.0, and new error-severity rules break existing CI (readiness S-07).
- **Warning tier.** `domain-table-coverage` is a legitimate observation. I found no rule using the warning tier to smuggle in a convention check.
- **Vocabulary deviation pathway.** The signal goes to the "Observations section of the review output" (`domain-review/SKILL.md:316`), which is a chat or file in the user's project. There is no path from there to the spec: no contribution guide or issue template exists (readiness S-13). The feedback loop the philosophy depends on is open at the last step.
- **Structural gaps that no agent catches.** A missing `governance:` block on an entity is caught by Governance Level 1/3. A masking entry that resolves to nothing (L2-04), a `references` key that names the wrong relationship (L2-01), and an unsourced attribute mapped by a product (L2-23) are not caught by any agent, and the gap between Tier 1 and Tier 2 is where they live.

---

## Evaluation methodology gaps

What the existing layers would miss, and why.

Gap | Missed by | Why | Mitigation
--- | --- | --- | ---
Cross-file semantic checks (masking against logical model, consumer mapping against sourced attributes, path steps against relationships) | Layer 1, linter, Layer 3 persona review | They read each file for structure or read as a persona; none compares two files' contents | Add a scripted "semantic cross-check" pass to the Layer 2 prompt; consider pre-flight rules for masking resolution and path steps
Two-way reading of a single rule on a concrete table | Layer 1, standard evaluation | Each spec sentence is true; the ambiguity appears when two sentences meet on one table | Make the determinism exercise (two compliant generations of two real mappings) a mandatory Layer 2 section
Agent lag behind the spec | Layer 1 (checks that files exist and paths resolve) | It does not diff spec vocabulary against skill vocabulary | Add a check: every key in the spec's fan-out and transformation tables appears in Source Mapping, generation-semantics and Agent Test, or is listed as unsupported
Example vs rule violations in the flagship | Layer 1 (lint clean), Layer 3 (the flagship is treated as ground truth) | The example is used as the benchmark, so departures from the spec are read as spec behaviour | Review the flagship against each "must" in §7 and §8 as a checklist, rather than the reverse
Regulatory and retention semantics | All AI layers | Needs a specialist | Have a compliance reviewer read L2-07, L2-08 and L2-M11 before any change

---

## Recommended order of work before v1

1. **Grammar decisions that freeze at 1.0** (L2-01, -02, -03, -05, -12, -15, -16): `references` key shape and relationship mapping, multi-source merge/hold semantics, cardinality vocabulary with optionality, attribute type properties, valid-time mapping, source key resolution, cross-domain references. Most are small text and vocabulary changes; L2-01 and L2-16 need a design decision.
2. **Normative rule corrections** (L2-04, -06, -07, -08, -09, -10, -11, -17): masking resolution, `pii` definition, retention model, conflict detection, consumer lineage, Rule 8, dedup key rules, breaking definition.
3. **Make the flagship pass the rules** (L2-04, -09, -10, -11, -13, -14, -23, L2-M4, -M5, -M6, -M7): the exemplar cannot ship as the benchmark while it violates Rule 8, the canonical-products rule and its own masking.
4. **Bring the agents up to date** (L2-18, -19, -20): handoff naming, contribution/hold/`earliest`/`references` semantics in generation and test skills, and the identifier rule. Then run the Agent Test compile against Financial Crime as an acceptance test.
5. **After 1 to 4**, run the readiness review's release candidate soak (V1-05) on Healthcare or Telecom rebuilt to the new grammar. If the constructs survive a second exemplar unchanged, freeze.

Items marked "Blocks v1: No" (L2-13, -14, -20 wording, -21, -22 bound, -23, Minors) can ship as documented limitations, provided the spec says so.
