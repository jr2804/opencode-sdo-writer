# XPath Patterns

Use style-based positional XPath for robust selection. Replace concrete
style IDs with those from the per-SDO drafting skill.

- Heading N-th first run:
  `(//w:p[w:pPr/w:pStyle/@w:val='<heading-style>'])[N]/w:r[1]`
- Enumeration N-th first run:
  `(//w:p[w:pPr/w:pStyle/@w:val='<enum-style>'])[N]/w:r[1]`
- Note N-th first run:
  `(//w:p[w:pPr/w:pStyle/@w:val='<note-style>'])[N]/w:r[1]`
- Content-based first run:
  `//w:p[starts-with(normalize-space(.),'Target text')]/w:r[1]`

**Common concrete examples (3GPP/ETSI):**

- `(//w:p[w:pPr/w:pStyle/@w:val='Heading1'])[1]/w:r[1]`
- `(//w:p[w:pPr/w:pStyle/@w:val='B1'])[3]/w:r[1]`
- `(//w:p[w:pPr/w:pStyle/@w:val='NO'])[2]/w:r[1]`

**Common concrete examples (ITU-T):**

- `(//w:p[w:pPr/w:pStyle/@w:val='Heading1'])[1]/w:r[1]`
- `(//w:p[w:pPr/w:pStyle/@w:val='enumlev1'])[3]/w:r[1]`
- `(//w:p[w:pPr/w:pStyle/@w:val='Note'])[2]/w:r[1]`
