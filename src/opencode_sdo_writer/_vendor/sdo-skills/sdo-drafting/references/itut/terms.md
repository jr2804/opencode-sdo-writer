# ITU-T term formatting (clause 3 Definitions)

Pseudo-subclause term paragraphs, tab stops and tracked-change construction.

## Term formatting (clause 3 Definitions)

Terms in clause 3 (both 3.1 "Terms defined elsewhere" and
3.2 "Terms defined in this Recommendation") use **pseudo-subclause**
formatting:

- Numbered like subclauses (3.1.1, 3.1.2, ...) but are NOT heading
  paragraphs — they do NOT appear in the table of contents

- Style: `Normal` (body-text style, fallback if `Body Text` absent)

- Each term is a single paragraph in the format:

  `<bold>3.1.N\tTERM NAME</bold>: definition text`

### Run structure

| Run | Content | Format |
|-----|---------|--------|
| r[1] | `3.1.N` (number prefix) | bold |
| r[2] | `<w:tab/>` | bold (on run) |
| r[3] | term name | bold |
| r[4] | `:` + definition text | normal |

### Tab stop

The ITU-T template's `Normal` style does **not** include a tab stop at
1.5 cm. Each term paragraph must have this added manually:

```xml
<w:pPr>
  <w:tabs>
    <w:tab w:val="left" w:pos="851"/>
  </w:tabs>
</w:pPr>
```

851 twips = 1.5 cm. Use `raw-set` to inject this since officecli L2
`set` on a paragraph with revision marks does not create tracked
changes.

### Creating terms with tracked changes

Since officecli L2 `set`/`add` does not create revision marks, terms
must be built via `raw-set` with the content wrapped in `w:ins`
elements:

```xml
<w:p xmlns:w="..." xmlns:w14="..." w14:paraId="PARAID">
  <w:pPr>
    <w:tabs>
      <w:tab w:val="left" w:pos="851"/>
    </w:tabs>
  </w:pPr>
  <w:ins w:author="Author Name" w:date="..." w:id="...">
    <w:r>
      <w:rPr><w:b/></w:rPr>
      <w:t xml:space="preserve">3.1.N</w:t>
    </w:r>
    <w:r>
      <w:rPr><w:b/></w:rPr>
      <w:tab/>
    </w:r>
    <w:r>
      <w:rPr><w:b/></w:rPr>
      <w:t xml:space="preserve">TERM NAME</w:t>
    </w:r>
    <w:r>
      <w:t xml:space="preserve">: definition text</w:t>
    </w:r>
  </w:ins>
</w:p>
```

Replace the target paragraph via:

```text
officeli raw-set <doc> /document \
  --xpath '//w:p[@w14:paraId="PARAID"]' \
  --action replace \
  --xml '<w:p>...</w:p>'
```

### Notes attached to terms

A `Note`-style paragraph that belongs to a term (e.g., clarifying a
definition) stays after the term paragraph with style `Note`. These are
not pseudo-subclauses — use the standard note formatting convention.

______________________________________________________________________
