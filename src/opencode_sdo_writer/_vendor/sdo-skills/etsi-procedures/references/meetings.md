# ETSI Meetings

Meeting types, the life of a meeting, and how to work with the documents that
belong to it. Normative source: TWP (Ch 11) and the Antitrust Guidelines
(Ch 05, C.3); portal mechanics: `etsi-portal-tool`.

## Which body meets

| Body | Basis | Term | Produces |
|------|-------|------|----------|
| ETSI Project (EP) | market-sector requirement | limited | deliverables within the TWP |
| Technical Committee (TC) | technical area (ToR) | no term limit | deliverables within the TWP |
| ETSI Partnership Project (EPP) | market sector + external partners | limited | its own approval incl. validation |
| Industry Specification Group (ISG) | technology area, >= 4 members request the DG | lifecycle-managed | GR / GS only |
| Software Development Group (SDG) | software activity, >= 4 members request the DG | lifecycle-managed | no ETSI Deliverables |

A Working Group (WG) is a sub-group of a TC. The Rapporteur of a Work Item
belongs to the WG or TG that adopted it.

## The life of a meeting

1. **Invitation** -- the meeting is announced with its agenda, its dates and
   the **contribution deadline**. Deadlines are per meeting; they are not a
   global ETSI rule, so always read them from the invitation.
2. **Registration** -- delegates register per meeting; the portal holds the
   delegate profile and the representing organisation.
3. **Contributions** -- members upload TDocs (see [tdocs.md](tdocs.md)) before
   the deadline; the agenda is built from the accepted contributions.
4. **Meeting** -- the Chair opens with the standing ritual (Code of Conduct,
   antitrust, IPR reminder) and walks the agenda item by item.
5. **Decisions** -- consensus is the default; a vote is the fallback.
6. **Meeting report** -- a contribution of type 2 that records every document
   with its outcome (agreed, noted, revised, withdrawn) and the decisions
   taken. The report is prepared under TWP section 1.9.3; concise minutes are
   kept (Antitrust Guidelines C.3).
7. **Follow-up** -- agreed work feeds the work item and the deliverable
   pipeline; contributions needing more work come back as revisions.

## Preparing the meeting (TWP 1.5)

The Chair and/or Secretary prepares each meeting with particular attention to
transparency (Antitrust Guidelines C.3). For a delegate that means:

- reading the invitation, the agenda and the contribution deadline;
- registering early -- registration closes before the meeting;
- checking which of your contributions were accepted and in which agenda
  item;
- preparing speaking notes, and for a draft deliverable the revision itself.

## Deciding in the meeting

From the TWP, voting in a meeting works like this:

- the Chair states a clear definition of the proposal or candidate list before
  opening the vote;
- only **registered and present** delegates of Full and Associate members may
  vote, physically or remotely;
- **one vote per member organisation** and **one per Academic, Corporate or
  Public Group**;
- electronic votes may be changed until the vote is closed;
- Counsellors' opinions should be noted;
- **voting by proxy is not permitted**;
- **there are no quorum requirements**;
- **splitting of the vote is not permitted**;
- the Chair evaluates and communicates the result, which is recorded as a
  decision in the meeting report.

Threshold: **71 % of votes cast**; if that fails, the result is recalculated on
Full members' votes alone and may still pass. Abstentions and non-votes are
excluded.

## Consensus between meetings

The TWP provides a remote consensus tool for decisions between meetings:

- the proposal and a comment/objection period are disseminated;
- only subscribed delegates participate;
- the period is **at least seven calendar days**;
- objections may be cleared before closing;
- the Chair ratifies the decision at the end, disseminates it within seven
  days and records it as a consensus decision.

Correspondence voting in a technical group runs for **at least two calendar
days**, with the proposal circulated at least **seven days** ahead.

## Working with the portal

Browsing is read-only and needs no authentication:

```bash
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool tc list                      # committees
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool tc get STQ                   # committee + sub-committees
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool meetings list --tc STQ       # upcoming meetings
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool meetings list --tc STQ --all # including past
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool meetings find "STQ#82" --tc STQ -r
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool meetings get 82821 --tc STQ  # details
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool documents list -m 82821 -t stq
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool documents list -m 82821 -t stq --type Draft
```

Registration needs authentication:

```bash
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool register status 82821
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool register signup 82821
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool register whoami
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool register roles 82821
```

Downloading the documents of a meeting needs authentication and a logged-in
session:

```bash
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool documents download 339450
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool etsi-portal-tool download meeting -m 82821 -t stq
```

See `etsi-portal-tool` for the full command surface, the session handling and
the authentication options.

## Cross-references

- [tdocs.md](tdocs.md) -- contribution types, fields and revisions
- [work-items.md](work-items.md) -- the work a meeting is asked to advance
- [approval.md](approval.md) -- what happens after the meeting
- `etsi-directives` -- Ch 11 (TWP), Ch 5 (antitrust), Ch 6 (codes of conduct)
