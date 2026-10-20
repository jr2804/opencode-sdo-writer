# Raw XML Manipulation Patterns for OOXML

Python string-based helpers for scanning, extracting and replacing content
in OOXML document XML. Use these patterns instead of ElementTree, which
rewrites namespace prefixes (`w:` → `ns0:`, `w14:` → `ns1:`, etc.) and
corrupts the output.

______________________________________________________________________

## 1. Paragraph extraction (handles self-closing `<w:p/>`)

Documents with tracked changes contain empty self-closing paragraphs
`<w:p w14:paraId="AAA" .../>`. The standard non-greedy regex incorrectly
captures them as openers and grabs the next paragraph's content as their
body — silently duplicating paragraphs and injecting duplicate `w:id` values.

```python
def extract_paragraphs(xml: str) -> list[tuple[str, str]]:
    """Return [(paraId, full_para_xml), ...] for all <w:p> elements."""
    results = []
    for m in re.finditer(r'<w:p [^>]*w14:paraId="([^"]+)"[^>]*>', xml, re.DOTALL):
        pid = m.group(1)
        tag_end = m.end() - 1  # index of the closing '>'
        if xml[tag_end - 1] == "/":  # self-closing: ends with '/>'
            results.append((pid, xml[m.start() : m.end() - 1] + "/>"))
        else:
            close = xml.find("</w:p>", m.end())
            if close >= 0:
                results.append((pid, xml[m.start() : close + 6]))
    return results
```

Self-closing paragraphs have no `<w:t>` content and are auto-skipped by
any text scanner.

______________________________________________________________________

## 2. Run scanner with del/ins depth tracking

Iterates all `<w:r>` elements in a paragraph XML string, tracking nesting
depth of `<w:ins>` and `<w:del>` elements so you know whether a run is
live text or deleted text.

```python
import re
from dataclasses import dataclass


@dataclass
class Run:
    start: int  # byte offset of <w:r> in para XML
    end: int  # byte offset of </w:r> end
    xml: str  # full run XML
    text: str  # content of <w:t>...</w:t> (raw, XML-escaped)
    is_del: bool  # True if inside <w:del>
    pre_text_xml: str  # elements between </w:rPr> and <w:t> (e.g. '<w:tab/>')


def scan_runs(para: str) -> list[Run]:
    runs: list[Run] = []
    del_depth = 0
    pos = 0
    while True:
        cands = []
        for tag, kind in [
            ("<w:ins ", "io"),
            ("</w:ins>", "ic"),
            ("<w:del ", "do"),
            ("</w:del>", "dc"),
            ("<w:r", "run"),
        ]:
            p = para.find(tag, pos)
            if p >= 0:
                cands.append((p, kind, tag))
        if not cands:
            break
        cands.sort()
        p, kind, tag = cands[0]

        if kind == "io":
            pos = para.find(">", p) + 1
        elif kind == "ic":
            pos = p + len(tag)
        elif kind == "do":
            del_depth += 1
            pos = para.find(">", p) + 1
        elif kind == "dc":
            del_depth -= 1
            pos = p + len(tag)
        elif kind == "run":
            gt = para.find(">", p)
            if gt < 0:
                break
            if para[gt - 1] == "/":  # self-closing <w:r/>
                pos = gt + 1
                continue
            nc = para.find("</w:r>", gt + 1)
            if nc < 0:
                break
            r_end = nc + 6
            run_xml = para[p:r_end]
            tm = re.search(r"<w:t[^>]*>([^<]*)</w:t>", run_xml)
            if tm:
                # Find outer </w:rPr> using balanced <w:rPr> counting
                # IMPORTANT: use '<w:rPr>' exact string, NOT '<w:rPr' prefix
                # which also matches '<w:rPrChange>' and breaks the balance count.
                rpr_s = run_xml.find("<w:rPr>")
                content_start = run_xml.find(">") + 1  # fallback
                if rpr_s >= 0:
                    depth2 = 0
                    for mo2 in re.finditer(r"<w:rPr>|</w:rPr>", run_xml[rpr_s:]):
                        if mo2.group(0) == "<w:rPr>":
                            depth2 += 1
                        else:
                            depth2 -= 1
                            if depth2 == 0:
                                content_start = rpr_s + mo2.end()
                                break
                t_start = run_xml.find("<w:t", content_start)
                pre = (
                    run_xml[content_start:t_start].strip()
                    if t_start > content_start
                    else ""
                )
                runs.append(Run(p, r_end, run_xml, tm.group(1), del_depth > 0, pre))
            pos = r_end
    return runs
```

**Critical pitfall — `<w:rPr>` vs `<w:rPrChange>`:**
`find('<w:rPr', ...)` matches both `<w:rPr>` and `<w:rPrChange ...>` because
they share the prefix. Always use `finditer(r'<w:rPr>|</w:rPr>', ...)` for
balanced traversal so that `<w:rPrChange>` openings are not miscounted as
`<w:rPr>` openings.

______________________________________________________________________

## 3. Extracting and cleaning `<w:rPr>` from a run

