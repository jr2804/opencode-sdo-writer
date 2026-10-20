# Python OOXML manipulation: namespace caveat

— namespace caveat

When using Python `zipfile` + `ElementTree` to manipulate OOXML directly,
`ET.register_namespace()` must be called for **every** namespace prefix used
in the document — otherwise `ET.tostring()` strips undeclared prefixes from
the root element, causing OpenXML schema validation errors and potentially
breaking the document in Word.

**Safer alternative:** Prefer `officecli batch` for template population,
text updates, and paragraph additions. `officecli batch` preserves all
namespace declarations automatically and handles the OOXML schema correctly.
Reserve Python zipfile/ElementTree for cases where officecli cannot express
the required edit (e.g., inserting hyperlink relationships in `.rels` files).

```python
# Required namespace registrations for even a simple docx:
ET.register_namespace(
    "w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
)
ET.register_namespace(
    "r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
)
ET.register_namespace("w14", "http://schemas.microsoft.com/office/word/2010/wordml")
ET.register_namespace("w15", "http://schemas.microsoft.com/office/word/2012/wordml")
# ... and potentially 20+ more (wp14, w16, w16se, w16cid, w16sdtdh, etc.)
```

If even one namespace is missing, the document's root element loses those
declarations on serialization and the file fails validation.

- Use `extract_paragraphs()` from `references/operations/raw-xml-manipulation.md`
  — never the naive `<w:p ...>.*?</w:p>` regex (breaks on self-closing `<w:p/>`).
- When extracting `<w:rPr>`, use balanced `<w:rPr>` token matching
  — never `find('<w:rPr', ...)` which also matches `<w:rPrChange>`.
- Validate replacement XML with `validate_para_xml()` before batching.
- Check for `' REF REF_' in pxml` before tag-scanning to avoid
  double-replacement after a paragraph is already fixed.
