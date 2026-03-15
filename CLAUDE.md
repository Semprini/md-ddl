# MD-DDL Project

This is the **source repository** for the MD-DDL standard — its specification, agent prompts, skills, and examples.

## Agents

MD-DDL provides AI agents for every stage of the modelling lifecycle.
Invoke them with slash commands or let the auto-routing below guide you.

Command | Agent | Purpose
--- | --- | ---
`/agent-guide` | Agent Guide | Learning, navigation, concept explanation. Start here.
`/agent-ontology` | Agent Ontology | Domain discovery, entity modelling, source mapping.
`/agent-artifact` | Agent Artifact | Physical schema generation (SQL DDL, JSON Schema, Parquet, Cypher).
`/agent-architect` | Agent Architect | Data product design, architecture discussion, ODPS manifests.
`/agent-governance` | Agent Governance | Standards conformance, compliance auditing, governance assurance.

Agent prompts: `agents/<agent-name>/AGENT.md`

## Auto-Routing

When no slash command is given, select the appropriate agent based on the request:

Request type | Agent to activate
--- | ---
"What is...", "How does...", "Explain...", onboarding | Read `agents/agent-guide/AGENT.md`
Modelling a domain, designing entities, mapping sources | Read `agents/agent-ontology/AGENT.md`
Brownfield adoption, "we already have", existing systems, import schema | Read `agents/agent-ontology/AGENT.md` (baseline-capture or schema-import skill)
Generating DDL, JSON Schema, Parquet, Cypher | Read `agents/agent-artifact/AGENT.md`
Reconcile generated vs existing, gap analysis | Read `agents/agent-artifact/AGENT.md` (reconciliation skill)
Data product design, architecture, ODPS | Read `agents/agent-architect/AGENT.md`
Compliance audit, governance review, standards check | Read `agents/agent-governance/AGENT.md`
Review, evaluate, audit the standard itself | Read `.prompts/md-ddl-layered-review-process.md` for orchestration, then load the appropriate layer prompt from `.prompts/`

When activating an agent, also follow its skill-loading protocol — read the applicable `SKILL.md` files before responding.

## Validation

MD-DDL uses **agent-driven quality review**, not traditional linting. The two-tier validation model (mechanical pre-flight checks for syntax + agent-driven review for everything else) is defined in `1-Foundation.md`. Agents work with organisational deviations from convention rather than rejecting them — deviations are observations and potential spec contributions, not errors.

## Review Output

All review, evaluation, and post-mortem outputs must be written to `roadmap/review/`,
prefixed with the date in `YYYY-MM-DD` format. Examples:

- `roadmap/review/2026-03-15-layer1-structural-review.md`
- `roadmap/review/2026-03-15-consolidated-review.md`
- `roadmap/review/2026-03-15-post-mortem-<topic>.md`

This applies whenever a user requests:

- A review of the spec, agents, examples, or repository structure
- A post-mortem on a completed piece of work
- Any evaluation, audit, or findings document intended to inform the roadmap

The `.prompts/` files contain the prompts for each layer of review. Each prompt
already includes the correct output path instruction.

## Working Style

### Sequential Execution

- **Never spin up parallel subagents or background agents for implementation
  work.** One task at a time, completed and verified before moving to the next.
- When implementing a plan with multiple items, create a TodoWrite task list at
  the start covering every item, then mark each complete before proceeding.
- Do not batch multiple file writes across unrelated items in a single response.
  Each plan item is its own step: write → verify → mark done → proceed.
- When a plan item requires reading files before writing, do the reads first
  in a single step, then write in the next.

### Resuming After Interruption

If the conversation starts mid-plan, or the user indicates work was cut off:

1. Run `git status` to identify which files have been modified since the last commit
2. Read any recently modified files to confirm their current state
3. Cross-reference against the plan to identify the last completed item
4. State what has been done and what remains before proceeding — do not
   silently re-do completed work or skip ahead

This keeps incomplete work recoverable without re-reading the full conversation
history or repeating already-finished steps.

## Architectural Philosophy

MD-DDL implements the **Data Autonomy** architectural style. See `references/architecture/` for foundational blog posts and external references, and `agents/agent-architect/skills/architecture/SKILL.md` for the distilled 13 tenets.

## Key References

- MD-DDL specification: `md-ddl-specification/`
- Foundation principles: `md-ddl-specification/1-Foundation.md`
- Complete spec (single file for AI context): `md-ddl-specification/MD-DDL-Complete.md`
- Architectural philosophy and tenets: `agents/agent-architect/skills/architecture/SKILL.md`
- Architecture source material: `references/architecture/`
- Examples: `examples/`
- Review and evaluation prompts: `.prompts/`
- Review outputs: `roadmap/review/`
- Spec concatenation rules: `.prompts/concat-md-ddl-specs.prompt.md`
