# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "lxml>=5.0",
# ]
# ///
"""Sync DOCX core, extended, and custom properties from PLAN.md frontmatter.

Usage:
    mise x uv -- uv run set_docx_props.py <docx_path> [--plan <plan_path>]
        [--title <title>] [--author <author>] [--company <company>]
        [--props key1=fm_key1,key2=fm_key2,...]

Default behavior: reads PLAN.md from the parent directory of <docx_path>,
extracts YAML frontmatter, and writes properties into the DOCX file.

Built-in properties (from PLAN.md unless overridden):
  - Title:   from 'title' key
  - Author:  from $USERNAME (or --author override)
  - Company: from 'source' key

Custom properties are controlled by the --props mapping:

    --props tdoc=tdoc,revision_of=revision_of,meeting=meeting,date=date,agenda_item=agenda_item,target=target

This maps custom property name "tdoc" to PLAN.md key "tdoc", etc.  Keys
with empty/missing values in PLAN.md are skipped (no custom property
written).  If --props is omitted, the default mapping above (3GPP-compatible)
is used.

Examples:
    # 3GPP TDoc (default mapping)
    mise x uv -- uv run set_docx_props.py "S4-260717 - Idle noise test method.docx"

    # ITU-T contribution (different custom property names)
    mise x uv -- uv run set_docx_props.py "C-1234 - New metric for P.1401.docx" \
      --props contribution=contribution,question=question,place=place,date=date,source=source

    # Override title and author from command line
    mise x uv -- uv run set_docx_props.py "doc.docx" --title "Revised proposal" --author "Jane Smith"
"""

import argparse
import io
import os
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree

# XML namespaces
CORE_NS = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
DC_NS = "http://purl.org/dc/elements/1.1/"
CP_NS = "http://schemas.openxmlformats.org/officeDocument/2006/custom-properties"
VT_NS = "http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"
EP_NS = "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"

FMTID = "{D5CDD505-2E9C-101B-9397-08002B2CF9AE}"

DEFAULT_PROPS = "tdoc=tdoc,revision_of=revision_of,meeting=meeting,date=date,agenda_item=agenda_item,target=target"


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("docx_path", help="Path to DOCX file to update")
    parser.add_argument("--plan", help="Path to PLAN.md (default: parent/PLAN.md)")
    parser.add_argument("--title", help="Override PLAN.md title")
    parser.add_argument("--author", help="Override author (default: $USERNAME)")
    parser.add_argument("--company", help="Override PLAN.md source/company")
    parser.add_argument(
        "--props",
        default=DEFAULT_PROPS,
        help=f"Custom property name -> frontmatter key mapping (default: {DEFAULT_PROPS})",
    )

    args = parser.parse_args()
    props_mapping = parse_props_mapping(args.props)

    docx_path = Path(args.docx_path).resolve()
    if not docx_path.exists():
        print(f"Error: DOCX file not found: {docx_path}", file=sys.stderr)
        sys.exit(1)

    plan_path = Path(args.plan) if args.plan else docx_path.parent / "PLAN.md"
    if not plan_path.exists():
        print(f"Warning: PLAN.md not found at {plan_path}, using CLI args only")
        plan_props = {}
    else:
        plan_props = read_plan_frontmatter(plan_path)
        print(f"Read PLAN.md from {plan_path}")

    title = args.title or plan_props.get("title")
    author = args.author or os.environ.get("USERNAME", "")
    company = args.company or plan_props.get("source")

    # Build custom properties from mapping
    custom_props = {}
    for custom_name, fm_key in props_mapping.items():
        value = plan_props.get(fm_key, "")
        if value and value != "~":
            custom_props[custom_name] = value

    if not custom_props and not title and not author:
        print("Warning: no properties to set (PLAN.md not found and no CLI args)")
        return

    with zipfile.ZipFile(docx_path, "r") as zin:
        files = {name: zin.read(name) for name in zin.namelist()}

    if "docProps/core.xml" in files:
        files["docProps/core.xml"] = patch_core_xml(
            files["docProps/core.xml"], title, author
        )
        print(
            f"  Patched docProps/core.xml (title: {title or '(none)'}, author: {author or '(none)'})"
        )

    if "docProps/app.xml" in files and company:
        files["docProps/app.xml"] = patch_app_xml(files["docProps/app.xml"], company)
        print(f"  Patched docProps/app.xml (company: {company})")

    if custom_props:
        files["docProps/custom.xml"] = build_custom_xml(custom_props)
        print(
            f"  Written docProps/custom.xml ({len(custom_props)} properties: {list(custom_props.keys())})"
        )
        update_content_types(files)
        update_rels(files)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in files.items():
            zout.writestr(name, data)

    with open(docx_path, "wb") as f:
        f.write(buf.getvalue())

    print(f"Done -- updated {docx_path}")


