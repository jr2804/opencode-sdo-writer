---
name: sdo-docx
description: 'Formatting conventions and safe editing operations for .docx deliverables in standards work. Use when formatting headings, notes, enumerations, tables, figures, equations, citations or text in a technical document; when applying named styles instead of direct formatting; when injecting SEQ/REF field codes, bookmarks or tab runs; when running the bundled officecli/OOXML helper scripts; or when preventing destructive raw-set and namespace errors. Covers ETSI, 3GPP and ITU-T templates.'
---

# SDO DOCX

Two halves of one job:

- **What to produce** -- formatting conventions (styles, headings, notes,
  enumerations, tables, figures, equations, citations, text). Detail in
  `references/formatting/`.
- **How to edit safely** -- officecli workflow, field codes, bookmarks, tab
  runs, tracked changes, raw XML. Detail in `references/operations/`.

## Core rules

1. Apply formatting exclusively through **named paragraph and character
   styles** defined in the document template. Never apply direct/ad-hoc
   formatting (toggling bold, changing font size, adding colour) without a
   named style. If a required named style is missing, inform the user and
   offer to create the style definition first.
2. Keep numbering and references **update-safe** -- use SEQ fields and
   bookmarks, never hard-coded numbers.
3. Use **non-breaking spaces** (`\u00a0`) for semantic units (number+unit,
   Figure/Table+number).
4. Use **real tab runs** (`<w:tab/>`), never spaces, for tab-separated
   structural elements (heading number+title, enumeration bullet+text, note
   label+text).
5. Never use `raw-set --action replace` with an empty XML payload; keep
   bookmark names and IDs unique; preserve non-breaking spaces and explicit
   tab runs.
6. Run helper scripts with `mise x uv -- uv run`, never bare `python`.
   Never assume a tool is installed: every external tool is pulled on
   demand through mise (see `references/operations/tool-usage.md`).

## Style-name abstraction

This skill uses **abstract style names**. The per-SDO reference in
`sdo-drafting` provides the concrete mapping.

| Abstract name | Purpose | 3GPP / ETSI | ITU-T |
|---|---|---|---|
| `body-text` | Main body paragraphs | `Normal` | `Body Text` |
| `heading-1` through `heading-3` | Section headings | `Heading 1`--`Heading 3` | `Heading 1`--`Heading 3` |

Always consult the per-SDO style map. If it is not in context, ask the user
which SDO applies and use the example mappings above as defaults.

## Document mode (decide first)

- **Standards mode** (specifications, reports, Recommendations, Norms):
  clause-centric structure (`N`, `N.M`, `N.M.P`); normative references are an
  early clause, typically clause 2.
- **Meeting-document mode** (contributions, submissions, TDoc/TD):
  section-oriented structure is allowed by template and SDO practice;
  reference sections often sit near the end.

If uncertain, ask whether the document is a meeting document or a standard.

## Conventions by domain

| Domain | Rule (critical points) | Detail |
| --- | --- | --- |
| Headings | Never use Word automatic numbering; `<w:tab/>` between number and title; `N` -> `N.M` -> `N.M.P`; clause terminology in standards mode; `References` unnumbered when standalone. | `references/formatting/headings.md` |
| Enumerations | Never use the Word built-in list feature; prefer en-dash (`–`) plus `<w:tab/>`; styles `enum-1`..`enum-3`. | `references/formatting/enumerations.md` |
| Notes | `NOTE\u00a0N:\t<text>` (uppercase NOTE, non-breaking space, real tab); omit the number for a single note; last note of a block is `note-main`, preceding ones `note-continuation`. | `references/formatting/notes.md` |
| Tables and figures | Table caption **above** (`Table\u00a0N: <text>`, `{SEQ Table \* ARABIC}`, bookmark `tbl_<name>` around the number); figure caption **below** (`Figure\u00a0N: <text>`, `{SEQ Figure \* ARABIC}`, bookmark `fig_<name>`); never hard-code numbers, cross-ref with `{REF bookmark}`. | `references/formatting/tables-figures.md` |
| Equations | Display equations: one paragraph, style `equation`, structure `\t<equation>\t(<SEQ EQ>)`; `{SEQ EQ \* ARABIC}` with bookmark `EQ_<name>`; inline equations use `oMath` runs, unnumbered. | `references/formatting/equations.md` |
| Citations | Entry `[N]\t<text>`, style `reference-entry`, `{SEQ Ref \* ARABIC}`, bookmark `ref_<name>` around the sequence field only. | `references/formatting/citations.md` |
| Text | `body-text` for paragraphs, `code-text` for inline code and filenames; non-breaking spaces between number+unit and Figure/Table+number; straight quotes only. | `references/formatting/text-formatting.md` |

