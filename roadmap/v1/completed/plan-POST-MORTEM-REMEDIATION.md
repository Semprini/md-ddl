# Post-Mortem Remediation Plan

Three work items from the Example Completeness post-mortem, sized and
sequenced for inclusion in the v1 roadmap.

---

## 1. `{{INCLUDE}}` Stub Mechanism — Needs Work

### Problem

The `{{INCLUDE: path}}` directive is used in 31 locations:

Location | Count | Purpose
--- | --- | ---
Reference stubs (`agents/*/skills/*/references/`) | 18 | Load spec sections into skills on demand
AGENT.md files | 5 | Load `1-Foundation.md` into every agent
SKILL.md files (inline) | 2 | Load specs directly (product-design, odps-alignment)
`.github/agents/` wrapper files | 6 | Load canonical AGENT.md into Copilot custom agents

The `.github/agents/` wrappers are the **only** location where `{{INCLUDE}}`
is actually processed — VS Code Copilot custom agents support this directive
natively. The other 25 uses are dead code in all current agent platforms
(VS Code Copilot Chat, Claude, ChatGPT).

### Why This Matters

Every skill that says "load `references/entities-spec.md`" currently resolves
to a 4-line file containing a path and nothing else. Agents must either:

- Recognise the `{{INCLUDE}}` pattern and follow the path (extra round-trip)
- Already know to load the spec file directly (bypassing the stub)

Neither is reliable across models.

### Proposed Fix

**Replace reference stubs with direct spec paths in skill loading instructions.**

This does not mean deleting the stub files — they serve as documentation of which
spec sections a skill depends on. But skills should not instruct agents to "load"
files that resolve to nothing.

#### Steps

Step | Action | Files Affected
--- | --- | ---
1a | In each SKILL.md that references a stub, change the loading instruction from "Load `references/X-spec.md`" to "Load `md-ddl-specification/X.md` (spec path: `references/X-spec.md`)" | ~10 SKILL.md files (domain-scoping, entity-modelling, relationship-events, source-mapping, domain-review, concept-explorer, orientation, product-design, odps-alignment)
1b | In each AGENT.md that uses `{{INCLUDE: md-ddl-specification/1-Foundation.md}}`, add a comment above: `<!-- Platform note: {{INCLUDE}} is processed by VS Code Copilot custom agents. Other platforms should load this file directly. -->` | 5 AGENT.md files
1c | Add a "Reference Loading" section to `copilot-instructions.md` explaining the `{{INCLUDE}}` convention and platform-specific behaviour | 1 file
1d | Keep stub files in place (they document dependencies) but add a header comment: `<!-- This stub is processed by {{INCLUDE}}-aware platforms. Other platforms: load the path below directly. -->` | 18 stub files

#### Size Estimate

~30 files touched, but all changes are mechanical (find-replace pattern). No
spec changes needed. No version bump.

#### Risk

Low. Changes are additive — nothing breaks if `{{INCLUDE}}` starts working on
a new platform. Stubs remain as documentation.

---

## 2. Example Authoring Orchestration — Needs Work

### Problem Statement

No skill provides end-to-end guidance for creating a complete MD-DDL example
domain. The worked-examples skill (agent-guide) teaches users how to *read*
examples. The ontology skills (domain-scoping, entity-modelling, etc.) cover
individual modelling stages but don't sequence file creation.

During Healthcare creation, guidance was composed implicitly from 5+ skills.

### Impact

When a user asks "create an example like Financial Crime for healthcare", the
agent must assemble orchestration from multiple skills without a blueprint. This
works with capable models but produces inconsistent results with smaller models
or when context is limited.

### Proposed Solution

**Add a "Domain Authoring Checklist" section to agent-ontology's domain-scoping skill.**

This belongs in domain-scoping (not worked-examples) because example authoring is
production modelling — it follows the ontology agent's lifecycle, not the guide
agent's teaching lifecycle.

#### Actions

Step | Action | Files Affected
--- | --- | ---
2a | Add a `## Domain Authoring Checklist` section to `agents/agent-ontology/skills/domain-scoping/SKILL.md` | 1 file
2b | Checklist covers the full file-creation sequence with cross-references to relevant skills | —
2c | Add Healthcare as a third track in `agents/agent-guide/skills/worked-examples/SKILL.md` (alongside Simple Customer and Financial Crime) | 1 file

#### Proposed Checklist Content

