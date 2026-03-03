---
name: domain-scoping
description: Use this skill when starting a new domain model, when the user says "model this domain" or describes a business area from scratch, when scoping or boundary questions arise, or when choosing between canonical and domain-driven modelling strategies. Also use when the user asks who should own a concept or whether two concepts are the same thing across different domains.
---

# Skill: Domain Scoping

Covers the interview protocol for new domains, the MD-DDL domain file structure,
and the modelling strategy decision (Canonical vs. Domain-Driven).

## MD-DDL Reference

The full Domains specification is in `references/domains-spec.md`. Read it before
drafting any domain file. Key sections to apply:

- **Domain Declaration and Description** — H1 heading, free-text before H2
- **Domain Metadata** — YAML block under `## Metadata`, fields and categories
- **Domain Overview Diagram** — required Mermaid graph, ELK engine, rules for what to include and exclude
- **Domain Structure** — the four summary tables (Entities, Enums, Relationships, Events) and the rules that govern them

---

## Interview Protocol

Run this protocol before drafting. Do not skip steps; each one surfaces a different
class of modelling error.

### Step 1 — Business Purpose
Understand *why* this domain exists before modelling *what* it contains.

Ask:
- What decisions or operations does this domain support?
- Who consumes the data from this domain, and what do they do with it?
- What goes wrong if this domain is missing or wrong?

### Step 2 — Candidate Concepts
Surface the nouns and verbs of the domain without committing to a structure yet.

Ask the user to describe the domain in plain language. Listen for:
- **Nouns** → candidate entities or enums
- **Verbs** → candidate relationships or events
- **Adjectives describing nouns** → candidate attributes or subtypes
- **Rules and conditions** → candidate constraints

Do not label these as entities/relationships/events during this step. Just capture
the vocabulary. Reflect it back to the user to confirm.

### Step 3 — Boundaries
Determine what is inside and outside this domain.

Ask:
- Are there concepts that *feel* like they belong here but might be owned elsewhere?
- Are there other teams or systems that model similar concepts?
- Should this domain be able to exist independently, or does it depend on concepts
  from another domain?

This surfaces the canonical vs. bounded context decision (see Modelling Strategy).

### Step 4 — Governance Posture
Capture the metadata inputs. These cannot be inferred.

Ask:
- Who is accountable for the business health of this data?
- Who is accountable for the technical health?
- Are there regulatory frameworks that apply (GDPR, AML, APRA, SOX, etc.)?
- How long does data in this domain need to be retained?
- What source systems feed this domain?

If the user does not know, mark the relevant YAML fields with `# TODO:` and proceed.

### Step 5 — Standards Check
Before drafting, check whether Standards Alignment applies.

If the domain maps to an industry (banking, insurance, healthcare, payments, telecom):
load `skills/standards-alignment/SKILL.md` and run the standards check in parallel
with drafting.

---

## Modelling Strategy

Determine and state the strategy explicitly in the domain description and in the
metadata `tags` field. Present both options to the user if it is not obvious.

### Canonical
**Use when:** the concept is universal across the organisation — reference data,
foundational objects (Party, Currency, Location), or data that must mean exactly
the same thing everywhere.

**Implications:**
- Strict governance; one domain owns it
- Other domains reference but do not redefine
- Changes require cross-domain impact assessment
- Tag: `Canonical`

### Domain-Driven (Bounded Context)
**Use when:** the concept has meaningfully different attributes or rules in different
business contexts, or teams need autonomous ownership.

**Implications:**
- The same real-world thing may appear as different entities in different domains
- The compiler maps them at integration time; each domain owns its version
- Lower governance overhead; higher integration complexity
- Tag: `BoundedContext`

**Decision prompt for the user:**

> "Does [concept] need to mean exactly the same thing everywhere in the organisation,
> or does [Team A]'s version of it differ meaningfully from [Team B]'s? If the answer
> is 'it's slightly different but close enough', that's often a signal for Canonical
> with a well-governed specialisation pattern."

---

## Domain File Checklist

Before handing a domain file to the user for review, confirm:

- [ ] H1 heading matches the agreed domain name
- [ ] Description explains business purpose, not technical implementation
- [ ] All required metadata fields present (or flagged `# TODO:`)
- [ ] `regulatory_scope` lists all frameworks identified in Step 4
- [ ] Domain Overview Diagram uses `graph TD` or `graph LR` with ELK engine
- [ ] Diagram includes all entities, inheritance arrows, and labelled relationship edges
- [ ] Diagram hyperlinks are on the 3–5 most central entities only
- [ ] All four summary tables present (Entities, Enums, Relationships, Events)
- [ ] Every Name cell contains a Markdown link to the detail file anchor
- [ ] `Specializes` column populated for all subtypes
- [ ] No H3 headings in the domain file (H3 is reserved for detail files)
- [ ] Modelling strategy stated in description and tags
