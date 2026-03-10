---
name: platform-setup
description: Use this skill when the user mentions VS Code, Claude Code, Copilot, or any IDE; asks about setup, installation, or configuration; asks "how do I use the agents"; asks "getting started with [platform]"; or needs help with platform-specific workflows, troubleshooting, or effective prompt patterns.
---

# Skill: Platform Setup

Covers environment setup, agent invocation, and daily workflow patterns for
VS Code Copilot and Claude Code. Teaches users how to get productive in their
specific environment.

---

## VS Code Copilot

### Prerequisites

- VS Code with GitHub Copilot extension installed and active
- GitHub Copilot Chat enabled
- Git (for submodule setup)

### Setup Steps

#### Step 1 — Add MD-DDL as a Submodule

MD-DDL is consumed as a git submodule in your project. This keeps the standard
updatable independently of your model files.

```bash
# Add the submodule
git submodule add https://github.com/[org]/md-ddl .md-ddl

# Initialize and fetch
git submodule update --init
```

Update to latest version later:

```bash
git submodule update --remote .md-ddl
```

#### Step 2 — Install Agent Wrapper Files

Copy the VS Code custom-agent wrappers from the submodule into your project's
`.github/agents/` directory:

```bash
# Create the agents directory
mkdir -p .github/agents

# Copy the wrapper files
cp .md-ddl/.github/agents/agent-guide.agent.md .github/agents/
cp .md-ddl/.github/agents/agent-ontology.agent.md .github/agents/
cp .md-ddl/.github/agents/agent-artifact.agent.md .github/agents/
cp .md-ddl/.github/agents/agent-architect.agent.md .github/agents/
cp .md-ddl/.github/agents/agent-governance.agent.md .github/agents/
```

These are lightweight wrappers that include the full agent prompts from the
submodule. Consider copying all even if you don't plan to use all immediately.

#### Step 3 — Verify Agent Availability

Open VS Code, start a Copilot Chat session, and type `@`. You should see the
agents listed:

- `@agent-guide` — Learning and navigation (start here)
- `@agent-ontology` — Domain modelling
- `@agent-artifact` — Physical schema generation
- `@agent-architect` — Data product design
- `@agent-governance` — Compliance auditing

If agents do not appear, check:

- `.github/agents/` directory exists in your workspace root
- Wrapper files have valid YAML frontmatter (check for syntax errors)
- Copilot Chat is using the latest version with custom-agent support
- Workspace is opened at the root where `.github/agents/` lives

### Daily Workflow in VS Code

#### Invoking Agents

Type `@agent-name` in Copilot Chat to invoke a specific agent:

- `@agent-guide What is an entity in MD-DDL?` — Learn a concept
- `@agent-ontology Model a Customer domain for retail banking` — Start modelling
- `@agent-artifact Generate Snowflake DDL for the Customer domain` — Generate schemas
- `@agent-architect Design a data product for the analytics team` — Design products
- `@agent-governance Audit the Customer domain against GDPR` — Run compliance audit

#### Context Tips

Agents work best when they have the right files in context:

- **Open your domain file** before asking modelling questions — the agent can read it
- **Reference files by path** in your prompt: "Review `domains/customer/domain.md`"
- **Start with Agent Guide** if you are unsure which agent to use — it will direct you
- **One domain at a time** — keep conversations focused on a single domain for best results

#### Workspace Structure

A well-organized workspace makes agent interactions more effective:

```text
your-project/
  .md-ddl/                    ← MD-DDL submodule (do not edit)
  .github/
    agents/                   ← Copied wrapper files
      agent-guide.agent.md
      agent-ontology.agent.md
      agent-artifact.agent.md
      agent-architect.agent.md
      agent-governance.agent.md
  domains/
    customer/
      domain.md               ← Your domain models
      entities/
        party.md
        customer.md
    financial-crime/
      domain.md
      entities/
  sources/
    salesforce-crm/
      source.md
```

---

## Claude Code

### Prerequisites

- Claude Code CLI installed and authenticated
- Git (for submodule setup)

### Setup Steps

#### Step 1 — Add MD-DDL as a Submodule

