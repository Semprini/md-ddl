# MD-DDL Layered Review Process

This document defines the multi-layer review process for the MD-DDL project.
Each layer uses a different review lens and should be run in a separate AI
conversation to prevent cross-contamination between evaluation stances.

---

## Why Layered Review?

A single AI evaluation session is vulnerable to:

- **Sycophancy bias** — AI defaults to approval over criticism
- **Shared blind spots** — generating and evaluating AI share training-data gaps
- **Anchoring** — findings from early in a session bias later assessment
- **Surface pattern matching** — structural conformance is mistaken for quality
- **Self-reinforcing loops** — each review round narrows the lens

Layered review mitigates these by forcing different evaluation stances in
separate sessions, cross-referencing findings between layers, and explicitly
declaring what each layer cannot assess.

---

## The Three Layers

### Layer 1 — Structural Review (Boolean / Mechanical)

**Prompt:** `.prompts/md-ddl-review-prompt.md`

**Lens:** "Is the repository internally consistent?"

**What it checks:**

- Version consistency across all files
- Rule duplication — rules stated in more than one place
- Dead references — links that point to nonexistent files or anchors
- Example currency — examples match the current spec version
- File structure — actual disk layout matches documented layout
- Agent boundary compliance — no capability overlap between agents
- Skill index accuracy — triggers match skills that exist on disk

**What it cannot check:**

- Whether rules are correct (only that they are consistently stated)
- Whether examples are semantically accurate (only that they use current syntax)
- Whether agents would produce good output (only that their structure is sound)

**AI strength:** High. These are objectively verifiable checks.

**Run frequency:** Every spec version bump or significant file change.

---

### Layer 2 — Adversarial Review (Find What's Wrong)

**Prompt:** `.prompts/md-ddl-adversarial-review-prompt.md`

**Lens:** "What would break, fail, or mislead?"

**What it checks:**

- Specification gaps — real-world scenarios the standard cannot express
- Agent failure modes — inputs that would cause wrong skill loading or wrong output
- Cross-agent handoff failures — context loss, circular handoffs
- Example weaknesses — missing entities, incorrect relationships, implausible governance
- Specification contradictions — conflicting rules between sections
- Scalability limits — where the format breaks under load
- Governance model stress — multi-jurisdiction conflicts, PII edge cases

**What it cannot check:**

- Whether the domain model matches real-world business processes
- Whether regulatory requirements are factually correct
- Whether the standard *should* express a particular scenario (that's a design decision)

**AI strength:** Moderate. AI can find structural failure modes but not semantic ones.
The adversarial framing helps but doesn't eliminate sycophancy entirely.

**Run frequency:** Before major releases. Ideally run by a different AI model than
the one that produced the content being reviewed.

---

### Layer 3 — Stakeholder Simulation (Fitness for Purpose)

**Prompt:** `.prompts/md-ddl-evaluation-prompt.md`

**Lens:** "Would real people find this useful?"

**What it checks:**

- Agent effectiveness per persona and scenario (skill loading, behaviour modes, output quality)
- Standard expressiveness, completeness, and learnability per scenario
- Cross-agent workflow coherence (handoff clarity, context continuity)
- Standard critique dimensions (conceptual completeness, learning curve, governance
  integration, industry alignment, scalability, physical generation gap, source
  coverage, model evolution)
- Stakeholder adoption likelihood

**What it cannot check:**

- Whether simulated persona reactions match real stakeholder reactions
- Whether the learning curve assessment reflects actual onboarding difficulty
- Whether adoption verdicts predict real adoption
- Whether governance metadata passes actual regulatory review

**AI strength:** Low-to-moderate. AI *simulates* stakeholder reactions through pattern
matching, not empathy or experience. Treat scores as directional signals, not measurements.

**Run frequency:** Every major release. Best combined with actual user feedback.

---

## Cross-Layer Protocol

### Running Order

Always run layers in order: 1 → 2 → 3. Each layer builds on the previous:

1. **Layer 1** establishes structural baseline — what's broken mechanically?
2. **Layer 2** receives Layer 1's findings and probes deeper — what would fail in use?
3. **Layer 3** receives Layers 1–2's findings and evaluates — despite the issues found, how well does this serve users?

### Cross-Referencing

Each layer's report should reference findings from previous layers:

- Layer 2 should note: "Layer 1 identified [issue]. This adversarial review confirms/extends/disagrees."
- Layer 3 should note: "Layers 1–2 identified [issues]. These affect stakeholder scenarios [X, Y, Z] as follows..."

### Disagreement as Signal

When layers disagree, that's where the most valuable insight lives:

- Layer 1 says "consistent" but Layer 2 finds a contradiction → investigate
- Layer 2 says "failure mode" but Layer 3 says "works for users" → the failure mode may be theoretical
- Layer 3 says "high score" despite Layer 2 findings → sycophancy bias may be operating

### Model Diversity

For maximum value, run different layers with different AI models:

- Layer 1 (structural) can run on any model — it's mechanical
- Layer 2 (adversarial) benefits from a model known for critical thinking
- Layer 3 (stakeholder) benefits from a model with broad domain knowledge

Cross-model disagreement is more informative than within-model consistency.

---

## Anti-Sycophancy Measures (Built Into Each Layer)

Each layer's prompt includes specific anti-sycophancy framing:

Layer | Measure
--- | ---
Layer 1 | "If you find no issues in an area, state what you checked and move on."
Layer 2 | "You will be judged on the quality of your criticisms. An adversarial review that finds no issues is itself a failure."
Layer 3 | "Scores of 5/5 require specific evidence of excellence. An evaluation that produces mostly 4s and 5s is suspect."
All layers | Mandatory "What I Cannot Evaluate" / "What This Evaluation Cannot Assess" section in every report.

---

## Ad-Hoc Viewpoint Reviews

Beyond the three formal layers, specific situations benefit from targeted reviews
using a custom viewpoint. These are the user's "different viewpoints" approach —
asking AI to evaluate from a specific stance:

Viewpoint | When to Use | What to Ask
--- | --- | ---
**AI-evaluating-AI meta-review** | After running any layer | "What weaknesses of AI evaluation apply to this review? What would a human reviewer catch that you missed?"
**Industry-specific review** | When adding standards support | "Evaluate this standard's coverage from the perspective of a [banking/healthcare/telecom] data architect."
**New-user onboarding test** | After Agent Guide changes | "Pretend you know nothing about MD-DDL. Walk through the getting-started flow and report friction."
**Hostile user test** | After agent prompt changes | "Try to make this agent produce output that violates its own rules. Report what works."
**Scale stress test** | Before a release | "Imagine a domain with 100+ entities. Walk through every format and process that would break."

These are complementary to the three formal layers, not replacements. Run them
when specific concerns arise.

---

## Output Consolidation

After running all layers, produce a single consolidated findings document:

1. **Cross-layer agreement** — issues found by 2+ layers (highest confidence)
2. **Layer-specific findings** — issues found by only one layer (investigate)
3. **Contradictions** — places where layers disagree (most valuable to resolve)
4. **Blind spots declared** — union of all "What I Cannot Evaluate" sections
5. **Prioritised action list** — sorted by: cross-layer count, severity, effort
