# Building the schedule in Word — working recipe

Hard-won mechanics for rendering the schedule grid + legend into the report
template via `officecli`. Everything here is verified against
`examples/stq82/example-report.docx` (anonymised) / the meeting-report template.

> The generic officecli mechanics below (atomic batch rollback,
> `colspan` vs `hmerge`, hyperlink placement inside cells, PowerShell/BOM
> and scripting gotchas) are not schedule-specific and would fit
> `sdo-docx-operations`. They are kept here until that skill is updated —
> flag it on the next pass rather than duplicating.

## 1. Work through a single `batch` call

Build the whole grid + legend as one JSON array and run
`officecli batch <file> --input <json>`. One open/save cycle, and — most
importantly — **atomic semantics**.

### Atomic rollback: check the summary, not the per-op flags

A batch is atomic by default: **if any item fails, the whole batch is rolled
back and nothing is applied.** The envelope then reports
`"success": false` and a `summary` with `atomicRolledBack: true`, while
individual `results[]` entries may still read `"success": true`. A run that
"looks fine" op-by-op can therefore leave the document untouched.

After every batch, read:

```json
{ "success": true, "data": { "results": [...], "summary": {
    "total": 89, "executed": 89, "succeeded": 89, "failed": 0,
    "skipped": 0, "atomicRolledBack": true } } }
```

`failed: 0` and envelope `success: true` are the acceptance criteria.
`--best-effort` opts out of rollback (leave it off for document builds).

### Batch item shape

```json
[
  {"command":"set","path":"/body/tbl[2]/tr[3]/tc[3]","props":{"fill":"#E69F00","bold":"true"}},
  {"command":"add","parent":"/body","type":"table",
   "props":{"rows":20,"cols":4,"data":"…"},"after":"/body/p[@paraId=4123DD31]"},
  {"command":"remove","path":"/body/tbl[3]"}
]
```

`props` values are strings; booleans are `"true"`/`"false"`. Command order
is the array order. Tables added later are addressable at their new index
(`tbl[2]`, `tbl[3]`) — resolve indices *inside* the batch, after the
insert that creates them.

## 2. Horizontal merges: `colspan`, never `hmerge`

`hmerge=restart` on a cell silently removes the following cells from the
row; any later `set` against `…/tc[4]` then fails with
`Path not found … Available at …: tc[1]..tc[3]`, which (because of the
atomic rollback) discards the entire batch.

Use **`colspan=N` on the leading cell** instead — it is the modern
gridSpan form and behaves predictably:

```json
{"command":"set","path":"/body/tbl[2]/tr[6]/tc[3]","props":{"colspan":"2","fill":"#999999"}}
```

For a break spanning the day columns, set `colspan` on the first day cell
and drop the following cells' own `set` operations — they no longer exist.

### `colspan` removes the trailing cells — index the survivors

Because `colspan` deletes the cells it absorbs, **any later op addressing
those cells fails the whole batch**. Emit such ops only for cells that exist
after the merges. Keep a map of surviving columns per row and iterate that:

```powershell
$rowCols = @{}
for ($r = 1; $r -le $lastRow; $r++) { $rowCols[$r] = @(1,2,3,4) }
$rowCols[$breakRow1]  = @(1,2,3)     # Tue+Wed merged into tc[3]
$rowCols[$breakRowAll] = @(1,2)      # all day columns merged into tc[2]
```

For vertical merges (`(no meeting)` blocks) `vmerge` is correct:
`vmerge=restart` on the top cell, `vmerge=continue` + `hideMark=true`
**and `text=''`** on each cell below (the seeded text would otherwise
survive inside the merged cell).

## 3. Hyperlinks must live inside a paragraph

A table cell accepts only block-level content. Adding a hyperlink directly
under a cell fails:

> Cannot add 'hyperlink' under /body/tbl[2]/tr[3]/tc[3]: table cells only
> accept paragraphs, tables, or SDTs (block-level content).

Sequence per linked cell (the `data` seed has already put text in `p[1]`):

```json
{"command":"add","parent":"/body/tbl[2]/tr[3]/tc[3]","type":"paragraph","props":{}},
{"command":"add","parent":"/body/tbl[2]/tr[3]/tc[3]/p[2]","type":"hyperlink",
 "props":{"url":"https://portal.etsi.org/ngppapp/ContributionCreation.aspx?primarykeys=<portal-id>",
          "text":"#005"}},
{"command":"remove","path":"/body/tbl[2]/tr[3]/tc[3]/p[1]"},
{"command":"set","path":"/body/tbl[2]/tr[3]/tc[3]/p[1]/r[1]",
 "props":{"underline":"none","color":"#000000","bold":"false","italic":"false"}}
```

