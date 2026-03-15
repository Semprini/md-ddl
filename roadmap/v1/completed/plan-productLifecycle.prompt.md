# Plan: Product Lifecycle and Versioning

## TL;DR

MD-DDL currently has no specification for the lifecycle of a domain or entity
definition itself — how it moves from draft to production, how it gets
versioned, deprecated, and retired, and how consumers are notified of breaking
changes. This gap affects every layer of the standard: the spec, Agent Ontology
(creating and promoting domains), Agent Architect (product design), Agent
Governance (compliance auditing), and the Financial Crime example. A related
gap exists in how AI-driven artifact regeneration interacts with lifecycle:
when Agent Artifact regenerates physical schemas from an updated logical model,
the output may differ structurally from the previous generation even for small
logical changes, making it impractical to derive migrations from physical diffs
alone. The diff must live at the logical layer, with reconciliation bridging
the gap to the physical layer. A third gap: data products already have `status`
and `version` fields in the spec but no versioning semantics, promotion rules,
or lifecycle file — and product lifecycle is independent from domain lifecycle
(a product can be `Draft` while its domain is `Active`). This plan defines the
scope of work needed to close all three gaps, unified around a `LIFECYCLE.md`
file that replaces the narrower `CHANGELOG.md` convention and tracks both
domain and product lifecycle in one place.

---

## Problem Statement

The current spec defines a `status` field in domain metadata (observed in
the Financial Crime example as `status: "Production"`) and a `version` field
(`version: "1.0.0"`), but neither field is defined in the spec. There is no:

- Canonical set of status values
- Versioning semantics (what constitutes a major, minor, or patch change)
- Deprecation protocol (how to signal that a definition is being retired)
- Consumer notification mechanism (how downstream data products or
  applications learn that a definition has changed)
- Agent guidance for promoting a definition through lifecycle stages
- Connection between logical model changes (versioning) and physical artifact
  changes (regeneration and reconciliation) — AI regeneration produces full
  artifacts rather than incremental deltas, so physical diffs are noisy and
  cannot reliably drive migration decisions without logical context
- Product versioning semantics — data products have `status` and `version`
  fields but no defined rules for what triggers a product version bump, no
  promotion protocol, and no product-domain lifecycle consistency rules (e.g.,
  a product referencing a `Deprecated` entity in an `Active` product is
  currently undetected)

---

## Scope of Work

### 1 — Spec: Domain Lifecycle Fields (3-Entities.md / 2-Domains.md)

Define the lifecycle metadata block as a first-class spec concept.

**Domain-level fields to specify:**

Field | Type | Required | Description
--- | --- | --- | ---
`status` | enum:DomainStatus | No | Current lifecycle state of the domain definition
`version` | semver string | No | Semantic version of the domain definition

**DomainStatus enum values:**

Value | Description
--- | ---
`draft` | Under active development. Not yet validated. Do not consume.
`review` | Under structured review (Layer 1/2/3 process). Stable enough for early feedback; breaking changes possible.
`active` | Validated and available for consumption. Stability guaranteed within major version.
`deprecated` | Retained for reference and migration support. Consumers should migrate to the superseding definition. No new consumers should onboard.
`retired` | No longer maintained. Historical record only.

**Versioning semantics:**

Version component | Trigger
--- | ---
Major (`x.0.0`) | Breaking change: attribute removed, type changed incompatibly, cardinality reduced, identifier changed
Minor (`x.y.0`) | Non-breaking addition: new attribute, new relationship, new enum value, new constraint
Patch (`x.y.z`) | Non-breaking clarification: description update, governance metadata update, constraint description clarified without logic change

### 2 — Spec: Entity-Level Lifecycle Fields

Entities within a domain may have their own lifecycle state (e.g., a domain
is `active` but a new entity within it is still `draft`).

Add to entity detail file spec (3-Entities.md):

Field | Type | Required | Description
--- | --- | --- | ---
`status` | enum:EntityStatus | No | Lifecycle state of this entity definition. Defaults to the domain status if omitted.
`since` | semver string | No | The domain version in which this entity was introduced
`deprecated_at` | semver string | No | The domain version in which this entity was deprecated
`breaking_in` | semver string | No | The domain version in which a breaking change will take effect (advance notice)

### 1b — Spec: Product Lifecycle Fields (9-Data-Products.md)

Data products already have `status` and `version` fields but no defined
semantics. Add to `9-Data-Products.md`:

**Product versioning semantics:**

