# BIAN Coreless Banking and Data Autonomy: A Discussion

---

## What BIAN Coreless Banking Actually Is

Coreless banking is the delivery of banking services that are not dependent on traditional core systems — a new way to build a digital customer journey from pre-defined, modular business functions.[^1] The BIAN framework provides the standardisation layer that makes this viable: a common, semantic language to connect, compose, and reuse modular business functions, with associated APIs defined to this standard, alleviating the issues of brittle integration between data streams, services, and monolithic applications.[^1]

Its evolution is telling: Coreless Banking 2.0 included canonical service designs such as semantic APIs and underlying data schema, allowing banks to modularize, standardize and develop new services more quickly in a best-of-breed environment.[^2] By version 3.0, it adds cross-bank customer consent and data portability. By 4.0, AI-driven personalisation and churn prediction.

The architectural philosophy is explicitly decomposition: coreless banking involves a shift away from monolithic and static technology systems to ones that are modular and composable,[^3] operating in four layers — banking-specific capabilities, cross-industry capabilities, orchestration, and customer experience.

---

## Where the Two Approaches Directly Converge

### 1. The Core Diagnosis Is Identical

Both the Data Autonomy body of work and BIAN start from the same place: applications are bad custodians of data. Data Autonomy argues that legacy line-of-business applications have "semantic misalignment" and are not appropriate custodians of an organisation's data.[^4] BIAN's whole raison d'être is undoing precisely this — often, applications and services have been integrated into core banking engines over decades.[^1]

The prescription is also structurally the same: segregation of data ownership from business logic ownership means application dependencies are limited and do not reduce overall IT agility over time.[^4] BIAN achieves this at the service/API level; Data Autonomy achieves it at the data ownership level. They are attacking the same problem from complementary angles.

### 2. BIAN Is the Canonical Model Banking Has Been Waiting For

This is perhaps the most important synthesis point. The Data Autonomy architecture requires a canonical data model at its centre — a business-semantic, domain-aligned representation of data that sits above any particular application's idiosyncrasies. Building this from scratch inside a bank is enormously expensive and politically fraught.

BIAN has done much of that work already. Its portal is home to 250 APIs and more than 5,000 service domains,[^5] each with defined semantic schemas. Data Autonomy explicitly notes that organisations should be using an industry-standard conceptual model to build upon all the hard work done in the industry.[^6] BIAN *is* that model for banking. A bank implementing Data Autonomy should be targeting BIAN's service domain schemas as the canonical shape of their data products, rather than inventing their own — dramatically reducing modelling cost and producing data products that are vendor-interoperable by design.

### 3. Both Demand Bounded Contexts with Domain Ownership

Each business domain has its own holistic data model, realised through data products forming a Data Mesh. This business domain-aligned bounded context allows the different areas of the business to mature independently.[^4] BIAN's service domains are the industry-standard articulation of exactly these bounded contexts for banking. "Current Account," "Customer Offer," "Credit Risk," "Payments" — these are BIAN service domains, and they are also precisely the bounded contexts Data Autonomy would expect a bank to build its data products around.

### 4. Legacy Transformation as the Strategic Engine

Both frameworks frame legacy decomposition not as a big-bang replacement but as a continuous, risk-managed process. Data Autonomy provides staged, low-risk legacy transformation, where each existing system of change publishes the data it creates and subscribes to the data it needs.[^7] BIAN similarly aims to solve the perpetual challenges presented by legacy core infrastructure.[^2] The mechanism differs — BIAN uses standardised APIs to decouple services, Data Autonomy uses abstraction data products to decouple data — but both enable the same incremental escape from monolithic lock-in.

---

## Where They Diverge and Expose Gaps in Each Other

### 1. BIAN Is a Service Architecture; Data Autonomy Is a Data Architecture

This is the sharpest tension. BIAN's primary frame is: *standardise the service interfaces*. Data Autonomy's primary frame is: *master data independently of applications*. These are not the same thing, and BIAN's Coreless framework does not fully resolve the data ownership question. A bank can implement 250 BIAN-compliant APIs and still have every service owning its own data silo, with no canonical master, no convergence of operational and analytic pipelines, no data marketplace.

BIAN adds data schemas from version 2.0 onwards, which moves it closer, but those schema definitions are designed around API message models — what data is passed in a service call — not around the data product ownership model Data Autonomy describes. There is a gap between "this is the schema for a payment message" and "here is the bounded, governed, business-owned canonical master of all payment data."

### 2. The Abstraction Data Product Pattern Is Missing from BIAN

Data Autonomy's key implementation mechanism is that each application gets a translator — in and out — responsible for abstracting all the application-specific behaviour via protocol and semantic transformation.[^8] This is what actually makes the canonical model work in a world of heterogeneous legacy systems.

BIAN tells you *what* the canonical shape should be. Data Autonomy tells you *how* to build the translation layer from a legacy core banking system to that canonical shape, with lineage, key mapping, CTL pipelines, and governance controls baked in. Banks implementing BIAN without this pattern will end up with well-specified APIs that are still point-to-point integrated underneath.

