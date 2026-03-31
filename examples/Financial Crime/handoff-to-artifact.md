---
from: agent-ontology
to: agent-artifact
domain: Financial Crime
domain_path: examples/Financial Crime/domain.md
created: 2026-03-14
status: archived
---

## Handoff Context — Agent Ontology → Agent Artifact

**Scope:** Party, Person, Company, Party Role, Contact Address, Address

**Key decisions:**
- Party uses bitemporal tracking — both valid-time and transaction-time
  required. AUSTRAC audit trail obligation drives this, not a modelling
  preference. Do not collapse to append-only.
- Company is a concrete specialisation of Party, not abstract. Enables direct
  instantiation without requiring a subtype record.
- self_referential relationship on Party carries relationship_attributes as
  edge properties (Association Type, Verified). Generate a bridge table for
  the many-to-many, not a FK on Party.

**Rejected alternatives:**
- Separate PartyAssociation entity — creates unnecessary indirection for
  graph traversal and was explicitly rejected by the domain owner.
- Append-only mutability for Party — rejected because AUSTRAC requires
  point-in-time reconstruction, not just event log replay.

**Do not re-open:**
- Risk Rating and Sanctions Screen Status are enums, not FK lookups.
- Next Review Date does not require a NOT NULL constraint — it is calculated
  and will be null at creation.
- The Financial Crime domain classification is Highly Confidential throughout.
  No override discussion needed.

**Task for next agent:**
Generate dimensional DDL for Party, Person, Company, Party Role, Contact
Address, and Address. Target: Snowflake. Apply SCD Type 2 for slowly_changing
entities. Party Identifier is the natural primary key — no surrogate needed.
