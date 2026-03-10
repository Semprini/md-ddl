#!/usr/bin/env python3
"""
MD-DDL Pre-Flight Check

Mechanical Level-1 syntax validation per the MD-DDL spec (1-Foundation.md).
Run against a domain folder before committing or publishing.

Usage:
    python preflight.py <domain-folder>
    python preflight.py domains/customer
    python preflight.py .          (run from within the domain folder)

Requires: Python 3.8+, pyyaml   (pip install pyyaml)

Exit codes:
    0  no findings
    1  one or more pre-flight failures
    2  usage or invocation error
"""

import re
import sys
import yaml
from dataclasses import dataclass
from pathlib import Path


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    file: str
    line: int
    check: str
    message: str


# ---------------------------------------------------------------------------
# Mermaid diagram types recognised by the spec
# ---------------------------------------------------------------------------

MERMAID_DIAGRAM_TYPES = {
    "graph", "flowchart", "sequenceDiagram", "classDiagram",
    "stateDiagram", "stateDiagram-v2", "erDiagram", "gantt",
    "journey", "gitGraph", "pie", "quadrantChart", "requirementDiagram",
    "mindmap", "timeline", "block-beta", "packet-beta",
    "xychart-beta", "sankey-beta", "kanban", "architecture-beta",
}

# YAML keys in relationship and event blocks that must name a domain entity.
# 'actor' is deliberately excluded — event actors may be roles or external
# systems, not MD-DDL entities.
ENTITY_REF_KEYS = {"source", "target", "entity", "extends"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _extract_code_blocks(text: str, lang: str) -> list[tuple[int, str]]:
    """Return (start_line_1indexed, content) for every fenced block of lang."""
    blocks: list[tuple[int, str]] = []
    lines = text.splitlines()
    fence = re.compile(rf"^```{re.escape(lang)}\s*$", re.IGNORECASE)
    close = re.compile(r"^```\s*$")
    in_block = False
    start = 0
    buf: list[str] = []
    for i, line in enumerate(lines, 1):
        if not in_block:
            if fence.match(line):
                in_block = True
                start = i + 1
                buf = []
        else:
            if close.match(line):
                blocks.append((start, "\n".join(buf)))
                in_block = False
                buf = []
            else:
                buf.append(line)
    return blocks


def _heading_slug(text: str) -> str:
    """GitHub-compatible anchor slug for a heading line."""
    # Strip inline markdown (bold, italic, backticks, links)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*_]", "", text)
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text).strip("-")
    return text


def _get_headings(path: Path) -> set[str]:
    """All heading slugs in a markdown file."""
    slugs: set[str] = set()
    try:
        for line in _read(path).splitlines():
            m = re.match(r"^#{1,6}\s+(.+)$", line)
            if m:
                slugs.add(_heading_slug(m.group(1)))
    except OSError:
        pass
    return slugs


# ---------------------------------------------------------------------------
# Check 1 — YAML syntax
# ---------------------------------------------------------------------------

def check_yaml_syntax(md_file: Path) -> list[Finding]:
    findings: list[Finding] = []
    text = _read(md_file)
    for start, content in _extract_code_blocks(text, "yaml"):
        try:
            yaml.safe_load(content)
        except yaml.YAMLError as exc:
            line_num = start
            if hasattr(exc, "problem_mark") and exc.problem_mark:
                line_num = start + exc.problem_mark.line
            msg = exc.problem if hasattr(exc, "problem") else str(exc)
            findings.append(Finding(str(md_file), line_num, "yaml-syntax",
                                    f"YAML parse error: {msg}"))
    return findings


# ---------------------------------------------------------------------------
# Check 2 — Mermaid syntax
# ---------------------------------------------------------------------------

def check_mermaid_syntax(md_file: Path) -> list[Finding]:
    findings: list[Finding] = []
    text = _read(md_file)
    for start, content in _extract_code_blocks(text, "mermaid"):
        stripped = content.strip()
        if not stripped:
            findings.append(Finding(str(md_file), start, "mermaid-syntax",
                                    "Empty Mermaid block"))
            continue

        lines = stripped.splitlines()
        idx = 0

        # Skip optional YAML config block (---...---)
        if lines[0].strip() == "---":
            idx = 1
            while idx < len(lines) and lines[idx].strip() != "---":
                idx += 1
            idx += 1  # step past closing ---

        # Find first meaningful content line
        diagram_type = None
        while idx < len(lines):
            line = lines[idx].strip()
            if line and not line.startswith("%%"):
                diagram_type = line.split()[0].rstrip(":")
                break
            idx += 1

        if diagram_type is None:
            findings.append(Finding(str(md_file), start, "mermaid-syntax",
                                    "Mermaid block has no diagram type declaration"))
        elif diagram_type not in MERMAID_DIAGRAM_TYPES:
            findings.append(Finding(str(md_file), start + idx, "mermaid-syntax",
                                    f"Unrecognised Mermaid diagram type: '{diagram_type}'"))
    return findings


