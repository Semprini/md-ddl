# [Retail Service](../domain.md)

## Data Products

### Service Domain Model

The authoritative domain-aligned view of the Retail Service bounded context. Exposes the canonical Customer (service definition), Service Request, Service Case, and Knowledge Article entities for integration with other domains.

```yaml
class: domain-aligned
schema_type: normalized
owner: domain.service@retailer.com
consumers:
  - Cross-domain Integration
  - Customer Experience Platform
status: Production
version: "1.0.0"

entities:
  - Customer
  - Service Request
  - Service Case
  - Knowledge Article

# TODO: Add lineage once sources/ directory is populated for this domain.
# lineage:
#   - source: <crm-system or service-platform>
#     tables:
#       - <transform files>

governance:
  classification: Internal
  pii: true

masking:
  - attribute: "Customer.Email Address"
    strategy: hash

sla:
  freshness: "< 10 minutes"
  availability: "99.5%"

refresh: real-time
```

#### Logical Model

```mermaid
---
config:
  layout: elk
---
classDiagram
  class Customer{
    * Customer Identifier : string
    Email Address : string
    Given Name : string
    Family Name : string
    Preferred Contact Channel : enum~ContactChannel~
    Language Preference : string
    Total Cases Raised : integer
    Last Contact Date : date
  }

  class ServiceRequest{
    * Service Request Identifier : string
    Status : enum~ServiceRequestStatus~
    Contact Channel : enum~ContactChannel~
    Subject : string
    Received At : datetime
    Resolved At : datetime
  }

  class ServiceCase{
    * Case Identifier : string
    Status : enum~ServiceCaseStatus~
    Priority : string
    Assigned Agent : string
    Opened At : datetime
    Closed At : datetime
    Resolution Summary : string
  }

  class KnowledgeArticle{
    * Article Identifier : string
    Title : string
    Issue Category : string
    Resolution Steps : string
    Published Date : date
    Last Reviewed Date : date
    Applicable Product Category : string
  }

  Customer "1" --> "0..*" ServiceRequest : raises
  ServiceRequest "0..1" --> "0..1" ServiceCase : escalates to
  ServiceCase "0..*" --> "0..1" KnowledgeArticle : resolved by

  class Customer["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Retail%20Service/entities/customer.md'>Customer</a>"]
  class ServiceRequest["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Retail%20Service/entities/service_request.md'>Service Request</a>"]
  class ServiceCase["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Retail%20Service/entities/service_case.md'>Service Case</a>"]
  class KnowledgeArticle["<a href='https://github.com/Semprini/md-ddl/blob/main/examples/Retail%20Service/entities/knowledge_article.md'>Knowledge Article</a>"]
```
