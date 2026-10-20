# Notes

## Styles

- Main note (last in a consecutive block): `note-main` (→ concrete style)
- All preceding notes in a block: `note-continuation`
- Table notes (merged bottom row of a table): `table-note`
- Figure notes (below a figure, before the caption): `figure-note`

## Formatting

- Format: `NOTE&#160;N:\t<text>` -- NOTE (uppercase), non-breaking space,
  number, colon, **real tab run**, note text.
- Omit the number when there is exactly one note in the section.
- For multiple notes: manually number them (`NOTE&#160;1`, `NOTE&#160;2`,
  ...); restart numbering from 1 in each section.
- The **last** note in a consecutive block uses `note-main`; all preceding
  notes in the block use `note-continuation` (prevents visual separation
  between grouped notes).
- Insert a real `<w:tab/>` run element after the colon; do not use spaces
  (see `sdo-docx` for officecli tab-run injection).
- Do not use manual formatting (bold, italic, font size) for note text --
  rely on the style definition.

## Content rules

- When generalising, expanding, or adding new content, **add a new note**
  rather than replacing an existing note. Existing notes may still be
  needed for context or may contain constraints that are not yet ready for
  removal.
- If an existing note is truly superseded or incorrect, replace it and
  mark the change with tracked changes (see
  `sdo-docx/references/operations/tracked-changes.md`).
- Keep each note focused on a single point. Split unrelated observations
  into separate notes.

## Example (3GPP/ETSI style names)

```text
NOTE 1:\t<text>     -- style NO (first note)
NOTE 2:\t<text>     -- style NW (continuation)
NOTE 3:\t<text>     -- style NO (last note in block)
```

## Style mapping

| Abstract | Concrete (per SDO drafting skill) |
|----------|-----------------------------------|
| `note-main` | SDO-specific style for the last note in a block |
| `note-continuation` | SDO-specific style for preceding notes in a block |
| `table-note` | SDO-specific style for table merged-bottom-row notes |
| `figure-note` | SDO-specific style for notes below a figure |
