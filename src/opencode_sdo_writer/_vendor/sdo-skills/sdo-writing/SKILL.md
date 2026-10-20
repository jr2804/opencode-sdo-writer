---
name: sdo-writing
description: 'Writing rules for formal standardization documents across ETSI, 3GPP and ITU-T. Use when drafting or revising standards prose, contributions, technical reports, meeting documents, or requirement text; when choosing wording, register, structure or terminology; when checking a draft for genericity, unsupported claims or style violations; or when applying mechanical conventions such as -ize/-ise spelling, hyphenation, number, date and capitalisation rules. Covers prose quality and mechanical correctness, not .docx formatting.'
---

# SDO Writing

Write for the actual context: precise, verifiable, concrete prose that fits
the medium, the task and the reader.

Two rule families live here:

- **Prose quality** -- specificity, fact discipline, anti-genericity, register,
  structure, revision. Detail: `references/prose-quality.md`.
- **Mechanical conventions** -- spelling, hyphens, numbers, dates,
  capitalisation, abbreviations, lists, non-discriminatory language.
  Detail: `references/mechanical-conventions.md` (11-section extract from the
  ITU English Language Style Guide, 2024).

## Precedence

When rules conflict:

1. Truth, safety, accessibility, and platform/legal requirements
2. Explicit user instructions
3. Genre and medium norms (standards documents are formal technical writing)
4. Core rules below
5. Optional heuristics

## Core workflow

1. Identify the medium, audience, reader need, and job of the text.
2. If task-oriented, identify the answer or next action that belongs first.
3. If long-form, decide the through-line and one concrete example, moment,
   or case that can carry real weight.
4. Draft to fit that context, not an abstract idea of "good writing."
5. Cut what sounds generic, ceremonial, over-engineered, or too cleanly
   modular.

## Safety rails

- Do not invent typos. Do not break grammar on purpose. Do not inject
  slang, profanity, fake uncertainty, or staged messiness.
- Do not make text less usable or accessible in the name of style.
- The recurring problem is **regularity and mismatch**, not any one feature.
- In standards documents, prefer straight ASCII quotes and apostrophes.
  Avoid curly quotes, smart apostrophes, and single-character ellipses.

## Document class switch

Classify the target before applying terminology rules:

- **Standards document** (specification, report, Recommendation, Norm): use
  "clause" for internal structure and references.
- **Meeting document** (contribution, submission, TDoc, TD): "section" is
  acceptable when aligned with SDO convention and the active template.

## Core rules (prose quality)

Full text and the review checks: `references/prose-quality.md`.

| # | Rule | Core instruction |
| --- | --- | --- |
| 1 | Anchor to context | Fix what the text is, who it is for, and what answer it owes the reader before drafting. |
| 2 | Fit the medium | Structure is expected in standards documents: headings, lists, tables, equations. |
| 3 | Prefer specificity | Every substantial paragraph carries one concrete anchor: a proper noun, a number, a quote, a named decision, a checkable detail. |
| 4 | Earned specificity | Fewer verified facts beat many guessed ones. Attribute, soften or cut what you cannot verify. |
| 5 | Plain words | Repeat the ordinary word; prefer `latency dropped` over `a reduction in latency was observed`. |
| 6 | Cohere by reference | Use pronouns and continued reference; signpost openers must earn their place. |
| 7 | Do not perform | No keynote cadence, mission statements, applause-line endings or ceremonial wrap-ups. |
| 8 | Calibrate stance | Standards text aims at neutrality; state a recommendation only when the document asks for one and evidence supports it. |
| 9 | Show before generalizing | Observation first, then where it appeared, then the constraint, then the failure, then the meaning. |
| 10 | Watch regularity | Three or more repetitions of the same rhetorical move means rewrite at least one. |
| 11 | Let the thought develop | Long pieces should not read as pre-solved; a concrete example beats an artificial aside. |
| 12 | Choose structure consciously | Task pages and procedures favour predictable structure; contributions and reports favour a through-line. |
| 13 | No catalog prose | If paragraphs are names and labels, or each maps to one topic, restructure around one change and its consequences. |
| 14 | Revise by cutting | Re-read as a first-time reader; cut anything that is auditioning. Most edits shorten the text. |

## Mechanical quick reference

SDO-agnostic; the per-SDO drafting skill wins on spelling variant.

| Category | Rule |
|----------|------|
| **Spelling** | UK Oxford spelling; prefer -ize (organize, standardize); use -ise only where removing -ise does not leave a recognizable English word or Latin root (e.g., surprise, comprise, advise, exercise). Some SDOs (e.g., ETSI) use -ise throughout; defer to the per-SDO drafting skill when it specifies a different convention. |
| **telecommunication** | Noun: "telecommunications"; Adjective: "telecommunication" |
| **ICT** | Full form: "information and communication technology" (NOT communications); adjective: "ICT" only |
| **Hyphens** | Minimum use; non-, self-, quasi-, ex- always hyphenated; cyber and tele not hyphenated; e- always hyphenated |
| **Numbers** | Spell out 0-9; figures for >=10, measurements, money, dates; use spaces not commas in large numbers |
| **Dates** | 17 January 1958; time 24h: 2100 hours; time 12h: 9 a.m., 1.15 p.m. |
| **Ranges** | "from ... to ..." or "13 360-13 410 kHz" -- never mix |
| **Decimals** | Precede with zero: 0.3; "per cent" in text, "%" in tables |
| **Capitalization** | General = lower case; specific reference with number = initial caps; "if in doubt, lower case" |
| **Cross-references** | Use "clause" (not "section") for internal references in standards; "section" may be used in meeting documents where the template allows it |
| **Abbreviations** | Spell out on first use; no "the" before org abbreviations (ITU, not the ITU) |
| **Lists** | Format A (items < 1 sentence): lower case, full stop only on last item; Format B (longer items): semicolons between items, full stop on last; Format C (each item >= 1 sentence): capitals, full stops on all. Consistency within document; "etc." never with "e.g."/"including" |
| **Gender** | Use "chair" not "chairman"; "workforce" not "manpower"; avoid masculine-only pronouns |
| **Disability** | People-first: "persons with disabilities"; "wheelchair user" not "wheelchair-bound" |

## Cross-references

- `references/prose-quality.md` -- the 14 core rules in full, the ten review
  checks, and the before/after correction table
- `references/mechanical-conventions.md` -- the 11-section ITU ELSG extract:
  written style, spelling, hyphens, punctuation, adjectives, numbers, proper
  names, capitalization, abbreviations, layout, non-discriminatory language
- `sdo-docx` -- .docx style rules and safe editing operations
- `sdo-drafting` -- deliverable skeletons, requirements language, numbering,
  and the per-SDO overrides (ETSI, 3GPP, ITU-T) in its reference sub-trees