When copying a run's character properties to new replacement runs, the
`<w:rPrChange>` sub-element (which records what the formatting used to be)
must be stripped — keeping it creates nesting mismatches. Self-closing
`<w:ins/>` inside `<w:rPr>` (character-format insertion markers) should
also be stripped since their `w:id` would otherwise be duplicated across
multiple new runs.

```python
def clean_rpr(run_xml: str) -> str:
    """
    Extract the outer <w:rPr>...</w:rPr>, stripping <w:rPrChange> and
    self-closing <w:ins/> elements.
    Returns empty string if no <w:rPr> found.
    """
    start = run_xml.find("<w:rPr>")
    if start < 0:
        return ""

    # Balanced traversal using EXACT '<w:rPr>' token.
    # DO NOT use '<w:rPr' — that also matches '<w:rPrChange>'.
    depth = 0
    end = -1
    for mo in re.finditer(r"<w:rPr>|</w:rPr>", run_xml[start:]):
        if mo.group(0) == "<w:rPr>":
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = start + mo.end()
                break
    if end < 0:
        return ""
    rpr = run_xml[start:end]

    # Strip <w:rPrChange>...</w:rPrChange> (may contain nested <w:rPr>)
    while "<w:rPrChange" in rpr:
        cs = rpr.find("<w:rPrChange")
        gt = rpr.find(">", cs)
        if gt >= 0 and rpr[gt - 1] == "/":  # self-closing
            rpr = rpr[:cs] + rpr[gt + 1 :]
            continue
        d = 0
        p = cs
        ce = -1
        while p < len(rpr):
            oc = rpr.find("<w:rPrChange", p)
            cc = rpr.find("</w:rPrChange>", p)
            if cc < 0:
                break
            if oc >= 0 and oc < cc:
                g = rpr.find(">", oc)
                if g >= 0 and rpr[g - 1] != "/":
                    d += 1
                p = (g + 1) if g >= 0 else oc + 12
            else:
                d -= 1
                if d == 0:
                    ce = cc + 14
                    break
                p = cc + 14
        if ce < 0:
            break
        rpr = rpr[:cs] + rpr[ce:]

    # Strip self-closing <w:ins/> (char-format insertion markers)
    rpr = re.sub(r"<w:ins[^>]*/>", "", rpr)
    return rpr
```

______________________________________________________________________

## 4. Span replacement strategy

### Split-character anti-pattern

Tracked changes by certain authors systematically split words into
individual character runs, each in its own `<w:r>` (often within separate
`<w:ins>` blocks). Example: "chapter" becomes `<w:t>c</w:t>` in one ins
and `<w:t xml:space="preserve">hapter </w:t>` in the next ins.

**Detection:** regex `<w:t[^>]*>([^<]*chapter[^<]*)</w:t>` will NOT match
because "chapter" never appears in a single `<w:t>`. Instead, test the
concatenated text:

```python
contiguous = bool(re.search(r'<w:t[^>]*>([^<]*chapter[^<]*)</w:t>', pxml))
if not contiguous and 'chapter' in ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', pxml)):
    # word is split — fix both runs individually
```

**Fix approach:** find both contributing runs and modify their `<w:t>`
content individually. Example for "chapter" → "clause":

```python
# Replace the single-char "c" run
old_c = "<w:t>c</w:t>"
new_c = "<w:t>cl</w:t>"
# Replace the "hapter " run (may have xml:space attr)
p2 = p2.replace(
    '<w:t xml:space="preserve">hapter ', '<w:t xml:space="preserve">ause ', 1
)
```

If both runs are in separate `<w:ins>` blocks, the replacement still works
because each run is modified in-place — the `<w:ins>` wrappers stay intact.

### Multi-run span replacement (standard pattern)

To replace a `[TAG]` pattern that may span multiple runs (possibly split
across separate `<w:ins>` elements):

