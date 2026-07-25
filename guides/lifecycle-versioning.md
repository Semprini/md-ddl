# MD-DDL Lifecycle & Versioning Guide

*A non-normative companion guide to the MD-DDL specification. The specification defines the lifecycle vocabularies — the `status` values, semver `version` fields, and lifecycle date fields on domains ([Section 2](../md-ddl-specification/2-Domains.md)), entities ([Section 3](../md-ddl-specification/3-Entities.md)), and data products ([Section 9](../md-ddl-specification/9-Data-Products.md)). This guide describes the change-management process built on those vocabularies: transitions, version-bump rules, and the `LIFECYCLE.md` history file. It is guidance for running a well-governed model, not part of the standard.*

---

## Domain Lifecycle Transitions

- A domain normally moves forward through lifecycle states: `Draft` → `Review` → `Active` → `Deprecated` → `Retired`.
- Reverting from `Active` to `Draft` or `Review` should be accompanied by a major version bump (the previous active version is effectively superseded).
- `Deprecated` domains should declare a `superseded_by` field in metadata pointing to the replacement domain (if one exists). No new consumers should onboard.
- `Retired` domains are immutable records. They remain in the repository for lineage and audit purposes.

### Lifecycle and Version Interaction

- A domain in `Draft` status may use version `0.x.y` to signal pre-release instability. The `0.x` convention indicates that breaking changes may occur without a major bump.
- A domain in `Active` status should have version `1.0.0` or higher. Stability guarantees apply from the first major release.
- When a domain transitions from `Review` to `Active` for the first time, its version should be set to `1.0.0`.

---

## Domain Evolution

Domains are living artifacts. They evolve as business understanding deepens, new source systems are integrated, regulatory requirements change, and consumer needs shift. The `version` field in domain metadata tracks this evolution using semantic versioning.

### Version Bump Rules

Change Type | Version Impact | Examples
--- | --- | ---
**Breaking** — changes meaning or removes consumer-visible structure | Major bump | Removing an entity or attribute; changing an attribute type incompatibly; reducing relationship cardinality; changing an identifier; removing or renaming an enum used by consumers
**Additive** — extends the model without altering existing meaning | Minor bump | Adding a new entity, attribute, relationship, event, enum value, or constraint; declaring a new source system or data product
**Corrective** — fixes errors without changing intended meaning | Patch bump | Clarifying descriptions; correcting broken links; updating governance metadata without changing logical structure; clarifying a constraint description without changing its logic

### Breaking vs Non-Breaking Changes

A change is **breaking** if a correctly-authored downstream consumer (data product, physical artifact, or integration) would produce different or incorrect output after the change is applied. Specifically:

- Removing or renaming an entity or enum is always breaking.
- Changing relationship cardinality (e.g., `1:N` to `M:N`) is breaking — physical schemas may need restructuring.
- Changing relationship granularity (`atomic` to `period`) is breaking — it alters the semantics of the join.
- Removing an attribute is breaking if any data product includes that entity.
- Changing an attribute's type or constraints is breaking if it narrows the valid domain.

A change is **non-breaking** if existing consumers continue to produce correct output without modification.

### Evolution Workflow

When modifying an existing domain:

1. Identify the change and classify it as breaking, additive, or corrective.
2. Bump the `version` field in metadata according to the rules above.
3. Record the logical change in `LIFECYCLE.md` if the domain maintains one. Include a machine-readable change manifest and any affected products.
4. If breaking: review all data products that reference the affected entities and update them accordingly.
5. If additive: update the relevant summary tables and create/update the detail definitions.
6. If corrective: fix the error in place.

---

## The LIFECYCLE.md Convention

A domain may include a `LIFECYCLE.md` file adjacent to `domain.md`. This file is optional, but recommended from the first version bump onward and strongly recommended for domains at `Active` status or higher.

`LIFECYCLE.md` replaces the narrower `CHANGELOG.md` convention used in earlier drafts. It combines a machine-readable change manifest with a human-readable changelog so the same file supports both agent workflows and human review.

Suggested structure:

````markdown
# Lifecycle - Financial Crime

## Current State

```yaml
domain_version: "1.1.0"
domain_status: Active

products:
  - name: Customer 360 Profile
    status: Active
    version: "1.0.0"
  - name: Suspicious Activity Report
    status: Draft
    version: "0.2.0"
```

## Version History

### Domain 1.1.0 - 2026-03-14

#### Change Manifest

