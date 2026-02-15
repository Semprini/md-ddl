# MD-DDL Skill Architecture

## Overview

MD-DDL skills are designed for AI-native data modeling where the AI has the pen and the human provides direction. Skills teach the AI how to research, model, and apply industry standards and regulatory requirements without loading massive amounts of irrelevant context.

---

## Skill Structure

```
/skills/
  /{skill-name}/
    SKILL.md                          # Main skill file (compact, always loaded)
    examples.md                       # Complete worked examples (loaded when needed)
    {topic-specific-guidance}.md      # Detailed guidance files (multiple, loaded on-demand)
    /standards/                       # Industry standards (loaded on-demand by industry)
      bian.md
      acord.md
      tm-forum.md
      fhir.md
      iso20022.md
      ...
    /regulators/                      # Regulatory requirements (loaded on-demand by jurisdiction)
      apra.md
      rbnz.md
      basel.md
      gdpr.md
      fatf.md
      ...
```

**Example - domain-discovery skill**:
```
/skills/
  /domain-discovery/
    SKILL.md                          # Core discovery workflow
    examples.md                       # Complete domain discovery examples
    governance-considerations.md      # How governance affects domain design
    domain-boundaries.md              # Deciding domain scope and boundaries
    canonical-vs-ddd.md               # Single canonical vs domain-driven approach
    cross-domain-relationships.md     # Handling concepts that span domains
```

**Example - entity-or-enum skill**:
```
/skills/
  /entity-or-enum/
    SKILL.md                          # Core classification decision tree
    examples.md                       # Complete examples across industries
    party-role-pattern.md             # Deep dive on Party/Party Role abstraction
    temporal-considerations.md        # How temporal needs affect entity vs enum
```

---

## File Types

### 1. SKILL.md (Compact, Always Loaded)

**Purpose**: Lightweight decision frameworks and workflows that activate based on user intent

**Size**: 100-200 lines maximum

**Contains**:
- Quick decision frameworks
- Questions to ask the user (only when information missing)
- Common patterns
- When to load detailed guidance
- When to load standards/regulators (on-demand)

**Does NOT contain**:
- Complete industry standard details
- Full regulatory requirements
- Exhaustive examples
- Edge case handling

**Example**: `entity-or-enum/SKILL.md` provides decision tree for entity vs enum, links to detailed guidance files

---

### 2. Detailed Guidance Files (Loaded When Needed)

**Purpose**: Comprehensive explanation of specific modeling topics

**Size**: 300-2000 lines per file

**Structure**: Multiple guidance files per skill, each focused on a specific topic

**Examples**:
- `domain-discovery/governance-considerations.md` - How governance affects domain design
- `domain-discovery/domain-boundaries.md` - Deciding where domains start and end
- `domain-discovery/canonical-vs-ddd.md` - Single canonical vs domain-driven approach
- `entity-or-enum/party-role-pattern.md` - Deep dive on Party/Party Role abstraction
- `inheritance/multi-level-hierarchies.md` - When and how to use >2 level inheritance

**Contains**:
- Core principles and deep explanations
- Decision frameworks with edge cases
- Cross-industry pattern comparisons
- Anti-patterns with explanations
- Complex scenario handling
- Complete case studies

**When AI loads**: 
- Skill indicates "load {specific-guidance-file} when..."
- User's scenario doesn't fit common patterns
- First time modeling a particular pattern
- User challenges AI's decision
- User asks for deeper explanation

**NOT formalized**: Each skill determines what detailed guidance files it needs based on the complexity of its domain

---

### 3. examples.md (Complete Examples, Loaded When Needed)

**Purpose**: Fully worked examples showing complete modeling workflows

**Size**: 300-1000 lines

**Contains**:
- End-to-end modeling examples
- User-AI dialogue flows
- Complete domain.md outputs
- Rationale for decisions made

**When AI loads**:
- User asks "can you show me an example?"
- AI needs reference implementation
- Complex multi-step workflow

