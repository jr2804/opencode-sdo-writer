# Project Agent Guide -- SDO Contribution Template

Copy this file to project root as `AGENTS.md` and fill in the sections marked
`[EDIT]`. The per-SDO drafting skill provides the concrete metadata schema
and template.

## Project Scope

**[EDIT]** Draft a `<SDO>` contribution titled `"[TITLE]"` for meeting
`[MEETING]`, agenda item `[AGENDA_ITEM]`, target `[TARGET_TYPE]`.

Add 1-2 sentences describing the technical motivation and scope.

______________________________________________________________________

## Skill Architecture

| Skill | Purpose | When to invoke |
|---|---|---|
| `sdo-project-setup` | Project layout, metadata sync, new-vs-ongoing detection | Every session start |
| `sdo-docx` | Formal-document styles, headings, enumerations, notes, tables, citations | Formatting clauses, captions, reference sections |
| `sdo-docx` | officecli safety patterns, tab/bookmark/field-code helpers | DOCX header, metadata, cross-references, XML-level mutations |
| `<sdo>-drafting` | SDO-specific template rules, metadata schema, revision workflow, style-name mapping | Document naming, PLAN.md setup, revision-of handling |

Replace `<sdo>` with the actual prefix: `3gpp`, `etsi`, or `itut`.

## Content Ownership

### Keep in AGENTS.md

- Contribution-specific technical scope and rationale.
- Current document structure (section outline only).
- Project-specific constraints not covered by skills (e.g. normative
  reference context, specific figure formats).

### Track in PLAN.md

- Resolved decisions and technical rationale updates.
- Open issues and checklist progress.
- Working assumptions and pending validation items.

### Do not duplicate

- officecli guardrails -> delegate to `sdo-docx`
- Editorial conventions -> delegate to `sdo-docx`
- SDO template mechanics -> delegate to `<sdo>-drafting`
- Project setup workflows -> delegate to `sdo-project-setup`

## Workflow Checklist

- [ ] Copy this template to project root as `AGENTS.md`
- [ ] Edit "Project Scope" section
- [ ] Create `PLAN.md` with SDO-specific frontmatter keys
- [ ] Copy SDO template `.docx` to `ref/`
- [ ] Run `set_docx_props.py` to sync metadata to DOCX
- [ ] Load the four skills listed above for every session
