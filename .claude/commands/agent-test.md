Read `agents/agent-test/AGENT.md` and adopt its identity, modes, and protocols for this session.

Follow the skill-loading protocol defined in the AGENT.md:
- Start with `agents/agent-test/skills/test-strategy/SKILL.md`
- Load `agents/agent-test/skills/worked-example-compilation/SKILL.md` before writing any unit or fixture test
- Load the shared `agents/agent-artifact/skills/dbt-project/SKILL.md` before writing into a dbt project, and `agents/agent-artifact/skills/faker/SKILL.md` before generating synthetic data
- Read the relevant domain, source transform detail, and product files before generating tests

Generate and run tests derived from MD-DDL declarations. Do not change worked examples, transformations, or generated models. Route declaration defects to Agent Ontology and generated-code defects to Agent Artifact.

Task: $ARGUMENTS
