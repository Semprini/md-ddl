# MD‑DDL Specification (Draft 0.9.2)

*Part of the MD‑DDL Specification. See [1-Foundation.md](./1-Foundation.md) for core principles and document structure.*

---

## **Transformations**

Transformations define how source system data is shaped and mapped into domain entities. They make the lineage from raw source field to governed domain attribute explicit, human-readable, and actionable by AI agents.

Transformations are **first-class citizens** of the source layer. They are declared in transform detail (see [Section 7 — Sources](./7-Sources.md)), not alongside entity definitions. The canonical domain model contains no source references — it defines meaning, not origin.

**This section defines the transformation type vocabulary** — the available types, their YAML syntax, and the expression language. Where transformations are declared and how they are organised is defined in Section 7.

---

### **What Transformations are not**

- **Not constraints.** A constraint defines what valid data looks like once it arrives in the domain. A transformation defines how data gets there. Keep them separate.
- **Not orchestration.** When a transformation runs, in what order, triggered by which event — that is a pipeline concern. MD-DDL declares the logic; the generating agent produces the pipeline artefact.
- **Not documentation of existing pipelines.** Transformations define the *intended* mapping as the source of truth. Existing pipelines should be aligned to the model, not the other way around.

---

### **Transformation Declaration**

Transformations are declared in transform detail, organised by source table. That structure — the source schema table, `Destination` column mechanics, and heading hierarchy — is defined in [Section 7 — Sources](./7-Sources.md); this section defines only the transformation types themselves.

Each non-direct transformation is declared under its own heading following the Key-as-Name principle. The heading text, with the `Transform: ` prefix removed, is the transformation's identity in the Knowledge Graph:

```markdown
##### Transform: Concatenate Name Parts
```

A short prose description of the business intent follows the heading, before the YAML block.

---

### **Transformation Definition**

All transformations share a common envelope:

```yaml
type: <transformation type>
target: Entity · Attribute
```

`type` and `target` are always required. Everything else depends on the type.

A transformation may also declare `quality_check: false` to indicate that a null target attribute after the transformation runs is legitimate (by default, generated quality tests assert non-null).

`target` uses `Entity · Attribute` notation. The entity name must match an entity in the canonical domain model. The attribute name must match an attribute declared in that entity's YAML block, or one inherited from its parent. Both are validated during generation.