Trigger | Product version impact
--- | ---
Domain breaking change affecting a referenced entity | Major bump — consumer contract broken
Domain adds an entity the product includes | Minor bump — schema extension
Product adds or removes an entity from its `entities` list (removal) | Major bump — schema reduction, breaking for consumers
Product adds an entity to its `entities` list | Minor bump — schema extension
Product changes masking rules, SLA, or consumers | Minor or patch bump — governance change, no schema impact

**Product-domain lifecycle consistency rules:**

- A product's `status` must not be more advanced than the domain it draws from
  (a product cannot be `Active` if its domain is `Draft`)
- A product referencing entities from a `Deprecated` domain must itself be
  `Deprecated` or have an explicit migration note
- When a domain is promoted to `Active`, products in `Draft` are not
  automatically promoted — they require independent promotion

### 3 — Spec: LIFECYCLE.md Convention

Replace the `CHANGELOG.md` convention with `LIFECYCLE.md` — a single file
adjacent to `domain.md` that serves as both a machine-readable state record
(change manifests, current status, affected products) and a human-readable
history (narrative changelog entries).

**File location:** `<domain-root>/LIFECYCLE.md` (optional; created on first
version bump or promotion)

**Format:**

```markdown
# Lifecycle — [Domain Name]

## Current State

domain_version: "1.3.0"
domain_status: Active

products:
  - name: [Product Name]
    status: Active
    version: "1.0.0"
  - name: [Other Product]
    status: Draft
    version: "0.1.0"

## Version History

### Domain [version] — [date]

#### Change Manifest
` ` `yaml
changes:
  - type: breaking | additive | corrective
    scope: entity | attribute | relationship | event | enum
    entity: EntityName
    attribute: attribute_name        # if scope is attribute
    description: "Human-readable description of the change"

affected_products:
  - name: Product Name
    impact: breaking | additive | none
    reason: "Why this product is affected"
` ` `

#### Changelog
[Keep a Changelog conventions: Added / Changed / Deprecated / Removed / Fixed]
```

The change manifest block is the machine-readable section consumed by the
reconciliation skill. The Changelog section is the human-readable narrative.
Both live under the same version header.

The agent should offer to create or update `LIFECYCLE.md` whenever a version
is bumped or a domain or product is promoted.

### 4 — Agent Ontology: Lifecycle Promotion Skill

Create `agents/agent-ontology/skills/lifecycle/SKILL.md` with:

- **Promote** mode: Walk the user through promoting a domain from `draft` →
  `review` → `active`. Runs a pre-promotion checklist (all entities have
  required fields, all relationships have targets, governance is complete).
  Outputs a promotion summary.
- **Version bump** mode: Analyses what changed since the last tagged version,
  suggests the appropriate semver bump (major/minor/patch), updates the
  `version` field, and writes the change manifest and changelog entry to
  `LIFECYCLE.md`. Also evaluates which products reference the changed entities
  and calculates the product-level impact (breaking/additive/none) for each,
  populating the `affected_products` block. Recommends whether each affected
  product needs its own version bump.
- **Change manifest** output: Structured YAML block written to `LIFECYCLE.md`
  listing each logical change (type, scope, entity, description) and an
  `affected_products` section. This is the bridge artifact consumed by the
  reconciliation skill to distinguish intentional physical changes from
  regeneration noise, and by Agent Architect to drive product version bumps.

### 4a — Agent Artifact: Lifecycle-Aware Reconciliation

Extend the reconciliation skill (`agents/agent-artifact/skills/reconciliation/SKILL.md`)
to accept a change manifest from the version bump skill and annotate each
physical gap with its logical cause.

**Current state:** Reconciliation compares generated artifacts against existing
baselines or deployed schemas and produces a gap report. It is stateless — it
does not know what logical changes drove the physical differences.

**Required changes:**

- Accept an optional change manifest as input (produced by the version bump
  skill when a domain version is bumped)
- When a change manifest is provided, correlate each physical gap to the
  logical change that caused it:
  - Gaps that match a logical change → annotated with version, change type,
    and affected entity/attribute
  - Gaps with no corresponding logical change → flagged as regeneration
    artefacts (column reordering, constraint reformulation, naming style
    shifts) that do not require migration
- Add a **Migration Relevance** column to the gap report:

  Relevance | Meaning
  --- | ---
  **Intentional — breaking** | Physical change caused by a breaking logical change. Migration required.
  **Intentional — additive** | Physical change caused by an additive logical change. Schema extension only.
  **Intentional — corrective** | Physical change caused by a corrective logical change. No structural migration.
  **Regeneration noise** | Physical difference not caused by any logical change. Safe to ignore or normalise.
  **Unexplained** | Physical difference with no logical change and no obvious regeneration cause. Flag for review.

