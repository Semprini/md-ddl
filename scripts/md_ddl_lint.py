#!/usr/bin/env python3
"""
MD-DDL Linter

Mechanical conformance checks for an MD-DDL project, implementing the rules in
`linter.md`:

Global
  - All links to markdown (within the same doc or local docs) must resolve.
  - All YAML must be well formed.

Domain
  - All entities, enums and relationships in the overview diagram must be
    reflected in the domain summary tables.
  - All links in the diagram and the tables must resolve to the detail level,
    named consistently with the summary level.

Entity
  - The H1 heading must be a link back to the domain.
  - Outgoing and inheritance relationships in the class diagram must have links
    to the detail markdown.
  - Enums used in attributes must be shown in the diagram.
  - Attributes must be consistent between the diagram and the YAML.

Usage:
    python md_ddl_lint.py <path> [<path> ...] [options]

    <path> may be a domain folder (containing domain.md), a folder containing
    several domain folders, or an individual markdown file.

Options:
    --format text|json   Output format (default: text)
    --strict             Exit non-zero on warnings as well as errors
    --disable RULE,...   Comma-separated rule ids to skip
    --list-rules         Print the rule ids and exit

Requires: Python 3.9+, pyyaml   (pip install pyyaml)

Exit codes:
    0  no findings (or warnings only, without --strict)
    1  one or more errors
    2  usage or invocation error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml
except ImportError:  # pragma: no cover
    print("error: pyyaml is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)


ERROR = "error"
WARNING = "warning"

RULES = {
    "yaml-syntax": "YAML blocks must parse",
    "mermaid-syntax": "Mermaid blocks must declare a recognised diagram type",
    "link-resolve": "Local markdown links and anchors must resolve",
    "entity-references": "YAML entity references must name an entity in the domain",
    "domain-version": "Domain metadata must declare a version",
    "domain-diagram-coverage": "Diagram nodes and edges must appear in the domain tables",
    "domain-table-coverage": "Domain table entries should appear in the overview diagram",
    "domain-link-consistency": "Summary links must reach a detail heading with a matching name",
    "entity-heading-link": "Detail file H1 must link back to the domain",
    "entity-diagram-links": "Outgoing and inheritance targets must link to detail markdown",
    "entity-enum-in-diagram": "Enums used in attributes must appear in the diagram",
    "entity-attribute-consistency": "Diagram attributes must match the YAML attributes",
}

# Mermaid diagram types recognised by the spec.
MERMAID_DIAGRAM_TYPES = {
    "graph", "flowchart", "sequenceDiagram", "classDiagram",
    "stateDiagram", "stateDiagram-v2", "erDiagram", "gantt",
    "journey", "gitGraph", "pie", "quadrantChart", "requirementDiagram",
    "mindmap", "timeline", "block-beta", "packet-beta",
    "xychart-beta", "sankey-beta", "kanban", "architecture-beta",
}

# YAML keys whose value must name an entity declared in the domain.
# 'actor' is deliberately excluded — event actors may be roles or external
# systems rather than MD-DDL entities.
ENTITY_REF_KEYS = ("extends", "source", "target", "entity")

# Folders inside a domain that are not MD-DDL detail definitions.
NON_DETAIL_DIRS = {"baselines"}

# Folders whose YAML 'source:'/'target:' keys do not name domain entities:
# sources/ may reference cross-domain entities, products/ uses 'source:' for
# a feeding system rather than an entity.
NON_ENTITY_REF_DIRS = {"sources", "products", "baselines"}

# Level-2 sections that mark a file as an MD-DDL detail file.
DETAIL_SECTIONS = {"entities", "enums", "relationships", "events", "data products"}


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    file: Path
    line: int
    rule: str
    severity: str
    message: str


class Report:
    def __init__(self, disabled: set[str]):
        self.findings: list[Finding] = []
        self.disabled = disabled

    def add(self, file: Path, line: int, rule: str, severity: str, message: str) -> None:
        if rule in self.disabled:
            return
        self.findings.append(Finding(file, max(line, 1), rule, severity, message))

    def error(self, file: Path, line: int, rule: str, message: str) -> None:
        self.add(file, line, rule, ERROR, message)

    def warn(self, file: Path, line: int, rule: str, message: str) -> None:
        self.add(file, line, rule, WARNING, message)


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

def normalise(name: str | None) -> str:
    """Fold a name to a comparison key: lowercase, alphanumerics only.

    'Party Role', 'PartyRole' and 'party_role' all fold to 'partyrole'.
    """
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def heading_slug(text: str) -> str:
    """GitHub-compatible anchor slug for heading text."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)   # links -> link text
    text = re.sub(r"<[^>]+>", "", text)                    # inline html
    text = re.sub(r"[`*_~]", "", text)                     # emphasis markers
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)                   # punctuation
    return re.sub(r"\s+", "-", text).strip("-")


def link_text_and_target(cell: str) -> tuple[str | None, str | None]:
    """Return (text, target) of the first markdown link in a string."""
    m = re.search(r"\[([^\]]*)\]\(([^)]*)\)", cell)
    if not m:
        return None, None
    return m.group(1).strip(), m.group(2).strip()


def is_external(url: str) -> bool:
    return url.startswith(("http://", "https://", "mailto:", "tel:"))


# ---------------------------------------------------------------------------
# Markdown document model
# ---------------------------------------------------------------------------

FENCE_RE = re.compile(r"^\s*(?P<fence>`{3,}|~{3,})\s*(?P<info>[^\s`~]*)")
HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<text>.*?)\s*#*\s*$")
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HREF_RE = re.compile(r"""href\s*=\s*["']([^"']+)["']""")


@dataclass
class CodeBlock:
    lang: str
    fence_line: int          # 1-indexed line of the opening fence
    body: list[str] = field(default_factory=list)

    @property
    def start_line(self) -> int:
        """1-indexed line of the first body line."""
        return self.fence_line + 1

    @property
    def content(self) -> str:
        return "\n".join(self.body)


@dataclass
class Heading:
    level: int
    text: str
    line: int


