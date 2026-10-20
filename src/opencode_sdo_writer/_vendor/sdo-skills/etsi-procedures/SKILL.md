---
name: etsi-procedures
description: 'ETSI working procedures: how to take part in a TC or WG meeting, submit a contribution (TDoc), propose or track a Work Item, and follow a deliverable through approval. Use when the agent needs to prepare or attend an ETSI meeting, write and submit a contribution, create a work item description, find meeting documents on the ETSI portal, or understand the ENAP / SRdAP / MAP approval routes and their deadlines. Normative source: `etsi-directives` (Ch 3 Rules of Procedure, Ch 11 Technical Working Procedures).'
---

# ETSI Procedures

How work actually flows through ETSI: a meeting, a contribution, a work item,
a deliverable. The binding rules are in `etsi-directives`; this skill is the
practical route through them. Portal mechanics are in `etsi-portal-tool`.

## The one-minute picture

```text
Proposal -> Work Item (adopted) -> Drafting (maturity milestones)
    -> Technical Group endorsement -> Secretariat submission
    -> Approval route (ENAP | SRdAP | MAP | TB adoption) -> Publication
    -> Maintenance
```

Three rules dominate everything else:

1. **Nothing is approved before its Work Item is adopted** (TWP).
2. **Consensus first**, then a two-stage vote: 71 % of votes cast, then
   recalculated on Full members' votes alone. No quorum, no proxy, no vote
   splitting in a technical group.
3. **The Work Item is the atom**: one responsible group, one named Rapporteur,
   one deliverable, at least four Full/Associate supporters.

## Preparing for a meeting

A meeting is a Technical Group session with a fixed set of documents. Before
it, a member organisation usually:

- registers the delegate(s) and checks the delegate profile;
- submits contributions as TDocs before the contribution deadline stated in
  the meeting invitation (the deadline is per meeting, not a global rule);
- prepares the agenda item material and, for draft deliverables, the draft
  text itself.

During the meeting the group walks the agenda, reaches consensus on the
contributions, and records decisions. Afterwards the **meeting report** lists
the documents with their final status (agreed, noted, revised, withdrawn).

Details: [references/meetings.md](references/meetings.md) — meeting types,
lifecycle, registration, agenda and report, how to list and download the
documents of a meeting.

## Submitting a contribution

A contribution is a portal **TDoc** with a contribution type, a source, a
contact, a title, an abstract, and usually a file. The portal contribution
types are:

| Type | Meaning |
|------|---------|
| 1 | Meeting Agenda |
| 2 | Meeting Report |
| 4 | Change Request |
| 5 | Liaison Statement IN |
| 6 | Liaison Statement OUT |
| 7 | New Draft |
| 8 | New WI Proposal / Description |
| 9 | Other Contribution (default) |
| 10 | Board Contribution |

A correction to a contribution that already carries a file must be published
as a **revision** of that TDoc, not as a new upload over it.

Details: [references/tdocs.md](references/tdocs.md) — fields, revision rules,
published file names, and the write boundaries to respect.

## Work Items

A Work Item proposal names the deliverable, the responsible group, the
Rapporteur and the supporters. The group records it as a **Work Item
Description** and adopts it. Drafting then tracks **maturity milestones**
(early → stable → mature → final) and **decision milestones** (WG
endorsement, TG endorsement).

Details: [references/work-items.md](references/work-items.md) — proposal and
description, supporters, rapporteur duties, stopping rules, SReq-derived
work, and binding a contribution to a work item.

## Approval routes and clocks

| Deliverable | Route | Clocks |
|-------------|-------|--------|
| EN (ETSI-originated) | ENAP — NSOG Weighted National Voting after Standstill and Public Enquiry | Standstill from +60 days |
| EN (SReq-derived) | SRdAP — NSBG competence | 25-day NSBG vote, 30-day DG notification |
| ES / EG | MAP — all Full and Associate members | submit +14 d, prepare +30 d, vote 60 d, publish +10 d |
| TS / TR | Technical Body adoption (no membership vote) | submit to Secretariat +14 d |
| GS / GR | ISG validation | per ISG ToR |
| SR | TB, ad-hoc group or DG on behalf of GA, Board or OCG | published on Drafting-Rules compliance |

Details: [references/approval.md](references/approval.md) — what each route
requires, how a vote fails and still passes, and the maintenance rules.

## Cross-references

- `etsi-directives` -- normative source: Ch 3 (Rules of Procedure), Ch 11 (Technical Working Procedures), Ch 13 (Drafting Rules)
- `etsi-governance` -- organisation, deliverable types, lifecycle, roles
- `etsi-tools` -- specification metadata retrieval, portal tooling
- `sdo-drafting` -- deliverable structure, style names and skeleton templates
- `sdo-docx` -- formatting and DOCX operations for the submitted file
- `sdo-project-setup` -- project layout and document properties
- `etsi-portal-tool` -- CLI and MCP for the portal (meetings, documents, TDocs, work items)
