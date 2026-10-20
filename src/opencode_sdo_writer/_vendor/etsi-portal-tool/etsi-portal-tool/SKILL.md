---
name: etsi-portal-tool
description: >-
  Practical CLI usage of the etsi-portal-tool binary for ETSI delegates.
  Covers authentication setup (SecretSpec, encrypted vault, browser,
  cookies), committee browsing, meeting management (list, get, register,
  permissions), document operations (list, get, url, download, bulk),
  TDoc write operations (create, edit, upload, revise, show), work items, and the
  local web GUI. Also covers the MCP stdio server mode for AI agents.
  Use when the user asks about running the etsi-portal-tool CLI/MCP,
  needs help with specific commands, or wants to follow a workflow for
  handling ETSI portal tasks.
---

# etsi-portal-tool — CLI & MCP Usage

`etsi-portal-tool` is a single-binary CLI for managing ETSI portal
operations: authentication, committee/meeting browsing, document download,
meeting registration, and TDoc write operations (create, edit, upload).

## Quick Reference

| Area          | Commands                                                                                                          | Auth needed?                        |
| ------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| Auth          | `auth login`, `auth status`, `auth logout`, `auth refresh`, `diagnose`, `vault`                                   | No (creates session)                |
| Committees    | `tc list`, `tc get`                                                                                               | No                                  |
| Meetings      | `meetings list`, `meetings get`, `meetings find`                                                                   | No                                  |
| Documents     | `documents list`, `documents get`, `documents url`, `documents download`                                          | No (list, get); Yes (download, url) |
| Bulk download | `download meeting`, `download extract`, `download list`, `download open`                                          | Yes                                 |
| Registration  | `register status`, `register signup`, `register cancel`, `register person`, `register roles`, `register whoami`, `register permissions` | Yes                     |
| TDoc ops      | `tdoc create`, `tdoc edit`, `tdoc show`, `tdoc upload`, `tdoc revise`                                              | Yes (+ write permission)            |
| Work items    | `workitems list`                                                                                                  | No                                  |
| Web GUI       | `serve`                                                                                                           | Uses cached session or /login       |
| Diagnostics   | `diagnose`                                                                                                         | No                                  |

## MCP Server Mode (AI agents)

`etsi-portal-tool mcp` runs the binary as an MCP stdio server
(newline-delimited JSON-RPC 2.0). Prefer this over shelling out to the
CLI when operating as an AI agent — typed tool schemas, no pterm parsing.
The authoritative tool list is always `tools/list` on a live server.

Public tools (no login required): `etsi_committees`, `etsi_meetings_list`,
`etsi_meeting_get`, `etsi_meeting_find`, `etsi_tdoc_list`, `etsi_tdoc_get`.