class Doc:
    """A parsed markdown file."""

    def __init__(self, path: Path):
        self.path = path
        self.text = path.read_text(encoding="utf-8", errors="replace")
        self.lines = self.text.splitlines()
        self.blocks: list[CodeBlock] = []
        self.code_lines: set[int] = set()
        self._parse_blocks()
        self.headings = self._parse_headings()
        self.slugs = {heading_slug(h.text) for h in self.headings}

    # -- parsing ----------------------------------------------------------

    def _parse_blocks(self) -> None:
        i, n = 0, len(self.lines)
        while i < n:
            m = FENCE_RE.match(self.lines[i])
            if not m:
                i += 1
                continue
            fence = m.group("fence")
            block = CodeBlock(lang=(m.group("info") or "").lower(), fence_line=i + 1)
            j = i + 1
            while j < n:
                m2 = FENCE_RE.match(self.lines[j])
                if (m2 and m2.group("fence")[0] == fence[0]
                        and len(m2.group("fence")) >= len(fence)
                        and not m2.group("info")):
                    break
                block.body.append(self.lines[j])
                j += 1
            self.blocks.append(block)
            self.code_lines.update(range(i + 1, min(j, n - 1) + 2))
            i = j + 1

    def _parse_headings(self) -> list[Heading]:
        out = []
        for idx, line in enumerate(self.lines, 1):
            if idx in self.code_lines:
                continue
            m = HEADING_RE.match(line)
            if m:
                out.append(Heading(len(m.group("hashes")), m.group("text").strip(), idx))
        return out

    # -- queries ----------------------------------------------------------

    def blocks_of(self, lang: str, span: tuple[int, int] | None = None) -> list[CodeBlock]:
        out = []
        for b in self.blocks:
            if b.lang != lang:
                continue
            if span and not (span[0] <= b.fence_line <= span[1]):
                continue
            out.append(b)
        return out

    def section(self, level: int, title: str) -> tuple[int, int] | None:
        """Line span (inclusive) of the first heading at `level` named `title`."""
        key = normalise(title)
        for i, h in enumerate(self.headings):
            if h.level == level and normalise(h.text) == key:
                return (h.line, self._span_end(i))
        return None

    def subsections(self, span: tuple[int, int], level: int) -> list[tuple[Heading, tuple[int, int]]]:
        """All headings at `level` inside `span`, with their own spans."""
        out = []
        for i, h in enumerate(self.headings):
            if h.level == level and span[0] <= h.line <= span[1]:
                end = min(self._span_end(i), span[1])
                out.append((h, (h.line, end)))
        return out

    def _span_end(self, index: int) -> int:
        level = self.headings[index].level
        for nxt in self.headings[index + 1:]:
            if nxt.level <= level:
                return nxt.line - 1
        return len(self.lines)

    def heading_texts_at(self, level: int) -> dict[str, Heading]:
        return {normalise(h.text): h for h in self.headings if h.level == level}


_DOC_CACHE: dict[Path, Doc | None] = {}


def load_doc(path: Path) -> Doc | None:
    key = path.resolve()
    if key not in _DOC_CACHE:
        try:
            _DOC_CACHE[key] = Doc(path)
        except OSError:
            _DOC_CACHE[key] = None
    return _DOC_CACHE[key]


# ---------------------------------------------------------------------------
# Markdown tables
# ---------------------------------------------------------------------------

SEPARATOR_CELL_RE = re.compile(r"^:?-{2,}:?$")


def _split_row(line: str) -> list[str]:
    line = line.strip()
    line = line.removeprefix("|")
    line = line.removesuffix("|")
    return [c.strip() for c in line.split("|")]


@dataclass
class TableRow:
    line: int
    cells: dict[str, str]


def parse_table(doc: Doc, span: tuple[int, int]) -> tuple[list[str], list[TableRow]]:
    """Parse the first markdown table inside `span`."""
    header: list[str] = []
    rows: list[TableRow] = []
    for ln in range(span[0], min(span[1], len(doc.lines)) + 1):
        if ln in doc.code_lines:
            continue
        line = doc.lines[ln - 1]
        if "|" not in line:
            if header and rows:
                break
            continue
        cells = _split_row(line)
        if cells and all(SEPARATOR_CELL_RE.match(c) for c in cells if c):
            continue
        if not header:
            header = cells
            continue
        rows.append(TableRow(ln, dict(zip(header, cells))))
    return header, rows


def column(row: TableRow, *names: str) -> str:
    for name in names:
        for key, value in row.cells.items():
            if normalise(key) == normalise(name):
                return value
    return ""


# ---------------------------------------------------------------------------
# Mermaid: flowchart (domain overview diagram)
# ---------------------------------------------------------------------------

GRAPH_TYPE_RE = re.compile(r"^\s*(graph|flowchart)\b", re.IGNORECASE)
GRAPH_NODE_RE = re.compile(r"(?P<id>[A-Za-z0-9_]+)\s*(?P<open>\[\[|\[\(|\(\(|\[|\(|\{\{|\{|>)(?P<label>[^\]\)\}]*)")
ANCHOR_RE = re.compile(r"<a\s+[^>]*href\s*=\s*[\"']([^\"']+)[\"'][^>]*>(?P<text>.*?)</a>", re.IGNORECASE | re.DOTALL)

ARROW_ALT = r"<-->|<-\.->|-\.->|<-\.-|<==>|<--|<==|-->|==>|-\.-|---|===|--|=="
GRAPH_EDGE_RE = re.compile(
    rf"^\s*(?P<src>[A-Za-z0-9_]+)\s*"
    rf"(?P<arrow>{ARROW_ALT})\s*"
    rf"(?:\|\s*(?P<label>[^|]*?)\s*\|\s*)?"
    rf"(?P<dst>[A-Za-z0-9_]+)\s*$"
)


@dataclass
class GraphNode:
    id: str
    label: str | None = None
    href: str | None = None
    line: int = 0


@dataclass
class GraphEdge:
    src: str
    dst: str
    label: str | None
    line: int


@dataclass
class Flowchart:
    nodes: dict[str, GraphNode] = field(default_factory=dict)
    edges: list[GraphEdge] = field(default_factory=list)
    referenced: dict[str, int] = field(default_factory=dict)   # id -> first line seen


