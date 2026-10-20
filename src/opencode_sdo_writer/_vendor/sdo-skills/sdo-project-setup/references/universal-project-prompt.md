# Universal SDO Project Prompt

Use this single prompt for both a fresh project and an ongoing project.
The per-SDO drafting skill provides the concrete metadata schema and
template; this prompt handles the common autodetection logic.

## Prompt

You are maintaining an SDO contribution project. Autodetect whether this
is a NEW project or an ONGOING project and execute the correct workflow
end-to-end.

Inputs and source of truth:

- `PLAN.md` frontmatter is authoritative metadata.
- `AGENTS.md` is orchestration-only (no open-issue tracking).
- Tracking lives in `PLAN.md` sections for resolved/open items.

Mandatory skills to load:

1. `<sdo>-drafting` (provides metadata schema, template, header structure)
2. `sdo-project-setup` (provides layout, sync, autodetection)
3. `sdo-docx` (officecli guardrails)
4. `sdo-docx` (formatting rules)

Replace `<sdo>` with the actual prefix: `3gpp`, `etsi`, or `itut`.

Autodetection logic:

1. Derive target doc filename from frontmatter: `<doc-id> - <title>.docx`.
   The `<doc-id>` key name is defined by the SDO drafting skill (e.g. `tdoc`
   for 3GPP, `C-nnnn` for ITU-T).
2. If target DOCX does not exist:
   - If the revision key is set (not `~`/empty): treat as revision bootstrap;
     copy `<revision-id> - <title>.docx` to the target filename.
   - Else: treat as new document bootstrap; copy the SDO template from the
     drafting skill's assets to `ref/`, then initialize from it.
3. If target DOCX exists: treat as ongoing project update.

Execution requirements:

1. Keep root clean; use `tmp/` for temporary artifacts.
2. Ensure `AGENTS.md` exists (copy from `sdo-project-setup/references/`
   if absent) and follows template behavior: keep only project scope and
   orchestration context; do not store open issues or resolved decisions.
3. Reconcile document header against `PLAN.md` using the header structure
   defined in the SDO drafting skill (paragraph-based or table-based).
4. Sync DOCX properties from `PLAN.md` using `set_docx_props.py` with the
   SDO-specific `--props` mapping.
5. Apply changes minimally; never rewrite unrelated body text for
   metadata-only updates.
6. Validate DOCX integrity after edits.

Safety rules:

- Never move old revision files; copy only.
- Never perform destructive XML replacement with empty payload.
- Use style/position XPath targeting, not unstable paragraph IDs.

Final output format:

1. Mode detected: `new` or `ongoing`
2. Files created/updated
3. Header changes applied
4. Metadata synced (list exact key/value results)
5. Validation result
6. Any blockers and fallback actions taken
