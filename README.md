[![CC BY 4.0][cc-by-shield]][cc-by]

# md-ddl
Markdown Data Definition Language (MD‑DDL) - a human‑ and AI‑friendly way to model data

## **What is MD‑DDL?**  
MD‑DDL is a simple, readable way for **humans and AI to collaboratively define data meaning** using Markdown and YAML/JSON. It captures business concepts, attributes, relationships, domains, governance metadata, and diagrams — all in a format that works naturally in Git and is easy for AI to generate, validate, and evolve.

- Human‑friendly  
- AI‑native  
- Version‑controlled  
- Semantically rich  
- Ready for automation  

MD‑DDL documents are the *authoritative source of truth* for your data definitions.

---
```
                          Humans + AI
                               ↓
                             MD‑DDL
                               ↓
                            Compiler
             ┌─────────────────┴────────────────────┐
 ┌──────────────────────────┐          ┌──────────────────────────┐
 │     Knowledge Graph      │          │ Data Products & Schemas  │
 │ (RDF / OWL / Prop Graph) │          │ (DDL, Avro, APIs, etc.)  │
 └──────────────────────────┘          └──────────────────────────┘
             ↓
 ┌──────────────────────────┐
 │ Catalog / API /Reasoning │
 └──────────────────────────┘
```
---

## **Why MD‑DDL exists**  
Traditional modelling tools (UML, ERDs, enterprise catalogues) are either too technical, too rigid, or too disconnected from modern workflows and AI accessibility. Meanwhile, knowledge graphs are powerful but not approachable for everyday contributors.

MD‑DDL bridges the gap by combining:

- **Markdown** for narrative and diagrams  
- **YAML/JSON** for structured definitions  
- **Knowledge graphs** for semantic reasoning  
- **Git** for governance and collaboration  
- **AI** for generation, validation, and refactoring  

This creates a modelling ecosystem that is **business‑friendly**, **developer‑friendly**, and **AI‑friendly**.

---

## **How MD‑DDL works**  
MD‑DDL defines:

- **Domains** (Sales, Finance, Risk…)
- **Entities** (Customer, Transaction…)
- **Attributes** (with classification, sensitivity, PII, keys, patterns…)
- **Relationships** (including cross‑domain links)
- **Enumerations** (controlled vocabularies)
- **Registries** (reusable attribute definitions)
- **Constraints**
- **Diagrams** (Mermaid/PlantUML)

---

## **What the knowledge graph does**  
Once compiled from the MD-DDL, the knowledge graph becomes the **semantic runtime** powering:

### **1. UI / Catalog / API**
- Data Dictionary & Catalogue
- Lineage
- Visual modelling tools  
- Search and discovery  
- Impact analysis  
- Domain maps  
- API generation  

### **2. Data Products / Schemas**
- SQL/DDL  
- Avro/Parquet schemas  
- Data Product Definitions
- Open API
- Event definitions  
- Data quality rules  

### **3. Reasoning**
- Lineage inference  
- Cross‑domain dependency analysis  
- Governance enforcement  
- Semantic search  
- AI‑assisted modelling  

---

## **Why adopt MD‑DDL**  
- **Business‑friendly**: readable by anyone  
- **AI‑native**: LLMs can generate, validate, and refactor it  
- **Governance‑ready**: lineage, classification, sensitivity, PII, ownership  
- **Domain‑driven**: aligns with business ownership
- **Git‑native**: version control, pull requests, auditability
- **Graph‑powered**: deep semantics and reasoning

Designed for **humans, and AI working together**.

---

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
