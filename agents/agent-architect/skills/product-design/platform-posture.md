# Platform Posture — Architecture Guidance

How an organisation relates data products to platforms shapes which product classes
apply, what artifacts get generated, and what infrastructure is assumed. Establish the
platform posture before designing data products (AGENT.md discovery step 3). The
`platform:` metadata block that records the decision is defined in
[Section 9 — Data Products](../../../../md-ddl-specification/9-Data-Products.md#platform-posture).

MD-DDL describes three postures:

## Single-Platform

All data products are self-contained on one platform (e.g., Snowflake, Databricks, BigQuery). Source ingestion, transformation, canonical storage, and consumer access all happen within the same platform.

- **Effect on classes:** All three classes (source-aligned, domain-aligned, consumer-aligned) are typically recognised as data products
- **Effect on artifacts:** Generation targets one platform; `schema_type` maps directly to platform-native constructs
- **Effect on infrastructure:** Minimal integration complexity; the platform provides compute, storage, and access control
- **Typical pattern:** Source-aligned = raw/staging schemas; domain-aligned = curated schemas; consumer-aligned = materialized views or denormalized tables

## Polyglot

Different product classes leverage different platforms and technologies depending on the data's lifecycle stage and access pattern. The organisation accepts that data products span infrastructure boundaries.

- **Effect on classes:** Each class may target a different platform stack:
  - **Source-aligned** — CDC, streaming (Kafka, Flink), operational data stores, event buses
  - **Domain-aligned / foundational** — polyglot persistence (relational + document + graph), analytical and operational interfaces, potentially spanning OLTP and OLAP stores
  - **Consumer-aligned** — purpose-built for the consumer's query engine (data warehouse, API layer, search index, dashboard cache)
- **Effect on artifacts:** Generation may target multiple platforms per domain; `schema_type` maps to platform-appropriate constructs for each product
- **Effect on infrastructure:** Higher integration complexity; requires cross-platform lineage tracking, consistent governance enforcement, and potentially different access control mechanisms per platform

## Selective Scope

The organisation does not consider all classes as "data products." Some layers are treated as infrastructure or engineering concerns rather than governed, published products.

- **Common pattern:** Source-aligned feeds are infrastructure (CDC pipelines, staging areas) managed by data engineering — not declared as data products. Only domain-aligned and consumer-aligned outputs are governed as products.
- **Alternative pattern:** Only consumer-aligned outputs are products. Domain-aligned canonical models are internal reference architectures, not published products.
- **Effect on MD-DDL:** Product classes that fall outside the org's product scope are still valid as infrastructure concepts but are not declared in `products/`. Source declarations and transforms still exist in `sources/` regardless of whether source-aligned products are declared.

## Recording the Decision

Platform posture is typically an organisation-wide decision, but is declared per domain because different parts of the organisation may be at different stages of platform strategy. When all domains share the same posture, use consistent values across domain files. If the posture is not yet recorded in the domain's `platform:` metadata block, propose adding it once the user has answered the discovery questions.
