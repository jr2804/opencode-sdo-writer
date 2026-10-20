# 3GPP style-name mapping

Concrete Word style IDs for 3GPP documents, keyed by the abstract names used
in `sdo-docx` and `sdo-drafting`.

## 3GPP style-name mapping

Concrete Word style IDs for 3GPP documents. Use these when applying
formatting rules from `sdo-docx`.

| Abstract name (`sdo-docx`) | 3GPP concrete style ID | Purpose |
|---|---|---|
| `body-text` | `Normal` | Main body paragraphs |
| `heading-1` | `Heading 1` | Top-level section heading |
| `heading-2` | `Heading 2` | Second-level section heading |
| `heading-3` | `Heading 3` | Third-level section heading |
| `enum-1` | `B1` | First-level enumeration (en-dash bullet) |
| `enum-2` | `B2` | Second-level enumeration |
| `enum-3` | `B3` | Third-level enumeration (if used) |
| `table-caption` | `TH` | Table caption (above table) |
| `table-header` | `TAH` | Table header row |
| `table-data` | `TAC` | Table data rows |
| `table-note` | `TAN` | Table merged-bottom-row note |
| `figure-para` | `FL` | Paragraph containing image |
| `figure-caption` | `TF` | Figure caption (below figure) |
| `figure-note` | `NF` | Note below figure, before caption |
| `note-main` | `NO` | Last note in a consecutive block |
| `note-continuation` | `NW` | Preceding notes in a block |
| `reference-entry` | `EX` | Each references section entry |
| `code-text` | `PL` | Inline code, function/variable names, filenames |

Additional 3GPP-specific styles (no abstract equivalent):

| Style ID | Purpose |
|----------|---------|
| `TDoc-Header` | Cover page header paragraphs (TDoc number, date, source, title, agenda item, target) |
