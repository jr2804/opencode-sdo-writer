# assets/

Generic assets of the skill. Nothing here belongs to one committee or one meeting.

| File | Purpose |
|---|---|
| `build-schedule.ps1` | Re-runnable schedule builder for the report's schedule grid and legend. Takes a per-meeting config with `-Config`; never edit it per meeting. |
| `schedule-config.example.ps1` | Config template with every field documented (manifest path, UID prefix, heading and caption, topics with colours, slot rows, topic per cell, document cells, merges, legend note). |
| `meeting-report.docx` | Generic Word template of the admin boilerplate. The meeting's own agenda document supersedes it in practice. |
| `agenda-template.md` | Lead-document skeleton: day tables, TDoc inventory, work items, open issues, change log. |

Worked examples of past meetings are in `../examples/`, not here. They show structure and
vocabulary; their content is never copied into a new meeting.

Issues convention: `references/issues-and-data-conflicts.md`. Meeting data (chair input):
`docs/<tc><nn>/meeting.toml` in the project. Agenda body: the Python pipeline in `tools/`.

## Regenerating the schedule for a meeting

1. Copy `schedule-config.example.ps1` to the meeting's `scripts/` folder as `<tc><nn>-schedule.ps1`
   and fill it in from the chair's explicit constraints. Design the schedule fresh; do not start
   from an earlier grid.
2. `powershell -ExecutionPolicy Bypass -File scripts/build-schedule.ps1 -Config scripts/<config>.ps1`
3. Check the summary (`failed=0`, `rolledBack=False`) and `validate`. Render the pages and look at them.
4. Update the agenda document and the lead document in the same change.

Save every `.ps1` as UTF-8 **with** BOM (Windows PowerShell 5.1 needs it for dashes and umlauts).
Save configs and markdown without BOM. The builders refuse a config without a BOM.