Authenticated, read-only (require login, do not modify the portal):
`etsi_documents_url`, `etsi_documents_download` (writes the file to
disk — into the download cache unless `output` is given; `extract` defaults to
true, `refresh` forces a re-download), `etsi_tdoc_show`, `etsi_workitems`,
`etsi_meeting_roles`,
`etsi_permissions` (your account's capability tokens), `etsi_auth_status`,
`etsi_whoami`, `etsi_registration_status`.

Mutating: `etsi_tdoc_create`, `etsi_tdoc_edit`, `etsi_tdoc_upload`,
`etsi_tdoc_revise`, `etsi_registration_signup`, `etsi_registration_cancel`. There is no
client-side write-permission pre-check on the TDoc operations: the portal's
permission endpoint carries account-scoped capability tokens only, so the
portal itself rejects a write that is not permitted.

Auth for authenticated tools is resolved exactly like the CLI (cached
session → SecretSpec → vault).

## Authentication

### 1. SecretSpec (primary credential path)

`auth login` (default) resolves the ETSI credential pair via SecretSpec
(a `secretspec.toml` declaration plus a provider). If SecretSpec is
configured but a required secret is missing, the CLI warns and falls back
to the vault. Users who previously relied on `ETSI_USERNAME` /
`ETSI_PASSWORD` environment variables should provision them through a
SecretSpec provider (e.g. dotenv or env) — the CLI no longer reads those
variables directly.

```bash
etsi-portal-tool auth login --verify
```

### 2. Vault (fallback, recommended for headless/agent use)

Encrypted vault at `~/.config/etsi-portal-tool/<profile>/vault.enc`
(Argon2id + AES-256-GCM). Two **different** secrets are involved — this trips
people up:

| Secret | Where it comes from | Prompt |
|---|---|---|
| Vault master passphrase | You choose it at `vault init` (typed twice) | `Vault master passphrase (new):` / `Repeat vault master passphrase:` |
| Vault master passphrase (again) | Required to unlock the vault | `Vault master passphrase:` |
| ETSI account password | Your portal.etsi.org password, stored *inside* the vault | `ETSI account password:` |

Both are prompted by `vault set`; `ETSI_PORTAL_TOOL_VAULT_PASSPHRASE` replaces only the
**master passphrase** prompt (never the ETSI one). Every vault command needs
the master passphrase.

```bash
# Initialize vault (prompts for the master passphrase twice)
etsi-portal-tool -p <profile> vault init

# Store the ETSI pair. Two prompts: "ETSI account password:" (the portal password)
# then "Vault master passphrase:" (the key to the vault, asked once).
etsi-portal-tool -p <profile> vault set <username>

# Verify what is stored (--show-password reveals it)
etsi-portal-tool -p <profile> vault get

# Also: vault passwd (change the master passphrase), vault rm (drop the pair)

# Log in from the vault
etsi-portal-tool -p <profile> auth login --vault --verify

# Headless / agent / CI: supply the MASTER passphrase via env so it cannot prompt
$env:ETSI_PORTAL_TOOL_VAULT_PASSPHRASE = "your-master-passphrase"   # bash: export ...
etsi-portal-tool -p <profile> vault set <username> <your-etsi-password>   # non-interactive
```

Gotchas:

- Passing the ETSI password as the second positional puts it in your shell
  history — prefer the prompt on a shared machine.
- A wrong master passphrase fails with `decrypting vault (wrong passphrase?)`.
- `-p` is a global flag: put it before the subcommand (`-p <profile> vault set ...`).

### 3. Browser (bypasses IP rate limits)

```bash
etsi-portal-tool auth login --browser
# Launches Camoufox (anti-detect Firefox) for interactive login
```

### 4. Cookie import (from DevTools)

```bash
# Copy Cookie header from browser DevTools → Network → request → Headers
etsi-portal-tool auth login --cookies "ASP.NET_SessionId=...; .DOTNETNUKE=..."
```

### Session management

- Session is cached at `~/.config/etsi-portal-tool/<profile>/session.json`
- Subsequent commands reuse the session automatically
- Session expires after some hours; re-run `auth login` or `auth refresh`
- Use `diagnose` to check full auth status

## Workflows

### A: Browse meetings and documents (read-only, no auth)

```bash
# 1. List known committees
etsi-portal-tool tc list

# 2. Get details for a specific committee (parent + sub-committees)
etsi-portal-tool tc get STQ

# 3. List upcoming meetings
etsi-portal-tool meetings list --tc STQ

# 4. List all meetings (including past) with date range
etsi-portal-tool meetings list --tc STQ --all
etsi-portal-tool meetings list --tc STQ -s 2026-01-01 -e 2026-12-31

# 5. Get meeting details
etsi-portal-tool meetings get 82821 --tc STQ

# 5a. Named rather than numbered, or from a past meeting? Find it by name — the
#     search covers the whole history and prints every match:
etsi-portal-tool meetings find "STQ#82" --tc STQ -r

# 6. List documents for a meeting
etsi-portal-tool documents list -m 82821 -t stq

# 7. Filter documents by type or search
etsi-portal-tool documents list -m 82821 -t stq --type Draft
etsi-portal-tool documents list -m 82821 -t stq --search "agenda"

# 8. Paginate document list
etsi-portal-tool documents list -m 82821 -t stq --head 5
etsi-portal-tool documents list -m 82821 -t stq --tail 3
```

### B: Download documents (needs auth)

The UID alone is sufficient everywhere — numeric ID (`339450`) or display
UID (`STQ(26)082029`). The `-m`/`-t` flags are accepted on download but
ignored (the resolution searches all committees).

```bash
# 1. Login first
etsi-portal-tool auth login

# 2. Print the download/viewer URL (numeric ID needs no auth)
etsi-portal-tool documents url 339450
etsi-portal-tool documents url STQ(26)082029   # resolves via search

# 3. Download a single document (goes into the download cache)
etsi-portal-tool documents download 339450
etsi-portal-tool documents download STQ(26)082029 -o report.pdf   # explicit path instead

# 4. Bulk download all documents for a meeting (into the cache, cache hits skipped)
etsi-portal-tool download meeting -m 82821 -t stq

# 5. Bulk download, cap at 10 documents, keep the .zip archives unextracted
etsi-portal-tool download meeting -m 82821 -t stq --no-extract --max 10

# 6. Custom output dir; --overwrite re-downloads instead of using the cache
etsi-portal-tool download meeting -m 82821 -t stq -o ./dl --overwrite

# 7. List the cache / extract a ZIP / open a file
etsi-portal-tool download list
etsi-portal-tool download extract STQ(26)082029/STQ-326v031.zip
etsi-portal-tool download open "STQ(26)082029/STQ-326v031.docx"
```

### C: Meeting registration (needs auth)

```bash
# 1. Check registration status
etsi-portal-tool register status 82821

# 2. Register for a meeting / cancel
etsi-portal-tool register signup 82821
etsi-portal-tool register cancel 82821

# 3. Check your identity / delegate profile
etsi-portal-tool register whoami
etsi-portal-tool register person

# 4. List available roles for a meeting
etsi-portal-tool register roles 82821

# 5. Check your portal permission tokens
etsi-portal-tool register permissions                 # e.g. CREATE_MEETING
etsi-portal-tool register permissions --json
```

### D: TDoc write operations (needs auth)

`tdoc create`, `tdoc edit` and `tdoc upload` have **no client-side write
pre-check**: the portal's `GetPermissions` endpoint returns only
account-scoped capability tokens (e.g. `CREATE_MEETING`) with no per-meeting
information, so it cannot say whether you may write to a given meeting — the
portal itself rejects a write that is not permitted. Inspect your tokens with
`register permissions` (informational only).

```bash
# 1. Show TDoc metadata (no side effects)
etsi-portal-tool tdoc show 339463
etsi-portal-tool tdoc show 339463 --json

# 2. Create a new TDoc
#    --source/--contact have no default: pass them, set ETSI_SOURCE/ETSI_CONTACT,
#    or put them in ~/.config/etsi-portal-tool/<profile>/config.json
etsi-portal-tool tdoc create \
  --meeting 82821 --tbid 275 --type 7 \
  --title "My New Draft" \
  --source "<your-org>" \
  --contact "<your-name>" \
  --abstract "Description of the contribution" \
  --for rbForDiscussion

# Contribution types:
#   1  Meeting Agenda
#   2  Meeting Report
#   4  Change Request
#   5  Liaison Statement IN
#   6  Liaison Statement OUT
#   7  New Draft
#   8  New WI Proposal / Description
#   9  Other Contribution (default)
#   10 Board Contribution (Test)

# 3. Edit TDoc properties (only provided flags change)
etsi-portal-tool tdoc edit 339463 --title "Updated Title"
etsi-portal-tool tdoc edit 339463 --abstract "New abstract text"
etsi-portal-tool tdoc edit 339463 --status "Noted"

# 3a. Bind a work item to a TDoc (the "Related WI(s)" / "Deliverable(s)" list)
etsi-portal-tool tdoc edit 339463 --wki 78261
etsi-portal-tool tdoc edit 339463 --wki "DTS/STQ-332 (TS 104 650)"
etsi-portal-tool tdoc edit 339463 --clear-wki    # remove the binding

# 4. Upload a file to an existing TDoc
etsi-portal-tool tdoc upload 339463 /path/to/document.docx

# 5. Publish a correction: a revision is the route, because the portal will not
#    re-point a contribution that already carries a payload. The child starts with no
#    payload. tdoc revise warns — never blocks — when the target's meeting has ended:
#    the rule is a 2-3 week window (.agents/POLICIES.md → Boundaries) and the warning
#    says which side you are on.
etsi-portal-tool tdoc revise 345607          # -> Created revision STQ(26)083013r1 (345922)
etsi-portal-tool tdoc upload 345922 /path/to/corrected.docx

# 6. Upload with a chosen published file name (title is restored afterwards)
etsi-portal-tool tdoc upload 339463 /path/to/document.docx \
  --slug-title "Considerations on Plugtests for Bluetooth LE Audio"
```

#### Published file names (how the URL is minted)

The published file name — and therefore the docbox URL — is
`<UID>_<slug>.<ext>`, where the **portal derives the slug from the document
TITLE at the moment a file is uploaded**, and freezes it there (a later title
edit does not rename the file). The slug rule (verified against live published
names): take the **first 60 characters** of the raw title, keep letters, digits
and `-`, turn **every other character into `_`** (nothing collapsed or trimmed —
two spaces give two underscores, and the 60-char cut can land mid-word). The
extension comes from the uploaded file.

Consequences for daily use:

- `tdoc show <id>` prints the projection for a file-less document
  (`File name (once uploaded): <UID>_<slug>.<ext>`), so the URL is knowable
  before any upload; once a file exists it prints the real stored name.
- **There is no slug field before upload.** The portal stores nothing and
  ignores the field on the create/edit forms — writing it does nothing. The
  portal UI's "File name" display is the same live projection of the title,
  not a stored value.
- To get a URL different from the title's slug **without changing the
document title**, use `tdoc upload --slug-title "<text>"`: the tool sets the
title to that text for the upload only and restores the original immediately
afterwards (also on upload failure). The CLI prints the exact name it will
mint before touching the portal.
- Titles are effectively ASCII-only: the portal silently drops `™`, `®` and
  other non-ASCII characters. The tool applies that rule itself and warns
  (`title adjusted for the portal …`) instead of letting the stored title
differ from what you typed.

#### Work-item binding (the "Related WI(s)" / "Deliverable(s)" list)

The portal commits a work-item change only through the full browser click
chain: the picker popup plus a parent refresh postback plus a final save.
A plain form post with `hidddlWIReference` set is silently ignored.

The tool drives that chain in Go (`internal/portal/tdoc_workitems.go`,
`TDocService.SetWorkItems`). `--wki` on create and edit resolves the id
(numeric or `DTS/STQ-332` code), enters edit mode, picks the work item in
the picker popup, refreshes the parent page, and saves. Verified live on
STQ#83 (083015, 083016 bound to WKI 78261).

```bash
# Bind one work item (id or code)
etsi-portal-tool tdoc edit 345630 --wki 78261
etsi-portal-tool tdoc edit 345630 --wki "DTS/STQ-332 (TS 104 650)"

# Remove the binding
etsi-portal-tool tdoc edit 345630 --clear-wki

# On `tdoc create`, --wki binds the work item after the create saves
etsi-portal-tool tdoc create --meeting 84544 --tbid 275 --type 9 \
  --title "..." --source "..." --contact "..." --for rbForDiscussion \
  --wki 78261
```

A work-item-only edit (only `--wki` or `--clear-wki`) skips the plain save —
the chain performs its own. The `Changed: wki` / `Changed: wi (cleared)`
lines in the CLI summary report the binding step.

### E: Work items (committee agenda)

```bash
# List open work items for a committee by code or TBID
etsi-portal-tool workitems list --tc STQ
etsi-portal-tool workitems list -t 275
```

### F: Local web GUI

```bash
# Serve the web GUI (M4) on loopback; reuses the cached session,
# otherwise /login prompts for the vault service name. PWA installable.
etsi-portal-tool serve

# Options: custom address, skip automatic session reuse
etsi-portal-tool serve --addr 127.0.0.1:8080 --no-auto-login

# --bind-public exists for LAN exposure but has NO built-in auth —
# only use it behind TLS termination and an authenticating proxy.
```

### G: Diagnostics

```bash
# Full auth diagnostic (login + session + credential-source report)
etsi-portal-tool diagnose
```

For anything beyond that — inspecting what a portal page really returns while
writing a parser — drive a browser externally (for example an agent browser or
DevTools); the tool deliberately ships no reverse-engineering commands.

## Common patterns

### TC codes

Committees can be referenced by:

- **Numeric TBID:** `275`, `276`
- **Short code:** `STQ`, `stq`, `Stq` (case-insensitive)
- **Comma-separated:** `STQ,ERM` or `275,276`
- **Recursive:** `--tc STQ -r` includes sub-committees (e.g. STQ + STQ Mobile)

### Date filtering for meetings

```bash
# Default: upcoming/ongoing meetings from today onward
etsi-portal-tool meetings list --tc STQ

# Past meetings: use --all or set --start-date in the past
etsi-portal-tool meetings list --tc STQ --all
etsi-portal-tool meetings list --tc STQ -s 2025-01-01

# Specific range / limit results
etsi-portal-tool meetings list --tc STQ -s 2026-06-01 -e 2026-12-31
etsi-portal-tool meetings list --tc STQ -s 2026-01-01 -l 5
```

### JSON output

```bash
etsi-portal-tool register status 82821 --json
etsi-portal-tool register permissions --json
etsi-portal-tool tdoc show 339463 --json
```

### Profiles

A profile is a complete isolated identity — its own encrypted vault, cached
session and settings — so several accounts coexist without logging out. The
profile is **required**: pass `-p, --profile` or set `ETSI_PORTAL_TOOL_PROFILE`.
There is NO implicit default — the OS / Windows login name is never used
(ETSI login names have no relation to the local account, so silently picking
the OS login would leak a personal identity into the vault directory name).

```bash
# Day-to-day profile
etsi-portal-tool -p main vault init
etsi-portal-tool -p main vault set alice
etsi-portal-tool -p main auth login --vault

# Second account, same binary, separate vault and session
etsi-portal-tool -p acct2 vault init
etsi-portal-tool -p acct2 vault set bob
etsi-portal-tool -p acct2 auth login --vault

etsi-portal-tool -p acct2 meetings list --tc STQ -r   # acts as bob
etsi-portal-tool -p main meetings list --tc STQ -r    # acts as alice
```

Names may contain letters, digits, `.`, `_` and `-`, starting with a letter
or digit.

### Styled output

- **Tables** with boxed borders for list/detail views
- **Section headers** (`── Registration Status ──`) group output
- **Colored status** — green ✓ / yellow ⚠ / red ✗
- **Progress bars** during bulk operations
- **Auto-disable** when stdout is piped (`| grep`, `> file`, `--json`)

## Pitfalls

1. **Session expiry:** The ETSI portal session expires after some hours
   of inactivity. If commands start failing with auth errors, re-run
   `auth login` (or `auth refresh`) to restore it.

2. **Rate limiting:** The portal has IP-level rate limiting on the EOL
   login endpoint. If `auth login` fails repeatedly with correct
   credentials, use `auth login --browser` (Camoufox) or
   `auth login --cookies` to bypass.

3. **No TDoc write-permission pre-check:** `tdoc create`, `tdoc edit` and
   `tdoc upload` rely on the portal to accept or reject the write; the
   permission endpoint exposes account-scoped tokens only (e.g.
   `CREATE_MEETING`) and cannot answer "may I write to meeting N?". A
   Reserved TDoc with no payload downloads as "skipped", not as a failure.
   Inspect your tokens with `register permissions`.

4. **Registration endpoint:** The tool uses the `Register` REST endpoint
   with the full payload (`PersonId`, `RepresentingOrganisationId`,
   `PresenceType`). A `RegisterUserToGTW` endpoint exists for
   GoToWebinar meetings, but the tool uses the generic `Register`
   endpoint by default.

5. **TDoc edit is incremental:** Only fields you pass via flags are
   changed. Omitted fields stay as-is. The tool fetches the current
   form state, merges your overrides, and submits.

6. **TDoc upload requires a real file:** The file must exist on disk
   at the path you provide. The tool uses multipart/form-data via the
   Telerik RadAsyncUpload control.

7. **No live testing on ongoing meetings:** TDoc create/upload/revise operations
   create real contributions on the portal. Verify state with `tdoc show`
   instead, which has no side effects. Do not write to an ended meeting's
   documents either: that boundary is a 2-3 week window
   (`.agents/POLICIES.md` → Boundaries), and `tdoc revise` warns when the
   target sits outside it.

8. **The published file name cannot be changed before upload:** the portal
   mints `<UID>_<slug>.<ext>` from the title at upload time and freezes it.
   There is no stored slug to edit while a document has no file — posting the
   field on the create/edit forms is ignored, and the portal UI's "File name"
   display is a live projection of the title. The levers are the title itself
   (before upload) or `tdoc upload --slug-title` (at upload, title restored
   afterwards). Renaming after upload is not possible at all — a re-upload is
   required.

9. **Work-item binding needs the full popup chain, not a field post:** the
   "Related WI(s)" link on a contribution is committed by the page's own
   Telerik JavaScript through a `ManageRelatedWI.aspx` popup plus a
   `ChangeRWI` postback plus a final save. Posting `hidddlWIReference` on
   the form is silently ignored; only `tdoc edit --wki <id>` (which drives
   the chain) and the browser click sequence work. Verified live.

10. **SecretSpec fallback:** If SecretSpec is configured but a required
    secret is missing, `auth login` prints `SecretSpec: ... (falling back
    to vault)` on stderr and continues with the vault — a login that
    succeeds may not be using the credential source you intended.

## Related skills

- `etsi-meeting-report` — prepare / conduct / document ETSI TC meetings;
  drafts the meeting report (agenda + schedule + per-document statuses)
  by composing this skill's commands with `officecli-docx`
- `etsi-directives` — ETSI governance and procedures knowledge base
  (voting, work items, drafting rules, IPR policy)
