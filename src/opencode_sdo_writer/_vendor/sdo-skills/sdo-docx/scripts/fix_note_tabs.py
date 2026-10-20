# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""Replace note first runs with NOTE-number-tab-text sequence."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from officecli_xml_common import load_json_spec, raw_set, validate_doc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", required=True)
    parser.add_argument("--notes", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    spec = load_json_spec(Path(args.notes))
    notes = spec.get("notes", [])
    if spec.get("enforce_restart_per_section", True):
        validate_restart(notes)

    for note in notes:
        style = note["style"]
        xpath = note.get("xpath")
        if not xpath:
            ordinal = note.get("ordinal")
            if not ordinal:
                raise ValueError("Each note needs xpath or ordinal")
            xpath = f"(//w:p[w:pPr/w:pStyle/@w:val='{style}'])[{ordinal}]/w:r[1]"
        num = int(note.get("note_number", 0))
        if style == "TAN" and num == 0:
            xml = f'<w:r><w:t xml:space="preserve">{note["text"]}</w:t></w:r>'
        else:
            xml = build_note_xml(num, note["text"])

        if args.dry_run:
            print(f"DRY RUN: {xpath}")
            continue
        raw_set(args.doc, xpath, "replace", xml, verbose=args.verbose)

    if not args.dry_run:
        validate_doc(args.doc, verbose=args.verbose)
    return 0


def build_note_xml(number: int, text: str) -> str:
    return (
        f"<w:r><w:t>NOTE&#160;{number}:</w:t></w:r>"
        "<w:r><w:tab/></w:r>"
        f'<w:r><w:t xml:space="preserve">{text}</w:t></w:r>'
    )


def validate_restart(notes: list[dict]) -> None:
    by_section: dict[str, list[int]] = defaultdict(list)
    for note in notes:
        section = note.get("section_key", "")
        num = int(note.get("note_number", 0))
        if num > 0:
            by_section[section].append(num)
    for section, nums in by_section.items():
        if nums and nums[0] != 1:
            raise ValueError(f"Section {section!r} note numbering does not start at 1")


if __name__ == "__main__":
    raise SystemExit(main())
