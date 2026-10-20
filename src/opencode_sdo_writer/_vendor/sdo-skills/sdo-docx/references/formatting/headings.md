# Headings

## Critical constraints

- **Never use MS Word automatic numbering** for clause/section headings.
  Automatic numbering causes formatting inconsistencies and can break
  references when using revision marks.

## Document mode terminology

- **Standards mode:** use clause terminology (`clause`, `subclause`) for
  structure and cross-references.
- **Meeting-document mode:** section terminology may be used when aligned
  with SDO convention and template wording.

## Numbering format

- Top level: `N` (e.g. `1`)
- Second level: `N.M` (e.g. `2.1`)
- Third level: `N.M.P` (e.g. `2.1.1`)
- `Introduction` is numbered like other top-level headings
  (e.g. `1\tIntroduction`).

## Formatting

- Insert a real `<w:tab/>` run element between the heading number and the
  heading title; never use spaces for indentation (see
  `sdo-docx` for officecli tab-run injection patterns).
- Use heading styles by level:
  `heading-1` (→ concrete style), `heading-2`, `heading-3`, etc.
- Do not apply manual font-size or bold overrides to heading paragraphs --
  rely on style definitions.
- The `References` section does **not** get a number. Use `heading-1` style
  but write only the word `References` without a manual number prefix.
- A **Bibliography** (informative references, some SDOs only) uses
  `bibliography-heading` style, **not** `heading-1`. It also requires
  `pageBreakBefore: true` set on the heading paragraph. See
  `citations.md` for Bibliography rules and the per-SDO drafting skill
  for the concrete style ID.

## Appendix and Bibliography headings

Non-integral appendix headings and Bibliography headings use a dedicated
`appendix-heading` / `bibliography-heading` abstract style that is
separate from `heading-1`. The per-SDO drafting skill provides the
concrete style ID (e.g. `Appendix_No & title` in ITU-T).

**Page break before:** Always set `pageBreakBefore: true` as a paragraph
property on `appendix-heading` and `bibliography-heading` paragraphs.
Do **not** insert a separate empty paragraph carrying a manual page break
— this creates double breaks under some Word pagination settings.

## Style mapping

| Abstract | Concrete (per SDO drafting skill) |
|----------|-----------------------------------|
| `heading-1` | SDO-specific style for top-level headings |
| `heading-2` | SDO-specific style for second-level headings |
| `heading-3` | SDO-specific style for third-level headings |
| `appendix-heading` | SDO-specific style for non-integral appendix headings |
| `bibliography-heading` | SDO-specific style for Bibliography heading (may equal `appendix-heading`) |
