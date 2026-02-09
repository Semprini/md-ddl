# **Relationships**
Each file must declare which domain it is part of by starting with a Level 1 heading with the domain name. 

Relationships are **first‑class citizens**.

### **Relationship Declaration**

```markdown
## Relationships
```

### **Relationship Declaration**

Each relationship uses a level‑3 heading:

```markdown
### Customer Has Preferences
```

### **Relationship Description**

Free‑text Markdown describes the semantics.

### **Relationship Definition**

````markdown
```yaml
source: Customer
target: Customer Preference
cardinality: one-to-many
ownership: Customer
```
````

### **Relationship Rules**

- Natural‑language names  
- No duplication  
- Ownership is optional  
- Cardinality uses natural language or UML notation  
- The compiler infers inverse relationships  

---

...next: [Events](MD-DDL-6-Events.md)

