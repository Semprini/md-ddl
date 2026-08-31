"""Command-line interface for the packaged MD-DDL standard.

`md-ddl init` is the pip equivalent of adding this repository as a git
submodule: it unpacks the standard into `.md-ddl/` and installs the agent
wrappers for Claude Code and/or GitHub Copilot, rewriting their paths so the
agents resolve against the unpacked copy.

pip has no post-install hook for wheels, so this runs as an explicit command
after `pip install md-ddl` rather than during the install itself.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

from md_ddl import DOCS_DIRNAME, __version__, docs_sources, includes, wrapper_source

#: Wrappers that drive review of the standard itself. They belong to the source
#: repository and are not installed into a consuming project.
INTERNAL_WRAPPERS = frozenset({"review-md-ddl.agent.md", "review.md"})

#: Claude slash commands carry paths relative to the source repository root.
#: Retarget them at the unpacked standard, as the bootstrap scripts do.
CLAUDE_PATH_REWRITES = (
    (re.compile(r"`agents/"), f"`{DOCS_DIRNAME}/agents/"),
    (re.compile(r"`md-ddl-specification/"), f"`{DOCS_DIRNAME}/md-ddl-specification/"),
)

TOOL_TARGETS = {
    "claude": Path(".claude") / "commands",
    "copilot": Path(".github") / "agents",
}

AGENTS = (
    ("agent-guide", "Agent Guide",
     "Learning, navigation, concept explanation. Start here."),
    ("agent-ontology", "Agent Ontology",
     "Domain discovery, entity modelling, source mapping."),
    ("agent-artifact", "Agent Artifact",
     "Physical schema generation (SQL DDL, JSON Schema, Parquet, Cypher)."),
    ("agent-architect", "Agent Architect",
     "Data product design, architecture discussion, ODPS manifests."),
    ("agent-governance", "Agent Governance",
     "Standards conformance, compliance auditing, governance assurance."),
)


def _agent_table(tool: str) -> str:
    """Markdown table of the agents, addressed the way `tool` invokes them."""
    if tool == "claude":
        rows = [f"`/{name}` | {title} | {purpose}" for name, title, purpose in AGENTS]
        header = ["Command | Agent | Purpose", "--- | --- | ---"]
    else:
        rows = [f"`{name}` | {purpose}" for name, _title, purpose in AGENTS]
        header = ["Agent | Purpose", "--- | ---"]
    return "\n".join(header + rows)


def _layout_block(project: str, tool: str) -> str:
    """Aligned project-tree sketch for the instructions file."""
    wrappers = (
        (".claude/commands/", "Claude slash commands") if tool == "claude"
        else (".github/agents/", "Copilot custom agent wrappers")
    )
    rows = [
        (f"{DOCS_DIRNAME}/", "MD-DDL standard (installed — do not edit)"),
        wrappers,
        ("domains/", "Domain files (one per business domain)"),
        ("entities/", "Entity detail files"),
    ]
    width = max(len(path) for path, _ in rows)
    return "\n".join(
        [f"{project}/"] + [f"  {path:<{width}}  {note}" for path, note in rows]
    )


def _instructions(project: str, tool: str) -> str:
    """Project-level agent instructions for `tool`."""
    if tool == "claude":
        invocation = "Invoke them with slash commands in Claude Code:"
    else:
        invocation = "Use the custom agents in `.github/agents/` via GitHub Copilot Chat:"
    invocation = f"{invocation}\n\n{_agent_table(tool)}"

    return f"""\
# {project}

