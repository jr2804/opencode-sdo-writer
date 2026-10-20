# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""Replace heading first runs with number-tab-title run sequence."""

from __future__ import annotations

import argparse
from pathlib import Path

from officecli_xml_common import load_json_spec, raw_set, validate_doc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", required=True)
    parser.add_argument("--mapping", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    spec = load_json_spec(Path(args.mapping))
    headings = spec.get("headings", [])
    for item in headings:
        xpath = item.get("xpath")
        if not xpath:
            style = item.get("style")
            ordinal = item.get("ordinal")
            if not style or not ordinal:
                raise ValueError("Each heading needs xpath or style+ordinal")
            xpath = f"(//w:p[w:pPr/w:pStyle/@w:val='{style}'])[{ordinal}]/w:r[1]"
        xml = build_xml(item["number"], item["title"])
        if args.dry_run:
            print(f"DRY RUN: {xpath}")
            continue
        raw_set(args.doc, xpath, "replace", xml, verbose=args.verbose)

    if not args.dry_run:
        validate_doc(args.doc, verbose=args.verbose)
    return 0


def build_xml(number: str, title: str) -> str:
    return (
        f"<w:r><w:t>{number}</w:t></w:r><w:r><w:tab/></w:r><w:r><w:t>{title}</w:t></w:r"
    )


if __name__ == "__main__":
    raise SystemExit(main())
