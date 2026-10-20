# Enumerations

## Critical constraints

- **Never use the MS Word built-in list feature** (automatic numbered lists
  or bullets). When using revision marks, automatic lists cause formatting
  inconsistencies and can break references during editing.
- **Avoid numbered lists.** Prefer en-dash enumerations. If numbered items
  ("1.", "2.") or lettered items ("a)", "b)") are necessary, use manual
  labelling -- never automatic list numbering.

## Style-based hierarchy

Use hierarchical styles for enumeration levels, not manual indentation or
bullets:

- First level: `enum-1` (→ concrete style)
- Second level: `enum-2`
- Third level: `enum-3` (if needed)

## Formatting rules

- Default bullet character: en-dash (`&#8211;`).
- Format: `<bullet>\t<text>` -- bullet, real tab run, then text (never spaces
  for indentation).
- Insert a real `<w:tab/>` run element after the bullet character; do not
  use space characters (see `sdo-docx` for officecli patterns).
- Do not apply manual bold, font-size, or indentation overrides.
- Manual formatting overrides can cause inconsistencies when regenerating
  or bulk-updating enumerations.

## XPath access (for officecli raw-set)

To target enumeration items programmatically by style:

```xpath
(//w:p[w:pPr/w:pStyle/@w:val='<enum-1-style>'])[N]/w:r[1]
(//w:p[w:pPr/w:pStyle/@w:val='<enum-2-style>'])[N]/w:r[1]
```

Replace `<enum-1-style>` with the concrete style ID from the SDO drafting
skill.

## Style mapping

| Abstract | Concrete (per SDO drafting skill) |
|----------|-----------------------------------|
| `enum-1` | SDO-specific style for first-level enumeration |
| `enum-2` | SDO-specific style for second-level enumeration |
| `enum-3` | SDO-specific style for third-level enumeration (if used) |
