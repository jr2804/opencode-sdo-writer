---
title: Overview
hide:
- feedback
---

## OpenCode SDO Writer

> An OpenCode agent, three writer profiles and twenty-one skills for writing standards contributions and deliverables (ETSI, 3GPP, ITU-T)

The package installs one agent, three writer profiles and the skills that carry the rules of three standardisation bodies into OpenCode.

### In one line

```bash
uvx --from "git+https://github.com/jr2804/opencode-sdo-writer" opencode-sdo-writer init --profile etsi
```

The examples in this documentation use the short alias `sdo-writer` for that command.

### The pieces

- **The agent** (`sdo-writer`) knows the difference between a contribution and a deliverable, reads
  the rules from the skills instead of from memory, and works from the document skeletons rather
  than from a blank page.
- **The profiles** (`etsi`, `3gpp`, `itut`) decide which skills are in scope and what the body-specific guidance says.
- **The skills** carry the rules, the checklists, the skeletons and the tooling notes. The text lives
  in [jr2804/sdo-skills](https://github.com/jr2804/sdo-skills); this package vendors a pinned
  snapshot.

### Documentation

- [Installation](installation.md) - where things land, how to update and uninstall
- [Usage](usage.md) - what a writing session looks like
- [Profiles](profiles.md) - what a profile contains and how to write one
- [Skills](skills.md) - the catalogue, the lock file, how to add a skill
- [CLI reference](reference/cli.md) - every command and option
- [API reference](reference/api.md) - the Python API
- [Credits](credits.md) - what this is built on
- [Contributing](contributing.md) - how to work on the package
- [License](license.md) - MIT
