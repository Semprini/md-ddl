# Example Completeness — Post-Mortem Report

## Skills & References Usefulness Assessment

This report evaluates how helpful the MD-DDL agent skills and reference
files were during the creation of the Healthcare example domain and the
gap-filling of the Financial Crime example. It covers what was used, what
was missing, and what should be improved.

---

## What Was Actually Used

### During Healthcare Domain Creation

Resource | Used? | How It Helped
--- | --- | ---
Spec `3-Entities.md` | Heavily | Verified governance fields (`pii`, `access_role` as array), mutability/temporal values, attribute types, constraint syntax
Spec `5-Relationships.md` | Moderately | Confirmed relationship types, granularity options, constraint format
Spec `6-Events.md` | Moderately | Confirmed payload structure, `emitted_on` semantics, actor vs entity distinction
Spec `9-Data-Products.md` | Heavily | SLA block syntax, masking rules, `schema_type`, lifecycle fields, product class definitions
FHIR `resources-detail.md` | Heavily | Patient, Encounter, Observation, Condition, Procedure, Practitioner, Organization, Location field definitions — directly drove attribute selection
FHIR `resources.md` | Lightly | Used for resource index and canonical URL verification
FHIR `terminology.md` | Lightly | Confirmed value set names for enum creation (Encounter Status, Observation Status, etc.)
FHIR `README.md` | Lightly | Lookup process guidance (though I already knew what I needed)
Financial Crime examples | Heavily | Used as structural templates for every file type — domain.md, entity files, events, sources, products, enums

### During Financial Crime Gap-Filling

Resource | Used? | How It Helped
--- | --- | ---
Spec `3-Entities.md` | Moderately | Verified `frequently_changing` and `bitemporal` as valid values
Spec `5-Relationships.md` | Moderately | Confirmed `group` and `period` granularity semantics
Spec `9-Data-Products.md` | Moderately | SLA block structure, deprecated product lifecycle fields
Existing Financial Crime files | Heavily | Read every entity, event, product, and source to identify what was already covered vs missing

### During Simple Customer Audit

Resource | Used? | How It Helped
--- | --- | ---
Spec `3-Entities.md` | Targeted | Confirmed `pii` is boolean (not list), `access_role` is array — caught the spec drift

---

## Effectiveness Rankings

### Most Valuable Resources (Rank Ordered)

1. **Existing examples as templates** — The Financial Crime example was by far the most useful resource. Every new file followed its structural patterns. An agent with zero skill files but the Financial Crime example could still produce correct MD-DDL. This validates the "examples are AI context references" design.

2. **FHIR `resources-detail.md`** (~1,083 lines) — Provided attribute-level field definitions for 16+ FHIR resources. Without it, entity attribute selection would have required hallucination or manual FHIR spec lookup. The auto-generated format with field names, types, and descriptions maps naturally to MD-DDL attributes.

3. **Spec sections directly** (§3, §5, §6, §9) — The canonical spec files were the authority for every syntax question. Skills and reference stubs were skipped entirely in favour of reading the spec files directly.

4. **FHIR `terminology.md`** (~2,389 lines) — Confirmed enum value sets (Encounter Status, Observation Status, etc.) from authoritative FHIR definitions rather than invented values.

### Least Valuable Resources (During This Task)

1. **Skill SKILL.md files** — Not used at all during example authoring. The interview protocols in domain-scoping, entity-modelling, and relationship-events are designed for interactive user sessions, not for batch file creation. An AI creating examples already knows the domain — it doesn't need to interview itself.

2. **Reference stubs** (`references/domains-spec.md`, etc.) — These 4-line `{{INCLUDE}}` stubs were bypassed entirely. It was faster and more reliable to read the spec files directly. The `{{INCLUDE}}` macro isn't processed by the tools available.

3. **Agent Artifact skills** — Not invoked because generated physical artifacts weren't part of this phase. However, the knowledge-graph and wide-column skills are well-structured for when that work is done.

4. **ODPS alignment skill** — Irrelevant for example authoring.

---

## Gaps Found

### Gap 1: No Example Authoring Orchestration

**Problem:** There is no skill that says "given a domain concept, produce a complete MD-DDL example set." The worked-examples skill teaches users how to *read* examples, not create them. To author Healthcare, I had to mentally compose guidance from 5+ skills (domain-scoping → entity-modelling → relationship-events → source-mapping → product-design) with no orchestration.

