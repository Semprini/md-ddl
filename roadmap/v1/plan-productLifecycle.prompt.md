# Plan: Product Lifecycle and Versioning

## TL;DR

MD-DDL currently has no specification for the lifecycle of a domain or entity
definition itself — how it moves from draft to production, how it gets
versioned, deprecated, and retired, and how consumers are notified of breaking
changes. This gap affects every layer of the standard: the spec, Agent Ontology
(creating and promoting domains), Agent Architect (product design), Agent
Governance (compliance auditing), and the Financial Crime example. This plan
defines the scope of work needed to close the gap.

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

### 3 — Spec: Change Log Convention

Define a lightweight changelog convention for domains. A `CHANGELOG.md`
adjacent to `domain.md` (optional) follows Keep a Changelog conventions.
The agent should offer to generate or update this file when version is bumped.

### 4 — Agent Ontology: Lifecycle Promotion Skill

Create `agents/agent-ontology/skills/lifecycle/SKILL.md` with:

- **Promote** mode: Walk the user through promoting a domain from `draft` →
  `review` → `active`. Runs a pre-promotion checklist (all entities have
  required fields, all relationships have targets, governance is complete).
  Outputs a promotion summary.
- **Version bump** mode: Analyses what changed since the last tagged version,
  suggests the appropriate semver bump (major/minor/patch), and offers to
  update the `version` field and `CHANGELOG.md`.

### 5 — Agent Governance: Lifecycle Compliance Check

Extend the governance agent's compliance audit to check:

- Domains with `status: active` must have a `version` field
- Entity `status` values must not be more advanced than the parent domain
  (an entity cannot be `active` in a `draft` domain)
- Warn when `version` is `1.0.0` or unset for a domain that has been in
  production (informed by `status: active` and relationship/consumer count)

### 6 — Agent Architect: Product Lifecycle Awareness

Update Agent Architect's data product skill to:

- Propagate domain `status` to product `status` by default (a product
  built on a `deprecated` domain should be flagged)
- Recommend versioning strategy for data products that parallels the domain
  versioning model

### 7 — Update Financial Crime Example

Apply the lifecycle fields to the Financial Crime domain as the canonical
example:

```yaml
status: "active"
version: "1.0.0"
```

Both fields are already present but unspecified. Once the spec defines them,
update the domain to use the canonical values and add the DomainStatus enum
reference.

---

## Acceptance Criteria

- [ ] `status` and `version` (domain and entity) are defined in the spec with
      canonical values and semantics
- [ ] `DomainStatus` enum is documented (in spec or as a cross-domain
      reference enum)
- [ ] Versioning semantics (major/minor/patch triggers) are documented
- [ ] Agent Ontology lifecycle skill exists and covers promote and version-bump modes
- [ ] Agent Governance compliance check includes lifecycle field validation
- [ ] Financial Crime example uses canonical lifecycle field values

---

## Dependencies and Order

1. Spec definitions (items 1–3) must be complete before agent work begins
2. Agent Ontology lifecycle skill (item 4) can be built in parallel with
   Agent Governance changes (item 5) once spec is done
3. Agent Architect updates (item 6) depend on both spec and Ontology skill
4. Financial Crime example update (item 7) is last — validates all the above

---

## Out of Scope

- Runtime contract enforcement (CI/CD pipeline schema validation) — the MD-DDL
  agent layer documents and governs, it does not deploy
- Consumer subscription or notification delivery (Slack, email, webhook) —
  `consumers` is an informational field; notification is the user's
  responsibility
- Automatic breaking-change detection from git diff — out of scope for v1;
  the version bump skill assists but does not automate this
- Deprecation