**Example**: `entity-or-enum/examples.md` shows complete banking, insurance, telecom examples with full domain.md output

---

### 4. standards/{standard}.md (On-Demand by Industry)

**Purpose**: Detailed guidance for specific industry standards

**Size**: 500-2000 lines per standard

**Contains**:
- Standard overview and structure
- How to find concept definitions
- URL patterns for references
- Common concept mappings (business term → standard term)
- When standard terminology differs from business language
- Integration with other standards

**When AI loads**:
- User mentions industry or specific standard
- **ONLY loads standards relevant to user's industry**

**Examples**:
- `external-standard-mapping/standards/bian.md` - Banking (BIAN BOM)
- `external-standard-mapping/standards/acord.md` - Insurance
- `external-standard-mapping/standards/tm-forum.md` - Telecommunications
- `external-standard-mapping/standards/fhir.md` - Healthcare

**Critical**: If user is modeling banking with BIAN, AI does NOT load acord.md, tm-forum.md, fhir.md, etc.

---

### 5. regulators/{regulator}.md (On-Demand by Jurisdiction)

**Purpose**: Detailed requirements for specific regulatory bodies

**Size**: 500-2000 lines per regulator

**Contains**:
- Regulator overview and scope
- Key regulations/standards (e.g., APRA CPS 234)
- Metadata requirements for entities
- Retention and residency rules
- Reporting requirements
- Compliance framework mappings

**When AI loads**:
- User mentions jurisdiction or specific regulator
- **ONLY loads regulators relevant to user's jurisdiction**

**Examples**:
- `regulatory-compliance/regulators/apra.md` - Australian Prudential Regulation Authority
- `regulatory-compliance/regulators/rbnz.md` - Reserve Bank of New Zealand
- `regulatory-compliance/regulators/basel.md` - Basel Committee standards
- `regulatory-compliance/regulators/gdpr.md` - EU data protection
- `regulatory-compliance/regulators/fatf.md` - Financial Action Task Force (AML/CTF)

**Critical**: If user is in Australia/NZ banking, AI does NOT load gdpr.md, ccpa.md, hipaa.md, etc.

---

## On-Demand Loading Pattern

### Problem

Industry standards and regulations are massive:
- BIAN has 300+ service domains
- APRA has dozens of prudential standards
- Basel III/IV is a complex framework
- Loading everything wastes context and confuses the AI

### Solution

**Infer from context, ask only when unclear**

```
User: "Model financial crime for a New Zealand bank"

AI (domain-discovery skill):
1. Infers: "New Zealand bank" → RBNZ regulator, likely APRA (if Australian-owned)
2. Infers: "financial crime" → FATF (AML/CTF) required
3. Infers: "bank" → BIAN standard, Basel framework
4. AI loads:
   - standards/bian.md (banking industry)
   - regulators/rbnz.md (NZ operations)
   - regulators/apra.md (assumes Australian parent - common pattern)
   - regulators/basel.md (international banking standard)
   - regulators/fatf.md (AML/CTF)
5. AI states: "I'm loading RBNZ, APRA, Basel, and FATF requirements. Are there other regulatory jurisdictions I should consider?"
6. AI does NOT load:
   - standards/acord.md (insurance - not relevant)
   - standards/tm-forum.md (telecom - not relevant)
   - regulators/gdpr.md (EU - not mentioned)
   - regulators/ccpa.md (California - not mentioned)
   - regulators/hipaa.md (US healthcare - not relevant)
```

**When AI asks**:
- Ambiguous jurisdiction (e.g., "international bank" - which countries?)
- Unusual regulatory combination
- User mentions cross-border operations without specifying countries
- Missing critical information (e.g., "financial institution" - bank? insurance? securities?)

**AI should NOT ask**:
- When jurisdiction is clear from context ("New Zealand bank" → RBNZ)
- When industry standard is obvious ("bank" → BIAN, "insurer" → ACORD)
- When regulatory frameworks are standard for the industry (banking → Basel, FATF)


