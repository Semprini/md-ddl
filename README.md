# Markdown Data Definition Language (MD-DDL)

[![CC BY 4.0][cc-by-shield]][cc-by]

> **Version 0.9.1**

**Model once. Reuse everywhere.**

MD-DDL is a Markdown-native standard for defining what data means, where it comes from, and how it is governed — then generating physical artifacts from a single source of truth that humans and AI agents share.

md-ddl is: **AI‑native · Human‑friendly · Version‑controlled · Semantically rich · Ready for automation**

**Read the spec**: [1-Foundation.md](./md-ddl-specification/1-Foundation.md) or [MD-DDL-Complete.md](./md-ddl-specification/MD-DDL-Complete.md) for single-file AI context

---

## What MD-DDL covers

- **Domain layer** — domains, entities, enums, relationships, events, and constraints
- **Source layer** — source system declarations and column-level transformation rules (direct, derived, conditional, lookup, reconciliation, aggregation)
- **Data products** — source-aligned, domain-aligned, and consumer-aligned products declaring scope, shape, consumers, SLA, governance, and masking — driving automated artifact generation
- **Governance** — classification, PII, retention, regulatory scope, access roles, and masking strategies living with the model, not in a separate system
- **Physical artifacts** — dimensional star schemas, normalized 3NF DDL, wide-column schemas, knowledge graph (Cypher), JSON Schema, Parquet contracts

---

## Quick Start

**Start a new project** using the bootstrap script — it sets up git, adds MD-DDL as a submodule, and installs the agent wrappers for your AI tool in one step.

Bash (macOS / Linux / WSL):

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/Semprini/md-ddl/main/start-project.sh)
```

PowerShell (Windows):

```powershell
Invoke-Expression (Invoke-WebRequest https://raw.githubusercontent.com/Semprini/md-ddl/main/start-project.ps1).Content
```

Or download [start-project.sh](./start-project.sh) / [start-project.ps1](./start-project.ps1) and run them locally.

---

**Learn by conversation**: MD-DDL includes **Agent Guide** an AI learning companion available from the repo via Claude or CoPilot in VS Code. It adapts to your role and goals, teaches through discussion rather than documentation, and routes you to the right specialist agent when you're ready to work.

Example prompts (Claude AI uses `/agent-guide`, CoPilot uses `@agent-guide`):

```text
/agent-guide I'm new to MD-DDL — walk me through the key concepts and help me get started.
```

```text
@agent-guide I'm a data architect at a retail bank. We have 15+ legacy source systems and no canonical data model. Give me an overview of MD-DDL and help me decide where to start.
```

```text
/agent-guide I need to model a Customer domain. We track individuals and business accounts. Walk me through the MD-DDL approach.
```

---

## Workflow

**md-ddl** is not rigid or dogmatic. A typical flow is:

1. **Discover** — scope the domain with Agent Ontology: identify entities, relationships, events, and governance posture
2. **Model** — write domain.md, entity files, enums, and events
3. **Map sources** — declare source systems and column-level transforms
4. **Publish** — declare data products with scope, shape, SLA, and masking
5. **Generate** — produce physical artifacts with Agent Artifact
6. **Govern** — audit standards conformance and regulatory posture with Agent Governance

Agent Guide helps you navigate between these stages and explains any concept along the way.

---

## Using MD-DDL in your project

MD-DDL is designed to be used as a git submodule dependency. Your model files live in your own repository; MD-DDL provides the specification, agents, and examples.

### Manual setup

If you prefer not to use the scripts and set up manually:

```bash
mkdir myproject
cd myproject
git init
git submodule add https://github.com/Semprini/md-ddl .md-ddl
git submodule update --init
```

Then copy the agent wrappers for your AI tool:

- **Copilot**: `.md-ddl/.github/agents/*.agent.md` → `.github/agents/`
- **Claude**: `.md-ddl/.claude/commands/*.md` → `.claude/commands/`

If you use Claude, you need to update `./claude/commands/*.md` files. The `agents/` path needs to be `.md-ddl/agents`

Next, create your `copilot-instructions.md` or `CLAUDE.md`. See the start project scripts for examples.

Update MD-DDL to a new release later:

```bash
git submodule update --remote .md-ddl
```

### Suggested project layout

```text
your-project/
  .md-ddl/                   ← submodule (this repo)
  .github/agents/            ← Copilot agent wrappers  (Copilot users)
  .claude/commands/          ← Claude slash commands    (Claude users)
  domains/
    customer/
      domain.md
      entities/
      products/
  sources/
    salesforce-crm/
      source.md
      transforms/
```

---

## Examples

Five reference domains at increasing complexity:

Example | Focus | Complexity
--- | --- | ---
[Simple Customer](examples/Simple%20Customer/domain.md) | Minimal — one domain, three entities, one event | Starter
[Financial Crime](examples/Financial%20Crime/domain.md) | AML/KYC/CTF — BIAN alignment, 15+ entities, sources, products, generated artifacts | Intermediate
[Healthcare](examples/Healthcare/domain.md) | FHIR R4 — HIPAA governance, source transforms, knowledge-graph product | Intermediate
[Telecom](examples/Telecom/domain.md) | TM Forum ODA — PCI-DSS, associative entities, new relationship types, dimensional product | Advanced
[Retail Sales + Retail Service](examples/Retail%20Sales/domain.md) | Bounded Context — two greenfield domains defining Customer differently, cross-domain Customer 360 | Advanced

The [feature coverage matrix](examples/README.md) maps every spec feature to the example that demonstrates it.

---

## Repository layout

```text
md-ddl-specification/        Normative standard
  1-Foundation.md            Start here to understand the model
  2-Domains.md … 9-Data-Products.md
  MD-DDL-Complete.md         Single-file version for AI context windows

agents/                      Canonical agent prompts and skills
  agent-guide/               Learning companion and navigator
  agent-ontology/            Domain modelling and source mapping
  agent-artifact/            Physical schema generation
  agent-architect/           Data product design and architecture
  agent-governance/          Standards conformance and compliance auditing

examples/                    Reference examples
  Simple Customer/
  Financial Crime/
  Healthcare/
  Telecom/
  Retail Sales/
  Retail Service/

references/                  Architecture and industry reference data
  industry_standards/        BIAN, FHIR, TM Forum reference datasets
  architecture/              Architecture blog posts and diagrams
```

---

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
