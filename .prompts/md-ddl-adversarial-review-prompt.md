# MD-DDL Adversarial Review Prompt

You are conducting a critical adversarial review of the md-ddl project. Your job
is to find weaknesses, gaps, contradictions, and failure modes — not to confirm
that things work.

**Evaluation stance:** You will be judged on the quality and specificity of your
criticisms, not on your supportiveness. An adversarial review that finds no issues
is itself a failure. If you cannot find genuine problems in an area, state what
aspects you lack the expertise to evaluate rather than giving a pass.

Write the findings to the `review.md` file.

---

## Before you begin — load context

Read these files first:

1. `md-ddl-specification/1-Foundation.md` — core principles
2. `md-ddl-specification/MD-DDL-Complete.md` — full spec (skim for breadth)
3. All 5 agent files: `agents/agent-guide/AGENT.md`, `agents/agent-ontology/AGENT.md`,
   `agents/agent-artifact/AGENT.md`, `agents/agent-architect/AGENT.md`,
   `agents/agent-governance/AGENT.md`
4. `examples/Financial Crime/domain.md` — the reference example
5. Contributor instructions — `.github/copilot-instructions.md` or `CLAUDE.md`

---

## Adversarial Review Protocol

For each area, ask these questions. Do not skip uncomfortable findings.

### 1. Specification Gaps — What Can't MD-DDL Express?

Identify real-world data modelling scenarios that MD-DDL cannot express or handles
awkwardly. For each gap:

- Describe the scenario concretely (not abstractly)
- Show what a practitioner would attempt to write
- Show where the spec fails or forces a workaround
- Assess the severity: is this a showstopper, a friction point, or a minor gap?

**Specific areas to probe:**

- Polymorphic relationships (an entity related to one of several types)
- Recursive/self-referential relationships (org hierarchies, graph structures)
- Computed/derived attributes that depend on other entities
- Multi-tenancy and tenant-specific model variations
- Schema evolution and backward compatibility
- Complex temporal patterns (bi-temporal with multiple valid-time ranges)
- Array/collection attributes (a person with multiple phone numbers)
- Conditional constraints (field X is required only when field Y = Z)

### 2. Agent Prompt Failure Modes — When Would Agents Produce Wrong Output?

For each agent, identify specific inputs or scenarios where the agent's prompt
architecture would cause incorrect output. Not theoretical — concrete.

- What user phrasing would cause the wrong skill to load?
- What valid request would load no skill at all?
- Where would the behaviour mode transitions produce awkward or incorrect output?
- What happens if the user provides conflicting requirements?
- What happens when the user knows more than the agent about their domain?
- Where do the non-negotiable rules conflict with each other?

Include Agent Guide in this analysis — probe whether onboarding flows correctly
route users to specialist agents, and whether the Guide's demonstrations could
be mistaken for production artifacts.

### 3. Cross-Agent Handoff Failures — Where Do Things Fall Through?

Simulate a handoff that goes wrong. Identify:

- What context is lost between agents (stateless sessions)?
- What happens when Agent Governance flags a gap that Agent Ontology disagrees with?
- What happens when a product design reveals missing entities but the user doesn't
  switch to Agent Ontology?
- Where do circular handoffs occur (A defers to B, B defers back to A)?
- What happens when Agent Guide hands off to a specialist but the user isn't ready?

### 4. Example Quality — What's Wrong with the Examples?

The Financial Crime example is the project's quality benchmark. Find its weaknesses:

- Are there entities that should exist but don't?
- Are there relationships that are modelled incorrectly?
- Are governance metadata values plausible for a real financial crime domain?
- Does the temporal tracking strategy make sense for each entity?
- Are the events comprehensive for the domain's business processes?
- Are the source mappings and transformations realistic?
- Are the data products well-designed for real consumer needs?

Also probe the other examples (Healthcare, Telecom, Retail Sales, Retail Service,
Brownfield Retail, Simple Customer):

- Do industry-specific examples use accurate industry standards references?
- Does the Brownfield Retail example genuinely demonstrate the adoption maturity
  model from Section 10, or is it superficial?
- Are newer examples at the same quality level as Financial Crime, or are there
  visible gaps?

### 5. Validation Philosophy Robustness

The standard explicitly rejects traditional linting above syntax level (see `1-Foundation.md` "Validation Model"). Probe whether this philosophy holds up in practice:

