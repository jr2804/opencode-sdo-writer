# Issues file and data conflicts

Every meeting collects its open problems in one markdown file, `docs/<tc><nn>/issues.md`
(for <TC>#<nn>: `docs/<tc><nn>/issues.md`). Do not fix a problem silently in the agenda or
the report. Record it, and decide with the owner what happens to the text.

## Sections

| Section | What goes in | Who acts |
|---|---|---|
| A — Contributions (template issues) | problems in the documents themselves: wrong template or meeting reference, file name used as title, version in title does not match content, cover-page source differs from the portal, reserved TDoc without abstract | the authors (through the TO) |
| B — etsi-portal-tool | missing, truncated or wrong data from the tool: missing fields, truncated titles, shifted columns, missing IDs | the tool owner (send through intercom with evidence) |
| C — Data conflicts | two sources disagree (portal vs cover page vs previous report vs chair's text) | the chair decides which source wins |
| D — Kept as they are | text that is outdated or uncertain but stays in the document until the owner decides | the owner; reason recorded |

## Entry format

One table row per item, with: ID, subject (TDoc or item), the issue in one sentence,
the evidence (the exact string or a link), the proposed action. Section D also gets
the reason the text was kept.

## Rules

1. **Portal title by default.** A cover-page title that differs goes to section A.
2. **Affiliations come from the participants list** once it is available. Until then,
   keep the affiliation as the portal gives it and record a section-C entry for any
   conflict.
3. **Evidence first.** Quote the source string. A conclusion without evidence is
   not an entry.
4. **Tool issues go to the tool owner with the evidence**, and the entry records
   the date sent. Do not work around a tool bug in the agenda data.
5. **Re-check the file on each daily check.** Close entries when the source is fixed,
   and say which change closed them in the agenda's `What changed` section.

## Example (<TC>#<nn>, rev 6)

| ID | Subject | Issue | Evidence | Proposed action |
|---|---|---|---|---|
| A4 | <UID> | Portal title says v0.4.2; content and cover say v0.7.1 | `documents get` title | author to correct the title |
| B3 | workitems list | Title truncated; a work-item ID was given for the wrong work item | the list title vs the report page title | tool fixed; use the report page |
| C2 | Pat Sample | Affiliation: Example Systems GmbH (agenda) vs Sample Telecom (portal WI supporting organisations) | report 1.6/1.7; `workitems list` | chair, pending the participants list |
| D1 | TR 103 907 | Note "<person> will upload the Final draft" is outdated: final draft v1.1.2 is registered | portal status | kept; owner to update |
