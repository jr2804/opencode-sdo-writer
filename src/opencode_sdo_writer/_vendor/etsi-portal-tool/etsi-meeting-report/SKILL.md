---
name: etsi-meeting-report
description: >-
  Prepare, conduct and document ETSI technical-committee meetings — draft the
  meeting report containing the agenda, a colour-coded graphical time-slot
  schedule of topics/documents, and per-document status assignments
  (Noted / Agreed / Postponed / Revised / …). Drives `etsi-portal-tool` for
  meeting and document access plus TDoc upload, and `officecli` for the Word
  deliverable. Use this skill whenever the user asks to draft, build, revise
  or update an ETSI meeting report, agenda or schedule; when a chair,
  vice-chair or technical officer needs a meeting prepared or a report
  produced; when assigning statuses to documents handled in a meeting; or
  whenever working with an ETSI TC meeting (past or upcoming) and a Word
  deliverable is the goal.
compatibility: requires the etsi-portal-tool skill (CLI + portal session for authenticated reads and all writes) and officecli. Reads without a session: meetings list/get, documents list. Everything else (documents get/download, workitems list, tdoc *) needs one.
---

# etsi-meeting-report

Workflow for an ETSI TC meeting: prepare the artefacts, draft the
report/agenda, render it in Word, publish, and update through the meeting.

The flagship deliverable is the **meeting report** — a Word document
containing the agenda, a **colour-coded schedule grid** mapping topics and
documents to 30-minute slots, the per-document outcomes, and the work-item
status table.

## The one thing to know first

**The agenda and the report are the same document at two stages of its
life.** The report is produced by *continuing the agenda* — copy the
meeting's agenda TDoc and adapt it, do not start from a blank template.
Verified: the <TC>#<nn> report (<UID>) and the <TC>#<nn> agenda
(<UID>) share their paragraph IDs.

| | Agenda | Report |
|---|---|---|
| Drafted by | TO + chair + vice-chair(s) | TO (for the chair) |
| When | before and during the meeting | at the end of the meeting |
| Focus | planning | decisions / formalism |

Corollary: the **report TDoc already exists** on the portal as `Reserved`
before the meeting. Publish into it (`tdoc edit` + `tdoc upload`) — never
`tdoc create` a second report TDoc.

## Planning rules (the essence of meeting planning)

These are the rules that carried over from planning a real meeting. They apply to any
ETSI meeting, not to one; the worked example is <TC>#<nn>.

- **Design the schedule fresh for each meeting.** A grid, slot placement or block from an
  earlier meeting or revision is not a decision and is never carried forward. Only the
  constraints the chair or the Technical Officer state explicitly stand, plus the standing
  formatting rules (one colour per topic, no merged topic cells, TAH/TAC, legend without times).
- **Chair decisions go into the issues file with their status and date.** Use *Resolved*
  (decided), *Answered* (a question with a yes/no), *Accepted for now*, *Deferred* (for example
  "decided at the end of the meeting"), or *Void* (the item came from a design that was dropped).
  Deferred items stay open until the meeting closes.
- **Documents keep their owners' names.** The meeting report is the Technical Officer's document:
  the planner never produces, publishes or names it. The agenda is the chair's document, so its
  file takes the agenda's TDoc number. Other working files get no TDoc number until the owner
  assigns one; never invent a number.
- **Affiliations are what the registration says.** The chair may accept a company's former name
  until ETSI renames it after an acquisition. A change of main contact is harmless when the
  source organisation is unchanged.
- **Participant lists are generated, never typed.** `meeting_report participants` builds one
  workbook per meeting pair, named `ETSI-<UID>-Meeting.xlsx`, one row per person, with a
  Meeting column that lists the meetings a person joins (", "-separated). Presence follows the
  portal's codes: 2 = face to face, 1 = online (the portal's own row labels agree for current
  meetings). Regenerate before the meeting and again on the planning day: registrations keep
  moving until the meeting. Lists are personal data and stay untracked.

## Workflow (5 phases)

