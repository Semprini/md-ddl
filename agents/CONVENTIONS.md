# Agent Conventions

Protocols shared by every MD-DDL agent. Each agent's `AGENT.md` says *when* to hand off and *to whom*; this file says *how*.

---

## Handoff Protocol

Agents own distinct parts of the work (see each agent's Boundaries table). When a request crosses into another agent's part, hand off. Do not do the other agent's work.

### Sending

1. Produce a **handoff block** (format below) in the conversation. It carries what was decided, so the next agent does not ask again.
2. Name the receiving agent (`@agent-<id>` or `/agent-<id>`), suggest an opening request, and tell the user to paste the block into it.
3. If the user will continue in a new session, also write the block to a **handoff file** (below) with `status: pending`.
4. When work goes to more than one agent (e.g. Agent Ontology for a declaration defect and
   Agent Architect for a missing consistency posture), write one block per recipient, each
   with only that agent's task, and say which order they should run in.

### Receiving

At session start, before loading domain files:

1. If the user names a domain, look in its folder for `handoff-to-<your-id>.md` with `status: pending`. Read it, then set `status: consumed`.
2. If the opening message contains a `## Handoff Context —` block, read it.
3. Don't re-ask questions the handoff answers. Treat anything under "Do not re-open" as settled.
4. Handoff files with status `consumed` or `archived` are history. Read them for context
   if useful, but don't act on their Task, and don't re-open the decisions they record
   without saying why.

### Returned work

When another agent hands back a defect in your part of the work (a missing entity, a model that does not implement a transformation, a governance gap in a product), treat it as a change request to your own artifacts. Fix the artifact. Do not change the other agent's output to make the problem go away.

---

## Handoff Block

```markdown
## Handoff Context — [Sending Agent] → [Receiving Agent]

**Domain:** [name and path to domain.md]
**Scope:** [entities, relationships, products, or files covered]

**Key decisions:**
- [decision and brief rationale, especially non-obvious choices]

**Rejected alternatives:**
- [what was considered but not chosen, and why]

**Do not re-open:**
- [questions already resolved that the next agent should accept as settled]

**Task for next agent:**
[What needs to be done]
```

---

## Handoff Artifact Files

The inline block is lost when the conversation ends. A handoff file keeps it across sessions.

**Location and name:** in the domain folder next to `domain.md`, named `handoff-to-<agent-id>.md` (e.g. `handoff-to-artifact.md`, `handoff-to-test.md`). The name encodes the destination.

**Frontmatter:**

Field | Required | Description
--- | --- | ---
`from` | Yes | Sending agent ID (e.g. `agent-ontology`)
`to` | Yes | Receiving agent ID (e.g. `agent-artifact`)
`domain` | Yes | Domain name
`domain_path` | Yes | Relative path to `domain.md`
`created` | Yes | Date written
`status` | Yes | `pending` · `consumed` · `archived`

The body is the handoff block.

**Lifecycle:** the sender writes it as `pending`; the receiver sets it to `consumed` after reading; the user or an agent sets it to `archived` when the work is done. Only one `pending` file per destination may exist. Archive the previous one before writing a new one.

**Cross-domain work:** a consumer-aligned product may span domains. The file lives in the primary domain's folder, and the block's Scope names the other domains' entities.

**Version control:** commit handoff files. `consumed` files show what an agent was told; `archived` files are the audit trail.
