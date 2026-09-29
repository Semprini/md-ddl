---
name: agent-test
description: Specialist MD-DDL test agent that compiles worked examples, constraints, temporal rules, and product SLAs into executable tests (dbt unit and data tests) and runs them locally with dbt-core and DuckLake before promotion to the cloud tier.
argument-hint: An MD-DDL domain or data product to test, whether its dbt project has been generated, and the organisation's template project if any.
tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search', 'web', 'todo']
---
Canonical source: `../../.md-ddl/agents/agent-test/AGENT.md`

<agent_test_core>
{{INCLUDE: ../../.md-ddl/agents/agent-test/AGENT.md}}
</agent_test_core>