# ---------------------------------------------------------------------------
# Check 3 — Internal link integrity
# ---------------------------------------------------------------------------

# Patterns that carry URL/path values in MD-DDL files:
#   [text](url)          — standard markdown link (also catches ![alt](url) images)
#   href='url'           — HTML anchor inside Mermaid node labels (single quotes)
#   href="url"           — same, double-quote variant
#
# Not checked here (out of scope for domain preflight):
#   {{INCLUDE: path}}    — agent/skill file directive; not used in domain folders
#   reference-style links [text][ref] / [ref]: url — only found as external URLs in README

_MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
_HREF_RE = re.compile(r'href=["\']([^"\']+)["\']')


def _check_url(url: str, line_num: int, md_file: Path, findings: list[Finding]) -> None:
    """Validate a single URL extracted from md_file at line_num."""
    # Skip external links — not our concern
    if url.startswith(("http://", "https://", "mailto:")):
        return

    # Pure same-page anchor: #heading — verify heading exists in this file
    if url.startswith("#"):
        anchor = url[1:]
        if anchor and _heading_slug(anchor) not in _get_headings(md_file):
            findings.append(Finding(str(md_file), line_num, "internal-links",
                                    f"Broken same-page anchor: '#{anchor}' not found in this file"))
        return

    # File path, with optional anchor
    file_part, anchor = (url.rsplit("#", 1) if "#" in url else (url, None))
    if not file_part:
        return

    target = (md_file.parent / file_part).resolve()
    if not target.exists():
        findings.append(Finding(str(md_file), line_num, "internal-links",
                                f"Broken link: '{file_part}' does not exist"))
    elif anchor:
        if _heading_slug(anchor) not in _get_headings(target):
            findings.append(Finding(str(md_file), line_num, "internal-links",
                                    f"Broken anchor: '#{anchor}' not found in {file_part}"))


def check_internal_links(md_file: Path) -> list[Finding]:
    findings: list[Finding] = []
    lines = _read(md_file).splitlines()

    for line_num, line in enumerate(lines, 1):
        seen: set[str] = set()
        for m in _MD_LINK_RE.finditer(line):
            url = m.group(1).strip()
            if url not in seen:
                seen.add(url)
                _check_url(url, line_num, md_file, findings)
        for m in _HREF_RE.finditer(line):
            url = m.group(1).strip()
            if url not in seen:
                seen.add(url)
                _check_url(url, line_num, md_file, findings)

    return findings


# ---------------------------------------------------------------------------
# Check 4 — Entity reference consistency
# ---------------------------------------------------------------------------

def _entity_names_from_domain(domain_file: Path) -> set[str]:
    """Extract canonical entity names from the ## Entities table in domain.md."""
    names: set[str] = set()
    text = _read(domain_file)
    in_section = False
    in_table = False

    for line in text.splitlines():
        if re.match(r"^##\s+Entities\s*$", line):
            in_section = True
            in_table = False
            continue
        if re.match(r"^##\s+", line) and in_section:
            break
        if in_section:
            if re.match(r"^\s*Name\s*\|", line):
                in_table = True
                continue
            if in_table and "|" in line:
                # Strip separator rows (--- | --- | ...)
                cells = [c.strip() for c in line.split("|") if c.strip()]
                if not cells or re.match(r"^-+$", cells[0]):
                    continue
                name_cell = cells[0]
                lm = re.match(r"\[([^\]]+)\]\([^)]*\)", name_cell)
                name = lm.group(1).strip() if lm else name_cell
                if name:
                    names.add(name)
    return names


