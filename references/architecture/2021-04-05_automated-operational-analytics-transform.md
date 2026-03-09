# Automated Operational to Analytics Transform

![Op2AnTitle.png](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/Op2AnTitle.8b170edb.fill-800x240.png)

The convergence of operational, reporting and analytic data is accelerating. Polyglot persistence in combination with Data Mesh concepts deliver a simpler, more accurate and semantically consistent view of the whole data landscape.

---

When we have a well defined logical model for our data products, our declarative meta-model can do more than simple schemas, API definitions and data dictionary. I guess it's polyglot modelling - building understanding into our data model which gives us direction on how to programmatically store and govern our data efficiently in multiple data persistence types.

Simply using the same data persisted in an operational store into a data warehouse database will not provide an efficient queryable interface for analytic & real-time reporting use cases. Nothing new to that but instead of building ETL/ELT (and I'm including streaming ELT), lets use our metadata to automatically create denormalised views, still in semantically consistent form to cover 80% of reporting use cases.

## Modelling

The pattern is to work recursively from the relationship owner to the relationship source for all "Things That Happen" (events) to "Things That Are".

From the data model point of view:

![OP2ANL.png](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/OP2ANL.width-800.png)

We can implement this in the stream processor (I like [Delta Lake](https://github.com/delta-io/delta) on Spark here) or as auto generated SQL code to create materialised views. Our data model nomenclature should include everything stream transformation or code generation needs to understand the relationship traversal.

Example of an event stream message:

![Nested Example.PNG](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/Nested_Example.width-800.png)

## Flatten to wide column

Denormalized, columnar data is performant for queries and storage and is rapidly replacing dimensional modelling, especially for cloud native workloads. The research done in this area shows that reducing joins is the most important factor in performance per price point for reporting and analytical workloads.

Once we have created our nested view, we can simply flatten our data, remove links and shortcut names which ends up as:

![Flatten Example.PNG](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/Flatten_Example.width-800.png)

We perform this for all 'things that happen' and automatically produce a wide column format which adheres to the canonical model and will remove most joins required in reporting use cases.

### Many to X

If the changed object owns a many to X relationship, the JSON representation will have an array. This should eventuate in multiple rows in the output wide column format. We should only apply this for the first level of the hierarchy and only for certain related objects - it's up to our nomenclature to provide this info.

## Automated Metrics

We can include hints in our logical canonical model for what aggregation dimensions are significant. If using UML, an attribute stereotype or constraint can be used and this can be used as the configuration for an aggregation engine.

This is discussed here: [Data Autonomy - BI & Analytics](./2020-07-30_data-autonomy-bi-analytics.md)

---

Hopefully, this shows the concept of programmatically transforming and aggregating our data to achieve efficient polyglot persistence based on understanding how our data works and modelling more than an entity relationship diagram.

This follows the 80/20 rule so I'm sure you can come up with other cases where this is not the best way but I hope you appreciate that we have created significant data assets for the business with very little effort.
