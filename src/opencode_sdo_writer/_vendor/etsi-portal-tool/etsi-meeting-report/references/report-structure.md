# Report structure

Verified against `examples/stq82/example-report.docx` (an anonymised prior report, names/orgs/metadata synthetic), the
<TC>#<nn> agenda (<UID>) and the <TC>#<nn> report draft (<UID>). Section
titles vary by TC; the pattern is stable.

## The central fact: agenda and report are the same document

The agenda and the report are one document at two stages of its life: same
structure, same paragraph IDs, same boilerplate. The report continues the agenda.

| | Agenda | Report |
|---|---|---|
| Drafted by | TO + chair + vice-chair(s), jointly | TO (on behalf of the chair) |
| When | before and during the meeting | at the end of the meeting |
| Focus | planning (slots, order, open points) | decisions and formalism |
| Lifecycle | living document, revised during the meeting | concludes the meeting |

Practical consequence: to scaffold a report, start from the meeting's agenda and
adapt it. A blank template loses the meeting-specific boilerplate and the planned
slot content.

## Section order (as built for <TC>#<nn>, rev 6)

| # | Section | Content |
|---|---|---|
| — | Title block | TC, TDoc UID, `Report for <TC>#<NN> (<dates>)`, venue, `Source:` |
| 1 | Admin, LSs, <TC>/<sub-TC code> matters | umbrella heading |
| 1.1 | Opening, IPR call, Antitrust & competition, Code of Conduct reminder | boilerplate, the schedule (1.1.1) and the legend |
| 1.1.1 | Meeting schedule for `<TC>#<NN>` (heading 3) | caption (no table counter), grid, legend, note row — see `schedule-table.md` |
| 1.1.2–1.1.4 | IPR Statement, Antitrust, Code of Conduct | standard ETSI boilerplate, verbatim |
| 1.2 | Approval of agenda | the agenda TDoc, and the decision sentence |
| 1.3 | Work Programme status | pointer to section 3 |
| 1.4 | Liaison Statements IN/OUT | LS IN with their TDoc blocks (Source, Presenter, Summary, Outcome), then the LS OUT decision |
| 1.5 | Report from ETSI Board, General Assembly and any other ETSI matters | BOARD and GA sub-headings, reports by the TO |
| 1.6 | <TC> Mobile update on work programme, report from last meeting, AOB | Meeting report <sub-TC>#NN (1.6.1); <TC> Mobile WIs for approval/publication (1.6.2) |
| 1.7, 1.8, … | custom admin items | e.g. officials renewal; a meeting-specific item (plugtest, election, ...) |
| 2 | Meeting Contributions | Heading 2 per topic group; TDoc blocks in UID order — see below |
| 3 | Open Work Items' status | intro (ETSI Directives clause 1.6.5, work-programme link), key status codes table, work-item table (generated from the portal) |
| 4 | Wrap-up and closure | 4.1 Approvals, 4.2 Future Meetings / Events, 4.3 Any Other Business, 4.4 Closure |

The routine items (1.2 to 1.6) are always present, in this order. Custom items
follow them.

## Section 2 — contributions per topic

Group the TDocs by topic or work item (Heading 2), not by UID. Liaison statements IN are in 1.4, not here. Within a group, list the documents in UID order. Each TDoc is a block of five lines:

```text
<UID><tab>Draft - <WI code> v0.7.1 (<deliverable>) "<title>"   (Header style)
Source:<tab>Example Systems GmbH                           (style EX)
Presenter:<tab>[Presenter]                                 (style EX)
Summary:<tab><abstract ...; review before publication>     (style EX)
Outcome:<tab>[To be recorded during the meeting]           (style EX)
```

Rules:

- The title line uses the **portal title** by default. Cover-page titles that differ go to the issues file, not into the agenda.
- **Source** is the **official portal source** (`documents list -m <meeting> -t <tc> --json`, per row). A chair text that differs from the portal is reported in the issues file, and the portal value is used.
- Key lines use the **EX** style with a real tab after the key, so values align (the EX hanging indent is the tab stop). The title line tab stop is set to the same position.
- Regular text uses the document's **Normal** style. No direct font formatting in the body.
- **Presenter** is the chair-facing placeholder. If the meeting has a participants roster (`etsi-portal-tool register list <meeting-id> --json`, v2026.10.30+), the name of the presenting delegate can be filled in: read the TDoc's main-contact from `tdoc show <id>` and the participants' `RepresentingOrganisation` from the roster. Until then, keep `[Presenter]`. Affiliations of contributors come from the work-item supporting organisations (per `workitems show <wki>`) and the per-contribution source.
- **Summary** is written from the downloaded text plus the work-item page and the agenda context. Keep it short (two to four sentences) and factual. A reserved TDoc with no file gets a placeholder.
- **Outcome** stays a placeholder until the meeting records it.

## Section 3 — open work items

1. Narrative intro (static ETSI boilerplate): the <TC> group keeps track of ongoing
   work; NB on ETSI Directives clause 1.6.5 (automatic stop after one year without
   progress); NB with the ETSI work-programme search link.
2. Key status codes table (`0a`, `1`, `2`, `4`, `6`, `8`, `12`). Both tables are in ETSI
   style: header row TAH, content TAC, centred, no table counter.
3. Work-item table, generated from `workitems list --tc <TC>`. Columns:
   `ETSI and WI Numbers | Title | Rapporteur | Last Draft and Status | Next Step | Notes on Status`.
   The portal list truncates long titles and status texts. Use the full title from
   the work-item page (`WorkProgram/Report_WorkItem.asp?WKI_ID=…`) when it is available.

## Section 4 — wrap-up and closure

- 4.1 Approvals: sub-labels in bold, each followed by the decision or `N/A`:
  Final drafts · LSs OUT · STF/TTF Reports · New WIs · Stopped WIs.
- 4.2 Future Meetings / Events: one line per meeting (`<TC>#<nn>: Mon 1st to Wed 3rd
  Feb 2027 …`). Use plain lines, not tabs.
- 4.3 Any Other Business.
- 4.4 Closure: `The Chair closed the meeting at HH:MM CEST on <date>.`

## Title block

```text
ETSI TC <TC>                                                    <UID>
Report for <TC>#<nn> (<dates>)      <organisation>, <venue>, <country>
Source: ETSI Secretariat, TO <person>
```

## Reserved report TDoc — do not create a new one

The report TDoc exists on the portal before the meeting, with status `Reserved`
and no payload (`<UID>`, DL-ID `<portal-id>`). Publish with `tdoc edit` and
`tdoc upload` against that ID. Never `tdoc create`, which would duplicate the
reserved row. See `portal-recipe.md`, phase 4.

## Placeholder convention

While drafting, mark every undecided text with square brackets in italics, for
example `[To be recorded during the meeting]`. They are then findable
(`officecli query <f> 'p:contains("[")'`). Resolve all of them before publishing.