def parse_flowchart(block: CodeBlock) -> Flowchart | None:
    lines = block.body
    if not any(GRAPH_TYPE_RE.match(ln) for ln in lines):
        return None

    chart = Flowchart()
    in_config = False
    for offset, raw in enumerate(lines):
        line_no = block.start_line + offset
        stripped = raw.strip()
        if stripped == "---":
            in_config = not in_config
            continue
        if in_config or not stripped or stripped.startswith("%%"):
            continue
        if GRAPH_TYPE_RE.match(raw) or stripped.startswith(("subgraph", "end", "click", "style", "classDef", "linkStyle")):
            continue

        # Node declarations, possibly inline within an edge.
        remainder = raw
        for m in GRAPH_NODE_RE.finditer(raw):
            node_id, label = m.group("id"), m.group("label").strip()
            href = None
            anchor = ANCHOR_RE.search(label)
            if anchor:
                href = anchor.group(1).strip()
                label = re.sub(r"<[^>]+>", "", anchor.group("text")).strip()
            label = label.strip().strip("\"'").strip()
            existing = chart.nodes.get(node_id)
            if existing is None or (label and not existing.label):
                chart.nodes[node_id] = GraphNode(node_id, label or None, href, line_no)
            chart.referenced.setdefault(node_id, line_no)
            remainder = remainder.replace(m.group(0), node_id)

        edge = GRAPH_EDGE_RE.match(remainder)
        if edge:
            src, dst = edge.group("src"), edge.group("dst")
            chart.edges.append(GraphEdge(src, dst, (edge.group("label") or "").strip() or None, line_no))
            chart.referenced.setdefault(src, line_no)
            chart.referenced.setdefault(dst, line_no)
    return chart


def node_name(chart: Flowchart, node_id: str) -> str:
    node = chart.nodes.get(node_id)
    return (node.label if node and node.label else node_id)


# ---------------------------------------------------------------------------
# Mermaid: classDiagram (entity diagram)
# ---------------------------------------------------------------------------

CLASS_DECL_RE = re.compile(
    r"^\s*class\s+(?P<id>[A-Za-z0-9_]+)\s*"
    r"(?:\[(?P<label>[^\]]*)\])?\s*"
    r"(?P<brace>\{)?\s*(?P<inline>.*)$"
)
CLASS_REL_ALT = r"<\|\.\.|\.\.\|>|<\|--|--\|>|\*--|--\*|o--|--o|<\.\.|\.\.>|<--|-->|\.\.|--"
CLASS_REL_RE = re.compile(
    rf"^\s*(?P<left>[A-Za-z0-9_]+)\s*"
    rf"(?:\"(?P<lcard>[^\"]*)\"\s*)?"
    rf"(?P<arrow>{CLASS_REL_ALT})\s*"
    rf"(?:\"(?P<rcard>[^\"]*)\"\s*)?"
    rf"(?P<right>[A-Za-z0-9_]+)\s*"
    rf"(?::\s*(?P<label>.*))?$"
)
ATTR_RE = re.compile(r"^\s*(?P<marker>[*+\-#~]\s*)?(?P<name>[^:()]+?)\s*:\s*(?P<type>.+?)\s*$")
STEREOTYPE_RE = re.compile(r"<<\s*([^>]+?)\s*>>")


@dataclass
class DiagramAttribute:
    name: str
    type: str
    identifier: bool
    line: int


@dataclass
class MermaidClass:
    id: str
    label: str | None = None
    href: str | None = None
    stereotypes: list[str] = field(default_factory=list)
    attributes: list[DiagramAttribute] = field(default_factory=list)
    line: int = 0

    @property
    def display(self) -> str:
        return self.label or self.id

    @property
    def is_enum(self) -> bool:
        return any(normalise(s) == "enumeration" for s in self.stereotypes)


@dataclass
class ClassRelation:
    left: str
    right: str
    arrow: str
    label: str | None
    line: int


@dataclass
class ClassDiagram:
    classes: dict[str, MermaidClass] = field(default_factory=dict)
    relations: list[ClassRelation] = field(default_factory=list)
    block: CodeBlock | None = None


def _class_for(diagram: ClassDiagram, class_id: str, line: int) -> MermaidClass:
    if class_id not in diagram.classes:
        diagram.classes[class_id] = MermaidClass(id=class_id, line=line)
    return diagram.classes[class_id]


def _apply_label(cls: MermaidClass, label: str) -> None:
    label = label.strip().strip("\"'").strip()
    if not label:
        return
    anchor = ANCHOR_RE.search(label)
    if anchor:
        cls.href = anchor.group(1).strip()
        label = re.sub(r"<[^>]+>", "", anchor.group("text")).strip()
    cls.label = label or cls.label


def _absorb_body_line(cls: MermaidClass, raw: str, line_no: int) -> None:
    stripped = raw.strip().rstrip("}").strip()
    if not stripped:
        return
    for st in STEREOTYPE_RE.findall(stripped):
        cls.stereotypes.append(st)
    stripped = STEREOTYPE_RE.sub("", stripped).strip()
    if not stripped or stripped.endswith(")"):
        return
    m = ATTR_RE.match(stripped)
    if not m:
        return
    marker = (m.group("marker") or "").strip()
    cls.attributes.append(DiagramAttribute(
        name=m.group("name").strip(),
        type=m.group("type").strip(),
        identifier=marker == "*",
        line=line_no,
    ))


def parse_class_diagram(block: CodeBlock) -> ClassDiagram | None:
    lines = block.body
    if not any(ln.strip().startswith("classDiagram") for ln in lines):
        return None

    diagram = ClassDiagram(block=block)
    in_config = False
    open_class: MermaidClass | None = None

    for offset, raw in enumerate(lines):
        line_no = block.start_line + offset
        stripped = raw.strip()
        if stripped == "---":
            in_config = not in_config
            continue
        if in_config:
            continue

        if open_class is not None:
            if stripped.startswith("}"):
                open_class = None
                continue
            _absorb_body_line(open_class, raw, line_no)
            if stripped.endswith("}"):
                open_class = None
            continue

        if not stripped or stripped.startswith(("%%", "classDiagram")):
            continue
        if stripped.startswith(("direction", "note", "click", "style", "cssClass", "namespace")):
            continue

        decl = CLASS_DECL_RE.match(raw)
        if decl:
            cls = _class_for(diagram, decl.group("id"), line_no)
            cls.line = min(cls.line or line_no, line_no)
            if decl.group("label"):
                _apply_label(cls, decl.group("label"))
            inline = (decl.group("inline") or "").strip()
            if decl.group("brace"):
                if inline:
                    _absorb_body_line(cls, inline, line_no)
                if not inline.endswith("}"):
                    open_class = cls
            continue

        rel = CLASS_REL_RE.match(raw)
        if rel:
            left, right = rel.group("left"), rel.group("right")
            _class_for(diagram, left, line_no)
            _class_for(diagram, right, line_no)
            diagram.relations.append(ClassRelation(
                left=left, right=right, arrow=rel.group("arrow"),
                label=(rel.group("label") or "").strip() or None, line=line_no,
            ))
    return diagram


