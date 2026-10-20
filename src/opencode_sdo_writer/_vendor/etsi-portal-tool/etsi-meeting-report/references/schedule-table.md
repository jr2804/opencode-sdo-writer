# Schedule table — rules for the meeting schedule (report section 1.1.1 and the agenda)

The schedule is a **time-slot × day** matrix: rows are 30-minute slots,
columns are the meeting days, and each cell names the topic or document in that
slot. It is a *planning* artefact. It shows what happens when. Outcomes belong
in section 2 and in the wrap-up.

It is produced by `assets/build-schedule.ps1` from a per-meeting config file
(`assets/schedule-config.example.ps1`; worked example
`assets/<tc><nn>-schedule.ps1`). The rules below are the ones the user settled on
for <TC>#<nn>; a new meeting inherits them unless the chair says otherwise.

## 1. Grid shape

- **Caption above the grid** (style `TH`), text like
  `Schedule of <TC>#<nn> by time slot and topic`. **No table counter**: no SEQ
  field, no `Table N:` label, no bookmark for schedule tables (chair decision,
  2026-10-14). Apply the same to the legend table.
- **Columns:** `Time` | Monday | Tuesday | Wednesday (day headers as in the
  agenda, e.g. `Monday – 19th October`).
- **Rows:** one row per 30-minute slot, start times only (`09:00`, `09:30`,
  … `17:30`), plus one row for the evening event (`19:00`) when there is one.
  Do not use ranges (`09:00 - 09:30`).
- **Day range:** the grid covers the working day 09:00–17:30 and the evening
  event. Outside the official meeting hours a day is `(no meeting)`.
- **Last row:** the note `White cells = unscheduled. Grey cells = breaks,
  outside meeting hours, or the social event.`, one merged row across the
  whole grid, style `TAN`.
- **Table width:** AutoFit to Contents (`tblW type=auto`, `tblLayout
  autofit`). The builder patches the width type in the XML after the batch.

## 2. Cell content

1. **One colour per topic block.** Every slot of a block carries the block's
   colour. Only the **first** slot of the block carries the text. The colour
   carries the continuation. Repeating `#<nnn>` or `<topic label>` in every
   slot is wrong.
2. **Short text.** Either the document number (`#005`, `#008, #008a1`) or a
   short topic label (`Opening, Agenda`, `<deliverable>`, `<topic>`, `<ANC-like topic>`
   methods (IEC 60268-24)`, `Social event / dinner`). Do not write `TBD`.
3. **Short numbers.** The short number is the UID without the meeting prefix:
   `<UID>` → `#003`; a revision keeps its suffix (`#008a1`).
4. **Hyperlinks for documents that have a file.** For each document with a
   `docbox_url` in the cache manifest, the short number is a hyperlink to that
   URL, using the `Hyperlink` character style on top of `TAC`. A reserved
   document (no payload, no URL) is plain text. Never compose a docbox URL by
   hand: the filename is truncated and carries the payload extension.
5. **Link colour.** Dark blue text (`#00008B`) on top of the `Hyperlink` style,
   so the link reads on every fill (chair decision). Never put blue on a
   background.
6. **No text formatting in cells.** No bold, italic or underline in the body
   cells. Clear run formatting, then apply `TAH` (header) or `TAC` (content).
7. **Unscheduled slots stay white.** Do not invent content. Do not write
   `TBD`; a slot without content is simply empty.
8. **Document-level sizing of blocks.** A topic that needs more than 30 minutes
   takes consecutive slots. Keep the 30-minute grid: **do not merge topic
   cells** (chair decision). A 1-hour block is two slots of one colour, label
   once. (Exception: a block labelled with a deliverable name was kept as one
   1-hour block when no document numbers existed. Keep it that way until
   documents are registered.)

## 3. Merges — the only allowed ones

| Case | Merge | Notes |
|---|---|---|
| Breaks across the day columns (coffee, lunch) | `colspan` | label once, grey |
| Out-of-hours slots, per day column | `vmerge` | label `(no meeting)` once, grey |
| Note row | `colspan` over the whole grid | style `TAN` |
| Legend header | `colspan` over both legend columns | style `TAH` |

A break that is not the same for all days (e.g. lunch Tuesday and Wednesday,
but not Monday) is a `colspan` over the affected days only, and the trailing
cells of that row are removed by the merge. The builder only supports merges
that end at the last column.

## 4. Colours (accessibility)

- Colour-blind safe palette (Okabe–Ito extended, plus matplotlib pink and
  brown). **Never yellow.**
- Each topic has its own colour. **Placeholder topics without a document each
  get a distinct colour** (chair decision, 2026-10-14).
- Blue (`#0072B2`) is used for a topic only when no link appears on it; links
  are dark blue, so a blue fill next to a link is confusing. Prefer another hue
  if the topic has documents.
- Grey (`#999999`) is reserved for breaks, `(no meeting)` and the social event.
  It is never a topic colour and never in the legend.

Fills used in <TC>#<nn> (reuse unless a conflict appears):

| Topic | Fill | Text |
|---|---|---|
| Administration | `#D55E00` | black |
| Topic A (+ related report) | `#E69F00` | black |
| Topic B | `#009E73` | black |
| Topic C (deliverable) | `#D9C2E9` | black |
| Topic D — placeholder | `#882255` | white |
| Topic E — placeholder | `#56B4E9` | black |
| Topic F — placeholder | `#8C564B` | white |
| <TC> Mobile report — placeholder | `#0072B2` | white |
| Other contributions | `#44AA99` | black |

## 5. Legend table

- **Separate table**, immediately after the grid, preceded by **one empty
  paragraph** (otherwise Word merges the two tables into one).
- **Header row** `Legend`, centred over both columns, style `TAH`.
- **One row per topic**, two columns: colour swatch (filled cell, **no text,
  never a hex code**) | topic label.
- **Label** names the real topic and lists its **document numbers at the end**
  (`… — #008, #008a1, #010`). Topics without a document say so
  (`— no document yet`). No times in the legend, no categories like
  "Decision" or "Discussion".
- **Keep one row per topic**, even when two topics share a theme (chair
  decision: "Other contributions" stays one row for #011 and #012).
- Legend rows use `TAC`. No `Breaks` row: the grey note row explains it.
- No table counter for the legend either.

## 6. Keeping the lead document in sync

The **lead document** is `agenda-draft.md` in the project root. It is the
chair's working agenda and it always matches the grid (chair decision,
2026-10-14). Every grid change is made in the same commit as the matching
agenda change, and the agenda carries a `What changed since rev N` section.

A checklist for every change:

1. Edit the config (slots, fills, document cells, merges).
2. Run the builder, check the batch summary (`failed=0`, `rolledBack=False`)
   and render both pages.
3. Update the agenda's day tables, the TDoc inventory and "What changed".
4. Commit grid, builder config and agenda together.

## 7. Don't

- Don't put per-document outcomes (Noted, Agreed, …) in the grid.
- Don't repeat a label across the slots of one block.
- Don't use yellow; don't use blue as a background; don't use hex codes in the
  legend.
- Don't add a table counter to the schedule or the legend.
- Don't merge topic cells; don't use `hmerge` (use `colspan`).
- Don't drop a slot because it is empty before the chair decides.
