---
name: sdo-project-setup
description: Bootstrap and maintain an agent-based document drafting project for any SDO. Use when starting a new standards contribution, setting up project structure (PLAN.md, AGENTS.md, directory layout), syncing metadata between PLAN.md and .docx properties, or detecting whether a project is new vs. ongoing. Provides common project infrastructure; SDO-specific templates and header structures live in the per-SDO drafting skill.
---

# SDO Project Setup

Common project infrastructure for agent-based standards document drafting --
independent of any specific SDO. Load this skill alongside the per-SDO
drafting skill (`sdo-drafting`, `sdo-drafting`, `sdo-drafting`) when
setting up or maintaining a contribution project.

## What this skill provides

| Concern | Where |
|---------|-------|
| Directory layout | [references/project-layout.md](references/project-layout.md) |
| AGENTS.md orchestration template | [references/AGENTS-template.md](references/AGENTS-template.md) |
| Universal new-vs-ongoing autodetection prompt | [references/universal-project-prompt.md](references/universal-project-prompt.md) |
| DOCX property sync from PLAN.md | [scripts/set_docx_props.py](scripts/set_docx_props.py) |

## What the per-SDO drafting skill provides

| Concern | Example (3GPP) |
|---------|----------------|
| Canonical template file | `Tdoc_Template.docx` with all required styles |
| SDO-specific metadata keys | `tdoc`, `meeting`, `revision_of` |
| Header structure for revision patching | Paragraph-based header with `TDoc-Header` style |
| Template substitution rules | `{{ tdoc }}` -> `S4-260717` |
| Concrete style-name mapping | `B1`, `NO`, `TF`, `TH`, etc. |

## Quick start: new 3GPP TDoc project

```bash
# 1. Copy AGENTS template (from sdo-project-setup)
cp .agents/skills/sdo-project-setup/references/AGENTS-template.md ./AGENTS.md
# Edit the "Project Scope" section

# 2. Create PLAN.md with frontmatter
# (keys defined in sdo-drafting/references/3gpp/frontmatter.md)

# 3. Copy template (from sdo-drafting)
cp .agents/skills/sdo-drafting/assets/3gpp/Tdoc_Template.docx ./ref/

# 4. Initialize document and sync properties
# (<skills-root> = the installed skills directory, e.g. .agents/skills in the
#  project or ~/.config/opencode/skills for a global install)
mise x uv -- uv run <skills-root>/sdo-project-setup/scripts/set_docx_props.py \
  "S4-260717 - Idle noise test method.docx" \
  --props tdoc=tdoc,revision_of=revision_of,meeting=meeting,date=date,agenda_item=agenda_item,target=target
```

## Cross-references

- `sdo-docx` -- formatting rules (loaded for all SDOs)
- `sdo-docx` -- officecli guardrails (loaded for all SDOs)
- `sdo-writing` -- prose quality (loaded when drafting content)
- `sdo-writing` -- mechanical writing rules (loaded when drafting content)
- `sdo-drafting` -- 3GPP-specific template, metadata, header structure
- `sdo-drafting` -- ETSI-specific template, metadata, header structure
- `sdo-drafting` -- ITU-T-specific template, header table structure
