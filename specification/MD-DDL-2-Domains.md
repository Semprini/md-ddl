# **Domains**

### **Domain Declaration**

A domain is declared using a **level‑1 Markdown heading**:

```markdown
# Customer
```

### **Domain Description**

All free‑text Markdown under the H1 heading and before the next H2 heading is considered the domain description.

### **Domain Metadata**

Metadata is appears under a level‑2 heading:

```markdown
## Metadata
```

Metadata may include:

- owners
- stewards
- tags
- classification
- diagrams

### **Metadata Format**

Metadata is expressed as YAML or JSON inside a fenced code block:

````markdown
## Metadata
```yaml
owners:
  - data.customer@example.com
stewards:
  - jane.doe@example.com
tags:
  - core
  - pii
```
````

### **Diagrams**

Diagrams appear under level‑3 headings inside the Metadata section:

````markdown
### Domain Overview Diagram
```mermaid
flowchart LR
    Customer --> "Customer Preference"
```
````

---
