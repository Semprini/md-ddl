This document is the todo list for modelling guidance.

---

# General

## AI-Friendly Modeling Practices

- How to write descriptions AI agents can understand
- Providing context without redundancy
- Using examples in descriptions
- Constraint logic clarity
- When to reference vs embed information

## Diagram Usage

- When to include diagrams
- Diagram types (domain overview, entity relationships, data flows, lifecycle)
- Mermaid vs PlantUML selection
- Keeping diagrams synchronized with definitions
- Diagram granularity

---

# Domain Guidance

## Domain Boundary Design

- How to identify domain boundaries (DDD bounded contexts vs enterprise canonical)
- When to split vs combine domains
- Signals that a domain is too large or too small
- Cross-domain relationship patterns
- Shared/Reference Data domain strategy

## Domain Ownership and Governance

- Assigning owners, stewards, and technical leads
- Single vs multiple owner models
- How ownership relates to organizational structure
- Escalation paths when domains overlap
- Accountability for cross-domain relationships

## Classification and Security Posture

- How to determine classification levels (Public, Internal, Confidential, Highly Confidential)
- PII identification and tracking
- Regulatory scope mapping (GDPR, CCPA, SOX, HIPAA, etc.)
- Default retention policies
- When to override domain defaults at entity level

## Domain Versioning Strategy

- Semantic versioning for domains (major.minor.patch)
- Breaking vs non-breaking changes
- Version compatibility across domain relationships
- Migration and deprecation strategies
- Communication patterns for version changes

---

# MD-DDL Logical Component Guidance

## Entity vs Relationship Modeling Decisions

- When a concept should be an entity vs a relationship
- When relationships need attributes (associative entities)
- Many-to-many relationship patterns
- Hierarchical relationship patterns
- Temporal relationships

## Enum Design Patterns

- When to use enums vs entities
- Simple vs structured enum values
- Enum versioning and evolution
- Domain-specific vs shared enums
- Dynamic vs static value lists

## Temporal Modeling Patterns

- Choosing temporal tracking models (current_state, valid_time, transaction_time, bitemporal)
- When entities need temporal tracking
- Point-in-time vs period modeling
- Temporal constraints and business rules
- Performance implications of temporal models

## Constraint Design

- Types of constraints (unique, not_null, check, derived)
- When to use constraints vs application logic
- Cross-entity constraint patterns
- Temporal constraints
- Constraint performance considerations
- Lifecycle-specific constraints (draft vs active vs archived)

## Event Modeling

- What qualifies as a business event
- Event granularity (fine-grained vs coarse-grained)
- Event vs entity state change
- Event sourcing patterns
- Event versioning and evolution
- Correlation and causation in event chains

## Identifier Strategy

- Primary vs alternate identifiers
- Natural vs surrogate keys
- Enterprise ID patterns
- Multi-system identity resolution
- Composite identifiers

## Inheritance and Specialization

- Modeling entity hierarchies without inheritance
- Using relationships for specialization
- Type discriminators with enums
- Polymorphic patterns
- When to split vs combine entities

# Performance Considerations

- How semantic models compile to physical schemas
- Index implications of unique constraints
- Temporal model performance
- Large array handling
- Relationship cardinality impacts

---

# Data Management

## Naming Conventions

- Natural language naming guidelines
- Consistency across domains
- Singular vs plural
- Abbreviation policies
- Handling acronyms and initialisms
- Multi-word attribute names

## Data Quality and Completeness

- Nullable vs not_null strategies
- Default values and their implications
- Data quality constraints
- Completeness scoring
- Validation rules vs quality rules

## Testing and Validation

- Validating domain definitions
- Testing constraints
- Sample data patterns
- Cross-domain validation
- Regression testing for model changes

## Documentation Best Practices

- Writing effective descriptions
- Using examples
- Linking to business processes
- Referencing policies and regulations
- Maintaining documentation currency

## Migration from Existing Models

- Mapping from relational schemas to MD-DDL
- Converting ER diagrams to entities/relationships
- Handling existing naming conventions
- Preserving legacy identifiers
- Phased migration approaches