Addressing `p[2]` works because the `data` seed created exactly one
paragraph; `add` appends after it. Removing the seed last keeps the cell
non-empty throughout, and after the removal the link paragraph **is** `p[1]`
— which is why the run op above addresses `p[1]/r[1]`.

### The hyperlink run needs its own styling

A hyperlink is inserted with Word's hyperlink character formatting (blue +
underlined). **A cell-level `set --prop underline=none color=…` does not
reach it**: the cell setter touches the paragraph's runs, but the link's run
lives inside `w:hyperlink`. The link cell therefore still reports
`underline=single color=#0000FF` after a cell-level clear.

Fix it by addressing the run directly — officecli exposes it as
`…/tc[C]/p[1]/r[1]` with `isHyperlink=true` and a `_hyperlinkParent`
pointer:

```powershell
$ops.Add(@{command='set'; path="$cell/p[1]/r[1]";
           props=@{underline='none'; color=$textColour; bold='false'; italic='false'}})
```

Alternatively — and where a printable schedule must stay plain — **order the
ops so hyperlinks are created before all styling**, then every later
cell/paragraph set lands on the surviving run. Do both: create links early
*and* style the run explicitly.

## 4. Styles: apply TAH / TAC at PARAGRAPH level

`TAH` (table header) and `TAC` (table data) are the ETSI concrete style IDs
(`etsi-drafting`).

**The `table-cell` element has no `style` property.** A
`set /body/tbl[2]/tr[1]/tc[2] --prop style=TAH` is accepted by the batch
(no error) and **silently does nothing** — the cell keeps `style=Normal`.
Apply the style to the cell's paragraph instead:

```powershell
$ops.Add(@{command='set'; path="/body/tbl[2]/tr[$r]/tc[$c]/p[1]"; props=@{style='TAC'}})
```

- One op per cell; merged rows have fewer cells (see §2).
- Run these ops **last**, after any hyperlink/paragraph insertion, so they
  land on the surviving paragraph.
- Cell-level run properties (`bold=false`, `underline=none`, `color`) *do*
  work — but only on runs directly in the paragraph, not inside hyperlinks
  (§3).

A template may already ship `TAH`/`TAC` as empty stubs, and applying a style
creates a stub if missing; either way a later `add style` with the same id
fails (`Style 'TAH' already exists`). If the template's definitions have
been tuned by hand, **leave them alone** — just apply them.

## 5. Table-level formatting

```json
{"command":"set","path":"/body/tbl[2]","props":{
   "align":"center","width":"100%","layout":"fixed",
   "colWidths":"2300,2300,2300,2300"}}
```

- `align=center` centres the table ("tables must be centred").
- `width=100%` maximises it to the text column (the visual effect of Word's
  *AutoFit Window*).
- `layout=autofit` makes the renderer re-flow columns **by content**, which
  *contradicts* "distribute columns evenly". Use `layout=fixed` + equal
  `colWidths` to hold both the full width and an even grid. Say why in the
  script comment — the next reader will otherwise "fix" it back.
- `colWidths` is in twips, comma-separated, one per column; a `colspan` in
  row 1 (e.g. a full-width caption) does not change the column count.

## 6. Scripting gotchas (PowerShell)

- **Write the script as UTF-8 *with BOM*.** Without it, an en-dash
  (`–`, used in `Monday – 19th October`) is mis-decoded and PowerShell
  aborts with `Unexpected token '19th'`.
- **Do not name helpers `ls`/`sl`/`s`** — they collide with built-in
  aliases (`ls`→`Get-ChildItem`, `sl`→`Set-Location`) and get resolved as
  the alias. Use explicit names (`SetSched`, `SetLeg`).
- **Quote CSS-like paths** (`'/body/tbl[2]/tr[3]/tc[1]'`) — PowerShell
  expands `[` `]`.
- **Quote unit values** in hashtables (`size='10pt'`); bare `10pt` is
  parsed as a command name.
- Do not build strings like `"op $i: $msg"` — `:` after a variable breaks
  parsing; use `("op " + $i + ": " + $msg)`.

## 7. Verify visually, then commit

1. `officecli save` then `officecli close` (release the resident).
2. `officecli validate` — expect `Validation passed: no errors found`.
3. `officecli view <file> screenshot --page N -o pN.png` for each page and
   **look at the images** — colour, merges, alignment and hyperlink
   rendering only surface visually.
4. `officecli query <file> 'p:contains("…")'` to confirm no duplicated
   note paragraphs survived a rebuild (removing `tbl[3]` leaves any
   paragraph that used to follow it).
5. Commit the document and the builder script together, so the grid can be
   regenerated after chair revisions.

## 8. Idempotency

