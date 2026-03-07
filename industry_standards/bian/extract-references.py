"""
BIAN v13 Reference Extractor
=============================
Reads raw BIAN v13 JSON files and produces clean markdown reference files
for the agent-ontology standards-alignment skill.

Usage:
    python industry_standards/bian/extract-references.py                   # generate from local JSON only
    python industry_standards/bian/extract-references.py --fetch-classes    # also fetch core class attributes via API

Output directory:
    agents/agent-ontology/skills/standards-alignment/standards/bian/

Source directory:
    industry_standards/bian/v13/

Cached class data:
    industry_standards/bian/v13/cached-classes/
"""

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOURCE_DIR = REPO_ROOT / "industry_standards" / "bian" / "v13"
CACHE_DIR = SOURCE_DIR / "cached-classes"
OUTPUT_DIR = (
    REPO_ROOT
    / "agents"
    / "agent-ontology"
    / "skills"
    / "standards-alignment"
    / "standards"
    / "bian"
)

API_BASE = "https://bian-modelapi-v4.azurewebsites.net"
BIAN_VERSION = "13.0.0"

# ---------------------------------------------------------------------------
# Core BO Classes — fetched with full attributes
# ---------------------------------------------------------------------------
# Selection criteria:
#   - Classes referenced in the Financial Crime example
#   - Abstract base classes forming inheritance roots
#   - Classes commonly encountered in banking/FS domains
#   - Covers party, account, product, agreement, payment, risk, location,
#     document, arrangement, and channel families

