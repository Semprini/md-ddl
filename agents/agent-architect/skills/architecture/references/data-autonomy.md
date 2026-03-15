# Data Autonomy — Core Architecture

Covers the core Data Autonomy architectural philosophy: semantic hubs, domain-aligned
bounded contexts, polyglot persistence, event-driven and RESTful integration patterns,
and the BI/analytics layer.

## Source Material

{{INCLUDE: ../../../../../references/architecture/2019-02-17_data-autonomy-overview.md}}

{{INCLUDE: ../../../../../references/architecture/2020-07-18_data-autonomy-holistic-data-mesh.md}}

{{INCLUDE: ../../../../../references/architecture/2020-07-19_data-autonomy-resource-oriented-event-driven.md}}

{{INCLUDE: ../../../../../references/architecture/2020-07-30_data-autonomy-bi-analytics.md}}

## Key Concepts

- **Semantic Hub** — The canonical data store at the centre of each domain's bounded
  context. Applications connect via abstraction layers, not directly.
- **Domain Gateway** — The controlled interface between bounded contexts, enabling
  cross-domain data flow without direct coupling.
- **Application Abstraction Layer** — Semantic and protocol translation between each
  application and the semantic hub.
- **Polyglot Persistence** — The same canonical data stored in multiple forms
  (relational, event stream, document, graph) for different workload patterns.
- **Resource-Oriented + Event-Driven** — RESTful resources and domain events as
  semantically aligned views of the same business data.

## Relevant Tenets

- Tenet 1: Master data where change is least
- Tenet 2: Separate data from logic ownership
- Tenet 3: Design for loose coupling
- Tenet 6: Use polyglot persistence
- Tenet 12: Event-driven = real-time semantics
