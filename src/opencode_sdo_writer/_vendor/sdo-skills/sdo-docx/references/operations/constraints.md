# OfficeCLI Constraints

## 1. Resident mode required

Open the document once with `mise x github:iOfficeAI/OfficeCLI -- officecli open <doc>` before editing, close
with `mise x github:iOfficeAI/OfficeCLI -- officecli close <doc>` afterwards. All intermediate commands run
in-memory. Skipping this causes repeated file I/O and risks partial writes.

## 2. One command at a time

Run one command and check the exit code before proceeding. Never execute a
batch of commands blindly -- if one fails, subsequent commands build on a
broken state.

## 3. `set --prop text=` cannot produce Word tab characters

Text values go into `<w:t>` XML nodes; `\t` in the string is treated as a
space. This affects headings (number/title separated by tab), enumerations
(bullet/text), and notes (NOTE colon/text). Consequence: tabs appear as
spaces, causing wrong indentation, misaligned bullets, and broken note
formatting.

**Workaround -- inject a separate `<w:r><w:tab/></w:r>` run:**

```xml
<!-- Heading 1 with correct tab -->
<w:r><w:t>1</w:t></w:r><w:r><w:tab/></w:r><w:r><w:t>Introduction</w:t></w:r>

<!-- Enumeration with correct tab -->
<w:r><w:t>&#8211;</w:t></w:r><w:r><w:tab/></w:r><w:r><w:t xml:space="preserve">Enumeration text.</w:t></w:r>

<!-- Note with correct tab after colon -->
<w:r><w:t>NOTE&#160;1:</w:t></w:r><w:r><w:tab/></w:r><w:r><w:t xml:space="preserve">Note text.</w:t></w:r>
```

Use the helper scripts in `scripts/` to apply these patterns without
hand-writing XML.

## 7. Tracked changes require correct OOXML marker placement

Inserting tracked changes via raw XML has a critical structural requirement:
revision markers (`<w:ins>`, `<w:del>`) go in different locations depending
on whether you are modifying a paragraph or individual runs.

| Scope | Marker location | Content element |
|-------|----------------|-----------------|
| Entire paragraph inserted | `<w:ins>` inside `<w:pPr>/<w:rPr>` | `<w:t>` |
| Run inserted within paragraph | `<w:ins>` wrapping `<w:r>` as child of `<w:p>` | `<w:t>` |
| Entire paragraph deleted | `<w:del>` inside `<w:pPr>/<w:rPr>` | `<w:delText>` |
| Run deleted within paragraph | `<w:del>` wrapping `<w:r>` as child of `<w:p>` | `<w:delText>` |

**The most common mistake:** wrapping entire paragraph content in `<w:ins>`
as a direct child of `<w:p>`. This produces zero visible tracked changes.
See `references/operations/tracked-changes.md` for complete OOXML patterns.

## 4. High-level commands cannot insert REF/SEQ field codes

Using `set --prop text=` for cross-references produces hardcoded plain text
that breaks when the document is revised. Always inject field codes via
`officecli raw-set`. See `references/operations/field-code-patterns.md` for OOXML
snippets.

## 5. `paraId` targeting requires the `w14:` namespace prefix

XPath like `//w:p[@w:paraId='101C5D24']` matches zero elements because
`paraId` is in the `w14:` namespace, not `w:`. Use `@w14:paraId` instead:

```bash
mise x github:iOfficeAI/OfficeCLI -- officecli raw-set doc.docx /document \
  --xpath '//w:p[@w14:paraId="101C5D24"]' \
  --action replace --xml '<w:p ...>...</w:p>'
```

This works reliably in officecli `raw-set`. The `w14:` prefix is
auto-registered by officecli's XPath engine.

**Style-based positional XPath** is still preferred for multi-step edits
(more readable, survives paragraph reordering):

- `(//w:p[w:pPr/w:pStyle/@w:val='Heading1'])[N]/w:r[1]`
- `(//w:p[w:pPr/w:pStyle/@w:val='enumlev1'])[N]/w:r[1]`
- `//w:p[starts-with(normalize-space(.),'Target text')]/w:r[1]`

## 8. `officecli batch` stdin redirect and command-line length limits

**Problem 1 — stdin conflict:** `mise x github:iOfficeAI/OfficeCLI -- officecli batch <doc> --input -` fails when
stdin is already redirected (e.g., from `subprocess.run(input=...)`). The
CLI detects the conflict and ignores the input:

```text
Warning: batch is reading from --input but stdin is also redirected; stdin ignored.
```

**Solution:** use `--commands` for inline JSON (≤ ~20 KB), or write to a
temp file and use `--input <file>` for large payloads:

