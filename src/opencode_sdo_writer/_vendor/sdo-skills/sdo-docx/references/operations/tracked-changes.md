# OOXML Tracked Changes Patterns

Correct XML structures for revision marks in .docx documents. These must be
applied via `officecli raw-set` -- high-level commands cannot produce them.

## Critical rule: paragraph-level vs. run-level

| Scope | Marker placement | Content element |
|-------|-----------------|-----------------|
| Entire paragraph inserted | `<w:ins>` in `<w:pPr>/<w:rPr>` | `<w:t>` (normal text) |
| Run inserted within existing paragraph | `<w:ins>` wrapping `<w:r>` | `<w:t>` (normal text) |
| Entire paragraph deleted | `<w:del>` in `<w:pPr>/<w:rPr>` | `<w:delText>` |
| Run deleted within existing paragraph | `<w:del>` wrapping `<w:r>` | `<w:delText>` |

**Never wrap entire paragraph content with `<w:ins>` or `<w:del>` at the
run-sibling level.** The OOXML spec requires revision markers on paragraph
properties, not as paragraph children. Wrong structure silently produces
no visible tracked changes.

______________________________________________________________________

## Pattern 1: Inserted paragraph (entire paragraph is new)

```xml
<w:p>
  <w:pPr>
    <w:rPr>
      <w:ins w:id="1" w:author="Author Name" w:date="2026-05-22T10:00:00Z"/>
    </w:rPr>
    <w:pStyle w:val="Note"/>
  </w:pPr>
  <w:r>
    <w:t xml:space="preserve">NOTE: New note text added to the document.</w:t>
  </w:r>
</w:p>
```

**Key points:**

- `<w:ins>` goes inside `<w:pPr>/<w:rPr>` for full-paragraph insertions
- Content uses normal `<w:t>` (not `<w:delText>`)
- `w:id` must be unique across all tracked changes in the document
- Before this paragraph, also inject the paragraph mark deletion marker
  in the preceding paragraph's `<w:pPr>/<w:rPr>` so Word shows the
  boundary correctly

______________________________________________________________________

## Pattern 2: Deleted paragraph (entire paragraph removed)

```xml
<w:p>
  <w:pPr>
    <w:rPr>
      <w:del w:id="2" w:author="Author Name" w:date="2026-05-22T10:00:00Z"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:delText xml:space="preserve">Old paragraph text that is being removed.</w:delText>
  </w:r>
</w:p>
```

**Key points:**

- `<w:del>` goes inside `<w:pPr>/<w:rPr>` for full-paragraph deletions
- Content MUST use `<w:delText>` (not `<w:t>`) -- otherwise text appears
  as still present with only the deletion marker
- `xml:space="preserve"` is critical on `<w:delText>` to preserve leading/
  trailing spaces

______________________________________________________________________

## Pattern 3: Inserted run (text added within existing paragraph)

```xml
<w:p>
  <w:pPr>
    <w:pStyle w:val="Normal"/>
  </w:pPr>
  <w:r>
    <w:t>Existing text remains unchanged.</w:t>
  </w:r>
  <w:ins w:id="3" w:author="Author Name" w:date="2026-05-22T10:00:00Z">
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
        <w:sz w:val="22"/>
      </w:rPr>
      <w:t xml:space="preserve"> New text inserted at this point.</w:t>
    </w:r>
  </w:ins>
  <w:r>
    <w:t>More existing text after the insertion.</w:t>
  </w:r>
</w:p>
```

**Key points:**

- `<w:ins>` wraps complete `<w:r>` elements as a child of `<w:p>`
- The inserted `<w:r>` should inherit or explicitly set the same
  formatting as surrounding runs
- Content uses normal `<w:t>` (not `<w:delText>`)

______________________________________________________________________

## Pattern 4: Deleted run (text removed within existing paragraph)

```xml
<w:p>
  <w:pPr>
    <w:pStyle w:val="Normal"/>
  </w:pPr>
  <w:r>
    <w:t>Text before the deletion.</w:t>
  </w:r>
  <w:del w:id="4" w:author="Author Name" w:date="2026-05-22T10:00:00Z">
    <w:r>
      <w:delText xml:space="preserve">This text is marked for deletion.</w:delText>
    </w:r>
  </w:del>
  <w:r>
    <w:t xml:space="preserve"> Text after the deletion.</w:t>
  </w:r>
</w:p>
```

**Key points:**

- `<w:del>` wraps complete `<w:r>` elements as a child of `<w:p>`
- Content MUST use `<w:delText>` (not `<w:t>`) -- `<w:t>` with `<w:del>`
  does not render as tracked-deleted
- `xml:space="preserve"` is critical on `<w:delText>`

______________________________________________________________________

## Pattern 5: Inserted paragraph preceded by run-level deletion

When inserting a new paragraph after existing text and also deleting some
of the preceding paragraph's runs, combine patterns:

```xml
<!-- Preceding paragraph with a deleted suffix -->
<w:p>
  <w:pPr>
    <w:pStyle w:val="Normal"/>
  </w:pPr>
  <w:r>
    <w:t>Text that stays.</w:t>
  </w:r>
  <w:del w:id="5" w:author="Author Name" w:date="2026-05-22T10:00:00Z">
    <w:r>
      <w:delText xml:space="preserve"> text being removed.</w:delText>
    </w:r>
  </w:del>
</w:p>

<!-- New fully inserted paragraph -->
<w:p>
  <w:pPr>
    <w:rPr>
      <w:ins w:id="6" w:author="Author Name" w:date="2026-05-22T10:00:00Z"/>
    </w:rPr>
    <w:pStyle w:val="Normal"/>
  </w:pPr>
  <w:r>
    <w:t>New paragraph with revision mark visible.</w:t>
  </w:r>
</w:p>
```

______________________________________________________________________

## Required attributes

| Attribute | Value | Notes |
|-----------|-------|-------|
| `w:id` | Positive integer | Must be unique across ALL tracked changes in the document. Start from a high number (e.g. 100) to avoid collisions with existing revisions. |
| `w:author` | Author name string | Must match the document's current author or the name shown in the revision. Use `mise x github:iOfficeAI/OfficeCLI -- officecli get <doc> "//w:ins/@w:author"` to find existing author names. |
| `w:date` | ISO 8601 timestamp | `2026-05-22T10:00:00Z` format. Use current date/time. |

______________________________________________________________________

## Finding the next available `w:id`

```bash
mise x github:iOfficeAI/OfficeCLI -- officecli query doc.docx "inserts" --json
# Parse the max `w:id` across all <w:ins> and <w:del> elements.
# Use max_id + 1 for the new change marker.
```

______________________________________________________________________

## Common mistakes

| Wrong | Why it fails |
|-------|-------------|
| `<w:p><w:ins w:id="1">...<w:r>...</w:r></w:ins></w:p>` | `<w:ins>` as direct child of `<w:p>` -- marker invisible. Must be in `<w:pPr>/<w:rPr>`. |
| `<w:del><w:r><w:t>text</w:t></w:r></w:del>` | Run-level deletion with `<w:t>` instead of `<w:delText>` -- text not shown as deleted. |
| `xml:space` missing on `<w:delText>` | Leading/trailing spaces in deleted text are stripped. |
| Paragraph has `<w:ins>` in `<w:rPr>` but preceding paragraph does NOT have a paragraph-mark deletion marker | Word may show a spurious empty deleted paragraph. Inject `<w:del>` in preceding paragraph's `<w:rPr>` too. |
| Reusing `w:id` values | Revision markers collide; some changes may not render correctly. |

______________________________________________________________________

## Pattern 6: Modifying text already inside `<w:ins>` — inherit context, don't wrap

When existing text inside `<w:ins w:author="X">` needs to be modified
(e.g. replacing a hardcoded reference tag with a REF field), **do not add
a new `<w:ins>` wrapper**. Instead, replace the run span in-place. The
new runs automatically inherit the surrounding `<w:ins>` context,
preserving the original author and date without any extra markup.

**Before (hardcoded reference inside existing ins):**

```xml
<w:ins w:id="1860" w:author="Ungerechts, Torsten" w:date="2026-05-07T...">
  <w:r><w:t>signal level according to [ITU-T P.56].</w:t></w:r>
</w:ins>
```

**After (REF field replacing tag — same ins context, no new wrapper):**

```xml
<w:ins w:id="1860" w:author="Ungerechts, Torsten" w:date="2026-05-07T...">
  <w:r><w:t>signal level according to [</w:t></w:r>
  <w:r><w:fldChar w:fldCharType="begin"/></w:r>
  <w:r><w:instrText xml:space="preserve"> REF REF_ITUT_P56 \h </w:instrText></w:r>
  <w:r><w:fldChar w:fldCharType="separate"/></w:r>
  <w:r><w:t xml:space="preserve">ITU-T P.56</w:t></w:r>
  <w:r><w:fldChar w:fldCharType="end"/></w:r>
  <w:r><w:t>].</w:t></w:r>
</w:ins>
```

**Implementation:** Replace from `fr.start` (start of first involved run)
to `lr.end` (end of last involved run). Everything before `fr.start`
contains the open `<w:ins>` tag; everything after `lr.end` contains its
closing `</w:ins>`. The new runs sit naturally inside that context.

**Key rule:** the brackets `[` and `]` are **kept as literal text** in
adjacent runs. Only the tag text between them is replaced by the REF field.
Never add extra brackets around the REF field.

**Auto-skip deleted text:** Deleted text uses `<w:delText>`, not `<w:t>`.
Any scanner based on `re.findall(r'<w:t[^>]*>([^<]+)</w:t>', pxml)` will
automatically skip deleted content — no special filtering needed.

**Idempotency:** After a paragraph is fixed, the REF field's display text
(e.g. `<w:t>ITU-T P.56</w:t>`) still appears in the `<w:t>` stream and
would re-match a tag pattern scan. Guard against double-replacement by
checking `' REF REF_' in pxml` before scanning for tags to replace.