```markdown
## Domain Authoring Checklist

When creating a complete domain from scratch, follow this sequence.
Each step references the skill that owns the detailed guidance.

1. **Domain file** — `domain.md`
   - Metadata, governance, overview diagram, summary tables
   - Guidance: this skill (domain-scoping) → Domain File Checklist
   - Standards: load standards-alignment if industry standard applies

2. **Entity detail files** — `entities/*.md` (one per entity)
   - Attributes, existence, mutability, temporal, governance, diagrams
   - Guidance: entity-modelling → Entity Checklist, Enum Checklist
   - Decisions: concept realisation framework, inheritance reasoning

3. **Enumerations file** — `enums.md`
   - All domain enums in one file (or co-located with entities)
   - Guidance: entity-modelling → Enum Checklist
   - External standards: representative subset (5–15 values) + standard reference

4. **Relationship YAML** — co-located in entity files
   - Type, cardinality, granularity, constraints
   - Guidance: relationship-events → Relationship Checklist

5. **Event files** — `events/*.md` (one per event)
   - Actor, entity, emitted_on, payload, governance
   - Guidance: relationship-events → Event Checklist

6. **Source system files** — `sources/*/source.md`
   - Change model, feeds table, data quality tier
   - Guidance: source-mapping → Source File Checklist

7. **Data product files** — `products/*.md`
   - Class, entities, SLA, governance overrides, masking
   - Guidance: product-design (agent-architect) → Product Design Process

8. **Update domain.md** — refresh summary tables to reflect all created files
```

#### Scope

~50 lines added to domain-scoping SKILL.md, ~15 lines added to worked-examples
SKILL.md. No spec changes. No version bump.

#### Assessment

Low risk. Additive content. Does not change any existing behaviour.

---

## 3. Minor Items (Bundled)

Three small items grouped as one work package.

### 3a. Enum Subset Guidance

**Problem:** The enumerations spec (§4) has no guidance on external standard enums
— how many values to include, or how to reference the authoritative source.

**Fix:** Add a paragraph to `md-ddl-specification/4-Enumerations.md` after the
Naming Rules section:

```markdown
### External Standard Enumerations

When an enum's values are defined by an external standard (e.g., ISO 4217
currencies, HL7 FHIR value sets, BIAN enumerations), include a representative
subset of 5–15 values sufficient to demonstrate the pattern. Reference the
authoritative source using a `standard` metadata field:

\`\`\`yaml
values:
  AUD:
    description: Australian Dollar
  USD:
    description: United States Dollar
  EUR:
    description: Euro
standard:
  name: ISO 4217
  version: "2024"
  url: https://www.iso.org/iso-4217-currency-codes.html
  note: Representative subset — full standard defines 180+ active currency codes
\`\`\`

Physical artifact generation should support loading the complete value set from
the referenced standard when the representative subset is insufficient.
```

**Files:** `md-ddl-specification/4-Enumerations.md` (1 file, ~20 lines added)
**Spec impact:** Minor additive guidance. Version bump: 0.9.0 → 0.9.1 (if this
is considered a rule change rather than a clarification).

### 3b. Event Payload Format Standardisation

**Problem:** The spec shows two payload formats:

- **List-of-dicts** (Pattern A): `- event timestamp:` with nested type/description
- **Flat dict** (Pattern B): `event_timestamp:` as a dict key

5 Financial Crime events use Pattern A, 5 Healthcare events + 1 Financial Crime
event use Pattern B. The spec's own examples use Pattern A.

**Fix:** Standardise on **flat dict format** (Pattern B) because:

- It is consistent with entity attribute YAML (which uses flat dicts)
- It avoids the YAML ambiguity of list-of-single-key dicts
- It is what new examples already use

Actions:

Step | Action | Files Affected
--- | --- | ---
3b-i | Update the spec example in `6-Events.md` to use flat dict format | 1 spec file
3b-ii | Update the 5 Financial Crime events that use list-of-dicts to flat dict | 5 event files
3b-iii | Add a note to the spec: "Event payload attributes use the same dict format as entity attributes" | 1 spec file

**Files:** 6 files total
**Spec impact:** Format standardisation. Version bump: 0.9.0 → 0.9.1.

### 3c. BIAN v14 Reference Data

**Problem:** The BIAN README says "default to v14" but:

- `references/industry_standards/bian/v14/` contains only a README (no source JSON)
- `agents/.../standards/bian/v14/` contains only a README (no generated markdown)
- `agents/.../standards/bian/v13/` — also only a README (v13 data lives at root level)

**Fix:** Two-phase approach:

Step | Action | Dependency
--- | --- | ---
3c-i | Update BIAN README to say "using v13 — v14 pending source data download" | None — can do now
3c-ii | Download v14 source JSON when BIAN publishes v14 BOM data | External dependency
3c-iii | Run `extract-references.py --version 14.0.0` to generate v14 markdown | Depends on 3c-ii
3c-iv | Move root-level v13 files (`bo-classes.md`, etc.) into `v13/` directory | After v14 is available

**Files:** 1 README update now; 4+ files later when v14 data is available
**Risk:** 3c-ii depends on BIAN publishing v14 BOM data. The interim fix (3c-i)
is honest labelling.

---

## Execution Sequence

The three items are independent and can be done in any order. Suggested sequence
based on impact and size:

Priority | Item | Rationale
--- | --- | ---
1 | 3b — Event payload format | Fixes inconsistency across two example domains; touches spec
2 | 3a — Enum subset guidance | Small spec addition; prevents future divergence
3 | 2 — Authoring checklist | Productivity improvement; additive to existing skill
4 | 1 — `{{INCLUDE}}` stubs | Largest scope (~30 files) but lowest urgency; current workaround is functional
5 | 3c — BIAN v14 | Blocked on external data; interim fix is trivial

Items 3a and 3b both touch the spec and could share a version bump (0.9.0 → 0.9.1).
