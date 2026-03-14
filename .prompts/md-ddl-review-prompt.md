# MD-DDL Periodic Review Prompt

You are conducting a structured review of the md-ddl project. This is a
Markdown-native data modelling standard with five AI agents, a set of skills,
worked examples, and supporting documentation.

Your job is to evaluate consistency, currency, and correctness across the
project — not to generate new content. Produce a structured findings report
at the end.

**Evaluation discipline:** This is Layer 1 of a multi-layer review process.
Your focus is structural and mechanical — things that are objectively verifiable.
Do not assess subjective quality, stakeholder fitness, or design adequacy — those
belong to Layer 2 (Adversarial) and Layer 3 (Stakeholder Simulation).

An honest review that finds real issues is more valuable than a clean bill of
health. If you find no issues in an area, state what you checked and move on.
If you cannot assess an area, say so explicitly.

Write the findings to the review.md file

---

## Before you begin — understand the architecture

Read these files first, in this order. Do not skip ahead.

1. `md-ddl-specification/1-Foundation.md` — the core principles
2. `agents/agent-guide/AGENT.md` — identity, user archetypes, skill index
3. `agents/agent-ontology/AGENT.md` — identity, lifecycle stage, skill index
4. `agents/agent-artifact/AGENT.md` — identity, lifecycle stage, skill index
5. `agents/agent-architect/AGENT.md` — identity, lifecycle stage, skill index
6. `agents/agent-governance/AGENT.md` — identity, lifecycle stage, skill index
7. `README.md` — the public face and integration guide

This gives you the mental model you need to evaluate everything else correctly.

---

## What each area is for — review lens

Before reviewing each area, internalise its purpose. Findings are only meaningful
when evaluated against intent.

### Specification (`md-ddl-specification/`)

**Purpose:** The normative authority. Every rule in the project must be traceable
here. No other file has the right to define language rules.

**Review lens:**

- Are rules stated once, in the owning section, and nowhere else?
- Is `MD-DDL-Complete.md` a faithful concatenation of sections 1–10 in order?
- Is the version number consistent across all section files?
- Are there rules implied by examples or agents that are missing from the spec?

### Agents (`agents/*/AGENT.md`)

**Purpose:** Define the identity, lifecycle stage, behaviour modes, and skill index
for each agent. Agent Guide owns Learning and Navigation. Agent Ontology owns
Discovery and Design. Agent Artifact owns Physical Artifact Generation. Agent
Architect owns Strategic Design and Data Product Publication. Agent Governance owns
Standards Conformance and Compliance Assurance. These are distinct — they must not
overlap.

**Review lens:**

- Does each agent's stated lifecycle stage and capabilities stay within its
  ownership boundary?
- Does Agent Guide defer production modelling to the specialist agents?
- Does Agent Governance defer structural modelling to Agent Ontology?
- Does Agent Ontology defer ongoing compliance assurance to Agent Governance?
- Does Agent Ontology defer physical generation to Agent Artifact?
- Does Agent Architect defer physical generation to Agent Artifact and
  structural modelling to Agent Ontology?
- Does Agent Artifact defer product design to Agent Architect?
- Does each skill index accurately describe the skills that exist on disk?
- Do the non-negotiable output rules in each AGENT.md align with the spec?
- Are behaviour modes clearly distinct and correctly triggered?

### Skills (`agents/*/skills/*/SKILL.md`)

**Purpose:** Process-oriented guidance for applying the spec. Skills teach an AI
*how* to apply rules, not *what* the rules are. Heavy spec content belongs in
`references/` files, not in SKILL.md bodies.

**Review lens:**

- Does each SKILL.md stay under 500 lines?
- Does any skill contain spec rules stated verbatim? (If yes, it should
  reference the spec instead.)
- Do all `references/` paths point to files that actually exist on disk?
- Does the trigger description (frontmatter) accurately describe when the skill
  should load? Is it specific enough to trigger reliably, not so broad it
  loads unnecessarily?