# ---------------------------------------------------------------------------
# YAML helpers
# ---------------------------------------------------------------------------

def load_yaml(block: CodeBlock) -> dict | None:
    try:
        data = yaml.safe_load(block.content)
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def yaml_key_line(block: CodeBlock, *path: str) -> int:
    """Best-effort line number of a (possibly nested) YAML key."""
    line = block.start_line
    depth = 0
    for target in path:
        pattern = re.compile(rf"^\s{{{depth},}}{re.escape(target)}\s*:", re.IGNORECASE)
        for offset, raw in enumerate(block.body):
            if block.start_line + offset < line:
                continue
            if pattern.match(raw):
                line = block.start_line + offset
                depth = len(raw) - len(raw.lstrip()) + 1
                break
    return line


TYPE_ENUM_RE = re.compile(r"^enum[:~]\s*(?P<name>[^~\[\]]+?)\s*~?\s*(?P<card>\[[^\]]*\])?$", re.IGNORECASE)


def canonical_type(raw: str) -> str:
    """Fold a type from either the diagram or the YAML to a comparable form."""
    value = (raw or "").strip().strip("\"'")
    m = TYPE_ENUM_RE.match(value)
    if m:
        return f"enum:{normalise(m.group('name'))}{m.group('card') or ''}"
    return re.sub(r"\s+", "", value.lower())


def enum_name_from_type(raw: str) -> str | None:
    m = TYPE_ENUM_RE.match((raw or "").strip().strip("\"'"))
    return m.group("name").strip() if m else None


# ---------------------------------------------------------------------------
# Link resolution
# ---------------------------------------------------------------------------

def resolve_link(doc: Doc, url: str) -> tuple[Path | None, str | None]:
    """Return (target file, anchor) for a local link; (None, anchor) for same-page."""
    if "#" in url:
        file_part, anchor = url.split("#", 1)
    else:
        file_part, anchor = url, None
    if not file_part:
        return None, anchor
    return (doc.path.parent / unquote(file_part)).resolve(), anchor


def check_link(report: Report, doc: Doc, url: str, line: int, rule: str = "link-resolve") -> Doc | None:
    """Validate one local link. Returns the target Doc when it resolves."""
    if not url.strip() or is_external(url):
        return None

    target_path, anchor = resolve_link(doc, url)
    if target_path is None:                       # same-page anchor
        if anchor and heading_slug(anchor) not in doc.slugs:
            report.error(doc.path, line, rule, f"anchor '#{anchor}' not found in this file")
        return doc

    if not target_path.exists():
        report.error(doc.path, line, rule, f"link target does not exist: '{url}'")
        return None
    if target_path.suffix.lower() != ".md":
        return None

    target = load_doc(target_path)
    if target is None:
        return None
    if anchor and heading_slug(anchor) not in target.slugs:
        report.error(doc.path, line, rule,
                     f"anchor '#{anchor}' not found in {target_path.name}")
    return target


# ---------------------------------------------------------------------------
# Check: YAML syntax (global)
# ---------------------------------------------------------------------------

def check_yaml_syntax(report: Report, doc: Doc) -> None:
    for block in doc.blocks:
        if block.lang not in {"yaml", "yml"}:
            continue
        try:
            yaml.safe_load(block.content)
        except yaml.YAMLError as exc:
            line = block.start_line
            mark = getattr(exc, "problem_mark", None)
            if mark is not None:
                line = block.start_line + mark.line
            problem = getattr(exc, "problem", None) or str(exc).splitlines()[0]
            report.error(doc.path, line, "yaml-syntax", f"YAML parse error: {problem}")


# ---------------------------------------------------------------------------
# Check: Mermaid syntax (global)
# ---------------------------------------------------------------------------

def check_mermaid_syntax(report: Report, doc: Doc) -> None:
    for block in doc.blocks_of("mermaid"):
        if not block.content.strip():
            report.error(doc.path, block.fence_line, "mermaid-syntax", "empty Mermaid block")
            continue

        idx = 0
        lines = block.body
        # Skip an optional leading YAML front-matter config block.
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        if idx < len(lines) and lines[idx].strip() == "---":
            idx += 1
            while idx < len(lines) and lines[idx].strip() != "---":
                idx += 1
            idx += 1

        while idx < len(lines) and (not lines[idx].strip() or lines[idx].strip().startswith("%%")):
            idx += 1

        if idx >= len(lines):
            report.error(doc.path, block.fence_line, "mermaid-syntax",
                         "Mermaid block has no diagram type declaration")
            continue

        declared = lines[idx].strip().split()[0].rstrip(":")
        if declared not in MERMAID_DIAGRAM_TYPES:
            report.error(doc.path, block.start_line + idx, "mermaid-syntax",
                         f"unrecognised Mermaid diagram type: '{declared}'")


# ---------------------------------------------------------------------------
# Check: link resolution (global)
# ---------------------------------------------------------------------------

def check_links(report: Report, doc: Doc) -> None:
    yaml_lines: set[int] = set()
    for block in doc.blocks:
        if block.lang in {"yaml", "yml", "json", "sql", "python", "shell", "bash"}:
            yaml_lines.update(range(block.start_line, block.start_line + len(block.body)))

    for line_no, line in enumerate(doc.lines, 1):
        if line_no in yaml_lines:
            continue
        seen: set[str] = set()
        for m in MD_LINK_RE.finditer(line):
            url = m.group(1).strip()
            if url and url not in seen:
                seen.add(url)
                check_link(report, doc, url, line_no)
        for m in HREF_RE.finditer(line):
            url = m.group(1).strip()
            if url and url not in seen:
                seen.add(url)
                check_link(report, doc, url, line_no)