Where `target` names an attribute declared on an **abstract** entity, the transformation states which attribute is populated but not which concrete instance receives it. That binding comes from the `produces:` block described under [Entity Fan-Out](./7-Sources.md#entity-fan-out) — the fan-out entry whose `condition` matched determines the concrete subtype. A transformation targeting an abstract entity without a corresponding fan-out declaration is a validation error.

Within transform detail, `source.system` is **omitted** — it is implicit from the owning source. Only the field path within the source system is declared:

```yaml
source:
  field: Contact.Email
```

See [Section 7 — Sources](./7-Sources.md) for the source idiosyncrasy annotations (`null_as`, `quality`, `format`, `normalise`) available on `source:` blocks.

---

### **Transformation Types**

#### `direct`

A one-to-one field map with an optional type cast. Use when the source field and domain attribute are semantically identical but may differ in name or type.

````markdown
##### Transform: Account Number
Maps the legacy account identifier from the core banking system.

```yaml
type: direct
target: Account · Account Number
source:
  field: ACCT_MASTER.ACCT_NO
  cast: string
```
````

---

`cast` is optional. Valid values match the MD-DDL type system:
`string`, `integer`, `decimal`, `boolean`, `date`, `datetime`.

---

#### `derived`

Computes a domain attribute from one or more source fields using an expression.
Inputs are named and declared separately from the expression so they can be
individually traced.

````markdown
##### Transform: Full Name
Combines given and family names from CRM into a single display name.

```yaml
type: derived
target: Customer · Full Name
expression: "trim(First Name) + ' ' + trim(Last Name)"
inputs:
  First Name:
    field: Contact.FirstName
  Last Name:
    field: Contact.LastName
```
````

**Expression syntax** uses natural-language input names as operands, matching
the keys declared in `inputs:`. Supported operations:

Operation | Syntax | Example
--- | --- | ---
Concatenation | `+` | `"First Name + ' ' + Last Name"`
Arithmetic | `+` `-` `*` `/` | `"Amount * Exchange Rate"`
String functions | `trim()`, `uppercase()`, `lowercase()`, `substring(n, m)`, `collapse_whitespace()` | `"trim(Email Address)"`
Date functions | `today()`, `date_diff(a, b, unit)`, `date_add(d, n, unit)` | `"date_diff(End Date, Start Date, 'days')"`
Null handling | `coalesce(a, b)` | `"coalesce(Preferred Name, First Name)"`
Branching | `if(condition, then, else)` | `"if(Company Name IS NOT NULL, Company Name, Full Name)"`

The generating agent is responsible for translating these expressions into the target physical syntax (SQL, Spark, dbt). Authors write expressions against domain attribute names, not physical column names. The function set above is the portable core, not a closed list — additional functions may be used where the generating agent and target platform support them.

Prefer `conditional` over a nested `if()` chain. `if()` is for a single branch inside an otherwise computational expression; multi-way value selection is what `conditional` is for, and it validates its case keys against the target's type.

---

#### `reconciliation`

Resolves a domain attribute when the same data exists in multiple source systems and a priority rule determines which value to use.

````markdown
##### Transform: Preferred Email Address
CRM is the master for contact data. The ERP value is used only when CRM has no email on record.

```yaml
type: reconciliation
target: Customer · Email Address
strategy: priority_non_null
sources:
  - priority: 1
    system: salesforce
    field: Contact.Email
  - priority: 2
    system: sap
    field: Customer.EmailAddress
```
````

**Reconciliation strategies:**

Strategy | Behaviour
--- | ---
`priority_non_null` | Take the highest-priority non-null value
`priority_always` | Always take the highest-priority value, even if null
`most_recent` | Take the value with the most recent timestamp; requires `timestamp_field` on each source
`consensus` | Take a value only when all sources agree; otherwise null

These strategies cover the common cases and are not a closed list — an organisation may declare another strategy, described in the transformation's prose, and the generating agent should confirm its interpretation rather than guess.

For `most_recent`, declare the timestamp field on each source:

```yaml
sources:
  - priority: 1
    system: salesforce
    field: Contact.Email
    timestamp_field: Contact.LastModifiedDate
```

`reconciliation` resolves an attribute **across source systems**. To collapse duplicate rows **within** one source table, use `deduplication`.

---

#### `deduplication`

Derives an instance identifier and collapses multiple source rows that describe the same real-world thing into a single canonical instance. Use when the source system holds one row per *usage* of an entity that the domain model holds once as reference data — addresses, products, counterparties.

`deduplication` is the only transformation type that determines how many instances exist. It targets an identifier attribute, and the instances that share a derived key become one.

````markdown
##### Transform: Address Uniqueness Merge

Once we have a Delivery Point Id (DPID) for an address we can merge multiple usages of that address. Where no DPID is present the address cannot be merged on an external key, so a normalised composite of the address components is used instead.

```yaml
type: deduplication
target: Address · Address Identifier
key:
  - when: "DPID_N IS NOT NULL"
    using:
      - field: ADDRESS.DPID_N
    prefix: "DPID"
  - when: "DPID_N IS NULL"
    using:
      - field: ADDRESS.ADDRESS1
      - field: ADDRESS.POST_CODE
      - field: ADDRESS.COUNTRY_CODE
    normalise: [trim, uppercase, collapse_whitespace]
    prefix: "COMP"
survivorship:
  strategy: most_recent
  timestamp_field: ADDRESS.UPDATE_DATE
```
````

`key` is an ordered list of derivation branches. The first branch whose `when` predicate holds supplies the key. A branch with no `when` is unconditional and must be last. Declaring at least one unconditional or exhaustive branch is the author's responsibility — a row matching no branch cannot be identified and is rejected.

Key | Purpose
--- | ---
`using` | Ordered list of source fields composing the key.
`normalise` | Normalisation applied to each field before composition: `trim`, `uppercase`, `lowercase`, `collapse_whitespace`, `strip_punctuation`.
`prefix` | Literal prefix distinguishing keys from different branches, so a composite key can never collide with an external-identifier key.

`survivorship` declares which row supplies attribute values when merged rows disagree. It reuses the `reconciliation` strategy vocabulary — `priority_non_null`, `priority_always`, `most_recent`, `consensus` — with `most_recent` requiring a `timestamp_field`. Without a survivorship rule, merge output is order-dependent and generation is not reproducible.

An entity produced by a `deduplication` transformation should be marked `deduplicated: true` in the source table's `produces:` block.

---

#### `lookup`

Enriches a source value by joining to a domain enum, a reference entity, or an inline mapping table. Use when the source system uses codes, abbreviations, or legacy identifiers that the domain model has standardised.

````markdown
##### Transform: Resolve Country Code
Translates two-character legacy country abbreviations from the core banking system into ISO 3166-1 alpha-3 codes used in the domain model.

```yaml
type: lookup
target: Customer · Country Code
source:
  field: Customer.CountryAbbrev
lookup:
  reference: Country Code
  match_on: Abbreviation
  return: ISO Code
fallback: null
```
````

---

`reference` must name a domain Enum or Entity defined in the same model. `match_on` and `return` must be valid attribute or value names within that reference. `fallback` declares what to do when no match is found: `null`, `reject` (fail the record), or a literal default value.

##### Inline lookups

Domain enums declare values and their meaning; they do not carry source system codes. A source code table therefore has nowhere to live on the enum, and putting it there would push a source idiosyncrasy into the canonical model. Where the mapping is from opaque source codes to canonical values, declare it inline on the transformation:

```yaml
type: lookup
target: Location Involvement · Address Purpose
source:
  field: ADDRESS.ADDRESS_TYPE_DID
lookup:
  inline:
    101890: Mailing
    101891: Residential
    111418: Registered Office
fallback: reject
```

`inline` and `reference` are mutually exclusive. Where the target is an `enum:` type, every value on the right-hand side must be a valid enum value.

Use `inline` when the mapping is an opaque code table with no logic in it. Use `conditional` when a case needs a predicate rather than an equality match — a range, a compound test, or several codes collapsing to one value.

---

#### `conditional`

Maps source values to domain values using explicit threshold or rule cases.
Each case key is a valid domain attribute value or enum value.

````markdown
##### Transform: Classify Customer Risk
Derives the domain risk tier from the raw numeric risk score produced by
the transaction monitoring system.

```yaml
type: conditional
target: Customer · Risk Rating
source:
  field: Customer.RiskScore
cases:
  Low:        "RiskScore < 30"
  Medium:     "RiskScore >= 30 AND RiskScore < 70"
  High:       "RiskScore >= 70 AND RiskScore < 90"
  Prohibited: "RiskScore >= 90"
fallback: null
```
````

---

Case keys must be valid values of the attribute's declared type. If `target` is an `enum:` type, case keys must be valid enum values. `fallback` behaves identically to the lookup type.

##### Multiple inputs

A conditional whose cases test a single column declares it with `source:`. Where cases test several columns, declare them with `inputs:`, using the same syntax and operand-naming rules as `derived`:

```yaml
type: conditional
target: Location Involvement · Verification Status
inputs:
  Is Validated:
    field: ADDRESS.IS_VALIDATED
  Confirmed By Customer:
    field: ADDRESS.ADD_CONFIRMED_BY_CUSTOMER
  Retired Date:
    field: ADDRESS.DSS_END_DATE
cases:
  Expired:  "Retired Date IS NOT NULL AND Retired Date < today()"
  Verified: "Confirmed By Customer == 1 OR Is Validated == 1"
fallback: Unverified
```

`source:` and `inputs:` are mutually exclusive. Every field a case predicate references must be declared — a predicate reading an undeclared field is a validation error, because it breaks lineage tracing.

##### Evaluation order

Case predicates frequently overlap. An address that is both expired and customer-confirmed satisfies two cases, and which one wins changes the output. Declare the intent:

```yaml
evaluation: first_match
```

Value | Behaviour
--- | ---
`first_match` | Cases are evaluated in declaration order; the first matching case wins. Later overlapping cases are unreachable by design.
`exclusive` | Cases are asserted to be mutually exclusive. Generation emits a data quality check that fails if a row matches more than one.

`evaluation` defaults to `first_match`. Case declaration order is therefore significant, and generators must preserve it. Use `exclusive` where non-overlap is a property of the data worth testing rather than an assumption worth relying on.

---

#### `aggregation`

Collapses multiple source rows into a single domain attribute value. Use when the source system operates at a finer grain than the domain entity.

````markdown
##### Transform: Total Outstanding Balance
Sums all active loan disbursement records from the core banking system
to produce the entity-level balance figure.

```yaml
type: aggregation
target: Loan Agreement · Outstanding Balance
function: sum
source:
  field: Loan_Disbursements.DisbursedAmount
filter: "Loan_Disbursements.Status == 'Active'"
grain:
  entity: Loan Agreement
  join_on: Loan Agreement Number
```
````

`function` supports: `sum`, `count`, `count_distinct`, `min`, `max`, `average`, `first`, `last`. Additional functions may be used where the target platform supports them.

`grain` declares which entity this aggregation rolls up to and the join key. The `entity` value must match an entity name in the domain model. The `join_on` value must match an attribute name on that entity.

`filter` is optional. It applies before aggregation.

---

### **Worked Examples**

A transformation's YAML declares intent. A worked example declares *outcome* — a source row and the exact set of canonical instances it must produce. For anything beyond a direct map, this is the only device in MD-DDL that pins behaviour: prose can be read two ways, and a fan-out with conditional routing and deduplication has enough moving parts that two correct-looking generations can disagree.

Worked examples are declared under `##### Worked Examples` in transform detail. They are a contract — a generated pipeline that does not reproduce these outputs from these inputs is incorrect — and they translate directly into test fixtures.

````markdown
##### Worked Examples

```yaml
example: Individual with a DPID-matched, customer-confirmed residential address
given:
  ADDRESS_ID: "3f2b-aaa1"
  OWNER_ID: "8c14-p001"
  OWNER_TYPE_ENUM: 1
  ADDRESS_TYPE_DID: 101891
  FIRST_NAME: "Jane"
  LAST_NAME: "Whitcombe"
  DPID_N: "1234567"
  ADD_CONFIRMED_BY_CUSTOMER: 1
produces:
  - entity: Address · Postal Address
    Address Identifier: "DPID:1234567"
    Delivery Point ID: 1234567
  - entity: Location Involvement
    Location Involvement Identifier: "8c14-p001:3f2b-aaa1"
    Address Purpose: Residential
    Verification Status: Verified
  - entity: Individual
    Party Identifier: "8c14-p001"
    Legal Name: "Jane Whitcombe"
notes: >
  Party is abstract, so the concrete instance is an Individual, selected by the
  OWNER_TYPE_ENUM condition in Entity Fan-Out.
```
````

Key | Purpose
--- | ---
`example` | Short name for the case being pinned. Unique within the source table.
`given` | The source row. A list of rows where the example demonstrates cross-row behaviour such as deduplication.
`produces` | The canonical instances emitted, each naming its entity and the attributes the example fixes. `cardinality` may be declared where the count itself is the point.
`notes` | Why the output is what it is. Written for the reader who expected something else.

Only the columns and attributes that matter to the example need to be listed — an example is an assertion about behaviour, not a complete row dump.

`produces:` here asserts values for one concrete case; the identically-named block under [Entity Fan-Out](./7-Sources.md#entity-fan-out) declares the general shape. The example must be consistent with the fan-out: an entity it produces that the fan-out does not declare is a validation error.

Cover the cases where the model could reasonably be read two ways: each branch of a fan-out condition, each branch of a deduplication key, and any case whose evaluation order is load-bearing.

---

### **Brownfield Adoption Note**

Existing ETL/ELT logic documented in `baselines/etl/` serves as the reference for creating MD-DDL transformation YAML. The transformation spec defines the target state; the baseline documents the current state. Reconciliation between the two is part of the adoption journey. See [Section 10 — Adoption](./10-Adoption.md) for the full adoption workflow.

---

### **Transformation Rules**

1. **Key-as-Name:** The rule heading is the transformation's identity in the Knowledge Graph. It must be unique within the source table's transform detail and is the authoritative name used in lineage tracing and generated output. The `Transform: ` prefix is not part of the name.

2. **Target must exist:** The entity and attribute in `target` must be declared in the canonical domain model, or inherited from a parent entity. Both are validated during generation.

3. **Source system is implicit:** Within transform detail, the source system is not declared on individual transformations — it is inherited from the owning source. Source idiosyncrasies (`null_as`, `quality`, `format`) are declared on the `source:` block within the transformation.

4. **One mapping path per canonical attribute per source table:** Use exactly one mapping path per target attribute from a given source table. The constraint is on the target, not the source — several rules may read the same source column, but two rules must not write the same attribute. Where mapping is non-direct, the `Destination` entry must link to the rule section that defines the logic.

5. **No transformation logic in constraints:** Constraints validate; they do not transform. The transformation defines the inbound mapping; the constraint defines the validation rule on the result.

6. **Expression operands use declared input names:** In `derived` and multi-input `conditional` expressions, operands match the keys declared in `inputs:`, not raw source field names. This keeps expressions readable and decoupled from physical source schema.

7. **Abstract targets require a fan-out:** A transformation whose `target` names an attribute on an abstract entity must be accompanied by an `Entity Fan-Out` declaration binding it to a concrete subtype.

8. **Identity is derived, never assumed:** Where a canonical instance's identifier is not a direct map from a source field, a `deduplication` transformation must declare how it is derived and how conflicts are resolved.

9. **Transformations are optional:** A source may be declared without any transform detail if mappings have not yet been authored. Transform detail is added when integration lineage is needed.

---

### **Example — Transform detail excerpt**

See [Section 7 — Sources](./7-Sources.md) for the complete example. The following shows the transformation type syntax in context:

````markdown
# [Financial Crime](../../domain.md)

## Sources

### [Salesforce CRM](../sources.md#salesforce-crm)

#### Contact

##### Transform: Concatenate Full Name

```yaml
type: derived
target: Customer · Full Name
expression: "trim(First Name) + ' ' + trim(Last Name)"
inputs:
  First Name:
    field: Contact.FirstName
  Last Name:
    field: Contact.LastName
```

##### Transform: Resolve Country Code

```yaml
type: lookup
target: Customer · Country Code
source:
  field: Contact.MailingCountry
  null_as: null
lookup:
  reference: Country Code
  match_on: Abbreviation
  return: ISO Code
fallback: null
```
````

---

...next: [Data Products](9-Data-Products.md)
