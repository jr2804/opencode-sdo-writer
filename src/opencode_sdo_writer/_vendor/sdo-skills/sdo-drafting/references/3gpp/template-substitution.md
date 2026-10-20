# Template Substitution

## Starting a new document

- Start from `ref/Tdoc_Template.docx` only when no document exists yet. If a
  document already exists, continue editing it -- do not re-apply the
  template, as doing so risks breaking existing references and formatting.
- The canonical template is bundled at `assets/3gpp/Tdoc_Template.docx` in this
  skill. Copy it to `ref/Tdoc_Template.docx` in the project root when
  initializing a new project.
- Output filename: `<tdoc> - <title>.docx` (values from PLAN.md front matter).

## Jinja-style placeholders

The template uses `{{ variable }}` placeholders following Jinja2 conventions.
Replace each with the corresponding front matter value:

| Placeholder | Front matter key | Example value |
|---|---|---|
| `{{ title }}` | `title` | Idle noise test method for immersive UEs |
| `{{ date }}` | `date` | 10 - 17 April 2026 |
| `{{ source }}` | `source` | HEAD acoustics GmbH |
| `{{ tdoc }}` | `tdoc` | S4-260615 |
| `{{ meeting }}` | `meeting` | #135-bis-e |
| `{{ agenda_item }}` | `agenda_item` | 7.6 |
| `{{ target }}` | `target` | Agreement |
| `{{ revision_of }}` | `revision_of` | see below |

## `revision_of` handling

- If the document is a revision: set to the TDoc number of the previous
  document (e.g. `S4-260xxx`); render as `Revision of: S4-260xxx` in the
  document header.
- If the document is **not** a revision: set `revision_of: ~` in front
  matter; delete the `{{ revision_of }}` placeholder **and** the surrounding
  "Revision of:" label text from the document header entirely.
- For detecting and applying revision changes in an existing document, see
  `references/3gpp/revision-workflow.md`.
