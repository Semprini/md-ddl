# Markdown Data Definition Language (md-ddl)

[![CC BY 4.0][cc-by-shield]][cc-by]

> **Version 0.9.0** (Latest)

**Model once. Reuse everywhere.**

MD-DDL is a Markdown-native standard for defining what data means, where it comes from, and how it is governed — then generating the physical artifacts your platforms need — all in one format for humans and AI agents.

md-ddl is: **AI‑native · Human‑friendly · Version‑controlled · Semantically rich · Ready for automation**

**Read the spec**: [1-Foundation.md](./md-ddl-specification/1-Foundation.md) or [MD-DDL-Complete.md](./md-ddl-specification/MD-DDL-Complete.md) for single-file AI context.

**Learn by conversation**: MD-DDL includes an AI learning companion. Set up md-ddl (below), then start **Agent Guide** (`@agent-guide` in VS Code Copilot, or via CLAUDE.md in Claude Code) — it adapts to your role and teaches the standard through discussion, not documentation.

---

## 🔌 Integrating md-ddl into your project

Use md-ddl as a dependency (recommended: git submodule), and keep your own model files outside `.md-ddl/`.

### 1) Add/update md-ddl

```bash
git submodule add https://github.com/[org]/md-ddl .md-ddl
git submodule update --init
```

Update later with:

```bash
git submodule update --remote .md-ddl
```

### 2) Copy integration files into your project `.github`

Copy these files from `.md-ddl` into your repository (same relative paths):

- `.md-ddl/.github/agents/*` → `.github/agents/*`

This keeps setup simple and lets you refresh from upstream when md-ddl updates.

### 3) Keep your model files in your project

```text
your-project/
  .md-ddl/                 ← dependency
  .github/                 ← copied wrapper/instruction files
  domains/
    customer/
      domain.md
      entities/
  transforms/
    salesforce-crm/
      source.md
      table_account.md
```

---

## 🌟 Why md-ddl

- **AI + human collaboration:** one shared language for SMEs, architects, and agents.
- **Standards-aligned:** practical patterns for BIAN, ISO 20022, and regulatory mapping.
- **Governance in-model:** classification, PII, retention, access roles, and regulatory scope live with definitions — with formal inheritance from domain to entity.
- **Source-to-canonical clarity:** source files + table transforms make mapping explicit and auditable.
- **Data products built in:** declare what you publish, for whom, in what shape, under what governance — right next to the model.
- **Multi-platform generation:** target Snowflake, Databricks, PostgreSQL, Neo4j, and more from one model.

---

## 🛠 Workflow

0. **Orient** with Agent Guide — understand the standard, explore concepts, find the right agent
1. **Discover** with Agent Ontology
2. **Model** domains/entities/relationships/events
3. **Map** sources in `sources/<system>/source.md` + `sources/<system>/transforms/table_<source-table>.md`
4. **Publish** data products — source-aligned, domain-aligned, or consumer-aligned
5. **Generate** schemas, lineage, and pipeline artefacts
6. **Govern** continuously with Agent Governance

---

## 📐 Scope

- **Domain layer:** domains, entities, enums, relationships, events, constraints
- **Source layer:** source files and transformation rules (direct, derived, lookup, reconciliation, conditional, aggregation)
- **Data products:** three classes (source-aligned, domain-aligned, consumer-aligned) declare publication scope, shape, audience, SLA, and masking — driving automated artifact generation
- **Governance layer:** ownership, classification, PII, retention, regulatory scope, access roles, masking strategies, lineage
- **Physical artifacts:** dimensional star schemas, normalized 3NF, wide-column reporting schemas, knowledge graph (Cypher), JSON Schema, Parquet contracts

---

## 📁 Repository layout

```text
md-ddl-specification/         Normative standard
  1-Foundation.md
  ...                         Sections 2–9
  MD-DDL-Complete.md

agents/                       Canonical agent prompts and skills
examples/                     Reference examples (Financial Crime, Simple Customer)
references/                    Architecture + industry standards reference data
```

### BIAN reference datasets

BIAN sources are maintained side-by-side by release under `references/industry_standards/bian/`
(`v13/`, `v14/`). New modelling defaults to v14; v13 remains for compatibility.

Refresh generated BIAN reference files with:

```powershell
python references/industry_standards/bian/extract-references.py --version 14.0.0
python references/industry_standards/bian/extract-references.py --version 13.0.0
```

Record file provenance in `references/industry_standards/bian/source-manifest.md` whenever
source snapshots are updated.

### Agents

Agent | Purpose
--- | ---
**Agent Guide** | Learning companion and navigator — start here
**Agent Ontology** | Domain discovery, entity modelling, source mapping
**Agent Artifact** | Physical schema generation (SQL DDL, JSON Schema, Parquet, Cypher)
**Agent Architect** | Strategic design, data product design, and ODPS manifest generation
**Agent Governance** | Standards conformance, compliance auditing, and governance assurance

> Maintainer note (this repo): `.github/agents/*.agent.md` wrappers are intentionally submodule-targeted (`.md-ddl/...`) templates for consumer projects. They are not intended to resolve local `agents/...` paths when editing/publishing this spec repository.

---

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