**Impact:** Medium. An experienced agent can compose skills implicitly. But a less-capable model or a user asking Agent Ontology to "create an example like Financial Crime but for healthcare" would get inconsistent results.

**Recommendation:** Add an `example-authoring` section to the worked-examples skill or create a new skill under agent-ontology that provides a file-creation checklist:

1. Create domain.md (checklist from domain-scoping)
2. Create entity files (one per concept, checklist from entity-modelling)
3. Create enums.md (from entity-modelling enum checklist)
4. Create events/ (from relationship-events event checklist)
5. Create sources/ (from source-mapping source checklist)
6. Create products/ (from product-design checklist)

### Gap 2: `{{INCLUDE}}` Stubs Are Fragile

**Problem:** All spec reference stubs use `{{INCLUDE: ../path/to/spec.md}}`. This macro is not processed by VS Code Copilot tools, GitHub Copilot Chat, or Claude. The stubs resolve to 4 lines of nothing.

**Impact:** High. Every skill that says "load `references/entities-spec.md`" gets zero content unless the agent knows to follow the path inside the stub and load the actual spec file. The indirection adds a round-trip for no benefit.

**Recommendation:** Either:

- (a) Replace stubs with the actual spec content (accepting the maintenance cost), or
- (b) Add a fallback instruction to each skill: "If `{{INCLUDE}}` is not processed, load the file referenced in the stub directly," or
- (c) Accept that agents will read spec files directly and remove the reference stubs from skill loading instructions.

Option (c) is simplest and matches actual behaviour.

### Gap 3: BIAN v14 Data Missing

**Problem:** The standards-alignment BIAN README says "default to v14" but v14 reference data doesn't exist. Both `standards/bian/v14/` and `industry_standards/bian/v14/` contain only empty READMEs. The root-level `bo-classes.md` etc. contain v13 data.

**Impact:** Low for current examples (Financial Crime uses v13 patterns successfully). Higher for future banking/payments examples that should reference v14 semantics.

**Recommendation:** Either generate v14 references from source data or update the README to say "using v13" until v14 extraction is done.

### Gap 4: No Enum Completeness Guidance

**Problem:** When creating Healthcare enums, the decision of "how many values to include for an external standard enum" had no guidance. LOINC has 90,000+ codes, SNOMED CT has 350,000+. I chose 10 representative values each, but there's no spec or skill guidance on this.

**Impact:** Low — the "representative subset with external standard reference" pattern is obvious. But different agents might make different choices (3 values? 50? all?).

**Recommendation:** Add a note to the enumerations spec or entity-modelling skill: "For external standard enums, include a representative subset (5–15 values) sufficient to demonstrate the pattern, with a `standard` reference field pointing to the authoritative source."

### Gap 5: Event Payload Format Inconsistency

**Problem:** Existing Financial Crime events used a list-of-single-key-dict format (`- event timestamp:` with nested type/description). New Healthcare events used a flat dict format (`event_timestamp:` at the same level as type/description). The spec (`6-Events.md`) doesn't enforce one format over the other.

**Impact:** Medium. Both parse as valid YAML, but the inconsistency between examples is confusing.

**Recommendation:** Pick one format in the spec's Events section and mark it as the canonical pattern. The flat dict format is cleaner and more consistent with entity attribute YAML.

---

## Overall Assessment

Rating | Area
--- | ---
Excellent | FHIR reference data pipeline (raw JSON → extracted markdown → agent-ready references)
Excellent | Spec sections as direct authoring references
Excellent | Financial Crime example quality as a template
Good | Skill structure and progressive disclosure design
Good | BIAN reference data (v13)
Needs work | `{{INCLUDE}}` stub mechanism — adds indirection without value in current tooling
Needs work | Missing orchestration for multi-file example creation
Minor | Enum subset guidance, event payload format standardisation, BIAN v14 gap

### Key Insight

**The examples themselves are the most powerful "skill" in the system.** A well-structured example with current spec patterns teaches an agent more effectively than any amount of procedural guidance. The skills are valuable for interactive modelling sessions with users, but for batch artifact creation, the spec + examples are sufficient.

This suggests the investment priority should be: **(1) keep examples current with the spec** > (2) improve reference data pipelines > (3) refine skills.
