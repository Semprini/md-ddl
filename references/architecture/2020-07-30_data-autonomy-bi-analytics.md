# Data Autonomy - BI & Analytics

![Big-Data-Banner.png](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/Big-Data-Banner.2e16d0ba.fill-800x240.png)

BI & analytics loves [Data Autonomy](./2019-02-17_data-autonomy-overview.md) and event driven architecture. In the operational side of Semantic Hub / Data Mesh, data is already clean and in business form. Data engineering can subscribe to all significant business object changes and metrics can be automatically calculated live. Dimensional modelling also becomes a much simpler process as canonical data is available near real time.

The data engineering and integration teams can become an active part of data governance and data stewardship. Working closely with the business domain SMEs, everyone is on the same page and reporting is simplified.

---

#### Data Warehouse / Lake

All the significant business events of relevance to each domain pass though the semantic hub / data mesh and each event of the same type is now in the same form. We can tap into this flow and stream all the events to reporting and analytic persistence engines.

ETL/ELT becomes legacy thinking for any data considered 'significant' (so has a canonical model) and the live data provides many opportunities. Because all reporting is sourced from the same foundation, the reports can be consistent, near real-time and analytics will provide business understandable insights.

Data warehousing & analytics require some different patterns. Some types of reporting (and reporting tools) work best where the underlying data is modelled as a star schema, others like a columnar normalized form or JSON documents. I prefer to leave this particular holy war to others but if feels that the next stage of evolution is virtual / logical warehouses running on top of a “[delta lake](https://github.com/delta-io/delta)”.

We can programmatically [convert the canonical schema to a columnar form](./2021-04-05_automated-operational-analytics-transform.md).

It's very easy to stream canonical JSON into NoSQL and flatten into Parquet for filesystem based persistence. I commonly use NoSQL persistence for audit & history to enable callers to request any object (modelled as 'auditable') as it was at any time or revision.

This deprecates the raw layer of the data lake as a source for curated / canonical data. The raw layer is only used for reconciliation and some data science investigation. Canonical data is streamed directly into the curated layer and it semantically matches the operational domains.

For me, the key for long term IT agility is to evolve this analytics side of persistence just as we mature the canonical model for operational persistence and [upgrade as we go](./2021-03-28_stop-versioning.md) - small changes regularly, so we don’t have to account for multiple schemas during query and have different results produced by different users. I.e. holistic management of our data assets through the entire data lifecycle.

A huge benefit to enterprise data quality is that by evolving the complete canonical layer including operational & analytic persistence, the maintenance becomes independent on project work. I.e. Data Autonomy.

---

#### Real Time Metrics

Events combined with autonomous data allow us to calculate many meaningful metrics live. Part of defining a domain model is to identify aggregation keys and dimensions. In the past I have created micro-services charged with listening to events and aggregating live across multiple configured dimensions. A better set of technologies here is either Kafka or the Spark analytics engine with [Delta Lake](https://github.com/delta-io/delta) storage layer but the principle is the same.

The resulting metrics become significant business objects which are POSTed or published back to the data platform or directly to BI persistence.

![]()

An example of this was when I was working in a nation-wide retail organisation who is naturally obsessed with the Sale object. The micro-service was able to aggregate live sales per day, per store, per customer and per product. The metrics created were POSTed back to the semantic hub which streamed to BI data stores and augmented then queried by a time series visualisation tool. Notably the same metrics were also subscribed to by the online team so were available for the corporate customer web interface.
