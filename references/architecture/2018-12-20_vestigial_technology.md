# Vestigial Technology

![evolution-of-tech-image.jpg](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/evolution-of-tech-image.1c377ff7.fill-800x240.jpg)

Corporate IT has evolved much like ourselves - as Darwin stated 'we bear the indelible stamp of our lowly origin' and IT has it's fair share of appendixes and male nipples. Also like ourselves, this legacy takes resource to maintain and can cause systemic issues if it breaks down.

I can milk this metaphor even more! Feeding these unwanted parts in the body is our blood flow and data is the lifeblood of any corporate IT system. The energy an organisation or organism uses to pump it's lifeblood is how IT becomes slower at responding to it's needs.

Unlike corporeal beings, however, IT and the demands on IT are changing at at ever increasing pace.

What are we to do? Unsurprisingly, dear reader, I have opinions.

---

The reason we still have vestigial body parts is dependencies. The evolutionary process takes aeons to sideline redundant functionality because all our systems are interdependent and there is no active mechanism to deprecate this legacy. This is very similar to how IT has become a lumbering mass of legacy technology.

On a side note, I have a great fondness for things that many like to lump into the legacy bucket. Mainframes were doing micro-services (of a kind) long before it was trendy and I don't particularly care if you have a green screen. Many times I've seen a "modern" GUI replace a legacy keyboard system, and productivity/performance plummets. What matters to me is that it hasn't had years of tactical solutions built on top of tactical solutions, that we can deploy to it repeatedly and reliably, and we're not afraid of change and regression tests because the system is brittle.

...We now return you back to your irregularly scheduled ranting...

---

***If dependency is the enemy of agility then the architecture focus needs to concentrate on limiting dependency.***

The most important responsibility of IT becomes enabling accuracy and access to significant businesses data. The active mechanism of legacy deprecation while enabling access accuracy, is what I call Data Autonomy.

The time between identifying a business need and delivering the required IT solution needs to become hours and days rather than months and years. Delivering this cadence must not introduce dependencies so we can continue to deliver again and again.

The costs of doing the same thing in the cloud that we did on-prem is hitting hard, the lift and shift is not seeing the long-term benefits as sold to us by consultants & vendors. The two biggest drivers to the way we architect enterprises and solutions are the proliferation of targeted cloud based services and overcoming the drag of legacy systems.

"...the real force behind the success of rapidly growing firms is rooted in their ability to adapt." - Jim Hatch, Jeffrey Zweig.

Key to the ability to change in a distributed landscape is effective management of significant business data.

---

#### Dangers of Shadow IT

*"Most organizations grossly underestimate the number of shadow IT applications already in use,"*

- Brian Lowans, Gartner.

Shadow IT can expose an organization to a host of data privacy and security-related compliance risks. *"A data breach resulting from any individual* [*BUIT*](https://acronyms.thefreedictionary.com/BUIT) *purchase will result in financial liabilities affecting the organization’s bottom line. Liabilities can be very large due to a mix of costs that include notification penalties, auditing processes, loss of customer revenue, brand damage, security remediation and investment, and cyber-insurance."* - Brian Lowans, Gartner

Bypassing IT to procure cloud services can also leave an organization in violation of regulatory compliance requirements such as the Payment Card Industry Data Security Standard, the Control Objectives for Information and Related Technology and the Basel II international standards for banking.

At some point in a firm's growth, the lack of practical policies toward shadow IT and adoption of unrestrained cloud services will fragment significant business data and become a significant drag on operational change.

Organizations which do not adapt to this distributed IT landscape and embrace some form of shadow IT will be less flexible and less able to compete. The cadence of change in an organization is key to it's growth.

---

#### Data

Applications are built to perform business functions and, to do their job efficiently, they rightly structure and store their data for that purpose. Applications and application vendors do not have a holistic view of how your business operates as they service multiple businesses or industries. Dependencies on the data sourced from applications which comes with a host of application idiosyncrasies is why deprecation of legacy systems is notoriously difficult. Issues managing dependencies are also manifested in integration and can lead to a proliferation of middleware layers and versioning as soon as regression testing becomes too complex.

The standard way of approaching data access is to expose and integrate the data held in various applications through middleware layers/ESB. Thus, in theory, de-coupling the back-end from the consumer. As business progresses and the data layer loses that new ESB smell, it becomes more and more clear that there are other forms of coupling which are slowing down the cadence of change over time.

Versioning seems to be the default position for handling change. [This is a false economy](./2021-03-28_stop-versioning.md). Under the pressure to keep time frames and budgets, the first casualty is upgrading old interfaces. I am yet to see a business case where upgrading old interfaces to keep an n-1 versioning strategy stacks up. Jamie Zawinski put it succinctly *"Some people, when confronted with a problem, think "I know, I'll use versioning." Now they have 2.1.0 problems. ".* Every version is another set of dependencies which increase the cost of changing, upgrading or replacing an application.

The more dependent we are on an applications data, the more inflexible we are in changing the application.

---

My solution to enable large enterprises to act as a startup is discussed here [Data Autonomy Overview](./2019-02-17_data-autonomy-overview.md)

---

#### References

<http://www.gartner.com/smarterwithgartner/dont-let-shadow-it-put-your-business-at-risk/>

<http://searchcompliance.techtarget.com/guides/FAQ-How-does-shadow-IT-complicate-enterprise-regulatory-compliance>

<http://iveybusinessjournal.com/publication/strategic-flexibility-the-key-to-growth/>

<https://www.martinfowler.com/articles/enterpriseREST.html>