CORE_CLASSES = [
    # Party family
    "Party",
    "Person",
    "PartyRole",
    "Merchant",
    # Account family
    "Account",
    "CurrentAccount",
    "SavingsAccount",
    "LoanAccount",
    "BalanceSheet",
    # Product family
    "ProductAgreement",
    "ProductFeature",
    "BankingProduct",
    # Agreement family
    "Agreement",
    "CustomerAgreement",
    "LoanAgreement",
    "TermDepositAgreement",
    "InsuranceAgreement",
    # Payment / Transaction family
    "Transaction",
    "CardPaymentService",
    # Financial instrument family
    "FinancialInstrument",
    "Security",
    # Risk and compliance
    "RiskAssessment",
    "ComplianceCheck",
    "ComplianceReport",
    "RegulatoryReport",
    "Audit",
    # Location and address
    "Location",
    "Address",
    "Country",
    # Document and communication
    "Document",
    "Correspondence",
    "Notification",
    # Arrangement and condition
    "Arrangement",
    "Condition",
    "Obligation",
    "AccessArrangement",
    # Channel and device
    "Channel",
    "Device",
    "ContactPoint",
    # Date/time and identifiers
    "DateTime",
    "Indicator",
    # Plan and strategy
    "Plan",
    "Strategy",
    "Goal",
    # Event
    "Event",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_json(filename: str) -> list:
    path = SOURCE_DIR / filename
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def first_sentence(text: str | None) -> str:
    """Return the first sentence (or first 200 chars) of a description."""
    if not text:
        return ""
    text = text.strip().replace("\n", " ").replace("\r", " ")
    # Remove redundant internal whitespace
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
# Generators
# ---------------------------------------------------------------------------


def generate_bo_classes() -> str:
    """Generate bo-classes.md — searchable index of all BO classes."""
    classes = load_json("BOClassesLite.json")
    classes.sort(key=lambda c: c["name"])

    lines = [
        "# BIAN v13 — Business Object Classes",
        "",
        f"Auto-generated index of {len(classes)} BO classes from BIAN v13.0.0.",
        "Use this file for name-matching when mapping MD-DDL entities to BIAN.",
        "",
        "Name | Description | Status",
        "--- | --- | ---",
    ]

    for c in classes:
        name = escape_md(c["name"])
        desc = escape_md(first_sentence(c.get("description")))
        status = c.get("status", "")
        lines.append(f"{name} | {desc} | {status}")

    lines.append("")
    return "\n".join(lines)


def generate_hierarchy() -> str:
    """Generate hierarchy.md — Business Areas > Domains > Service Domains."""
    areas = load_json("BusinessAreas.json")
    domains = load_json("BusinessDomains.json")
    service_domains = load_json("ServiceDomainsBasic.json")

    # Index areas by bianId
    area_map: dict[str, dict] = {}
    for a in areas:
        area_map[a["bianId"]] = a

    # Group domains by area bianId
    domain_by_area: dict[str, list] = {}
    for d in domains:
        area_id = (
            d.get("businessArea", {}).get("bianId", "unknown")
            if d.get("businessArea")
            else "unknown"
        )
        domain_by_area.setdefault(area_id, []).append(d)

    # Group service domains by domain bianId
    sd_by_domain: dict[str, list] = {}
    for sd in service_domains:
        dom_id = (
            sd.get("businessDomain", {}).get("bianId", "unknown")
            if sd.get("businessDomain")
            else "unknown"
        )
        sd_by_domain.setdefault(dom_id, []).append(sd)

    lines = [
        "# BIAN v13 — Taxonomy Hierarchy",
        "",
        "Business Areas → Business Domains → Service Domains.",
        "Use this to understand where a concept sits in BIAN's taxonomy.",
        "",
    ]

    for area in sorted(areas, key=lambda a: a["name"]):
        area_id = area["bianId"]
        lines.append(f"## {area['name']}")
        lines.append("")
        if area.get("description"):
            lines.append(f"> {first_sentence(area['description'])}")
            lines.append("")

        area_domains = sorted(domain_by_area.get(area_id, []), key=lambda d: d["name"])
        if not area_domains:
            lines.append("*No domains listed.*")
            lines.append("")
            continue

        for domain in area_domains:
            domain_id = domain["bianId"]
            lines.append(f"### {domain['name']}")
            lines.append("")
            if domain.get("description"):
                lines.append(f"> {first_sentence(domain['description'])}")
                lines.append("")

            sds = sorted(sd_by_domain.get(domain_id, []), key=lambda s: s["name"])
            if sds:
                lines.append("Service Domain | Summary")
                lines.append("--- | ---")
                for sd in sds:
                    name = escape_md(sd["name"])
                    summary = escape_md(
                        first_sentence(
                            sd.get("executiveSummary") or sd.get("roleDefinition") or ""
                        )
                    )
                    lines.append(f"{name} | {summary}")
                lines.append("")
            else:
                lines.append("*No service domains listed.*")
                lines.append("")

    return "\n".join(lines)


def generate_enumerations() -> str:
    """Generate enumerations.md — BO Enumerations index."""
    enums = load_json("BOEnumerationsLite.json")
    enums.sort(key=lambda e: e["name"])

    lines = [
        "# BIAN v13 — Business Object Enumerations",
        "",
        f"Auto-generated index of {len(enums)} BO enumerations from BIAN v13.0.0.",
        "Use this file when mapping MD-DDL enums to BIAN counterparts.",
        "",
        "Name | Description",
        "--- | ---",
    ]

    for e in enums:
        name = escape_md(e["name"])
        desc = escape_md(first_sentence(e.get("description")))
        lines.append(f"{name} | {desc}")

    lines.append("")
    return "\n".join(lines)


def generate_bo_classes_detail() -> str:
    """Generate bo-classes-detail.md from cached class JSON files."""
    if not CACHE_DIR.exists():
        return _detail_placeholder()

    cached_files = sorted(CACHE_DIR.glob("*.json"))
    if not cached_files:
        return _detail_placeholder()

    lines = [
        "# BIAN v13 — Core Class Detail",
        "",
        f"Detailed definitions for {len(cached_files)} core BO classes,",
        "including inheritance, abstraction, and attribute lists.",
        "",
    ]

    for path in cached_files:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            if not data:
                continue
            data = data[0]

        name = data.get("name", path.stem)
        super_type = data.get("superType")
        is_abstract = data.get("isAbstract", False)
        description = first_sentence(data.get("description"))
        attrs = data.get("attributeList") or []

        lines.append(f"## {name}")
        lines.append("")
        if description:
            lines.append(f"> {description}")
            lines.append("")

        meta_parts = []
        if super_type:
            super_name = (
                super_type.get("name", "")
                if isinstance(super_type, dict)
                else str(super_type)
            )
            if super_name:
                meta_parts.append(f"**Extends:** {super_name}")
        if is_abstract:
            meta_parts.append("**Abstract:** yes")
        if meta_parts:
            lines.append(" | ".join(meta_parts))
            lines.append("")

        if attrs:
            lines.append("Attribute | Type | Mandatory | Multi-valued | Description")
            lines.append("--- | --- | --- | --- | ---")
            for attr in attrs:
                attr_name = escape_md(attr.get("featureName") or attr.get("name") or "")
                # Resolve type: prefer dataType string, then boEnumeration name, then boDataType name
                attr_type = attr.get("dataType") or ""
                if not attr_type and attr.get("boEnumeration"):
                    attr_type = attr["boEnumeration"].get("name", "")
                if not attr_type and attr.get("boDataType"):
                    attr_type = attr["boDataType"].get("name", "")
                attr_type = escape_md(attr_type)
                mandatory = "yes" if attr.get("isMandatory") else ""
                multi = "yes" if attr.get("isMultiValued") else ""
                desc = escape_md(first_sentence(attr.get("description")))
                lines.append(
                    f"{attr_name} | {attr_type} | {mandatory} | {multi} | {desc}"
                )
            lines.append("")
        else:
            lines.append("*No attributes in cached data.*")
            lines.append("")

    return "\n".join(lines)


def _detail_placeholder() -> str:
    return "\n".join(
        [
            "# BIAN v13 — Core Class Detail",
            "",
            "No cached class data found. Run with `--fetch-classes` to populate:",
            "",
            "```",
            "python industry_standards/bian/extract-references.py --fetch-classes",
            "```",
            "",
        ]
    )


# ---------------------------------------------------------------------------
# API Fetcher
# ---------------------------------------------------------------------------


def fetch_core_classes() -> None:
    """Fetch full BO class data for each core class and cache as JSON."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # Load existing class names from BOClassesLite to validate names
    all_classes = load_json("BOClassesLite.json")
    known_names = {c["name"] for c in all_classes}

    fetched = 0
    skipped = 0
    failed = 0

    for name in CORE_CLASSES:
        cache_path = CACHE_DIR / f"{name}.json"
        if cache_path.exists():
            skipped += 1
            continue

        url = f"{API_BASE}/BOClassByName/{urllib.parse.quote(name)}/BIAN/{BIAN_VERSION}"
        note = "" if name in known_names else " (not in Lite index)"
        print(f"  fetching {name}{note}...", end=" ", flush=True)

        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = json.loads(resp.read().decode("utf-8"))

            # Strip deep noise from the response before caching
            cleaned = _clean_class_response(raw)
            cache_path.write_text(
                json.dumps(cleaned, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            fetched += 1
            print("OK")

        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            print(f"FAILED ({exc})")
            failed += 1

        # Rate limit — be polite to the API
        time.sleep(0.5)

    print(f"\n  Fetch summary: {fetched} fetched, {skipped} skipped, {failed} failed")


def _clean_class_response(raw) -> dict:
    """Strip noise fields from a full BOClass API response."""
    if isinstance(raw, list):
        if not raw:
            return {}
        raw = raw[0]

    keep_keys = {
        "name",
        "description",
        "status",
        "isAbstract",
        "isRoot",
        "superType",
        "attributeList",
        "ownerName",
        "bianId",
    }

    cleaned: dict = {k: raw[k] for k in keep_keys if k in raw}

    # Clean superType
    if cleaned.get("superType") and isinstance(cleaned["superType"], dict):
        cleaned["superType"] = {
            "name": cleaned["superType"].get("name"),
            "bianId": cleaned["superType"].get("bianId"),
        }

    # Clean attributes
    if cleaned.get("attributeList"):
        clean_attrs = []
        for attr in cleaned["attributeList"]:
            clean_attr = {
                "featureName": attr.get("featureName"),
                "name": attr.get("name"),
                "dataType": attr.get("dataType"),
                "description": attr.get("description"),
                "isMandatory": attr.get("isMandatory"),
                "isMultiValued": attr.get("isMultiValued"),
            }
            # Keep enum name if present
            if attr.get("boEnumeration"):
                clean_attr["boEnumeration"] = {
                    "name": attr["boEnumeration"].get("name")
                }
            # Keep data type name if present
            if attr.get("boDataType"):
                clean_attr["boDataType"] = {"name": attr["boDataType"].get("name")}
            clean_attrs.append(clean_attr)
        cleaned["attributeList"] = clean_attrs

    return cleaned


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    fetch = "--fetch-classes" in sys.argv

    print("BIAN v13 Reference Extractor")
    print(f"  source: {SOURCE_DIR}")
    print(f"  output: {OUTPUT_DIR}")
    print()

    if fetch:
        print("Phase 1: Fetching core class attributes from API...")
        fetch_core_classes()
        print()

    print("Phase 2: Generating markdown reference files...")
    write_file("bo-classes.md", generate_bo_classes())
    write_file("hierarchy.md", generate_hierarchy())
    write_file("enumerations.md", generate_enumerations())
    write_file("bo-classes-detail.md", generate_bo_classes_detail())

    print("\nDone.")


if __name__ == "__main__":
    main()
