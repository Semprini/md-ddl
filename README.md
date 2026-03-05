# Markdown Data Definition Language (md-ddl)

[![CC BY 4.0][cc-by-shield]][cc-by]

> **Version 0.7.3** (Latest)

**Model once. Reuse everywhere.**

MD-DDL is a Markdown-native standard for defining what data means, where it comes from, and how it is governed — in one format for humans, AI agents, and compilers.

md-ddl is: **AI‑native · Human‑friendly · Version‑controlled · Semantically rich · Ready for automation**

Start with [1-Foundation.md](./md-ddl-specification/1-Foundation.md) or load [MD-DDL-Complete.md](./md-ddl-specification/MD-DDL-Complete.md) for single-file AI context.

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

- `.md-ddl/.github/copilot-instructions.md` → `.github/copilot-instructions.md`
- `.md-ddl/.github/agents/agent-ontology.agent.md` → `.github/agents/agent-ontology.agent.md`
- `.md-ddl/.github/agents/agent-regulation.agent.md` → `.github/agents/agent-regulation.agent.md`

This keeps setup simple and lets you refresh from upstream when md-ddl updates.

> Maintainer note (this repo): `.github/agents/*.agent.md` wrappers are intentionally submodule-targeted (`.md-ddl/...`) templates for consumer projects. They are not intended to resolve local `agents/...` paths when editing/publishing this spec repository.

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
- **Governance in-model:** classification, PII, retention, lineage, and ownership live with definitions.
- **Source-to-canonical clarity:** source files + table transforms make mapping explicit and auditable.

---

## 🛠 Workflow

1. **Discover** with Agent Ontology
2. **Model** domains/entities/relationships/events
3. **Map** sources in `transforms/<system>/source.md` + `table_<source-table>.md`
4. **Generate** schemas, lineage, and pipeline artefacts
5. **Govern** continuously with Agent Regulation

---

## 📐 Scope

- **Domain layer:** domains, entities, enums, relationships, events, constraints
- **Source layer:** source files and transformation rules (direct, derived, lookup, reconciliation, conditional, aggregation)
- **Governance layer:** ownership, classification, PII, retention, regulatory scope, lineage

---

## 📁 Repository layout

```text
md-ddl-specification/         Normative standard
  1-Foundation.md
  ...                         Sections 2–8
  MD-DDL-Complete.md

agents/                       Canonical agent prompts and skills
examples/                     Reference examples
```

---

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
