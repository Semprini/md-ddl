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
`/review` | Review | Layered structural, adversarial, and stakeholder review.

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
Review, evaluate, audit the standard itself | Read `.prompts/md-ddl-layered-review-process.md` for orchestration, then the appropriate layer prompt

When activating an agent, also follow its skill-loading protocol — read the applicable `SKILL.md` files before responding.

## Validation

MD-DDL uses **agent-driven quality review**, not traditional linting. The two-tier validation model (mechanical pre-flight checks for syntax + agent-driven review for everything else) is defined in `1-Foundation.md`. Agents work with organisational deviations from convention rather than rejecting them — deviations are observations and potential spec contributions, not errors.

## Key References

- MD-DDL specification: `md-ddl-specification/`
- Foundation principles: `md-ddl-specification/1-Foundation.md`
- Complete spec (single file for AI context): `md-ddl-specification/MD-DDL-Complete.md`
- Examples: `examples/`
- Review and evaluation prompts: `.prompts/`
- Spec concatenation rules: `.prompts/concat-md-ddl-specs.prompt.md`
