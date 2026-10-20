---
name: sdo-drafting
description: 'Deliverable drafting for ETSI, 3GPP and ITU-T standards documents: skeleton and template selection, deliverable structure, clause ordering, per-SDO style-name maps, ITU-T equations, terms and numbering, 3GPP TDoc metadata and revision workflow. Use when creating or editing a standards .docx (TS/ES/EN/TR/EG/SR/GS, TDoc, change request, contribution, Liaison Statement, Recommendation), when picking a skeleton, when mapping abstract style names to concrete Word styles, or when a document needs SDO-specific structure rules.'
---

# SDO Drafting

One skill, three SDOs. The body below is SDO-neutral; every SDO-specific
rule lives in `references/<sdo>/`.

## Workflow

1. **Identify SDO and document type.** If the user has not said, ask.
   - ETSI deliverables: TS, ES, EN, TR, EG, SR, GS, GR, hEN.
   - 3GPP: TDoc (meeting submission), CR (change request), TS/TR (specification).
   - ITU-T: contribution (C- or TD-series), Liaison Statement, Recommendation.
2. **Start from the right template** (see Assets). Never edit a template in
   place -- copy it into the project (`ref/`) and work on the copy. Never add,
   rename or override template styles.
3. **Read the per-SDO reference** for structure, style names and numbering
   before writing content.
4. **Delegate formatting and editing** to `sdo-docx` (styles, headings,
   notes, enumerations, tables, figures, equations, citations; officecli
   operations, field codes, bookmarks, tracked changes).
5. **Delegate prose** to `sdo-writing` (mechanical conventions and prose
   quality).
6. **Delegate project scaffolding** to `sdo-project-setup` (project layout,
   `AGENTS.md`, `PLAN.md`, document properties).

## Assets

| SDO | Files | Notes |
|---|---|---|
| ETSI | ETSI deliverable skeletons in `assets/etsi/` -- one `.docx` per deliverable type (TS, ES, EN, TR, EG, SR, GS, GR, hEN Directive, hEN Regulation), file names of the form `ETSI_<TYPE>_skeleton.docx` | Always start from the skeleton matching the deliverable type; the skeleton carries all required styles |
| 3GPP | `assets/3gpp/Tdoc_Template.docx` | User-crafted TDoc template carrying the 3GPP styles (`B1`, `B2`, `NO`, `NW`, `TH`, `TAH`, `TF`, `EX`, `PL`); not tied to an official release cycle |
| ITU-T | `assets/itut/template.docx`, `assets/itut/itu-t-sg12-contribution-template.docx`, `assets/itut/itu-t-sg12-liaison-statement-template.docx` | Contribution and Liaison Statement templates; the Recommendation skeleton stays with `itut-reference/assets/itu-t-recommendation-skeleton.docx` |

Upstream refresh for the ETSI skeletons:
<https://portal.etsi.org/Services/editHelp/Standards-development/Drafting/Skeletons>

## Per-SDO references

| SDO | Structure and conventions | Style names | Additional |
|---|---|---|---|
| ETSI | `references/etsi/structure.md` | `references/etsi/style-map.md` | `references/etsi/drafting-rules.md` (ETSI Drafting Rules extract) |
| 3GPP | `references/3gpp/tdoc.md` | `references/3gpp/style-map.md` | `references/3gpp/frontmatter.md`, `references/3gpp/template-substitution.md`, `references/3gpp/revision-workflow.md` |
| ITU-T | `references/itut/structure.md` | `references/itut/style-map.md` | `references/itut/equations.md`, `references/itut/terms.md`, `references/itut/numbering.md` |

## Rules that hold everywhere

- Template styles are the single source of truth: apply formatting through
  named styles only, never direct formatting.
- Numbers, captions and cross-references must be update-safe -- SEQ fields
  and bookmarks, never hard-coded numbers (`sdo-docx`).
- Use non-breaking spaces for number+unit and Figure/Table+number.
- Use real tab runs (`<w:tab/>`), never spaces, for structural tabs.
- Requirements wording follows the SDO's modal verbs (ETSI: shall / should /
  may) and is checked against the SDO's drafting rules reference.
- Deliverables keep the SDO's element order (unnumbered preliminary
  elements, then numbered clauses, then annexes) -- see the per-SDO reference.
- ITU-T deviates from the generic rules in three places: equation structure
  (`references/itut/equations.md`), term paragraphs in clause 3
  (`references/itut/terms.md`) and per-clause table/figure counters
  (`references/itut/numbering.md`). Read them before editing an ITU-T file.

## Cross-references

- `sdo-docx` -- formatting conventions and safe editing operations
- `sdo-writing` -- mechanical conventions and prose quality
- `sdo-project-setup` -- project layout, metadata, document properties
- `etsi-governance`, `etsi-directives` -- ETSI organisation and rules
- `3gpp-tdocs`, `3gpp-change-request` -- 3GPP submission and CR workflow
- `itut-contributions`, `itut-reference` -- ITU-T contribution and
  Recommendation rules