| # | Phase | Actions | Reference |
|---|---|---|---|
| 1 | Prepare | Identify the committee + meeting ID; list the meeting's documents (authoritative UID set); download them (the run writes a `manifest.json` with each document's DL-ID, payload state and links — see `references/portal-recipe.md`); get the previous report as baseline; list work items with their WKI_IDs (full titles: see `references/portal-recipe.md`, known gaps) | `references/portal-recipe.md` |
| 2 | Draft | Start from the **agenda TDoc**: set title block, plan the slots (colours + legend), map each TDoc → slot, prepare per-TDoc outcome text and WI-table updates | `references/schedule-table.md`, `references/status-vocabulary.md`, `references/report-structure.md` |
| 3 | Render | Build the schedule (config + `assets/build-schedule.ps1`, see "Schedule: regenerate for a new meeting") and fill the report sections in Word, section by section | `references/schedule-table.md`, `references/docx-build-patterns.md`, `assets/build-schedule.ps1` |
| 4 | Publish | `tdoc edit` the reserved report TDoc, then `tdoc upload` the file | `references/portal-recipe.md` |
| 5 | Conduct / revise | Chair fills outcomes and adjusts slots during the meeting; regenerate the grid, fill the narrative, re-upload | same as 2–4 |

## Inputs to collect from the user before drafting

The user (chair / vice-chair / TO) supplies constraints the portal cannot:

- **committee + meeting ID** (and the meeting number, e.g. `<TC>#<nn>`);
- **fixed slots** (e.g. an external speaker at a pinned hour, a demo, a
  social event that forces an early close);
- **items without a TDoc yet** (planned but unregistered contributions,
  discussion points, AOB);
- **constraints** such as "must be early enough to allow revisions", "must
  finish before the social event", "at least one full slot";
- **who attends / who presents** (for the per-document paragraphs). Affiliations come from the participants list (`etsi-portal-tool register list <meeting-id> --json`, v2026.10.30+). The portal roster gives person, role, presence (face-to-face or online) and representing organisation; affiliations are not to be guessed. The JSON and the chair-facing workbook stay untracked (personal data).

Record them in a plan document before building — the schedule is a
negotiated artefact, not a derivation.

## CLI vs MCP (verified on v2026.10.6)

| Step | CLI | MCP |
|---|---|---|
| Meeting list / detail | `meetings list --tc <tc>` · `meetings get <id> --tc <tc>` · `meetings find <query> --tc <tc> -r` (whole history; returns every match) | `etsi_meetings_list`, `etsi_meeting_get`, `etsi_meeting_find` |
| Meeting document list | `documents list -m <id> -t <tc>` | `etsi_tdoc_list` (no `tc` argument) |
| TDoc metadata | `documents get <uid>` | `etsi_tdoc_get` |
| Download (bulk / single) | `download meeting -m <id> -t <tc> --extract` · `documents download <uid>` | `etsi_documents_download` |
| Work items | `workitems list --tc <tc>` | — |
| Session / identity | `auth status`, `register whoami` | `etsi_auth_status`, `etsi_whoami` |
| Capability tokens | `register permissions` | `etsi_permissions` |
| TDoc create / edit / upload | `tdoc create`, `tdoc edit <id>`, `tdoc upload <id> <file>` | — |

Reads that need no session: `meetings list`, `meetings get`,
`documents list`. Everything else needs one.

## Schedule: regenerate for a new meeting

The schedule is produced, not hand-drawn. To regenerate it for a new meeting
(or to update the current one) follow these steps. The rules behind them are in
`references/schedule-table.md`; the builder details are in
`references/docx-build-patterns.md`, section 10.

1. **Collect the chair's inputs** (see "Inputs to collect"): day and time
   constraints, fixed slots, topics without documents, breaks, the social event.
2. **Pull the documents** with `etsi-portal-tool` (meeting list, `documents list`,
   `download meeting --overwrite`). The cache `manifest.json` gives the UIDs,
   DL-IDs, payload state and `docbox_url` for each document.
3. **Copy the config example** `assets/schedule-config.example.ps1` into the
   meeting's `scripts/` folder as `<tc><nn>-schedule.ps1`, and fill in: the
   manifest path, the UID prefix, the heading and caption text, the topics
   (colour, label with document numbers), the slot rows, the topic per cell,
   the document cells, and the merges. a complete worked example is in `examples/`.