def check_entity_references(domain_file: Path) -> list[Finding]:
    """YAML source/target/actor/entity/extends values must name a domain entity."""
    findings: list[Finding] = []
    entity_names = _entity_names_from_domain(domain_file)
    if not entity_names:
        return []

    domain_root = domain_file.parent

    # Check entity and event detail files; skip sources/ (cross-domain references allowed)
    for md_file in domain_root.rglob("*.md"):
        rel = md_file.relative_to(domain_root)
        # Skip sources/ (cross-domain entity refs allowed) and products/
        # (the 'source' key there names a data source system, not an entity)
        if rel.parts and rel.parts[0] in {"sources", "products"}:
            continue

        text = _read(md_file)
        for start, content in _extract_code_blocks(text, "yaml"):
            try:
                data = yaml.safe_load(content)
            except yaml.YAMLError:
                continue  # caught by yaml-syntax check
            if not isinstance(data, dict):
                continue

            block_lines = content.splitlines()
            for key in ENTITY_REF_KEYS:
                value = data.get(key)
                if not isinstance(value, str):
                    continue
                if value in entity_names:
                    continue

                # Find the line number of the key within this block
                key_line = start
                for i, bl in enumerate(block_lines):
                    if re.match(rf"^{re.escape(key)}\s*:", bl):
                        key_line = start + i
                        break

                findings.append(Finding(
                    str(md_file), key_line, "entity-references",
                    f"'{key}: {value}' does not match any entity in domain.md",
                ))
    return findings


# ---------------------------------------------------------------------------
# Check 5 — Domain version field
# ---------------------------------------------------------------------------

def check_domain_version(domain_file: Path) -> list[Finding]:
    findings: list[Finding] = []
    text = _read(domain_file)
    lines = text.splitlines()

    in_metadata = False
    collecting = False
    buf: list[str] = []
    start = 1
    found_block = False

    for i, line in enumerate(lines, 1):
        if re.match(r"^##\s+Metadata\s*$", line):
            in_metadata = True
            continue
        if in_metadata and re.match(r"^##\s+", line):
            in_metadata = False
        if in_metadata and re.match(r"^```yaml\s*$", line):
            collecting = True
            start = i + 1
            buf = []
            continue
        if collecting:
            if re.match(r"^```\s*$", line):
                collecting = False
                in_metadata = False
                found_block = True
                content = "\n".join(buf)
                try:
                    data = yaml.safe_load(content)
                    if not isinstance(data, dict) or "version" not in data:
                        findings.append(Finding(
                            str(domain_file), start, "domain-version",
                            "Metadata YAML block is missing the 'version:' field",
                        ))
                except yaml.YAMLError:
                    pass  # caught by yaml-syntax check
                break
            buf.append(line)

    if not found_block:
        findings.append(Finding(
            str(domain_file), 1, "domain-version",
            "No YAML block found under '## Metadata' — 'version:' field cannot be verified",
        ))
    return findings


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run_preflight(domain_folder: str) -> list[Finding]:
    domain_root = Path(domain_folder).resolve()
    if not domain_root.exists():
        print(f"error: path not found: {domain_folder}", file=sys.stderr)
        sys.exit(2)
    if not domain_root.is_dir():
        print(f"error: not a directory: {domain_folder}", file=sys.stderr)
        sys.exit(2)

    domain_file = domain_root / "domain.md"
    findings: list[Finding] = []

    # Checks 1–3: run across every .md file in the domain folder
    for md_file in sorted(domain_root.rglob("*.md")):
        findings += check_yaml_syntax(md_file)
        findings += check_mermaid_syntax(md_file)
        findings += check_internal_links(md_file)

    # Check 4: entity reference consistency (requires domain.md)
    if domain_file.exists():
        findings += check_entity_references(domain_file)

    # Check 5: domain version (requires domain.md)
    if domain_file.exists():
        findings += check_domain_version(domain_file)
    else:
        findings.append(Finding(
            str(domain_file), 0, "domain-version",
            "domain.md not found — is this a domain folder?",
        ))

    return findings


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python preflight.py <domain-folder>", file=sys.stderr)
        sys.exit(2)

    findings = run_preflight(sys.argv[1])

    if not findings:
        print("Pre-flight passed. No findings.")
        sys.exit(0)

    # Group by check for readability
    by_check: dict[str, list[Finding]] = {}
    for f in findings:
        by_check.setdefault(f.check, []).append(f)

    print(f"Pre-flight: {len(findings)} finding(s)\n")
    for check, group in by_check.items():
        print(f"  [{check}]  {len(group)} finding(s)")
        for f in group:
            path = f.file
            print(f"    {path}:{f.line}")
            print(f"    {f.message}")
        print()

    sys.exit(1)


if __name__ == "__main__":
    main()
