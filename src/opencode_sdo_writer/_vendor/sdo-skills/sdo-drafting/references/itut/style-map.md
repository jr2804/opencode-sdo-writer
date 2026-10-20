# ITU-T style-name mapping

Concrete Word style IDs for ITU-T documents, keyed by the abstract names used
in `sdo-docx` and `sdo-drafting`.

## ITU-T style-name mapping

Concrete Word style IDs for ITU-T documents. Use these when applying
formatting rules from `sdo-docx`.

| Abstract name (`sdo-docx`) | ITU-T concrete style ID | Notes |
|---|---|---|
| `body-text` | `Body Text` | If absent, fall back to `Normal`; verify with `mise x github:iOfficeAI/OfficeCLI -- officecli get <doc> /styles` |
| `heading-1` | `Heading 1` | Section headings (numbered) |
| `heading-2` | `Heading 2` | Subsection headings |
| `heading-3` | `Heading 3` | Sub-subsection headings |
| `enum-1` | `enumlev1` | First-level enumeration |
| `enum-2` | `enumlev2` | Second-level enumeration |
| `enum-3` | `enumlev3` | Third-level enumeration (if used) |
| `table-caption` | `Table_No & title` | officecli styleId: `TableNotitle` |
| `table-header` | `Table_head` | officecli styleId: `Tablehead` |
| `table-data` | `Table_text` | officecli styleId: `Tabletext` |
| `table-note` | (varies by template) | If not found in template, omit styling and add a TODO comment for manual review |
| `figure-para` | `Figure` | Paragraph containing image |
| `figure-caption` | `Figure_No & title` | Below figure |
| `figure-note` | (varies by template) | If not found in template, omit styling and add a TODO comment for manual review |
| `note-main` | `Note` | Last note in block |
| `note-continuation` | (varies by template) | If not found in template, omit styling and add a TODO comment for manual review |
| `reference-entry` | `References` | Each references entry (normative references *and* bibliography entries) |
| `appendix-heading` | `Appendix_No & title` | Non-integral (informative) appendix headings |
| `bibliography-heading` | `Appendix_No & title` | Bibliography clause heading (same style as appendix) |
| `code-text` | `Macro Text` | officecli styleId: `MacroText` |

Additional ITU-T-specific styles (no abstract equivalent):

| Style ID | Purpose |
|----------|---------|
| `Equation` | Display equation paragraph (centred equation + right-aligned label via tab stops) |
| `Equation_legend` | officecli styleId: `Equation_legend` -- annotation paragraph following equation |
| `Headingb` | Sub-headings within a proposed clause block (not auto-numbered) |
| `TSBHeaderSummary` | Abstract table cell content |

______________________________________________________________________
