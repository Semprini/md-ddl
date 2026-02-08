# **Entities**

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

Free‑text Markdown under the heading describes the entity.

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
