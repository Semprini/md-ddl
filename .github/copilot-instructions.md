# Copilot Instructions for md-ddl

## What this repository is

This repo is the **source of the MD-DDL standard** — its specification, agent prompts, skills, and worked examples. It is not a runtime application and not a domain modelling workspace.

Contributors here are working on one of four things:

1. **The specification** — the normative rules of the MD-DDL language
2. **Agent prompts and skills** — the AI guidance layer built on top of the spec
3. **Examples** — reference domain and entity files that demonstrate the spec
4. **Tooling** — any compiler, validator, or utility that processes MD-DDL files

Understanding which of these you are working on determines everything about how to proceed.

---

## Repository layout

```
md-ddl-specification/         Normative spec — source of truth for all rules
  1-Foundation.md             Core principles and document structure
  2-Domains.md                Domain file format and metadata
  3-Entities.md               Entity and attribute definitions
  4-Enumerations.md           Enum structure and naming
  5-Relationships.md          Relationship semantics and YAML
  6-Events.md                 Event structure and temporal rules
  MD-DDL-Complete.md          Concatenated single-file version (generated)

agents/
  agent-ontology/             Discovery and design agent
    AGENT.md                  Core prompt — identity, modes, skill index
    skills/
      domain-scoping/         Interview protocol + Domains spec
      entity-modelling/       Concept realisation + Entities + Enumerations spec
      relationship-events/    Relationships + Events spec
      standards-alignment/    Industry standards mapping (self-contained)

  agent-regulation/           Regulatory compliance and audit agent
    AGENT.md                  Core prompt — identity, modes (Audit/Monitor/Remediate), skill index
    skills/
      regulatory-compliance/  Jurisdiction mapping + regulator file loader (shared with agent-ontology)
        regulators/           Per-regulator guidance files (apra.md, gdpr.md, fatf.md, etc.)
      compliance-audit/       Three-level audit protocol, gap report format, severity rules

examples/
  Financial Crime/            Primary reference example (most current)
    domain.md                 Reference-quality domain file
    entities/party.md         Reference-quality entity detail file
    entities/party_role.md    Reference-quality entity detail file
```

---

## Working on the specification

### The spec is the authority — agents defer to it

Every rule in every agent prompt and skill must be traceable to the spec. If a rule exists in an agent prompt but not in the spec, it should either be
added to the spec (if it's a genuine standard) or removed from the prompt (if it's agent-specific behaviour).

### Section ownership

Each spec section owns a distinct layer of the language:

File | Owns
--- | ---
`1-Foundation.md` | Principles, document structure, two-layer model
`2-Domains.md` | Domain file format, metadata schema, diagram rules, summary tables
`3-Entities.md` | Entity YAML, attribute types, constraints, diagrams, inheritance
`4-Enumerations.md` | Enum formats, naming, dictionary vs. simple list
`5-Relationships.md` | Relationship types, granularity, cardinality, constraint syntax
`6-Events.md` | Event structure, payload design, temporal priority, actor/entity

When adding or changing a rule, edit the owning section only. Do not duplicate rules across sections.

### MD-DDL-Complete.md

This is a generated file — a concatenation of sections 1–6 in order. It exists for AI context loading (single-file spec injection into agent prompts). Do not edit it directly. Regenerate it by concatenating the section files after any spec change. When concatenating, strip the first 2 lines which contain the same level 1 heading in each file and last 2 lines which contain a url link to the next file.

### Versioning

The spec uses semantic versioning in the H1 heading of each file. A version bump is required any time a rule changes in a way that would alter the output of a correctly-authored MD-DDL file. Corrections to examples or prose clarifications do not require a version bump.

---

## Working on agents and skills

### The agent/spec relationship

Agent prompts and skills are **guidance built on top of the spec** — they teach an AI how to apply the rules, not what the rules are. If you find yourself
repeating a spec rule verbatim inside a skill, that's a signal to reference the spec file instead.

### Skill structure

Each skill follows the progressive disclosure pattern:

```
skills/<skill-name>/
  SKILL.md              Trigger description (frontmatter) + process guidance
  references/           Spec sections or external references loaded on demand
```

The `SKILL.md` body should stay under 500 lines. Heavy spec content belongs in `references/` and is loaded only when the skill is active. See the skill-creator skill pattern for detailed guidance on writing effective skill files.

### The spec reference stub pattern

