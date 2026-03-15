---
name: lifecycle
description: Promote domains through lifecycle stages (Draft → Review → Active → Deprecated → Retired) and manage semantic version bumps. Use when the user wants to promote a domain, bump its version, deprecate or retire a domain, or generate/update lifecycle history.
---

# Skill: Lifecycle Management

Manages the lifecycle state and versioning of MD-DDL domain definitions. This skill
has two modes: **Promote** (advancing lifecycle status) and **Version Bump** (updating
the semantic version based on changes made). It also maintains the domain-scoped
`LIFECYCLE.md` file that records machine-readable change manifests and human-readable
history for both domains and products.

## Load the Specification

Read the lifecycle and versioning rules from:

- `md-ddl-specification/2-Domains.md` — Domain Lifecycle and Domain Evolution sections
- `md-ddl-specification/3-Entities.md` — Entity Lifecycle Fields section
- `md-ddl-specification/9-Data-Products.md` — Product Lifecycle, Product Versioning, and Product-Domain Lifecycle Consistency

---

## Mode 1 — Promote

Walk the user through promoting a domain from one lifecycle state to the next.

### Valid Transitions

From | To | Gate
--- | --- | ---
`Draft` | `Review` | Pre-promotion checklist passes
`Review` | `Active` | Structured review complete; version set to `1.0.0` or higher
`Active` | `Deprecated` | `superseded_by` declared (if a replacement exists); consumers notified
`Deprecated` | `Retired` | No active consumers remain; domain retained for audit

### Pre-Promotion Checklist

Before promoting from `Draft` → `Review`, verify:

- [ ] All entities in the domain summary table have corresponding detail files
- [ ] Every entity has at least one `identifier: true` attribute
- [ ] All relationships declared in the summary table have YAML definitions with `source`, `target`, `cardinality`, and `granularity`
- [ ] The Domain Overview Diagram includes all declared entities
- [ ] Domain metadata has `owners`, `stewards`, `classification`, and `regulatory_scope`
- [ ] No unresolved `# TODO:` markers remain in entity definitions (metadata TODOs are acceptable at this stage)

Before promoting from `Review` → `Active`, additionally verify:

- [ ] Domain `version` is set to `1.0.0` or higher
- [ ] All `# TODO:` markers are resolved (including metadata)
- [ ] Governance metadata is complete at domain level (`classification`, `pii`, `regulatory_scope`, `default_retention`)
- [ ] Entity governance overrides are declared where entity obligations differ from domain defaults
- [ ] All entity `status` values are consistent with the target domain status (no entity can be more advanced than its domain)
- [ ] The structured review process (Layer 1/2/3) has been completed or the user confirms it is not required

### Promotion Output

When a promotion passes all checks, produce:

1. The updated `status` field value for the domain metadata
2. If promoting to `Active`: set `version` to `1.0.0` if not already ≥ 1.0.0
3. A promotion summary listing what was checked and confirmed
4. Offer to create or update `LIFECYCLE.md`
5. Flag any data products whose status is now inconsistent with the promoted domain

When a promotion fails one or more checks, produce:

1. A list of failing checks with the specific entities or files affected
2. Recommended remediation for each failure
3. Do not update the `status` field — the promotion is blocked until all checks pass

### Demotion

Reverting from `Active` to `Draft` or `Review` is permitted only when accompanied by a major version bump. This signals to consumers that the domain is undergoing significant rework. Warn the user:

> "Reverting an Active domain to [Draft/Review] is a breaking change. This will require
> a major version bump (current: x.y.z → next: (x+1).0.0). All consumers should be
> notified. Proceed?"

---

## Mode 2 — Version Bump

Analyse what changed since the last tagged version and suggest the appropriate
semantic version bump.

### Process

1. **Identify changes**: Ask the user what has changed, or review the domain files
   to identify differences from the last known version. If git history is available,
   use it to enumerate changes.

2. **Classify each change** using the version bump rules from the spec:

   Change Type | Version Impact
   --- | ---
   Breaking — removes concepts, changes meaning, alters cardinality/granularity | Major bump
   Additive — new entities, attributes, relationships, events, enum values | Minor bump
   Corrective — typo fixes, description updates, formatting, link corrections | Patch bump

3. **Determine the bump**: The highest-impact change determines the version bump.
   If any change is breaking, it is a major bump regardless of how many additive or
   corrective changes are also present.

4. **Propose the new version**: Show the current version, the proposed new version,
   and the list of changes that drove the decision.

5. **Assess product impact**: Review data products that reference the changed entities.
   For each affected product, classify impact as:
   - `breaking` — the product's consumer contract is reduced or made incompatible
   - `additive` — the product gains schema or semantic scope without breaking existing consumers
   - `none` — the domain changed, but the product's published contract does not

6. **Produce the change manifest**: Build the machine-readable `changes:` and
   `affected_products:` block that will be written to `LIFECYCLE.md`.

7. **Update artifacts**:
   - Update the `version` field in domain metadata
   - Update entity `since` fields for newly added entities
   - Update entity `deprecated_at` fields for newly deprecated entities
   - Update entity `breaking_in` fields if advance notice of future breaking changes is needed
   - Offer to create or update `LIFECYCLE.md`

### Lifecycle File Generation

When generating or updating `LIFECYCLE.md`:

- Place the file adjacent to `domain.md`
- Maintain a `## Current State` section with current domain status/version and product status/version snapshots
- For each domain version entry, include:
  - `#### Change Manifest` — machine-readable YAML with `changes:` and `affected_products:`
  - `#### Changelog` — human-readable narrative using `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`
- Reference the specific entities, relationships, events, and products affected

Suggested manifest structure:

```yaml
changes:
  - type: breaking | additive | corrective
    scope: entity | attribute | relationship | event | enum
    entity: Entity Name
    attribute: Attribute Name
    description: Human-readable explanation

affected_products:
  - name: Product Name
    impact: breaking | additive | none
    reason: Why this product is affected
```

### Example Interaction

```
User: "I added two new entities and renamed an existing one."

Agent: "Renaming an entity is a breaking change. Combined with the two additions,
this requires a major version bump.

Current version: 1.2.0
Proposed version: 2.0.0

Changes:
- [Breaking] Entity 'Old Name' renamed to 'New Name'
- [Added] Entity 'First New Entity'
- [Added] Entity 'Second New Entity'

Affected products:
- [Breaking] Customer 360 Profile — includes the renamed entity

Shall I update the version field and write the `LIFECYCLE.md` entry?"
```

---

## Entity Lifecycle Updates

When promoting or versioning a domain, also review entity-level lifecycle fields:

- **New entities** added in this version should have `since` set to the new version number.
- **Deprecated entities** should have `status: Deprecated` and `deprecated_at` set to the current version.
- **Entities with upcoming breaking changes** should have `breaking_in` set to the planned version.
- **Entity status consistency**: After promotion, verify no entity has a status more advanced than the domain. If a domain moves to `Active`, entities still in `Draft` should either be promoted alongside it or explicitly excluded from the release.

---

## Cross-Agent Considerations

- **Agent Governance**: After promoting to `Active`, recommend a compliance audit to confirm governance metadata completeness. Produce a handoff context block if the user wants to proceed.
- **Agent Architect**: After a version bump that affects entities included in data products, pass the `affected_products` section from the change manifest so product versions can be reviewed or bumped consistently.
- **Agent Artifact**: When a physical reconciliation or migration discussion follows a version bump, provide the change manifest from `LIFECYCLE.md` as the logical intent record so physical gaps can be distinguished from regeneration noise.
