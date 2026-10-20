# Field Code Patterns

Use OOXML field char runs for all dynamic references. Never hard-code
reference numbers or figure/table numbers as plain text.

## REF cross-reference pattern

```xml
<w:r><w:fldChar w:fldCharType="begin"/></w:r>
<w:r><w:instrText xml:space="preserve"> REF tbl_example \h </w:instrText></w:r>
<w:r><w:fldChar w:fldCharType="separate"/></w:r>
<w:r><w:t>Table&#160;1</w:t></w:r>
<w:r><w:fldChar w:fldCharType="end"/></w:r>
```

The `<w:t>` between `separate` and `end` is the cached display value --
Word replaces it when fields are updated (F9). Bookmark names follow
the convention `tbl_<short_name>`, `fig_<short_name>`, or `ref_<short_name>`.

## SEQ auto-numbering pattern (figures and tables)

```xml
<w:r><w:fldChar w:fldCharType="begin"/></w:r>
<w:r><w:instrText xml:space="preserve"> SEQ Figure \* ARABIC </w:instrText></w:r>
<w:r><w:fldChar w:fldCharType="separate"/></w:r>
<w:r><w:t>1</w:t></w:r>
<w:r><w:fldChar w:fldCharType="end"/></w:r>
```

Replace `Figure` with `Table` for table captions. The bookmark for
cross-referencing must wrap only the numbered label part (e.g.
`Figure&#160;1`), not the full caption text.

## Citation SEQ + bookmark pattern

For reference list entries, use `SEQ Ref \* ARABIC` and insert a bookmark
`ref_<short_name>` around only the sequence counter field (not the square
brackets). Cross-reference in body text with `REF ref_<short_name>`.

______________________________________________________________________

## Replacing hardcoded reference tags with REF fields

### Rule: preserve existing brackets, replace only the tag text

Documents often contain `[ITU-T P.501]` as plain text. The `[` and `]` are
already in the document as literal characters. When replacing with a REF
field, keep those brackets as plain `<w:t>` text in adjacent runs — only
replace the tag text between them:

```xml
<!-- BEFORE: single run with hardcoded tag -->
<w:r><w:t>clause 7.3.4 of [ITU-T P.501].</w:t></w:r>

<!-- AFTER: bracket runs stay literal, only tag text becomes REF field -->
<w:r><w:t>clause 7.3.4 of [</w:t></w:r>
<w:r><w:fldChar w:fldCharType="begin"/></w:r>
<w:r><w:instrText xml:space="preserve"> REF REF_ITUT_P501 \h </w:instrText></w:r>
<w:r><w:fldChar w:fldCharType="separate"/></w:r>
<w:r><w:t xml:space="preserve">ITU-T P.501</w:t></w:r>
<w:r><w:fldChar w:fldCharType="end"/></w:r>
<w:r><w:t>].</w:t></w:r>
```

Never add brackets **around** a REF field — this produces `[[TAG]]`.

### REF fields inside `<w:ins>` elements are valid OOXML

Field character runs (`<w:fldChar>`, `<w:instrText>`) placed inside an
existing `<w:ins w:author="X">` element are valid and render correctly in
Word. There is no need to unwrap the field from tracked-change markup.

### Idempotency guard

After a paragraph is fixed, the REF field's display text (e.g.
`<w:t>ITU-T P.501</w:t>`) remains in the `<w:t>` stream and would
re-match a tag-pattern scanner. Always check `' REF REF_' in pxml` before
scanning a paragraph for tags to replace, to avoid double-processing.