Make the builder re-runnable: `remove` the previous schedule and legend at
the start and rebuild both. Never patch the previous grid incrementally.
Regenerating from the data tables keeps the grid and the legend consistent
with the single source of truth in the script.

Three traps:

1. **Remove tables highest-index-first.** `remove /body/tbl[2]` shifts a
   following legend table down to `tbl[2]`; the subsequent
   `remove /body/tbl[3]` then fails and rolls the batch back.
2. **The document may hold one table or two.** Word silently merges two
   adjacent tables when the paragraph between them is deleted, so a legend
   that was a separate `tbl[3]` can come back as extra rows of `tbl[2]`.
   Query first and emit only the removes that match:

   ```powershell
   $tblList = officecli query $doc 'table' --compact 2>&1 | Out-String
   if ($tblList -match '/body/tbl\[3\]') { $ops.Add(@{command='remove'; path='/body/tbl[3]'}) }
   if ($tblList -match '/body/tbl\[2\]') { $ops.Add(@{command='remove'; path='/body/tbl[2]'}) }
   ```

3. **Own paragraphs survive a table removal.** A note paragraph placed
   after the legend is *not* removed when the legend table is; it accumulates
   on every run. Query and remove it in the same pre-pass:

   ```powershell
   $prev = officecli query $doc 'p:contains("<note text>")' --compact 2>&1 | Out-String
   foreach ($ln in ($prev -split "`n")) {
     if ($ln -match '^(/body/p\[@paraId=[0-9A-F]+\])') { $ops.Add(@{command='remove'; path=$Matches[1]}) }
   }
   ```

   (A bare selector is refused for `remove` — you must resolve the path.)

Also re-read the anchor: a heading the user edited by hand comes back with a
**new `paraId`**. Re-query it (`p:contains("schedule")`) instead of reusing
the old constant.

## 9. ETSI table formatting checklist (default, per etsi-drafting)

> **Superseded for schedule and legend tables (2026-10-14):** the user decided that schedule tables carry **no table counter**. Skip the SEQ/bookmark rows of this checklist for them; the rest still applies. See section 10.

Applied to the schedule (`tbl[2]`) and legend (`tbl[3]`) and verified on
<TC>#<nn>. Each item is a concrete officecli call or XML edit.

| Rule | Source | How |
|---|---|---|
| Caption **above** the table, style `TH`, `Table N: <text>` | sdo-docx-formatting, tables-figures.md | `add --type paragraph --prop style=TH` after the 1.1.1 heading, text `Table` + U+00A0; then `add --type field --prop fieldType=seq --prop name=Table`; then `add --type run` with `: <text>` |
| Caption number is a SEQ field, not typed | tables-figures.md | the field above; instruction `SEQ Table \* ARABIC` |
| Bookmark `tbl_<short>` around `Table N` only | tables-figures.md | officecli's bookmark tool wraps literal text only, so insert `w:bookmarkStart`/`w:bookmarkEnd` in `word/document.xml` (zip Update mode): start **before** the "Table" run, end **after** the field's `end` run. Verify the pair (one start, one end) before saving |
| Header row style `TAH`, repeated on every page | tables-figures.md | paragraph `style=TAH` per header cell; `set /body/tbl[N]/tr[1] --prop header=true` |
| Content cells style `TAC` | etsi-drafting style mapping | paragraph `style=TAC` per cell, after merges |
| Table centred | tables-figures.md | `set /body/tbl[N] --prop align=center` |
| Column width | tables-figures.md says Autofit to contents; the <TC>#<nn> user rule is Autofit to window + distribute evenly | **conflict**: the user's instruction governs the schedule; `width=100%` + `layout=fixed` + equal `colWidths` |
| Table note below, style `TF` | sdo-docx-formatting | `set <para> --prop style=TF`. The ETSI `TF` style is based on `FL`, so it renders bold and centred by definition |
| Header bold | `TAH` in the user's template is `bold=true` | officecli cannot inherit bold (`bold=inherit` is rejected), so header runs get an explicit `bold=true` to match the style |

Known limit: officecli reports explicit run overrides (`bold=false`,
`underline=none`) even when they equal the style, so a later "clear
formatting" pass has to be a rebuild, not a patch.

## 10. Builder architecture and lessons (schedule builder; the agenda body is now Python)

`assets/build-schedule.ps1` renders the schedule from a config file. Use it
as the pattern for any officecli build.

### 10.1 Pipeline

1. **Batch 1 (atomic):** remove every paragraph and table between the heading
   and the end anchor (e.g. `IPR Statement`), then add the caption after the
   heading (style `TH`, plain text, no field).
2. **Batch 2 (atomic):** add the grid, the spacer paragraph and the legend,
   then fill, links, merges and styles. All of it in one batch.
3. **Post-step (XML):** set `tblW` to `type=auto` on the two tables that follow
   the caption (AutoFit to Contents). officecli writes `dxa` only.
4. `officecli validate`.

Two batches give a clean re-run: batch 1 always leaves an empty section, and
batch 2 can address fresh paths (`tbl[2]`, `tbl[3]`).

### 10.2 Ordering inside batch 2 (this order avoids every failure seen so far)

- Base formatting and fills on every cell **that will survive** the merges.
- Document links (add paragraph, add hyperlink, set link run colour, remove the
  seed paragraph last).
- **Merges last.** A `colspan` removes the trailing cells of its row; any op
  addressing them afterwards fails the whole batch.
- Paragraph styles last, on surviving cells only (`p[1]`; `p[2]` for cells that
  keep their seed label).
- Legend after the grid, with its header merge.

### 10.3 Merge rules the builder enforces

- Horizontal merges (`colspan`) must end at the last column. Otherwise the
  cells after the merge shift and later paths point at the wrong cells.
- Vertical merges (`vmerge`) use `restart` on the top cell and `continue` +
  `hideMark` + empty `text` below.
- Continuation cells of a merge take the fill of the restart cell.

### 10.4 Things that bit us

- **A file open in Word blocks officecli** with "The process cannot access the
  file … being used by another process". The lock file is `~$<name>.docx`.
  Ask the user to close the document in Word; do not kill the process (it may
  hold unsaved work). Test on a temp copy meanwhile.
- **Resident sessions:** `officecli view` and `officecli open` can keep a
  resident open; `officecli close <file>` releases it. Batches work without it.
- **Shell-generated paths:** write the `$doc` path explicitly; a `$PSScriptRoot`
  join inside a dot-sourced config resolves relative to the config file.
- **Table counter gone:** after removing the old caption paragraph, its bookmark
  goes too. Don't keep orphaned bookmarks.
- **Stray empty paragraphs** between the schedule and the next heading survive
  a table removal. The clear batch removes them explicitly.
- **Cell-level `style`** is silently ignored; apply paragraph styles.
- **Bold cannot be inherited**: `bold=inherit` is rejected. Set explicit values.
- **Atomic rollback** reports `success: true` on individual items while the
  envelope says `success: false`. Check the envelope and `summary.failed`.

### 10.5 Verifying a rebuild

- Compare cell text, fill and merge flags before and after
  (`officecli get <file> /body/tbl[2] --depth 3`, one line per cell). An
  identical dump means an identical grid.
- Check the hyperlink count and the dark-blue run count.
- Render both pages (`officecli view <file> screenshot --page N`) and look at
  them. Colour and merge problems show only in the image.

### 10.6 PowerShell and officecli traps found while building the agenda

- **PowerShell variables are case-insensitive.** `$w` (loop variable) and `$W`
  (the XML namespace URI) are the same variable. The loop silently replaced
  the namespace, and XML operations failed without an error. Use distinct
  names, e.g. `$wiItem` for loop variables.
- **A one-element array is serialised as an object.** `ConvertTo-Json` on a
  single item gives `{...}`, which officecli rejects ("Batch input must be a
  JSON array"). Use `ConvertTo-Json -InputObject @($ops.ToArray()) -Depth 8`.
- **`@( @('a','b') )` flattens to `@('a','b')`.** Iterating over pairs then
  yields strings, and `$pair[0]` is the first character. A bulk text
  replacement written this way damaged every `$` in a script. Verify a bulk
  edit with a parse check (`[Management.Automation.Language.Parser]::ParseFile`)
  before copying the file anywhere.
- **Paragraph tab stops set through officecli** (`set ... tabs=1418`) are
  inserted in the wrong order inside `w:pPr` and fail schema validation. Insert
  `w:tabs` directly in the XML, right after `w:pStyle`. Also use namespace-
  qualified attributes: `SetAttribute('val', $W, 'left')`. The prefixed name
  `'w:val'` writes an unqualified attribute that Word ignores.
- **A style-level tab change** (`set /styles/Header --prop tabs=...`) produced
  an invalid style definition. Do not use it.
- **Normal-style text has no tab stop by default.** A `\t` between two words
  may collapse to nothing. Use a dash or a colon in body lines and reserve
  tabs for lines with a defined tab stop.
- **Resident sessions go stale.** After `officecli view` on a copy, the
  resident session holds the old document in memory; the next batch on the
  file fails with "Path not found". Run `officecli close <file>` before
  replacing the file on disk.
- **Binary files through `Out-File` are corrupted.** Copy `.docx` files with
  `Copy-Item`, never by piping `git show` output.
