# Data Autonomy - Holistic Data Mesh

![data.JPG](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/data.2e16d0ba.fill-800x240_wCeqgF5.jpg)

Standard event driven integration practice is to take data from a system, transform into a middle model and then transform to each destination. [Data Autonomy](./2019-02-17_data-autonomy-overview.md) simply says that while we have the data in the middle form, lets save it.

Each business domain must be free to evolve and mature independently as the view of significant business objects evolves. The data governance group with data stewards and SMEs should be responsible for producing domain aligned data product definitions which are then realized into data products. The features of these data products should cover interfaces and persistence for both operational and analytical data.

---

#### Data Mesh

True loose coupling comes when we start actually treating data as a business asset by creating a set of canonical data products designed for our business domains.

By including polyglot persistence for operational, reporting, analytics and machine learning workloads in our data products we form a "Data Mesh" which is an upcoming buzzword and all data architects should start using to sound cool in meetings.

I like to think of each domain as a "Semantic Hub" I.e. A realization of a domains semantics and responsible for interfaces, storage and implementing data governance policies.

To achieve eventual consistency, and support both events and real time queries, we must persist the data as it passes through the Hub in its canonical form.

![BoundedContext.png](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/BoundedContext.width-800.png)

The domain forms are exceptionally important. Please see Martin Fowlers discussion on [Bounded Context](https://www.martinfowler.com/bliki/BoundedContext.html). The Data Mesh has all the important business events passing through it, from and to a wide variety of systems but each event of the same type is now in the domain form, irrespective of its issuing or receiving system. It is not a neutral form; it is a chosen common form for that business domain.

The decoupling of systems established using a data mesh enables significant flexibility:

- A business domain can be created or expanded by replication or transfer of existing systems in other domains.
- A domain can reduce its role by transferring systems to other domains, or even be shut down completely.
- Domains can merge or split to suit business aspirations.
- New systems can be assimilated quickly by reusing existing integration deliverables.
- Systems only need to be retained when they provide business benefit and not because they are so tightly coupled with other systems they cannot be decommissioned.
- Legacy systems can continue to support business without them inhibiting other changes.
- Business owners are enabled to take decisions based on the system support they want themselves and not what others want from them.

---

#### Application Abstraction

The Data Mesh is concerned with data in business form. It has access via API, streaming and analytic interfaces with Attribute Based Access Control (ABAC) based on data classification. Most applications don't natively talk in your business form or streaming protocols so we must do semantic and protocol transformation. The middleware responsible for this is an "application abstraction". Use whatever tech you like from Microservice to Mulesoft to Kafka filestream - as long as the application idiosyncrasies are abstracted and the semantic transform is agile and part of the automated regression testing with the application stubbed.

![SH Integration.png](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/SH_Integration1.width-800.png)

Automated regression tests can be created by the data modelling process and we can examine the impact of schema changes via continuous delivery and containerisation. A good resource for this is CDAF: <http://cdaf.io/about>

Our data is governed and managed by the Data Mesh and we are agile enough to upgrade as we go. See [Stop Versioning!](./2021-03-28_stop-versioning.md) for more info.

---

#### Eventual Consistency / Enrichment

As significant business objects change in back-end systems, events are populated to the Data Mesh. A significant form of tight coupling comes when we put destination system requirements into a source systems abstraction and we try to enrich close to source. So instead, for loose coupling, each application need only publish the parts of canonical objects they are responsible for as they change (or as close to real-time as the app allows). The Data Mesh will accumulate the changes with previous changes and other systems changes and publish what it's got, when it gets it.

There will not be a complete 1 to 1 mapping to the canonical model from each technical change so subscribers can choose not receive a business object until other processes complete and generate their required data.

Part of designing the canonical view of significant business objects is to also decide on routing keys. The routing keys allow subscribers to receive only complete events if they wish or all events to meet their needs. If your integration platform has a message broker like RabbitMQ / Service Bus etc, this routing can be achieved through configuration. If you use a streaming platform like Kafka then it's the abstraction layer (which may also be Kakfa streams) which will understand the routing rules.

---

#### Gateways

Here we agree exactly the message forms and conditions that are allowed and agree to send and/or receive those messages. Inter-domain messages will be allowed through gateways at a domain’s boundary. Incoming/outgoing messages at the gateway are sent to/delivered from the semantic hub. From the perspective of the semantic hub a gateway is no different from any other system “spoke”.

A security gateway is required to control message delivery. This must authenticate and verify the integrity of messages entering the domain. It may also play a role in message payload encryption and/or signing. The gateway may also authenticate and validate messages on egress from the enterprise. But it must not perform any authorisation. The gateway does not make any policy decisions on what services can be reached by properly formed and authenticated messages. Also, messages within the domain are not further validated nor authenticated.

---

#### Context Aware

The Data Governance group will define a set of policies which the Data Mesh data products must enforce, and the data must be context aware. Having context aware data means that while the schema will be consistent, different roles will receive appropriate data. I.e. the data responses will be filtered by record (row-level security in RDBMS parlance) and attribute (column-level security).

This context aware access can be achieved through Attribute Based Access Controls (ABAC) in concert with the Identity Provider (IDP). The ABAC policies are themselves 'significant business objects' and so should be modelled, governed and added to the Semantic Hub.

Our ABAC policies should be used to enforce masking and filtering based on the data classification. For example, a consumer may have read access to sensitive data on a specific object and write access to protected data. We must model our data with more than simple entity relationships, including classification, audit requirements, volumetrics etc.

---

#### Analytics, ML and Real-time metrics

As mentioned, we store data flowing through the mesh in polyglot persistence - operational DBs and data lake-houses. While we should store raw data in our lake for audit purposes, the data has already been curated via the operational interfaces, saving us lots of work. There is no use of raw data in creating curated lake-house layers - we simply flatten the incoming data and produce virtual data warehouses through columnar views. More on this here: [Data Autonomy - BI & Analytics](./2020-07-30_data-autonomy-bi-analytics.md)

The analytic interfaces must also be capable of enforcing ABAC policies. If you're in the Hadoop ecosystem then Apache Ranger has worked for me in the past.

The key for technology choice here is agility - our stored data must be able to change as our business view of our data changes.

---

#### Changing the solution

Data autonomy has an effect on the way we solution. Instead of solutioning a process, we look at what logic each application is responsible for and what significant business data we need to feed each application and what data it creates and updates.

For each significant business object in and out of the applications we decide on the appropriate mechanism - [APIs, pub/sub](./2020-07-19_data-autonomy-resource-oriented-event-driven.md) or a custom flow. This is often dependent on what triggers the applications business logic.

This is fulfilling 2 important concepts:

- Event Driven Architecture: 'It is better to have the data you need to do your job when you go to do it'.
- Data Autonomy: Making each application dependent on the business semantics rather than application idiosyncrasies.

By looking at discrete pieces of business logic, the triggers and the data required, we can modernize the business much easier than a strict process view of a solution. This is especially powerful if we are moving to an [enterprise micro-service architecture](./2020-06-24_enterprise-microservices.md) as the logic can be moved from the legacy systems.