```yaml
changes:
  - type: additive
    scope: entity
    entity: Exchange Rate
    description: "Added Exchange Rate entity for multi-currency analysis"
  - type: additive
    scope: attribute
    entity: Transaction
    attribute: Exchange Rate
    description: "Added Exchange Rate attribute to Transaction"

affected_products:
  - name: Suspicious Activity Report
    impact: additive
    reason: "Transaction schema extended with exchange-rate context"
```

#### Changelog

### Added
- Exchange Rate entity for multi-currency transaction analysis
- Currency entity as reference data

### Changed
- Transaction entity: added `Exchange Rate` attribute

### Domain 1.0.0 - 2025-11-01

#### Changelog

### Added
- Initial domain release with Party, Account, Transaction, and Agreement entity families
````

Conventions:

- `LIFECYCLE.md` is domain-scoped and may also record product status/version snapshots in the `## Current State` section.
- Each domain version entry corresponds to a semantic version used in the domain metadata.
- The `#### Change Manifest` block is the machine-readable section. It may be consumed by reconciliation and impact-analysis workflows.
- The `#### Changelog` section is the human-readable section and should use `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed` headings where applicable.
- Agents should offer to create or update `LIFECYCLE.md` whenever the domain version is bumped or a product is promoted, deprecated, or retired.
- `LIFECYCLE.md` is the authoritative lifecycle history file. If an older `CHANGELOG.md` exists, it should be migrated or treated as legacy documentation.

---

## Entity Lifecycle Practices

Entity lifecycle fields (`status`, `since`, `deprecated_at`, `breaking_in`) are defined in [Section 3 — Entities](../md-ddl-specification/3-Entities.md). Practices for using them:

- An entity's `status` should not be more advanced than its parent domain's status. An entity cannot be `Active` in a `Draft` domain.
- The `since` field is informational — it records provenance and aids lifecycle history generation.
- The `deprecated_at` field signals to consumers that this entity should no longer be relied upon. Deprecated entities should include a description noting the replacement or migration path.
- The `breaking_in` field provides advance notice of an upcoming breaking change. Agents and consumers can use this to plan migrations before the change takes effect.
- When an entity is introduced, deprecated, or flagged with `breaking_in`, the domain's `LIFECYCLE.md` should be updated if that file is maintained.

---

## Product Lifecycle Transitions

Product lifecycle states and metadata fields are defined in [Section 9 — Data Products](../md-ddl-specification/9-Data-Products.md).

- `Draft` → `Active`: Product has passed quality review, names at least one consumer, and declares version `1.0.0` or higher.
- `Active` → `Deprecated`: Add a `deprecated_date` to the product metadata. A `successor` field should name the replacement product if one exists.
- `Deprecated` → `Retired`: Add a `sunset_date`. After this date the product is no longer generated or published. The declaration remains in the model for audit purposes.
- `Retired` → any: Not recommended. Retired products are immutable records. If the concept needs to be revived, create a new product with a new name.

### Product Versioning

The `version` field tracks the evolution of the product contract. Product versions are independent from domain versions: a product may remain `Draft` while its domain is `Active`, and a product may lag behind the latest domain version while consumers migrate.

Trigger | Version Impact
--- | ---
Domain breaking change affecting an entity in the product's `lineage` | Major bump
Domain additive change affecting an entity in the product's `lineage` and reflected in the product's logical model | Minor bump
Product removes an entity from its `entities` list | Major bump
Product adds an entity to its `entities` list | Minor bump
Product changes masking rules, SLA, consumers, or other governance contract details without reducing schema scope | Minor or patch bump depending on consumer impact
Corrective documentation or descriptive fixes with no contract impact | Patch bump

Use a major bump when a correctly-authored consumer must change to keep working. Use a minor bump when the published contract is extended but existing consumers can continue unchanged. Use a patch bump for non-breaking clarifications or corrective metadata changes.

### Product-Domain Lifecycle Consistency

Products evolve independently, but they cannot be more mature than the model they publish.

- A product's `status` should not be more advanced than the owning domain's status. A product cannot be `Active` if its domain is `Draft` or `Review`.
- Products may lag the domain. A product may remain `Draft` while its domain is `Active`.
- Promoting a domain to `Active` does not automatically promote any products declared within it.
- An `Active` product should declare version `1.0.0` or higher.
- If a product references deprecated entities or draws from a deprecated lineage dependency, it should either move to `Deprecated` or declare a `migration_note` explaining the consumer migration path.
- When a domain version bump changes referenced entities, affected products should evaluate their own version independently using the rules above and record the result in the domain's `LIFECYCLE.md` when that file is maintained.

### Lifecycle History Recording

Product promotions, version bumps, deprecations, and retirements should be recorded in the owning domain's `LIFECYCLE.md` file when present. The domain owns the lifecycle history file because product lifecycle is part of the domain's publication history.
