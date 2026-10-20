---
title: Installation
---

## Installation

The package installs itself into an OpenCode configuration directory. Nothing else is needed:
every external tool the skills use is pulled on demand through `mise`.

### One line

```bash
uvx --from "git+https://github.com/jr2804/opencode-sdo-writer" opencode-sdo-writer init --profile etsi
```

`uvx` downloads the package, runs the `init` command and throws the temporary environment away. The installed skills and the agent stay behind.

The command is long, so most people alias it once:

```bash
alias sdo-writer='uvx --from "git+https://github.com/jr2804/opencode-sdo-writer" opencode-sdo-writer'
```

The examples below use that alias.

### Where things land

| Path | Content |
| ---- | ------- |
| `~/.config/opencode/agents/sdo-writer.md` | The writer agent |
| `~/.config/opencode/skills/<skill-id>/` | One directory per skill, with its `references/`, `assets/` and `scripts/` |
| `~/.config/opencode/sdo-writer.json` | The manifest: profile, source, timestamp and the hash of every installed skill |

On Windows the global directory is `%USERPROFILE%\.config\opencode`. When `XDG_CONFIG_HOME` is set, it wins.

OpenCode reads `~/.config/opencode/skills/` without any further configuration, so the skills are available in every project once the install finishes.

### Choosing a target

```bash
# Global: available in every project (default)
sdo-writer init --profile etsi

# One project only
sdo-writer init --profile etsi --project /path/to/repo

# An explicit configuration directory
sdo-writer init --profile etsi --config /path/to/.opencode
```

### Profiles

```bash
sdo-writer profiles
```

| Profile | Layers | Focus |
| ------- | ------ | ----- |
| `etsi` | common, etsi | Contributions, meeting documents, work items, ETSI deliverables |
| `3gpp` | common, 3gpp | TDoc conventions, change requests, working groups, specification metadata |
| `itut` | common, itut | Contribution rules, recommendation structure, patent policy |

The `etsi` profile also installs the two tool skills `etsi-portal-tool` and `etsi-meeting-report`.
They come from the portal tool repository rather than from the skills repository.

### Checking the result

```bash
sdo-writer status
```

The output lists the installed skills. A `!` next to a skill means its files on disk no longer match
the recorded hash - somebody edited them. `update` restores them.

The hash ignores the line endings of text files, so a checkout that converts them (git with
`core.autocrlf` on Windows) does not report a change.

### Updating

```bash
sdo-writer update --profile etsi
```

`update` is `init` with the same guarantees: skills whose content changed are replaced, skills that
are unchanged are left alone, and skills that a previous install added but the profile no longer
contains are removed.

### Removing

```bash
sdo-writer uninstall
```

Only what the installer wrote is removed. A skill directory that you created yourself is never touched.

### Conflicts

If a skill directory with the same name already exists and the manifest does not list it, the install leaves it alone and reports it as a conflict:

```text
Conflicts: sdo-writing
```

That is the case when a project already carries a hand-made copy of one of the skills. Either
rename the old directory or pass `--force` to let the installer replace it.

### Development mode

To install straight from a checkout of the skills repository instead of the vendored snapshot:

```bash
sdo-writer init --profile etsi --source /path/to/sdo-skills
```

The manifest then records the checkout, and `status` shows that path as the source.

### Requirements

- Python 3.13 or newer to run the installer (through `uvx`, nothing has to be installed).
- [mise](https://mise.jdx.dev/) for the skills to pull their tools on demand. The skills call
  `mise x <tool> -- <command>`; without mise they report what is missing instead of failing silently.
