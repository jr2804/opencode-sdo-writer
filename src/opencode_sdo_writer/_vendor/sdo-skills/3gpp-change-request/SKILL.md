---
name: 3gpp-change-request
description: Change Request procedure, workflow, status tracking, CR database, and step-by-step instructions. Use when working with 3GPP Change Requests to modify specifications, understanding CR lifecycle, or querying CR status.
  Use when the user asks for the CR number format, a CR cover sheet, the CR
  submission checklist, CR status codes, CR categories (F / A / TEI), mirror
  CRs, work item codes, the CR databases, or how a CR is drafted, agreed and
  approved.
---

# 3GPP Change Requests

> **Quick Start**: For workflow overview and submission checklist, see
> [references/workflow.md](references/workflow.md); for the number format, status
> table, document structure and databases, see
> [references/cr-format.md](references/cr-format.md); for the checklist, pitfalls
> and best practices, see
> [references/cr-checklist.md](references/cr-checklist.md).

## Overview

Change Requests (CRs) are documents submitted to 3GPP Working Groups to create revised versions of specifications. They represent the formal mechanism for modifying 3GPP specs after initial approval.

## What is a CR?

A CR is a **temporary document** (tdoc) to a meeting which specifies in precise detail changes to be made to a specification. It consists of:

- **CR Cover Sheet**: Describes why a change is needed and summarizes how the change is made
- **Attached Parts of Spec**: Word™ "Track Changes" (revision marks) identifying affected sections
- **Summary of Changes**: Brief explanation of the proposed modification

## Why Changes Are Needed

Three main reasons for creating a CR:

1. **Add a new feature** to a Release still under development
2. **Correct / clarify / enhance** an existing feature in a Release still under development
3. **Correct an error** in a spec which is functionally frozen

## CR Number Format

```text
<specnumber_no_dot>*_CR*<4-character_CR_number>*[r*<revision_number>*]
```

Component breakdown, examples, document sections and the file naming
convention: `references/cr-format.md`.

## CR Categories

Three categories: **F** (corrective), **A** (mirror) and **TEI** (technical
enhancement or improvement). A mirror CR applies the same change to another
Release of the same spec. Definitions: `references/cr-format.md`.

## Mirror CRs

A spec maintained in several parallel Releases needs one mirror CR per
Release, all sharing the same Work Item code. Concepts and checklist:
`references/cr-checklist.md`.

## Change Request Workflow

1. **Draft CR**
   Member organization creates CR document
2. **Submit to WG**
   WG discusses and agrees CR is valid
3. **WG Presents to TSG**
   WG presents CR at TSG plenary for approval
4. **TSG Approval**
   TSG approves CR (becomes decision)
5. **MCC Incorporates**
   MCC incorporates CR into new spec version
6. **Publish**
   New spec version becomes available

Detailed steps, status transitions and the quick checklist:
`references/workflow.md`.

## Reference Files

- `references/cr-format.md` - CR number format, components and examples, CR
  status table, CR categories, document sections, revision history, file naming
  convention, work item codes, CR databases, resources
- `references/cr-checklist.md` - CR submission checklist, common pitfalls, best
  practices, mirror CR and editorial concepts
- `references/workflow.md` - CR lifecycle, six-step submission and approval
  process, status transitions, quick checklist

## Cross-References

- `3gpp-basics` - 3GPP organization and structure
- `3gpp-working-groups` - Working Group responsibility for specs
- `3gpp-tdocs` - CRs as meeting documents (tdocs)
- `3gpp-releases` - Understanding Release structure
- `3gpp-portal-authentication` - Some CR documents may require EOL access
- `3gpp-specifications` - Spec numbering and structure
- `sdo-drafting` - TDoc template, frontmatter and revision workflow
