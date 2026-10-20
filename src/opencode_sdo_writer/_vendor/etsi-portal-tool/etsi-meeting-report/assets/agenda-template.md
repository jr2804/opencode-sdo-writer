# Lead-document skeleton — agenda and report are the same document lineage

Use this skeleton for the lead document (`agenda-draft.md` in the meeting's
project root). The agenda is the working version; the report is the same
document continued at the end of the meeting. Keep the sections and their
order; the content follows the meeting.

Rules: grid and agenda are updated in the same commit; every revision carries a
`What changed since rev N` section; placeholders for undecided items are *(TBD)*.

---

## <TC> #<NN> — Draft agenda / schedule (rev 1)

<Dates>, <venue> (portal meeting <MeetingID>, "<meeting name>").
Status: **DRAFT for chair review**. Portal state of **<date>** (<n> TDocs, <m> work items), queried with `etsi-portal-tool`.
This document is the lead document. The schedule grid in the report (section 1.1.1) is generated from it and kept in sync.
Items marked *(TBD)* depend on documents that are not registered yet.

Fixed constraints: <start time and day>; <fixed slots, e.g. remote participation>; <closing time>; <social event>; <other constraints>.

Decision rule: <when formal approvals are taken, e.g. at the closing session>.

### What changed since rev <N-1>

- <change>

### TDoc inventory (portal, <date>)

| TDoc | Title | Status | For |
|---|---|---|---|
| <UID> | <title from documents get> | Available / Reserved | Decision / Discussion / Info |

Reserved documents have no file yet; say so in the table.

### <Day 1, date>

| Time | Item | TDoc | For |
|---|---|---|---|
| <start>–<end> | <item> | <UIDs> | <disposition> |
| <start>–<end> | Coffee break | | |

### <Day 2, date>

(same table)

### <Day 3, date>

(same table)

### Work items (portal status, <date>)

| WI | Title | Version | Status | Next | Rapporteur |
|---|---|---|---|---|---|
| <WI number> | <title> | <version> | <status> | <next step> | <rapporteur> |

Take status codes from `workitems list` (the portal is authoritative for them).

### Open issues

1. <decision needed, with the options>
2. <decision needed>

Reproduce the portal data:

```bash
mise x -- etsi-portal-tool documents list -m <MeetingID> -t <tc>
mise x -- etsi-portal-tool workitems list -t <tc>
```
