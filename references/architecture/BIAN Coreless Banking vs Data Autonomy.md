# BIAN Coreless Banking vs. Data Autonomy: A Discussion

## What BIAN Coreless Banking Actually Is

Coreless banking is the delivery of banking services that are not dependent on traditional core systems — a new way to build a digital customer journey from pre-defined, modular business functions. The BIAN framework provides the standardisation layer that makes this viable: a common, semantic language to connect, compose, and reuse modular business functions, with associated APIs defined to this standard, alleviating the issues of brittle integration between data streams, services, and monolithic applications.

Its evolution is telling: Coreless Banking 2.0 included canonical service designs such as semantic APIs and underlying data schema, allowing banks to modularize, standardize and develop new services more quickly in a best-of-breed environment. By 3.0, it adds cross-bank customer consent and data portability. By 4.0, AI-driven personalisation and churn prediction.

The architectural philosophy is explicitly decomposition: Coreless banking involves a shift away from monolithic and static technology systems to ones that are modular and composable, operating in four layers — banking-specific capabilities, cross-industry capabilities, orchestration, and customer experience.

---

## Where the Two Approaches Directly Converge

**1. The core diagnosis is identical**

Both Data Autonomy and BIAN start from the same place: applications are bad custodians of data. The Data Autonomy body of work argues that legacy line-of-business applications have "semantic misalignment" and are "not appropriate custodians of our data." Often, applications and services have been integrated into core banking engines over decades — BIAN's whole raison d'être is undoing this.

The prescription is also structurally the same: segregation of data ownership from business logic ownership means application dependencies are limited and do not reduce overall IT agility over time. BIAN achieves this at the service/API level; Data Autonomy achieves it at the data ownership level. They're attacking the same monster from different angles.

**2. BIAN is the canonical model banking has been waiting for**

This is perhaps the most important synthesis point. The Data Autonomy architecture requires a canonical data model at its centre — a business-semantic, domain-aligned representation of data that sits above any particular application's idiosyncrasies. Building this from scratch inside a bank is enormously expensive and politically fraught.

BIAN has done much of that work already. BIAN's Portal is home to 250 APIs and more than 5,000 service domains, each with defined semantic schemas. The Data Autonomy body of work explicitly argues that organisations "should be using an industry standard conceptual model to build upon all the hard work done in the industry." BIAN IS that model for banking. A bank implementing Data Autonomy should be targeting BIAN's service domain schemas as the canonical shape of their data products, rather than inventing their own. This dramatically reduces the modelling cost and produces data products that are vendor-interoperable by design.

**3. Both demand bounded contexts with domain ownership**

Each business domain has its own holistic data model which we realise through data products forming a Data Mesh. This business domain aligned bounded context allows the different areas of the business to mature independently. BIAN's service domains are the industry-standard articulation of exactly these bounded contexts for banking. "Current Account," "Customer Offer," "Credit Risk," "Payments" — these are BIAN service domains and they are also exactly the bounded contexts Data Autonomy would expect a bank to build their data products around.

**4. Legacy transformation as the strategic engine**

Both frameworks frame legacy decomposition not as a big-bang replacement but as a continuous, risk-managed process. Data products provide staged, low risk legacy transformation. Each existing "system of change" publishes the data it creates and subscribes to the data it needs. The initial Coreless Banking concept aimed to promote a more efficient and effective approach to modernising banking software... this will solve the perpetual challenges presented by legacy core infrastructure. The mechanism differs — BIAN uses standardised APIs to decouple services, Data Autonomy uses abstraction data products to decouple data — but both enable the same incremental escape from monolithic lock-in.

---

## Where They Diverge and Expose Gaps in Each Other

**1. BIAN is a service architecture; Semprini is a data architecture**

This is the sharpest tension. BIAN's primary frame is: *standardise the service interfaces*. Data Autonomy's primary frame is: *master data independently of applications*. These are not the same thing, and BIAN's Coreless framework does not fully resolve the data ownership question. A bank can implement 250 BIAN-compliant APIs and still have every service owning its own data silo, with no canonical master, no convergence of operational and analytic pipelines, no data marketplace.

BIAN adds data schemas in version 2.0+, which moves it closer, but the schema definitions in BIAN are designed around API message models — what data is passed in a service call — not around the data product ownership model Semprini describes. There's a gap between "this is the schema for a payment message" and "here is the bounded, governed, business-owned canonical master of all payment data."