Same as VS Code — MD-DDL is a git submodule:

```bash
git submodule add https://github.com/[org]/md-ddl .md-ddl
git submodule update --init
```

#### Step 2 — Create CLAUDE.md

Claude Code uses a `CLAUDE.md` file at the project root for configuration.
Create or update it to reference the MD-DDL agents:

```markdown
# Project Context

This project uses the MD-DDL standard for data modelling.

## MD-DDL Agents

For learning and guidance, read: `.md-ddl/agents/agent-guide/AGENT.md`
For domain modelling, read: `.md-ddl/agents/agent-ontology/AGENT.md`
For physical schema generation, read: `.md-ddl/agents/agent-artifact/AGENT.md`
For data product design, read: `.md-ddl/agents/agent-architect/AGENT.md`
For compliance auditing, read: `.md-ddl/agents/agent-governance/AGENT.md`

## Key References

- MD-DDL specification: `.md-ddl/md-ddl-specification/`
- Examples: `.md-ddl/examples/`
- Foundation principles: `.md-ddl/md-ddl-specification/1-Foundation.md`
- Complete spec (single file): `.md-ddl/md-ddl-specification/MD-DDL-Complete.md`
```

#### Step 3 — Verify Setup

Start a Claude Code session in your project directory:

```bash
claude
```

Ask Claude to read the agent guide:

```
Read .md-ddl/agents/agent-guide/AGENT.md and help me get started with MD-DDL
```

### Daily Workflow in Claude Code

#### Invoking Agents

Claude Code does not have the `@agent` syntax of VS Code. Instead, ask Claude
to adopt an agent's role by reading its prompt:

```
Read .md-ddl/agents/agent-ontology/AGENT.md and model a Customer domain for
retail banking.
```

Or set up the agent at the start of a session:

```
Read .md-ddl/agents/agent-guide/AGENT.md — I need help understanding MD-DDL.
```

#### Context Management

Claude Code reads files when asked. Effective patterns:

- **Provide file paths** — "Read `domains/customer/domain.md` and review it"
- **Load the spec when needed** — "Read `.md-ddl/md-ddl-specification/3-Entities.md`
  for the entity rules"
- **Use CLAUDE.md** — Claude automatically reads this at session start, so your
  agent references are always available
- **Keep prompts specific** — "Generate a Snowflake star schema from
  `domains/customer/domain.md`" is better than "generate a schema"

#### Differences from VS Code

Feature | VS Code Copilot | Claude Code
--- | --- | ---
Agent invocation | `@agent-name` in chat | Ask Claude to read AGENT.md
Wrapper files | `.github/agents/*.agent.md` | `CLAUDE.md` at project root
File context | Automatically from open tabs | Explicitly via file paths or tool use
Skill loading | Automatic via triggers in AGENT.md | Same — triggers still apply once agent prompt is loaded
Output | In chat panel | In terminal

---

## Effective Prompt Patterns

These patterns work across both platforms:

### Starting a New Domain

> "I need to model a [domain name] domain for [industry/purpose]. The key
> business concepts are [list 3-5 concepts]. We use [source systems] and need
> to comply with [regulations]."

### Asking About a Concept

> "Explain how [concept] works in MD-DDL. I am familiar with [tool/standard]
> so compare it to what I already know."

### Reviewing Existing Work

> "Review [path to domain.md] for structural conformance and decision quality.
> Flag any issues by severity."

### Generating Physical Schemas

> "Generate [schema type] for [platform] from [path to domain.md]. Scope it
> to the [product name] data product."

### Troubleshooting

If an agent is not behaving as expected:

- **Agent seems generic** — Make sure the wrapper file or CLAUDE.md reference
  is loading the correct AGENT.md. Check that skill triggers match your request.
- **Agent skipped governance** — Explicitly mention regulatory scope or
  governance requirements in your prompt.
- **Output does not match spec** — Ask Agent Guide to explain the relevant spec
  rule, then re-engage the specialist agent with the rule clarified.
- **Agent generated production MD-DDL when it should not have** — You may be
  talking to Agent Guide (which only demonstrates). Switch to Agent Ontology
  for production modelling.
