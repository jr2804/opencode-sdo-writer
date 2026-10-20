# Portal recipe — exact command sequence per phase

Composes `etsi-portal-tool` commands (CLI + MCP) into the meeting-report
workflow. For full option/flag docs see the `etsi-portal-tool` skill.
Behaviour notes below are verified against **v2026.10.30**. Older builds
(≤ v2026.10.4) differ where called out. v2026.10.30 brings `register list`
(per-meeting participant roster) and v2026.10.13 brings WKI/report-URL.
The notes also call out the v2026.10.10/v2026.10.27 history for the gaps
that have since been closed.

## Phase 1 — Prepare

Goal: identify the meeting, download every TDoc, get the previous report as
structural baseline, and list open work items.

### 1a. Confirm meeting + committee

```bash
etsi-portal-tool meetings list --tc <TC>
etsi-portal-tool meetings get <portal-id> --tc <TC>     # "Documents: 10" is the expected doc count
```

```text
# MCP
etsi_meetings_list  { tbids: [275], include_past: true }
etsi_meeting_get    { meeting_id: <portal-id>, tbid: 275 }
```

`meetings list` / `meetings get` are anonymous — they work without a
session.

### 1b. The meeting's document list (the authoritative UID set)

```bash
etsi-portal-tool documents list -m <portal-id> -t <tc>
```

Verified on v2026.10.6: this is **meeting-scoped** and returns exactly the
meeting's documents — including `Reserved` ones and revision rows
(`…083008a1`). In ≤ v2026.10.4 the meeting filter was ignored server-side
and the command returned the whole committee archive (thousands of rows);
if you see that, upgrade.

Use the returned UIDs **plus** `meetings get`'s `Documents: N` as the
expected set. Cross-check the count — a missing row usually means a
`Reserved` TDoc (no payload), not a fetch failure.

### 1c. Bulk-download the meeting's documents

```bash
etsi-portal-tool download meeting -m <portal-id> -t <tc> --extract
```

Verified download model (v2026.10.5+):

- Files land in a **per-user cache**:
  `~/.cache/etsi-portal-tool/meetings/<YYYY-MM-DD>-<MeetingID>/<UID>.<ext>`
  (on Windows `%USERPROFILE%`-redirected homes apply; <TC>#<nn> →
  `…/meetings/2026-10-19-<portal-id>/`). The date prefix is the meeting's **start
  date**.
- **UID filenames** — `<UID>.doc`, and ZIP payloads extract one
  level into a UID-named folder (`<UID>/`), keeping the archive
  removed.
- **Single-level extraction only** — a nested archive (e.g.
  `<TC>-327v0133.zip`) is a deliverable package and is deliberately left
  intact; extract it by hand when reading the content.
- Repeat runs are **cache hits** (`Downloaded 0 documents (9 already
  cached), 1 skipped (no payload), 0 failed`).
- `Reserved` TDocs have no payload and are reported
  `skipped (no payload — …)`, not as failures.
- `--overwrite` = ignore the cache and re-download. `-o <dir>` writes a
  one-off copy outside the cache (and skips files already present there
  since v2026.10.6 — check before fetch). `download list` lists the cache.
- **A `manifest.json`** is written per meeting folder — see step 1d.
- ≤ v2026.10.4: the output defaulted to `./<meeting-id>_<tbid>` relative to
  the CWD, and a repeat run re-downloaded everything.

Keep a **curated copy** of the meeting's documents in the project (e.g.
`docs/<tc><nn>/<portal-id>/`) if the repo is the long-lived artefact store; the
cache is tool-internal dedup and may be cleared.

### 1d. TDoc metadata — read the cache manifest first

Since v2026.10.7, every cache meeting folder carries a **`manifest.json`**
written by the download, which supplies per document: `uid`, numeric
`id` (the DL-ID the schedule hyperlinks need), `title`, `type`,
`status` (`Available` / `Reserved`), `payload` (`file` / `extracted` /
`none` / `unknown`), the cached artefact name + `size` + `present`, the
`download` block (`bytes`, `sha256`) when that run fetched the bytes, and
both `portal_url` (works for anything, including `Reserved`) and
`docbox_url` (present only when the portal linked an actual file).

That single file replaces a per-TDoc `documents get` sweep:

```powershell
# list the meeting's documents with their DL-IDs, payload state and links
$m = Get-Content "$env:USERPROFILE\.cache\etsi-portal-tool\meetings\*\manifest.json" -Raw | ConvertFrom-Json
$m.documents | Select-Object uid, id, type, status, payload, docbox_url
```