**2. The abstraction data product pattern is missing from BIAN**

Each application gets a translator — in and out. This is also known as application abstraction as each translator is responsible for abstracting all the application shenanigans via protocol and semantic transformation. This is Data Autonomy's key implementation mechanism — the pattern that actually makes the canonical model work in a world of heterogeneous legacy systems.

BIAN tells you *what* the canonical shape should be. Data Autonomy tells you *how* to build the translation layer from your legacy Oracle Flexcube or Temenos core to that canonical shape, with lineage, key mapping, CTL pipelines, and governance controls baked in. Banks implementing BIAN without this pattern will end up with well-specified APIs that are still point-to-point integrated underneath.

**3. Operational/analytical convergence is a blind spot in BIAN**

These master data products use polyglot persistence to store the data for efficient operational and analytic queries and streams... we've converged operational integration with old school ETLs to deliver Continuous Transform and Load (CTL), so not only do we save on legacy transformation, we reduce the size of teams engineering data.

BIAN is almost entirely transactional/operational in orientation. The analytical dimension — data lakes, BI, ML/AI feature stores, real-time aggregation — isn't addressed. This matters enormously in a bank, where the same customer data needs to serve both real-time fraud detection and monthly regulatory reporting. Data Autonomy's CTL pattern, where the canonical data product serves all use cases from a single canonical store, is not something BIAN has an answer to. Coreless Banking 4.0 gestures at AI and ML but doesn't provide an architecture for how the data gets there.

**4. The versioning tension**

The broader Data Autonomy body of work argues against internal versioning strategies — continuous change is better than version management. But BIAN releases new versions of its framework on a regular basis, and banks need to stay in sync. For inter-institutional, inter-vendor standards, versioning is unavoidable and appropriate. But there's a real risk that banks treat BIAN version compliance as justification for the same rigid governance processes that Data Autonomy is trying to dismantle internally. The discipline Data Autonomy advocates — being good at small, regular changes — actually makes BIAN version upgrades *cheaper*, because the canonical data product abstraction layer means changes propagate cleanly rather than cascading through brittle point-to-point integrations.

**5. Open Banking and the Data Autonomy marketplace**

Coreless Banking 3.0 placed the customer at the heart of banks' operations by providing the ability to obtain customer consent to retrieve their banking data held with another bank. This is essentially an open banking / data portability play. Data Autonomy's data marketplace concept — as we deploy our data products, we publish the endpoints and structure to the data marketplace — because we have modelled and mastered our data including sensitivity and privacy, we can provide the right data, at the right time, securely and with appropriate authorisation and oversight — is a natural architectural foundation for exactly this. A well-implemented Data Autonomy landscape gives you consent-driven cross-bank data sharing almost for free, because the governance, access controls, and discoverability infrastructure is already in place. BIAN's 3.0 concept needs this as the delivery mechanism and doesn't currently specify it.

---

## The Synthesis

The most productive framing is that these are complementary layers of the same transformation, not competing approaches:

**BIAN provides the "what"** — the industry-standard canonical vocabulary, service definitions, and API schemas for banking. It defines the shape that your data products should conform to, ensures vendor interoperability, and reduces the modelling cost of building your own canonical model.

**Data Autonomy provides the "how"** — the architectural patterns (abstraction data products, key mapping, CTL, data mesh governance, the marketplace) to actually implement canonical data ownership, unify operational and analytical pipelines, enable legacy transformation, and make data a genuinely governed business asset.

A bank that implements BIAN Coreless Banking without Data Autonomy principles will have standard APIs over still-siloed data. They'll have solved interoperability but not data governance or analytical convergence. A bank that implements Data Autonomy without BIAN will spend enormous effort inventing canonical schemas that BIAN has already defined, and will face harder vendor integration negotiations.

Together, they resolve something neither fully addresses alone: a bank where domain-owned data products conform to BIAN's industry-standard schemas, are served via BIAN-compliant APIs, are governed and mastered independently of any application, converge operational and analytical use cases through CTL pipelines, and expose a consent-aware marketplace — that's a genuinely modern, sovereign bank. The data is no longer held hostage by the core system, and neither is the bank.
