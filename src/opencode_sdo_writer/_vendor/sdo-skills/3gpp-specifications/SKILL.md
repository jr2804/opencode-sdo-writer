---
name: 3gpp-specifications
description: TS and TR numbering, spec file formats, FTP directory structure, and accessing 3GPP specifications. Use when working with 3GPP specification numbering, finding spec files, or understanding spec directory organization.
---

# 3GPP Specifications

## Overview

3GPP specifications are the primary deliverables of the 3GPP partnership. They include:

- **Technical Specifications (TS)** - Normative technical documents
- **Technical Reports (TR)** - Informative studies and reports

## Key Facts

- **Numbering**: two-digit series + three-digit spec number, written `<series>.<spec>` (e.g. TS 21.456, TS 22.101, TR 21.900)
- **Series**: 21 requirements, 22-24 service/realization/signalling, 25/36-38 radio (UTRA, LTE, NR), 26/32 codecs and OAM, 31-35 security and terminal testing
- **Type prefixes**: `TS` (normative) and `TR` (informative)
- **Files**: Word™ (`.doc`) for review, Zip™ (`.zip`) for distribution
- **Versions**: dot notation, e.g. `21.456.0` (initial) → `21.456.1`, `21.456.2`
- **FTP root**: `https://www.3gpp.org/ftp/Specs/<YYYY>-<MM>/` (one directory per TSG round)
- **Publication**: MCC aims to publish all specs within 4 weeks after the TSG plenary

## Key Points

- **Spec Numbering is hierarchical**: Series → Spec Number
- **TR numbers are separate series**: Use TR prefix for reports
- **Revisions create new versions**: Each CR creates a new version number
- **Multiple CRs can affect one spec**: All are merged into single version
- **Mirror CRs require same WI code**: For specs in multiple releases

## Reference Files

- `references/spec-numbering.md` - TS vs TR, numbering scheme and series table, spec categories, file naming, WG ownership, version control, CR/work item databases
- `references/spec-ftp-structure.md` - FTP directory layout, TSG round examples, delta directories, release management, finding spec files in code

## Cross-References

- `3gpp-releases` - For release structure and freeze concepts
- `3gpp-working-groups` - For understanding which WG owns which specs
- `3gpp-change-request` - For modification process via CRs
- `3gpp-meetings` - For understanding when specs are approved (at TSG plenaries)

## Resources

- **3GPP Official**: <https://www.3gpp.org/>
- **3GPP Portal**: <https://portal.3gpp.org/>
- **3GPP Work Plan**: <https://www.3gpp.org/specifications-technologies/3gpp-work-plan/>
- **MCC Info**: Available in spec list tables
