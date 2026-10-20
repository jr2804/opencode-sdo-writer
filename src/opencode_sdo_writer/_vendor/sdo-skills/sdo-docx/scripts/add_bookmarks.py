# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""Insert figure/table bookmarks and replace reference runs."""

from __future__ import annotations

import argparse
from pathlib import Path

from officecli_xml_common import load_json_spec, raw_set, validate_doc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    spec = load_json_spec(Path(args.spec))
    operations = [spec["figure"], spec["table"]]

    ids = [o["bookmark_id"] for o in operations] + [
        r["bookmark_id"] for r in spec["references"]
    ]
    names = [o["bookmark_name"] for o in operations] + [
        r["bookmark_name"] for r in spec["references"]
    ]
    if len(ids) != len(set(ids)):
        raise ValueError("Bookmark ids must be unique")
    if len(names) != len(set(names)):
        raise ValueError("Bookmark names must be unique")

    if args.dry_run:
        for op in operations:
            print(f"DRY RUN: bookmark wrap for {op['bookmark_name']} at {op['xpath']}")
        for ref in spec["references"]:
            print(
                f"DRY RUN: reference replace {ref['bookmark_name']} at {ref['xpath']}"
            )
        return 0

    for op in operations:
        raw_set(
            args.doc,
            op["xpath"],
            "before",
            bookmark_start(op["bookmark_name"], op["bookmark_id"]),
            verbose=args.verbose,
        )
        raw_set(
            args.doc,
            op["xpath"],
            "after",
            bookmark_end(op["bookmark_id"]),
            verbose=args.verbose,
        )

    for ref in spec["references"]:
        xml = reference_run(ref["number"], ref["bookmark_name"], ref["bookmark_id"])
        raw_set(args.doc, ref["xpath"], "replace", xml, verbose=args.verbose)

    validate_doc(args.doc, verbose=args.verbose)
    return 0


def reference_run(number: int, name: str, bookmark_id: int) -> str:
    return (
        "<w:r><w:t>[</w:t></w:r>"
        f"{bookmark_start(name, bookmark_id)}"
        f"<w:r><w:t>{number}</w:t></w:r>"
        f"{bookmark_end(bookmark_id)}"
        '<w:r><w:t xml:space="preserve">]&#9;</w:t></w:r>'
    )


def bookmark_start(name: str, bookmark_id: int) -> str:
    return f'<w:bookmarkStart xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:id="{bookmark_id}" w:name="{name}"/>'


def bookmark_end(bookmark_id: int) -> str:
    return f'<w:bookmarkEnd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:id="{bookmark_id}"/>'


if __name__ == "__main__":
    raise SystemExit(main())