This project uses the [MD-DDL standard](https://github.com/Semprini/md-ddl) for
data domain modelling. MD-DDL is installed from PyPI (`pip install md-ddl`) and
unpacked into `{DOCS_DIRNAME}/` by `md-ddl init`.

## Agents

MD-DDL provides AI agents for every stage of the modelling lifecycle.
{invocation}

## Validation

Run the mechanical pre-flight checks with `md-ddl lint <domain-folder>`.
Everything beyond syntax is agent-driven review — see
`{DOCS_DIRNAME}/guides/validation-tooling.md`.

## Key references

- MD-DDL specification: `{DOCS_DIRNAME}/md-ddl-specification/`
- Complete spec (single file): `{DOCS_DIRNAME}/md-ddl-specification/MD-DDL-Complete.md`
- Examples: `{DOCS_DIRNAME}/examples/`

## Project layout

```
{_layout_block(project, tool)}
```

Upgrade the standard with `pip install --upgrade md-ddl && md-ddl init`.
"""


def _guard_submodule(target: Path, force: bool) -> None:
    """Refuse to overwrite an existing MD-DDL git submodule."""
    docs_root = target / DOCS_DIRNAME
    if (docs_root / ".git").exists() and not force:
        raise SystemExit(
            f"error: {docs_root} looks like the MD-DDL git submodule.\n"
            "       Installing over it would discard it. Remove the submodule first\n"
            "       (git submodule deinit), or re-run with --force to overwrite."
        )


def _install_docs(target: Path) -> list[str]:
    """Unpack the standard into `<target>/.md-ddl/`. Returns log lines."""
    docs_root = target / DOCS_DIRNAME
    log = []
    docs_root.mkdir(parents=True, exist_ok=True)
    for dest, source in docs_sources().items():
        if not source.is_dir():
            raise SystemExit(f"error: packaged payload is missing {source}")
        destination = docs_root / dest
        # Replace rather than merge, so an upgrade cannot leave files that the
        # new version has deleted.
        if destination.exists():
            shutil.rmtree(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination)
        log.append(f"  {DOCS_DIRNAME}/{dest}")
    return log


def _install_wrappers(target: Path, tool: str, force: bool) -> tuple[list[str], list[str]]:
    """Install the agent wrappers for `tool`. Returns (written, skipped)."""
    source_dir = wrapper_source(tool)
    dest_dir = target / TOOL_TARGETS[tool]
    dest_dir.mkdir(parents=True, exist_ok=True)

    written: list[str] = []
    skipped: list[str] = []
    for source in sorted(source_dir.glob("*.md")):
        if source.name in INTERNAL_WRAPPERS:
            continue
        destination = dest_dir / source.name
        if destination.exists() and not force:
            skipped.append(f"  {TOOL_TARGETS[tool]}/{source.name}")
            continue

        content = source.read_text(encoding="utf-8")
        if tool == "claude":
            for pattern, replacement in CLAUDE_PATH_REWRITES:
                content = pattern.sub(replacement, content)
        destination.write_text(content, encoding="utf-8")
        written.append(f"  {TOOL_TARGETS[tool]}/{source.name}")
    return written, skipped


def _include_roots(target: Path) -> list[Path]:
    """Everything in a project that may carry `{{INCLUDE}}` directives."""
    return [target / DOCS_DIRNAME] + [target / path for path in TOOL_TARGETS.values()]


def _verify_includes(target: Path) -> int:
    """Report whether every agent prompt can reach what it includes.

    The wrappers and the unpacked standard use file-relative include paths so
    they resolve from `.md-ddl/`. Checking after install catches a payload or a
    wrapper that would otherwise load a silently truncated prompt.
    """
    directives = includes.scan(_include_roots(target))
    broken = [d for d in directives if not d.resolves()]

    if not broken:
        print(f"\nVerified {len(directives)} include directives resolve.")
        return 0

    print(f"\nwarning: {len(broken)} of {len(directives)} include directives do not resolve.")
    print("         The agents referencing them will load an incomplete prompt.")
    for directive in broken:
        try:
            location = directive.file.relative_to(target)
        except ValueError:
            location = directive.file
        print(f"  {location}:{directive.line} -> {directive.target}")
    return 1


def cmd_check(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    if not (target / DOCS_DIRNAME).is_dir():
        raise SystemExit(
            f"error: no {DOCS_DIRNAME}/ in {target}; run `md-ddl init` there first"
        )
    return _verify_includes(target)


def cmd_init(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    if target.exists() and not target.is_dir():
        raise SystemExit(f"error: {target} is not a directory")
    target.mkdir(parents=True, exist_ok=True)

    _guard_submodule(target, args.force)

    tools = ["claude", "copilot"] if args.ai == "both" else [args.ai]
    project = args.name or target.name

    print(f"Installing MD-DDL {__version__} into {target}")

    print(f"\nStandard ({DOCS_DIRNAME}/):")
    for line in _install_docs(target):
        print(line)

    if not args.track:
        # A self-ignoring directory keeps the unpacked standard out of the
        # project's history without editing the project's own .gitignore.
        (target / DOCS_DIRNAME / ".gitignore").write_text(
            "# Unpacked by `md-ddl init` from the md-ddl PyPI package.\n"
            "# Re-create it with `md-ddl init` rather than committing it.\n"
            "*\n",
            encoding="utf-8",
        )
        print(f"  {DOCS_DIRNAME}/.gitignore  (pass --track to commit the standard instead)")

    for tool in tools:
        written, skipped = _install_wrappers(target, tool, args.force)
        print(f"\nAgent wrappers ({tool}):")
        for line in written:
            print(line)
        for line in skipped:
            print(f"{line}  (exists, skipped)")

        if not args.no_instructions:
            path = target / ("CLAUDE.md" if tool == "claude" else ".github/copilot-instructions.md")
            if path.exists() and not args.force:
                print(f"  {path.relative_to(target)}  (exists, skipped)")
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(_instructions(project, tool), encoding="utf-8")
                print(f"  {path.relative_to(target)}")

    status = _verify_includes(target)

    print("\nDone. Next steps:")
    if "claude" in tools:
        print("  Claude Code:    /agent-guide  — start here")
    if "copilot" in tools:
        print("  Copilot Chat:   @agent-guide  — start here")
    print("  Validate:       md-ddl lint <domain-folder>")
    return status


def cmd_path(args: argparse.Namespace) -> int:
    """Print where the packaged standard lives, for scripts and CI."""
    for dest, source in docs_sources().items():
        print(f"{dest}\t{source}")
    return 0


def run_lint(argv: list[str]) -> int:
    """Hand the remaining arguments to the linter, untouched."""
    from md_ddl.lint import main as lint_main

    return lint_main(argv, prog="md-ddl lint")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="md-ddl",
        description="The MD-DDL standard: project setup and mechanical validation.",
    )
    parser.add_argument("--version", action="version", version=f"md-ddl {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser(
        "init",
        help=f"unpack the standard into {DOCS_DIRNAME}/ and install the agent wrappers",
    )
    init.add_argument("target", nargs="?", default=".",
                      help="project directory to set up (default: current directory)")
    init.add_argument("--ai", choices=["claude", "copilot", "both"], default="both",
                      help="which AI tool's agent wrappers to install (default: both)")
    init.add_argument("--name", help="project name for the generated instructions "
                                     "(default: the target directory name)")
    init.add_argument("--force", action="store_true",
                      help="overwrite existing wrappers and instructions")
    init.add_argument("--no-instructions", action="store_true",
                      help="do not write CLAUDE.md or copilot-instructions.md")
    init.add_argument("--track", action="store_true",
                      help=f"commit {DOCS_DIRNAME}/ to the project instead of ignoring it")
    init.set_defaults(func=cmd_init)

    # Registered for `md-ddl --help` only; `main` routes `lint` before parsing so
    # every linter flag, `--help` included, reaches the linter unchanged.
    subparsers.add_parser(
        "lint",
        help="run the MD-DDL pre-flight checks (see `md-ddl lint --help`)",
        add_help=False,
    ).add_argument("lint_args", nargs="*", help=argparse.SUPPRESS)

    check = subparsers.add_parser(
        "check", help="verify the installed agent prompts resolve what they include")
    check.add_argument("target", nargs="?", default=".",
                       help="project directory to check (default: current directory)")
    check.set_defaults(func=cmd_check)

    path = subparsers.add_parser("path", help="print the location of the packaged standard")
    path.set_defaults(func=cmd_path)

    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "lint":
        return run_lint(argv[1:])
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
