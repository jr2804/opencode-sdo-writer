# Revision Workflow

## Principle

Front matter in `PLAN.md` is the single source of truth. DOCX custom
properties are a persisted copy of the previous state, used to detect
what changed between editing sessions.

## Session start procedure

Run these steps at the beginning of every editing session before touching
the document body.

### Step 1 -- Derive the target filename

```text
<tdoc> - <title>.docx
```

Example: `S4-260717 - Idle noise test method for immersive UEs.docx`

### Step 2 -- Locate or create the working file

| Condition | Action |
|---|---|
| Target file exists in project root | Open it; proceed to step 4 |
| Target file absent, `revision_of` is set | Derive source filename as `<revision_of> - <title>.docx`; **copy** it to the target filename |
| Target file absent, `revision_of` is `~` | Copy `assets/3gpp/Tdoc_Template.docx` to `ref/Tdoc_Template.docx` (if absent), then initialize a new document from the template |

**Always copy, never move.** The original file under its old TDoc number must
remain intact for SVN diff and review.

### Step 3 -- Read the DOCX custom property `tdoc`

Use `mise x github:iOfficeAI/OfficeCLI -- officecli get <doc> --prop tdoc` (or read `docProps/custom.xml`). This
is the TDoc number from the *previous* editing session.

### Step 4 -- Determine the required action

| Front matter `tdoc` vs DOCX `tdoc` | Front matter `revision_of` | Action |
|---|---|---|
| Same | `~` or empty | No structural change; sync properties only (step 6) |
| Different | `~` or empty | Simple renumber: replace old tdoc with new tdoc in header paragraph 1; sync properties |
| Different | Set to a TDoc number | **Revision**: renumber + update `revision_of` run in header paragraph 2 (see step 5) |

### Step 5 -- Patch the header

**The header is NOT a table.** It consists of styled paragraphs:

| Paragraph | Style | Content |
|---|---|---|
| 1 | `TDoc-Header` | Run 1: `3GPP TSG-SA WG4 Meeting <meeting>` · Run 2: `<w:tab/>` · Run 3: `<tdoc>` |
| 2 | `TDoc-Header` | Run 1: `<date>, <place>` · Run 2: `<w:tab/>` · Run 3: `Revision of: <revision_of>` (absent when not a revision) |
| 3 | `Normal` (bold Arial) | `Source:` · `<w:tab/>` · `<source>` |
| 4 | `Normal` (bold Arial) | `Title:` · `<w:tab/>` · `<title>` |
| 5 | `Normal` (bold Arial) | `Agenda item:` · `<w:tab/>` · `<agenda_item>` |
| 6 | `Normal` (bold Arial) | `Document for:` · `<w:tab/>` · `<target>` |

Use officecli `raw-set` with XPath to patch runs. See `sdo-docx`
for the safe raw-set patterns.

### Step 6 -- Sync DOCX properties

After patching, write properties using `set_docx_props.py`:

```bash
mise x uv -- uv run set_docx_props.py "S4-260717 - ...docx"
```

The script reads `PLAN.md` automatically and sets all built-in and custom
properties.
