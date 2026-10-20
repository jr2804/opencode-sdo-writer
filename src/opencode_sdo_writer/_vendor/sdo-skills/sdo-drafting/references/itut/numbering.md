# ITU-T numbering: bibliography, tables and figures

Bibliography clause rules and the per-clause SEQ counters for tables and
figures (differs from the global counters in `sdo-docx`).

## Bibliography clause

The **Bibliography** is an optional, non-normative clause that lists
informative references. It appears as the **very last element** of a
Recommendation, after all integral and non-integral annexes.

### Three mandatory rules — never drop any of them

1. **Heading style** — Use style `Appendix_No & title` (abstract:
   `bibliography-heading`), **not** `Heading 1`. The Bibliography is a
   non-integral appendix in ITU-T, so it shares the appendix heading style.
   Write the heading text as `Bibliography` without a number prefix.

2. **Page break before heading** — Insert a page break immediately before
   the `Bibliography` heading paragraph. Apply it as a paragraph property
   (`w:pageBreakBefore` = `true`, or `pageBreakBefore: true` in the
   officecli `set` command) on the heading paragraph itself — **do not**
   insert a separate empty paragraph with a manual page break.

   ```json
   { "command": "set",
     "path": "/body/p[<bibliography-heading-ordinal>]",
     "props": { "style": "Appendix_No & title",
                "pageBreakBefore": true,
                "text": "Bibliography" } }
   ```

3. **Entry style** — Each bibliography entry uses style `References`
   (abstract: `reference-entry`) — the **same** style as normative
   reference entries in clause 2. Do not use `Body Text`, `Normal`, or
   any other style for bibliography entries.

### Entry format

Format identical to normative references:

```text
[N]\t<citation text>
```

- Square-bracket-wrapped `{SEQ Ref \* ARABIC}` field (no hard-coded number).
- Real `<w:tab/>` run between the bracket and the citation text.
- Bookmark `ref_<short_name>` around the sequence field only.
- Style: `References` on every entry paragraph.

### Common agent failure modes

| Mistake | Correct behaviour |
|---------|-------------------|
| Using `Heading 1` for the Bibliography heading | Use `Appendix_No & title` |
| Omitting the page break before Bibliography | Set `pageBreakBefore: true` on the heading paragraph |
| Styling entries with `Body Text` or `Normal` | Apply `References` style to every entry |
| Hard-coding `[1]`, `[2]` as plain text | Use `{SEQ Ref \* ARABIC}` field with bookmark |

______________________________________________________________________

## Table and figure numbering (per-clause counters)

ITU-T Recommendations use **per-clause** SEQ field counters for tables
and figures. This differs from the generic `sdo-docx` convention
(global `SEQ Figure` / `SEQ Table`).

### SEQ field naming

| Element | SEQ field name | Bookmark prefix | Caption style ID |
|---------|---------------|-----------------|-------------------|
| Figures | `FIG<N>` where N = clause number | `FIG_` | `FigureNotitle0` (`Figure_No & title`) |
| Tables | `TAB<N>` where N = clause number | `TAB_` | `TableNoTitle` (`Table_No & title`) |

Examples:

- Clause 6 figures: `SEQ FIG6`, bookmarks `FIG_EQUIPMENT_*`
- Clause 8 tables: `SEQ TAB8`, bookmarks `TAB_SETUP_*`

### Caption structure

```text
Figure\u00a0<N>-{SEQ FIG<N>}: caption text
Table\u00a0<N>-{SEQ TAB<N>}: caption text
```

- The clause-number prefix (`6-`) is hardcoded text before the field
- The SEQ field provides the running number within the clause
- A non-breaking space separates "Figure"/"Table" from the number
- The bookmark wraps around the full compound number (`6-1`, `6-2`, etc.)
  — start bookmark before the `6-` run, end bookmark after the field end

### Bookmark naming

Use `FIG_` / `TAB_` prefix followed by a short descriptive name in
UPPER_SNAKE_CASE. Follow the naming scheme already used in the document:

- Look at existing bookmarks in nearby clauses for the naming pattern
- Choose a 1–2 word description that fits the topic
- Examples: `FIG_EQUIPMENT_RRS_SP`, `TAB_SIGNALS_ACCURACYMEASUREMENTS`

### Run-level structure for a correct caption

```text
r[1]   run          "Figure "           (non-breaking space)
       bookmark     (around 6-N)         name="FIG_xxx"
r[2]   run          "6-"
r[3]   fieldChar    begin
r[4]   instrText    " SEQ FIG6 "
r[5]   fieldChar    separate
r[6]   run          "N"                 (field result)
r[7]   fieldChar    end
       bookmarkEnd
r[8]   run          ": caption text"
```

### Cross-references

Body text references use `REF` fields pointing to the bookmark:

```text
{ REF FIG_EQUIPMENT_RRS_SP \h }
{ REF TAB_SIGNALS_ACCURACYMEASUREMENTS \h }
```

### Procedure: fix table/figure numbering in a clause

When asked to "fix table/figure numbers in clause N", follow this workflow:

1. **Analyse**: Scan all figure/table captions in the clause. For each,
   check:

   - Does it have a `SEQ FIG<N>` / `SEQ TAB<N>` field?
   - Does it have a bookmark with `FIG_` / `TAB_` prefix?
   - Is the number hardcoded (no field) or auto-numbered?
   - Are there duplicate numbers?

2. **Add missing SEQ fields**: For captions with hardcoded numbers,
   replace the hardcoded number with `{SEQ FIG<N>}` / `{SEQ TAB<N>}`.

3. **Add missing bookmarks**: For captions without bookmarks, add a
   bookmark around the compound number (`N-M`). Choose a descriptive
   name that fits the naming pattern of existing bookmarks in that
   clause.

4. **Fix duplicate numbers**: If adding SEQ fields changes the sequence
   order, the field results will auto-update. If a figure/table has a
   duplicate hardcoded number, let the SEQ field resolve it — do not
   assign numbers manually.

5. **Check cross-references**: Search the clause body text for `REF`
   fields. Verify each references a bookmark that still exists with
   the correct name. If a hardcoded reference (plain text "Figure 6-3")
   is found, replace it with a `{REF <bookmark> \h}` field.

6. **Rebuild captions**: Use `raw-set` with `--action replace` targeting
   `//w:p[@w14:paraId="PARAID"]` to replace each caption paragraph with
   a correctly structured one. The replacement XML must include:

   - `w:pPr` with the correct style (`FigureNotitle0` / `TableNoTitle`)
   - Bookmark start/end around the number
   - SEQ field (begin/instrText/separate/result/end)
   - Caption text after the field

7. **Refresh fields**: Run `mise x github:iOfficeAI/OfficeCLI -- officecli refresh <doc>` to re-evaluate all
   SEQ and REF fields.

8. **Verify**: Check field results in the raw XML:

   ```bash
   mise x github:iOfficeAI/OfficeCLI -- officecli raw <doc> /document | grep -A1 'fldCharType="separate"'
   ```

### Common pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| Duplicate figure/table numbers | Missing SEQ field, hardcoded number | Add SEQ field; let field auto-resolve |
| Cross-reference shows wrong number | REF bookmark name doesn't match caption bookmark | Update REF instruction to point to correct bookmark |
| Caption shows empty number | `officecli refresh` didn't update the field | Re-run `officecli refresh`; check raw XML for result |
| Bookmark name doesn't match nearby pattern | Newly invented name inconsistent with document | Review existing bookmarks in clause; match the naming scheme |

______________________________________________________________________
