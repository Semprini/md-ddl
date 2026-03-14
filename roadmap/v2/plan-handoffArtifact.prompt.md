# Plan: Handoff Artifact File Convention

## TL;DR

The short-term fix for CLA-5 (cross-agent handoff loses decision context) adds
inline handoff context blocks produced by the sending agent at the moment of
handoff. This is sufficient for same-session or near-same-session transitions.
The V2 file convention solves the harder problem: **cross-session handoffs**,
where the user closes one agent conversation and opens a new one days later.
The sending agent's context is gone. The handoff artifact is the only durable
record of what was decided.

---

## Problem

The inline context block (V1 fix) lives in the conversation transcript. If the
user:

- Closes the sending agent session and opens a fresh receiving agent session
- Returns to a domain days or weeks after the initial modelling session
- Shares a domain with a colleague who needs to continue the work

...the context block is inaccessible. The receiving agent reads the domain files
but has no record of decisions, rejected alternatives, or resolved questions.

---

## Proposed Convention

### File Location

Handoff files live in the domain folder alongside `domain.md`:

```
examples/Financial Crime/
  domain.md
  entities/
  handoff-to-artifact.md       ← written by Agent Ontology
  handoff-to-governance.md     ← written by Agent Ontology or Agent Artifact
  handoff-to-ontology.md       ← written by Agent Artifact, Architect, or Governance
  handoff-to-architect.md      ← written by Agent Ontology
```

The file name encodes the destination — the receiving agent can look for its
own handoff file on startup.

### File Format

```markdown
---
from: agent-ontology
to: agent-artifact
domain: Financial Crime
domain_path: examples/Financial Crime/domain.md
created: 2026-03-14
status: pending  # pending | consumed | archived
---

## Handoff Context — Agent Ontology → Agent Artifact

**Scope:** Party, Person, Company, Party Role, Contact Address, Address

**Key decisions:**
- Party uses bitemporal tracking — both valid-time and transaction-time
  required. AUSTRAC audit trail obligation drives this, not a modelling
  preference. Do not collapse to append-only.
- Company is a concrete specialisation of Party, not abstract. Enables direct
  instantiation without requiring a subtype record.
- self_referential relationship on Party carries relationship_attributes as
  edge properties (Association Type, Verified). Generate a bridge table for
  the many-to-many, not a FK on Party.

**Rejected alternatives:**
- Separate PartyAssociation entity — creates unnecessary indirection for
  graph traversal and was explicitly rejected by the domain owner.
- Append-only mutability for Party — rejected because AUSTRAC requires
  point-in-time reconstruction, not just event log replay.

**Do not re-open:**
- Risk Rating and Sanctions Screen Status are enums, not FK lookups.
- Next Review Date does not require a NOT NULL constraint — it is calculated
  and will be null at creation.
- The Financial Crime domain classification is Highly Confidential throughout.
  No override discussion needed.

**Task for next agent:**
Generate dimensional DDL for Party, Person, Company, Party Role, Contact
Address, and Address. Target: Snowflake. Apply SCD Type 2 for slowly_changing
entities. Party Identifier is the natural primary key — no surrogate needed.
```

### Frontmatter Fields

Field | Type | Required | Description
--- | --- | --- | ---
`from` | string | Yes | Sending agent ID (e.g., `agent-ontology`)
`to` | string | Yes | Receiving agent ID (e.g., `agent-artifact`)
`domain` | string | Yes | Domain name
`domain_path` | string | Yes | Relative path to domain.md
`created` | date | Yes | Date the file was written
`status` | enum | Yes | `pending` (not yet consumed), `consumed` (receiving agent has read it), `archived` (no longer active)

### Lifecycle

1. **Sending agent writes** the file at handoff time, drawing on session context
2. **Receiving agent reads** the file at session start — before loading domain files
3. **Receiving agent marks** `status: consumed` in the frontmatter after reading
4. **User or agent archives** the file (`status: archived`) when the work it
   describes is complete. Old handoff files are informational history.

---

## Spec Changes Required

### New section in `md-ddl-specification/` (or agent conventions doc)

Define:

- File naming convention (`handoff-to-<agent>.md`)
- Location (domain folder root)
- Required frontmatter fields
- Format of the content block (sections: Scope, Key decisions, Rejected
  alternatives, Do not re-open, Task for next agent)
- Lifecycle states and what each means
- How receiving agents discover and consume the file

### AGENT.md Changes

Each agent that receives handoffs needs a startup check:

> "At session start, look for a `handoff-to-[agent-id].md` file in the domain
> folder. If one exists with `status: pending`, read it before reading any
> domain files. Update its status to `consumed` after reading."

Each sending agent's handoff protocol needs the instruction to write the file
if the handoff is likely cross-session:

> "If the user indicates they will open a new session for the receiving agent,
> write a `handoff-to-[agent-id].md` file rather than (or in addition to) the
> inline context block."

---

## Design Decisions for V2

### Multiple handoffs to the same agent

A domain may be handed from Ontology to Artifact twice (first generation, then
an update after new entities are added). File naming collision options:

1. **Overwrite** — single file, always the latest handoff. Simple but loses
   history.
2. **Timestamp suffix** — `handoff-to-artifact-20260314.md`. Preserves history
   but requires the receiving agent to pick the latest.
3. **Status-driven** — only one `pending` file allowed; previous one must be
   `archived` before a new one is written.

Recommendation: **Status-driven** (option 3). Enforces single active handoff.
The receiving agent looks for the file with `status: pending`.

### Cross-domain handoffs

A consumer-aligned data product may span multiple domains. The handoff file
lives in the primary domain's folder. The `scope` section of the handoff
content block explicitly names any cross-domain entities referenced.

### Handoff files in version control

Handoff files should be committed to version control. They are living
documentation of modelling decisions. `archived` files are the audit trail;
`consumed` files show what the receiving agent was told. `.gitignore` should
not exclude them.

---

## Relationship to V1 Fix

The V1 inline context block and the V2 file convention are complementary, not
alternative:

- **V1 (inline block)** — Required for all handoffs. Produced at the moment of
  handoff, lives in the conversation. Solves same-session transitions.
- **V2 (file convention)** — Optional enhancement for cross-session durability.
  The sending agent writes the file when the user will switch to a new session.
  The receiving agent reads it at startup.

The file format is intentionally the same as the inline block format — the
difference is only persistence. An agent implementing V2 produces the inline
block first, then writes it to file if cross-session durability is needed.

---

## Acceptance Criteria

- [ ] File naming convention defined and documented in the spec
- [ ] Frontmatter schema defined (from, to, domain, domain_path, created, status)
- [ ] Content block sections defined (Scope, Key decisions, Rejected alternatives,
      Do not re-open, Task for next agent)
- [ ] Lifecycle states defined (pending, consumed, archived)
- [ ] All AGENT.md files updated with startup handoff-file check
- [ ] All sending AGENT.md files updated with instruction to write file for
      cross-session handoffs
- [ ] Financial Crime example includes at least one sample handoff file
      (e.g., `handoff-to-artifact.md` with `status: archived`)

---

## Out of Scope

- Automatic handoff file generation from git history or diff — V2 is
  agent-authored, not tool-generated
- Handoff file validation in CI/CD — structural checks are agent-driven, not
  linting-driven (consistent with the rest of MD-DDL validation philosophy)
- Handoff files for agent-to-agent communication within a single session —
  the inline context block handles this; files are only for cross-session
  durability