## Editing workflow

All commands below are written the pull-on-demand way: `mise x <spec> --
<command>`. Drop the `mise x <spec> --` prefix when the tool is already on
PATH.

1. Open the document in resident mode before multi-step edits:
   `mise x github:iOfficeAI/OfficeCLI -- officecli open <doc>`
2. Run one mutation command at a time and check exit codes.
3. Use style/ordinal or explicit XPath targeting, not paraId targeting.
4. **Prefer `officecli batch`** for template population, text updates and
   paragraph additions -- Python zipfile/ElementTree can strip namespace
   declarations from the root element. Reserve Python for edits officecli
   cannot express.
5. Validate with `officecli view`/`get`/`query` before and after mutation.
6. Close the document at the end:
   `mise x github:iOfficeAI/OfficeCLI -- officecli close <doc>`

### Script entry points

| Script | Purpose |
| --- | --- |
| `scripts/add_bookmarks.py` | figure/table/reference bookmark insertion, reference run replacement |
| `scripts/fix_heading_tabs.py` | heading number-tab-title run repair |
| `scripts/fix_enum_tabs.py` | enumeration dash-tab-text run repair |
| `scripts/fix_note_tabs.py` | NOTE number-tab-text run repair and sequence validation |
| `scripts/officecli_xml_common.py` | shared helpers (run_officecli, raw_set, validate_doc, load_json_spec) |

All scripts declare PEP 723 inline metadata and run via mise, which
installs uv on demand:

```bash
mise x uv -- uv run scripts/add_bookmarks.py --doc <doc> --spec assets/specs/add_bookmarks.example.json
mise x uv -- uv run scripts/fix_heading_tabs.py --doc <doc> --mapping assets/specs/fix_heading_tabs.example.json
mise x uv -- uv run scripts/fix_enum_tabs.py --doc <doc> --items assets/specs/fix_enum_tabs.example.json
mise x uv -- uv run scripts/fix_note_tabs.py --doc <doc> --notes assets/specs/fix_note_tabs.example.json
```

- `assets/schemas/` -- JSON Schema contracts for each script input.
- `assets/specs/` -- example specs for reuse across projects.

### Two failure modes to check first

- **Hanging paragraphs** on re-runs -- remove `style=Figure` paragraphs
  before re-inserting; rebuild table sections in a retry loop. Details:
  `references/operations/idempotent-updates.md`.
- **Namespace stripping** with Python zipfile/ElementTree -- register every
  namespace prefix or the document fails OpenXML validation. Details:
  `references/operations/python-ooxml-namespace.md`.

## References

Formatting:

- [references/formatting/headings.md](references/formatting/headings.md)
- [references/formatting/enumerations.md](references/formatting/enumerations.md)
- [references/formatting/notes.md](references/formatting/notes.md)
- [references/formatting/tables-figures.md](references/formatting/tables-figures.md)
- [references/formatting/equations.md](references/formatting/equations.md)
- [references/formatting/citations.md](references/formatting/citations.md)
- [references/formatting/text-formatting.md](references/formatting/text-formatting.md)

Operations:

- [references/operations/tool-usage.md](references/operations/tool-usage.md)
- [references/operations/constraints.md](references/operations/constraints.md)
- [references/operations/xpath-patterns.md](references/operations/xpath-patterns.md)
- [references/operations/field-code-patterns.md](references/operations/field-code-patterns.md)
- [references/operations/tracked-changes.md](references/operations/tracked-changes.md)
- [references/operations/raw-xml-manipulation.md](references/operations/raw-xml-manipulation.md)
- [references/operations/idempotent-updates.md](references/operations/idempotent-updates.md)
- [references/operations/python-ooxml-namespace.md](references/operations/python-ooxml-namespace.md)

## Cross-references

- `sdo-writing` -- prose quality rules for the textual content
- `sdo-drafting` -- deliverable skeletons and the per-SDO style maps
- `officecli` -- the tool this skill drives
- `docx-svg` -- SVG image insertion when officecli is not available
