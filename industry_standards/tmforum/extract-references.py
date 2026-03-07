"""
TM Forum SID v4 Reference Extractor
=====================================
Downloads TM Forum Open API JSON schemas from GitHub, then extracts
clean markdown reference files for the agent-ontology standards-alignment skill.

Usage:
    python industry_standards/tmforum/extract-references.py                  # generate from already-downloaded schemas
    python industry_standards/tmforum/extract-references.py --download       # download schemas first, then generate

Output directory:
    agents/agent-ontology/skills/standards-alignment/standards/tmforum/

Schema cache:
    industry_standards/tmforum/v4/schemas/<Domain>/*.schema.json

Source:
    https://github.com/tmforum-apis/Open_Api_And_Data_Model  (Apache 2.0)
"""

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMA_DIR = REPO_ROOT / "industry_standards" / "tmforum" / "v4" / "schemas"
OUTPUT_DIR = (
    REPO_ROOT
    / "agents"
    / "agent-ontology"
    / "skills"
    / "standards-alignment"
    / "standards"
    / "tmforum"
)

GITHUB_RAW = "https://raw.githubusercontent.com/tmforum-apis/Open_Api_And_Data_Model/master/schemas"
GITHUB_API = (
    "https://api.github.com/repos/tmforum-apis/Open_Api_And_Data_Model/contents/schemas"
)

# SID domains present in the GitHub repo schemas directory
SID_DOMAINS = [
    "Analytics",
    "Common",
    "Customer",
    "Customer360",
    "EngagedParty",
    "Iot",
    "MarketingSales",
    "Product",
    "Resource",
    "Service",
]

# ---------------------------------------------------------------------------
# Core SID Entities — selected for detail extraction
# ---------------------------------------------------------------------------
# Selection criteria:
#   - Entities commonly encountered in telecoms domain modelling
#   - Abstract base types that form inheritance roots
#   - Entities that map to common MD-DDL concepts (party, product, service, etc.)
#   - Covers party, customer, product, service, resource, agreement, order,
#     account, payment, and common base families

