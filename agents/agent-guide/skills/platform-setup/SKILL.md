---
name: platform-setup
description: Use when the user asks how to install, set up, or configure MD-DDL; mentions VS Code, Copilot, Claude Code, or an IDE; asks "how do I use the agents" or "getting started with [platform]"; or needs help with invocation, troubleshooting, or effective prompts.
---

# Skill: Platform Setup

Get the user from nothing to a working agent in their environment. The setup steps
below match `README.md § Quick Start`. If the two ever disagree, the README is current.

---

## Install

**Recommended: PyPI.** Works in an existing project or an empty directory, and through a
corporate artifactory:

```bash
pip install md-ddl
md-ddl init                 # --ai claude|copilot|both (default both)
```

`md-ddl init`:

- unpacks the standard into `.md-ddl/`, which is git-ignored by default (`--track` commits it)
- installs the agent wrappers with paths rewritten to `.md-ddl/`: Claude Code slash
  commands in `.claude/commands/`, Copilot custom agents in `.github/agents/`
- writes `CLAUDE.md` or `.github/copilot-instructions.md` (skip with `--no-instructions`)
- creates `.md-ddlignore`
- checks that every agent prompt's includes resolve

Upgrade with `pip install --upgrade md-ddl && md-ddl init`. Use `--force` to overwrite
wrappers and instructions.

**Alternative: bootstrap a new project with a git submodule.**
`scripts/start-project.sh` (or `.ps1` on Windows) sets up git, adds the standard as a
submodule at `.md-ddl/`, and installs the wrappers for the chosen tool. The README has
the one-line `curl` / `Invoke-WebRequest` commands.

**Other tools installed with the package:**

- `md-ddl lint <domain-folder>`: pre-flight checks, honouring `.md-ddlignore`
- `md-ddl check`: re-verifies the agent prompts' includes

## Using the Agents

Tool | Invoke | Example
--- | --- | ---
Claude Code | Slash command | `/agent-guide I'm new to MD-DDL, where do I start?`
VS Code Copilot | `@` mention | `@agent-ontology Model a Customer domain for retail banking`

Agents: `agent-guide` (start here), `agent-ontology`, `agent-artifact`,
`agent-architect`, `agent-governance`, `agent-test`. If commands don't appear, check
that the wrappers exist (`.claude/commands/` or `.github/agents/`), that the workspace
is opened at the project root, and that Copilot Chat supports custom agents. Run
`md-ddl check` to confirm the prompts load completely.

## Working Effectively

- **Name files by path.** For example: "Review `domains/customer/domain.md`."
- **Keep one domain per conversation.** Handoffs between agents carry decisions
  across sessions (handoff files in the domain folder).
- **Be specific.** "Generate a Snowflake star schema for the Customer 360 product" beats
  "generate a schema".
- **Start with Agent Guide if you're unsure** which agent fits.

Useful opening requests:

- **New domain.** Name the domain, its purpose, three to five key concepts, the source
  systems, and the regulations that apply.
- **Concept.** Name the concept and a tool you already know to compare it with.
- **Review.** Give the path to `domain.md` and ask for structural and decision-quality
  findings by severity.
- **Generation.** Give the style, the platform, and the data product that scopes it.

## Troubleshooting

Symptom | Likely cause
--- | ---
Agent seems generic or ignores MD-DDL rules | The wrapper isn't loading `AGENT.md`, or includes failed. Run `md-ddl check`.
Governance was skipped | The request didn't mention regulatory scope. State the jurisdictions.
Output contradicts the spec | Ask Agent Guide to explain the rule, then re-engage the specialist with it.
Got a demonstration instead of production files | You're talking to Agent Guide. Switch to Agent Ontology.