### 3. Operational/Analytical Convergence Is a Blind Spot in BIAN

The Data Autonomy approach uses polyglot persistence to store data for efficient operational and analytic queries and streams, converging operational integration with ETL to deliver Continuous Transform and Load (CTL) — so that legacy transformation savings are compounded by a reduction in the size of teams engineering data.[^7]

BIAN is almost entirely transactional and operational in orientation. The analytical dimension — data lakes, BI, ML/AI feature stores, real-time aggregation — is not addressed. This matters enormously in a bank, where the same customer data needs to serve both real-time fraud detection and monthly regulatory reporting. Coreless Banking 4.0 gestures at AI and ML but does not provide an architecture for how the data gets there. The CTL pattern, where the canonical data product serves all use cases from a single canonical store, is something BIAN currently has no equivalent for.

### 4. The Versioning Tension

Data Autonomy's broader thinking argues against internal versioning strategies — continuous change is preferable to version management. But BIAN releases new versions of its framework on a regular basis,[^9] and banks are expected to stay in sync. For inter-institutional, inter-vendor standards, versioning is unavoidable and appropriate. The risk is that banks treat BIAN version compliance as justification for the same rigid governance processes that Data Autonomy is trying to dismantle internally. Paradoxically, the discipline Data Autonomy advocates — being good at small, regular changes — actually makes BIAN version upgrades *cheaper*, because the abstraction layer means changes propagate cleanly rather than cascading through brittle integrations.

### 5. Open Banking and the Data Autonomy Marketplace

Coreless Banking 3.0 places the customer at the heart of operations by providing the ability to obtain customer consent to retrieve banking data held with another institution.[^2] This is essentially an open banking and data portability play.

Data Autonomy's data marketplace — where deployed data products publish their endpoints and structure, and because data has been modelled and mastered including sensitivity and privacy, the right data can be provided at the right time, securely and with appropriate authorisation[^7] — is a natural architectural foundation for exactly this capability. A well-implemented Data Autonomy landscape gives you consent-driven cross-bank data sharing almost for free, because the governance, access controls, and discoverability infrastructure are already in place. BIAN's 3.0 concept needs this as the delivery mechanism and does not currently specify it.

---

## The Synthesis

The most productive framing is that these are complementary layers of the same transformation, not competing approaches.

**BIAN provides the "what"** — the industry-standard canonical vocabulary, service definitions, and API schemas for banking. It defines the shape that data products should conform to, ensures vendor interoperability, and significantly reduces the modelling cost of building a canonical model from scratch.

**Data Autonomy provides the "how"** — the architectural patterns (abstraction data products, key mapping, CTL, data mesh governance, the marketplace) to actually implement canonical data ownership, unify operational and analytical pipelines, enable legacy transformation, and make data a genuinely governed business asset.

A bank that implements BIAN Coreless Banking without Data Autonomy principles will have standard APIs over still-siloed data. They will have solved interoperability but not data governance or analytical convergence. A bank that implements Data Autonomy without BIAN will spend enormous effort inventing canonical schemas that BIAN has already defined, and will face harder vendor integration negotiations.

Together, they resolve something neither fully addresses alone: a bank where domain-owned data products conform to BIAN's industry-standard schemas, are served via BIAN-compliant APIs, are governed and mastered independently of any application, converge operational and analytical use cases through CTL pipelines, and expose a consent-aware marketplace. The data is no longer held hostage by the core system — and neither is the bank.

---

## References

[^1]: Red Hat, *Build a foundation for coreless banking with Red Hat OpenShift*. <https://www.redhat.com/en/resources/build-digital-foundation-coreless-banking-overview>

[^2]: BIAN, *Coreless Banking*. <https://bian.org/deliverables/coreless-banking/>

[^3]: Thoughtworks, *How BIAN can help drive coreless banking and improve innovation in the industry*. <https://www.thoughtworks.com/insights/blog/platforms/bian-coreless-banking>

[^4]: semprini.me, *Data Autonomy Overview* (2019). <https://www.semprini.me/2019/02/17/data-autonomy-overview/>

[^5]: BIAN, *BIAN Deliverables*. <https://bian.org/>

[^6]: semprini.me, *Data Products: Architecting Data Autonomy* (2024). <https://www.semprini.me/2024/08/07/architecting_data_autonomy/>

[^7]: semprini.me, *Data Products: Save $150 million, Reduce risk, Increase speed* (2024). <https://www.semprini.me/2024/07/11/data_products/>

[^8]: semprini.me, *Data Products: Architecting Data Autonomy* (2024). <https://www.semprini.me/2024/08/07/architecting_data_autonomy/>

[^9]: BusinessToday, *BIAN: a path to banking interoperability* (2023). <https://www.businesstoday.in/opinion/columns/story/bian-a-path-to-banking-interoperability-393481-2023-08-09>