```python
import subprocess, json, tempfile, pathlib

from officecli_xml_common import officecli_command


def run_batch(doc, commands, env):
    cmd_json = json.dumps(commands)
    if len(cmd_json) > 20000:  # Windows ~32 KB command-line limit
        tmp = pathlib.Path(tempfile.mktemp(suffix=".json"))
        tmp.write_text(cmd_json, encoding="utf-8")
        args = officecli_command(["batch", doc, "--input", str(tmp), "--json"])
    else:
        tmp = None
        args = officecli_command(["batch", doc, "--commands", cmd_json, "--json"])
    try:
        r = subprocess.run(args, capture_output=True, text=True, env=env)
        return json.loads(r.stdout)
    finally:
        if tmp and tmp.exists():
            tmp.unlink()
```

**Problem 2 — Windows CLI length limit:** `--commands` with large replacement
XML (e.g. full paragraphs) can exceed Windows' ~32 KB `CreateProcess` limit
and raise `FileNotFoundError: [WinError 206] The filename or extension is too long`. The 20 KB threshold above gives safe headroom.

## 9. Self-closing `<w:p/>` paragraphs break naive paragraph extraction

Documents with tracked changes often contain empty self-closing paragraph
marks such as `<w:p w14:paraId="AAA" .../>` (no content, no `</w:p>`).

The standard regex `<w:p [^>]*w14:paraId="([^"]+)"[^>]*>.*?</w:p>` matches
the self-closing tag as the _opener_ and then captures the **entire next
paragraph** as its body — silently duplicating content.

**Safe extraction function:**

```python
def extract_paragraphs(xml):
    """Return [(paraId, full_xml)] handling self-closing <w:p/> correctly."""
    results = []
    for m in re.finditer(r'<w:p [^>]*w14:paraId="([^"]+)"[^>]*>', xml, re.DOTALL):
        pid = m.group(1)
        tag_end = m.end() - 1  # position of final '>'
        if xml[tag_end - 1] == "/":  # self-closing: ends with '/>'
            results.append((pid, xml[m.start() : m.end() - 1] + "/>"))
        else:
            close = xml.find("</w:p>", m.end())
            if close >= 0:
                results.append((pid, xml[m.start() : close + 6]))
    return results
```

Self-closing paragraphs contain no runs, so they are auto-skipped by any
`<w:t>`-based text scan.

An empty XML string replaces the matched element with nothing, permanently
deleting it -- with no undo. This mistake occurred during document
production and required manual restoration of a deleted figure caption
paragraph.

**Safe inspection alternative:** use `mise x github:iOfficeAI/OfficeCLI -- officecli get <doc> "/body/p[N]" --depth 5`
or `mise x github:iOfficeAI/OfficeCLI -- officecli view <doc> annotated`. Never use `raw-set --action replace`
for inspection.

## 6. Heading separator patterns (tab between number and title)

Headings must have exactly one `<w:tab/>` between the heading number and
the title text, with no extra space runs. Two common defects require
correction:

**Pattern A — `<w:tab/>` followed by a space-only run (remove it):**

```xml
<!-- BROKEN: space run after tab -->
<w:r><w:tab/></w:r>
<w:r w:rsidRPr="006E4971"><w:t xml:space="preserve"> </w:t></w:r>  <!-- REMOVE THIS -->
<w:r><w:t>Loudness Rating</w:t></w:r>
```

Fix: locate and delete the space-only run that immediately follows the
`<w:tab/>` run. Detect with:
`<w:tab\s*/>\s*</w:r>\s*(<w:r(?:\s[^>]*)?>\s*(?:<w:rPr>.*?</w:rPr>)?\s*<w:t\s+xml:space="preserve">\s+</w:t>\s*</w:r>)`

Also check for trailing space in the numbering text itself (e.g.
`<w:t xml:space="preserve">11.2 </w:t>` where "11.2 " should be "11.2").

**Pattern B — Missing `<w:tab/>` (insert it):**

```xml
<!-- BROKEN: title text directly follows numbering run -->
<w:r w:rsidRPr="00E44759"><w:t>Test method</w:t></w:r>

<!-- FIXED: <w:tab/> inserted before <w:t> -->
<w:r w:rsidRPr="00E44759"><w:tab/><w:t>Test method</w:t></w:r>
```

Find the first non-numeric/not-dot `<w:t>` after the numbering runs and
insert `<w:tab/>` before its text content. For paragraphs entirely within
`<w:ins>` blocks (all content tracked as insertion), the replacement stays
within the existing revision context — no new `<w:del>`/`<w:ins>` needed.

## 10. `raw-set` replaces only the single matched element

When the XPath `//w:p[@w14:paraId="X"]` matches a self-closing
`<w:p .../>`, `raw-set` replaces **only that one element**. If the
replacement XML string accidentally contains two `<w:p>` elements (e.g.
because a naive extractor bundled a self-closing `<w:p/>` with the following
real paragraph), `raw-set` inserts both — duplicating the following paragraph
and introducing duplicate `w:id` values on all its `<w:ins>` / `<w:del>`
elements.

Always validate that the replacement XML contains **exactly one** top-level
element matching the XPath target before executing `raw-set`.