def parse_props_mapping(raw: str) -> dict[str, str]:
    """Parse 'custom_name=fm_key,...' into {custom_name: fm_key}."""
    mapping = {}
    for pair in raw.split(","):
        pair = pair.strip()
        if "=" not in pair:
            continue
        custom_name, fm_key = pair.split("=", 1)
        mapping[custom_name.strip()] = fm_key.strip()
    return mapping


def read_plan_frontmatter(plan_path):
    """Parse YAML frontmatter from PLAN.md."""
    try:
        with open(plan_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return {}

    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    yaml_lines = match.group(1).strip().split("\n")
    props = {}
    for line in yaml_lines:
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if (
            val.startswith('"')
            and val.endswith('"')
            or val.startswith("'")
            and val.endswith("'")
        ):
            val = val[1:-1]
        props[key] = val
    return props


def build_custom_xml(custom_props):
    """Build docProps/custom.xml from {name: value} dict."""
    root = etree.Element(
        f"{{{CP_NS}}}Properties",
        nsmap={"cp": CP_NS, "vt": VT_NS},
    )
    for i, (name, value) in enumerate(custom_props.items(), start=2):
        prop = etree.SubElement(root, f"{{{CP_NS}}}property")
        prop.set("fmtid", FMTID)
        prop.set("pid", str(i))
        prop.set("name", name)
        val_el = etree.SubElement(prop, f"{{{VT_NS}}}lpwstr")
        val_el.text = value
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def patch_core_xml(xml_bytes, title, author):
    """Patch docProps/core.xml with title and author."""
    tree = etree.fromstring(xml_bytes)
    ns = {"dc": DC_NS, "cp": CORE_NS}

    if title:
        title_el = tree.find("dc:title", ns)
        if title_el is None:
            title_el = etree.SubElement(tree, f"{{{DC_NS}}}title")
        title_el.text = title

    if author:
        for tag, ns_uri in [("creator", DC_NS), ("lastModifiedBy", CORE_NS)]:
            el = tree.find(f"{{{ns_uri}}}{tag}")
            if el is None:
                el = etree.SubElement(tree, f"{{{ns_uri}}}{tag}")
            el.text = author

    return etree.tostring(tree, xml_declaration=True, encoding="UTF-8", standalone=True)


def patch_app_xml(xml_bytes, company):
    """Patch docProps/app.xml with company name."""
    if not company:
        return xml_bytes

    tree = etree.fromstring(xml_bytes)
    ns = {"ep": EP_NS}
    company_el = tree.find("ep:Company", ns)
    if company_el is None:
        company_el = etree.SubElement(tree, f"{{{EP_NS}}}Company")
    company_el.text = company
    return etree.tostring(tree, xml_declaration=True, encoding="UTF-8", standalone=True)


def update_content_types(files):
    """Ensure custom.xml content type is registered."""
    CT_PATH = "[Content_Types].xml"
    CUSTOM_CT = "application/vnd.openxmlformats-officedocument.custom-properties+xml"

    if CT_PATH not in files:
        return

    ct_tree = etree.fromstring(files[CT_PATH])
    ct_ns = {"ct": "http://schemas.openxmlformats.org/package/2006/content-types"}
    existing = {e.get("PartName") for e in ct_tree.findall("ct:Override", ct_ns)}
    part_name = "/docProps/custom.xml"

    if part_name not in existing:
        override = etree.SubElement(
            ct_tree,
            "{http://schemas.openxmlformats.org/package/2006/content-types}Override",
        )
        override.set("PartName", part_name)
        override.set("ContentType", CUSTOM_CT)
    else:
        for e in ct_tree.findall("ct:Override", ct_ns):
            if e.get("PartName") == part_name:
                e.set("ContentType", CUSTOM_CT)
    files[CT_PATH] = etree.tostring(
        ct_tree, xml_declaration=True, encoding="UTF-8", standalone=True
    )


def update_rels(files):
    """Ensure custom.xml relationship exists."""
    RELS_MAIN = "_rels/.rels"
    if RELS_MAIN not in files:
        return

    rels_tree = etree.fromstring(files[RELS_MAIN])
    nsmap = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}
    existing = [r.get("Target") for r in rels_tree.findall("r:Relationship", nsmap)]

    if "docProps/custom.xml" not in existing:
        rel = etree.SubElement(
            rels_tree,
            "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship",
        )
        rel.set("Id", "rId_custom")
        rel.set(
            "Type",
            "http://schemas.openxmlformats.org/officeDocument/2006/relationships/custom-properties",
        )
        rel.set("Target", "docProps/custom.xml")
        files[RELS_MAIN] = etree.tostring(
            rels_tree, xml_declaration=True, encoding="UTF-8", standalone=True
        )


if __name__ == "__main__":
    main()
