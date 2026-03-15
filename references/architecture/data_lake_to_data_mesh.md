# How to Move Beyond a Monolithic Data Lake to a Distributed Data Mesh

**By Zhamak Dehghani** **20 May 2019**

---

Many enterprises are investing in their next generation data lake, with the hope of democratizing data at scale to provide business insights and ultimately make automated intelligent decisions. Data platforms based on the data lake architecture have common failure modes that lead to unfulfilled promises at scale. To address these failure modes we need to shift from the centralized paradigm of a lake, or its predecessor data warehouse. We need to shift to a paradigm that draws from modern distributed architecture: considering domains as the first class concern, applying platform thinking to create self-serve data infrastructure, and treating data as a product.

### Table of Contents

* [The current enterprise data platform architecture](https://www.google.com/search?q=%23the-current-enterprise-data-platform-architecture)
* [Architectural failure modes](https://www.google.com/search?q=%23architectural-failure-modes)
* [Centralized and monolithic](https://www.google.com/search?q=%23centralized-and-monolithic)
* [Coupled pipeline decomposition](https://www.google.com/search?q=%23coupled-pipeline-decomposition)
* [Siloed and hyper-specialized ownership](https://www.google.com/search?q=%23siloed-and-hyper-specialized-ownership)

* [The next enterprise data platform architecture](https://www.google.com/search?q=%23the-next-enterprise-data-platform-architecture)
* [Data and distributed domain driven architecture convergence](https://www.google.com/search?q=%23data-and-distributed-domain-driven-architecture-convergence)
* [Domain oriented data decomposition and ownership](https://www.google.com/search?q=%23domain-oriented-data-decomposition-and-ownership)
* [Source oriented domain data](https://www.google.com/search?q=%23source-oriented-domain-data)
* [Consumer oriented and shared domain data](https://www.google.com/search?q=%23consumer-oriented-and-shared-domain-data)
* [Distributed pipelines as domain internal implementation](https://www.google.com/search?q=%23distributed-pipelines-as-domain-internal-implementation)

* [Data and product thinking convergence](https://www.google.com/search?q=%23data-and-product-thinking-convergence)
* [Domain data as a product](https://www.google.com/search?q=%23domain-data-as-a-product)

* [Domain data cross-functional teams](https://www.google.com/search?q=%23domain-data-cross-functional-teams)

* [Data and self-serve platform design convergence](https://www.google.com/search?q=%23data-and-self-serve-platform-design-convergence)
* [The paradigm shift towards a data mesh](https://www.google.com/search?q=%23the-paradigm-shift-towards-a-data-mesh)

---

## The current enterprise data platform architecture

It is centralized, monolithic and domain agnostic aka data lake.

Almost every client I work with is either planning or building their 3rd generation data and intelligence platform, while admitting the failures of the past generations:

* **The first generation:** proprietary enterprise data warehouse and business intelligence platforms; solutions with large price tags that have left companies with equally large amounts of technical debt.
* **The second generation:** big data ecosystem with a data lake as a silver bullet; complex big data ecosystem and long running batch jobs operated by a central team of hyper-specialized data engineers.
* **The third generation:** similar to the previous, but with a modern twist towards streaming (Kappa architecture), unifying batch and stream (Apache Beam), and cloud-managed services.

Despite these advancements, the third generation suffers from the same underlying characteristics that led to the failures of the previous generations.

## Architectural failure modes

### Centralized and monolithic

At 30,000 feet, the data platform architecture looks like a centralized piece of architecture whose goal is to:

1. **Ingest** data from all corners of the enterprise.
2. **Cleanse, enrich, and transform** source data into trustworthy data.
3. **Serve** the datasets to a variety of consumers.

> **Figure 1:** The 30,000 ft view of the monolithic data platform

While we have successfully applied domain-driven design and bounded context to operational systems, we have largely disregarded domain concepts in data platforms. We have moved toward centralized, domain-agnostic data ownership.

### Coupled pipeline decomposition

The second failure mode is related to how we decompose the architecture. It is often decomposed around mechanical functions (ingestion, preparation, aggregation, serving) rather than business domains. This leads to high coupling and slow delivery as any change requires coordination across the entire pipeline.

### Siloed and hyper-specialized ownership

The centralized platform is typically managed by a siloed team of hyper-specialized data engineers who are disconnected from the source domains and the end consumers. This creates a bottleneck for the organization's innovation agenda.

---

## The next enterprise data platform architecture

To escape the current paradigm, we need to shift towards a distributed data mesh.

> **Figure 6:** Convergence: the paradigm shift for building the next data platforms

### Data and distributed domain driven architecture convergence

#### Domain oriented data decomposition and ownership

Instead of flowing data from domains into a centrally owned data lake, domains need to host and serve their domain datasets in an easily consumable way. The architectural quantum in a domain-oriented data platform is a **domain**, not a pipeline stage.

#### Source oriented domain data

Some domains naturally align with the source, where the data originates. These datasets represent the "facts of the business."

#### Consumer oriented and shared domain data

Other domains are consumer-aligned, transforming source data into specific aggregates or insights required for end-user applications.

#### Distributed pipelines as domain internal implementation

Pipelines are no longer a central concern but an internal implementation detail of the domain that owns the data.

### Data and product thinking convergence

#### Domain data as a product

Domain teams must apply product thinking to their datasets, treating them as products and other teams as customers.

> **Figure 9:** Characteristics of domain datasets as product

A data product must be:

* **Discoverable:** Easily found via a data catalog.
* **Addressable:** Reachable through unique and stable addresses.
* **Trustworthy and truthful:** Backed by SLAs and data quality metrics.
* **Self-describing semantics and syntax:** Easy to understand without manual intervention.
* **Inter-operable:** Governed by global standards for linking datasets.
* **Secure:** Governed by global access control.

### Domain data cross-functional teams

Teams should be cross-functional, including data engineers and domain experts, working together to deliver data products.

---

## Data and self-serve platform design convergence

To prevent duplication of effort, we need a self-serve data infrastructure platform. This platform provides the tools for domain teams to build, deploy, and manage their data products without needing a central team to do it for them.

---

## The paradigm shift towards a data mesh

The data mesh is an ecosystem of data products that play nicely together. This requires a shift in language and principles:

* **Serving** over ingesting
* **Discovering and using** over extracting and loading
* **Publishing events as streams** over flowing data via centralized pipelines
* **Ecosystem of data products** over centralized data platform

Let's break down the big data monolith into a harmonized, collaborative, and distributed ecosystem of data mesh.

---

*For the full text and diagrams, visit the original article at [martinfowler.com](https://martinfowler.com/articles/data-monolith-to-mesh.html).*
