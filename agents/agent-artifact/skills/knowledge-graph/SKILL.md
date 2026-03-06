---
name: knowledge-graph
description: Use this skill when the user asks to generate a knowledge graph, graph database schema, Cypher DDL, or Neo4j model from an MD-DDL domain. Also use when the user wants to realize MD-DDL entities, relationships, events, and enums as labeled property graph structures.
---

# Skill: Knowledge Graph Generation

Covers translation of MD-DDL conceptual and logical models into labeled property graph structures expressed as Neo4j Cypher. The output is a complete graph schema — node labels, relationship types, property keys, constraints, and indexes — plus seed data for enums and reference entities.

MD-DDL was designed with a Knowledge Graph as its semantic runtime. This skill makes the implicit graph structure explicit and deployable.

## Load First

- `../../agent-ontology/skills/entity-modelling/SKILL.md`
- `../../agent-ontology/skills/entity-modelling/conceptual-to-physical-realisation.md`
- `../../agent-ontology/skills/relationship-events/SKILL.md`
- `../../agent-ontology/skills/standards-alignment/SKILL.md` (when industry-standard domains apply)

---

## Core Mapping Rules

### Entities → Nodes

Every entity in the domain becomes a node label. The label uses PascalCase derived from the natural-language entity name.

MD-DDL concept | Graph realization
--- | ---
Entity heading | Node label (PascalCase: `Party`, `ContactAddress`, `PartyRole`)
Entity attributes | Node properties (camelCase: `legalName`, `partyIdentifier`)
`identifier: primary` attribute | Uniqueness constraint on the label
`identifier: alternate` or `natural` | Additional unique constraint or index
`type` values | Property type annotations in schema comments
`pii: true` attributes | Tagged with `:PII` metadata label or property-level annotation

#### Naming Convention

- Node labels: PascalCase, no spaces, no underscores (`PartyRole`, `ContactAddress`, `ExchangeRate`)
- Property keys: camelCase, no spaces (`partyIdentifier`, `legalName`, `riskRating`)
- Relationship types: UPPER_SNAKE_CASE (`ASSUMES_ROLE`, `HAS_CONTACT_ADDRESS`, `HOLDS_ACCOUNT`)

### Inheritance → Label Hierarchies

MD-DDL inheritance (`extends:`) maps to multi-label nodes in the graph.

Pattern | Graph realization
--- | ---
`Person extends Party` | Person nodes carry both `:Person` and `:Party` labels
Abstract parent entity | No standalone nodes with only the parent label are created directly; the label exists only on specialized nodes
Concrete parent entity | Parent label may appear on nodes that are not further specialized

Cypher example:

```cypher
// Creating a Person (inherits Party)
CREATE (p:Party:Person {
  partyIdentifier: $partyId,
  legalName: $legalName,
  firstName: $firstName,
  lastName: $lastName,
  dateOfBirth: date($dob)
})
```

Inherited attributes from the parent entity become properties on the node alongside the child entity's own attributes. The full attribute set is the union of the parent chain.

### Relationships → Graph Relationships

Every MD-DDL relationship becomes a typed graph relationship.

MD-DDL property | Graph realization
--- | ---
Relationship heading | Relationship type (UPPER_SNAKE_CASE)
`source` | Start node label
`target` | End node label
`type` (owns/has/references etc.) | Encoded as the relationship type name, or as a `semanticType` property when the heading already captures the verb
`cardinality` | Not enforced structurally in the graph (graphs are naturally multi-valued); documented as a schema comment
`granularity` | Property on the relationship when not `atomic`
`ownership` | Determines which node is the start of the relationship
Relationship `constraints` | Translated to validation queries or trigger logic

#### Relationship Type Derivation

Derive the relationship type from the relationship heading:

Heading | Relationship type
--- | ---
Customer Holds Account | `HOLDS_ACCOUNT`
Party Assumes Roles | `ASSUMES_ROLE`
Contact Address References Address | `REFERENCES_ADDRESS`
Transaction Has Debtor | `HAS_DEBTOR`

Strip the source entity name from the heading, then UPPER_SNAKE_CASE the remainder.

#### Relationship Properties

Relationships with `granularity: period` or temporal constraints carry temporal properties:

```cypher
-[:ASSUMES_ROLE {validFrom: date('2024-01-01'), validTo: date('2025-12-31'), isCurrent: true}]->
```

Relationship constraints translate to Cypher property conditions or validation queries.

### Events → Event Nodes

Events become nodes connected to their actor and entity by typed relationships.

MD-DDL property | Graph realization
--- | ---
Event heading | Node label (PascalCase) + `:DomainEvent` label
`actor` | `TRIGGERED_BY` relationship from event to actor node (or label)
`entity` | `AFFECTS` relationship from event to entity node (or label)
`emitted_on` | `emittedOn` property (array of trigger conditions)
`business_meaning` | `businessMeaning` text property
`downstream_impact` | `downstreamImpact` array property
Event `attributes` | Properties on the event node
Event `constraints` | Validation queries

Cypher example:

```cypher
CREATE (e:DomainEvent:CustomerOnboarded {
  timestamp: datetime($ts),
  businessMeaning: 'New Customer relationship established'
})
WITH e
MATCH (actor:Party {partyIdentifier: $actorId})
MATCH (entity:Customer {customerNumber: $customerId})
CREATE (e)-[:TRIGGERED_BY]->(actor)
CREATE (e)-[:AFFECTS]->(entity)
```

### Enums → Constraint Values or Reference Nodes

Enum realization depends on complexity:

