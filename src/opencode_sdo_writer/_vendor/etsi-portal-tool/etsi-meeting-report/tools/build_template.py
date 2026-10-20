"""Build the agenda BODY template (sections 1.2 to 4.4) from the styles of a committee document.

    uv run python build_template.py --styles-from <any agenda or report of the committee>.docx \
        tools/templates/agenda-body.docx

The styles (Heading 1-3, TH, TAH, TAC, EX, Header, Normal, ...) come from the given document, so the
template matches the committee's own look. The body text is generic ETSI agenda text with tags only:
no committee, person, organisation, venue or date is written into the template. The meeting's own
document provides the head (cover, schedule, IPR and Code of Conduct boilerplate); see render.py.

Tags are filled from docs/<tc><nn>/meeting.toml through model.build_context().
"""
from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

EX_VALUE_TAB = Cm(3.0)  # EX key lines: values start after the key at this tab stop


def style_obj(doc, name: str):
    for s in doc.styles:
        if s.name.lower() == name.lower():
            return s
    raise SystemExit(f"style {name!r} is missing in the styles source; use a committee report or agenda that has it")


def clear_body(doc) -> None:
    body = doc.element.body
    sect = body.find(qn("w:sectPr"))
    for el in list(body):
        if el is not sect:
            body.remove(el)


def para(doc, text: str = "", style: str = "Normal", bold: bool = False, italic: bool = False):
    p = doc.add_paragraph()
    p.style = style_obj(doc, style)
    if text:
        run = p.add_run(text)  # python-docx turns \t into a real tab element
        if bold:
            run.bold = True
        if italic:
            run.italic = True
    return p


def header_line(doc, text: str):
    """TDoc title line: UID, tab, title. Header style; tab stop aligned with the EX values."""
    p = para(doc, text, style="Header")
    p.paragraph_format.tab_stops.add_tab_stop(EX_VALUE_TAB)
    p.paragraph_format.space_before = Pt(10)
    return p


def table(doc, rows: list[list[str]], header_style: str, body_style: str,
          body_align=WD_ALIGN_PARAGRAPH.CENTER):
    """A table with AutoFit to Contents, centred. Borders come from the styles source if it has a table."""
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    existing = [tb for tb in doc.tables]
    if existing:
        src = existing[0]._tbl.tblPr
        t._tbl.remove(t._tbl.tblPr)
        t._tbl.insert(0, deepcopy(src))
    tblPr = t._tbl.tblPr
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is not None:
        tblW.set(qn("w:w"), "0")
        tblW.set(qn("w:type"), "auto")
    layout = tblPr.find(qn("w:tblLayout"))
    if layout is not None:
        layout.set(qn("w:type"), "autofit")
    for gc in t._tbl.tblGrid.findall(qn("w:gridCol")):
        gc.attrib.pop(qn("w:w"), None)
    for tcW in t._tbl.iter(qn("w:tcW")):
        tcW.set(qn("w:w"), "0")
        tcW.set(qn("w:type"), "auto")
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r, values in enumerate(rows):
        for c, value in enumerate(values):
            cell = t.rows[r].cells[c]
            cell.text = value
            cell.paragraphs[0].style = style_obj(doc, header_style if r == 0 else body_style)
            if r > 0:
                cell.paragraphs[0].alignment = body_align
    return t


def tdoc_block(doc, var: str, loop: str):
    """One loop over documents: title line, then Source, Presenter, Summary, Outcome in EX."""
    para(doc, f"{{%p for {var} in {loop} %}}")
    header_line(doc, f"{{{{ {var}.uid }}}}\t{{{{ {var}.title }}}}")
    para(doc, f"Source:\t{{{{ {var}.source }}}}", style="EX")
    para(doc, f"Presenter:\t{{{{ {var}.presenter }}}}", style="EX")
    para(doc, f"Summary:\t{{{{ {var}.summary }}}}", style="EX")
    para(doc, f"Outcome:\t{{{{ {var}.outcome }}}}", style="EX")
    para(doc, "{%p endfor %}")