4. **Run the builder** against the report: `powershell -ExecutionPolicy Bypass
   -File scripts/build-schedule.ps1 -Config scripts/<config>.ps1`. Check the batch
   summary (`failed=0`, `rolledBack=False`) and that `validate` passes.
5. **Render and look at the pages** (`officecli view <file> screenshot --page N`).
   Colour and merge problems show only in the image.
6. **Agenda body (sections 1.2–4.4)**: the Python pipeline in `tools/` (see `references/python-pipeline.md`). Chair data for the meeting lives in `docs/<tc><nn>/meeting.toml`. Render to a scratch file (`render --base <the meeting's own agenda document>`) and run `roundtrip` against that document first; patch the live report only after the differences are listed and explained. The work-item table comes from `workitems list` (portal login required).
7. **Lead document** (`agenda-draft.md` in the project root): generated by the Python `lead` command only if the file does not exist. Once it exists it is edited directly (an agent or a targeted patch), never regenerated: the
   day tables, the TDoc inventory and a `What changed since rev N` section.
   Grid and agenda go in the same commit. Record every open problem in
   `docs/<tc><nn>/issues.md` (see `references/issues-and-data-conflicts.md`); do not fix a problem silently in the text.

When a file is open in Word, the builder fails with "being used by another
process". Ask the user to close it; do not kill Word.

### Daily check during a meeting week

When the chair asks for a daily check (for example until the Friday before the
meeting), repeat every day:

1. Re-download the meeting: `download meeting -m <id> -t <tc> --overwrite`.
2. Compare against the grid and the agenda: new UIDs, changed titles (take
   titles from `documents get`, not the list), DL-IDs, Reserved → Available.
3. Update the config and the agenda in one commit, and record the change.
4. Report "changes" or "no change" to the chair.

Keep every slot until the chair decides to drop it. Empty slots are not
deleted automatically.

## Pitfalls

- **Live meeting side effects.** `tdoc upload` writes a real contribution on
  `portal.etsi.org`. Experiments never run on live contributions: a probe that
  stages a file can publish it (this happened on 2026-10-16). Test write paths on
  a throwaway contribution in a past meeting, or not at all.
- **Publishing a file.** The first upload into a `Reserved` contribution with no
  payload works. Once a contribution has a payload, the portal will not re-point
  it: publish a new revision (`rN`, via `tdoc revise`) instead. Verify every
  publish by comparing the served size and SHA-256 with the local file. The
  published name comes from the title at upload time (`--slug-title` names it
  explicitly); keep titles exactly as the chair wrote them, and expect ™/® to be
  stripped.
- **There is no per-meeting write gate.** `register permissions` returns
  account capability tokens (e.g. `CREATE_MEETING`) — informational. Token
  absence does not mean you cannot write; the portal rejects a write it
  does not want.
- **Session state is not session validity.** `auth status` proves cookies
  exist, not that they work. Expect a credential error from the first
  authenticated command once the session is stale; re-run
  `auth login --vault` (or `--browser`, `--cookies`).
- **The report TDoc is normally already `Reserved`.** Check with
  `documents list -m <id> -t <tc> --type Report` before creating anything.
- **`documents list -m` was not meeting-scoped before v2026.10.5** — it
  returned the whole committee archive. If you see thousands of rows
  spanning years, upgrade the tool.
- **Downloads go to a global cache, not the CWD** (v2026.10.5+):
  `~/.cache/etsi-portal-tool/meetings/<start-date>-<MeetingID>/<UID>.<ext>`.
  Repeat runs are cache hits. Keep a curated copy in the project if the repo
  is the long-lived store.
- **Colour coding needs its legend, and yellow is banned.** The schedule is
  unreadable without the legend table; yellow is illegible in print.
  See `references/schedule-table.md`.
- **Never compose a docbox file URL.** The filename embeds a truncated
  title slug and the original payload extension. Link to the portal viewer
  (`…/ContributionCreation.aspx?primarykeys=<DL-ID>`) instead — that also
  works for `Reserved` TDocs, which have no file at all.
