---
name: inheritance
description: Design entity inheritance hierarchies. Use when modeling entities that share common attributes or when user mentions "types of" or "kinds of" something.
---

# Inheritance Design

**📚 Detailed Guidance**: [Inheritance Patterns](./inheritance-patterns.md)

## When to Create Abstract Parent

Create parent when ≥2 children share >50% attributes and are semantically related.

## Common Industry Patterns

**Banking** (BIAN):
- Party → Individual, Legal Entity
- Party Role → Customer, Merchant, Creditor

**Insurance** (ACORD):
- Party → Person, Organization
- Coverage → Auto Coverage, Property Coverage, Life Coverage

**Telecom** (TM Forum):
- Party → Individual, Organization
- Product → Mobile Product, Broadband Product, TV Product

**Healthcare** (FHIR):
- Resource → Patient, Practitioner, Organization

## Syntax
[Summary and detail syntax examples]

## When to Load Detailed Guidance

Load [Inheritance Patterns](./inheritance-patterns.md) when:
- Dealing with >2 level hierarchies
- Need industry-specific pattern examples
- Handling abstract vs concrete questions
- Discriminator design questions