---

## Skill Cross-References

Skills reference each other and their components:

```markdown
# In domain-discovery/SKILL.md

## When to Load Detailed Guidance

Load specific guidance files based on user's questions:
- Domain scope unclear → Load [domain-boundaries.md](domain-boundaries.md)
- Governance questions → Load [governance-considerations.md](governance-considerations.md)
- DDD vs canonical debate → Load [canonical-vs-ddd.md](canonical-vs-ddd.md)

## Load Relevant Standards
Based on user's industry, load applicable standards:
- Banking → Load [BIAN](../external-standard-mapping/standards/bian.md)
- Insurance → Load [ACORD](../external-standard-mapping/standards/acord.md)

## Load Relevant Regulators
Based on user's jurisdiction (inferred from context), load applicable regulators:
- New Zealand bank → Load [RBNZ](../regulatory-compliance/regulators/rbnz.md), likely [APRA](../regulatory-compliance/regulators/apra.md)
- EU operations → Load [GDPR](../regulatory-compliance/regulators/gdpr.md)
```

---

## User Context File (Optional)

For recurring projects, users can provide upfront context to avoid repeated questions:

**user-context.yaml**:
```yaml
organization:
  name: "Example Bank NZ"
  jurisdiction: "New Zealand"
  parent_jurisdiction: "Australia"
  
industry:
  primary: "Banking"
  
standards:
  - BIAN BOM
  - ISO 20022
  
regulators:
  - APRA (primary)
  - RBNZ (local)
  - FATF (AML/CTF)
  - Basel III
```

AI reads this and automatically loads:
- `standards/bian.md`
- `standards/iso20022.md`
- `regulators/apra.md`
- `regulators/rbnz.md`
- `regulators/fatf.md`
- `regulators/basel.md`

---

## Complete Skill Set

### Core Modeling Skills
1. **domain-discovery** - Research and scope domains
2. **entity-or-enum** - Classify concepts
3. **inheritance** - Design entity hierarchies
4. **temporal-selection** - Choose temporal patterns
5. **relationship-design** - Model entity connections
6. **constraint-logic** - Express business rules
7. **summary-writing** - Write effective concept summaries
8. **iterative-workflow** - Manage the modeling process

### Integration Skills
9. **external-standard-mapping** - Reference industry standards (with on-demand standard loading)
10. **regulatory-compliance** - Apply regulatory metadata (with on-demand regulator loading)

---

## Skill Development Principles

### Compact Skills (SKILL.md)
- ✅ Quick decision trees
- ✅ Questions to ask users (only when information missing)
- ✅ Inference from context when possible
- ✅ Common patterns only
- ✅ Links to specific detailed guidance files
- ❌ No exhaustive examples
- ❌ No edge case handling
- ❌ No industry-specific deep dives

### Detailed Guidance Files
- ✅ Focused on specific topic (not everything in one file)
- ✅ Comprehensive explanations
- ✅ Edge cases and anti-patterns
- ✅ Cross-industry comparisons
- ✅ Complete case studies for that topic
- ❌ Not loaded by default
- ❌ Only loaded when skill indicates or user needs

### Standards & Regulators
- ✅ Deep industry/jurisdiction knowledge
- ✅ URL patterns and mappings
- ✅ Specific requirements
- ✅ AI infers which to load from context
- ❌ Only loaded for relevant industry/jurisdiction
- ❌ Never load all at once
- ❌ AI should not ask if context is clear

---

## Benefits of This Architecture

1. **Context Efficiency**: AI only loads what it needs for the specific domain being modeled
2. **Scalability**: Can add new standards/regulators without bloating core skills
3. **Maintainability**: Standards and regulations updated independently of core modeling skills
4. **Clarity**: Separation of modeling patterns (universal) from industry specifics (contextual)
5. **Flexibility**: Same modeling skills work across all industries, standards loaded adapt to context