- **What happens when an organisation uses non-standard vocabulary?** If a domain uses `phi: true` instead of `pii: true`, does any agent prompt reject it or flag it as an error? If so, that is a prompt bug contradicting the stated philosophy.
- **Is there hidden rigidity in agent prompts?** Search agent SKILL.md files for "must have", "required", "error if missing", "not valid" language. Identify any instance where this language applies to convention or quality concerns rather than syntax-level failures.
- **Pre-flight check scope creep risk.** The spec defines exactly 5 pre-flight checks. What prevents a sixth check being added casually? Is there a mechanism (spec version bump requirement) that makes scope expansion a deliberate decision rather than a silent accumulation? If the mechanism exists only as text in the spec, how would a contributor know to check?
- **Agents as quality layer — can they actually deliver?** The spec defers Levels 2–5 entirely to agents. Is there any category of structural gap (e.g., completely missing `governance:` block) where no agent would currently catch it? Is the handoff between pre-flight checks and agent review gapless?
- **Vocabulary deviation pathway.** When an agent flags "potential spec vocabulary gap", where does that signal go? Is there a community contribution mechanism? If not, the feedback loop the philosophy depends on does not yet exist.

### 6. Specification Internal Contradictions

Search for rules in the spec that contradict each other or create ambiguity:

- Where two spec sections give different guidance on the same topic
- Where a rule is stated at one level of specificity in one section and a different
  level in another
- Where the spec is silent on something that a rule implies should be addressed
- Where examples in the spec demonstrate patterns that conflict with stated rules

### 7. Scalability Stress Test

Evaluate how the standard and agents would handle scale:

- A domain with 100+ entities — does the domain file format break?
- A domain with 20+ source systems — does the source layer become unmanageable?
- An organisation with 50+ domains — is cross-domain referencing workable?
- A single entity with 50+ attributes — does the YAML format scale?
- 10+ data products from a single domain — does the product layer scale?

### 8. Governance Model Stress Test

Push the governance model to its limits:

- A domain operating under 5+ conflicting jurisdictions
- An entity where every attribute is PII with different retention requirements
- A data product that must satisfy both GDPR right-to-erasure and SOX 7-year retention
- A source system that feeds PII into a domain that doesn't declare PII handling
- Governance metadata that is technically valid but operationally meaningless

### 9. Adoption Model Stress Test

Probe the brownfield adoption model (Section 10):

- What happens when baseline capture reveals a schema too messy to map cleanly?
- Does the maturity ladder (documented → mapped → governed → canonical) reflect
  real-world adoption patterns, or does it impose an unrealistic linear progression?
- When baseline files are superseded by canonical entities, is the transition
  traceable or does it create orphaned references?
- Can the adoption model handle partial adoption — some domains canonical,
  others still at baseline — without inconsistency?

### 10. Where Would AI Evaluation Miss the Problem?

This is the meta-question. For each finding above, annotate:

- Would a standard AI evaluation (using the evaluation prompt) have found this?
- If not, why not?
- What would need to change in the evaluation methodology to catch it?

---

## What You Must Not Do

- Do not soften findings. If something is broken, say it's broken.
- Do not offer mitigating context. Present the problem; the team decides whether
  it matters.
- Do not suggest fixes inline. Collect all findings first. Fixes come later.
- Do not evaluate aspects you cannot meaningfully assess. State your limits.
- Do not claim to be an expert in regulatory compliance, healthcare informatics,
  or any specific industry domain. State facts you can verify from the loaded
  files and flag where domain expertise is needed.

---

## Report Format

```markdown
## MD-DDL Adversarial Review — [date]
**Spec version:** [version from 1-Foundation.md]

### What I Cannot Evaluate
[Explicit list of aspects outside AI's competence for this review. Be honest.]

### Critical Findings
Issues that would cause incorrect output, regulatory risk, or user harm.

[finding: severity — file path — description — why AI evaluation would miss this]

### Structural Weaknesses
Issues that are not currently broken but represent design fragility.

[finding: area — description — stress scenario that would break it]

### Missing Capability
Things practitioners would expect that MD-DDL cannot do.

[gap: scenario — what the practitioner would attempt — where the standard fails]

### Specification Contradictions
Places where the spec disagrees with itself.

[contradiction: section A vs section B — what each says — which should win]

### Agent Failure Modes
Concrete scenarios where agent prompts would produce wrong output.

[failure: agent — user input — expected behaviour — actual behaviour — root cause]

### Evaluation Methodology Gaps
What the existing review and evaluation prompts would miss.

[gap: what would be missed — why — proposed mitigation]
```