- For shared skills (e.g. `regulatory-compliance` used by both agents): does
  the trigger description reflect all contexts in which it is used?
- Does each skill stay within its agent's lifecycle boundary?

### Examples (`examples/`)

**Purpose:** Demonstrate correct application of the current spec. They serve as
both human reference and AI context (agents are instructed to use
`examples/Financial Crime/` as the quality benchmark).

**Review lens:**

- Does every example conform to the current spec version?
- Check for outdated patterns using this table:

  Old pattern | Current pattern | Owning spec section
  --- | --- | ---
  `- name: Foo` / `type: bar` list-style attributes | `Foo:` / `type: bar` key-as-name | `3-Entities.md`
  `- name: Rule` / `logic: "..."` constraints | `Rule Name:` / `check: "..."` | `3-Entities.md`
  H3 headings in domain file sections | Markdown summary tables | `2-Domains.md`
  Missing `type:` on relationships | `type: owns` (or appropriate) explicit | `5-Relationships.md`
  Missing `existence` and `mutability` | Both declared explicitly | `3-Entities.md`
  Missing `granularity` on relationships | Explicit value | `5-Relationships.md`
  Missing `classification` in `governance:` | Declared | `3-Entities.md`
  Detail file H1 not linking back to domain | `# [Domain](../domain.md)` | `3-Entities.md`

- Do all internal links (table Name columns, Mermaid hyperlinks) resolve to
  files and anchors that exist?
- **Cardinality conflicts (Mermaid vs YAML):** When a diagram and YAML disagree
  on cardinality, do **not** recommend a specific correction. State the conflict
  as a structural observation and flag it as requiring domain semantics review —
  the diagram may be correct and the YAML wrong, or vice versa, and the answer
  depends on business meaning that a structural review cannot determine.
  Recommend Agent Ontology review before any fix is applied. Exception: if one
  representation is an isolated transcription error obvious from context (e.g.,
  a `"1"` vs `"0..1"` on a clearly optional field), note the likely error but
  still flag for confirmation.
- Does `examples/Financial Crime/` remain the highest-quality example — the one
  you would point a new user to?
- If `examples/Simple Customer/` exists, is it genuinely simpler and correct,
  not just shorter?
- If `examples/Brownfield Retail/` exists, does it correctly demonstrate the
  adoption maturity model from Section 10?
  - Does the domain have an `adoption` block if `baselines/` exists?
  - Are baseline files using the required metadata format (baseline type,
    source_system, captured_date, captured_by, status)?
  - Is `maturity` consistent with the actual state of the domain (e.g., if
    canonical entities exist and baselines have mapping blocks, maturity
    should be at least `mapped`)?
  - Do baseline `superseded_by` links point to existing canonical entity files?
- For industry-specific examples (Healthcare, Telecom, Retail Sales, Retail Service),
  do they demonstrate correct spec application for their respective industries?
  Are industry standards references (FHIR, TM Forum SID, etc.) accurate?

### README (`README.md`)

**Purpose:** The public face of the project. It must accurately describe what
md-ddl is, what the agents do, how to integrate the standard, and the data
product framing. It is read by people deciding whether to adopt md-ddl.

**Review lens:**

- Does the repository layout section match the actual file structure on disk?
- Are all agent capabilities described accurately against what the AGENT.md files
  actually define? No overselling, no omissions.
- Is the integration section (submodule + tooling configuration) correct and
  current for VS Code Copilot, Claude Code, and Claude.ai Projects?
- Does the Domains as Data Products section accurately reflect the current mapping
  between MD-DDL concepts and data product concepts?
- Are there any capability claims in the README that are not yet supported by
  the spec or agents (promises without implementation)?

### Validation Philosophy Consistency

**Purpose:** Verify that the two-tier validation model defined in `1-Foundation.md` is consistently applied across all agent prompts and review tooling.

**Review lens:**

