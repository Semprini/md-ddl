# Data Autonomy - Resource Oriented & Event Driven

![architecture.JPG](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/architecture.2e16d0ba.fill-800x240.jpg)

[Data Autonomy](./2019-02-17_data-autonomy-overview.md) is a collaboration of A Holistic Data Fabric/Mesh, RESTful interfaces, streaming events and enterprise micro-services. Focused around Resource Oriented Architecture (ROA) rather than Service Oriented Architecture (SOA), its purpose is to provide the ability to change rapidly by keeping the level of dependencies constant across the IT landscape.

---

#### RESTful Resources

REST is a significant enabler of change. Properly defined RESTful interfaces can have more non-breaking changes than SOAP based integrations.

This allows a better versioning strategy and easier consumer upgrades. In integration architecture parlance - if you own both sides of the integration contract then upgrade as you go. Please see Brandon Byars and Martin Fowlers article: [enterprise REST](https://martinfowler.com/articles/enterpriseREST.html#versioning)

A key concept in REST to enable rapid change is HATEOAS as this enables consumers to use the end points provided in a response to get to another resource rather than rely on a configured end point. The pace we can create micro-services is greatly increased by letting the data layer instruct us on how to query itself.

As an extension to REST, responses from the API layer contain not only URLs to the current and related resources but URI to resource event subscription and routable attributes. REST is generally regarded as a request/response communication model, however Data Autonomy combines an event driven architecture with REST concepts. I.e. the representations of resources returned via RESTful APIs must be the same as representations in event messages (with some context specifics).

---

#### Events

Here's my favourite, elegant tenant of Event Driven Architecture: *It is better to have the information we need to do a job when we start.*

It is business events that have cause and effect and when events cross system boundaries we have a need for integration. Integration is the act of communicating a resultant event in one system to a triggering event in another.

The assertion of Data Autonomy is that it is better to respond to changes in *significant business objects* caused by operational processes due to the maturing nature of data models. This is discussed in [Data Autonomy Overview](./2019-02-17_data-autonomy-overview.md)

Data Autonomy doesn't mandate an event model for all integration. It aims to mitigate the overhead in implementing an event driven architecture so solution architectures can pick the right approach each time. I often favour subscribing to events and then POSTing changed significant business objects so we can handle exceptions in real-time or put the incoming event through retry or dead letter process.

Since our events are resource oriented, there will naturally be evens for resource POST, PUT, PATCH, DELETE. This means that by providing a good (self documenting OpenAPI, RAML etc.) REST API interface we also know the event model. For example:

`POST /customer/account/`

Can be subscribed to at (assuming a message broker here):

`.customer.account.post`

And the messages that come back will be identical including links to further resources. E.g:

![customer_GET_Queue.png](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/customer_GET_Queue.width-800.png)

An important point to emphasise here is that the queues and APIs are not defined by application processes but data semantics. True decoupling of application idiosyncrasies and changeable business process - this is how we create a high cadence of change which does not diminish over time.

---

#### This is bollocks, my process must be synchronous to a system of record!

Data Autonomy is not a panacea but aims to solve for the 80% or more.

As an example of an exception and how to elegantly interface with data autonomy, lets look at a credit card payment from an online channel in a banking organisation.

This situation is where the front-end response is dependent on logic in a core system and it must block until this logic is run and the decision is reached.

Here we use standard synchronous integration patterns ([www.enterpriseintegrationpatterns.com](https://www.enterpriseintegrationpatterns.com/patterns/messaging/ComposedMessagingWS.html)) with a data siphon to complete the task. There are few points to note:

1. The number of processes using this pattern is vastly reduced so the infrastructure and component architecture requirements are reduced.
2. If data governance and the payment area data stewards have defined a requested payment as a 'significant business object' then the payment data from the synchronous payment request will be published or POSTed to the data platform.
3. Since the payments core system will have created or updated significant business data, this must now be published, POSTed, PUT, PATCHed to the data platform. This can be done either:
   1. If the response data has the significant business objects then we can siphon the data off here
   2. If the application abstraction layer uses some form of change data capture then the data may flow from this.
4. If the flow used enrichment of data from a 3rd party and the data returned is considered significant then this data should also be sent to the data platform.

Key to the thinking in this example is that data is treated holistically - it is not published for a specific business destination but because the data stewards & modellers decide that it is "significant".
