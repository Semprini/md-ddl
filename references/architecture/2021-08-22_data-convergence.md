# Data Convergence

![AI Overlords.png](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/AI_Overlords.2e16d0ba.fill-800x240.png)

There is so much scope for change in IT. It's quite a pure form of expression of ideas because its underlying logic gates have been virtualized and almost completely abstracted. There are no laws of physics that apply.

But Semprini, you wizened lothario of technology, why then is the pace of change at most companies ever slower?

Excellent question my intrepid reader, lets dive into this and hopefully even plausibly relate it to the topic of the blog - data convergence.

---

The reason I seem to have started on a tangent is that I think that it's the way we approach and handle data which is an underlying cause of slow IT. I also think there is a possibility of the industry having a real paradigm shift (yes, I hate myself for those wank words) because of convergence of data technology.

So, what exactly is converging? Another perceptive question dear reader - I can see we're kindred spirits.

***1 - Operationally***

Firstly, the line between operational and BI/ML/analytic data has blurred. I'm old enough to remember the advent of cell phones, and at the time it was considered self important or arrogant to think you needed to be contactable away from your office or home. Mobile tech is now fully integrated into our lives and similarly, the once fringe disciplines of AI & machine learning has moved from a curiosity to core business application.

The point here is that machine learning and analytics increasingly needs real-time streams to trigger it, then extra data in real-time to augment but it also needs vast quantities of data to train it. "...this can’t be achieved with two separate data planes - analytical and operational data planes - that are far from each other and connected through fragile data pipelines and intermediary data teams. Data pipelines must dissolve and give way to a new way " - Zhamak Deghani.

Streaming and event driven architectures have brought new ways to process business functions, machine learning algorithms and micro-services have [taken data mastery away from COTS applications](./2021-04-24_systems-record-bollocks.md) and each can choose a funky way to store its data.

This convergence means we can master canonical business data for operational APIs & events, reporting, analytics and ML via polyglot persistence as a set of data products. I'm pretty biased here based on my thinking in [Vestigial Technology](./2018-12-20_vestigial_technology.md) which leads us to Zhamak Dehghani's [Data Mesh](https://martinfowler.com/articles/data-mesh-principles.html) principles.

***2 - Technology***

Secondly, coming is a time where computers, networks and AI are powerful enough to decide for themselves on how to store data on the fly and change dynamically. It may choose to transform as it stores for consistency or may decide for a schema on read - or a composite style because it's a full moon and there's inaccurate data about because people have lied about their werewolf status.

The spacecraft that got us to the moon had many orders of magnitude less compute and storage so every byte and instruction were precious and we were so much closer to the underlying technology. Since the start we have been using added compute power to add abstraction layers which soak up that extra performance but enable us to spend more time on the human problems and less time on the technical ones.

Once an AI understands the semantics of our data and the use of our data, the need for us to choose persistence technology goes away, the need to define and migrate schema goes away and "I finally rest and watch the sun rise on a grateful universe." - Thanos

So in the meantime, before we welcome our new AI overlord(s?) what have we got? Most database platforms are multi-model and you get the same performance out of SQL vs NoSQL if you do a like for like comparison - it's just the ease of setup for specific modes which is the differentiator.

SQL, NoSQL databases and blob storage are being used for columnar storage, and all have GraphQL interfaces. Let's face it you don't have big data unless you're doing specialist work or a cloud provider. Rocket Labs here in NZ targets up to 3M telemetry readings per second and analysis is done across petabytes for example so fair enough, but compare that to a telco, utility or bank which deal in hundreds or thousands of events per second but often from disparate sources. The questions asked in analytics and data science can be more easily answered if the data is more consistent which is kind of the point of both databases and the up and coming Delta Lake.

***3 - Architecturally***

In an event driven architecture, we typically have a 3 flow, 2 transform pattern which loosely couples publisher from subscriber by abstracting the semantics of the data to a middle/canonical model. Similarly, in data lakes we often take data from raw to curated to business layers for the same reason. Now that batch ETLs aren't cool and streaming is the hipster beer of IT, these pipelines can converge into a more holistic, end-to-end handling of our data. If we're smart in our integration architecture, there need be no difference between synchronising data to a line of business application, analytics engine or triggering a machine learning flow.

---

...and now back to my raison d'etre: cynical ranting about enterprise architecture.

The ease of cloud blob storage like ADLS and S3 with cloud vendors desperately trying to get lock-in through 'best practice architectures' of processing raw data have led us to heavy data wrangling solutions.

We now have vast workforces invested in what I call 'plumbing architecture' where we think that just because the end to end flow uses nifty cloud tech that we can stand up with a few clicks or infrastructure definition, that we have a well architected solution. We can easily draw up that architecture with beautifully clean viewpoints which will get IT managers aroused, but we can equally simply draw up that architecture as a bloated mess of data spaghetti. Both views can be accurate and it's the logical architecture which shows if data will be treated well.

The Peter Parker Principle applies here - "With great power comes great responsibility" I.e. we are able to do more harm more quickly in the cloud if we don't respect our data through our logical architecture.

I think I would like to amend a [previous statement](./2021-04-30_architecture-rant.md). Good architecture is the *sympathetic treatment of people, process, technology*, ***and data***.

Management seems to suffer from FOMO brought on by vendors and consultants selling the current buzz words (lake-house, I'm talking about you and 'delta lake' coming soon to an EA conversation near you). Architecture needs to get better at scything through the noise, lifting the skirts and inspiring both management and delivery teams to see a better way. Remember: 'the fact a solution works is proof of nothing more than it is working.' - R.M. Bastien.

---

Actually, I'm a bit of a fan of Delta Lakes but that's for a different blog. However, I almost missed this gem due to a combination of cynicism and the amazing amount of wank used to push it. Just like any technology silver bullet it's not what you've got, it's how you use it.
