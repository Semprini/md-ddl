# Systems of Record. Bollocks.

![SystemsOfRecord.png](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/SystemsOfRecord.2e16d0ba.fill-800x240.png)

Having systems of record is a widely accepted architectural pattern used to provide clear delineation of responsibilities and guidance to end-to-end solution architectures.

It is an architectural pattern of it's time, suited to an IT landscape of large monolithic applications and was the dominant strategy since the 90s across almost all corporate IT. If this it your IT strategy, you have good governance and patterns for change and an integration architecture which is for keeping these monoliths in-sync then go forth and prosper - you will have mature IT and a reasonable cadence of change.

More likely however, is that significant data is created in what is considered systems of record, half migrated new systems of record plus micro-services and analytic / machine learning flows so the misalignment of systems of record to the business view has become more obvious and material.

There is not a good semantic fit between an applications view of data and the business view of data so lets stop pretending.

---

## Semantic Misalignment

I'll use customer as an example but the logic applies to all domains of the organisation. The business view of it's data has evolved and we must become more holistic about how we see our data to enable the next generation of hyper competitive business through analytics and machine learning. The system of record style architecture has very different concepts for operational vs reporting/analytic data because we try to map the "master" to the application functionalities and persistence technologies. This is further complicated by micro-services with their own data sources. As we bring micro-services, machine learning and analytics into operational flows this distinction is no longer valid - significant data is now created in what is considered systems of record plus micro-services and analytic / machine learning flows.

Lets use the BIAN reference model for banking for our customer:

*Service view: "The collection of activities that maintain, manage and leverage customer relationships, providing cross-product perspectives, matching products and services to customers and providing targeted analtics and decision support to enhance the bank's delivery performance, 'share of wallet' and overall customer experience"*

*Capability view :"Ability to define, control, predict, process, organize, present, and analyse all aspects of information, documents, preferences, experiences, and history related to an individual or other legal entity that has, plans to have, has had, or is a recipient or beneficiary of a legally binding agreement with the organization."*

BIAN is modelled around how banking works (feel free to use any industry reference model or a lower level of the model). If we compare the capabilities of an out of the box CRM (the most common system of record for "Customer"), there are multiple functional areas not found out of the box. Due to systems of record, we have previously been forced to customise and wedge in the missing areas. This is even before we look at the associated/dependent areas in the parent Customer and Distribution area and other areas.

We can therefore see that there is not a semantic fit of the holistic business view of customer to the system of record for customer. If you have customer data being created and owned in multiple places, then do you really have a system of record for customer? or do you have applications responsible for certain areas of business logic and a distributed customer master?

All of these semantic misalignments can be accounted for in middleware to some extent and give the appearance of true systems of record. If your organisation has that mature, monolithic landscape I mentioned earlier, then this is perfectly valid but will never deliver more than a certain cadence of change. The more we wedge into the out of the box application, the more work we have to do in middleware to account for the misalignments and therefore the slower we can change.

---

## Legacy Transformation

The vast majority of organisations I engage with have legacy transformation issues. In some theoretical future state, there will be a beautiful, clean IT landscape leading the organisation into the broad sunlit uplands of peace and prosperity.

The reality for the next n years however, (assuming we're not doing a big bang) is that we will be hiving off functionality from our current systems of record piece by piece. Once again do we therefore have a master? or do we have a system responsible for generating the customer number and then a distributed set of business logic?

With the increasing pace of change required by the business and the prevailing system of record mindset we have to in effect start painting the bridge at the start before we've finished painting on the other side. Architecture must be practical as well as being an intellectual pursuit and the sooner we give up the misnomer of a system of record the sooner we can deliver improved cadence of delivery.
