# Data Products: Architecting Data Autonomy

![Architecting Data Autonomy](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/Architecting_Data_Autonomy.2e16d0ba.fill-800x240.png)

Hello, people of the internet, browsing blogs to do with IT and Data. You've found the 2nd part of a data blog which looks at using patterns to form data products. Welcome, dear reader.

In the [previous blog](./2024-07-11_data_products.md), I made some bold claims - promised some patterns to unlock all the goodness, save hundreds of millions, speed everybody up and unify classical physics and quantum mechanics. Ok, not that last one, but it's still pretty cool stuff.

When we write software, we write it for the next person who must read our code. This too is how we should solution - for the next initiative. I.e. what have I done in the current solution to make my and others lives better for the next solution? This is part of the intent of canonical models - for both data and capabilities. If we conform our solution to an industry standard view, rather than an application-to-application view it makes everyone's lives easier.

---

What we need is a reusable architecture pattern and engineering patterns which help us implement this canonical view. Luckily, [Gregor Hohpe](https://www.linkedin.com/in/ghohpe?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAADMZ0BDKCmI9lFuuQ_q31EDBKxnZA5igg&lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_all%3BphvYNh3KRkCQyiYpsjguwg%3D%3D), and Bobby Wolfe come to the rescue with: [Canonical Data Model](https://www.enterpriseintegrationpatterns.com/patterns/messaging/CanonicalDataModel.html). Able to leap tall buildings in a single bound, and translate rom coms for blokes, this is the key architecture pattern which we can use to standardise data products.

![Canonical Data Model Pattern](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/CanonicalDataModel2.width-800.png)

---

Each application gets a translator - in and out. This is also known as application abstraction as each translator is responsible for abstracting all the application shenanigans via protocol and semantic transformation.

As we will have a range of source and destination systems to translate, we should end up with a kitbag of abstraction tools. From Change Data Capture (CDC), to data transformers, to data lineage, etc. These are the platforms on which we build our first type of data products - Abstraction Data Products. Please don't call them abstract data products - that's a whole different thing.

"But Semprini, you audacious agitator of architecture." you say, "That's not a data product, it's just ETL and [bronze to silver data layers](https://dataengineering.wiki/Concepts/Medallion+Architecture) - I'm just going to use my data lake.". Ah, my data engineer friend, Big Data platforms are indeed a big hammer which makes every data movement look like a nail. Being holistic and solutioning for the next initiative means looking at the data and its canonical uses in the organisation. If the online channels would love to have this data available, or the data is part of a user business process which involves multiple applications, then the data's non-functional requirements are probably sub-second and micro-batch ETLs are not gonna cut it. This is a key point in thinking architecturally, "The *data's* non-functional requirements" - not an initiatives requirements.

If we can make the data available and timely for all use cases, future us will be rightly smug. The best, most performant way of doing things becomes the easiest and the next initiatives naturally fall into this pit of success.

![Abstraction Data Product2](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/Abstraction_Data_Product2.width-800.png)

We must fight against Conway's Law and actively drive the convergence of operational and analytic integration. If an initiative falls into the data space, then the people will push for data engineering tools which make timeliness beyond the current initiative harder, and if the initiative falls to the integration teams then iPaaS, micro-services or ESB will be pushed which can make lineage and governance harder. I'm not saying which is right or wrong, I'm saying your data's requirements will tell you. By pushing the right thing for our data, not the simple thing for our initiative, we will create an ecosystem of data improvement. I use the Māori term Rongoā here - if we look after our data landscape (Papatūānuku - the land) then it will nourish us all.

---

From our pattern, the abstraction data products are the translators. This leaves the canonical thingy in the middle. Welcome to our master/canonical/foundational data product - for free!. "Wait, what? Did you skip ahead there Semprini?" you ask, incredulous. No dear reader, I'm saying that the canonical data product is made up of stuff we should be doing anyway, we're just applying domain driven design, and iterative practices for bite sized features which initiatives should have implemented in some way - we're just being opinionated on a standard data flow and thereby driving that pit of success.

Significant data should be loosely coupled (general principle), with or without data products. When applying the canonical pattern, data products tell us the scope for source code repos, system testing and atomic deployments. Yes, this may mean the first data product is little more than a Kafka topic or CRUD API pass through - as long as the topic/API has a canonical schema and is deployed independently we have a proto product which we can add features to as we go.

This way of solutioning is to deal with the interim state, a way of steering the ship while under the waterline, we convert it to something spectacular.

![](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/Flying_Ship.width-800.png)

There are a more features we need to turn these canonical flows & CRUD into valuable data assets and unlike the proto products, this will cost. However, the business case for these data product and platform features is pretty simple to make and the implementation can run along side the loose coupling pattern for interim solutions.

- If your business is concentrated on risk then data products provide business ownership and accountability (please note the difference to responsibility) for the availability, security and accuracy of data - and not at some conceptual level but at a physical level as data products are business assets. We have also standardised the number of data hops to make data governance with automated controls simpler.
- If your business is concerned with technical debt and legacy transformation, even easier - as discussed in [part one](./2024-07-11_data_products.md), data products are your engine for legacy transformation.
- Lastly, if your business is looking for fast time to insight, or fast time to market, our ecosystem of abstraction to canonical, makes all significant data available by default, in business form, on a marketplace with automated controls.

This means our canonical data products can evolve from the proto product into the source of truth for each domains data. A true asset for the org, serving trusted data for all use cases.

![Canonical Data Product](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/Canonical_Data_Product.width-800.png)

---

Now, my intrepid data pal, you may have noticed something that is missing between the proto products and the data assets - Key Management/MDM. Informatica has a good description of Master Data Management: "creating a single master record for each person, place, or thing in a business, from across internal and external data sources and applications ". However, there is a semantic misalignment between each application and our canonical model. I discuss this here: [Systems of Record. Bollocks.](./2021-04-24_systems-record-bollocks.md) To create a true master record, we need not only to create an enterprise Id, but we need to maintain key mapping between the various system viewpoints and relationships to allow efficient on-boarding via our abstraction data products.

![Key Mapping](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/Key_Mapping.width-800.png)

Our abstraction data products will need to look up the key mapping to publish it's data changes. Just like any other piece of required data, the abstraction can choose to read from the canonical data product via API or stream & cache the key mapping data.

In our canonical data product, we need a "get or allocate Id" function for returning the enterprise Id. The most efficient way to do this is as a stored proc on the ODS but you may have other means.

This key mapping engineering pattern means our canonical data products know where each piece of data came from. This is automatic, real-time lineage of on-boarding for all significant data.

---

What I'm doing here is taking Zhamak Deghani's Data Mesh thinking and combining it with Hohpe & Woolf's integration pattern and extended it with Key Mapping to provide Data Autonomy. Zhamak uses the term "architectural quantum", and this is what I'm delivering here - data movement is solutioned by placing data products like Lego and we have convergence of operational and analytic pipelines: “To make good decisions in the moment, analytical data must reflect business truthful‐ness. They must be as close as possible to the facts and reality of the business at the moment the decision is made ... this can’t be achieved with two separate data planes - analytical and operational data planes - that are far from each other and connected through fragile data pipelines and intermediary data teams. Data pipelines must dissolve and give way to a new way” – Zhamak Deghani.

You'll see in this blog I have been deliberately agnostic of tech stack. It's all about capabilities and at this point we should start to see how our data platform, management and governance services need to be exposed to our engineers & stewards:

![Data Products E2E](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/Data_Products_E2E.width-800.png)

As data products follow domain driven design, there will be multiple canonical data products. The granularity of these will likely be a negotiation between the product owners, engineering, modellers and governance. We should expect to get this wrong, which is Ok! We're setting up an ecosystem where the right data products can evolve as our understanding of our data evolves - be good at small regular change.

In the 3rd part of this 2-part blog, I'm going to model and build a canonical data product. What I'll show is that the canonical data products can be 100% automated from the data model - except breaking schema changes which require data migration.
