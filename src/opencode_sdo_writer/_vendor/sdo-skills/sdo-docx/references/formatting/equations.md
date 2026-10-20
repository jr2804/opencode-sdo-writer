# Equations

## Display equations (numbered, standalone)

Use a **single paragraph** with style `equation` containing
`\t<equation>\t(<SEQ EQ>)`.

### Structure

```text
[p style=equation]  <- \t + oMathPara + \t + (N)  -- one paragraph
```

The `equation` style must define two tab stops:

1. **Centre-aligned** tab (positions the equation in the middle of the page)
2. **Right-aligned** tab (positions the equation number at the right margin)

Set paragraph `alignment: left` so the tab stops (not paragraph
justification) control positioning — `left` here means "do not
centre-justify the paragraph itself," not "left-align the equation."

### Numbering

Do **not** hard-code the equation number. Use a `{SEQ EQ \* ARABIC}`
field for automatic numbering.

Insert a **bookmark** around the `(<SEQ EQ>)` part (the number and
parentheses). Name it `EQ_<short_name>`.

Cross-reference in body text with `{REF EQ_<short_name>}`.

### Bookmark naming

| Equation content | Suggested bookmark |
|---|---|
| Left-hand variable or short mnemonic | `EQ_XPLUS`, `EQ_MOSK`, `EQ_IFFT` |

Keep names short (≤10 chars), uppercase, ASCII-only.

### Field code pattern

```text
{ SEQ EQ \* ARABIC }
```

Wrapped in a bookmark:

```xml
<w:bookmarkStart w:name="EQ_MOSK" w:id="N"/>
<w:r><w:fldChar w:fldCharType="begin"/></w:r>
<w:r><w:instrText xml:space="preserve"> SEQ EQ \* ARABIC </w:instrText></w:r>
<w:r><w:fldChar w:fldCharType="separate"/></w:r>
<w:r><w:t>6</w:t></w:r>
<w:r><w:fldChar w:fldCharType="end"/></w:r>
<w:bookmarkEnd w:id="N"/>
```

## Inline equations in body text

Use `oMath` (inline Office Math) mixed with text runs inside `body-text`
paragraphs. No numbering, no tab stops.

## Style mapping

| Abstract | Concrete (per SDO drafting skill) |
|----------|-----------------------------------|
| `equation` | SDO-specific style for display equation paragraph |
| `equation-legend` | SDO-specific style for annotation paragraph below equation |
