# Data Products: Save $150 million, Reduce risk, Increase speed

![Data Products Header](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/Data_Products_Header.2e16d0ba.fill-800x240.png)

Sounds like I'm selling a silver bullet doesn't it? Actually no. What I'm selling is a butt-load of hard work, arguments and pain. And I'm trying to do this before vendors subvert the meaning of the Data Product and Data Mesh terms to the point where it becomes more meaningless buzzword bullshit.

Firstly, a business friendly definition of data product: A data asset designed for good user experience and trust, accessed via self-serve. It has a business owner who is accountable for its quality and reliability. Simple eh? As Blackadder says, "It's not what you've got, it's where you stick it."

This will be a blog in a couple of parts. In the first blog, I'll prove the statements in the title and in the next part I'll get into the details of the architecture and implementation. This will provide a blueprint on moving an enterprise laden with legacy and technical debt to a lean, keen, data driven machine.

---

## Save $150 Million

Is this big number just plucked out of the architecture ivory tower random number generator? I'll leave that decision in your hands dear reader. However, I think it's a pretty simple, traceable and logical proof and the number is conservative as this is just the direct saving. There's three parts to these savings.

### Legacy Transformation

In the intro I mention that data products shine in organisations with a large legacy footprint. A big chunk of the $150 million cost saving comes from legacy transformation and specifically the data migration/assurance/reconciliation budget. I've been involved in 2 legacy transformations - a bank and a telco, one cost, and one was forecast to cost close to a billion dollars overall. In each case, and looking at similar cases around the world, data migration was 20 - 30% of the total budget.

"But Semprini, you illuminating eminence of information, your not suggesting a big bang are you?" you ask. Indeed not, dear reader, I don't even know you... We didn't change from doing big bang transforms to iterative transforms because they're cheaper, we did it because iterative is lower risk. As you will see data products provide staged, low risk legacy transformation.

"How do data products remove a large part of the data migration budget?" You ask, interest piqued. Well, random voice in my head, key here is the concept that data products become the "system of record", "authoritative source", "source of truth", "master" etc. Why? Because data products abstract system specific semantics into canonical business constructs. Each existing "system of change" publishes the data it creates and subscribes to the data it needs - I'll discuss the pattern which enables this in the next blog, however, in this model we do the load assurance as a standard part of the "Continuous Transform and Load" (CTL). This is true loose coupling - we have decoupled our data from our business logic so when we want to move off a legacy system, responsible for some business processes & logic, we have already done the data migration work before we start.

***Data products are the engine for legacy transformation.***

### Convergence of Operational and Analytic Pipelines

This is only the start of savings. These "Master" data products use polyglot persistence to store the data for efficient operational and analytic queries & streams. This is part of a product mindset - thinking about the data, it's consumers and creating our product to effectively serve those uses. We also source the data in near real-time as we do in standard event driven architecture. I.e. we've converged operational integration with old school ETLs to deliver Continuous Transform and Load (CTL), so not only do we save on legacy transformation, we reduce the size of teams engineering data. Broadcom reduced their BI team size by 50% by making the data standardised and available by default.

### Billing Systems

The next major thing that data products can remove is your billing system - or at least reduce it down to a few simple micro-services. "Bold claim Semprini, I hope you can back that up?" I hear. I believe I can dear reader.

I'm not talking about rating engines or invoicing platforms here, just billing. Having been an Oracle billing architect and writing 2 bespoke billing systems (telco and energy), each time when I look under the hood, billing is 90% aggregation. Events roll into items per product, per period. Items roll into accounts per period. As we have sourced the rated events, charges and payments in near real-time into our data products for each event, we add the totals to the correct item aggregation buckets. To drive this aggregation, one of the features we add to our master data products is a configurable aggregation engine for 1, 2, or 3 dimensions of aggregation.

This leaves us with micro-services for bill-time discounting, late arriving usage, pro-ration, re-rating. It is actually that simple, if we have a good bounded context for billing.

Yes, this violates the ubiquitous "buy for commodity, build for competitive advantage" principle. These principles should not trump it being massively cheaper with huge utility. This also further converges the operational side with the analytic side as the real-time aggregation engine is massively reusable for ML/AI flow triggers and metrics.

Rating is a bit more complex and where a lot of idiosyncrasies live, but with data products come a proficiency with pipeline processing, audit, and reconciliation, plus our product configurations are easily available as data products so this should be evaluated against the cost of off-the-shelf rating engines too.

---

## Reduce Risk

Culture and operating model changes of data products significantly reduce risk. This is one of the strengths of the Data Mesh model - business has ownership and accountability for the data products. There's lots of info on the Data Mesh ownership model online for you, I'll not do it justice in a small section of a blog - have at it! my intrepid data technologist!

There must be a culture change in technical and business teams. For technology, this involves how we on-board and evolve our application landscape. We include on-boarding significant data produced by the application in the implementation of each application, thus all significant data is available, governed and in canonical form by default.

