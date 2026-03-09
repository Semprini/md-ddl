#!/usr/bin/env python3
"""
Builds a local FHIR R4 standards cache for MD-DDL standards alignment.

Outputs generated files into:
  agents/agent-ontology/skills/standards-alignment/standards/fhir/

Usage:
    python references/industry_standards/fhir/extract-references.py
    python references/industry_standards/fhir/extract-references.py --download

Data source:
  https://hl7.org/fhir/R4/profiles-resources.json
  License: HL7 FHIR is published under CC0.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import textwrap
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

FHIR_R4_BUNDLE_URL = "https://hl7.org/fhir/R4/profiles-resources.json"
FHIR_R4_VALUESETS_URL = "https://hl7.org/fhir/R4/valuesets.json"
FHIR_R4_V3_CODESYSTEMS_URL = "https://hl7.org/fhir/R4/v3-codesystems.json"
FHIR_R4_V2_TABLES_URL = "https://hl7.org/fhir/R4/v2-tables.json"

CORE_RESOURCE_TYPES = [
    "Patient",
    "Encounter",
    "Condition",
    "Observation",
    "Procedure",
    "Medication",
    "MedicationRequest",
    "MedicationAdministration",
    "AllergyIntolerance",
    "CarePlan",
    "CareTeam",
    "Goal",
    "Organization",
    "Practitioner",
    "PractitionerRole",
    "RelatedPerson",
    "Location",
    "HealthcareService",
    "Coverage",
    "Claim",
    "ClaimResponse",
    "ExplanationOfBenefit",
    "Account",
    "DiagnosticReport",
    "Specimen",
    "ImagingStudy",
    "ServiceRequest",
    "Appointment",
    "Task",
    "Communication",
    "Consent",
    "Provenance",
    "AuditEvent",
    "Device",
    "DeviceMetric",
    "DocumentReference",
    "Composition",
    "Bundle",
    "ValueSet",
    "CodeSystem",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate FHIR R4 standards cache files"
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download the latest profiles-resources bundle before generating output",
    )
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")


def download_bundle(url: str, out_path: Path) -> None:
    ensure_parent(out_path)
    with urllib.request.urlopen(url) as response:
        payload = response.read()
    out_path.write_bytes(payload)


def get_entries(bundle: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    return bundle.get("entry", [])


def get_resource(entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    resource = entry.get("resource")
    if isinstance(resource, dict):
        return resource
    return None


def md_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.replace("|", "\\|").replace("\n", " ").strip()
    return text


def short_text(text: str, max_len: int = 200) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def canonical_from_structure_definition(sd: Dict[str, Any]) -> str:
    url = sd.get("url") or ""
    return str(url)


def collect_structure_definitions(bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
    found: List[Dict[str, Any]] = []
    for entry in get_entries(bundle):
        resource = get_resource(entry)
        if not resource:
            continue
        if resource.get("resourceType") != "StructureDefinition":
            continue
        if resource.get("kind") != "resource":
            continue
        found.append(resource)
    found.sort(key=lambda r: str(r.get("type") or r.get("name") or ""))
    return found


def collect_resources_by_type(
    bundle: Dict[str, Any], resource_type: str
) -> List[Dict[str, Any]]:
    found: List[Dict[str, Any]] = []
    for entry in get_entries(bundle):
        resource = get_resource(entry)
        if not resource:
            continue
        if resource.get("resourceType") == resource_type:
            found.append(resource)
    found.sort(key=lambda r: str(r.get("name") or r.get("id") or ""))
    return found


def merge_resources_by_url(resources: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_key: Dict[str, Dict[str, Any]] = {}
    fallback_index = 0
    for resource in resources:
        url = str(resource.get("url") or "").strip()
        name = str(resource.get("name") or resource.get("id") or "").strip()
        if url:
            key = f"url::{url}"
        elif name:
            key = f"name::{name}"
        else:
            fallback_index += 1
            key = f"anon::{fallback_index}"
        if key not in by_key:
            by_key[key] = resource
    merged = list(by_key.values())
    merged.sort(key=lambda r: str(r.get("name") or r.get("id") or r.get("url") or ""))
    return merged


def extract_base_type(sd: Dict[str, Any]) -> str:
    base = str(sd.get("baseDefinition") or "")
    if not base:
        return ""
    return base.rstrip("/").split("/")[-1]


def extract_key_elements(
    sd: Dict[str, Any], max_items: int = 30
) -> List[Dict[str, str]]:
    target_type = str(sd.get("type") or "")
    differential = sd.get("differential") or {}
    elements = differential.get("element") or []
    out: List[Dict[str, str]] = []
    for elem in elements:
        path = str(elem.get("path") or "")
        if not path.startswith(target_type + "."):
            continue
        if path.count(".") != 1:
            continue
        field = path.split(".", 1)[1]
        if field in {
            "id",
            "meta",
            "implicitRules",
            "language",
            "text",
            "contained",
            "extension",
            "modifierExtension",
        }:
            continue
        min_v = str(elem.get("min", ""))
        max_v = str(elem.get("max", ""))
        type_codes: List[str] = []
        for t in elem.get("type", []) or []:
            code = t.get("code")
            if code:
                type_codes.append(str(code))
        short = str(elem.get("short") or "")
        out.append(
            {
                "field": field,
                "min": min_v,
                "max": max_v,
                "types": ", ".join(type_codes),
                "short": short_text(short, max_len=120),
            }
        )
        if len(out) >= max_items:
            break
    return out


def format_resources_index(
    structure_defs: List[Dict[str, Any]], generated_at: str
) -> str:
    lines: List[str] = []
    lines.append("# FHIR R4 Resources Index")
    lines.append("")
    lines.append("Auto-generated from `profiles-resources.json`. Do not edit manually.")
    lines.append("")
    lines.append(f"Generated: {generated_at}")
    lines.append("")
    lines.append(
        "Resource Type | Canonical URL | Base Type | Abstract | Status | Description"
    )
    lines.append("--- | --- | --- | --- | --- | ---")

    for sd in structure_defs:
        resource_type = md_escape(sd.get("type") or sd.get("name"))
        canonical = md_escape(canonical_from_structure_definition(sd))
        base = md_escape(extract_base_type(sd))
        abstract = "yes" if sd.get("abstract") else "no"
        status = md_escape(sd.get("status") or "")
        description = md_escape(
            short_text(str(sd.get("description") or ""), max_len=180)
        )
        lines.append(
            f"{resource_type} | `{canonical}` | {base} | {abstract} | {status} | {description}"
        )

    lines.append("")
    lines.append(f"Total resources: {len(structure_defs)}")
    lines.append("")
    return "\n".join(lines)


def format_core_resources_detail(
    structure_defs: List[Dict[str, Any]], generated_at: str
) -> str:
    by_type = {str(sd.get("type") or ""): sd for sd in structure_defs}

    lines: List[str] = []
    lines.append("# FHIR R4 Core Resources Detail")
    lines.append("")
    lines.append("Auto-generated from `profiles-resources.json`. Do not edit manually.")
    lines.append("")
    lines.append(f"Generated: {generated_at}")
    lines.append("")
    lines.append(
        "This file captures a focused subset of high-value resource definitions"
    )
    lines.append("for healthcare modelling and standards alignment in MD-DDL.")
    lines.append("")

    for resource_type in CORE_RESOURCE_TYPES:
        sd = by_type.get(resource_type)
        if not sd:
            continue

        canonical = canonical_from_structure_definition(sd)
        base = extract_base_type(sd)
        abstract = "yes" if sd.get("abstract") else "no"
        status = str(sd.get("status") or "")
        description = short_text(str(sd.get("description") or ""), max_len=500)
        elements = extract_key_elements(sd, max_items=24)

        lines.append(f"## {resource_type}")
        lines.append("")
        lines.append(f"- Canonical: `{canonical}`")
        lines.append(f"- Base type: `{base}`")
        lines.append(f"- Abstract: `{abstract}`")
        lines.append(f"- Status: `{status}`")
        lines.append("")
        if description:
            lines.append(textwrap.fill(description, width=100))
            lines.append("")

        if elements:
            lines.append("Field | Min | Max | Type(s) | Description")
            lines.append("--- | --- | --- | --- | ---")
            for elem in elements:
                lines.append(
                    f"{md_escape(elem['field'])} | {md_escape(elem['min'])} | {md_escape(elem['max'])} | {md_escape(elem['types'])} | {md_escape(elem['short'])}"
                )
            lines.append("")
        else:
            lines.append("No core differential fields captured in this cache.")
            lines.append("")

    return "\n".join(lines)


def format_terminology_assets(
    code_systems: List[Dict[str, Any]],
    value_sets: List[Dict[str, Any]],
    generated_at: str,
) -> str:
    lines: List[str] = []
    lines.append("# FHIR R4 Terminology Assets")
    lines.append("")
    lines.append(
        "Auto-generated from FHIR R4 terminology bundles. Do not edit manually."
    )
    lines.append("")
    lines.append(f"Generated: {generated_at}")
    lines.append("")

    lines.append("## Code Systems")
    lines.append("")
    lines.append("Name | Canonical URL | Status | Description")
    lines.append("--- | --- | --- | ---")
    for cs in code_systems:
        name = md_escape(cs.get("name") or cs.get("id") or "")
        url = md_escape(cs.get("url") or "")
        status = md_escape(cs.get("status") or "")
        desc = md_escape(short_text(str(cs.get("description") or ""), max_len=160))
        lines.append(f"{name} | `{url}` | {status} | {desc}")
    lines.append("")
    lines.append(f"Total code systems: {len(code_systems)}")
    lines.append("")

    lines.append("## Value Sets")
    lines.append("")
    lines.append("Name | Canonical URL | Status | Description")
    lines.append("--- | --- | --- | ---")
    for vs in value_sets:
        name = md_escape(vs.get("name") or vs.get("id") or "")
        url = md_escape(vs.get("url") or "")
        status = md_escape(vs.get("status") or "")
        desc = md_escape(short_text(str(vs.get("description") or ""), max_len=160))
        lines.append(f"{name} | `{url}` | {status} | {desc}")
    lines.append("")
    lines.append(f"Total value sets: {len(value_sets)}")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    args = parse_args()

    root = repo_root()
    cache_dir = root / "references" / "industry_standards" / "fhir" / "r4"
    cache_path = cache_dir / "profiles-resources.json"
    valuesets_path = cache_dir / "valuesets.json"
    v3_codesystems_path = cache_dir / "v3-codesystems.json"
    v2_tables_path = cache_dir / "v2-tables.json"
    out_dir = (
        root
        / "agents"
        / "agent-ontology"
        / "skills"
        / "standards-alignment"
        / "standards"
        / "fhir"
    )

    if args.download or not cache_path.exists():
        print(f"Downloading FHIR R4 bundle from {FHIR_R4_BUNDLE_URL} ...")
        download_bundle(FHIR_R4_BUNDLE_URL, cache_path)
        print(f"Saved: {cache_path}")

    if args.download or not valuesets_path.exists():
        print(f"Downloading FHIR R4 ValueSets bundle from {FHIR_R4_VALUESETS_URL} ...")
        download_bundle(FHIR_R4_VALUESETS_URL, valuesets_path)
        print(f"Saved: {valuesets_path}")

    if args.download or not v3_codesystems_path.exists():
        print(
            f"Downloading FHIR R4 v3 code systems bundle from {FHIR_R4_V3_CODESYSTEMS_URL} ..."
        )
        download_bundle(FHIR_R4_V3_CODESYSTEMS_URL, v3_codesystems_path)
        print(f"Saved: {v3_codesystems_path}")

    if args.download or not v2_tables_path.exists():
        print(f"Downloading FHIR R4 v2 tables bundle from {FHIR_R4_V2_TABLES_URL} ...")
        download_bundle(FHIR_R4_V2_TABLES_URL, v2_tables_path)
        print(f"Saved: {v2_tables_path}")

    print(f"Loading bundle: {cache_path}")
    bundle = read_json(cache_path)
    terminology_bundles = [
        read_json(valuesets_path),
        read_json(v3_codesystems_path),
        read_json(v2_tables_path),
    ]

    generated_at = (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    structure_defs = collect_structure_definitions(bundle)
    code_systems_raw: List[Dict[str, Any]] = []
    value_sets_raw: List[Dict[str, Any]] = []
    for terminology_bundle in terminology_bundles:
        code_systems_raw.extend(
            collect_resources_by_type(terminology_bundle, "CodeSystem")
        )
        value_sets_raw.extend(collect_resources_by_type(terminology_bundle, "ValueSet"))
    code_systems = merge_resources_by_url(code_systems_raw)
    value_sets = merge_resources_by_url(value_sets_raw)

    resources_index = format_resources_index(structure_defs, generated_at)
    core_detail = format_core_resources_detail(structure_defs, generated_at)
    terminology = format_terminology_assets(code_systems, value_sets, generated_at)

    resources_index_path = out_dir / "resources.md"
    resources_detail_path = out_dir / "resources-detail.md"
    terminology_path = out_dir / "terminology.md"

    write_text(resources_index_path, resources_index)
    write_text(resources_detail_path, core_detail)
    write_text(terminology_path, terminology)

    print(f"Wrote: {resources_index_path}")
    print(f"Wrote: {resources_detail_path}")
    print(f"Wrote: {terminology_path}")
    print(
        f"Resources: {len(structure_defs)} | CodeSystems: {len(code_systems)} | ValueSets: {len(value_sets)}"
    )


if __name__ == "__main__":
    main()