Field semantics — read them together, they answer different questions:

| Field | Means |
| --- | --- |
| `payload: file` / `extracted` | the document has a payload; `cached.path` names it (a file, or a folder for an extracted archive) |
| `payload: none` | **no payload exists at the source** (e.g. a `Reserved` report TDoc) — there is nothing to download, and no link to invent |
| `payload: unknown` | the run never reached the contribution page — usually an auth failure, not a property of the document |
| `cached.present: false` | a file that should be there is gone = cache damaged |
| `docbox_url` absent | the portal does not link a file (combines with `payload: none`) |

`download.sha256` covers the fetched archive; for `payload: extracted`
entries the archive itself is removed after extraction, so only
`cached.size` (the extracted folder's total) can be re-checked locally.

Still fall back to `documents get <uid>` when you need something the
manifest does not carry (source/contact, `For:` disposition, abstract).

### 1e. Previous report (baseline)

```bash
etsi-portal-tool documents list -m <previous_meeting_id> -t <tc> --search "report"
etsi-portal-tool documents download "<uid>"
```

Keep it locally and untracked — a real report carries personal data and must
never be committed; the tracked `examples/stq82/example-report.docx` is the anonymised
baseline (ground truth for structure,
schedule and vocabulary).

### 1f. Work items

```bash
etsi-portal-tool workitems list --tc <TC>
```

Needs a session. The portal work programme is **authoritative for the WI
status code** — use it to update the report's WI tracking table (see
`report-structure.md`, section 3). No MCP equivalent. Since v2026.10.13 the
list carries the WKI-ID and a full-title column (truncation removed); use
`workitems list --json` for machine-readable output and `workitems show <wki>`
for the per-WI report page (rapporteur with given-first name, technical
officer, supporting organisations, report URL).

## Phase 5a — Participants roster

```bash
etsi-portal-tool -p <profile> register list <meeting-id> --json
# aliases: participants, attendees
# flags: --presence f2f|online (fixed v2026.10.31, commit 6518543 — the portal ignores the field; the filter is applied client-side), --role Delegate|Chairman|ViceChairman|Staff, --limit N, --json
```

Verified live on <TC>#<nn> (15 registered: 10 face to face / 5 online) and
<sub-TC>#<nn> (6 registered). The list is produced by the skill command
`uv run python -m meeting_report participants --tc <TC> --tc <sub-TC code> --meeting <TC>#<nn>
--meeting <sub-TC>#<nn> --out <file.xlsx>` (any committees and meetings, see
`references/python-pipeline.md`). Raw rosters stay in `tools/var/participants/`
(git-ignored, personal data); the workbook is untracked (`**/participants*.xlsx`).
The MCP equivalent of the roster is `etsi_register_list`.

## Phase 2 — Draft

