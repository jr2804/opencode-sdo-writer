---
name: 3gpp-working-groups
description: Working group nomenclature, tbid/SubTB identifiers, subgroup hierarchy, and TSG structure. Use when working with 3GPP working groups, parsing meeting codes, or understanding TBID mappings.
  Use when the user asks about 3GPP working groups and subgroups (RAN1-RAN6, SA1-SA6, CT1-CT6), TSG tbid or SubTB numbers and their mapping to working groups, 3GPP FTP directory naming (WG1_RL1, TSG_RAN), meeting code conventions (RP, SP, CP, R1-R6) and meeting name formats, or how to normalize working group codes for database lookups.
---

# 3GPP Working Groups

## Overview

3GPP has three main Technical Specification Groups (TSGs), each with multiple Working Groups (WGs) and Sub-Working Groups (SWGs):

### TSG Structure

- **TSG RAN** (Radio Access Network)
- **TSG SA** (Service and System Aspects)
- **TSG CT** (Core Network and Terminals)

## Key Identifiers

| TSG | tbid | Plenary SubTB | WGs |
|-----|------|---------------|-----|
| RAN | 373 | 373 | RAN1-RAN6 |
| SA | 375 | 375 | SA1-SA6 |
| CT | 649 | 649 | CT1-CT6 |

The full canonical SubTB -> WG mapping table with focus areas is in `references/tbid-mappings.md` (single source of truth - do not duplicate).

## See Also

- `references/tbid-mappings.md` - Canonical TBID/SubTB table, TSG responsibilities, per-TSG working group details, normalization code
- `references/ftp-structure.md` - Meeting code URLs, name formats, meeting ID resolution, FTP directory trees, meeting table structure

## Cross-References

- `3gpp-basics` - For 3GPP organization and structure
- `3gpp-meetings` - For meeting pages and naming conventions
- `3gpp-tdocs` - For TDoc handling and FTP structure
- `3gpp-portal-authentication` - For portal access when authentication required

## Resources

- 3GPP Groups: <https://www.3gpp.org/3gpp-groups/>
- 3GPP Portal: <https://portal.3gpp.org/>
- 3GPP Work Plan: <https://www.3gpp.org/specifications-technologies/3gpp-work-plan/>
