"""Spike: can docxtpl render Jinja2 tags that Word has split across runs?

Checks (each prints PASS/FAIL):
  1. a {{ tag }} split over three runs with different formatting
  2. a paragraph loop {%p for %} with a named paragraph style
  3. a table-row loop {%tr for %} whose rows keep the cell paragraph style
  4. a hyperlink created inside the loop (RichText + build_url_id)
  5. an optional block {%p if %} that is dropped when false
"""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docxtpl import DocxTemplate, RichText

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "spike-out")
OUT.mkdir(parents=True, exist_ok=True)
TEMPLATE = OUT / "spike-template.docx"
RENDERED = OUT / "spike-rendered.docx"


def make_template(path: Path) -> None:
    doc = Document()
    # 1. tag split across three runs, the middle one bold
    p = doc.add_paragraph()
    p.add_run("Source: {{ ")
    r = p.add_run("item.source")
    r.bold = True
    p.add_run(" }} (split)")
    # 5. optional block
    doc.add_paragraph("{%p if show_note %}")
    doc.add_paragraph("Optional note is shown.")
    doc.add_paragraph("{%p endif %}")
    # 2. paragraph loop with a named style (Heading 2 exists in the default template)
    doc.add_paragraph("{%p for item in items %}")
    doc.add_paragraph("{{ item.uid }}\t{{ item.title }}", style="Heading 2")
    doc.add_paragraph("Source: {{ item.source }}")
    doc.add_paragraph("{%p endfor %}")
    # 3. table-row loop: tag rows are removed, the middle row repeats
    table = doc.add_table(rows=4, cols=2)
    table.style = doc.styles["Table Grid"]
    hdr = table.rows[0].cells
    hdr[0].text = "UID"
    hdr[1].text = "Title"
    loop_open = table.rows[1].cells
    loop_open[0].text = "{%tr for w in wis %}"
    loop_open[1].text = ""
    body = table.rows[2].cells
    body[0].text = "{{ w.uid }}"
    body[1].text = "{{ w.title }}"
    body[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    loop_close = table.rows[3].cells
    loop_close[0].text = "{%tr endfor %}"
    loop_close[1].text = ""
    # 4. placeholder paragraph for a hyperlink
    doc.add_paragraph("Link: {{ link }}")
    doc.save(path)


def check(label: str, ok: bool) -> bool:
    print(("PASS " if ok else "FAIL ") + label)
    return ok


def main() -> int:
    make_template(TEMPLATE)
    tpl = DocxTemplate(TEMPLATE)
    rt = RichText()
    url = "https://portal.etsi.org/ngppapp/ContributionCreation.aspx?primarykeys=<portal-id>"
    rt.add("#009", url_id=tpl.build_url_id(url))
    context = {
        "item": {"source": "Example Systems GmbH"},
        "show_note": False,
        "items": [
            {"uid": "<UID>", "title": "Draft deliverable B", "source": "Example Systems GmbH"},
            {"uid": "<UID>", "title": "Suggested improvements", "source": "Sample Telecom"},
        ],
        "wis": [
            {"uid": "WI-A", "title": "Unified test methods"},
            {"uid": "WI-B", "title": "M-Measure framework"},
        ],
        "link": rt,
    }
    tpl.render(context)
    tpl.save(RENDERED)

    out = Document(RENDERED)
    texts = [p.text for p in out.paragraphs]
    ok = True
    ok &= check("1 split tag rendered", "Source: Example Systems GmbH (split)" in texts)
    ok &= check("5 optional block dropped", "Optional note is shown." not in texts)
    ok &= check("2 paragraph loop: two Heading 2 lines",
                sum(1 for p in out.paragraphs if p.style.name == "Heading 2") == 2)
    ok &= check("2 loop body keeps style and tab",
                any(p.text == "<UID>\tSuggested improvements" and p.style.name == "Heading 2"
                    for p in out.paragraphs))
    ok &= check("3 table rows repeated, tag rows removed",
                len(out.tables[0].rows) == 3 and out.tables[0].rows[1].cells[0].text == "WI-A")
    ok &= check("3 centred cell paragraph kept in loop row",
                out.tables[0].rows[2].cells[1].paragraphs[0].alignment == WD_ALIGN_PARAGRAPH.CENTER)
    body_xml = out.element.body.xml
    hyperlinks = out.element.body.findall(".//" + qn("w:hyperlink"))
    link_texts = ["".join(t.text or "" for t in h.iter(qn("w:t"))) for h in hyperlinks]
    ok &= check("4 hyperlink element with the link text inside it", "#009" in link_texts)
    ok &= check("4 hyperlink target present",
                url in [rel.target_ref for rel in out.part.rels.values() if "hyperlink" in rel.reltype])
    print("\nlink texts found inside w:hyperlink:", link_texts)
    print("\nparagraphs:")
    for p in out.paragraphs:
        print(f"  [{p.style.name}] {p.text!r}")
    print("\nresult:", "ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
