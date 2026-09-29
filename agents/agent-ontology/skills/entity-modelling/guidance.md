# Classification and Inheritance — Detailed Guidance

Load this guidance when a concept could reasonably be an entity, an enum, a relationship
attribute, or a subtype, and the Entity Modelling skill's quick framework doesn't settle
it. In MD-DDL syntax, a subtype declares `extends: Parent` in its YAML and fills the
`Specializes` column in the domain's Entities table. A relationship attribute is
declared under `relationship_attributes` on the relationship (`5-Relationships.md`).

---

## Signals

Signal | Points to | Why
--- | --- | ---
A different business team owns or answers for it | Entity | Different owners mean different governance, change approval, quality metrics, and lifecycle
More than about three attributes that similar concepts don't have | Entity | Unique attributes are unique semantics that need an explicit home
Different compliance, retention, or security requirements | Entity | Governance attaches at entity level
A controlled list, rarely changing, with a label and perhaps a score or description | Enum | No independent lifecycle or owner to govern
Only meaningful while two specific things are connected | Relationship attribute | It describes the connection, not either participant

The same word can land differently in different industries, and ownership is usually
the deciding signal. Examples from the standards:

Domain | Concept | Decision | Reason
--- | --- | --- | ---
Banking (BIAN) | Customer, Merchant | Entities extending Party Role | Different owning teams; KYC vs MCC and settlement attributes
Banking (BIAN) | Debtor, Creditor in a single payment | Relationship attribute (role in transaction) | No attributes of their own. Promote them to entities, as Financial Crime does with Payer and Payee, when they gain attributes, rules, or an owner.
Insurance (ACORD) | Policy Holder, Insured, Claimant, Beneficiary | Entities | Different teams, processes, and attributes (billing, claims history, estate rules)
Telecom (TM Forum SID) | Customer vs Subscriber | Two entities | Commercial relationship vs service user: a company is the customer, its employee the subscriber
Healthcare (FHIR) | Patient, Practitioner, Related Person | Entities extending an abstract Party | Different regulatory treatment and ownership (HIPAA, credentialing, privacy)

Load the matching standard in `../standards-alignment/standards/` before relying on these.

## Hard Cases

- **"It's just a type now, but it may get attributes later."** If the attributes are
  certain soon, or teams are already arguing over ownership, make it an entity. If it's
  hypothetical, make it an enum. Promoting an enum later is a normal, additive change.
- **"The entity has only two attributes."** Check ownership, planned growth (KYC,
  preferences, relationships), and governance. Thin entities in early models usually
  fill out. If none of those apply, it may really be reference data.
- **"The enum has fifty values."** Size doesn't decide it. If every value has the same
  structure, it stays an enum. If groups of values carry different attributes, use an
  entity hierarchy (for example, 50 plan names form an enum, while five product
  categories with distinct technical attributes form a hierarchy).
- **"Our status values change over time."** Adding values is normal enum evolution.
  Tracking which instance had which status when is temporal tracking on the *entity*
  that holds the status, not a reason to make the enum an entity.

## Anti-Patterns

- **Everything an entity.** Statuses and types as entities add owners nobody wants and
  joins nobody needs.
- **Everything an enum.** A `Party Role Type` enum hides Customer's and Merchant's distinct
  attributes and governance.
- **Both.** A `Customer Type` entity *and* a `Customer Type` enum. Pick one.

## Changing Your Mind

- **Enum to entity**, when it gains four or more attributes, an owner, or distinct
  governance: create the entity, move the values, update the summary tables, and deprecate
  the enum with a migration note for consumers. This is usually a minor version bump.
- **Entity to enum**, which is rare: an entity nobody owns, whose attributes never
  arrived. Deprecate it and give consumers a migration path. This is a breaking change.

---

## Inheritance

Use inheritance when subtypes share real attributes and constraints *and* add their own.
Mark the parent `<<abstract>>` when it is never instantiated directly. Subtypes don't
repeat inherited attributes.

Typical hierarchies:

Standard | Hierarchy
--- | ---
BIAN | Party (abstract) → Individual, Legal Entity (→ Corporation, Partnership, Trust). Party Role (abstract) → Customer, Merchant, and other owned roles.
ACORD | Party (abstract) → Person, Organization. Coverage (abstract) → Auto, Property, Life, each with its own specialisations.
TM Forum SID | Party → Individual, Organization, with roles such as Customer modelled as Party Roles. Product (abstract) → Mobile, Broadband, TV.
FHIR | Resources are flat, but an abstract Party → Patient, Practitioner, Related Person gives shared governance and identity a home.

Avoid inheritance:

- **For reuse alone.** Shared columns without shared meaning call for composition
  through relationships.
- **More than three levels deep.** Deep trees are hard to generate and harder to change.
- **When children override most of the parent.** If a subtype replaces more than half of
  what it inherits, it isn't really that parent.
- **When only a label differs.** Use a discriminator attribute with an enum.

Edge cases:

- **An instance changes subtype** (a prospect becomes a customer). Model the roles as
  separate Party Roles of the same Party, not as a subtype change.
- **An instance is two subtypes at once** (a party that is both customer and merchant).
  This again means roles, not subtypes. Subtypes of Party are exclusive; Party Roles are not.
- **Physical realisation** (single table, table per type, or table per concrete type) is
  Agent Artifact's decision, driven by the generation skill. The logical hierarchy
  shouldn't bend to it.
