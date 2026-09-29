---
name: adoption-planning
description: Use when the user mentions existing systems, legacy, migration, brownfield, "we already have", "starting from", or "current state"; asks how to adopt MD-DDL alongside existing data assets; or asks about maturity levels, adoption timelines, or planning a rollout.
---

# Skill: Adoption Planning

Help the user assess their current data landscape and plan adoption, domain by domain.

Load `guides/adoption-playbook.md` (maturity model, advancement criteria, the four
journey patterns, baselines, coexistence) and `md-ddl-specification/10-Adoption.md`
(the `adoption:` and `baseline:` metadata) before answering.

---

## Process

1. **Current state.** Ask what assets exist, on which platforms, and across how many
   domains. The signals map to the playbook's patterns, and most organisations mix
   several:

   Signal | Pattern
   --- | ---
   Star schemas, fact and dimension tables, a warehouse | A: existing schemas (the default)
   Enterprise, canonical, or common data model | B: canonical models
   dbt, SSIS, Informatica, ETL/ELT pipelines | C: pipelines
   Collibra, Purview, Alation | D: catalogue

2. **Target state.** Ask for the maturity level and timeline, and whether this is a
   single-domain pilot. Declarative (Level 4) is a realistic first target. Automated
   (Level 5) needs CI/CD integration and usually comes later.
3. **Starting domain.** Recommend one well-understood domain with clear ownership and
   willing stakeholders. Success there becomes the template for the next.
4. **Roadmap.** For each domain, give the starting pattern, assets to baseline, target
   maturity and date, milestones per level, and risks (stakeholder time, platform
   access). Present it as a table the user can keep.
5. **Hand off** to Agent Ontology. Use baseline-capture to document existing assets,
   schema-import to fast-track from DDL to a draft domain, or domain-scoping for
   greenfield modelling. Offer to draft the opening request.

**Stalled adoption.** If a domain's `adoption.target_date` has passed without reaching
`target_maturity`, flag it as stalled and help the user decide: reassess the timeline,
remove blockers, or change the target.

## Points Worth Making

- You don't start from scratch. Baselines document what exists and are superseded as
  canonical entities replace them.
- Maturity is per domain, so the organisation progresses one domain at a time.
- Coexistence of baselines and canonical entities during transition is expected.
- Schema import is the fastest path: paste DDL, answer a few questions, and get a
  draft domain.
