---
title: Profiles
---

## Profiles

A profile decides three things: which skills are installed, what the agent is called and how it behaves, and which tools it may run.

Profiles are TOML files in `src/opencode_sdo_writer/profiles/`. They are part of the package, so they ship with it.

### The three profiles

| Profile | Layers | Extra skills |
| ------- | ------ | ------------- |
| `etsi` | `common`, `etsi` | `etsi-portal-tool`, `etsi-meeting-report` |
| `3gpp` | `common`, `3gpp` | none |
| `itut` | `common`, `itut` | none |

The common layer is always included: it carries the writing style, the DOCX mechanics, the drafting skeletons, the IPR notes and the project setup.

### Anatomy

```toml
id = "etsi"
title = "ETSI Writer"
description = "Drafts ETSI contributions, meeting documents, work item descriptions and deliverables (TS, ES, EN, TR, EG, GS, SR)."

[agent]
name = "sdo-writer"
mode = "primary"
color = "#2f6f9f"
temperature = 0.1

[layers]
include = ["common", "etsi"]

[skills]
extra = ["etsi-portal-tool", "etsi-meeting-report"]

[tools]
allow = [
  "mise *",
  "uv run *",
  "uvx *",
  "npx *",
  "bunx *",
  "git status*",
  "git log*",
  "git diff*",
  "etsi-portal-tool *",
]

[notes]
body = """
## ETSI specifics

- **Two kinds of document.** ...
"""
```

#### `id`, `title`, `description`

The identifier is what `--profile` expects. The title and description are shown by the `profiles` command and written into the agent file.

#### `[agent]`

| Key | Meaning |
| --- | ------- |
| `name` | File name of the agent, without extension: `agents/sdo-writer.md` |
| `mode` | `primary` or `subagent` |
| `color` | Hex colour for the agent in the OpenCode interface |
| `temperature` | Sampling temperature; the writer profiles use a low value because the rules are the point, not the phrasing |

#### `[layers]`

The layers of the skills repository to install. `common` first, then the body.

#### `[skills]`

`extra` lists skills that do not live in the skills repository. The ETSI profile uses it for the two skills that come with the portal tool.

#### `[tools]`

The commands the agent may run, written as the patterns OpenCode matches against. `mise *`
covers the on-demand tool calls; the `git *` entries are there for checking the state of a working
document.

#### `[notes]`

Body-specific guidance that is appended to the agent file. This is where the differences between the
bodies live: ETSI's contribution-versus-deliverable distinction, the approval routes, the portal.
A profile is a small fragment, not a fork of the agent.

### Writing a new profile

1. Copy the closest existing profile.
2. Give it an `id`, a `title` and a `description`.
3. List the layers you need.
4. Write the body-specific notes. If a rule matters for more than one body, it belongs in a common skill, not in a profile.
5. Add it to the package data so it ships.

The layers are resolved through `vendor.lock`, so a profile that names a layer the lock file does not
have installs nothing for that layer. The `init` command reports missing skills and exits with a
non-zero status.

### Agent file

The agent is rendered from the template in `src/opencode_sdo_writer/templates/`:

- `sdo-writer.md` - the frontmatter, the permissions derived from `[tools]`, and the body.
- `sdo-writer-body.md` - the shared behaviour, the same for every profile.

The rendered file lands next to the skills, in `agents/<name>.md`, and OpenCode picks it up from there.