- Include a **Product Version** column in the gap report identifying which
  product version the gap belongs to, so a user running multiple products off
  the same domain can triage by product scope
- The annotated gap report becomes the handoff artifact to the user's migration
  toolchain (Alembic, Atlas, Flyway, SQLMesh, etc.)

**Why not build a custom diff/migration engine?**

AI-driven artifact generation produces complete schemas, not incremental deltas.
Diffing two generated schemas to produce a migration is the wrong abstraction —
it conflates intentional logical changes with incidental physical differences
introduced by regeneration. The correct approach is:

1. Diff at the logical layer (git + version bump skill)
2. Regenerate physical artifacts from the updated logical model
3. Reconcile new generated artifacts against existing deployed state
4. Annotate each gap with its logical cause using the change manifest
5. Hand the annotated gap report to the platform-specific migration tool

This keeps MD-DDL focused on what it does well (logical modelling, governance,
and artifact generation) and delegates migration execution to tools that
understand platform-specific DDL semantics.

### 5 — Agent Governance: Lifecycle Compliance Check

Extend the governance agent's compliance audit to check:

- Domains with `status: active` must have a `version` field
- Entity `status` values must not be more advanced than the parent domain
  (an entity cannot be `active` in a `draft` domain)
- Warn when `version` is `1.0.0` or unset for a domain that has been in
  production (informed by `status: active` and relationship/consumer count)
- Product `status` must not be more advanced than the domain it draws from
- Products referencing entities from a `Deprecated` domain must themselves be
  `Deprecated` or declare an explicit migration note
- Products with no `version` field while the domain is `active` should be warned

### 6 — Agent Architect: Product Lifecycle

Extend the product-design skill (`agents/agent-architect/skills/product-design/SKILL.md`)
with a **product lifecycle** mode, parallel to the domain lifecycle skill in
Agent Ontology.

**Product lifecycle mode — Promote:**

- Walk the user through promoting a product from `Draft` → `Active`
- Pre-promotion checklist:
  - [ ] Product references only entities whose `status` is at least as advanced
        as the target product status
  - [ ] Domain `status` is at least as advanced as the target product status
  - [ ] `version` field is set (minimum `1.0.0` for `Active`)
  - [ ] Governance overrides are declared where product obligations differ from
        domain defaults (masking, retention, classification)
  - [ ] At least one named consumer is declared
- On promotion to `Active`: offer to update `LIFECYCLE.md` with a product
  status entry

**Product lifecycle mode — Version Bump:**

- Triggered by the domain lifecycle skill when a domain version bump produces
  an `affected_products` block with `impact: breaking` or `impact: additive`
- Also triggered directly when the user changes a product's `entities` list,
  masking rules, SLA, or consumers
- Classify the change using the product versioning semantics from item 1b
- Propose the new product version and offer to update `LIFECYCLE.md`

**Product lifecycle mode — Deprecate / Retire:**

- When a domain is deprecated, flag all `Active` products drawing from it
- Guide the user through setting product `status: Deprecated` and declaring
  a migration path for consumers

**Product-domain consistency check** (always-on, not a separate mode):

- When designing or reviewing any product, warn if product `status` is more
  advanced than the domain
- Warn if any referenced entity has `status: Deprecated` while the product is
  `Active`

### 7 — Update Financial Crime Example

Apply the lifecycle fields to the Financial Crime domain as the canonical
example:

```yaml
status: "active"
version: "1.0.0"
```

Both fields are already present but unspecified. Once the spec defines them:

- Update the domain metadata to use canonical status and version values
- Add `since` fields to entity detail files for entities whose introduction
  version is known
- Create `LIFECYCLE.md` as the canonical example of the combined format,
  including a domain version entry with a change manifest and changelog section,
  and a products section showing the Patient Financial Fraud Detection product
  with its own status and version

### 8 — Agent Guide: Lifecycle and Evolution Teaching

Update Agent Guide's concept explorer skill to teach the lifecycle and
evolution model, including:

- The distinction between logical evolution (incremental MD-DDL changes tracked
  by git and classified by the version bump skill) and physical regeneration
  (full artifact generation by Agent Artifact)
- Why the diff lives at the logical layer, not the physical layer — AI
  regeneration produces structurally different but logically equivalent output,
  so physical diffs are unreliable for migration planning
- The workflow: logical diff → version bump → regenerate → reconcile →
  annotated gap report → migration tool
