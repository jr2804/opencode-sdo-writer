---
name: itut-reference
description: 'ITU-T organisation, roles and terminology, plus the structure, approval and amendment of ITU-T Recommendations. Use when the agent needs to know how ITU-T works (study groups, working parties, rapporteurs, Questions, WTSA/TSAG/TSB, meeting procedures), how a Recommendation is structured (clause order, annex conventions, terms, numbering), how it is approved (TAP/AAP), how amendments and corrigenda are handled, or how ITU-T | ISO/IEC common text works. Sources: Rec. ITU-T A.1 (09/2019) + Rules for presentation of ITU-T | ISO/IEC common text (2014).'
---

# ITU-T Reference

Two things in one: **how ITU-T works** and **what a Recommendation looks
like**. Sources: Rec. ITU-T A.1 (09/2019) and the Rules for presentation of
ITU-T | ISO/IEC common text (2014).

## Organisation

| Body | Role |
|------|------|
| **WTSA** (World Telecommunication Standardization Assembly) | Meets every 4 years; establishes study topics and mandates |
| **TSAG** (Telecommunication Standardization Advisory Group) | Advises on priorities, coordination, work programme between WTSAs |
| **TSB** (Telecommunication Standardization Bureau) | Secretariat: circulates documents, organizes meetings, publishes Recommendations |
| **Study Groups** (SG) | Core technical bodies; approve Recommendations; manage work programmes |
| **Working Parties** (WP) | Subsets of study groups handling specific Questions or spec maintenance |
| **Rapporteur Groups** | Appointed experts coordinating detailed study of individual Questions |
| **Focus Groups** (FG) | Forward-looking; non-member participation; do not write Recommendations |
| **Joint Coordination Activities** (JCA) | Cross-study-group coordination; do not perform technical studies |
| **Intersector Rapporteur Groups** (IRG) | Coordinate between ITU sectors (ITU-T, ITU-R, ITU-D) |

## Roles

| Role | Responsibilities |
|------|-----------------|
| **Study Group Chairman** | Establishes work structure, selects WP chairmen, directs meetings, promotion |
| **Rapporteur** | Coordinates detailed study of a Question; holds rapporteur group meetings; submits progress reports and draft Recommendations as TDs |
| **Editor** | Assists rapporteur in preparing text of draft Recommendations |
| **Associate Rapporteur** | Assists rapporteur generally or with a particular study area |
| **Liaison Rapporteur** | Ensures liaison with other groups by attending meetings or correspondence |

## Key terminology

| Term | Definition |
|------|-----------|
| **Question** | Description of an area of work to be studied, normally leading to new or revised Recommendations |
| **Work item** | Assigned piece of work identifiable with a Question |
| **Work programme** | List of work items owned by a study group |
| **Recommendation** | The normative output; approved via TAP or AAP |
| **Amendment** | Changes or additions to an already published Recommendation |
| **Corrigendum** | Corrections to a published Recommendation (same approval as amendment) |
| **Erratum** | Correction of publication/editorial errors; published by TSB with Chairman concurrence |
| **Annex** | Integral material necessary for completeness; same approval as the Recommendation |
| **Appendix** | Supplementary material not essential for completeness; agreed by study group only |
| **Normative reference** | External document whose provisions, through reference, become provisions of the referring document |
| **Clause** | Single-digit or multiple-digit numbered text passages |

## Meeting procedures (summary)

- Meetings require TSB Director approval
- Timetable published at least 1 year in advance
- Collective letter (agenda + work plan) sent ~2 months before meeting
- Participants register at least 1 month before
- Meeting may be cancelled if insufficient contributions received
- IPR declaration is requested at each meeting
- Rapporteur meetings: convening letter >= 2 months before; report as TD to parent group

Details: [references/a1-working-methods.md](references/a1-working-methods.md).

## Document types by lifecycle stage

| Document type | Meaning | Approval |
|---------------|---------|----------|
| **Recommendation** | Normative output of a study group | TAP or AAP |
| **Amendment** | Changes/additions to published Recommendation | Same approval as the Recommendation |
| **Corrigendum** | Corrections to published Recommendation | Same approval as amendment |
| **Erratum** | Publication/editorial error fix | Published by TSB with Chairman concurrence (no SG approval) |
| **Annex** (integral) | Material necessary for completeness | Same approval as Recommendation |
| **Appendix** (non-integral) | Supplementary, not essential | Agreed by study group (not full approval) |

## Recommendation clause structure

Per the Rules for presentation of ITU-T | ISO/IEC common text:

| Clause | Element | Content |
|--------|---------|---------|
| *(preliminary)* | Cover page, Contents, Foreword, Introduction | Roman numeral pages |
| 1 | **Scope** | Defines subject and limits; no requirements |
| 2 | **Normative references** | Documents whose provisions are referenced normatively |
| 3 | **Definitions** *(optional)* | Terms defined for this Recommendation. Subdivided into 3.1 "Terms defined elsewhere" and 3.2 "Terms defined in this Recommendation" (if both are used). |
| 4 | **Abbreviations** *(optional)* | All abbreviations used in the text |
| 5 | **Conventions** *(optional)* | Any particular notation used |
| 6+ | **Text** | Body of the Recommendation |
| Annex A+ | **Integral annexes** | Normative material (same approval as Recommendation) |
| Annex (continues) | **Non-integral annexes** | Informative/supplementary (SG agreement, not full approval) |
| *(last, optional)* | **Bibliography** | Informative references not cited normatively; heading style `Appendix_No & title` with page break before |
| *(last)* | **Index** *(optional)* | |

### Canonical skeleton template

For new Recommendation drafting and for checking published Word style
definitions, use the local skeleton first:

- `assets/itu-t-recommendation-skeleton.docx`

Upstream source URL (for refresh):

- `https://www.itu.int/en/ITU-T/studygroups/Documents/Doc-ITUT-Recs-Skelet.docx`

### Subdivision numbering

- Digits separated by periods: 1, 1.1, 1.1.1
- No trailing period after single number
- Do not create subclause 1.1 unless 1.2 also exists

Details: [references/terms-and-numbering.md](references/terms-and-numbering.md)
(term formatting in clause 3, subdivision numbering, the Bibliography
clause), [references/rules-recommendation-structure.md](references/rules-recommendation-structure.md)
(full Rules extract, including the ITU-T | ISO/IEC common text conventions).

## Reference files

- [references/a1-working-methods.md](references/a1-working-methods.md) -- detailed extract from Rec. ITU-T A.1: working methods, meeting and rapporteur-group procedures
- [references/rules-recommendation-structure.md](references/rules-recommendation-structure.md) -- detailed extract from the Rules for presentation: clauses, lists, figures, tables, notes, normative words, annexes, common text
- [references/terms-and-numbering.md](references/terms-and-numbering.md) -- term paragraphs in clause 3, subdivision numbering, the Bibliography clause

## Cross-references

- `itut-contributions` -- contribution submission, TDocs, liaison statements
- `sdo-drafting` -- ITU-T contribution and Recommendation templates, style names, structure rules
- `sdo-ipr` -- patent policy, IPR disclosure, licensing declarations
- `sdo-docx` -- formatting rules and safe DOCX operations
- `sdo-project-setup` -- project bootstrap workflow
