# Data Products — Architecture Quantum

Covers data products as the independently deployable, governed, business-owned
architecture quantum. Includes the canonical data model pattern, key mapping,
abstraction data products, and the $150M case study evidence.

## Source Material

{{INCLUDE: ../../../../../references/architecture/2024-07-11_data_products.md}}

{{INCLUDE: ../../../../../references/architecture/2024-08-07_architecting_data_autonomy.md}}

{{INCLUDE: ../../../../../references/architecture/2020-08-05_data-autonomy-case-study.md}}

## Key Concepts

- **Data Products as Architecture Quantum** — The smallest independently deployable
  unit of data architecture. Each data product is owned by a domain, governed,
  versioned, and publishable.
- **Canonical Data Model Pattern** — Each source application translates to/from
  a canonical form via abstraction data products. The canonical model is the stable
  centre; application formats change without propagating.
- **Key Mapping** — Source system identifiers are mapped to canonical enterprise
  identifiers. This enables cross-system identity resolution without requiring
  source systems to agree on a common key.
- **Abstraction Data Products** — Inbound and outbound translation layers that
  abstract each application's idiosyncratic data format into the canonical shape.
- **$150M Case Study** — Real-world evidence of Data Autonomy at enterprise scale:
  $150M savings, 3x delivery cadence, risk reduction through model-driven generation
  and canonical data products.
- **Continuous Transform and Load (CTL)** — The convergence of operational integration
  and analytics ETL into a single continuous pipeline, enabled by canonical data products.

## Relevant Tenets

- Tenet 1: Master data where change is least
- Tenet 3: Design for loose coupling
- Tenet 10: Data products are architecture quantum
- Tenet 11: Canonical models + key mapping
