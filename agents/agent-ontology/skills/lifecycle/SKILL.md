---
name: lifecycle
description: Promote domains through lifecycle stages (Draft → Review → Active → Deprecated → Retired) and manage semantic version bumps. Use when the user wants to promote a domain, bump its version, deprecate or retire a domain, or generate/update a changelog.
---

# Skill: Lifecycle Management

Manages the lifecycle state and versioning of MD-DDL domain definitions. This skill
has two modes: **Promote** (advancing lifecycle status) and **Version Bump** (updating
the semantic version based on changes made).

## Load the Specification

Read the lifecycle and versioning rules from:

- `md-ddl-specification/2-Domains.md` — Domain Lifecycle and Domain Evolution sections
- `md-ddl-specification/3-Entities.md` — Entity Lifecycle Fields section

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
4. Offer to generate or update the `CHANGELOG.md`

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

5. **Update artifacts**:
   - Update the `version` field in domain metadata
   - Update entity `since` fields for newly added entities
   - Update entity `deprecated_at` fields for newly deprecated entities
   - Update entity `breaking_in` fields if advance notice of future breaking changes is needed
   - Offer to generate or update the `CHANGELOG.md`

### Changelog Generation

When generating or updating a `CHANGELOG.md`:

- Place the file adjacent to `domain.md`
- Follow Keep a Changelog conventions
- Use `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed` as section headings
- Include the version number and date as the entry header
- Reference the specific entities, relationships, or events affected

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

Shall I update the version field and generate a changelog entry?"
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
- **Agent Architect**: After a version bump that affects entities included in data products, flag the affected products and recommend a review. Breaking changes may require product updates.
