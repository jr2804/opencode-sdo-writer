# Python pipeline for the agenda body and the lead document

Scope: the agenda body (sections 1.2 to 4.4) and the lead document. The schedule grid is
still built by PowerShell (`scripts/build-schedule.ps1`, officecli) until it is ported to
python-docx.

## Layout

The pipeline is part of the skill folder (`.agents/skills/etsi-meeting-report/tools/`),
which is not committed in the Meeting repository.

```text
tools/
  pyproject.toml          uv project: docxtpl, python-docx, jinja2
  build_template.py       builds templates/agenda-body.docx from the styles of one of the committee's own documents (once per committee; re-run when the body text changes)
  meeting_report/
    cli.py                commands: roundtrip, render, crawl, lead
    model.py              chair data + portal rows -> render context; work-item normalisation
    render.py             docxtpl render; body comparison (roundtrip)
    lead.py               Jinja2 lead document; refuses to overwrite an existing file
  templates/
    agenda-body.docx       tagged agenda body, generic ETSI text only; no committee, person or date is in it
    lead.md.j2            lead document template (new meetings)
  spike/spike_docxtpl.py  the docxtpl spike (kept as a reference test)
  var/                    git-ignored: crawled output, scratch renders, round-trip files
```

## Chair data (committed with the meeting)

`docs/<tc><nn>/meeting.toml`: meeting IDs and profile, placeholders, agenda, LS OUT, officials and
custom item text, the LS IN documents (`[[ls.docs]]`, section 1.4), the topics with their documents
(UID, title, chair summary; section 2), work-item title and note overrides, wrap-up text and future
meetings. The file contains no crawled data.

## Commands (run from `tools/`)

```powershell
uv sync
uv run python -m meeting_report crawl --meeting <meeting.toml>                      # raw + normalised -> var/
uv run python -m meeting_report roundtrip --meeting <meeting.toml> --reference <report.docx>
uv run python -m meeting_report render --meeting <meeting.toml> --base <agenda.docx> --out <scratch.docx>
uv run python -m meeting_report lead --meeting <meeting.toml> --out <file.md>      # refuses if the file exists
uv run python -m meeting_report participants --tc <TC> --tc <sub-TC code> --meeting <TC>#<nn> --meeting <sub-TC>#<nn> --out <file.xlsx>
```

### Participant list (any meetings, any committees)

`participants` is not tied to one meeting. It takes any number of committees (`--tc`,
short code or TBID, repeatable) and any number of meetings (`--meeting`, UID such as
`<TC>#<nn>` or a portal ID, repeatable), and writes one workbook with one sheet. Each row is one person
(portal `PersonId`), with a Meeting column that lists the meetings the person joins, separated by ", "
(e.g. `<TC>#<nn>, <sub-TC>#<nn>`). Columns: Meeting, First name, Last name, Organisation, Role, Presence
(`face to face` / `online`, from the portal's PresenceType), Registration date (UTC). If a person's
presence differs between the meetings, the cell lists it per meeting. Titles (Dr, Mr, Ms) are left
out. Rows: face to face first, then by registration date (earliest across meetings). No summary,
no portal IDs in the workbook.

A UID must match exactly one meeting in the given committees. Past meetings (for example <TC>#<nn>,
which is not in the default list) need `--since YYYY-MM-DD` on the command line; without it the portal
lists upcoming meetings only. An unknown or ambiguous UID
exits with code 2 and names the available meetings; a meeting of another committee (<TC>
MOBILE is `<sub-TC code>`) needs its `--tc`. Raw rosters go to `tools/var/participants/` (git-ignored).
The workbook is personal data: keep it outside git (`**/participants*.xlsx` is ignored).

`--workitems <file>` reads the work-item table from a saved `workitems list` output instead of
calling the portal (useful for a repeatable round trip).

## Rules

- **The live report and the lead document are not regenerated.** Render to a scratch file,
  compare, and then patch the live file deliberately.
- **Round trip before patch.** `roundtrip` compares the body from "Approval of agenda" to the
  end (paragraph style and text, table cells). Every difference is listed and explained before
  anything is changed.
- **Portal data is read at run time.** Work items come from `workitems list`; document titles
  for checks come from the cache manifest. Raw output stays in `tools/var/`.
- **Tabs:** the template holds real tab elements (python-docx writes them). docxtpl inserts
  tag values as plain text, so tabs belong in the template, not in the values.
- **Source:** the official portal source per TDoc, from `documents list --json`. The chair's
  source text is only a fallback; every difference is reported (issues file, C8).
- **Styles:** body text in Normal (no direct font); TDoc title lines in Header; the key lines
  Source, Presenter, Summary and Outcome in EX, each with a tab after the key.
- **Work-item titles:** the portal list truncates long titles. Full titles come from the
  work-item page; until `--json` is released, use `[wi_titles]` in `meeting.toml`.

## docxtpl spike (docxtpl 0.20.2, python-docx 1.2.0)

Passed (`spike/spike_docxtpl.py`):

- a tag split over three runs with different formatting;
- paragraph loops `{%p for %}` with a paragraph style, and nested loops (topics, documents);
- table-row loops `{%tr for %}` where the tag rows are removed and cell paragraph styles stay;
- optional blocks `{%p if %}`;
- a hyperlink created in a loop with `RichText` and `build_url_id`, with the link text inside
  `w:hyperlink`.

Not yet tested: a template saved by Word itself. Word splits runs at revision boundaries. To
test it, retype one tag in `templates/agenda-body.docx` in Word, save, and run `roundtrip`.

Verification caveat: python-docx `paragraph.text` does not show hyperlink text, so check
hyperlinks in the XML.

## Milestone 1 result (<TC>#<nn>)

The agenda body round-trips with 8 differing lines, all intended:

- two work-item lines: the title of the work item <WI code> is the full title again (it was truncated
  since v9; flagged as unverified against WKI <portal-id>);
- six future-meeting lines: a tab replaces the colon.

The live report has not been changed.

## Known limitations

- Round trip against a live agenda: the rendered body matches the document except for three kinds of
  difference, all data rather than structure: (1) work-item rows that were edited by hand after the last
  portal crawl; (2) the annex, when the roster has changed since the document was written (regenerate it);
  (3) admin list items, which render in the Normal style, while a document may use its own list style
  (for example B1+). Check these by eye before a patch.
- The cover, schedule and IPR blocks in the template head are <TC>#<nn>-specific. They are not
  yet tagged, so a new meeting needs its schedule and cover prepared first.
- The schedule grid is still PowerShell (`build-schedule.ps1`, officecli). The port to
  python-docx is the next step.
- Presenters stay placeholders until the participants list is available (portal, `etsi-mzw`).
- Summaries and outcomes are text in `meeting.toml`; nothing is summarised automatically.
