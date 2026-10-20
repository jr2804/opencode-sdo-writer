#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""TDoc number pattern parsing and validation.

Usage:

    from tdoc_pattern import is_valid_tdoc, parse_tdoc, normalize_tdoc_id

    parse_tdoc("R1-2301234.zip")
    # TdocMatch(tdoc_id="R1-2301234", extension="zip")

Run the self-test from the command line:

    mise x uv -- uv run scripts/tdoc_pattern.py
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# 1st char [RSC] = TSG (RAN/SA/CT); 2nd char [1-6P] = subgroup or Plenary;
# then 4-10 identifier chars; extension .zip/.txt/.pdf (case-insensitive).
TDOC_PATTERN = re.compile(r"([RSC][1-6P].{4,10})\.(zip|txt|pdf)", re.IGNORECASE)

TSG_BY_FIRST_CHAR = {"R": "RAN", "S": "SA", "C": "CT"}

EXCLUDED_DIRS = {"Inbox", "Draft", "Drafts", "Agenda", "Invitation", "Report"}

TDOC_SUBDIR_NAMES = {"docs", "documents", "tdocs"}


@dataclass(frozen=True)
class TdocMatch:
    """A parsed TDoc filename."""

    tdoc_id: str
    extension: str

    @property
    def working_group(self) -> str | None:
        """TSG (RAN/SA/CT) inferred from the first character, or None."""
        return TSG_BY_FIRST_CHAR.get(self.tdoc_id[0].upper())

    @property
    def subgroup(self) -> str:
        """Second character: 1-6 for WGs, 'P' for Plenary."""
        return self.tdoc_id[1].upper()


def is_valid_tdoc(filename: str) -> bool:
    """Return True if the filename matches the TDoc pattern."""
    return TDOC_PATTERN.fullmatch(filename.strip()) is not None


def parse_tdoc(filename: str) -> TdocMatch | None:
    """Parse a TDoc filename into its ID and extension (or None)."""
    match = TDOC_PATTERN.fullmatch(filename.strip())
    if match is None:
        return None
    return TdocMatch(
        tdoc_id=match.group(1).upper(),
        extension=match.group(2).lower(),
    )


def normalize_tdoc_id(tdoc_id: str) -> str:
    """Normalize a TDoc ID to uppercase for case-insensitive lookup."""
    return tdoc_id.upper().strip()


def infer_working_group_from_tdoc(tdoc_id: str) -> str | None:
    """Infer the TSG (RAN/SA/CT) from a TDoc ID's first character."""
    return TSG_BY_FIRST_CHAR.get(tdoc_id[0].upper())


if __name__ == "__main__":
    for _sample in ("R1-2301234.zip", "S4-251209.txt", "RP-230045.zip", "README.txt"):
        _match = parse_tdoc(_sample)
        print(f"{_sample:<20} -> {_match}")
    print(f"normalize_tdoc_id('r1-2301234') -> {normalize_tdoc_id('r1-2301234')}")
    print(f"infer_working_group_from_tdoc('c1-2345678') -> {infer_working_group_from_tdoc('c1-2345678')}")
    print(f"is_valid_tdoc('R1-2301234.zip') -> {is_valid_tdoc('R1-2301234.zip')}")