Enum shape | Graph realization
--- | ---
Simple value list | Property type constraint (Cypher `CHECK` or application-level validation)
Dictionary with metadata | Reference nodes with `:Enum` and `:<EnumName>` labels, connected to their values

Simple enum (constraint approach):

```cypher
// Schema-level: document allowed values as a comment or application constraint
// PartyStatus property on :Party nodes must be one of: ['Active', 'Inactive', 'Under Review']
```

Dictionary enum (reference node approach):

```cypher
CREATE (e:Enum:LoyaltyTier {name: 'Bronze', description: 'Entry level tier', score: 1})
CREATE (e:Enum:LoyaltyTier {name: 'Silver', description: 'Standard tier', score: 2})
CREATE (e:Enum:LoyaltyTier {name: 'Gold', description: 'Premium tier', score: 3})
```

Default: use simple property constraints unless the enum carries metadata beyond labels.

---

## Temporal Realization

MD-DDL temporal tracking translates to specific property patterns on nodes and relationships.

`temporal.tracking` | Graph properties
--- | ---
`valid_time` | `validFrom`, `validTo` (date/datetime)
`transaction_time` | `recordedAt`, `supersededAt` (datetime)
`bitemporal` | All four properties above
`point_in_time` | `eventTimestamp` (datetime), optional `sequenceNumber`

For `slowly_changing` entities with `valid_time`, generate versioned node patterns:

```cypher
// Current version
MATCH (p:Party {partyIdentifier: $id, isCurrent: true})

// Historical query
MATCH (p:Party {partyIdentifier: $id})
WHERE p.validFrom <= date($asOf) AND (p.validTo IS NULL OR p.validTo > date($asOf))
```

---

## Existence and Mutability

These MD-DDL properties inform graph schema annotations, not structural differences (unlike relational models, graph nodes are structurally uniform).

`existence` | Graph guidance
--- | ---
`independent` | Standalone node; guaranteed to have a uniqueness constraint on its identifier
`dependent` | Node that should always be connected to at least one parent via a relationship; document orphan-detection query
`associative` | Consider whether to model as a relationship with properties or as an intermediate node; prefer intermediate node when the association carries more than two properties or has its own temporal lifecycle

`mutability` | Graph guidance
--- | ---
`immutable` | Node properties are write-once; document as a schema annotation
`append_only` | New nodes only; no property updates on existing nodes
`slowly_changing` | Versioned nodes with `isCurrent` flag and valid-time properties
`frequently_changing` | Standard mutable node; consider indexing frequently-queried properties
`reference` | Low-churn reference node; candidate for eager loading / caching

---

## Schema Output: Constraints and Indexes

Generate Cypher constraint and index statements for every entity.

### Uniqueness Constraints

One per `identifier: primary` attribute:

```cypher
CREATE CONSTRAINT party_pk IF NOT EXISTS
FOR (n:Party) REQUIRE n.partyIdentifier IS UNIQUE;
```

### Additional Indexes

- `identifier: alternate` or `natural` → unique constraint
- Attributes used in relationship constraints → composite or single-property index
- Temporal properties (`validFrom`, `validTo`) → range index for point-in-time queries
- Enum properties with frequent filtering → index

### Node Key Constraints (when supported)

For entities with composite identifiers, use node key constraints:

```cypher
CREATE CONSTRAINT contact_address_pk IF NOT EXISTS
FOR (n:ContactAddress) REQUIRE (n.contactAddressIdentifier) IS NODE KEY;
```

---

## Governance Metadata

Domain-level and entity-level governance translates to graph metadata:

- `classification` → property on node or relationship, or metadata label (`:Confidential`, `:HighlyConfidential`)
- `pii: true` → `:PII` label on the node, or `pii: true` property on individual attributes (document which properties are PII in schema comments)
- `retention` → schema annotation; generation of TTL-based cleanup queries when the platform supports them
- `regulatory_scope` → metadata properties on domain-level nodes or as a `:RegulatoryScope` reference structure

---

## Output Contract

When producing a knowledge graph schema, always include:

1. **Schema summary** — node labels, relationship types, and their mappings to MD-DDL concepts
2. **Constraint and index DDL** — Cypher `CREATE CONSTRAINT` and `CREATE INDEX` statements
3. **Node creation templates** — parameterized Cypher `CREATE` statements for each entity, showing full property sets including inherited attributes
4. **Relationship creation templates** — parameterized `MATCH`/`CREATE` patterns for each declared relationship
5. **Event node templates** — parameterized patterns for each domain event
6. **Enum seed data** — `CREATE` statements for dictionary enums; constraint documentation for simple enums
7. **Validation queries** — Cypher queries that enforce MD-DDL constraints (relationship cardinality checks, orphan detection for dependent entities, temporal consistency checks)
8. **Assumptions and open questions** — any ambiguities in the conceptual model that affected graph design decisions

---

## Decision Checklist

Before finalizing a knowledge graph schema, confirm:

- [ ] Every entity has a node label and uniqueness constraint
- [ ] Inheritance hierarchies use multi-label nodes with full attribute union
- [ ] Every declared relationship has a typed graph relationship with correct start/end labels
- [ ] Temporal properties match declared `temporal.tracking` values
- [ ] Enum realization strategy is explicit (property constraint vs reference node)
- [ ] Governance metadata is represented (classification, PII, retention)
- [ ] Event nodes carry `:DomainEvent` label and are connected to actor/entity
- [ ] Associative entities are realized appropriately (intermediate node vs relationship properties)
- [ ] Dependent entities have orphan-detection validation queries
- [ ] All constraint and index statements use `IF NOT EXISTS` for idempotency
