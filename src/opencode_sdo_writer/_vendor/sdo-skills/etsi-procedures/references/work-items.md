# ETSI Work Items

The Work Item is the unit of work in ETSI. A group may not approve a final
draft before the Work Item has been adopted, and a Work Item that has made no
progress for a year is stopped.

## Who may propose

At least **four Full and/or Associate members** must support the creation
proposal. If the subject does not fit a single Technical Group, it goes to the
**OCG** for allocation.

## The parameters a group records

The Work Item Description records the Annex K parameters:

- title;
- intended ETSI deliverable type;
- technical scope, including the field of application;
- schedule of tasks;
- the supporting Full/Associate member identities;
- the Rapporteur;
- environmental aspects, user and consumer aspects, labour and workplace
  aspects, specific relevance to SMEs, security and privacy aspects;
- the position of the Work Item in the hierarchical tree of ETSI work.

A **single named Rapporteur** is appointed per Work Item. The Rapporteur is
the prime technical contact and the owner of the maturity milestones.

## Two milestone families

| Family | Milestones | Set by |
|--------|-----------|--------|
| Decision milestones | Work Item adoption, Working Group endorsement, Technical Group endorsement, adoption by the TG / ETSI membership / NSOG / NSBG | the TG or WG |
| Maturity milestones | Early draft, Stable draft, Mature draft (informal, for SReq deliverables), Final draft | the Rapporteur |

The maturity ladder carries an explicit warning: *Early draft* should
discourage any implementation attempt, while *Stable draft* signals that no
major technical changes are expected.

## Lifecycle

```text
Proposal -> WI Description recorded -> TG adopts the WI
    -> Drafting against the maturity milestones
    -> WG endorsement -> TG endorsement
    -> Secretariat submission -> approval route
```

Stopping rules:

- a Work Item **shall be stopped after one year without progress** -- the rule
  is automatic, not discretionary;
- a ceasing body publishes or stops its Work Items and finds a maintainer for
  the deliverables;
- if a deliverable is withdrawn, the Work Item follows.

## Work Items from Standardisation Requests

An SReq from the European Commission produces a **SReq-derived Work Item**
(WISR). The **GoSR coordinates SReqs but does not accept them** -- the
acceptance sits with the National Standardisation Bodies, which trigger the
**SRdAP** route (see [approval.md](approval.md)). An ISG may not handle an
SReq; that work belongs to the SRdAP track.

## Publicly Available Specifications

A **PAS Work Item** produces a **TS or TR only**, and the Rapporteur is
designated by the PAS submitter (Annex Q form).

## From the portal

```bash
# List the open work items of a committee by code or TBID
etsi-portal-tool workitems list --tc STQ
etsi-portal-tool workitems list --tbid 275

# Bind a contribution to a work item
etsi-portal-tool tdoc edit 339463 --wki 78261
```

The work item a contribution belongs to is also visible in the portal as the
"Related WI(s)" list on the contribution.

## Cross-references

- [meetings.md](meetings.md) -- where a Work Item proposal is decided
- [tdocs.md](tdocs.md) -- the contribution that carries a WI proposal
- [approval.md](approval.md) -- the route a deliverable takes after the WI is adopted
- `etsi-directives` -- Ch 11 (Technical Working Procedures), Ch 9 (committee ToR)