# ---------------------------------------------------------------------------
# Domain model
# ---------------------------------------------------------------------------

@dataclass
class SummaryEntry:
    name: str
    link: str | None
    line: int
    row: TableRow


@dataclass
class DomainSummary:
    doc: Doc
    entities: dict[str, SummaryEntry] = field(default_factory=dict)
    enums: dict[str, SummaryEntry] = field(default_factory=dict)
    relationships: dict[str, SummaryEntry] = field(default_factory=dict)
    events: dict[str, SummaryEntry] = field(default_factory=dict)
    diagram: Flowchart | None = None
    diagram_line: int = 0


def _read_summary_table(doc: Doc, title: str) -> dict[str, SummaryEntry]:
    span = doc.section(2, title)
    if not span:
        return {}
    _, rows = parse_table(doc, span)
    entries: dict[str, SummaryEntry] = {}
    for row in rows:
        cell = column(row, "Name")
        if not cell:
            continue
        text, target = link_text_and_target(cell)
        name = text or re.sub(r"[`*]", "", cell).strip()
        if not name:
            continue
        entries[normalise(name)] = SummaryEntry(name, target, row.line, row)
    return entries


def read_domain(doc: Doc) -> DomainSummary:
    summary = DomainSummary(doc)
    summary.entities = _read_summary_table(doc, "Entities")
    summary.enums = _read_summary_table(doc, "Enums")
    summary.relationships = _read_summary_table(doc, "Relationships")
    summary.events = _read_summary_table(doc, "Events")
    for block in doc.blocks_of("mermaid"):
        chart = parse_flowchart(block)
        if chart:
            summary.diagram = chart
            summary.diagram_line = block.fence_line
            break
    return summary


def is_domain_file(doc: Doc) -> bool:
    if doc.path.name.lower() == "domain.md":
        return True
    h1 = next((h for h in doc.headings if h.level == 1), None)
    if not h1 or link_text_and_target(h1.text)[1]:
        return False
    return bool(doc.section(2, "Metadata") and doc.section(2, "Entities"))


def is_detail_file(doc: Doc) -> bool:
    return any(normalise(h.text) in {normalise(s) for s in DETAIL_SECTIONS}
               for h in doc.headings if h.level == 2)


# ---------------------------------------------------------------------------
# Check: domain diagram coverage
# ---------------------------------------------------------------------------

IS_A_LABELS = {"isa", "isakindof", "specialises", "specializes", "extends", "subtypeof"}


def _relationship_matches(summary: DomainSummary, src: str, label: str, dst: str) -> bool:
    subject, predicate, obj = normalise(src), normalise(label), normalise(dst)
    for key in summary.relationships:
        if key == subject + predicate + obj:
            return True
        if key.startswith(subject + predicate):
            return True
        if key.startswith(subject) and predicate and predicate in key:
            return True
        if key.startswith(subject) and obj and key.endswith(obj):
            return True
    return False


def check_domain_diagram_coverage(report: Report, summary: DomainSummary) -> None:
    doc, chart = summary.doc, summary.diagram
    if chart is None:
        report.warn(doc.path, 1, "domain-diagram-coverage",
                    "no domain overview diagram (mermaid graph) found")
        return

    known_entities = summary.entities
    known_enums = summary.enums

    # Every node must be declared in the Entities (or Enums) table.
    for node_id, line in sorted(chart.referenced.items(), key=lambda kv: kv[1]):
        name = node_name(chart, node_id)
        key = normalise(name)
        if key in known_entities or key in known_enums:
            continue
        if normalise(node_id) in known_entities or normalise(node_id) in known_enums:
            continue
        report.error(doc.path, line, "domain-diagram-coverage",
                     f"diagram node '{name}' is not listed in the Entities or Enums table")

    # Every edge is either an is-a assertion or a named relationship.
    for edge in chart.edges:
        src_name = node_name(chart, edge.src)
        dst_name = node_name(chart, edge.dst)
        if not edge.label:
            report.warn(doc.path, edge.line, "domain-diagram-coverage",
                        f"unlabelled edge '{src_name} --> {dst_name}' asserts no relationship")
            continue

        if normalise(edge.label) in IS_A_LABELS:
            child = summary.entities.get(normalise(src_name))
            if child is None:
                continue
            specialises = column(child.row, "Specializes", "Specialises")
            declared = link_text_and_target(specialises)[0] or specialises
            if not normalise(declared):
                report.error(doc.path, child.line, "domain-diagram-coverage",
                             f"'{src_name} is a {dst_name}' in the diagram, but the Entities "
                             f"table declares no Specializes value for '{child.name}'")
            elif normalise(declared) != normalise(dst_name):
                report.error(doc.path, child.line, "domain-diagram-coverage",
                             f"'{src_name}' specialises '{declared}' in the Entities table "
                             f"but '{dst_name}' in the diagram")
            continue

        if not _relationship_matches(summary, src_name, edge.label, dst_name):
            report.warn(doc.path, edge.line, "domain-diagram-coverage",
                        f"edge '{src_name} --{edge.label}--> {dst_name}' does not match any "
                        f"entry in the Relationships table")


def check_domain_table_coverage(report: Report, summary: DomainSummary) -> None:
    chart = summary.diagram
    if chart is None:
        return
    drawn = {normalise(node_name(chart, nid)) for nid in chart.referenced}
    drawn |= {normalise(nid) for nid in chart.referenced}
    for key, entry in summary.entities.items():
        if key not in drawn:
            report.warn(summary.doc.path, entry.line, "domain-table-coverage",
                        f"entity '{entry.name}' does not appear in the domain overview diagram")


# ---------------------------------------------------------------------------
# Check: domain link consistency
# ---------------------------------------------------------------------------

def _detail_heading_matches(target: Doc, anchor: str) -> str | None:
    """Return the detail heading text when the anchor resolves; None otherwise."""
    slug = heading_slug(anchor)
    for h in target.headings:
        if heading_slug(h.text) == slug:
            return h.text
    return None