"But Semprini, what about [YAGNI](https://en.wikipedia.org/wiki/You_aren't_gonna_need_it)?" I hear. This is why I say "significant" data. We should be using an industry standard conceptual model to build upon all the hard work done in the industry. We can use this model to identify what data we should include in the data models by default as we create the logical model. Other attributes and objects are easy to include once we have the application abstraction in-place - data products are designed to change as our understanding of our data evolves and the data product templates should include a kit-bag of tools for on-boarding significant data as it changes in our source systems.

The on-boarding tools include data lineage, audit and data quality enforcement. We can automate this by modelling our data up-front - part of a shift compliance left ethos. We move to a declarative approach by integrating our model with governance, and then use the power of our governance tool scanners to validate that what we declared is what we delivered.

The master data products include a policy enforcement point where we can decide on authorization, quality and error handling. Most times we can hold our data when there are problems so the blast radius of errors does not blow out. We apply data fixes to our master data products which then populate the correct data to all systems needing it.

***Data Governance stops being the ambulance at the bottom of the cliff and starts enforcing guardrails at the top.***

Digital transformation is risky for our data landscape if not done well. See [increasing-odds-of-success-in-digital-transformation](https://www.bcg.com/publications/2020/increasing-odds-of-success-in-digital-transformation). We need to be wary of the data swamps caused by a lift and shift of legacy warehouses and sources: [drowning-in-a-data-lake-gartner-analyst-offers-a-life-preserver](https://www.datanami.com/2021/05/07/drowning-in-a-data-lake-gartner-analyst-offers-a-life-preserver/). We start thinking about our data as an asset by having a product lens and implementing the culture change to on-board as a standard part of our application life-cycle.

---

## Increase Speed

It would be easy for us to build bespoke data products, turning them into pets rather than cattle. A better approach is to standardize and limit the types of data products we support, have opinionated and templated deployment pipelines and we can therefore use data products as a "unit of work" for all data movement. This is "pit of success" thinking where we actively make the best thing to do also the easiest & fastest.

The operational model of on-boarding data to data products as our application ecosystem changes not only provides greater governance but also greater cadence of change. [Oracle talks about](https://www.oracle.com/a/ocom/docs/datamesh-ebook.pdf) "10x faster innovation cycles, shifting away from batch ETL (eliminate batch windows), to continuous transformation and loading (CTL) via streaming ingest". Feels like one of those "in lab conditions" statements that vendors use, and practically I have seen a 3x improvement in change cadence.

A huge improvement for the whole organisation is created by the discoverability and accessibility of our data. As we deploy our data products, we publish the endpoints and structure to the data marketplace. Because we have modelled and mastered our data including sensitivity & privacy, we can provide the right data, at the right time, securely and with appropriate authorization and oversight.

There are some great examples now of these claims being realised:

- **LinkedIn** implemented a [Kafka and Flink based real-time processing architecture](https://www.confluent.io/blog/event-streaming-platform-1/) for both operational and analytical data. Data is transformed and available within "milliseconds" which provides great customer experience as well as trustable, discoverable, consumable data - in fact, all the ibbles.
- **Starbucks** delivered an expected 12 Month Project in 10 weeks by standardisation of data engineering.
- **Wells Fargo** combined operational data events with analytics and data lakes to [simplify the data architecture](https://medium.com/@kshi/data-transformation-of-wells-fargo-en-f025843f5e2d). They reduced the number of ‘hops’ that the data must take prior to being prepared for analytics.
- **Netflix** use the distributed architecture of data mesh to perform [real-time migration to new platforms with no downtime](https://netflixtechblog.com/netflix-billing-migration-to-aws-part-iii-7d94ab9d1f59?gi=2a0f181d73d5).

---

## Hard Work

Data products done well are a beautiful thing. It's the necessary culture change, Conway's Law and buy-in from the exec which is the hard part.

There's a catch-22 here. To get buy-in we need to prove data products but to prove data products we need buy-in. If we don't have business buy-in, and data products become just a technology driven thing, we will fail. There are so many holy wars fought over data technologies, and if we fail to align on a small set of technologies, we will fail.

My approach to this catch-22 has multiple threads. Firstly, I always wear my agenda on my sleeve with all stakeholders. I provide a north star in the strategy, reference architecture and roadmap. An organisation can only implement a certain amount of change in one go, so sympathetic treatment of people, process and technology is vital while we agitate towards the north star. Lastly, I use integration patterns to form "proto data products" - I'll cover this in the next blog but this is a powerful extension to loose coupling integration.

Data products are not [faster horses](https://hbr.org/2011/08/henry-ford-never-said-the-fast). The desperate need before cars was to reduce the horse manure problem, but iterative, "good enough" manure solutions would have simply left us drowning in less horse shit. Like the car assembly line, a data product assembly line can invalidate the problems (legacy systems data lock in, data swamps, vendor lock-in, data debt, governance, security and accessibility issues) through opinionated pipelines, "product thinking" and standardisation.
