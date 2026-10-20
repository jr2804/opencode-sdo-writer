# Citations

## References section placement

- The `References` section (normative) typically appears as the last numbered
  clause before any annexes, or as the last unnumbered section after annexes,
  depending on SDO conventions.
- Unlike numbered clauses, `References` is **not** numbered; use `heading-1`
  style without a manual number prefix.
- For some SDOs (e.g. ITU-T), a **Bibliography** may follow all annexes as
  the very last element. The Bibliography uses a different heading style
  (`appendix-heading` abstract name) and requires a page break before it.
  See the per-SDO drafting skill for details.

## Entry format

- Each entry: `[N]\t<citation text>` -- bracket-wrapped number, real tab
  run, then citation text.
- Style: `reference-entry` (→ concrete style) for every reference entry.
- Do **not** hard-code the number. Use a `{SEQ Ref \* ARABIC}` field and
  place a **bookmark** (`ref_<short_name>`) around the sequence field only
  -- not around the square brackets.
- Cross-reference in body text with `{REF ref_<short_name>}`. Never use
  hard-coded plain-text reference numbers.
- See `sdo-docx` for officecli field-code and bookmark injection.

## Ordering and completeness

- List references in the order they first appear in the body text.
- Every listed reference **must** be cited at least once in the body.
- Do not include uncited references.

## Style mapping

| Abstract | Concrete (per SDO drafting skill) |
|----------|-----------------------------------|
| `reference-entry` | SDO-specific style for each references entry |

______________________________________________________________________

## Bibliography (informative references)

Some SDOs (e.g. ITU-T) include a **Bibliography** as the last clause,
containing informative references that are not cited normatively.

### Rules

- **Heading style:** Use `bibliography-heading` (abstract name) — a
  distinct style from `heading-1`. In ITU-T this maps to `Appendix_No & title`. Do **not** apply `heading-1` to a Bibliography heading.
- **Page break before:** The Bibliography heading paragraph **must** have
  `pageBreakBefore: true` set as a paragraph property. Never use a
  separate empty paragraph with a manual page break.
- **Entry style:** Identical to normative references — use `reference-entry`
  style with the same `[N]\t<text>` format, `{SEQ Ref \* ARABIC}` fields,
  and bookmarks. Do not use `body-text` or `Normal` for entries.

### Style mapping

| Abstract | Concrete (per SDO drafting skill) |
|----------|-----------------------------------|
| `bibliography-heading` | SDO-specific style for Bibliography heading (may equal `appendix-heading`) |
| `reference-entry` | Same style used for normative reference entries |