def _check_summary_link(report: Report, doc: Doc, entry: SummaryEntry, kind: str) -> None:
    if not entry.link:
        report.error(doc.path, entry.line, "domain-link-consistency",
                     f"{kind} '{entry.name}' has no link to its detail definition")
        return
    if is_external(entry.link):
        report.warn(doc.path, entry.line, "domain-link-consistency",
                    f"{kind} '{entry.name}' links to an external URL instead of a local detail definition")
        return

    target_path, anchor = resolve_link(doc, entry.link)
    target = doc if target_path is None else load_doc(target_path) if target_path.exists() else None
    if target is None:
        return  # link-resolve reports the broken path

    if not anchor:
        report.warn(doc.path, entry.line, "domain-link-consistency",
                    f"{kind} '{entry.name}' links to a file with no detail anchor")
        return

    heading = _detail_heading_matches(target, anchor)
    if heading is None:
        return  # link-resolve reports the broken anchor
    if normalise(heading) != normalise(entry.name):
        report.error(doc.path, entry.line, "domain-link-consistency",
                     f"{kind} '{entry.name}' links to detail heading '{heading}' — "
                     f"summary and detail names must match")


def check_domain_link_consistency(report: Report, summary: DomainSummary) -> None:
    doc = summary.doc
    for kind, entries in (("entity", summary.entities), ("enum", summary.enums),
                          ("relationship", summary.relationships), ("event", summary.events)):
        for entry in entries.values():
            _check_summary_link(report, doc, entry, kind)

    chart = summary.diagram
    if chart is None:
        return
    # Not every node needs a link (see guides/diagram-style.md); but where one is
    # present it must agree with the summary table.
    for node in sorted(chart.nodes.values(), key=lambda n: n.line):
        if not node.href:
            continue
        name = node_name(chart, node.id)
        entry = summary.entities.get(normalise(name)) or summary.enums.get(normalise(name))
        if is_external(node.href) or entry is None or not entry.link or is_external(entry.link):
            continue
        node_target, _ = resolve_link(doc, node.href)
        table_target, _ = resolve_link(doc, entry.link)
        if node_target and table_target and node_target != table_target:
            report.error(doc.path, node.line, "domain-link-consistency",
                         f"diagram node '{name}' links to '{node.href}' but the summary table "
                         f"links to '{entry.link}'")


# ---------------------------------------------------------------------------
# Check: entity reference consistency
# ---------------------------------------------------------------------------

def check_entity_references(report: Report, doc: Doc, summary: DomainSummary) -> None:
    """`extends`/`source`/`target`/`entity` values must name a declared entity."""
    if not summary.entities:
        return

    for block in doc.blocks_of("yaml"):
        data = load_yaml(block)
        if not data:
            continue
        for key in ENTITY_REF_KEYS:
            value = data.get(key)
            if not isinstance(value, str) or not value.strip():
                continue
            if normalise(value) in summary.entities:
                continue
            report.error(doc.path, yaml_key_line(block, key), "entity-references",
                         f"'{key}: {value}' does not name an entity declared in "
                         f"{summary.doc.path.name}")


# ---------------------------------------------------------------------------
# Check: domain metadata version field
# ---------------------------------------------------------------------------

def check_domain_version(report: Report, summary: DomainSummary) -> None:
    doc = summary.doc
    span = doc.section(2, "Metadata")
    if span is None:
        report.error(doc.path, 1, "domain-version",
                     "no '## Metadata' section — the domain 'version:' cannot be verified")
        return

    blocks = doc.blocks_of("yaml", span) + doc.blocks_of("json", span)
    if not blocks:
        report.error(doc.path, span[0], "domain-version",
                     "no YAML block under '## Metadata' — the domain 'version:' cannot be verified")
        return

    for block in blocks:
        data = load_yaml(block) if block.lang == "yaml" else _load_json(block)
        if data is None:
            return   # unparseable — yaml-syntax already reports it
        if "version" in data:
            return
    report.error(doc.path, blocks[0].fence_line, "domain-version",
                 "domain metadata does not declare a 'version:' field")


def _load_json(block: CodeBlock) -> dict | None:
    try:
        data = json.loads(block.content)
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


# ---------------------------------------------------------------------------
# Check: entity file heading links back to the domain
# ---------------------------------------------------------------------------

def check_entity_heading_link(report: Report, doc: Doc, domain_doc: Doc) -> None:
    h1 = next((h for h in doc.headings if h.level == 1), None)
    if h1 is None:
        report.error(doc.path, 1, "entity-heading-link",
                     "detail file has no level-1 heading linking back to the domain")
        return

    _, target = link_text_and_target(h1.text)
    if not target:
        report.error(doc.path, h1.line, "entity-heading-link",
                     f"level-1 heading '{h1.text}' must be a link back to the domain "
                     f"(e.g. '# [{h1.text}]({_relative(doc.path, domain_doc.path)})')")
        return
    if is_external(target):
        report.warn(doc.path, h1.line, "entity-heading-link",
                    "level-1 heading links to an external URL rather than the local domain file")
        return

    resolved, _ = resolve_link(doc, target)
    if resolved != domain_doc.path.resolve():
        report.error(doc.path, h1.line, "entity-heading-link",
                     f"level-1 heading links to '{target}', not to the domain file "
                     f"'{_relative(doc.path, domain_doc.path)}'")


def _relative(source: Path, target: Path) -> str:
    try:
        import os
        return os.path.relpath(target, source.parent).replace("\\", "/")
    except ValueError:
        return str(target)


# ---------------------------------------------------------------------------
# Checks: entity detail sections
# ---------------------------------------------------------------------------

INHERITANCE_ARROWS = {"--|>", "<|--", "..|>", "<|.."}
OUTGOING_ARROWS = {"-->", "..>"}
INCOMING_ARROWS = {"<--", "<.."}


def _subject_class(diagram: ClassDiagram, entity_name: str) -> MermaidClass | None:
    key = normalise(entity_name)
    for cls in diagram.classes.values():
        if normalise(cls.id) == key or normalise(cls.display) == key:
            return cls
    return None


def _entity_yaml(doc: Doc, span: tuple[int, int]) -> CodeBlock | None:
    for block in doc.blocks_of("yaml", span):
        data = load_yaml(block)
        if data and "attributes" in data:
            return block
    return None


