# [Financial Crime](../domain.md)

## Data Products

### Salesforce CRM Raw Feed

Raw audit feed from Salesforce CRM preserving source schema and change
events for replay, integration debugging, and compliance audit trails.

```yaml
class: source-aligned
source: salesforce-crm
owner: data.engineering@bank.com
consumers:
  - Data Engineering
  - Audit & Compliance
status: Production
version: "1.0.0"

governance:
  classification: Internal
  retention: "3 years"
```
