---
name: etsi-tools
description: 'Retrieving metadata and documentation for ETSI specifications, and the tooling around the ETSI portal. Use when you need to find the latest version, full title, publication date, download URLs or version history for any ETSI specification (EN, ES, EG, TS, TR, SR, GS, GR, PAS, parts such as -1, -2, -3), or when you need to work with the ETSI portal (meetings, documents, TDocs, work items, registration) through the `etsi-portal-tool` CLI or its MCP server.'
---

# ETSI Tools

Two tool surfaces for ETSI: the **published specifications** (metadata,
version history, download URLs) and the **portal** (meetings, documents,
contributions, work items).

## Portal tooling

The portal (meetings, documents, contributions, work items, registration) is
reached with the `etsi-portal-tool` CLI, which also exposes an MCP server for
agents. Browsing is read-only and needs no authentication; downloading,
registering and writing need a logged-in session.
See [references/portal-tooling.md](references/portal-tooling.md) for the
command areas and a typical sequence, and the `etsi-portal-tool` skill for
the full surface. The procedure around those commands -- when a contribution
is due, what a revision is, how a work item is bound -- is in
`etsi-procedures`.

## Specification metadata

Retrieve comprehensive metadata for ETSI (European Telecommunications Standards Institute) specifications including latest version, full title, publication date, download URLs, and version history.

## Quick Start

To get metadata for an ETSI specification:

```bash
mise x uv -- uv run scripts/get_etsi_spec.py <spec-number>
```

**Accepted formats:**

- `103224` (six digits, defaults to TS type)
- `103 224` (three digits, space, three digits)
- `ETSI TS 103 224` (with prefix)
- `EG 202 396-3` (document type + spec + part)
- `TR 103 907` (document type + six digits)
- `ES 200 381-1` (document type + six digits + part)

**Examples:**

```bash
# TS (Technical Specification)
mise x uv -- uv run scripts/get_etsi_spec.py 103224
mise x uv -- uv run scripts/get_etsi_spec.py ETSI TS 103 224

# EG (ETSI Guide)
mise x uv -- uv run scripts/get_etsi_spec.py EG 202 396-3

# TR (Technical Report)
mise x uv -- uv run scripts/get_etsi_spec.py TR 103 907

# ES (ETSI Standard)
mise x uv -- uv run scripts/get_etsi_spec.py ES 200 381-1
```

## ETSI Document Types

ETSI publishes multiple document types, each with different purposes:

| Type | Name | Purpose |
|------|------|----------|
| EN | European Standard | Harmonized standard |
| ES | ETSI Standard | Technical specification for market implementation |
| EG | ETSI Guide | Guidance document |
| TS | Technical Specification | Technical specification |
| TR | Technical Report | Informational report |
| SR | Special Report | Temporary or specific-use document |
| GS | Group Specification | Specification from a specific group |
| GR | Group Report | Report from a specific group |
| PAS | Publicly Available Specification | Document for public use |

## Specification Numbering

ETSI specifications follow this pattern:

- **Document type**: EN, ES, EG, TS, TR, SR, GS, GR, or PAS
- **Prefix**: Series identifier (3 digits) - indicates technical area
- **Number**: Unique identifier within series (3 digits)
- **Part**: Optional component (-1, -2, -3, etc.) for multi-part standards
- **Full format**: `<doc_type> XXX YYY[-Z]`

**Common series prefixes:**

- `200`: General telephony requirements
- `103`: Speech and multimedia Transmission Quality (STQ)
- `123`: System architecture
- `128`: Security
- `133`: Protocol stack
- `202`: Network protocols

**Examples:**

- `ETSI TS 103 224`: TS type, series 103, specification 224
- `EG 202 396-3`: EG type, series 202, specification 396, part 3
- `ES 200 381-1`: ES type, series 200, specification 381, part 1

## Script Output

The script returns:

- Latest version number (e.g., V1.7.1)
- Release code (e.g., 60 for 60th revision)
- Full specification title
- Publication date
- Direct download URL for PDF
- Version history (all available versions)

**Example output for ETSI TS 103 224:**

```text
======================================================================
SPECIFICATION: ETSI TS 103224
======================================================================
Latest Version:  V1.7.1
Release Code:    60
Directory:       01.07.01_60
Title:           Speech and multimedia Transmission Quality (STQ); A sound field reproduction method...
Publication Date: nov 2025
Download URL:    https://www.etsi.org/deliver/etsi_ts/103200_103299/103224/01.07.01_60/ts_103224v010701p.pdf
======================================================================

Full versions available: 7
Version history:
  - V1.7.1 (release 60) ~ 2025
  - V1.7.0 (release 59) ~ 2025
  ...
```

## How It Works

The script parses the specification number, walks the ETSI delivery
directory, picks the latest version directory, derives the PDF URL and
reads the title and date from the PDF metadata. Directory layout, URL
patterns and known failure modes: `references/script-details.md`.

If the script fails, retrieve the metadata manually -- see
`references/manual-retrieval.md`.

## Reference Documentation

For detailed ETSI standards organization and search capabilities, see:

- ETSI Search Engine: <https://www.etsi.org/standards>
- ETSI Document Types: <https://www.etsi.org/standards/types-of-standards>
- ETSI Delivery Directory: <https://www.etsi.org/deliver>
- ETSI Portal: <https://portal.etsi.org/>

## Cross-references

- `etsi-procedures` -- meetings, contributions, work items, approval routes
- `etsi-governance` -- deliverable types and the development lifecycle
- `etsi-portal-tool` -- the portal CLI and MCP server

## Requirements

Python 3.11+ only. The dependencies (`requests`, `beautifulsoup4`, `PyPDF2`)
are declared in the script's PEP 723 header, so `mise x uv -- uv run`
installs them on demand -- nothing to install by hand.
