# Comprehensive Examples Plan

## User decisions

- Bounded Context: YES — two small domains defining 'Customer' differently
- Industry: Telecom (TM Forum, full-size) + Retail/E-Commerce (greenfield, minimal)
- Cross-domain: Both — one realistic (connecting existing), one minimal (purpose-built pair)
- Size: Mix — one full-size Telecom + several minimal focused examples
- Greenfield: Retail/E-Commerce — natural Bounded Context contrast with Financial Crime
- Bounded Context approach: Two small domains defining 'Customer' differently

## Modelling permutations to cover

1. Canonical vs Bounded Context strategy
2. Cross-domain consumer-aligned products
3. Associative entities (M:N bridges)
4. All mutability types demonstrated
5. All temporal types demonstrated
6. All granularity types in multiple contexts
7. Masking strategies (hash, redact, year-only, truncate, tokenize, null)
8. Deprecated/Retired product lifecycle
9. Standards: BIAN (done), FHIR (done), TM Forum (new), No-standard (new)
10. Governance profiles: AML/GDPR (done), HIPAA (done), PCI-DSS (new?), minimal (new)

## TM Forum reference data

- 782 indexed entities, 46 detailed, full JSON schemas in v4/schemas/
- Core entities: Individual, Organization, PartyRole, Customer, BillingAccount, ProductOrder, ProductOffering, Service, ServiceOrder, NetworkProduct
- Telecom-specific: prepaid/postpaid, SLA/SLO, subscriber vs customer

## Plan summary (presented to user)

- Phase 1: Telecom (full-size, 10-12 entities, TM Forum, PCI-DSS, associative, triggers/assigned_to/supersedes, dimensional+wide-column generation, cross-domain product with Financial Crime)
- Phase 2: Retail Sales + Retail Service (minimal, ~4 entities each, BoundedContext, no-standard, greenfield, cross-domain customer-360)
- Phase 3: Masking across Telecom + Retail, deprecated product lifecycle in Retail
- Phase 4: Coverage matrix update (7 columns), verification

## New features exercised

- existence: associative (Subscription in Telecom)
- modelling_strategy: BoundedContext (both Retail domains)
- cross_domain products (2: Telecom+FinCrime, Retail Sales+Service)
- All 6 masking strategies across 2 products
- Relationship types: assigned_to, triggers, supersedes (Telecom)
- PCI-DSS regulatory scope (Telecom)
- No-standard greenfield (Retail)
- schema_type: dimensional, wide-column generation (Telecom)
- Deprecated product lifecycle (Retail)
