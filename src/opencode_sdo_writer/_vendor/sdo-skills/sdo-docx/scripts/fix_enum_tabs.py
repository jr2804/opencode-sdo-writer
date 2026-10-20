# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""Replace enumeration first runs with dash-tab-text sequence."""

from __future__ import annotations

import argparse
from pathlib import Path

from officecli_xml_common import load_json_spec, raw_set, validate_doc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", required=True)
    parser.add_argument("--items", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    spec = load_json_spec(Path(args.items))
    style = spec.get("style", "B1")
    bullet = spec.get("bullet", "&#8211;")
    for item in spec.get("items", []):
        xpath = item.get("xpath")
        if not xpath:
            ordinal = item.get("ordinal")
            if not ordinal:
                raise ValueError("Each enum item needs xpath or ordinal")
            xpath = f"(//w:p[w:pPr/w:pStyle/@w:val='{style}'])[{ordinal}]/w:r[1]"
        xml = build_xml(bullet, item["text"])
        if args.dry_run:
            print(f"DRY RUN: {xpath}")
            continue
        raw_set(args.doc, xpath, "replace", xml, verbose=args.verbose)

    if not args.dry_run:
        validate_doc(args.doc, verbose=args.verbose)
    return 0


def build_xml(bullet: str, text: str) -> str:
    return (
        f"<w:r><w:t>{bullet}</w:t></w:r>"
        "<w:r><w:tab/></w:r>"
        f'<w:r><w:t xml:space="preserve">{text}</w:t></w:r>'
    )


if __name__ == "__main__":
    raise SystemExit(main())
