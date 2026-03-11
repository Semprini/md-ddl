#Requires -Version 5.1
<#
.SYNOPSIS
    MD-DDL project bootstrap script.

.DESCRIPTION
    Creates a new project folder with MD-DDL as a git submodule and
    installs the appropriate AI agent wrappers for Claude or Copilot.
#>

# --- Input ----------------------------------------------------------------

$projectName = (Read-Host "Project name").Trim()
if ([string]::IsNullOrWhiteSpace($projectName)) {
    Write-Error "Project name cannot be empty."
    exit 1
}

Write-Host ""
Write-Host "Which AI system are you using?"
Write-Host "  1) Claude (Claude Code)"
Write-Host "  2) GitHub Copilot"
$aiChoice = (Read-Host "Enter 1 or 2").Trim()

switch ($aiChoice) {
    "1" { $aiSystem = "claude" }
    "2" { $aiSystem = "copilot" }
    default {
        Write-Error "Invalid choice. Enter 1 or 2."
        exit 1
    }
}

# --- Project creation -----------------------------------------------------

Write-Host ""
Write-Host "Creating project '$projectName'..."

New-Item -ItemType Directory -Path $projectName | Out-Null
Set-Location $projectName

git init
git submodule add https://github.com/Semprini/md-ddl .md-ddl
git submodule update --init

# Starter directories for domain files
New-Item -ItemType Directory -Path "domains"  -Force | Out-Null
New-Item -ItemType Directory -Path "entities" -Force | Out-Null

# --- Agent wrappers -------------------------------------------------------

if ($aiSystem -eq "claude") {

    New-Item -ItemType Directory -Path ".claude/commands" -Force | Out-Null

    # Copy slash commands, excluding the internal review command.
    # Update paths so agents load from the submodule (.md-ddl/) instead of
    # the spec repo root.
    Get-ChildItem ".md-ddl/.claude/commands/*.md" | Where-Object { $_.Name -ne "review.md" } | ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        $content = $content -replace '`agents/',              '`.md-ddl/agents/'
        $content = $content -replace '`md-ddl-specification/', '`.md-ddl/md-ddl-specification/'
        Set-Content -Path ".claude/commands/$($_.Name)" -Value $content -NoNewline
    }

    # Project-level CLAUDE.md
    @"
# $projectName

This project uses the [MD-DDL standard](https://github.com/Semprini/md-ddl) for data domain modelling.
The MD-DDL standard is available as a git submodule at ``.md-ddl/``.

## Agents

MD-DDL provides AI agents for every stage of the modelling lifecycle.
Invoke them with slash commands in Claude Code:

Command | Agent | Purpose
--- | --- | ---
``/agent-guide`` | Agent Guide | Learning, navigation, concept explanation. Start here.
``/agent-ontology`` | Agent Ontology | Domain discovery, entity modelling, source mapping.
``/agent-artifact`` | Agent Artifact | Physical schema generation (SQL DDL, JSON Schema, Parquet, Cypher).
``/agent-architect`` | Agent Architect | Data product design, architecture discussion, ODPS manifests.
``/agent-governance`` | Agent Governance | Standards conformance, compliance auditing, governance assurance.

## Key references

- MD-DDL specification: ``.md-ddl/md-ddl-specification/``
- Complete spec (single file): ``.md-ddl/md-ddl-specification/MD-DDL-Complete.md``
- Examples: ``.md-ddl/examples/``

## Project layout

``````
$projectName/
  .md-ddl/        MD-DDL standard (submodule — do not edit)
  domains/        Domain files (one per business domain)
  entities/       Entity detail files
``````
"@ | Set-Content -Path "CLAUDE.md"

} elseif ($aiSystem -eq "copilot") {

    New-Item -ItemType Directory -Path ".github/agents" -Force | Out-Null

    # Copy Copilot custom-agent wrappers, excluding the internal review agent.
    # Wrapper files already contain paths relative to .github/agents/ that
    # resolve correctly once .md-ddl/ is a submodule at the project root.
    Get-ChildItem ".md-ddl/.github/agents/*.agent.md" | Where-Object { $_.Name -ne "review-md-ddl.agent.md" } | ForEach-Object {
        Copy-Item $_.FullName ".github/agents/$($_.Name)"
    }

    # Project-level Copilot instructions
    @"
# $projectName

This project uses the [MD-DDL standard](https://github.com/Semprini/md-ddl) for data domain modelling.
The MD-DDL standard is available as a git submodule at ``.md-ddl/``.

## Agents

MD-DDL provides AI agents for every stage of the modelling lifecycle.
Use the custom agents in ``.github/agents/`` via GitHub Copilot Chat:

Agent | Purpose
--- | ---
``agent-guide`` | Learning, navigation, concept explanation. Start here.
``agent-ontology`` | Domain discovery, entity modelling, source mapping.
``agent-artifact`` | Physical schema generation (SQL DDL, JSON Schema, Parquet, Cypher).
``agent-architect`` | Data product design, architecture discussion, ODPS manifests.
``agent-governance`` | Standards conformance, compliance auditing, governance assurance.

## Key references

- MD-DDL specification: ``.md-ddl/md-ddl-specification/``
- Complete spec (single file): ``.md-ddl/md-ddl-specification/MD-DDL-Complete.md``
- Examples: ``.md-ddl/examples/``

## Project layout

``````
$projectName/
  .md-ddl/           MD-DDL standard (submodule — do not edit)
  .github/agents/    Copilot custom agent wrappers
  domains/           Domain files (one per business domain)
  entities/          Entity detail files
``````
"@ | Set-Content -Path ".github/copilot-instructions.md"

}

# --- Done -----------------------------------------------------------------

Write-Host ""
Write-Host "Done. Project '$projectName' is ready."
Write-Host ""
Write-Host "Next steps:"
Write-Host "  cd $projectName"
if ($aiSystem -eq "claude") {
    Write-Host "  Open in VS Code and start Claude Code"
    Write-Host "  Run /agent-guide to get started with MD-DDL"
} else {
    Write-Host "  Open in VS Code with GitHub Copilot enabled"
    Write-Host "  Use @agent-guide in Copilot Chat to get started with MD-DDL"
}
