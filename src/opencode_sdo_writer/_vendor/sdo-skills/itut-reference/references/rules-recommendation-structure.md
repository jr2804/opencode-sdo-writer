# ITU-T Recommendation Structure & Common Text Conventions

Extracted from: Rules for presentation of ITU-T | ISO/IEC common text (September 2014)
(based on Rec. ITU-T A.1000)

## Purpose

Establishes presentation rules for documents that are intended to be both
ITU-T Recommendations and ISO/IEC International Standards. Based on the
"Author's guide for drafting ITU-T Recommendations" and ISO/IEC Directives,
Part 2. A template is available from TSB and ITTF.

______________________________________________________________________

## General arrangement of elements

| Element | Numbering | Required? |
|---------|-----------|-----------|
| Cover page | None | Yes |
| Contents | None | Optional |
| Foreword | None | Yes |
| Introduction | None | Optional |
| Title | None | Yes |
| Scope | 1 | Yes |
| Normative references | 2 | Yes (if any) |
| Definitions | 3 | Optional |
| Abbreviations | 4 | Optional (required if abbreviations used) |
| Conventions | 5 | Optional |
| Text of Recommendation | 6 onwards | Yes |
| Integral annexes | A, B, C... | Optional |
| Non-integral annexes | (continues letters) | Optional |
| Index | None | Optional |

Preliminary material (cover page through introduction) uses lowercase roman
numerals. Core text starts on page 1.

______________________________________________________________________

## Subdivision numbering

- Subdivisions numbered with digits separated by periods: 1, 1.1, 1.1.1
- No trailing period after a single number
- Subdivision number on separate line with title
- Do not create a subclause (e.g. 1.1) unless there is at least one further
  subclause at the same level (e.g. 1.2)

______________________________________________________________________

## Lists

Two forms allowed:

**Form 1 -- dashed list:**

```text
- first item;
- second item;
- etc.
```

**Form 2 -- lettered/numbered list:**

```text
a) first item;
b) second item;
c) etc.
```

**Sublists:**

```text
a) first item:
    1) first sub-item;
    2) second sub-item.
b) second item:
    1) first sub-item;
    2) second sub-item.
```

______________________________________________________________________

## Figures

- Each figure must be explicitly referenced in the text.
- Numbered with Arabic numerals, beginning with 1 (independent of clause numbering).
  Exception: for large/complex publications, may use clause-relative numbering
  (e.g. "Figure 4-3" = third figure in clause 4).
- Single figure: "Figure 1".
- **Title below figure**, centred: "Figure x -- title".
- References use uppercase "F": "see Figure 1".
- Title: first letter capitalized; rest lowercase unless special terms.
- Within annexes: numbering restarts, preceded by annex letter (e.g. Figure A.1).

______________________________________________________________________

## Tables

- Each table must be explicitly referenced in the text.
- Numbered with Arabic numerals, beginning with 1 (independent of clause numbering).
  Exception: clause-relative ("Table 4-3") for large publications.
- Single table: "Table 1".
- **Title above table**, centred: "Table x -- title".
- References use uppercase "T": "see Table 1".
- Column headings: first letter capitalized.
- Columns separated by vertical lines if possible; heading separated by
  horizontal line; elements framed.
- Within annexes: numbering restarts, preceded by annex letter.

### Tables spanning pages

- Bottom of first page: "(continued)"
- Top of intermediate pages: "Table x (continued)"
- Top of last page: "Table x (concluded)"
- Column headings repeated on each page.

### Tables wider than page

- Split into sub-tables: intermediate = "Table x (continued)", last = "Table x (concluded)"
- First column in each sub-table carries index number with appended letter
  ("1a", "2a" in first; "1b", "2b" in second; etc.)

______________________________________________________________________

## Equations and formulas

- Written using the "Equation" style in the template.
- Numbered consecutively with Arabic numerals, beginning with 1 (independent
  of clauses). For large publications, may use clause-relative: "(6-1)".
- Number in parentheses, right-aligned (or after equation).
- Within annexes: numbering restarts, preceded by annex letter.

______________________________________________________________________

## Notes

- Information helping understanding; **shall not contain requirements**.
- Placed after the clause, subclause, or paragraph to which they refer.

### Single note

```text
NOTE -- Text of the note.
```

### Multiple notes within same subdivision

```text
NOTE 1 -- First note text.
NOTE 2 -- Second note text.
NOTE 3 -- Third note text.
```

- Alternatively: notes may be numbered continuously throughout the whole
  publication.
- Notes should be indented from the main text margin.

### Notes to tables and figures

- Treated independently from text notes.
- Located within the table frame or immediately above the figure title.
- Always start with "NOTE 1 -- " for first note.
- **May contain requirements** (unlike text notes).

______________________________________________________________________

## Use of words (normative language)

| Word | Meaning |
|------|---------|
| **shall** | Mandatory requirement |
| **shall not** | Prohibition |
| **may** | Optional requirement |
| **need not** | Negative of "may" (NOT "may not" -- avoid "may not") |

______________________________________________________________________

## Integral vs non-integral annexes

### Integral annex

- Forms an integral part of the Recommendation.
- Appears immediately after text.
- Designated A, B, C...
- Title followed by: "(This annex forms an integral part of this
  Recommendation | International Standard.)"
- Numbering within: A.1, A.2, Figure A.1, Table A.1, Equation A-1 (start
  afresh per annex).
- Same approval procedure as the Recommendation itself.

### Non-integral annex

- Does NOT form an integral part.
- Appears after last integral annex (or after text if none).
- Designated continuing the letter sequence from integral annexes.
- Title followed by: "(This annex does not form an integral part of this
  Recommendation | International Standard.)"
- Numbering same pattern as integral annexes.
- Agreement by study group is sufficient (no full approval needed).

______________________________________________________________________

## ITU-T | ISO/IEC common text conventions

### Terminology

- "Common text": text in both an ITU-T Recommendation AND an ISO/IEC
  International Standard developed jointly.
- "Identical Recommendations | International Standards": identical (common) text.
- "Paired Recommendations | International Standards": technically aligned
  but not identical text ("twin text").
- "Twin text": texts developed in close collaboration, technically aligned
  but not identical; differences noted in an annex.

### Self-reference

- In Scope and boilerplate: "this Recommendation | International Standard"
- Elsewhere: use a descriptive capitalized term (e.g. "this Specification",
  "this Protocol Specification", "this Model", "this Framework")

### Dual notation

When referencing an identical Recommendation \| International Standard outside
the text, use ITU-T first: "see Rec. ITU-T X.882 | ISO/IEC 13712-3".

### Internal references

- "in accordance with clause 3"
- "according to 3.1" or "according to clause 3.1"
- "see Annex B"

### Title format

- "Information technology" as introductory element
- Up to three elements, from general to particular
- First letter of each element capitalized; rest lowercase unless special terms

______________________________________________________________________

## Referencing ITU-T Recommendations

### In normative reference list

Format: `Recommendation ITU-T X.613 (1992) | ISO/IEC 10588:1993, Information technology -- Title.`

### Within text

Format: `[ITU-T X.613]` for ITU-T-only references.
For common text: use dual notation as above.
