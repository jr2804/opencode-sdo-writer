# ETSI Contributions (TDocs)

A contribution to an ETSI meeting is a portal document -- a **TDoc**. It has
a type, a source, a contact, a title, an abstract and, usually, a file.

## Contribution types

| Type | Meaning | Typical author |
|------|---------|----------------|
| 1 | Meeting Agenda | Secretariat |
| 2 | Meeting Report | Secretariat |
| 4 | Change Request | Working Group |
| 5 | Liaison Statement IN | receiving group |
| 6 | Liaison Statement OUT | sending group |
| 7 | New Draft | member organisation or rapporteur |
| 8 | New WI Proposal / Description | member organisation |
| 9 | Other Contribution (default) | member organisation |
| 10 | Board Contribution | Board / Secretariat |

Type 7 carries a draft deliverable, type 8 carries a work item proposal, type
2 is the record of the meeting itself.

## Fields a contribution needs

| Field | Meaning |
|-------|---------|
| Meeting | the meeting the contribution belongs to |
| TBID | the technical group the contribution is addressed to |
| Type | one of the contribution types above |
| Title | the title shown in the agenda |
| Source | the contributing member organisation |
| Contact | the person responsible for the contribution |
| Abstract | the short description used in the agenda |
| For | the intended outcome, e.g. discussion, agreement, information |
| Related WI(s) | the work item the contribution belongs to |
| File | the attached document, if any |

`--source` and `--contact` have no default: pass them, set `ETSI_SOURCE` and
`ETSI_CONTACT`, or put them in the tool profile configuration.

## Revisions

A correction to a contribution that already carries a payload **must be
published as a revision**:

```bash
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool tdoc create --meeting 82821 --tbid 275 --type 7 \
  --title "My New Draft" --source "<org>" --contact "<name>" \
  --abstract "Description of the contribution" --for rbForDiscussion
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool tdoc revise 345607          # -> Created revision STQ(26)083013r1
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool tdoc upload 345922 /path/to/corrected.docx
```

The portal will not re-point a contribution that already carries a payload, so
the revision child starts with no payload and receives the corrected file.

## Published file names

The published file name -- and therefore the download URL -- is
`<UID>_<slug>.<ext>`. The portal derives the slug from the document **title
at the moment a file is uploaded** and freezes it there. A later title edit
does not rename the file.

Levers:

- change the title before the upload, or
- use `tdoc upload --slug-title "<title>"` at upload time (the title is
  restored afterwards).

Renaming after the upload is not possible; a re-upload is required.

## Binding a contribution to a work item

The "Related WI(s)" list is committed by the portal through its own popup
chain (`ManageRelatedWI.aspx` plus a `ChangeRWI` postback and a final save).
Posting the field on the form is silently ignored. Use the command:

```bash
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool tdoc edit 339463 --wki 78261
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool tdoc edit 339463 --wki "DTS/STQ-332 (TS 104 650)"
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool tdoc edit 339463 --clear-wki
```

`tdoc create --wki <id>` binds the work item right after the create.

## Editing is incremental

`tdoc edit` changes only the fields you pass; omitted fields stay as they
are. The tool fetches the current form state, merges your overrides and
submits.

## Write boundaries

- There is **no client-side write pre-check**. The permission endpoint returns
  account-scoped capability tokens only (for example `CREATE_MEETING`) and
  cannot answer "may I write to meeting N". The portal itself accepts or
  rejects the write.
- `tdoc create`, `tdoc edit`, `tdoc upload` and `tdoc revise` create **real**
  contributions. Verify state with `tdoc show`, which has no side effects.
- A TDoc that is reserved but has no payload downloads as "skipped", not as a
  failure.
- The portal session expires after a period of inactivity; re-run
  `auth login` when calls start failing with authentication errors.

## Cross-references

- [meetings.md](meetings.md) -- when a contribution is due and how it is discussed
- [work-items.md](work-items.md) -- the work item a contribution belongs to
- `etsi-portal-tool` -- full command reference, authentication, MCP server mode
- `sdo-drafting` -- the structure and style of the attached deliverable
