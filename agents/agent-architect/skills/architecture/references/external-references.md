# External References

Third-party articles and framework discussions that provide context for positioning
Data Autonomy relative to other architectural approaches.

## Source Material

### Bounded Context — Martin Fowler (2014)

Foundational DDD concept that Data Autonomy builds upon. Each domain is a bounded
context with its own unified model; inter-domain communication happens through
explicit gateways, not shared databases.

{{INCLUDE: ../../../../../references/architecture/bounded_context.md}}

### How to Move Beyond a Monolithic Data Lake to a Distributed Data Mesh — Zhamak Dehghani (2019)

The article that coined "Data Mesh." Shares domain orientation and data-as-product
thinking with Data Autonomy. Data Autonomy predates and extends it with canonical
models, key mapping, model-driven generation, and polyglot persistence.

{{INCLUDE: ../../../../../references/architecture/data_lake_to_data_mesh.md}}

### BIAN Coreless Banking and Data Autonomy — Discussion

Analysis of how BIAN's industry-standard canonical vocabulary for banking
complements Data Autonomy's implementation architecture. BIAN provides the "what"
(canonical shape); Data Autonomy provides the "how" (translation, key mapping,
CTL, governance).

{{INCLUDE: ../../../../../references/architecture/BIAN Coreless Banking vs Data Autonomy.md}}

## How These References Support the Architecture Skill

Reference | Use in Teach mode | Use in Discuss mode
--- | --- | ---
Fowler — Bounded Context | Explain how Data Autonomy's domain model inherits and extends DDD bounded contexts | Position canonical models as the practical implementation of DDD's strategic design
Dehghani — Data Mesh | Explain the shared heritage and where Data Autonomy adds implementation specifics | Compare frameworks honestly; acknowledge Data Mesh strengths while articulating what Data Autonomy adds
BIAN — Coreless Banking | Explain how industry standards provide the canonical vocabulary | Position the combination for banking organisations; BIAN for service vocabulary + Data Autonomy for data architecture
