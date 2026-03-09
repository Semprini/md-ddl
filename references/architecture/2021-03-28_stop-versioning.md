# Stop Versioning!

![versioning.png](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/versioning_rKNAWvM.91d64086.fill-800x240.png)

This concept will clash with many peoples thinking on the topic but I ask for willing suspension of disbelief and to challenge your existing bias. This is the right conversation to be having for many organisations.

"I'm not having anyone stare in disbelief at My willy suspension!" - Capt. Edmund Blackadder

My assertion is that integration versioning should be a last resort, used in specific situations. If you own both sides of the integration contract then it is better to not version.

The famous dig from Jamie Zawinski:

***Some people, when confronted with a problem, think "I know, I'll use versioning." Now they have 2.1.0 problems.***

---

Versioning is in effect kicking the can down the road for your future self, or worse - leaving it for someone with no knowledge of the interface.

By following [Postel's Law](http://en.wikipedia.org/wiki/Robustness_principle), using abstraction layers, micro-service boilerplate and not being afraid of regression testing (I.e. modern IT practices) we have simple to change components which we can track and upgrade.

***"Be good at small, regular change."***

We do not version our DB tables. Why? Because we do not want to push knowledge about what data is in what format to our consumers. If we just look at 'System Level' data access interfaces (API and messaging) these are simply wrappers around a data-store so why version just because we change protocol from SQL to REST/Messaging?

Here's a couple of common versioning strategies and behaviors which show why versioning system level interfaces is an anti-pattern to well governed and agile organisations.

### n-1

Let us say you are a developer who is responsible for writing a breaking change to an interface. You pull the existing code in, create a new version and a new endpoint for the version and push your code.

This seems fine; however, the old version was V2 and the new version is V3, so you now must find all producers and consumers of V1 and upgrade them all. As per usual, there is no budget for upgrading old interfaces, the project doesn’t care or want to pay for it, no one knows the systems and a business case shows there is no functional benefit, so it is quickly de-scoped.

By having an N-1 strategy you have gained nothing and just made things harder as the changes are more remote and opaque than just upgrading V2 consumers and producers would have been.

### n-n

Another prevalent approach is to only upgrade interfaces when the consumers need something different. The idea being some interfaces can sit for decades, servicing a set of clients well. While n-1 is a death by a thousand cuts, n-n is more of a cancer which slowly atrophies an organisation. Decisions begin to be made based on avoiding changes to the interfaces as the people who have any knowledge of how it works have long since moved on. Changes become bigger and slower to manage.

---

## So, what's the plan then?

Revisioning is great, keep semantic versioning for that but do not maintain multiple live versions longer than the time to upgrade.

### Autonomous development, authoritative release

Experience level interfaces can be versioned but system level interfaces should not.

Everyone who consumes the system level operational interfaces must be part of the regression testing suite and every team involved in a change may have their own source repo ([hopefully not a feature branch](https://thinkinglabs.io/articles/2021/10/25/on-the-evilness-of-feature-branching-why-do-teams-use-feature-branches.html)). For each repo, our continuous integration pipeline should generate revision tagged artefacts and the manifesto of the release is compiled from these artefact revision tags.

We then release together. I submit that the longer term overhead & reduction over time of delivery cadence caused by n-1 & n-n make this overwhelmingly better practice.

All our consumers become either new micro-services or simple abstraction layers which are all extremely nimble and changeable. Throw a semantic change of a well documented, well encapsulated, well unit tested middleware micro-service to any developer and you should be able to expect it to be ready for production release in minutes/hours.

[Here's a blog on the topic](https://www.linkedin.com/pulse/autonomous-development-authoritative-release-jules-clements/?trackingId=RLrUlTZTRxmnXt%2BGTDx%2BPw%3D%3D)

"The time between identifying a business need and delivering the required IT solution needs to become hours and days rather than months and years." - Adam Althus: The composable enterprise.

### + Transitionary Versioning

When dealing with large database migrations, deployments can take hours. We probably have SLAs to meet which means we cannot take down production for anything like that long - this is a common problem which drives many versioning strategies and often atrophies our semantics. My approach here is to either use one of the read replicas or, because most DBaaS have a triggerable / 5 min snapshot, we spool up an independent DB in the old schema during the deployment window and keep track of the changes to replay once the new schema is migrated.

Keeping track is a simple task for brokers like Kafka as we simply note the offset with the snapshot but synchronous API change calls need to be replayed too. In this case, use an empty database in the old schema, turn off relational integrity checks, apply all interim changes to both the independent DB with the current data and this empty DB. Once the new schema migration is complete, then run the same migrations against the temp DB and load into the new production DB. Yes, this is a pain in the ass, and if you can stop write access during the deployment window, it will save you a lot of faffing about.

### Event Driven Adapters

In a distributed, event-driven environment, the culture may not allow for a larger product release style. To upgrade consumers gradually, we can introduce a temporary adapter. To do this we create new topics in the new format, which the adapter subscribes to, transforms and publishes to the old topics. We then upgrade the consumers independently and finally decommission the old topics and adapter.

### Green/Blue Versioning

The upgrade as you go concept may be challenging to many peoples view of integration practices but hopefully we can all agree that versioning is a hard question, there is no silver bullet and to some extent we have to pick our poison. One easier to swallow option is to adopt transitory versions which live as long as the next change (minor releases included) - or "Green/Blue" versioning.

This linking of deployment solution to versioning is intentional and I think leads the conversation in interesting ways. The idea here is to have a small buffer to allow teams working on different schedules to deliver their changes independently but rapidly behind a breaking change. There is a little more coding here as the new deployment of interfaces have to handle the previous version and the new but the next feature will be coming down the pipeline so we have a transient window to move off the previous version.

With Green/Blue versioning, the persistence schema (E.g. DDLs) would always be migrated to the latest version but the operational interfaces would need to accommodate the new and the older version during the transient window.

### 

---

## System Level vs Experience Level Interfaces

When we treat data as a product, we expose the current business view of our data in both operational and analytic interfaces. These operational interfaces are 'system level' APIs and streams which we then create our rich 'experience level' interfaces. We control the interface contract between system and experience layers therefore we upgrade these as we go. However, the experience APIs can be versioned or new micro-services written as we probably don't own both the experience and consumer sides of the integration contract.

***"Be good at small, regular change."***

IT should be able to maintain multiple data model changes to production per day. If an application cannot be part of the automated regression tests, then we must abstract that consumer with some middle-ware (Application Abstraction Layer) which can be part of the regression tests and stub the application. We must be able to spool up these environments in minutes, test, report and destroy.

Unlike code of business logic where feature branching leads to version dependency hell, the data model can adopt a product release branching strategy to introduce breaking changes. This encapsulates the infrastructure as code, all abstraction layers, DB migrations and any micro-services part of the regression testing scope.

More discussion, focussed more on compile time dependencies here: [Enterprise Integration Using REST (martinfowler.com)](https://martinfowler.com/articles/enterpriseREST.html#versioning).
