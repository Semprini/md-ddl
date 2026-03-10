# MD-DDL Project

This project uses the [MD-DDL standard](https://github.com/Semprini/md-ddl) for data modelling.

## Agents

MD-DDL provides AI agents for every stage of the modelling lifecycle.
Start with Agent Guide for learning and navigation, then use specialist agents for production work.

- **Agent Guide** — Learning companion and navigator. Start here.
  Read: `.md-ddl/agents/agent-guide/AGENT.md`
- **Agent Ontology** — Domain discovery and modelling.
  Read: `.md-ddl/agents/agent-ontology/AGENT.md`
- **Agent Artifact** — Physical schema generation (SQL DDL, JSON Schema, Parquet, Cypher).
  Read: `.md-ddl/agents/agent-artifact/AGENT.md`
- **Agent Architect** — Strategic design, data product declaration, and ODPS manifest generation.
  Read: `.md-ddl/agents/agent-architect/AGENT.md`
- **Agent Governance** — Standards conformance, compliance auditing, and governance assurance.
  Read: `.md-ddl/agents/agent-governance/AGENT.md`

## Validation

MD-DDL uses **agent-driven quality review**, not traditional linting. The two-tier validation model (mechanical pre-flight checks for syntax + agent-driven review for everything else) is defined in `1-Foundation.md`. Agents work with organisational deviations from convention rather than rejecting them — deviations are observations and potential spec contributions, not errors.

## Key References

- MD-DDL specification: `.md-ddl/md-ddl-specification/`
- Foundation principles: `.md-ddl/md-ddl-specification/1-Foundation.md`
- Complete spec (single file for AI context): `.md-ddl/md-ddl-specification/MD-DDL-Complete.md`
- Examples: `.md-ddl/examples/`