1. Build a concatenated string from all non-deleted runs' `text` fields.
2. Find the match positions; map them back to run indices via `cmap`.
3. Replace from `fr.start` (first run's start offset) to `lr.end` (last
   run's end offset) with the new XML content.

**Surrounding `<w:ins>` context is inherited automatically.** The text
before `fr.start` contains the opening `<w:ins>` tag; the text after
`lr.end` contains the eventual `</w:ins>` close. New runs placed between
them are implicitly inside that `<w:ins>` — no new wrapper needed.

```python
def process_para(para: str, tag_re, tag_to_bm) -> tuple[str, int]:
    runs = scan_runs(para)
    nd = [r for r in runs if not r.is_del]
    concat = "".join(r.text for r in nd)
    matches = list(tag_re.finditer(concat))
    if not matches:
        return para, 0

    # Map character index in concat → run index in nd
    cmap: list[int] = []
    for ri, r in enumerate(nd):
        cmap.extend([ri] * len(r.text))

    total = 0
    mod = para

    for m in reversed(matches):  # reverse so earlier offsets stay valid
        tag = m.group(1)
        bm = tag_to_bm[tag]
        cs, ce = m.start(), m.end()
        if cs >= len(cmap) or ce - 1 >= len(cmap):
            continue

        ri_s = cmap[cs]
        ri_e = cmap[ce - 1]
        fr = nd[ri_s]
        lr = nd[ri_e]

        if any(nd[ri].is_del for ri in set(cmap[cs:ce])):
            continue  # skip matches inside deleted text

        chars_before_s = sum(len(nd[i].text) for i in range(ri_s))
        before = fr.text[: cs - chars_before_s]  # text in fr before '['

        chars_before_e = sum(len(nd[i].text) for i in range(ri_e))
        after = lr.text[ce - chars_before_e :]  # text in lr after ']'

        rpr = clean_rpr(fr.xml)
        pre = fr.pre_text_xml  # e.g. '<w:tab/>' if run has a tab before <w:t>

        new = (
            make_text_run(pre, before + "[", rpr)
            + ref_field_xml(bm, tag, rpr)
            + make_text_run("", "]" + after, rpr)
        )
        mod = mod[: fr.start] + new + mod[lr.end :]
        total += 1

    return mod, total
```

**Why reverse order?** Each replacement shifts offsets for everything
before it. Processing matches from last to first means earlier offsets
(used in later loop iterations) are always still valid in `mod`.

______________________________________________________________________

## 5. OOXML validation checks

After generating replacement XML, run these sanity checks before submitting
to `officecli raw-set`:

```python
import xml.etree.ElementTree as ET, re


def validate_para_xml(pxml: str, ns_decl: str) -> list[str]:
    """Return list of issue descriptions, empty = clean."""
    issues = []

    # 1. Valid XML (inject namespace declarations for parse)
    def inject_ns(x):
        gt = x.find(">")
        return x[:gt] + " " + ns_decl + x[gt:]

    try:
        ET.fromstring(inject_ns(pxml).encode())
    except ET.ParseError as e:
        issues.append(f"XML invalid: {e}")

    # 2. Field characters balanced
    b = pxml.count('fldCharType="begin"')
    s = pxml.count('fldCharType="separate"')
    e = pxml.count('fldCharType="end"')
    if not (b == s == e):
        issues.append(f"fldChar unbalanced: begin={b} sep={s} end={e}")

    # 3. Non-self-closing <w:ins> balanced
    opens = len(re.findall(r"<w:ins [^>]*[^/]>", pxml))
    closes = pxml.count("</w:ins>")
    if opens != closes:
        issues.append(f"w:ins unbalanced: open={opens} close={closes}")

    # 4. <w:rPrChange> balanced (open != close → clean_rpr failure)
    rc_o = len(re.findall(r"<w:rPrChange[^>]*[^/]>", pxml))
    rc_c = pxml.count("</w:rPrChange>")
    if rc_o != rc_c:
        issues.append(f"w:rPrChange unbalanced: open={rc_o} close={rc_c}")

    # 5. No double brackets (indicates accidental bracket duplication)
    t = "".join(re.findall(r"<w:t[^>]*>([^<]+)</w:t>", pxml))
    if "[[" in t or "]]" in t:
        issues.append("Double brackets in text")

    return issues
```

**Run this on every paragraph before submitting the batch.** It catches
all the failure modes observed during ITU-T P.340 production.

______________________________________________________________________

## 6. Whole-document OOXML health check

```python
import zipfile, re
from collections import Counter


def check_document(docx_path: str) -> dict:
    with zipfile.ZipFile(docx_path) as z:
        data = z.read("word/document.xml").decode("utf-8")

    # Field balance
    b = data.count('fldCharType="begin"')
    s = data.count('fldCharType="separate"')
    e = data.count('fldCharType="end"')

    # Duplicate w:ins IDs (structural, non-self-closing)
    ins_ids = [m.group(1) for m in re.finditer(r'<w:ins [^>]* w:id="(\d+)"[^/]', data)]
    dup_ins = {k: v for k, v in Counter(ins_ids).items() if v > 1}

    # rPrChange balance per paragraph
    rpr_issues = []
    for m in re.finditer(
        r'<w:p [^>]*w14:paraId="([^"]+)"[^>]*>.*?</w:p>', data, re.DOTALL
    ):
        pid = m.group(1)
        pxml = m.group(0)
        opens = len(re.findall(r"<w:rPrChange[^>]*[^/]>", pxml))
        closes = pxml.count("</w:rPrChange>")
        if opens != closes:
            rpr_issues.append(f"{pid}: open={opens} close={closes}")

    return {
        "fldChar_balanced": b == s == e,
        "fldChar": (b, s, e),
        "dup_ins_ids": dup_ins,
        "rPrChange_unbalanced": rpr_issues,
    }
```

A clean document shows:

- `fldChar_balanced: True`
- `dup_ins_ids: {}` (empty — no structural duplicates)
- `rPrChange_unbalanced: []`

Note: `w:bookmarkStart`/`w:bookmarkEnd` and `w:commentRangeStart`/
`w:commentRangeEnd`/`w:commentReference` legitimately share the same `w:id`
by design — do **not** count these as duplicates.
