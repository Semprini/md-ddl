---
name: worked-examples
description: Use when the user asks to see an example, says "walk me through" or "show me how [concept] looks in practice", mentions an example domain (Simple Customer, Financial Crime, Healthcare, Telecom, Retail, Brownfield Retail), or wants to see how a complete MD-DDL model fits together.
---

# Skill: Worked Examples

Teach by walking through the real example domains in `examples/`. Read the files as you
go rather than describing them from memory. The examples change, and their details are
the lesson.

## Choosing an Example

`examples/README.md` lists every example with its complexity, and includes a feature
coverage matrix showing which spec features each one uses. Use it to pick the example
for the user's question:

- **First look:** Simple Customer. The smallest complete model: `domain.md` plus `details.md`.
- **Production-quality reference:** Financial Crime. Inheritance, governance, BIAN
  alignment, sources, data products, lifecycle history, synthetic data.
- **Healthcare and FHIR:** Healthcare. Bitemporal and transaction-time patterns, a
  knowledge-graph product.
- **Specific features:** find them in the coverage matrix (associative entities are in
  Telecom and Retail Sales; bounded contexts in Retail Sales and Retail Service).
- **Brownfield adoption:** Brownfield Retail (below).

---

## Walking Through an Example

1. **Big picture.** Open `domain.md`: description, metadata (ownership, governance,
   regulatory scope), overview diagram, and summary tables. The domain file is a table
   of contents, and detail lives in linked files.
2. **One entity.** Let the user choose, or suggest one that suits their archetype:
   inheritance for modellers, PII and governance for stewards, constraints and temporal
   tracking for engineers, regulatory scope for compliance. Walk through the heading
   hierarchy, the YAML (attributes, `existence`, `mutability`, `temporal`, governance),
   and the diagram.
3. **A design decision.** This teaches how to *think* in MD-DDL. Check the decision
   against the files before presenting it. Examples:
   - Simple Customer: Party Role is abstract and exists only to be specialised (Customer
     extends it). Loyalty Tier is an enum because it has no attributes or lifecycle of
     its own. Customer Preference is `existence: dependent` because it can't exist
     without its customer.
   - Financial Crime: Party is abstract, with Person and Company as concrete subtypes,
     because a party is always one or the other and each adds different attributes.
     Payer, Payee, and Payment Initiator are Party Role specialisations, because the same
     party plays different roles in different transactions. Transaction is
     `existence: dependent` and `append_only` with transaction-time tracking: a
     settled transaction is never modified. The file doesn't state why it's dependent.
     Ask the user what they would choose and why, which makes a good discussion.

   Then ask whether the user's domain has a similar either/or choice.
4. **Connections.** Show how the entity links to the rest: relationship YAML
   (cardinality, identifying or not), events that affect it, data products that publish
   it (`data_products/`), and sources that feed it, including transform detail and
   worked examples where present (`sources/`).
5. **Their own concept.** Invite the user to describe a concept from their domain and
   sketch it in MD-DDL, marked as a demonstration. When they're ready to build it for
   real, offer a drafted opening request for Agent Ontology.

If the user would rather explore than follow a sequence, jump straight to what they ask
for: inheritance, governance metadata, a data product, source mapping, an event. Use the
coverage matrix to find the best instance.

---

## Brownfield Retail: From Star Schema to Declarative MD-DDL

`examples/Brownfield Retail/` shows the adoption journey for a retail domain that
starts from a Snowflake star schema. Walk it phase by phase, reading the files:

1. **Documented (Level 1).** `baselines/` records the existing state: dimensional tables
   (`fact_sales`, `dim_product`, `dim_store`), an ETL pipeline, and Collibra catalogue
   metadata. Each file has a `baseline:` metadata block, type-specific YAML, and a
   free-form body of business rules and known issues.
2. **Mapped (Level 2).** `entities/` holds canonical entities derived from the baselines
   (Sale, not `fact_sales`), with natural-language attributes and audit columns dropped.
   `sources/pos-system/` carries the lineage from baseline fields to canonical attributes.
3. **Governed (Level 3).** Classification, PII, retention, regulatory scope, and a
   passing domain review.
4. **Declarative (Level 3 → 4).** Agent Artifact regenerates the star schema from the
   canonical model and reconciles it against the baseline. The differences are either
   intentional improvements or prompts to update the model. Superseded baselines are
   marked `status: superseded`.

Check the domain's `adoption` metadata for its current maturity rather than assuming it.
