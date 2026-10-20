---
title: Skills
---

## Skills

The skill text does not live in this repository. It comes from
[jr2804/sdo-skills](https://github.com/jr2804/sdo-skills), and this package vendors a pinned
snapshot of it.

### Why the split

The rules change on different schedules. The Directives are revised twice a year, a document
skeleton changes when a body changes its templates, the writing style changes when you decide it
does. The installer changes when a new release of this package appears. Keeping the text in its
own repository means a rules fix does not need a new installer, and the installer does not need
to carry the rules.

### The layers

| Layer | Skills | Holds |
| ----- | ------ | ----- |
| `common` | `sdo-writing`, `sdo-docx`, `sdo-drafting`, `sdo-ipr`, `sdo-project-setup` | Writing style, DOCX mechanics, drafting skeletons, IPR notes, project setup |
| `etsi` | `etsi-governance`, `etsi-directives`, `etsi-procedures`, `etsi-tools` | ETSI structure, the Directives, procedures and approval routes, portal and specification tooling |
| `3gpp` | `3gpp-basics`, `3gpp-meetings`, `3gpp-working-groups`, `3gpp-releases`, `3gpp-specifications`, `3gpp-tdocs`, `3gpp-change-request`, `3gpp-portal-authentication` | 3GPP structure, meetings, working groups, releases, specification metadata, TDoc conventions, change requests, portal session handling |
| `itut` | `itut-reference`, `itut-contributions` | ITU-T working methods, recommendation structure, contribution rules |
| `tools` | `etsi-portal-tool`, `etsi-meeting-report` | The portal CLI and the meeting report builder, from the portal tool repository |

### The shape of a skill

```text
<skill-id>/
├── SKILL.md          # the entry point: what it is, when to use it, the short rules
├── references/       # the long text, read only when it is needed
├── assets/           # skeletons, templates, images
├── scripts/          # helpers, each with PEP 723 metadata
└── examples/         # worked examples
```

`SKILL.md` stays small. The linter in the skills repository holds the body under 8 KiB; anything
longer moves into `references/`. A skill that answers one question fits in one prompt; a skill that
answers a family of questions gets a directory.

The frontmatter carries a `name` and a `description`. The description is a list of triggers, not a
summary: the agent matches the request against it to decide whether to load the skill.

### The lock file

`src/opencode_sdo_writer/vendor.lock` records what is vendored:

```toml
version = 1

[[source]]
id = "sdo-skills"
repo = "https://github.com/jr2804/sdo-skills.git"
ref = "v0.1.0"

[[source]]
id = "etsi-portal-tool"
repo = "D:\\SVN\\Projects\\Standardization\\etsi-portal-tool"
ref = "v0.1.0"

[skill]
"3gpp-basics" = { layer = "3gpp", source = "sdo-skills" }
"sdo-writing" = { layer = "common", source = "sdo-skills" }
```

The `layer` decides which profile gets the skill. The `source` decides which directory in `_vendor/` it is copied from.

### Re-vendoring

```bash
uv run python scripts/vendor_skills.py \
    --source /path/to/sdo-skills \
    --ref v0.1.0 \
    --repo https://github.com/jr2804/sdo-skills.git \
    --extra-source etsi-portal-tool=/path/to/etsi-portal-tool
```

The script copies the skill directories into
`src/opencode_sdo_writer/_vendor/<source-id>/<skill-id>/` and rewrites the lock file. It never
touches the network: whoever prepares a release decides what goes into the package.

Options:

| Option | Meaning |
| ------ | ------- |
| `--source` | Checkout of the skills repository (required) |
| `--ref` | Revision to record in the lock file (required) |
| `--repo` | Repository URL to record for the main source |
| `--extra-source ID=PATH` | Additional source of skills, for example a tool repository |
| `--output` | Lock file to write (default `src/opencode_sdo_writer/vendor.lock`) |
| `--vendor-dir` | Directory for the snapshot (default `src/opencode_sdo_writer/_vendor`) |

### Adding a skill

1. Write it in the skills repository, under the layer that owns the topic, and let the linter there pass.
2. Re-vendor. The new skill appears in `_vendor/` and in the lock file with its layer.
3. If a profile should get it, add the layer to the profile's `[layers] include` list. A skill outside the profile's layers is vendored but not installed.
4. Run `mise all` and `mise run test`.

The install path needs no change: the installer reads the lock file, and the profile decides the layers.

### Rules for the skills

The skills repository enforces these through its linter:

- A `SKILL.md` body stays under 8 KiB. Overflow moves to `references/`.
- The description is a trigger enumeration.
- Every referenced path - `references/`, `assets/`, `scripts/` - must exist.
- Every mentioned skill identifier must exist.
- External tools are invoked as `mise x <tool> -- <command>`, so that nothing has to be installed by hand.
