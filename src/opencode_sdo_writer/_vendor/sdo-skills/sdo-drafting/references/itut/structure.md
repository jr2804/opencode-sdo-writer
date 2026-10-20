# ITU-T template structure and batch workflow

Template layout (contribution and liaison statement), heading conventions and
officecli batch patterns for ITU-T documents.

## Assets

- `assets/itut/template.docx` -- canonical ITU-T contribution Word template with
  all required styles and header structure (9-row header table, abstract
  table, running header, footer). Copy or use as reference when starting a
  new contribution. This is a user-provided template carrying ITU-T branding,
  predefined styles, and placeholder content. Do **not** modify the original;
  always work on a copy.
- `assets/itut/itu-t-sg12-contribution-template.docx` -- downloaded official ITU-T
  contribution template (SG12 example) for reproducible offline use.
- `assets/itut/itu-t-sg12-liaison-statement-template.docx` -- downloaded official ITU-T
  Liaison Statement template (SG12 example) for drafting outgoing LS documents.
- `itut-reference/assets/itu-t-recommendation-skeleton.docx` --
  downloaded official ITU-T Recommendation skeleton for style-baseline checks.

## Canonical ITU-T template sources (online)

These are the upstream sources for the downloaded assets above:

- Contribution template (example SG12):
  `https://www.itu.int/dms_pub/itu-t/oth/0A/0F/T0A0F00002F0012MSWE.docx`
- Liaison Statement template (example SG12):
  `https://www.itu.int/dms_pub/itu-t/oth/0A/0F/T0A0F00000B0006MSWE.docx`
- New Recommendation skeleton (latest Word styles baseline):
  `https://www.itu.int/en/ITU-T/studygroups/Documents/Doc-ITUT-Recs-Skelet.docx`

### Template selection rule

- For **meeting contributions**: start from
  `assets/itut/itu-t-sg12-contribution-template.docx`.
- For **outgoing Liaison Statements**: start from
  `assets/itut/itu-t-sg12-liaison-statement-template.docx`.
- For **Recommendation drafting or style refresh checks**: use
  `itut-reference/assets/itu-t-recommendation-skeleton.docx`
  to confirm style definitions (including appendix and bibliography headings).
- Use the online URLs only to refresh these local files when needed.

______________________________________________________________________

## Template structure

ITU-T contribution documents use a structured header **table** (not
paragraphs). This differs from 3GPP.

### Header table (`/body/tbl[1]`)

9 rows with the following cell layout:

| Row | Cell | Content |
|-----|------|---------|
| tr[1]/tc[3] | Document number | 3rd run is the highlighted placeholder; set text to `0xxx` |
| tr[4]/tc[2] | Question(s) | e.g. `Question 9/12` |
| tr[4]/tc[3] | Place and date | e.g. `Geneva, 09-17 June 2026` |
| tr[6]/tc[2] | Source organization | e.g. `HEAD acoustics GmbH` |
| tr[7]/tc[2] | Title | Contribution title |
| tr[8]/tc[2] | Contact 1 | Tab-separated: `Name\tOrganization\tCountry` |
| tr[8]/tc[3]/p[1]/r[4] | Tel number | Highlighted run |
| tr[8]/tc[3]/p[1]/r[8] | E-mail | Highlighted run |
| tr[9] | Contact 2 | Clear with `""` if unused |

### Abstract table (`/body/tbl[2]`)

1 row x 2 cells: `"Abstract:"` label (tc[1]) + content (tc[2]/p[1]).

### Running header

`/header[1]/p[@paraId=00100052]/r[4]` -- document number (e.g. `SG12-C0xxx`).

### Instruction paragraphs to delete

Remove all 8 yellow-highlighted instruction paragraphs (paraIds
`0010003A` through `00100048`) using `remove` commands in a setup batch
before adding content.

### Horizontal rule

`/body/p[@paraId=0010004C]` -- `_______________________` separator.

### First content paragraph

`/body/p[@paraId=0010004E]` -- empty paragraph after the rule; first
content goes after this.

> **Key finding:** The ITU-T template may NOT contain a `Body Text` style.
> If absent, use `Normal` for body paragraphs. Always verify with
> `mise x github:iOfficeAI/OfficeCLI -- officecli get <doc> /styles --depth 1` on any new template.

______________________________________________________________________

## Liaison Statement template structure

The LS template (`assets/itut/itu-t-sg12-liaison-statement-template.docx`) uses an
11-row header table. This differs from the contribution template above.

### Header table (`/body/tbl[1]`)