CORE_ENTITIES = [
    # EngagedParty — Party family
    "Party",
    "Individual",
    "Organization",
    "PartyRole",
    "Partner",
    "Partnership",
    "Contact",
    "DigitalIdentity",
    "Credential",
    # EngagedParty — Account and Agreement
    "Account",
    "Agreement",
    "AgreementSpecification",
    # Customer domain
    "Customer",
    "BillingAccount",
    "CustomerBill",
    "Payment",
    "PaymentMethod",
    "ProductOrder",
    "ShoppingCart",
    "Quote",
    # Product domain
    "Product",
    "ProductOffering",
    "ProductSpecification",
    "Catalog",
    "Category",
    "Usage",
    "Promotion",
    # Service domain
    "Service",
    "ServiceSpecification",
    "ServiceOrder",
    "ServiceCatalog",
    "ServiceCandidate",
    "ServiceQualification",
    # Resource domain
    "Resource",
    "ResourceSpecification",
    "ResourceOrder",
    "ResourceCatalog",
    "LogicalResource",
    "PhysicalResource",
    # Common — base types and shared
    "GeographicAddress",
    "GeographicSite",
    "GeographicLocation",
    "ContactMedium",
    "TroubleTicket",
    "Document",
    "Notification",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def first_sentence(text: str | None) -> str:
    """Return the first sentence (or first 200 chars) of a description."""
    if not text:
        return ""
    text = text.strip().replace("\n", " ").replace("\r", " ")
    while "  " in text:
        text = text.replace("  ", " ")
    for sep in (". ", ".\n"):
        idx = text.find(sep)
        if 0 < idx < 200:
            return text[: idx + 1]
    return text[:200].rstrip()


def escape_md(text: str) -> str:
    """Escape pipe characters for markdown table cells."""
    return text.replace("|", "\\|").replace("\n", " ")


def write_file(name: str, content: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / name
    path.write_text(content, encoding="utf-8")
    lines = content.count("\n") + 1
    print(f"  wrote {path.relative_to(REPO_ROOT)}  ({lines} lines)")


# ---------------------------------------------------------------------------
# Schema loading and parsing
# ---------------------------------------------------------------------------


def load_all_schemas() -> list[dict]:
    """Load all .schema.json files across all SID domains.

    Returns a list of dicts with keys:
        name, domain, description, properties, inherits, file_path
    """
    entities = []

    for domain in SID_DOMAINS:
        domain_dir = SCHEMA_DIR / domain
        if not domain_dir.exists():
            continue

        for schema_file in sorted(domain_dir.glob("*.schema.json")):
            entity = parse_schema_file(schema_file, domain)
            if entity:
                entities.append(entity)

    return entities


def parse_schema_file(path: Path, domain: str) -> dict | None:
    """Parse a single JSON schema file into a normalized entity dict."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

    title = data.get("title", "")
    if not title:
        return None

    definitions = data.get("definitions", {})
    if not definitions:
        return None

    # The main definition matches the title
    defn = definitions.get(title)
    if not defn:
        # Try first definition
        defn = next(iter(definitions.values()), None)
    if not defn:
        return None

    description = defn.get("description", "")

    # Extract properties
    properties = []
    for prop_name, prop_def in (defn.get("properties") or {}).items():
        prop_type = _resolve_type(prop_def)
        prop_desc = prop_def.get("description", "")
        is_array = prop_def.get("type") == "array"
        properties.append(
            {
                "name": prop_name,
                "type": prop_type,
                "description": prop_desc,
                "is_array": is_array,
            }
        )

    # Extract inheritance from allOf
    inherits = []
    for ref_item in defn.get("allOf") or []:
        ref = ref_item.get("$ref", "")
        if ref:
            # Extract just the class name from ../Domain/Class.schema.json#Class
            ref_name = ref.split("#")[-1] if "#" in ref else ""
            if not ref_name:
                ref_name = ref.split("/")[-1].replace(".schema.json", "")
            inherits.append(ref_name)

    return {
        "name": title,
        "domain": domain,
        "description": description,
        "properties": properties,
        "inherits": inherits,
        "file_name": path.name,
    }


def _resolve_type(prop_def: dict) -> str:
    """Resolve a property definition to a human-readable type string."""
    # Direct type
    if "type" in prop_def and prop_def["type"] != "array":
        t = prop_def["type"]
        fmt = prop_def.get("format", "")
        if fmt:
            return f"{t} ({fmt})"
        return t

    # Array of refs
    if prop_def.get("type") == "array":
        items = prop_def.get("items", {})
        if "$ref" in items:
            ref_name = (
                items["$ref"].split("#")[-1]
                if "#" in items["$ref"]
                else items["$ref"].split("/")[-1].replace(".schema.json", "")
            )
            return f"{ref_name}[]"
        return f"{items.get('type', 'object')}[]"

    # Direct $ref
    if "$ref" in prop_def:
        ref = prop_def["$ref"]
        ref_name = (
            ref.split("#")[-1]
            if "#" in ref
            else ref.split("/")[-1].replace(".schema.json", "")
        )
        return ref_name

    return "object"


def is_ref_wrapper(name: str) -> bool:
    """Return True if this entity is a reference wrapper (not a standalone entity)."""
    lower = name.lower()
    return (
        lower.endswith("ref")
        or lower.endswith("reforvalue")
        or lower.endswith("refOrValue".lower())
    )


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------


def generate_sid_entities(entities: list[dict]) -> str:
    """Generate sid-entities.md — searchable index of all SID entities."""
    # Filter out Ref/RefOrValue wrappers and state types
    filtered = [
        e
        for e in entities
        if not is_ref_wrapper(e["name"])
        and not e["name"].endswith("StateType")
        and not e["name"].endswith("ActionType")
        and not e["name"].endswith("StatusType")
        and not e["name"].startswith("Target")
        and not e["name"].startswith(".")  # hidden files
    ]
    filtered.sort(key=lambda e: (e["domain"], e["name"]))

    lines = [
        "# TM Forum SID v4 — Entity Index",
        "",
        f"Auto-generated index of {len(filtered)} SID entities (excluding Ref wrappers",
        "and state/action/status types) from TM Forum Open API Data Model v4.0.0.",
        "Use this file for name-matching when mapping MD-DDL entities to TM Forum SID.",
        "",
        "Name | SID Domain | Description",
        "--- | --- | ---",
    ]

    for e in filtered:
        name = escape_md(e["name"])
        domain = escape_md(e["domain"])
        desc = escape_md(first_sentence(e["description"]))
        lines.append(f"{name} | {domain} | {desc}")

    lines.append("")
    return "\n".join(lines)


def generate_sid_domains(entities: list[dict]) -> str:
    """Generate sid-domains.md — SID domain taxonomy."""
    # Group entities by domain
    by_domain: dict[str, list[dict]] = {}
    for e in entities:
        by_domain.setdefault(e["domain"], []).append(e)

    # Domain descriptions
    domain_desc = {
        "Analytics": "Data analytics, AI models, and performance measurement entities.",
        "Common": "Shared base types, geographic/address entities, events, documents, and cross-domain utilities.",
        "Customer": "Customer management, billing, payment, ordering, quotes, shopping carts, and risk assessment.",
        "Customer360": "Unified customer view aggregating data from multiple domains.",
        "EngagedParty": "Party (Individual/Organization), Party Roles, Accounts, Agreements, Partnerships, and identity management.",
        "Iot": "Internet of Things device management and telemetry.",
        "MarketingSales": "Market segments, competitors, sales leads, and loyalty programs.",
        "Product": "Product catalog, offerings, specifications, inventory, usage, and promotions.",
        "Resource": "Physical and logical resources, resource catalog, alarms, and inventory.",
        "Service": "Service catalog, specifications, orders, problems, tests, and qualification.",
    }

    lines = [
        "# TM Forum SID v4 — Domain Taxonomy",
        "",
        "The SID (Shared Information/Data) model organises telecoms entities into",
        "functional domains. Each domain groups related entity families.",
        "",
        "Source: TM Forum Open API Data Model v4.0.0 (Apache 2.0)",
        "",
    ]

    for domain in SID_DOMAINS:
        domain_entities = by_domain.get(domain, [])
        # Filter out wrappers for the domain view
        core = [
            e
            for e in domain_entities
            if not is_ref_wrapper(e["name"])
            and not e["name"].endswith("StateType")
            and not e["name"].endswith("ActionType")
            and not e["name"].endswith("StatusType")
            and not e["name"].startswith("Target")
            and not e["name"].startswith(".")
        ]
        core.sort(key=lambda e: e["name"])

        desc = domain_desc.get(domain, "")

        lines.append(f"## {domain}")
        lines.append("")
        if desc:
            lines.append(f"> {desc}")
            lines.append("")
        lines.append(
            f"**{len(core)} entities** (excluding Ref wrappers and state types)"
        )
        lines.append("")

        if core:
            lines.append("Entity | Description")
            lines.append("--- | ---")
            for e in core:
                name = escape_md(e["name"])
                edesc = escape_md(first_sentence(e["description"]))
                lines.append(f"{name} | {edesc}")
            lines.append("")

    return "\n".join(lines)


def generate_sid_entities_detail(entities: list[dict]) -> str:
    """Generate sid-entities-detail.md — core entities with full properties."""
    # Build lookup by name
    by_name = {e["name"]: e for e in entities}

    lines = [
        "# TM Forum SID v4 — Core Entity Detail",
        "",
        f"Detailed definitions for {len(CORE_ENTITIES)} core SID entities,",
        "including inheritance chains and property tables.",
        "",
    ]

    found = 0
    missing = []

    for name in CORE_ENTITIES:
        entity = by_name.get(name)
        if not entity:
            missing.append(name)
            continue

        found += 1
        lines.append(f"## {entity['name']}")
        lines.append("")
        if entity["description"]:
            lines.append(f"> {escape_md(entity['description'])}")
            lines.append("")

        # Metadata
        meta_parts = [f"**SID Domain:** {entity['domain']}"]
        if entity["inherits"]:
            meta_parts.append(f"**Extends:** {', '.join(entity['inherits'])}")
        lines.append(" | ".join(meta_parts))
        lines.append("")

        # Properties table
        if entity["properties"]:
            lines.append("Property | Type | Description")
            lines.append("--- | --- | ---")
            for prop in entity["properties"]:
                pname = escape_md(prop["name"])
                ptype = escape_md(prop["type"])
                pdesc = escape_md(first_sentence(prop["description"]))
                lines.append(f"{pname} | {ptype} | {pdesc}")
            lines.append("")
        else:
            lines.append("*Properties inherited from parent type(s).*")
            lines.append("")

    if missing:
        lines.append("## Entities Not Found in Schema Cache")
        lines.append("")
        lines.append(
            "The following core entities were not found in the downloaded schemas."
        )
        lines.append(
            "They may use different names or may not exist as standalone schemas."
        )
        lines.append("")
        for m in missing:
            lines.append(f"- {m}")
        lines.append("")

    # Update count in header
    lines[2] = (
        f"Detailed definitions for {found} core SID entities (of {len(CORE_ENTITIES)} requested),"
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Schema Downloader
# ---------------------------------------------------------------------------


def download_schemas() -> None:
    """Download all .schema.json files from the TM Forum GitHub repo."""
    print("Downloading TM Forum schemas from GitHub...")
    print(f"  target: {SCHEMA_DIR}")
    print()

    total_downloaded = 0
    total_skipped = 0
    total_failed = 0

    for domain in SID_DOMAINS:
        domain_dir = SCHEMA_DIR / domain
        domain_dir.mkdir(parents=True, exist_ok=True)

        # List files in domain directory via GitHub API
        api_url = f"{GITHUB_API}/{domain}"
        print(f"  [{domain}] listing files...", end=" ", flush=True)

        try:
            req = urllib.request.Request(
                api_url,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "md-ddl-extractor/1.0",
                },
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                files = json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            print(f"FAILED ({exc})")
            total_failed += 1
            continue

        schema_files = [
            f
            for f in files
            if isinstance(f, dict)
            and f.get("name", "").endswith(".schema.json")
            and not f.get("name", "").startswith(".")
        ]
        print(f"{len(schema_files)} schema files")

        downloaded = 0
        skipped = 0

        for file_info in schema_files:
            fname = file_info["name"]
            local_path = domain_dir / fname

            if local_path.exists():
                skipped += 1
                continue

            raw_url = file_info.get("download_url", f"{GITHUB_RAW}/{domain}/{fname}")

            try:
                req = urllib.request.Request(
                    raw_url, headers={"User-Agent": "md-ddl-extractor/1.0"}
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    content = resp.read()

                local_path.write_bytes(content)
                downloaded += 1

            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
                total_failed += 1

            # Rate limit — be polite to GitHub
            time.sleep(0.05)

        total_downloaded += downloaded
        total_skipped += skipped
        print(f"    {downloaded} downloaded, {skipped} already cached")

    print(
        f"\n  Download summary: {total_downloaded} downloaded, "
        f"{total_skipped} skipped, {total_failed} failed"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    download = "--download" in sys.argv

    print("TM Forum SID v4 Reference Extractor")
    print(f"  schemas: {SCHEMA_DIR}")
    print(f"  output:  {OUTPUT_DIR}")
    print()

    if download:
        print("Phase 1: Downloading schemas from GitHub...")
        download_schemas()
        print()

    # Check schemas exist
    if not SCHEMA_DIR.exists() or not any(SCHEMA_DIR.rglob("*.schema.json")):
        print("ERROR: No schemas found. Run with --download first:")
        print()
        print("  python industry_standards/tmforum/extract-references.py --download")
        print()
        sys.exit(1)

    print("Phase 2: Loading and parsing schemas...")
    entities = load_all_schemas()
    print(f"  loaded {len(entities)} total schema definitions")
    print()

    print("Phase 3: Generating markdown reference files...")
    write_file("sid-entities.md", generate_sid_entities(entities))
    write_file("sid-domains.md", generate_sid_domains(entities))
    write_file("sid-entities-detail.md", generate_sid_entities_detail(entities))

    print("\nDone.")


if __name__ == "__main__":
    main()
