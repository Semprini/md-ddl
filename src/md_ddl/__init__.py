"""MD-DDL — the Markdown Data Definition Language standard, packaged for pip.

The distribution carries the standard itself as package data: the
specification, the agent prompts and skills, the companion guides, the
reference examples, and the architecture source material. `md-ddl init`
unpacks that payload into a project so the agents resolve exactly as they do
when MD-DDL is added as a git submodule.

Spec and repository: https://github.com/Semprini/md-ddl
"""

from __future__ import annotations

from importlib import resources
from pathlib import Path

__version__ = "0.9.2"

__all__ = [
    "DOCS_DIRNAME",
    "DOCS_PAYLOAD",
    "WRAPPER_PAYLOAD",
    "__version__",
    "docs_sources",
    "wrapper_source",
]

#: Directory an installed project keeps the standard in. The Copilot agent
#: wrappers include `../../.md-ddl/agents/...`, and `md-ddl init` rewrites the
#: Claude slash commands to match, so this name is part of the contract.
DOCS_DIRNAME = ".md-ddl"

#: Source-repository directory -> path inside `.md-ddl/` once installed.
#: `references/industry_standards/` is deliberately absent: the raw BIAN, FHIR
#: and TM Forum snapshots are 63 MB, and the distilled markdown the agents
#: actually load ships under `agents/*/skills/standards-alignment/standards/`.
DOCS_PAYLOAD = {
    "agents": "agents",
    "md-ddl-specification": "md-ddl-specification",
    "guides": "guides",
    "examples": "examples",
    "references/architecture": "references/architecture",
}

#: Source-repository directory -> subdirectory of the packaged `wrappers/`.
WRAPPER_PAYLOAD = {
    ".github/agents": "copilot",
    ".claude/commands": "claude",
}


def _package_dir() -> Path:
    """Directory this package is installed in."""
    return Path(str(resources.files(__name__)))


def _repo_root() -> Path | None:
    """Repository root, when running from a source checkout rather than a wheel.

    An editable install or a `python -m md_ddl` from a clone has no packaged
    payload; the standard lives at the repository root instead. `src/md_ddl`
    means the root is two levels up.
    """
    root = _package_dir().parents[1]
    return root if (root / "md-ddl-specification").is_dir() else None


def docs_sources() -> dict[str, Path]:
    """Map each `.md-ddl/` destination path to the directory supplying it.

    Raises:
        FileNotFoundError: if neither the packaged payload nor a source
            checkout can be found.
    """
    package_dir = _package_dir()
    if (package_dir / "docs").is_dir():
        return {
            dest: package_dir / "docs" / dest
            for dest in DOCS_PAYLOAD.values()
        }

    repo_root = _repo_root()
    if repo_root is not None:
        return {
            dest: repo_root / source
            for source, dest in DOCS_PAYLOAD.items()
        }

    raise FileNotFoundError(
        f"no MD-DDL payload found in {package_dir} and no source checkout above it; "
        "reinstall the package with `pip install --force-reinstall md-ddl`"
    )


def wrapper_source(tool: str) -> Path:
    """Directory holding the agent wrappers for `tool` ('claude' or 'copilot').

    Raises:
        KeyError: if `tool` is not a known AI tool.
        FileNotFoundError: if the wrappers cannot be located.
    """
    sources = {dest: source for source, dest in WRAPPER_PAYLOAD.items()}
    if tool not in sources:
        raise KeyError(tool)

    package_dir = _package_dir()
    packaged = package_dir / "wrappers" / tool
    if packaged.is_dir():
        return packaged

    repo_root = _repo_root()
    if repo_root is not None:
        return repo_root / sources[tool]

    raise FileNotFoundError(
        f"no {tool} agent wrappers found in {package_dir}; "
        "reinstall the package with `pip install --force-reinstall md-ddl`"
    )