| Row | Cell | Content | Style |
|-----|------|---------|-------|
| tr[1]/tc[2] | Question(s) | e.g. `4/12` | `TSBHeaderQuestion` |
| tr[1]/tc[4] | Meeting | e.g. `Geneva, 9-17 June 2026` | `VenueDate` (right-aligned) |
| tr[2]/tc[2] | Study Group | e.g. `12` | `Normal` |
| tr[2]/tc[4] | Working Party | e.g. `WP1/12` | `Normal` |
| tr[3]/tc[2] | Source | e.g. `ITU-T Study Group 12` | `TSBHeaderSource` |
| tr[4]/tc[2] | Title | LS title | `TSBHeaderTitle` |
| tr[5] | "LIAISON STATEMENT" banner | merged across all 6 columns, centred | `Normal` + bold |
| tr[6]/tc[2] | For action to | e.g. `ITU-T Q10/21` | `LSForAction` |
| tr[7]/tc[2] | For information to | e.g. `ITU-T SG21` | `LSForInfo` |
| tr[8]/tc[2] | Approval | e.g. `Q4/12 rapporteur group meeting...` | `LSApproval` |
| tr[9]/tc[2] | Deadline | e.g. `1 September 2026` | `LSDeadline` |
| tr[10]/tc[2] | Contact 1 — Name/Org/Country | Tab-separated fields | `Normal` |
| tr[10]/tc[3] | Contact 1 — Tel/E-mail | Tab-separated with labels | `Normal` + tabs @ 794 twips |
| tr[11] | Contact 2 | Clear with `""` if unused | `Normal` |

**Note:** The LS template has 6 table columns (not 2). Cells use `colspan`
and `rowspan`:

- tr\[1\]: 4 visible cells with colspans 1/2/2/1
- tr[3] onward: cells span across all 6 columns

Populate via officecli batch targeting the style names rather than paraIds:

```json
[
  { "command": "set", "path": "/body/tbl[1]/tr[1]/tc[2]/p",
    "props": { "text": "4/12" } },
  { "command": "set", "path": "/body/tbl[1]/tr[4]/tc[2]/p",
    "props": { "text": "LS on ...", "style": "TSBHeaderTitle" } }
]
```

### LS-specific fields

- **Abstract** is in a separate table (`/body/tbl[2]`), same structure as
  the contribution template.
- The LS body follows after the abstract table, with no instruction
  paragraphs to delete (unlike the contribution template).
- The first body paragraph is at `/body/p[paraId=70FBDF66]` in the template.

______________________________________________________________________

## Heading conventions (ITU-T-specific)

- **No hard-coded numbers in heading text.** The template's heading styles
  have automatic outline numbering. Write just the title: `"Introduction"`
  not `"1\tIntroduction"`.
- `Headingb` style is used for sub-headings *within a proposed clause
  block* (e.g. `"7.5.4 Maximum absolute prediction error (maxabs)"`,
  subsection labels `"a)\tUnconstrained least-squares fit"`). These appear
  in the TOC as `Heading_b` entries but do NOT get automatic numbering.

______________________________________________________________________

## Batch workflow patterns

### General workflow

1. **Start from template**: `Copy-Item "docs\template.docx" -Destination "<output>.docx" -Force`
2. **Resident mode**: `mise x github:iOfficeAI/OfficeCLI -- officecli open <doc>` before editing; `mise x github:iOfficeAI/OfficeCLI -- officecli close <doc>` at end.
3. **Batch mode**: pipe JSON arrays to `mise x github:iOfficeAI/OfficeCLI -- officecli batch <doc>`. Each JSON
   array must contain at most 12 JSON command objects. If more are needed,
   split into sequential batch calls.
4. **Validate frequently**: `mise x github:iOfficeAI/OfficeCLI -- officecli validate <doc>` after every major
   batch update.

### Common errors

| Error | Root Cause | Fix |
|-------|-----------|-----|
| Conclusion heading missing | Batch added heading + table together; table `set` commands failed (index didn't exist yet) | Split: add heading separately, then table, then fill with dedicated batch |
| Paragraphs reversed in `add` with `after` | Each `add` with `after: anchor` inserts immediately after the anchor, pushing any previously added paragraphs down | Submit `add` commands in **reverse reading order** (last paragraph first, first paragraph last). The first add ends up furthest from the anchor, the last add ends up closest. |
| `\left\right` with subscripts crashes equation | OMML parser limitation | Use plain `(` `)` delimiters |
| "Body Text" style not found | Template uses `Normal` as body style | Use `Normal` for body paragraphs |
| Running header shows placeholder | Header paragraph r[4] not updated | Target `/header[1]/p[@paraId=00100052]/r[4]` and set text |
| `ind.left` + `alignment` in one command | Schema ordering bug in officecli | Split into separate `add` + `set` calls |

### Indentation for proposed clause text

Text inside a proposed new/amended clause uses `"ind.left":"720"`
(720 twips = 0.5 inch). Sub-items use `"ind.left":"1080"`.

______________________________________________________________________
