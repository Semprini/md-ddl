"""Resolution of the `{{INCLUDE: <path>}}` directive used by agent prompts.

Agent prompts and skill reference stubs pull in canonical content with
`{{INCLUDE: <path>}}`, resolved by the AI platform at prompt-load time. Paths
are file-relative by convention, precisely so the standard keeps working when
it is consumed as a `.md-ddl/` submodule or unpacked there by `md-ddl init` —
a workspace-root path resolves in this repository and breaks in every project
that vendors it.

`md-ddl init` verifies the directives after unpacking, so a prompt that cannot
reach its spec section is reported at setup time rather than silently loading a
truncated prompt.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path
from typing import NamedTuple

FENCE = re.compile(r"^\s*(```|~~~)")
DIRECTIVE = re.compile(r"\{\{INCLUDE:\s*([^}]+?)\s*\}\}")

#: Directories that hold no active prompts when nested inside a vendored copy
#: of the standard, and whose directives must therefore not be resolved there.
#:
#: `.github/agents/` and `.claude/commands/` are wrapper *templates*: they are
#: copied out to the consuming project, and their `../../.md-ddl/...` paths
#: resolve from that destination, never from inside the standard itself. A
#: project's own wrapper directory is checked by passing it as its own root.
#: `roadmap/` and `.prompts/` are project history and review prompts that quote
#: the directive syntax.
INERT_SUBDIRS = frozenset({".github", ".claude", "roadmap", ".prompts"})


class Directive(NamedTuple):
    """One `{{INCLUDE}}` occurrence."""

    file: Path
    line: int
    target: str

    def resolves(self) -> bool:
        return (self.file.parent / self.target).resolve().exists()


def _is_live_target(target: str) -> bool:
    """Whether `target` is a real path rather than prose about the syntax.

    The guides and instructions describe the directive using placeholders —
    `{{INCLUDE: <path>}}`, `{{INCLUDE: ...}}` — which are documentation, not
    references to resolve.
    """
    return target.endswith(".md")


def scan(paths: Iterable[Path]) -> list[Directive]:
    """Collect the live directives under each path in `paths`.

    Occurrences inside fenced code blocks are documentation examples showing
    the syntax, and are skipped.
    """
    directives: list[Directive] = []
    for root in paths:
        if not root.exists():
            continue
        files = sorted(root.rglob("*.md")) if root.is_dir() else [root]
        for file in files:
            if INERT_SUBDIRS.intersection(file.relative_to(root).parts[:-1]):
                continue
            in_fence = False
            text = file.read_text(encoding="utf-8", errors="ignore")
            for number, line in enumerate(text.splitlines(), 1):
                if FENCE.match(line):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                for target in DIRECTIVE.findall(line):
                    if _is_live_target(target):
                        directives.append(Directive(file, number, target))
    return directives


def unresolved(paths: Iterable[Path]) -> list[Directive]:
    """The directives under `paths` whose target does not exist."""
    return [d for d in scan(paths) if not d.resolves()]
