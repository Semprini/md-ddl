# Data Autonomy Overview

![autonomy.jpg](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/autonomy.2e16d0ba.fill-800x240.jpg)

Data Autonomy is a holistic data strategy which is based on the rationale discussed in [Vestigial Technology](./2018-12-20_vestigial_technology.md). This is an overview of the concepts.

The purpose of Data Autonomy is to counteract increasing costs and loss of flexibility in IT as the business grows and changes. Data Autonomy limits IT complexity by providing loosely coupled, consistent, accessible, and secure information anytime, anywhere, on any device.

Data Autonomy works best in conjunction with modern IT practices like automated regression, DevOps and infrastructure as code. We must embrace change and be good at implementing small changes regularly.

#### High level rationale

The main assertion of Data Autonomy is that data should be mastered where there is least change and where change is easiest to manage.

If we are honest, our legacy line of business applications are not appropriate custodians of our data. The semantic misalignment is discussed here: [Systems of Record. Bollocks.](./2021-04-24_systems-record-bollocks.md) Often, our systems of record are inflexible, have janky data quality controls and data is not easily accessible without serious integration systems and in-depth system knowledge. Therefore, it is not best to master data in these applications.

We move from having systems of record to systems of change and systems of experience.

Data Autonomy is a strategy of making business less dependent on applications, and primarily dependent on the business' own semantics plus being good at making small, regular changes.

Segregation of data ownership from business logic ownership means application dependencies are limited and do not reduce overall IT agility over time.

The more a company knows about its customers, partners and itself, the more opportunities that are available. The catch 22 has historically been that more information requires/produces more complexity of systems and ever-increasing overhead in both managing and accessing the information.

Data Autonomy enables staged, low risk legacy transformation by gradually removing data mastery from applications and persisting in holistic data mesh. The holistic data products of the mesh are the realization of business semantics and master of all significant business data.

---

#### Data Maturity and Governance

Data is the one of the few differentiating factors between companies. Almost everything we do in business revolves around our data and it is therefore one of, if not the most important strategic asset we have.

A key rationale for Data Autonomy is that a holistic data model evolves differently to application data and business processes. Holistic data models are measured in maturity – i.e. less change over time, whereas business processes and application data is in a constant state of change to keep ahead of the competition, application upgrades and project implementation. Information can be modelled, governed and exposed as the business/industry view of data without being limited by the idiosyncrasies of back-end systems.

Data governance quite often an deals with an abstract view of information. When data is mastered in a holistic data mesh there is almost a one to one mapping of the logical and physical models.

By using a data mesh, the data policies and data quality measures which the governance group decides on can be easily realised and automatically enforced in the platforms.

---

#### Bounded Context

Each business domain has it's own holistic data model which we realize through data products forming a Data Mesh. This business domain aligned bounded context allows the different areas of the business to mature independently.

For example I recently worked at a power company and they had generation assets (power plants) and a retail business. Each has customers but the view of what a customer is, the pace of change and risk profile in each domain was very different so it was worth having independent models. This makes IT more resilient to forces like regulatory change.

Each domain needs business ownership and each owner will be part of and work with the Data Governance group and modellers to ensure appropriate information management practices.

![boundedcontextdata.png](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/boundedcontextdata.width-800.png)

*Martin Fowler - Bounded Context*

---

#### Better Uptime

In a complicated system it becomes more and more difficult to maintain a three or four 9 (99.99%) uptime. Applications may reach this uptime, but the overall uptime of the system includes all dependent applications and integrations.

A huge advantage of Data Autonomy is the reduction in chained dependencies. By having fewer dependencies each application needs only to service its own uptime requirements – not as part of a larger system (to a significant extent).

The uptime benefit is common to event driven architectures. A standard event driven pattern is 3-flow, 2-transform. This is one of the key patterns supported via Data Autonomy with the major benefit of storing the data once it's been transformed into the business view.

---

#### Implementing Data Autonomy

At the core of Data Autonomy are holistic data products which together form a "Data Mesh". The mesh delivers data for all use cases - event driven, synchronous, reporting, analytics. These holistic data systems are where the policies of data governance are enacted and the business view evolves and matures.

![BoundedContext.png](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/BoundedContext.width-800.png)

More can be found in the blog post: [Data Autonomy - Holistic Data Mesh](./2020-07-18_data-autonomy-holistic-data-mesh.md)

The Integration domain under Data Autonomy becomes a set of application abstraction layers which are responsible for subscribing to the significant business data that the application needs to run and publishing changes to any significant business data.

We must build these abstraction layers to change. Business data semantics and policy will mature based on data governance and stewardship and when it does, we will break things - this is good.

IT has moved on from the days where change had to be difficult - we now have things like microservices, CI/CD, infrastructure as code, containers, automated regression etc to enable this change. We no longer need archaic versioning strategies for internal systems - more on this here: [Stop Versioning!](./2021-03-28_stop-versioning.md)

---

#### 80/20

Data autonomy does not claim to cover all processes in a business. By covering 80% of the business processes, we have enabled and governed our most strategic asset - our data.

The rule is: If a system has created or updated 'significant business data' then it falls under the purview of data governance and must be published to the data platform.

We have therefore moved from having systems of record to systems of change and systems of experience.
