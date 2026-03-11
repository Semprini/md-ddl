#!/usr/bin/env bash
# MD-DDL project bootstrap script
# Creates a new project folder with MD-DDL as a git submodule and
# installs the appropriate AI agent wrappers for Claude or Copilot.

set -euo pipefail

# --- Input ----------------------------------------------------------------

read -rp "Project name: " PROJECT_NAME
if [[ -z "${PROJECT_NAME// /}" ]]; then
    echo "Error: project name cannot be empty." >&2
    exit 1
fi

echo ""
echo "Which AI system are you using?"
echo "  1) Claude (Claude Code)"
echo "  2) GitHub Copilot"
read -rp "Enter 1 or 2: " AI_CHOICE

case "$AI_CHOICE" in
    1) AI_SYSTEM="claude" ;;
    2) AI_SYSTEM="copilot" ;;
    *)
        echo "Error: enter 1 or 2." >&2
        exit 1
        ;;
esac

# --- Project creation -----------------------------------------------------

echo ""
echo "Creating project '$PROJECT_NAME'..."

mkdir "$PROJECT_NAME"
cd "$PROJECT_NAME"

git init
git submodule add https://github.com/Semprini/md-ddl .md-ddl
git submodule update --init

# Starter directories for domain files
mkdir -p domains entities

# --- Agent wrappers -------------------------------------------------------

if [[ "$AI_SYSTEM" == "claude" ]]; then

    mkdir -p .claude/commands

    # Copy slash commands, excluding the internal review command.
    # Update paths so agents load from the submodule (.md-ddl/) instead of
    # the spec repo root.
    for src in .md-ddl/.claude/commands/*.md; do
        fname=$(basename "$src")
        [[ "$fname" == "review.md" ]] && continue
        sed \
            -e 's|`agents/|`.md-ddl/agents/|g' \
            -e 's|`md-ddl-specification/|`.md-ddl/md-ddl-specification/|g' \
            "$src" > ".claude/commands/$fname"
    done

    # Project-level CLAUDE.md
    cat > CLAUDE.md << EOF
# $PROJECT_NAME

This project uses the [MD-DDL standard](https://github.com/Semprini/md-ddl) for data domain modelling.
The MD-DDL standard is available as a git submodule at \`.md-ddl/\`.

## Agents

MD-DDL provides AI agents for every stage of the modelling lifecycle.
Invoke them with slash commands in Claude Code:

Command | Agent | Purpose
--- | --- | ---
\`/agent-guide\` | Agent Guide | Learning, navigation, concept explanation. Start here.
\`/agent-ontology\` | Agent Ontology | Domain discovery, entity modelling, source mapping.
\`/agent-artifact\` | Agent Artifact | Physical schema generation (SQL DDL, JSON Schema, Parquet, Cypher).
\`/agent-architect\` | Agent Architect | Data product design, architecture discussion, ODPS manifests.
\`/agent-governance\` | Agent Governance | Standards conformance, compliance auditing, governance assurance.

## Key references

- MD-DDL specification: \`.md-ddl/md-ddl-specification/\`
- Complete spec (single file): \`.md-ddl/md-ddl-specification/MD-DDL-Complete.md\`
- Examples: \`.md-ddl/examples/\`

## Project layout

\`\`\`
$PROJECT_NAME/
  .md-ddl/        MD-DDL standard (submodule — do not edit)
  domains/        Domain files (one per business domain)
  entities/       Entity detail files
\`\`\`
EOF

elif [[ "$AI_SYSTEM" == "copilot" ]]; then

    mkdir -p .github/agents

    # Copy Copilot custom-agent wrappers, excluding the internal review agent.
    # Wrapper files already contain paths relative to .github/agents/ that
    # resolve correctly once .md-ddl/ is a submodule at the project root.
    for src in .md-ddl/.github/agents/*.agent.md; do
        fname=$(basename "$src")
        [[ "$fname" == "review-md-ddl.agent.md" ]] && continue
        cp "$src" ".github/agents/$fname"
    done

    # Project-level Copilot instructions
    cat > .github/copilot-instructions.md << EOF
# $PROJECT_NAME

This project uses the [MD-DDL standard](https://github.com/Semprini/md-ddl) for data domain modelling.
The MD-DDL standard is available as a git submodule at \`.md-ddl/\`.

## Agents

MD-DDL provides AI agents for every stage of the modelling lifecycle.
Use the custom agents in \`.github/agents/\` via GitHub Copilot Chat:

Agent | Purpose
--- | ---
\`agent-guide\` | Learning, navigation, concept explanation. Start here.
\`agent-ontology\` | Domain discovery, entity modelling, source mapping.
\`agent-artifact\` | Physical schema generation (SQL DDL, JSON Schema, Parquet, Cypher).
\`agent-architect\` | Data product design, architecture discussion, ODPS manifests.
\`agent-governance\` | Standards conformance, compliance auditing, governance assurance.

## Key references

- MD-DDL specification: \`.md-ddl/md-ddl-specification/\`
- Complete spec (single file): \`.md-ddl/md-ddl-specification/MD-DDL-Complete.md\`
- Examples: \`.md-ddl/examples/\`

## Project layout

\`\`\`
$PROJECT_NAME/
  .md-ddl/           MD-DDL standard (submodule — do not edit)
  .github/agents/    Copilot custom agent wrappers
  domains/           Domain files (one per business domain)
  entities/          Entity detail files
\`\`\`
EOF

fi

# --- Done -----------------------------------------------------------------

echo ""
echo "Done. Project '$PROJECT_NAME' is ready."
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
if [[ "$AI_SYSTEM" == "claude" ]]; then
    echo "  Open in VS Code and start Claude Code"
    echo "  Run /agent-guide to get started with MD-DDL"
else
    echo "  Open in VS Code with GitHub Copilot enabled"
    echo "  Use @agent-guide in Copilot Chat to get started with MD-DDL"
fi
