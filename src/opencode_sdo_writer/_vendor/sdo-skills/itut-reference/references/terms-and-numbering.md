# ITU-T Terms and Numbering

## Term formatting (clause 3 Definitions)

Terms in clause 3 -- both 3.1 "Terms defined elsewhere" and 3.2 "Terms defined
in this Recommendation" -- use **pseudo-subclause** formatting:

- They are numbered like subclauses (3.1.1, 3.1.2, ...) but are **not**
  heading paragraphs and do **not** appear in the table of contents.
- Each term is a single paragraph in the pattern

  ```text
  <bold>3.1.N\tTERM NAME</bold>: definition text
  ```

- The number prefix (`3.1.N`) and the term name are **bold**; a **tab**
  separates the number from the term name; the term name ends with a
  **colon and space**, followed by the definition text (not bold).
- The paragraph uses the body-text style with a manually set tab stop at
  1.5 cm (851 twips) -- that tab stop is not part of the default `Normal`
  style in the ITU-T template.

Operational construction (run structure, tab stop XML, tracked-change
assembly) is in `sdo-drafting` -> `references/itut/terms.md`.

## Subdivision numbering

- Digits separated by periods: 1, 1.1, 1.1.1
- No trailing period after a single number
- Do not create subclause 1.1 unless 1.2 also exists

## Bibliography

The Bibliography is an **optional, non-normative** clause with informative
references (sources not cited normatively in the body).

- **Position:** always the last clause of the Recommendation, after all
  integral and non-integral annexes, and before the Index if present.
- **Heading:** style `Appendix_No & title` (the same style used for
  non-integral appendix headings). Write only the word `Bibliography` -- no
  number prefix.
- **Page break:** there must be a page break immediately before the heading,
  applied as `pageBreakBefore: true` on the heading paragraph and not as a
  separate break paragraph.
- **Entries:** style `References`, the same style as normative reference
  entries in clause 2. Format `[N]\t<citation text>` with a
  `{SEQ Ref \* ARABIC}` field and a bookmark.

Counter and field details: `sdo-drafting` -> `references/itut/numbering.md`.

## Cross-references

- `sdo-drafting` -- ITU-T structure, style names, terms and numbering rules
- `itut-reference` -- organisation, roles, document types
