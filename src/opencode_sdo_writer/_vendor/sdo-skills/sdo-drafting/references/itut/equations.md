# ITU-T equation conventions

Display and inline equation structure, SEQ numbering, bookmarks and known
KaTeX/OMML constraints.

## Equation conventions

### Display equations (numbered, standalone)

Use a **single paragraph** with style `Equation` containing
`\t[equation]\t(<SEQ EQ>)`. The `Equation` style has two tab stops:
first centred at 4820 (for the equation), second right-aligned at 9639
(for the label). This centres the equation and right-aligns the label
on the same line. Set paragraph `alignment: left` so the tab stops
(not paragraph justification) control positioning — `left` here means
"do not centre-justify the paragraph itself," not "left-align the
equation."

Target structure:

```text
[p intro sentence]
[p style=Equation]  <- \t + oMath + \t + (EQ_seq_result)  -- one paragraph
[p style=Equation_legend]  <- "where..." annotation paragraph
```

**Numbering:** Do NOT hard-code equation numbers. Use `{SEQ EQ \* ARABIC}`
for automatic numbering. Wrap the label `(SEQ)` in a bookmark named
`EQ_<short_name>` (e.g., `EQ_MOSK`, `EQ_XPLUS`). Cross-reference in body
text with `{REF EQ_<short_name>}`.

Build with officecli in order:

```json
[
  { "command": "set", "path": "/body/p[@paraId=XXXX]",
    "props": { "style": "Equation", "alignment": "left", "text": "\t" } },
  { "command": "add", "parent": "/body/p[@paraId=XXXX]", "type": "equation",
    "props": { "mode": "inline", "formula": "..." } },
  { "command": "add", "parent": "/body/p[@paraId=XXXX]", "type": "run",
    "props": { "text": "\t(" } },
  { "command": "add", "parent": "/body/p[@paraId=XXXX]", "type": "field",
    "props": { "code": "SEQ EQ \\* ARABIC", "bookmark": "EQ_NAME" } },
  { "command": "add", "parent": "/body/p[@paraId=XXXX]", "type": "run",
    "props": { "text": ")" } }
]
```

**IMPORTANT:** Do NOT combine `ind.left` with `alignment` in a single
`add` paragraph command. officecli emits `w:ind` AFTER `w:jc` in the
OOXML, violating the schema. Use a separate `set` call to add indentation
after creation.

### Inline equations in body text

Rebuild paragraphs with mixed text + inline equations as a sequence of
`set` + `add` commands (run, equation, run, ...). Each JSON array
passed to `officecli batch` must contain at most 12 JSON command objects.
If more are needed, split into sequential batch calls.

### Known KaTeX constraints

| Forbidden | Use instead |
|---|---|
| `\text{word}` | `\mathrm{word}` |
| `\left(...\right)` with sub/superscripts inside | plain `(...)` -- OMML auto-sizes |
| `\tag{label}` | Put label in the same paragraph with tab |
| `\mathcal{L}` | `\mathit{L}` |

______________________________________________________________________