No portal calls. Reasoning over the downloaded documents, the **agenda
TDoc** (the report's starting point — see `report-structure.md`), the prior
report, and the chair's constraints. Produce:

- slot assignments + colours + legend (per `references/schedule-table.md`)
- per-document outcome text (per `references/status-vocabulary.md`)
- WI tracking table updates

## Phase 3 — Render (Word)

Hand off to `officecli`; recipe in `references/docx-build-patterns.md`,
builder script in `assets/build-schedule.ps1`.

## Phase 4 — Publish

### 4a. The report is the Technical Officer's document

The meeting report TDoc belongs to the Technical Officer. The planner does not produce,
publish, name or upload it, so no command in this skill targets it. The planner's
document is the chair's agenda, which takes the agenda's TDoc number.

### 4a'. Publishing a file into a contribution

- **Reserved, no payload:** `tdoc upload <id> <file>` works (verified 2026-10-16).
- **Already has a payload:** the portal will not re-point the contribution. Publish a
  revision instead (`rN`, `tdoc revise`, available from v2026.10.33). The old
  contribution keeps its stale pointer; say so in the issues file.
- **Verify:** `tdoc show <id>` (status, file name) and a `documents download` of the
  contribution, compared by size and SHA-256 with the local file. Use `--slug-title` only
  when the chair wants a specific published name.

### 4b. Permissions — informational, not a gate

`register permissions` (MCP `etsi_permissions`) prints the account's
capability tokens, e.g. `CREATE_MEETING`. It is **not** per-meeting write
permission: token absence does not mean you cannot write, and since
v2026.10.4 `tdoc create/edit/upload` no longer consult it at all — the
portal itself is the authority on whether a write is permitted. A rejected
write is the real answer; do not pre-block on tokens.

## Phase 5 — Conduct / revise

During the meeting the chair fills outcomes and adjusts slots. Re-run the
builder (regenerate grid + legend), fill the narrative sections, re-upload.
After the meeting the final report replaces the working copy.

## Cross-cutting

| Concern | CLI | MCP |
| --- | --- | --- |
| Session state | `auth status` | `etsi_auth_status` |
| Refresh session | `auth login --vault` (or `--browser`, `--cookies`) | — |
| Who am I (source/contact) | `register whoami` | `etsi_whoami` |
| Capability tokens | `register permissions` | `etsi_permissions` |

### Session notes

- `auth status` reports **cookie presence, not validity**. A stale session
  surfaces later as a credential error from a command that needs auth
  (`documents get`, `documents download`, `workitems list`, all `tdoc`
  writes). Since v2026.10.5 the error names each credential source it tried
  instead of a bare "no credentials available".
- Commands that need auth: `documents get`, `documents download`,
  `workitems list`, every `tdoc` mutation, `register whoami`. Anonymous:
  `meetings list/get`, `documents list`.
- In a mise-activated project shell the vault passphrase may already be in
  the environment (`ETSI_PORTAL_TOOL_VAULT_PASSPHRASE`, renamed from
  `ETSI_VAULT_PASSPHRASE` in v2026.10.9 — the old name warns once per
  process and stops working after that release), so downloads work
  non-interactively; a plain tool shell will prompt. Running the tool via
  `mise exec -- <tool> …` injects the same environment without handling the
  secret yourself.
- **A login can fail silently in older builds** (≤ v2026.10.7): the POST
  can answer 200 while the session is still unauthenticated, after which a
  protected fetch redirects to the login page and dies on a transport
  error. v2026.10.8 confirms the session after login and reports
  `login did not establish a session`; it also recognises the login
  redirect and tells you to re-authenticate.

## Known gaps (tool maintainer's reply, updated 2026-10-14)

Gaps found while building the <TC>#<nn> agenda. The ones marked *fixed* are in
released binaries. Open ones are tracked in the issues file (`docs/<tc><nn>/issues.md`,
sections B/C) and the live status of each is below.

| Gap | Status | Effect on the agenda | Workaround |
| --- | --- | --- | --- |
| Shifted columns in `documents list -m` (the column layout depends on authentication) | **Fixed** (v2026.10.13) | wrong titles in the cache manifest | none |
| `workitems list` truncated titles and status text | **Fixed** (v2026.10.13) | cut WI titles | none |
| No WKI_ID in `workitems list` | **Fixed** (v2026.10.13) | the WI page could not be found from the list | none |
| Empty ETSI number (`TS )`) | **Fixed** (v2026.10.12) | blank parenthesis | none |
| `reference` reading `Type` instead of the code (work items without a number) | **Fixed** (v2026.10.12) | wrong WI title | none |
| Official Source not in `documents get` / `tdoc show` (form has it in `hidlblSourcevalue`) | **Fixed** (v2026.10.13) | source had to be read from the cover page | none — `documents list --json` has a `source` per row |
| **Per-meeting participant roster** (face-to-face / remote, roles) | **Fixed** (v2026.10.30, `register list`) | presenters stayed `[Presenter]`; affiliations came from the work-item supporting organisations and the per-contribution source | none — `register list --json` returns the full roster; `--presence f2f` / `--presence online` is honoured end-to-end (v2026.10.31, commit 6518543) |
| Rapporteur names: surname-first in the list, given-first on the report page | **Open** (etsi-8bh) | inconsistent names | normalise by hand in the config, or read from `workitems show <wki>` |

### Work-item IDs

`workitems list --json` gives each work item's `wki_id` and ready-to-open `report_url`.
Take the title from the report page, not from the list (the list truncates). Do not
guess an ID from a link: check that the page's title matches the work item. A worked
table of IDs for one meeting is in `examples/` (not part of the generic workflow).

## Sequencing rules

1. **Download before drafting.** Phase 2/3 depend on the local documents.
2. **Confirm the session before phase 4** — but expect that permission
   checks are informational, and let the portal reject a bad write.
3. **Test end-to-end on a past meeting.** `tdoc upload` is a real write to
   `portal.etsi.org`; an idempotent same-value `tdoc edit` against a
   `Reserved` TDoc is a safe smoke test of the write path.
