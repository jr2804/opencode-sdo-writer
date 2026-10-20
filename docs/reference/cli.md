---
title: CLI reference
---

## CLI reference

```text
opencode-sdo-writer [OPTIONS] COMMAND [ARGS]...
```

The package installs one command, `opencode-sdo-writer`. After `uvx` it is `uvx opencode-sdo-writer ...`.

### `init`

Install a profile and the writer agent.

```bash
uvx opencode-sdo-writer init --profile etsi
```

| Option | Short | Default | Meaning |
| ------ | ----- | ------- | ------- |
| `--profile` | `-p` | none | Profile to install: `etsi`, `3gpp` or `itut` |
| `--source` | `-s` | the vendored snapshot | Path to a local checkout of the skills repository |
| `--config` | `-c` | the global config dir | OpenCode configuration directory to write to |
| `--project` | - | none | Install into the `.opencode` directory of this project |
| `--force` | `-f` | off | Overwrite skill directories the installer did not create |
| `--dry-run` | - | off | Show what would be done without writing anything |

The report lists what was installed, updated, left alone, removed, and what was missing or in conflict.

### `update`

Re-install a profile, replacing the skills whose content changed.

```bash
uvx opencode-sdo-writer update --profile etsi
```

Takes the same options as `init`.

### `status`

Show what is installed.

```bash
uvx opencode-sdo-writer status
```

| Option | Short | Meaning |
| ------ | ----- | ------- |
| `--config` | `-c` | OpenCode configuration directory to inspect |
| `--project` | - | Inspect the `.opencode` directory of this project |

A `!` next to a skill means its files no longer match the recorded hash.

### `uninstall`

Remove the installed skills, the agent and the manifest.

```bash
uvx opencode-sdo-writer uninstall
```

Only what a previous install wrote is removed.

### `profiles`

List the available profiles.

```bash
uvx opencode-sdo-writer profiles
```

### Exit codes

| Code | Meaning |
| ---- | ------- |
| `0` | Success |
| `1` | No profile given, unknown profile, a source could not be read, or some skills were missing |

### Examples

```bash
# See what an install would do
uvx opencode-sdo-writer init --profile etsi --dry-run

# Install into one project
uvx opencode-sdo-writer init --profile 3gpp --project .

# Install from a checkout of the skills repository
uvx opencode-sdo-writer init --profile itut --source ../sdo-skills

# Replace a hand-made skill directory
uvx opencode-sdo-writer init --profile etsi --force
```
