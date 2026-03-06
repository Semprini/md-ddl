# [Financial Crime](../domain.md)

## Data Products

### Canonical Party

The governed canonical representation of Party, Party Role, and related
identity entities for consumption by downstream domains and cross-domain
integration points.

```yaml
class: domain-aligned
owner: data.architecture@bank.com
consumers:
  - Cross-domain Integration
  - Customer Domain
  - Regulatory Reporting
status: Production
version: "1.0.0"

entities:
  - Party
  - Person
  - Company
  - Party Role
  - Customer
  - Contact Address
  - Address
```