Reference files in `skills/*/references/` are stubs that point to the canonical spec file — they do not duplicate content. This means a spec update propagates automatically without touching agent files. When adding a new spec reference, create the stub and point it at the correct `md-ddl-specification/` file.

### Agent responsibilities and boundaries

Each agent owns a distinct lifecycle stage. Do not add capabilities to an agent that belong to another agent's stage.

Agent | Lifecycle stage | Owns
--- | --- | ---
`agent-ontology` | Discovery and design | Domain modelling, entity authoring, relationship and event design, standards alignment during authoring
`agent-regulation` | Governance assurance | Compliance metadata auditing, regulatory monitoring, governance remediation

**Boundary rule:** Agent Ontology applies governance metadata during authoring (first pass). Agent Regulation audits and maintains that metadata over time
(ongoing assurance). If a compliance gap requires a structural model change — a new entity, attribute, or relationship — Agent Regulation flags it and
defers the structural work to Agent Ontology. Do not add structural modelling capability to Agent Regulation.

### Shared skills

Some skills are used by more than one agent. The `regulatory-compliance` skill is the current example — Agent Ontology uses it to apply governance metadata
during domain authoring; Agent Regulation uses it as the requirements benchmark during audits.

Shared skills live under the agent that owns them conceptually. Agent Regulation owns `regulatory-compliance` because compliance assurance is its primary purpose. Agent Ontology loads it as an external reference.

When editing a shared skill, consider the impact on both agents. The skill's trigger description should reflect all contexts in which it is used.

### Adding a new agent

New agents follow the same structure as `agent-ontology/`:
- `AGENT.md` — identity, behaviour modes, skill index, non-negotiable output rules
- `skills/` — one skill per coherent process area, not per spec section

The skill index in `AGENT.md` is the triggering mechanism. Write trigger descriptions to be specific and slightly pushy — the agent should load a skill
when in doubt, not skip it to save context.

Before adding a new agent, confirm it occupies a distinct lifecycle stage not already covered. Add it to the agent responsibilities table above.

### What belongs in agents, not in the spec

- Interview protocols and question sequences
- Decision frameworks for trade-offs (entity vs. enum vs. attribute)
- Checklists for output quality review
- Industry standards mapping tables
- Behaviour modes (Interview / Drafting / Refinement)

None of these are rules of the language. They are guidance for applying the language.

---

## Table formatting in markdown

When writing tables in markdown, use pipe (`|`) syntax without leading and trailing pipes with a header row and separator line. For example:

```markdown
Column 1 | Column 2 | Column 3
--- | --- | ---
Value 1 | Value 2 | Value 3
```

---

## Working on examples

### What examples are for

Examples serve two purposes: they demonstrate correct spec application for human readers, and they act as AI context references (agents are instructed to use `examples/Financial Crime/` as the quality benchmark).

### The current reference example

`examples/Financial Crime/` is the highest-quality example in the repo. When in doubt about what correct MD-DDL looks like, this is the reference. The domain file uses v0.6 table format; the entity files use current classDiagram and YAML patterns.

### Adding or updating examples

- New examples must conform to the current spec version — check the version header in `1-Foundation.md` before writing.
- If spec and example disagree, the spec wins. Flag the discrepancy and update the example to match the spec — do not leave known-incorrect examples in place.
- Keep links in examples relative and navigable: `entities/party.md`, `#party`.
- Never invent reference URLs for standards. Verify before adding.

### Upgrading existing examples

Examples must stay current with the spec. When a spec version bumps, check all examples for patterns that the new version has superseded and update them.

When upgrading an example, update all patterns in the file in a single pass — do not partially upgrade a file, as mixed old/new patterns are more confusing than either consistently old or consistently new.

---

## Cross-cutting rules for all contributions

- **Spec owns the rules.** Agents and examples implement them. When they conflict, fix the agent or example, not the spec (unless the spec is genuinely wrong).
- **One source of truth per rule.** If a rule appears in multiple places, that's technical debt. Flag it.
- **No invented content.** Do not fabricate standards references, regulatory requirements, or example data that is not verifiable.
- **Validate Markdown structure** on any changed file: table/link integrity, Mermaid syntax, heading hierarchy, and YAML block correctness.
- **No runtime assumptions.** There is no build system. Validation is structural and manual (or via a linter if one is added). Do not add code that assumes a compilation or test pipeline exists unless one has been defined.