def build_body(doc) -> None:
    # 1.2 approval of the agenda
    para(doc, "Approval of agenda", style="Heading 2")
    para(doc, "{{ agenda.line }}")
    para(doc, "{{ agenda.decision }}", italic=True)
    # 1.3 work programme status
    para(doc, "Work Programme status", style="Heading 2")
    para(doc, "The Technical Officer regularly looks after this agenda item throughout the meeting. "
              "The status of the open work items is in section 3.")
    # 1.4 liaison statements IN (blocks) and OUT
    para(doc, "Liaison Statements IN/OUT", style="Heading 2")
    para(doc, "LS IN:", bold=True)
    tdoc_block(doc, "d", "ls.docs")
    para(doc, "{{ ls.out }}", italic=True)
    # 1.5 ETSI matters
    para(doc, "Report from ETSI Board, General Assembly and any other ETSI matters", style="Heading 2")
    para(doc, "{{ board.heading }}", style="Heading 3")
    para(doc, "[Report by the Technical Officer]", italic=True)
    para(doc, "GA", style="Heading 3")
    para(doc, "[Report by the Technical Officer]", italic=True)
    # 1.6 sub-committee report (if the meeting has one)
    para(doc, "{{ sub_tc.heading }}", style="Heading 2")
    para(doc, "{{ sub_tc.report_heading }}", style="Heading 3")
    para(doc, "{{ sub_tc.report_line }}")
    para(doc, "{{ sub_tc.wi_heading }}", style="Heading 3")
    para(doc, "{{ sub_tc.wi_placeholder }}", italic=True)
    # 1.7 onwards: the meeting's own administrative items (officials, elections, special items)
    para(doc, "{%p for item in admin_items %}")
    para(doc, "{{ item.heading }}", style="Heading 2")
    para(doc, "{%p for line in item.paragraphs %}")
    para(doc, "{{ line }}")
    para(doc, "{%p endfor %}")
    para(doc, "{%p endfor %}")
    # section 2: contributions grouped by topic
    para(doc, "Meeting Contributions", style="Heading 1")
    para(doc, "{%p for topic in topics %}")
    para(doc, "{{ topic.title }}", style="Heading 2")
    tdoc_block(doc, "d", "topic.docs")
    para(doc, "{%p endfor %}")
    # section 3: open work items
    para(doc, "Open Work Items' status", style="Heading 1")
    para(doc, "This agenda item is to ensure that the {{ meeting.tc }} group keeps track of ongoing work, "
              "and work which needs to progress or to be stopped.")
    para(doc, 'NB: Clause 1.6.5, Stopping an ETSI Work Item, of the ETSI Directives, established by the ETSI '
              'Membership, indicates that "Any ETSI Work Item shall automatically be stopped, if no progress has '
              'been achieved in a period of one (1) year". The ETSI Secretariat is requested to strictly enforce '
              'this rule. Said that, once a WI is stopped, a new one can be opened on the same or similar subject '
              'matter, when time and situation is more appropriate to ensure good progress.')
    para(doc, "NB: For Reference to check a document progress (and any published ETSI standards): go to the ETSI "
              "work programme search, type the ETSI number e.g. 123 567, search, click Details and Download, click "
              "below Current Status (Click to View Full Schedule). This is globally visible by everybody, not by "
              "ETSI Members only.")
    para(doc, "Key status codes", style="TH")
    table(doc, [["Code", "Meaning"], ["0a", "Work item adopted"], ["1", "Start of work"], ["2", "Early draft"],
                ["4", "Stable draft"], ["6", "Final draft for approval"], ["8", "TB approval"],
                ["12", "Published"]], "TAH", "TAC")
    para(doc, "Open work items (portal work programme, committee {{ meeting.tc }})", style="TH")
    wi = table(doc, [["ETSI and WI Numbers", "Title", "Rapporteur", "Last Draft and Status",
                      "Next Step", "Notes on Status"],
                     ["{%tr for w in wi %}", "", "", "", "", ""],
                     ["{{ w.number }}", "{{ w.title }}", "{{ w.rapporteur }}", "{{ w.last_draft }}",
                      "{{ w.next }}", "{{ w.note }}"],
                     ["{%tr endfor %}", "", "", "", "", ""]], "TAH", "TAC", body_align=WD_ALIGN_PARAGRAPH.LEFT)
    wi.rows[0].cells[0].paragraphs[0].alignment = None
    # section 4: wrap-up and closure
    para(doc, "Wrap-up and closure", style="Heading 1")
    para(doc, "Approvals", style="Heading 2")
    for label, tag in [("Final drafts", "{{ wrapup.final_drafts }}"), ("LSs OUT", "{{ wrapup.lss_out }}"),
                       ("STF/TTF Reports", "{{ wrapup.stf }}"), ("New WIs", "{{ wrapup.new_wis }}"),
                       ("Stopped WIs", "{{ wrapup.stopped }}")]:
        para(doc, label, bold=True)
        para(doc, tag, italic=True)
    para(doc, "Future Meetings / Events", style="Heading 2")
    para(doc, "{%p for f in wrapup.future %}")
    para(doc, "{{ f.name }}\t{{ f.text }}")
    para(doc, "{%p endfor %}")
    para(doc, "Any Other Business", style="Heading 2")
    para(doc, "{{ wrapup.aob }}", italic=True)
    para(doc, "Closure", style="Heading 2")
    para(doc, "{{ wrapup.closure }}", italic=True)
    # Annex A: the participant list (only when meeting.toml has an [annex] section)
    para(doc, "{%p if annex %}")
    annex_head = para(doc, "{{ annex.heading }}", style="Heading 1")
    annex_head.paragraph_format.page_break_before = True
    para(doc, "{{ annex.caption }}", style="TH")
    table(doc, [["First name", "Last name", "Organisation", "Role", "Presence", "Registration date (UTC)"],
                ["{%tr for r in annex.rows %}", "", "", "", "", ""],
                ["{{ r.first }}", "{{ r.last }}", "{{ r.org }}", "{{ r.role }}", "{{ r.presence }}", "{{ r.date }}"],
                ["{%tr endfor %}", "", "", "", "", ""]], "TAH", "TAC", body_align=WD_ALIGN_PARAGRAPH.LEFT)
    para(doc, "{%p endif %}")


