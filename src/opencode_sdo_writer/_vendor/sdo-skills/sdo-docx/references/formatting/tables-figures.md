# Tables and Figures

## Tables

> **SDO-specific note:** ITU-T uses per-clause SEQ counters (`SEQ TAB6`)
> with `TAB_` bookmark prefix instead of the generic `tbl_` prefix and
> global `SEQ Table`. See the per-SDO drafting skill for the concrete
> convention.

### Styles (use concrete names from SDO drafting skill)

- Caption (placed **above** the table): `table-caption`
- Header row: `table-header`
- Data rows: `table-data`
- Table notes (merged row at bottom of table): `table-note`

### Layout

- Every table **must** have at least one header row (style `table-header`),
  which by default is the first row (`header_rows=1`). Tables without a header
  row are not allowed.
- Centre all tables horizontally on the page.
- Final edit: set column width to "Autofit to contents" for all tables.
- **Header row repetition:** Enable "Repeat as header row at the top of each
  page" on **all** header rows (style `table-header`), not just the first row.
  Some tables have multi-row headers (e.g., a spanning title row followed by
  column labels). In OOXML this is `<w:tblHeader/>` inside `<w:trPr>` for each
  header row. This ensures headers repeat when a table spans a page break.
  Apply to every row that uses the header style, even if the table is expected
  to fit on a single page.

### Table captions and cross-references

- Caption format: `Table&#160;N: <caption text>` -- use a non-breaking
  space between "Table" and the number.
- Do **not** hard-code the table number. Use a `{SEQ Table \* ARABIC}`
  field for automatic numbering.
- Insert a **bookmark** around the `Table&#160;N` part only (not the full
  caption text). Name it `tbl_<short_name>`.
- Cross-reference in body text with `{REF tbl_<short_name>}`. Never insert
  hard-coded plain-text references.
- See `sdo-docx` for officecli field-code and bookmark injection.

## Figures

> **SDO-specific note:** ITU-T uses per-clause SEQ counters (`SEQ FIG6`)
> with `FIG_` bookmark prefix instead of the generic `fig_` prefix and
> global `SEQ Figure`. See the per-SDO drafting skill for the concrete
> convention.

### Styles (use concrete names from SDO drafting skill)

- Paragraph containing the image: `figure-para`
- Caption (placed **below** the figure): `figure-caption`
- Figure notes placed directly below the image and before the caption:
  `figure-note`

### Layout

- Maintain the original aspect ratio when resizing.
- Labels inside figures must be clearly legible; use maximum feasible font
  size.
- Prefer page width. Reduce only if the figure would exceed about 50% of
  the page height; minimum width is half the page width.
- Export diagrams as SVG for maximum quality. When using Draw.io, follow the
  [Draw.io SVG text rendering guidelines](https://www.drawio.com/doc/faq/svg-export-text-problems)
  to avoid text display issues in Word.

### ETSI-specific figure paragraph override

When the active per-SDO drafting skill is ETSI (`sdo-drafting`), enforce all
of the following:

- Figure image layout must be **In line with text**. Other Word wrapping
  layouts are forbidden.
- A single nominal figure may include multiple images/pictures within one
  `figure-para` paragraph.
- The image paragraph must end immediately after the final image. Do not place
  caption text in the same paragraph.
- Do not use soft line breaks (`Shift+Enter`) between image content and
  caption.
- Put the caption in a new paragraph using `figure-caption` style.

### Figure captions and cross-references

- Caption format: `Figure&#160;N: <caption text>` -- use a non-breaking
  space between "Figure" and the number.
- Do **not** hard-code the figure number. Use a `{SEQ Figure \* ARABIC}`
  field for automatic numbering.
- Insert a **bookmark** around the `Figure&#160;N` part only (not the full
  caption text). Name it `fig_<short_name>`.
- Cross-reference in body text with `{REF fig_<short_name>}`. Never insert
  hard-coded plain-text references.
- See `sdo-docx` for officecli field-code and bookmark injection.

## Style mapping

| Abstract | Concrete (per SDO drafting skill) |
|----------|-----------------------------------|
| `table-caption` | SDO-specific style for table caption above table |
| `table-header` | SDO-specific style for table header row |
| `table-data` | SDO-specific style for table data rows |
| `table-note` | SDO-specific style for table bottom-row notes |
| `figure-para` | SDO-specific style for paragraph containing image |
| `figure-caption` | SDO-specific style for figure caption below figure |
| `figure-note` | SDO-specific style for notes below figure |