- **The schedule is a plan; statuses are outcomes.** They live in different
  tables/sections — do not mix them.
- **`officecli batch` is atomic.** One failing item rolls back the whole
  batch while per-item flags still read `success: true`. Read
  `summary.failed` and the envelope's `success`. See
  `references/docx-build-patterns.md`.
- **Placeholders are bracketed italics** — `[The chair opened the meeting
  at HH:MM CEST on <date>.]` — so they are greppable
  (`officecli query <f> 'p:contains("[")'`) and must all be resolved before
  publishing.
- **The portal tool's read surface has been filling in.** v2026.10.13 brought correct columns in `documents list`, full titles in `workitems list`, and the official source per TDoc. v2026.10.30 brought the participants roster (`register list`). The remaining gaps (rapporteur name normalisation, `--presence` filter bug, etc.) are listed in `references/portal-recipe.md`, known gaps.
- **Titles and sources differ between sources.** Portal title by default. A cover-page title that differs goes to the issues file, not into the agenda.
- **Crawled data is never committed.** Raw portal output, cache manifests, downloads and normalised records stay in `tools/var/` (git-ignored) or the portal cache. Only curated chair inputs (`meeting.toml`, `issues.md`) and rendered deliverables are committed.
- **Per-committee conventions vary.** Treat every reference here as a
  verified baseline for TC <TC> and check the previous report for local
  habits.

## Pointers

- `references/python-pipeline.md` — the Python pipeline for the agenda body and the lead document: layout, commands, round-trip rule, docxtpl spike results, known limitations.
- `references/schedule-table.md` — the colour-coded schedule grid + legend:
  shape, colours, short codes, links, merge rules, and the "don't" list.
- `references/report-structure.md` — verified section order, title block,
  the agenda→report lineage, per-TDoc paragraph shape, WI table columns,
  wrap-up sub-labels.
- `references/issues-and-data-conflicts.md` — the issues file convention (author issues, tool issues, data conflicts, kept items), with an example.
- `references/status-vocabulary.md` — the two vocabularies: per-document
  outcomes (Noted / Agreed / …) and WI lifecycle codes (`0a`…`12`).
- `references/portal-recipe.md` — command sequence per phase, download/cache
  behaviour, reserved-TDoc publishing, permission semantics.
- `references/docx-build-patterns.md` — officecli batch mechanics, merge
  primitives, hyperlink-in-cell, scripting gotchas, verification steps.
- `assets/build-schedule.ps1` — generic, re-runnable schedule builder. It takes
  a per-meeting config (`-Config`), so the builder itself never needs editing.
- `assets/schedule-config.example.ps1` — the config template, with every field
  documented. A complete filled-in example is in `examples/` (one past meeting; not
  part of the generic workflow).
- `tools/` — the Python pipeline (uv project, docxtpl): `build_template.py`,
  `meeting_report` (CLI: roundtrip, render, crawl, lead, participants),
  `templates/agenda-body.docx` (built by `build_template.py`), `templates/lead.md.j2`.
  Content for a meeting: `docs/<tc><nn>/meeting.toml`.
- `assets/agenda-template.md` — the lead-document skeleton (agenda = report
  lineage): day tables, TDoc inventory, work items, open issues.
- `assets/meeting-report.docx` — a generic Word template of the admin boilerplate.
  The meeting's own agenda document supersedes it in practice (see "the one thing to
  know first").
- `tools/meeting_report/` — the agenda body is rendered by the Python pipeline
  (sections 1.2–4.4, see `references/python-pipeline.md`). There is no PowerShell agenda
  builder; the content of a meeting is in `docs/<tc><nn>/meeting.toml`.
- `examples/` — worked examples of past meetings (a schedule config and a prior report,
  anonymised). Read them for structure; never copy their content into a new meeting.
- Related skills: `etsi-portal-tool` (CLI/MCP reference), `officecli`
  (Word/Excel/PPT I/O), `sdo-docx-formatting` + `etsi-drafting`
  (styles: `TAH`, `TAC`, deliverable conventions), `etsi-basics`
  (organisation, deliverable types).