def check_entity_section(report: Report, doc: Doc, heading: Heading, span: tuple[int, int]) -> None:
    diagrams = [d for d in (parse_class_diagram(b) for b in doc.blocks_of("mermaid", span)) if d]
    yaml_block = _entity_yaml(doc, span)
    data = load_yaml(yaml_block) if yaml_block else None

    if not diagrams:
        if data is not None:
            report.warn(doc.path, heading.line, "entity-attribute-consistency",
                        f"entity '{heading.text}' has no classDiagram to check against its YAML")
        return
    diagram = diagrams[0]
    subject = _subject_class(diagram, heading.text)

    _check_diagram_links(report, doc, heading, diagram, subject)
    if yaml_block is not None and data is not None:
        _check_enums_in_diagram(report, doc, heading, diagram, data, yaml_block)
        _check_attribute_consistency(report, doc, heading, diagram, subject, data, yaml_block)


def _check_diagram_links(report: Report, doc: Doc, heading: Heading,
                         diagram: ClassDiagram, subject: MermaidClass | None) -> None:
    """Outgoing and inheritance targets must link to their detail markdown."""
    if subject is None:
        report.warn(doc.path, heading.line, "entity-diagram-links",
                    f"no class named '{heading.text}' found in the diagram for this entity")
        return

    needs_link: dict[str, tuple[str, int]] = {}   # class id -> (kind, line)
    optional: dict[str, tuple[str, int]] = {}

    for rel in diagram.relations:
        if rel.arrow in INHERITANCE_ARROWS:
            child, parent = (rel.left, rel.right) if rel.arrow in {"--|>", "..|>"} else (rel.right, rel.left)
            other = parent if child == subject.id else child if parent == subject.id else None
            kind = "inheritance"
        elif rel.arrow in OUTGOING_ARROWS:
            other = rel.right if rel.left == subject.id else None
            kind = "outgoing relationship"
        elif rel.arrow in INCOMING_ARROWS:
            other = rel.left if rel.right == subject.id else None
            kind = "incoming relationship"
        else:
            other, kind = None, "association"
            if subject.id in (rel.left, rel.right):
                other = rel.right if rel.left == subject.id else rel.left

        if other is None or other == subject.id:
            continue
        if kind in {"inheritance", "outgoing relationship"}:
            needs_link.setdefault(other, (kind, rel.line))
        else:
            optional.setdefault(other, (kind, rel.line))

    for class_id, (kind, line) in sorted(needs_link.items(), key=lambda kv: kv[1][1]):
        cls = diagram.classes.get(class_id)
        display = cls.display if cls else class_id
        if cls is None or not cls.href:
            report.error(doc.path, line, "entity-diagram-links",
                         f"{kind} target '{display}' has no link to its detail markdown "
                         f"(declare it as: class {class_id}[\"<a href='...'>{display}</a>\"])")

    for class_id, (kind, line) in sorted(optional.items(), key=lambda kv: kv[1][1]):
        if class_id in needs_link:
            continue
        cls = diagram.classes.get(class_id)
        if cls is None or not cls.href:
            report.warn(doc.path, line, "entity-diagram-links",
                        f"referenced class '{cls.display if cls else class_id}' has no link to "
                        f"its detail markdown")


def _check_enums_in_diagram(report: Report, doc: Doc, heading: Heading, diagram: ClassDiagram,
                            data: dict, yaml_block: CodeBlock) -> None:
    """Every enum used by an attribute must be shown in the diagram."""
    attributes = data.get("attributes")
    if not isinstance(attributes, dict):
        return

    declared = {normalise(c.id) for c in diagram.classes.values()}
    declared |= {normalise(c.display) for c in diagram.classes.values()}
    linked = {normalise(c.id) for c in diagram.classes.values() if c.href}
    linked |= {normalise(c.display) for c in diagram.classes.values() if c.href}

    for attr_name, spec in attributes.items():
        raw_type = spec.get("type") if isinstance(spec, dict) else spec
        enum_name = enum_name_from_type(str(raw_type or ""))
        if not enum_name:
            continue
        line = yaml_key_line(yaml_block, "attributes", str(attr_name))
        key = normalise(enum_name)
        if key not in declared:
            report.error(doc.path, line, "entity-enum-in-diagram",
                         f"attribute '{attr_name}' uses enum '{enum_name}', which is not declared "
                         f"in the '{heading.text}' diagram (add: class {re.sub(r'[^A-Za-z0-9]', '', enum_name)}"
                         f"[\"<a href='...'>{enum_name}</a>\"]{{<<enumeration>>}})")
        elif key not in linked:
            report.warn(doc.path, line, "entity-enum-in-diagram",
                        f"enum '{enum_name}' is shown in the diagram but has no link to its "
                        f"detail definition")


def _check_attribute_consistency(report: Report, doc: Doc, heading: Heading, diagram: ClassDiagram,
                                 subject: MermaidClass | None, data: dict,
                                 yaml_block: CodeBlock) -> None:
    if subject is None:
        return
    attributes = data.get("attributes")
    if not isinstance(attributes, dict):
        return

    inherits = bool(data.get("extends"))
    yaml_attrs = {normalise(k): (str(k), v) for k, v in attributes.items()}
    diagram_attrs = {normalise(a.name): a for a in subject.attributes}

    for key, attr in diagram_attrs.items():
        if key in yaml_attrs:
            continue
        message = (f"attribute '{attr.name}' appears in the '{heading.text}' diagram but not in "
                   f"its YAML definition")
        if inherits:
            report.warn(doc.path, attr.line, "entity-attribute-consistency",
                        message + f" — inherited from '{data['extends']}'?")
        else:
            report.error(doc.path, attr.line, "entity-attribute-consistency", message)

    for key, (name, spec) in yaml_attrs.items():
        if key in diagram_attrs:
            continue
        report.error(doc.path, yaml_key_line(yaml_block, "attributes", name),
                     "entity-attribute-consistency",
                     f"attribute '{name}' is defined in YAML but not shown in the "
                     f"'{heading.text}' diagram")

    for key, attr in diagram_attrs.items():
        if key not in yaml_attrs:
            continue
        name, spec = yaml_attrs[key]
        line = yaml_key_line(yaml_block, "attributes", name)
        yaml_type = spec.get("type") if isinstance(spec, dict) else spec
        if yaml_type and canonical_type(attr.type) != canonical_type(str(yaml_type)):
            report.error(doc.path, line, "entity-attribute-consistency",
                         f"attribute '{name}' is '{yaml_type}' in YAML but '{attr.type}' in the diagram")
        declared = spec.get("identifier") if isinstance(spec, dict) else None
        is_primary = str(declared or "").strip().lower() == "primary"
        if is_primary and not attr.identifier:
            report.warn(doc.path, attr.line, "entity-attribute-consistency",
                        f"attribute '{name}' is the primary identifier in YAML but is not "
                        f"prefixed with '*' in the diagram")
        elif attr.identifier and not _truthy_identifier(declared):
            report.warn(doc.path, line, "entity-attribute-consistency",
                        f"attribute '{name}' is marked as an identifier ('*') in the diagram but "
                        f"declares no 'identifier:' in YAML")