def main(argv: list[str]) -> int:
    if len(argv) != 4 or argv[1] != "--styles-from":
        print(__doc__)
        return 2
    styles_src, out = Path(argv[2]), Path(argv[3])
    doc = Document(styles_src)
    clear_body(doc)
    build_body(doc)
    cp = doc.core_properties  # no author, title or dates from the styles source leak into the template
    for attr in ("author", "last_modified_by", "title", "subject", "keywords", "comments", "category"):
        setattr(cp, attr, "")
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out)
    _scrub_package(out)
    print(f"body template written: {out} (styles from {styles_src.name})")
    return 0


def _scrub_package(path: Path) -> None:
    """Drop document-specific text the styles source carries: header and footer text, application
    properties (titles, company) and relationships to committee-specific targets."""
    import re
    import zipfile
    minimal_app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                   '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
                   '<Application>Microsoft Office Word</Application></Properties>')
    tmp = path.with_suffix(".scrub.tmp")
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            name = item.filename
            if name == "docProps/app.xml":
                data = minimal_app.encode("utf-8")
            elif re.match(r"word/(header|footer)\d*\.xml$", name):
                text = data.decode("utf-8")
                text = re.sub(r"(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)",
                              lambda m: m.group(1) + ("" if re.search(r"\(\d\d\)\d{6}", m.group(2)) else m.group(2)) + m.group(3),
                              text)
                data = text.encode("utf-8")
            elif name == "word/_rels/document.xml.rels":
                text = data.decode("utf-8")
                text = re.sub(r'<Relationship [^>]*Target="[^"]*\(\d\d\)[^"]*"[^>]*/>', "", text)
                data = text.encode("utf-8")
            zout.writestr(item, data)
    tmp.replace(path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
