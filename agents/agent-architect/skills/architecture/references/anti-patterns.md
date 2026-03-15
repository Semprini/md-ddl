# Anti-Patterns — What Goes Wrong Without This Architecture

Covers the problems that Data Autonomy addresses: vestigial technology dependency,
versioning as false economy, the Systems of Record myth, and PoC-to-production abuse.

## Source Material

{{INCLUDE: ../../../../../references/architecture/2018-12-20_vestigial_technology.md}}

{{INCLUDE: ../../../../../references/architecture/2021-03-28_stop-versioning.md}}

{{INCLUDE: ../../../../../references/architecture/2021-04-24_systems-record-bollocks.md}}

{{INCLUDE: ../../../../../references/architecture/2021-09-23_poc-poc-poc-production.md}}

## Key Concepts

- **Vestigial Technology** — Legacy systems that persist not because they add value
  but because they have accumulated dependencies. The longer they persist, the more
  dependent the organisation becomes.
- **Versioning as False Economy** — Internal versioning strategies create the illusion
  of stability while accumulating integration debt. Small, regular change is cheaper
  than version management.
- **Systems of Record Myth** — The belief that each data element has exactly one
  authoritative source. In practice, "system of record" is often meaningless —
  data is mastered by the domain, not by the application that happened to store it.
- **PoC Abuse** — Proof of Concept projects that never transition to production,
  consuming budget and creating technical debt without delivering value.

## Relevant Tenets

- Tenet 1: Master data where change is least
- Tenet 3: Design for loose coupling
- Tenet 7: Embrace small, regular change
- Tenet 8: Ask "what does good look like?"