- Does `md-ddl-specification/1-Foundation.md` contain a "Validation Model" section that defines the two-tier model and lists exactly 5 pre-flight checks?
- Do all agent SKILL.md files use `flag` / `note` / `suggest` / `observe` language for convention and quality concerns (Levels 3–5)?
- Is `error` / `reject` / `fail` language in agent prompts limited to syntax-level failures (Level 1)?
- Does the domain-review SKILL.md (Agent Ontology) explicitly state it is a contextual quality review, not a lint pass?
- Does the compliance-audit SKILL.md (Agent Governance) distinguish between structurally missing governance (structural absence) and substantively incomplete governance (quality concern)?
- Does the compliance-audit SKILL.md treat governance vocabulary deviations as Advisory observations rather than Critical gaps?

Flag any agent prompt where enforcement language is used for convention or quality issues — this is a prompt bug.

---

### Contributor Guidance

**Purpose:** Developer guidance for contributors working on the standard itself.
This may exist in multiple platform-specific locations (`.github/copilot-instructions.md`
for Copilot, `CLAUDE.md` for Claude Code) and shared locations (`.prompts/`).

**Review lens:**

- Does the repository layout match the actual file structure on disk?
- Is the agent responsibilities table current and complete?
- Does the shared skills section correctly identify all skills used by more than
  one agent?
- Is the upgrade patterns table in "Upgrading existing examples" current with the
  latest spec version?
- Are there any references to files that don't exist, or missing references to
  files that do?

---

## Cross-cutting checks

After reviewing each area individually, run these checks across the whole project.

### Version consistency

- What version is declared in `1-Foundation.md`?
- Is the same version in `README.md`?
- Are there any spec section files with different version numbers?

### Rule duplication audit

Pick five rules from the spec at random. Search for those rules in agent prompts,
skills, and contributor instructions. Are any stated verbatim in more than one place?
Duplication is technical debt — it means a spec update may not propagate.

### Lifecycle boundary audit

For each agent, list the capabilities it claims. Check that no capability claimed
by one agent overlaps with another agent's ownership.

### Dead reference audit

Check all Markdown links in:

- Domain file summary tables (Name column links)
- Mermaid diagram hyperlinks
- AGENT.md skill index paths
- SKILL.md `references/` paths
- Contributor instructions file references

Flag any link that points to a file or anchor that does not exist on disk.

### Example currency audit

For each example file, identify the three most recently changed spec rules
(check git log or version history if available, otherwise use the spec version).
Verify the examples reflect those rules.

---

## Report format

Produce your findings in this structure. Be specific — cite file paths and line
numbers where possible. Do not pad findings; if an area is clean, say so briefly.

```markdown
## MD-DDL Review — [date]
**Spec version reviewed:** [version from 1-Foundation.md]

### Critical findings
Issues where a stated rule is violated, a link is broken, or a claim in the
README has no implementation behind it. These should be fixed before the next
version bump.

[finding: file path — description — recommended fix]

### Advisory findings
Issues where best practice is not met, a pattern is inconsistent, or a forward
signal in the README may need updating. These should be addressed in the next
maintenance pass.

[finding: file path — description — recommended fix]

### Observations
Things that are working well, patterns that are consistently applied, or
structural strengths worth preserving.

### Areas not reviewed
Anything you could not assess due to missing file access, ambiguous scope,
or files not provided. Be explicit so the reviewer knows what to check manually.

### Suggested agenda for next spec version
Based on findings above, what should be addressed in the next version of the
spec or agents? Separate "fix existing" from "extend capability".
```

---

## What this review is not

- Not a content generation task. Do not rewrite files unless explicitly asked
  after the report is complete.
- Not a compliance audit of someone's domain model. You are reviewing the
  standard itself, not a model built with it.
- Not a style review. Do not flag prose preferences or formatting opinions
  unless they cause genuine ambiguity.
- Not exhaustive line-by-line proofreading. Focus on structural correctness,
  consistency, and accuracy of claims.
