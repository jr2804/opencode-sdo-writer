---
name: 3gpp-tdocs
description: TDoc patterns, filename conventions, metadata structure, HTTP/FTP server access, and TDoc identification. Use when crawling TDocs from FTP directories, parsing TDoc metadata from portal, or validating TDoc numbers.
  Use when the user asks for 3GPP TDoc numbers or TDoc filenames (R1-..., RP-..., S4-..., SP-..., C1-..., CP-...), the 3GPP FTP/HTTP document server layout and TDoc download URLs, TDoc subdirectory detection (Docs/, Documents/) and excluded directories, 3GPP portal TDoc metadata fields and parsing, or validating, matching and normalizing TDoc IDs.
---

# TDocs (Temporary Documents)

## Overview

TDocs are meeting documents produced by members participating in 3GPP Working Groups and Sub-Working Groups. They include proposals, reports, and other documents related to the development of 3GPP standards.

## Quick Reference

| Pattern | Example | WG | Subgroup |
|---------|---------|----|----------|
| R1-xxxx | R1-2301234 | RAN | 1 |
| RP-xxxx | RP-230045 | RAN | Plenary |
| S4-xxxx | S4-251209 | SA | 4 |
| SP-xxxx | SP-240001 | SA | Plenary |
| C1-xxxx | C1-2345678 | CT | 1 |
| CP-xxxx | CP-123456 | CT | Plenary |

**Regex:** `[RSC][1-6P].{4,10}\.(zip|txt|pdf)`

## Ready-Made Pattern Module

`scripts/tdoc_pattern.py` is a dependency-free PEP 723 script (no third-party packages). Run it directly:

```bash
mise x uv -- uv run scripts/tdoc_pattern.py
```

or import it from the script directory:

```python
from tdoc_pattern import parse_tdoc

match = parse_tdoc("r1-2301234.zip")
# TdocMatch(tdoc_id="R1-2301234", extension="zip")
# match.working_group == "RAN", match.subgroup == "1"
```

| Function | Purpose |
|---|---|
| `is_valid_tdoc(filename)` | Full-match validation of a TDoc filename |
| `parse_tdoc(filename)` | Parse into `TdocMatch(tdoc_id, extension)` with `.working_group`/`.subgroup` |
| `normalize_tdoc_id(tdoc_id)` | Uppercase normalization for DB lookups |
| `infer_working_group_from_tdoc(tdoc_id)` | R/S/C -> RAN/SA/CT |

## Key Points

- **Case-insensitive**: TDoc IDs should be normalized to uppercase for database operations
- **99%+ .zip files**: Most TDocs use `.zip` format
- **Public FTP access**: Files are publicly accessible without authentication
- **Portal metadata**: Requires EOL account for detailed metadata
- **Subdirectory handling**: Always check for Docs/, Documents/, etc. before crawling base directory
- **Excluded directories**: Skip Inbox/, Draft/, Agenda/, Invitation/, Report/ as they are not TDocs

## See Also

- `references/tdoc-number-format.md` - Pattern breakdown, matching/non-matching examples, TDoc allocation, ID normalization, working group inference
- `references/tdoc-metadata.md` - Portal metadata fields, parsing workflow, metadata code pattern
- `references/ftp-crawling.md` - Server structure, TDoc URL pattern, subdirectory detection, direct links, crawling workflow

## Cross-References

- `3gpp-working-groups` - For understanding working group and subgroup structure
- `3gpp-meetings` - For understanding how TDocs are associated with meetings
- `3gpp-portal-authentication` - For accessing TDoc metadata from portal

## Resources

- **3GPP Official:** <https://www.3gpp.org/>
- **3GPP Portal:** <https://portal.3gpp.org/>
- **3GPP FTP:** <https://www.3gpp.org/ftp/>
