# **Entities**
Each file must declare which domain it is part of by starting with a Level 1 heading with the domain name. 


### **Entity Declaration**

The Entities section appear under a level‑2 heading:

```markdown
## Entities
```

Each entity is introduced with a **level‑3 heading**:

```markdown
### Customer
```

### **Entity Description**

Free‑text Markdown under the heading describes the entity in more detail than was found in the domain summary.

### **Entity Definition**

A structured block defines the entity's attributes:

````markdown
```yaml
attributes:
  - name: customer identifier
    type: string
    identifier: true
  - name: email address
    type: string
    pii: true
```
````

### **Naming Rules**

- Entity names use natural language.  
- Attribute names use natural language.  
- No camelCase, PascalCase, or snake_case.  
- No redundant 'name:' field inside the block — the heading is the name.
- No relationship attributes. Relationships are defined in the relationships section.  

---
