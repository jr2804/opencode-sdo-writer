# Status vocabulary

THREE distinct vocabularies appear around an ETSI meeting report. Don't
conflate them — they answer different questions.

| # | Vocabulary | Where it lives | Answers |
|---|---|---|---|
| 1 | Per-document outcome | narrative paragraph per TDoc (section 2 + wrap-up) | what did the TC do with this document? |
| 2 | Work-item lifecycle code | `Last Draft and Status` column of the WI tracking table | how far has this work item progressed? |
| 3 | Portal disposition (`For:`) | the portal, per TDoc | what is the document *for* (Decision / Discussion / Information) |

The portal disposition is not printed in the report, but it drives the
schedule colour semantics (an item tabled "For: Decision" is an approval
item) and it is available from `documents get <uid>`.

## 1. Per-document decision (the chair's call on each TDoc)

Used in the **narrative per-TDoc paragraphs** of the wrap-up section. One
status per TDoc. The chair writes them as inline sentences; the agent must
recognise and surface them.

| Status | Meaning | Example from a verified report |
|---|---|---|
| **Noted** | Presented, no decision required. Document is on the record. | "The contribution is Noted." |
| **Agreed** | Accepted (often as the basis for further work). | "The contribution is Noted as agreed for basis for further work." |
| **Revised** | Edited; a new revision UID is referenced. | "The contribution was edited and revised in <UID>." |
| **Approved** | Formal TC-level approval (titles, LSs, reports). Almost always preceded by "Decision:". | "Decision: TC <TC> approved the change." |
| **Decision:** (prefix) | A formal decision statement, not a status per se. Always followed by an action (approve, send out, etc.). | "Decision: Anton will send it out." |

The exact phrase is the signal, not a parsed field. Detection is
phrase-match ("Noted", "Agreed", "Revised", "Decision: ... approved"),
not table parsing.

### When other statuses appear

These are NOT in the verified report but are common in other ETSI TCs and
should be recognised if present:

- **Postponed** — decision deferred to a later meeting.
- **Withdrawn** — contributor pulled the document.
- **Liaised-out** — sent to another TC for review.
- **Rejected** — TC declined the contribution.

Per-TC verification recommended: read the previous meeting's report
section headers (Approvals / LSs OUT / New WIs / Stopped WIs) for the
TC's local conventions.

## 2. Work-item lifecycle (ongoing work tracking)

Used in the **"Last Draft and Status" column of the work-item tracking
table**. This is a *progress* indicator, not a decision outcome.

| Code | Stage |
|---|---|
| `0a` | Work item adopted |
| `1`  | Start of work |
| `2`  | Early draft |
| `4`  | Stable draft |
| `6`  | Final draft for approval |
| `8`  | TB approval |
| `12` | Published |

The codes are defined in the report's own **"Key Status" sub-table**
(typically between the schedule and the work-item tracking table). The
agent must read that sub-table for the exact mapping — codes can vary
between ETSI groups, and the key sub-table is the authoritative source
in the meeting itself.

**The portal work programme is authoritative for the code.**
`workitems list --tc <TC>` reports each WI's current status and the next
step (e.g. `Stable draft (2026-10-02)`, `next: Final draft`), which is the
value the report's table should carry. Verified against <TC>#<nn>:

| WI | Portal says | report code |
|---|---|---|
| Deliverable A (WI code A) | Stable draft, next: Final draft | `4` — not `6`, even though its draft is tabled for approval |
| Deliverable B (WI code B) | Final draft registered by the Secretariat, next: publication | `8` |
| Deliverable C (WI code C) | Start of work | `1` — not `0a` |

Lesson: a draft being *tabled* does not advance the WI status code. The
code changes when the milestone is actually reached (approval at the
meeting, registration by the Secretariat).

Common compound forms found in the verified report: `0` (zero / not
started — but `0a` means "adopted"), `-` (no draft yet), trailing
letter codes (e.g. `2m` = milestone variant of stage 2). Treat any code
not in the local key as **opaque — display the code verbatim, do not
interpret it**.

## Putting them together

A TDoc paragraph from the verified report reads:

> **<UID>** Draft – <WI code> v0.0.1 (<deliverable>) ...
> <person> presented the first draft for <deliverable>. The contribution
> is **Noted as agreed** for basis for further work.

That paragraph carries:

- Decision status: **Noted** + **Agreed** (compound outcome).
- No work-item lifecycle code — the contribution creates a new WI
  (the WI in the table starts at status `-` / `0a`).

The skill's phase-2 agent must extract both vocabularies when present,
keeping them on different rows in the draft decisions list (per-TDoc
outcomes) vs the work-item table (per-WI progress).
