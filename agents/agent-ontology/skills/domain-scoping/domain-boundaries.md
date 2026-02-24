# **Canonical Definitions and Domain Boundaries**

## **The Canonical Definition Challenge**

In traditional enterprise data modeling, there's often a push for **single canonical definitions** - one "Customer" entity that serves the entire organization. However, this approach has significant challenges:

**Problems with enterprise-wide canonical definitions:**

- **Semantic overload** - A "Customer" in Sales vs Support vs Billing has different meanings and different required attributes
- **Coordination overhead** - Changes require consensus across all domains, slowing evolution
- **Coupling** - Domains become tightly coupled through shared definitions
- **Lowest common denominator** - The canonical definition becomes bloated with every domain's needs, or too minimal to be useful

## Knowledge Graph Implications

### Both Approaches Work

MD-DDL and the resulting knowledge graph support both:

- **Single canonical definitions** - Simpler structure, requires enterprise coordination
- **Domain-driven definitions** - Explicit boundaries, independent evolution

### Complexity Trade-offs

**Single Canonical:**

- Simpler graph structure (fewer nodes and edges)
- Implicit semantic complexity (hidden in attributes and rules)
- Coordination overhead (all domains must agree)
- Harder to govern cross-domain data flows

**Domain-Driven:**

- More explicit graph structure (more nodes, explicit relationships)
- Semantic clarity (each node has clear meaning)
- Independent evolution (domains change separately)
- Easier to govern cross-domain data flows

### Knowledge Graph Benefits of Domain-Driven

If you choose domain-driven definitions, the knowledge graph provides:

1. **Clear domain boundaries** - Visualize and query domain structure
2. **Cross-domain lineage** - Track data flows between domains
3. **Governance at boundaries** - Apply policies to cross-domain relationships
4. **Independent versioning** - Track domain evolution separately
5. **Impact analysis** - See what changes affect which domains

## Choosing Your Approach

Consider domain-driven when:

- Different parts of the organization need to evolve independently
- The same concept has genuinely different meanings in different contexts
- Governance requires tracking cross-domain data flows
- Your organization follows Domain-Driven Design principles

Consider single canonical when:

- The concept is truly universal across the organization
- Coordination overhead is acceptable
- You have strong enterprise data governance
- The organization is small enough for consensus-driven change

### Hybrid Approach

Most organizations use a hybrid:

- **Shared reference data** - Countries, currencies, codes (single canonical)
- **Domain-specific entities** - Customer, Product, Order (domain-driven)
- **Cross-domain relationships** - Explicit integration points

The knowledge graph handles this naturally - some nodes are shared, some are domain-specific, relationships connect them.
