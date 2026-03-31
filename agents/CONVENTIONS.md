# Agent Conventions

Shared conventions for MD-DDL agents. Individual agent behaviour is defined in each agent's `AGENT.md`; this file covers cross-agent protocols that all work-performing agents follow.

---

## Handoff Artifact Files (V2)

### Purpose

When a user closes one agent session and opens a new session with a different agent, the inline handoff context block (V1) is lost with the conversation. Handoff artifact files provide **cross-session durability** — a persistent record of decisions, rejected alternatives, and task instructions that the receiving agent can read at startup.

### Relationship to Inline Handoff Blocks (V1)

V1 and V2 are complementary, not alternative:

- **V1 (inline block)** — Required for all handoffs. Produced at the moment of handoff, lives in the conversation. Solves same-session transitions.
- **V2 (file)** — Optional enhancement for cross-session durability. The sending agent writes the file when the user will switch to a new session. The receiving agent reads it at startup.

The file format mirrors the inline block format — the difference is persistence. An agent implementing V2 produces the inline block first, then writes it to file if cross-session durability is needed.

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

### File Naming

`handoff-to-<agent-id>.md` — the file name encodes the destination. The receiving agent looks for its own handoff file on startup.

### Frontmatter Schema

Field | Type | Required | Description
--- | --- | --- | ---
`from` | string | Yes | Sending agent ID (e.g., `agent-ontology`)
`to` | string | Yes | Receiving agent ID (e.g., `agent-artifact`)
`domain` | string | Yes | Domain name
`domain_path` | string | Yes | Relative path to domain.md
`created` | date | Yes | Date the file was written
`status` | enum | Yes | `pending` · `consumed` · `archived`

### Content Block Template

```markdown
## Handoff Context — [Sending Agent] → [Receiving Agent]

**Scope:** [entities, relationships, or aspects covered]

**Key decisions:**
- [decision and brief rationale — especially non-obvious choices]

**Rejected alternatives:**
- [what was considered but not chosen, and why]

**Do not re-open:**
- [questions already resolved that the next agent should accept as settled]

**Task for next agent:**
[Clear description of what needs to be done]
```

### Lifecycle

1. **Sending agent writes** the file at handoff time, drawing on session context. Set `status: pending`.
2. **Receiving agent reads** the file at session start — before loading domain files. Accept decisions marked "Do not re-open" as settled.
3. **Receiving agent updates** `status: consumed` in the frontmatter after reading.
4. **User or agent archives** the file (`status: archived`) when the work it describes is complete. Archived files are informational history.

### Multiple Handoffs to the Same Agent

Status-driven: only one `pending` file per destination agent is allowed. The previous handoff file must be `archived` before a new one is written. The receiving agent looks for the file with `status: pending`.

### Cross-Domain Handoffs

A consumer-aligned data product may span multiple domains. The handoff file lives in the primary domain's folder. The Scope section explicitly names any cross-domain entities referenced.

### Version Control

Handoff files should be committed to version control. They are living documentation of modelling decisions. `archived` files are the audit trail; `consumed` files show what the receiving agent was told. `.gitignore` should not exclude them.