def _truthy_identifier(value: object) -> bool:
    """An attribute is an identifier for any declared, non-false `identifier:` value."""
    if value is None or value is False:
        return False
    return str(value).strip().lower() not in {"", "false", "none", "no"}


# ---------------------------------------------------------------------------
# Project traversal
# ---------------------------------------------------------------------------

def markdown_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md") if p.is_file())


def lint_domain(report: Report, domain_file: Path, only: set[Path] | None = None) -> None:
    domain_root = domain_file.parent
    domain_doc = load_doc(domain_file)
    if domain_doc is None:
        report.error(domain_file, 1, "yaml-syntax", "could not read domain file")
        return

    summary = read_domain(domain_doc)

    for path in markdown_files(domain_root):
        if only is not None and path.resolve() not in only:
            continue
        doc = load_doc(path)
        if doc is None:
            continue

        check_yaml_syntax(report, doc)
        check_mermaid_syntax(report, doc)
        check_links(report, doc)

        rel_parts = path.relative_to(domain_root).parts
        if not (rel_parts and rel_parts[0] in NON_ENTITY_REF_DIRS):
            check_entity_references(report, doc, summary)

        if path.resolve() == domain_file.resolve():
            check_domain_version(report, summary)
            check_domain_diagram_coverage(report, summary)
            check_domain_table_coverage(report, summary)
            check_domain_link_consistency(report, summary)
            continue

        if rel_parts and rel_parts[0] in NON_DETAIL_DIRS:
            continue
        if not is_detail_file(doc):
            continue

        check_entity_heading_link(report, doc, domain_doc)

        entities_span = doc.section(2, "Entities")
        if entities_span:
            for heading, span in doc.subsections(entities_span, 3):
                check_entity_section(report, doc, heading, span)


def discover_targets(paths: Iterable[str]) -> tuple[list[Path], dict[Path, set[Path]]]:
    """Map each requested path onto the domain(s) it belongs to."""
    domains: list[Path] = []
    file_filter: dict[Path, set[Path]] = {}

    for raw in paths:
        p = Path(raw).resolve()
        if not p.exists():
            print(f"error: path not found: {raw}", file=sys.stderr)
            sys.exit(2)

        if p.is_file():
            domain_file = _find_domain_file(p.parent)
            if domain_file is None:
                print(f"error: no domain.md found above {raw}", file=sys.stderr)
                sys.exit(2)
            if domain_file not in domains:
                domains.append(domain_file)
            file_filter.setdefault(domain_file, set()).add(p)
            continue

        local = p / "domain.md"
        if local.exists():
            found = [local]
        else:
            found = sorted(f.resolve() for f in p.rglob("domain.md"))
        if not found:
            print(f"error: no domain.md found in or under {raw}", file=sys.stderr)
            sys.exit(2)
        for f in found:
            if f not in domains:
                domains.append(f)

    return domains, file_filter


def _find_domain_file(start: Path) -> Path | None:
    current = start.resolve()
    while True:
        candidate = current / "domain.md"
        if candidate.exists():
            return candidate.resolve()
        if current.parent == current:
            return None
        current = current.parent


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_text(findings: list[Finding], base: Path) -> None:
    if not findings:
        print("MD-DDL lint: no findings.")
        return

    by_file: dict[Path, list[Finding]] = {}
    for f in findings:
        by_file.setdefault(f.file, []).append(f)

    errors = sum(1 for f in findings if f.severity == ERROR)
    warnings = len(findings) - errors

    for path in sorted(by_file):
        try:
            shown = path.resolve().relative_to(base)
        except ValueError:
            shown = path
        print(f"\n{shown}")
        for f in sorted(by_file[path], key=lambda x: (x.line, x.rule)):
            print(f"  {f.line:>5}  {f.severity:<7} {f.rule:<30} {f.message}")

    print(f"\n{errors} error(s), {warnings} warning(s)")


def print_json(findings: list[Finding]) -> None:
    print(json.dumps([
        {
            "file": str(f.file),
            "line": f.line,
            "column": 1,
            "severity": f.severity,
            "rule": f.rule,
            "message": f.message,
        }
        for f in findings
    ], indent=2))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lint an MD-DDL project.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="*", default=["."],
                        help="domain folder, parent folder, or individual markdown file")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--strict", action="store_true",
                        help="exit non-zero on warnings as well as errors")
    parser.add_argument("--disable", default="",
                        help="comma-separated rule ids to skip")
    parser.add_argument("--list-rules", action="store_true",
                        help="print available rule ids and exit")
    args = parser.parse_args()

    if args.list_rules:
        width = max(len(r) for r in RULES)
        for rule, description in RULES.items():
            print(f"{rule:<{width}}  {description}")
        sys.exit(0)

    disabled = {r.strip() for r in args.disable.split(",") if r.strip()}
    unknown = disabled - set(RULES)
    if unknown:
        print(f"error: unknown rule id(s): {', '.join(sorted(unknown))}", file=sys.stderr)
        sys.exit(2)

    domains, file_filter = discover_targets(args.paths or ["."])
    report = Report(disabled)
    for domain_file in domains:
        lint_domain(report, domain_file, file_filter.get(domain_file))

    findings = sorted(report.findings, key=lambda f: (str(f.file), f.line, f.rule))
    if args.format == "json":
        print_json(findings)
    else:
        print_text(findings, Path.cwd().resolve())

    if any(f.severity == ERROR for f in findings):
        sys.exit(1)
    if args.strict and findings:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
