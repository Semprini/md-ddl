# Model Driven Generation

Where is the truth of an organisation? Many programmers would say that the truth is in the code as this is what is actually running the organisation. The code is in effect a realization of business demand and therefore the truth of what an organisation actually is can be found within.

I think that while somewhat accurate, it is a little 'ambulance at the bottom of the cliff' thinking and we should rather strive to be declarative in what the organisation is. Also, assuming we buy for commodity then the view is obscured and incomplete. The declaration of a business is best done via modelling as the related views can inform and align everyone from board to developers.

---

Architecturally, I like to separate out business logic from business data - a little like we separate out UI/UX from application logic. So while the logic of an organisation may be found in the code, the lifeblood of the business can be found in the semantic meaning of it's data.

We have a very powerful declarative tool once we have a conceptual and logical model of our data and infrastructure. I like to use this tool to master and automatically generate many things like infrastructure as code (e.g. Terraform definitions), schemas (e.g. OpenAPI) or even complete data platforms.

We should imbue more than simple entity relationships into our models. Capturing the policies which need to be enforced from business to security to data governance strengthens the declarative power of the model. My view is that tools commonly seen in enterprises for data lineage (E.g. Informatica EDC advanced scanners) and application licence / CMDB scanning should be used to validate & audit what the models intend - not to be a source of truth.

---

My open source version of a model driven generation tool is pyMDG. While it's modelling tool agnostic, each modelling tool needs a parser library which I've written for Sparx EA and Diagrams.net so far. It will also be modelling language independent but I'm working on UML at the moment.

[Read The Docs: pyMDG](https://pymdg.readthedocs.io/en/latest/index.html)

#### To use pyMDG we need to build:

1. A UML model
2. A generation recipe

The recipe tells pyMDG about your model and what files to output. This tutorial uses the sample templates and config which you can find in the sample\_recipe folder from the project on GitHub: <https://github.com/Semprini/pyMDG>

#### Data Model Nomenclature

When pyMDG parses the source model file it parses into specific python classes.

![Nomenclature.png](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/Nomenclature.width-800.png)

#### Example Data Model

![TestDomain.png](https://s3.ap-southeast-2.amazonaws.com/semprini.me/media/images/TestDomain.width-800.png)
