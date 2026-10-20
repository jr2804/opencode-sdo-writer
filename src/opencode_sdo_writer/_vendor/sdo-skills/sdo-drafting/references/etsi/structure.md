# ETSI deliverable structure and drafting rules

Applies to ETSI deliverables (TS, ES, EN, TR, EG, SR, GS).
Style names: `etsi/style-map.md`. Full EDR extract: `etsi/drafting-rules.md`.

## Assets

ETSI provides deliverable skeletons (Word templates) for each type via the
editHelp! website at <https://portal.etsi.org/edithelp/home.asp>. These contain
all required styles and structural elements. Always start from the appropriate
skeleton for the deliverable type being drafted. Do not add new styles or
modify existing ones.

### Downloaded skeletons (`assets/`)

| File | Deliverable type | Notes |
|------|-----------------|-------|
| `ETSI_ES_skeleton.docx` | ES (ETSI Standard) | |
| `ETSI_EN_skeleton.docx` | EN (European Norm) | |
| `ETSI_TS_skeleton.docx` | TS (Technical Specification) | |
| `ETSI_TR_skeleton.docx` | TR (Technical Report) | |
| `ETSI_EG_skeleton.docx` | EG (ETSI Guide) | |
| `ETSI_SR_skeleton.docx` | SR (Special Report) | |
| `ETSI_GS_skeleton.docx` | GS (Group Specification) | |
| `ETSI_GR_skeleton.docx` | GR (Group Report) | |
| `ETSI_hEN_Directive_skeleton.docx` | hEN (Harmonised EN under Directive) | |
| `ETSI_hEN_Regulation_skeleton.docx` | hEN (Harmonised EN under Regulation) | |

Upstream refresh URL:

- `https://portal.etsi.org/Services/editHelp/Standards-development/Drafting/Skeletons`

### Template selection rule

- **Always start from the skeleton** matching the target deliverable type.
- If unsure which type applies, ask the user.
- The skeleton contains all required styles; do not create new styles or
  rename existing ones.

______________________________________________________________________

## ETSI deliverable structure

Per the ETSI Drafting Rules (EDR), an ETSI deliverable follows this order:

**Unnumbered preliminary elements (informative):**

- Cover page (title, deliverable type, version, date, logos)
- Contents (generated)
- Intellectual Property Rights (provided by Secretariat -- do not modify)
- Foreword (TC that prepared it; optional: relationship to other docs,
  superseded docs, technical changes from previous version)
- Transposition table (EN only -- provided by Secretariat)
- Modal verbs terminology (provided by Secretariat -- do not modify)
- Executive summary (optional)
- Introduction (optional)

**Numbered core:**

1. Scope
2. References (2.1 Normative, 2.2 Informative)
3. Definitions of terms, abbreviations and symbols
   (3.1 Terms, 3.2 Symbols, 3.3 Abbreviations)
   4+ Technical content

**Supplementary:**

- Annex A, B, C... (normative): title -- integral part of the deliverable
- Annex (continued lettering) (informative): title -- non-integral
- Bibliography (optional)
- Change history (required for EN HS; optional otherwise)
- History (provided by Secretariat)

______________________________________________________________________

## Key drafting rules

### Requirements language

| Verbal form | Meaning |
|-------------|---------|
| **shall** | Mandatory requirement |
| **shall not** | Prohibition |
| **should** | Recommendation |
| **should not** | Recommendation against |
| **may** | Permission |
| **need not** | No requirement |
| **can** | Possibility or capability (informative only) |
| **cannot** | Impossibility (informative only) |

Each requirement should be: necessary, unambiguous, complete, precise,
well-structured, consistent, and testable.

### Clause numbering

- Arabic numerals from 1 (for Scope)
- Up to 6 heading levels (e.g. 5.1, 5.1.1, 5.1.1.1, ...)
- If subdivisions exist, at least two at each level
- Never mix numbered and unnumbered subdivisions at the same level
- To insert between existing clauses: use alphanumeric (clause "8a")
- To delete: mark as "Void" to preserve numbering
- Automatic numbering may be used with proper ETSI styles

### Scope

Worded as statements of fact:

- "The present document specifies..." / "establishes..." / "gives guidelines for..."
- "The present document is applicable to..."

### References

- Normative references (2.1): must be publicly available in English
- Prefer specific (dated) references
- Non-specific (undated) allowed only if referring TC controls the document
- References to 3GPP deliverables: replace with ETSI equivalents
  (e.g. 3GPP TS 23.040 -> ETSI TS 123 040)

### Figures and tables

- Numbered with Arabic numerals from 1
- Title below figure: "Figure N: title"
- Title above table: "Table N: title"
- Notes within the figure/table frame

### ETSI-specific figure paragraph rules (mandatory)

Apply these rules for all ETSI deliverables (TS, ES, EN, TR, EG, SR, GS):

- Figure layout in Word must be **In line with text**. Floating layouts
  (Square, Tight, Through, Top and Bottom, Behind Text, In Front of Text)
  are forbidden.
- A single nominal figure may contain multiple images/pictures inside the
  same figure paragraph.
- The paragraph containing the figure(s) must use style `FL`
  (`figure-para`).
- After the last image in the figure paragraph, end the paragraph before
  adding the caption (equivalent to pressing Enter). Do not use a soft line
  break (`Shift+Enter`) between image content and caption.
- Place the caption in a separate paragraph with style `TF`
  (`figure-caption`).

### Notes

- Integrated in text: "NOTE: " or "NOTE N: " for multiple
- Notes shall NOT contain requirements (except notes to tables/figures)
- Examples: "EXAMPLE: " or "EXAMPLE N: "
- Avoid footnotes; if used, shall not contain requirements

### Neutrality

Do not promote or endorse services, products, or technologies of one
company over another. If only one product/technology is available and
needed, follow the rules in EDR clause 4 (copyright provisions).

______________________________________________________________________
