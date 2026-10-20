# Text Formatting

## Base style

- Use `body-text` (→ concrete style) for all main body paragraphs. Do not
  mix manual font overrides into body text.

## Inline code and filenames

- Use `code-text` (→ concrete style) for inline code snippets, function/
  variable names, and filenames that refer to code artifacts.
- Do not apply manual monospace formatting (bold, italic, font change)
  for these elements.

## Non-breaking spaces

- Insert a non-breaking space (`&#160;` / `\u00a0`) between a number and
  its unit: e.g. `-26&#160;dBov`, `96&#160;dB`.
- Insert a non-breaking space between "Figure" / "Table" and their number
  in captions and cross-references: e.g. `Figure&#160;1`, `Table&#160;1`.

## Alignment

- Never insert multiple consecutive spaces to achieve visual alignment. Use
  explicit tab characters (`\t` via a `<w:tab/>` run) or rely on
  style-defined indentation.
- Do not use manual indentation overrides for alignment purposes.

## Quotation marks

- Never use curly/typographic quotes (`"`, `"`, `'`, `'`) in document text.
  Always use straight quotes (`"` for double, `'` for single).

## Emphasis

- Do not apply manual bold or italic formatting to notes, enumerations, or
  headings -- use the appropriate paragraph style instead.

## Style mapping

| Abstract | Concrete (per SDO drafting skill) |
|----------|-----------------------------------|
| `body-text` | SDO-specific style for main body paragraphs |
| `code-text` | SDO-specific style for inline code / filenames |