- How the change manifest bridges versioning and reconciliation
- When to hand off to Agent Ontology (domain lifecycle), Agent Architect
  (product lifecycle), Agent Artifact (reconciliation), or the user's
  migration toolchain (deployment)
- The product-domain lifecycle relationship: products can lag behind the domain
  (a product can be `Draft` while the domain is `Active`), but products cannot
  lead the domain (a product cannot be `Active` if the domain is `Draft`), and
  products cannot silently reference deprecated entities

Add a comparison entry to the Concept Explorer's analogy table:

MD-DDL Concept | ER / UML analogy | dbt / SQL analogy | Data Mesh analogy
--- | --- | --- | ---
**Version / Lifecycle** | Schema version in migration tool | dbt project version, model deprecation | Domain version, contract versioning
**Change Manifest** | — | dbt `state:modified` selector | — (no direct equivalent)
**Reconciliation** | Schema compare tool | `dbt run --defer` against prod | Contract compatibility check

---

## Acceptance Criteria

- [ ] `status` and `version` (domain and entity) are defined in the spec with
      canonical values and semantics
- [ ] Domain status metadata enum is documented in `2-Domains.md`
- [ ] Domain versioning semantics (major/minor/patch triggers) are documented
- [ ] Product versioning semantics are documented in `9-Data-Products.md`
- [ ] Product-domain lifecycle consistency rules are documented
- [ ] `LIFECYCLE.md` format is defined in the spec (combined change manifest +
      changelog, covering both domain and product lifecycle)
- [ ] Agent Ontology lifecycle skill covers promote, version-bump, change
      manifest output (with `affected_products`), and writes to `LIFECYCLE.md`
- [ ] Agent Artifact reconciliation skill accepts a change manifest and
      annotates gap reports with logical cause, migration relevance, and
      product version scope
- [ ] Agent Architect product-design skill has a lifecycle mode covering
      product promote, version-bump, and deprecation
- [ ] Agent Governance compliance check includes domain and product lifecycle
      consistency validation
- [ ] Agent Guide concept explorer covers domain and product lifecycle,
      evolution vs regeneration, and the logical-diff-to-reconciliation workflow
- [ ] Financial Crime example has a `LIFECYCLE.md` demonstrating the format
      with domain and product entries

---

## Dependencies and Order

1. Spec definitions (items 1, 1b, 2, 3) must be complete before agent work
   begins — the `LIFECYCLE.md` format (item 3) and product versioning semantics
   (item 1b) are required inputs for both agent skills
2. Agent Ontology lifecycle skill (item 4) and Agent Architect product lifecycle
   mode (item 6) can be built in parallel once spec is done; both write to
   `LIFECYCLE.md` and must agree on the format
3. Agent Artifact lifecycle-aware reconciliation (item 4a) depends on the
   change manifest format from item 4 and the product version scope from item 6
4. Agent Governance compliance check (item 5) depends on both the domain
   lifecycle spec (items 1–2) and product lifecycle spec (item 1b)
5. Agent Guide teaching updates (item 8) can begin once items 4 and 6 are
   designed (does not need them fully implemented)
6. Financial Crime example update (item 7) is last — validates all the above

---

## Out of Scope

- **Runtime contract enforcement** (CI/CD pipeline schema validation) — the
  MD-DDL agent layer documents and governs, it does not deploy
- **Consumer subscription or notification delivery** (Slack, email, webhook) —
  `consumers` is an informational field; notification is the user's
  responsibility
- **Automatic breaking-change detection from git diff** — out of scope for v1;
  the version bump skill assists but does not automate this
- **Custom diff engine or migration generator** (Alembic, Atlas, Flyway,
  SQLMesh equivalent) — AI-driven artifact generation produces complete
  schemas, not incremental deltas. Diffing two generated schemas to produce
  migrations conflates intentional logical changes with incidental physical
  differences introduced by regeneration (column reordering, constraint
  reformulation, naming style shifts). The correct approach is to diff at the
  logical layer (git + version bump), reconcile at the physical layer
  (annotated gap report), and delegate migration execution to the user's
  platform-specific toolchain. MD-DDL's contribution is the annotated gap
  report — the bridge between logical intent and physical migration — not the
  migration itself.
- **Git revision tracking in the spec** — git is the revision tracker. The
  version bump skill uses git history when available but the spec does not
  define its own revision tracking layer. Domain `version` is a semantic
  version reflecting logical evolution, not a commit reference.
- **Deprecation workflow automation** — the lifecycle skill supports the
  `Active` → `Deprecated` → `Retired` transitions and the version bump
  skill classifies deprecations, but automated consumer migration is outside
  MD-DDL's scope
