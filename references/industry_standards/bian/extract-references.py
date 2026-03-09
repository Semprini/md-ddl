"""
BIAN Reference Extractor
========================
Reads raw BIAN JSON files for a selected release and produces clean markdown
reference files for the agent-ontology standards-alignment skill.

Usage examples:
    python references/industry_standards/bian/extract-references.py
    python references/industry_standards/bian/extract-references.py --version 13.0.0
    python references/industry_standards/bian/extract-references.py --fetch-classes
    python references/industry_standards/bian/extract-references.py --version 14.0.0 --output-mode flat

Default output mode writes to versioned directories:
    agents/agent-ontology/skills/standards-alignment/standards/bian/v13/
    agents/agent-ontology/skills/standards-alignment/standards/bian/v14/

Flat mode preserves legacy output path:
    agents/agent-ontology/skills/standards-alignment/standards/bian/
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_VERSION = "14.0.0"
API_BASE = "https://bian-modelapi-v4.azurewebsites.net"

# Selection criteria:
#   - Classes referenced in the Financial Crime example
#   - Abstract base classes forming inheritance roots
#   - Classes commonly encountered in banking/FS domains
#   - Covers party, account, product, agreement, payment, risk, location,
#     document, arrangement, and channel families
CORE_CLASSES = [
    "Party",
    "Person",
    "PartyRole",
    "Merchant",
    "Account",
    "CurrentAccount",
    "SavingsAccount",
    "LoanAccount",
    "BalanceSheet",
    "ProductAgreement",
    "ProductFeature",
    "BankingProduct",
    "Agreement",
    "CustomerAgreement",
    "LoanAgreement",
    "TermDepositAgreement",
    "InsuranceAgreement",
    "Transaction",
    "CardPaymentService",
    "FinancialInstrument",
    "Security",
    "RiskAssessment",
    "ComplianceCheck",
    "ComplianceReport",
    "RegulatoryReport",
    "Audit",
    "Location",
    "Address",
    "Country",
    "Document",
    "Correspondence",
    "Notification",
    "Arrangement",
    "Condition",
    "Obligation",
    "AccessArrangement",
    "Channel",
    "Device",
    "ContactPoint",
    "DateTime",
    "Indicator",
    "Plan",
    "Strategy",
    "Goal",
    "Event",
]


@dataclass
class ExtractorConfig:
    version: str
    major_version: str
    source_dir: Path
    cache_dir: Path
    output_dir: Path
    api_base: str


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate BIAN reference markdown files."
    )
    parser.add_argument(
        "--version",
        default=DEFAULT_VERSION,
        help="BIAN release version (for example: 13.0.0, 14.0.0).",
    )
    parser.add_argument(
        "--source-dir",
        help="Override source directory containing raw BIAN JSON files.",
    )
    parser.add_argument(
        "--output-dir",
        help="Override output directory where markdown files are generated.",
    )
    parser.add_argument(
        "--output-mode",
        choices=["versioned", "flat"],
        default="versioned",
        help="Write to standards/bian/v{major}/ (versioned) or standards/bian/ (flat).",
    )
    parser.add_argument(
        "--fetch-classes",
        action="store_true",
        help="Fetch core class details from the BIAN API into cache.",
    )
    parser.add_argument(
        "--api-base",
        default=API_BASE,
        help="BIAN model API base URL.",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


def major_version_from(version: str) -> str:
    # Accept semver-like strings and use the first component for path names.
    return version.split(".")[0]


def build_config(args: argparse.Namespace) -> ExtractorConfig:
    major = major_version_from(args.version)

    if args.source_dir:
        source_dir = Path(args.source_dir).resolve()
    else:
        source_dir = (
            REPO_ROOT / "references" / "industry_standards" / "bian" / f"v{major}"
        )

    cache_dir = source_dir / "cached-classes"

    if args.output_dir:
        output_dir = Path(args.output_dir).resolve()
    else:
        base = (
            REPO_ROOT
            / "agents"
            / "agent-ontology"
            / "skills"
            / "standards-alignment"
            / "standards"
            / "bian"
        )
        output_dir = base if args.output_mode == "flat" else base / f"v{major}"

    return ExtractorConfig(
        version=args.version,
        major_version=major,
        source_dir=source_dir,
        cache_dir=cache_dir,
        output_dir=output_dir,
        api_base=args.api_base,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_json(config: ExtractorConfig, filename: str) -> list:
    path = config.source_dir / filename
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def first_sentence(text: str | None) -> str:
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
    return text.replace("|", "\\|").replace("\n", " ")


def version_label(config: ExtractorConfig) -> str:
    return f"v{config.major_version}"


def write_file(config: ExtractorConfig, name: str, content: str) -> None:
    config.output_dir.mkdir(parents=True, exist_ok=True)
    path = config.output_dir / name
    path.write_text(content, encoding="utf-8")
    lines = content.count("\n") + 1
    print(f"  wrote {path.relative_to(REPO_ROOT)}  ({lines} lines)")


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------


def generate_bo_classes(config: ExtractorConfig) -> str:
    classes = load_json(config, "BOClassesLite.json")
    classes.sort(key=lambda c: c["name"])

    label = version_label(config)
    lines = [
        f"# BIAN {label} - Business Object Classes",
        "",
        f"Auto-generated index of {len(classes)} BO classes from BIAN {config.version}.",
        "Use this file for name-matching when mapping MD-DDL entities to BIAN.",
        "",
        "Name | Description | Status",
        "--- | --- | ---",
    ]

    for item in classes:
        name = escape_md(item["name"])
        desc = escape_md(first_sentence(item.get("description")))
        status = item.get("status", "")
        lines.append(f"{name} | {desc} | {status}")

    lines.append("")
    return "\n".join(lines)


def generate_hierarchy(config: ExtractorConfig) -> str:
    areas = load_json(config, "BusinessAreas.json")
    domains = load_json(config, "BusinessDomains.json")
    service_domains = load_json(config, "ServiceDomainsBasic.json")

    domain_by_area: dict[str, list] = {}
    for domain in domains:
        area_id = (
            domain.get("businessArea", {}).get("bianId", "unknown")
            if domain.get("businessArea")
            else "unknown"
        )
        domain_by_area.setdefault(area_id, []).append(domain)

    sd_by_domain: dict[str, list] = {}
    for service_domain in service_domains:
        domain_id = (
            service_domain.get("businessDomain", {}).get("bianId", "unknown")
            if service_domain.get("businessDomain")
            else "unknown"
        )
        sd_by_domain.setdefault(domain_id, []).append(service_domain)

    lines = [
        f"# BIAN {version_label(config)} - Taxonomy Hierarchy",
        "",
        "Business Areas -> Business Domains -> Service Domains.",
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


def generate_enumerations(config: ExtractorConfig) -> str:
    enums = load_json(config, "BOEnumerationsLite.json")
    enums.sort(key=lambda e: e["name"])

    lines = [
        f"# BIAN {version_label(config)} - Business Object Enumerations",
        "",
        f"Auto-generated index of {len(enums)} BO enumerations from BIAN {config.version}.",
        "Use this file when mapping MD-DDL enums to BIAN counterparts.",
        "",
        "Name | Description",
        "--- | ---",
    ]

    for enum_item in enums:
        name = escape_md(enum_item["name"])
        desc = escape_md(first_sentence(enum_item.get("description")))
        lines.append(f"{name} | {desc}")

    lines.append("")
    return "\n".join(lines)


def generate_bo_classes_detail(config: ExtractorConfig) -> str:
    if not config.cache_dir.exists():
        return detail_placeholder(config)

    cached_files = sorted(config.cache_dir.glob("*.json"))
    if not cached_files:
        return detail_placeholder(config)

    lines = [
        f"# BIAN {version_label(config)} - Core Class Detail",
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

        meta_parts: list[str] = []
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


def detail_placeholder(config: ExtractorConfig) -> str:
    return "\n".join(
        [
            f"# BIAN {version_label(config)} - Core Class Detail",
            "",
            "No cached class data found. Run with `--fetch-classes` to populate:",
            "",
            "```",
            f"python references/industry_standards/bian/extract-references.py --version {config.version} --fetch-classes",
            "```",
            "",
        ]
    )


# ---------------------------------------------------------------------------
# API Fetcher
# ---------------------------------------------------------------------------


def fetch_core_classes(config: ExtractorConfig) -> None:
    config.cache_dir.mkdir(parents=True, exist_ok=True)

    all_classes = load_json(config, "BOClassesLite.json")
    known_names = {item["name"] for item in all_classes}

    fetched = 0
    skipped = 0
    failed = 0

    for name in CORE_CLASSES:
        cache_path = config.cache_dir / f"{name}.json"
        if cache_path.exists():
            skipped += 1
            continue

        url = f"{config.api_base}/BOClassByName/{urllib.parse.quote(name)}/BIAN/{config.version}"
        note = "" if name in known_names else " (not in Lite index)"
        print(f"  fetching {name}{note}...", end=" ", flush=True)

        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = json.loads(resp.read().decode("utf-8"))

            cleaned = clean_class_response(raw)
            cache_path.write_text(
                json.dumps(cleaned, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            fetched += 1
            print("OK")

        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            print(f"FAILED ({exc})")
            failed += 1

        time.sleep(0.5)

    print(f"\n  Fetch summary: {fetched} fetched, {skipped} skipped, {failed} failed")


def clean_class_response(raw) -> dict:
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

    cleaned: dict = {key: raw[key] for key in keep_keys if key in raw}

    if cleaned.get("superType") and isinstance(cleaned["superType"], dict):
        cleaned["superType"] = {
            "name": cleaned["superType"].get("name"),
            "bianId": cleaned["superType"].get("bianId"),
        }

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
            if attr.get("boEnumeration"):
                clean_attr["boEnumeration"] = {
                    "name": attr["boEnumeration"].get("name")
                }
            if attr.get("boDataType"):
                clean_attr["boDataType"] = {"name": attr["boDataType"].get("name")}
            clean_attrs.append(clean_attr)
        cleaned["attributeList"] = clean_attrs

    return cleaned


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_source_layout(config: ExtractorConfig) -> None:
    required = [
        "BOClassesLite.json",
        "BOEnumerationsLite.json",
        "BusinessAreas.json",
        "BusinessDomains.json",
        "ServiceDomainsBasic.json",
    ]
    missing = [name for name in required if not (config.source_dir / name).exists()]
    if missing:
        missing_list = ", ".join(missing)
        raise FileNotFoundError(
            f"Missing required BIAN source files in {config.source_dir}: {missing_list}"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    args = parse_args()
    config = build_config(args)

    print("BIAN Reference Extractor")
    print(f"  version: {config.version}")
    print(f"  source: {config.source_dir}")
    print(f"  output: {config.output_dir}")
    print(f"  mode: {args.output_mode}")
    print()

    validate_source_layout(config)

    if args.fetch_classes:
        print("Phase 1: Fetching core class attributes from API...")
        fetch_core_classes(config)
        print()

    print("Phase 2: Generating markdown reference files...")
    write_file(config, "bo-classes.md", generate_bo_classes(config))
    write_file(config, "hierarchy.md", generate_hierarchy(config))
    write_file(config, "enumerations.md", generate_enumerations(config))
    write_file(config, "bo-classes-detail.md", generate_bo_classes_detail(config))

    print("\nDone.")


if __name__ == "__main__":
    main()
