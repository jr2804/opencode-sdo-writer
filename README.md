# OpenCode SDO Writer

> An OpenCode agent, three writer profiles and twenty-one skills for writing standards contributions and deliverables (ETSI, 3GPP, ITU-T)

<p align="center">
  <a href="#"><img alt="Python 3.13+" src="https://img.shields.io/badge/python-3.13%2B-3776ab?logo=python"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg"></a>
  <a href="https://github.com/jr2804/opencode-sdo-writer/actions">
    <img alt="CI" src="https://github.com/jr2804/opencode-sdo-writer/actions/workflows/ci.yml/badge.svg">
  </a>
</p>

---

## What this is

Standards writing has two problems: the *rules* (who decides what, how a document is numbered, what
a contribution must contain) and the *mechanics* (getting a skeleton document filled in without
breaking its styles).

This package installs both into OpenCode:

- **`sdo-writer`**, an OpenCode agent that knows the difference between a contribution and a deliverable, and that refuses to invent a rule it has not read.
- **Three profiles** — `etsi`, `3gpp`, `itut` — that decide which skills are in scope.
- **Twenty-one skills** that carry the rules, the document skeletons, the checklists and the tooling
  notes. The skill text lives in [jr2804/sdo-skills](https://github.com/jr2804/sdo-skills); this
  repository vendors a pinned snapshot of it.

Nothing has to be installed. Every external tool is pulled on demand through [mise](https://mise.jdx.dev/):

```bash
mise x github:iOfficeAI/OfficeCLI -- officecli get file.docx
```

## Install

The package lives in this repository, so it is installed straight from git:

```bash
uvx --from "git+https://github.com/jr2804/opencode-sdo-writer" opencode-sdo-writer init --profile etsi
```

The command is long, so alias it once:

```bash
alias sdo-writer='uvx --from "git+https://github.com/jr2804/opencode-sdo-writer" opencode-sdo-writer'
sdo-writer init --profile etsi
```

That writes the agent and the skills into your global OpenCode configuration (`~/.config/opencode/`),
so they are available in every project. Use `--project .` to install into a single repository
instead.

```bash
sdo-writer init --profile 3gpp    # 3GPP
sdo-writer init --profile itut    # ITU-T
sdo-writer profiles               # list them
sdo-writer status                 # what is installed
sdo-writer update --profile etsi  # restore or refresh
sdo-writer uninstall              # remove everything again
```

Full details in [docs/installation.md](docs/installation.md).

## Profiles

| Profile | In scope | Adds |
| ------- | -------- | ---- |
| `etsi` | common + ETSI | Directives, procedures, portal and specification tooling |
| `3gpp` | common + 3GPP | Working groups, meetings, TDoc conventions, change requests, portal session handling |
| `itut` | common + ITU-T | Working methods, recommendation structure, contribution rules, patent policy |

The common layer carries the writing style, the DOCX mechanics, the drafting skeletons, the IPR
notes and the project setup. See [docs/profiles.md](docs/profiles.md).

## The skills

| Layer | Skills |
| ----- | ------ |
| common | `sdo-writing`, `sdo-docx`, `sdo-drafting`, `sdo-ipr`, `sdo-project-setup` |
| etsi | `etsi-governance`, `etsi-directives`, `etsi-procedures`, `etsi-tools` |
| 3gpp | `3gpp-basics`, `3gpp-meetings`, `3gpp-working-groups`, `3gpp-releases`, `3gpp-specifications`, `3gpp-tdocs`, `3gpp-change-request`, `3gpp-portal-authentication` |
| itut | `itut-reference`, `itut-contributions` |
| tools | `etsi-portal-tool`, `etsi-meeting-report` |

Each skill is a directory with a `SKILL.md` and, where the content is too long for a prompt,
`references/`, `assets/` and `scripts/`. The agent loads a skill when the request matches its
description, and reads the references only when it needs them. The catalogue is in
[docs/skills.md](docs/skills.md).

## How a writing session looks

1. You ask for a contribution, a meeting document, a work item description or a deliverable section.
2. The agent loads the drafting skill for your body, plus the procedure skill that explains who does what.
3. It copies the skeleton from `assets/`, fills it through OfficeCLI, and keeps the styles intact.
4. It runs the checklist that belongs to the document type before it calls the work done.

The agent does not write from memory about a body it has a rule for. If the request touches IPR,
the Directives or a numbering rule, it loads the skill that holds the rule.

## Working with the sources

The skill text is not edited here. It comes from the skills repository, pinned in `src/opencode_sdo_writer/vendor.lock`:

```bash
uv run python scripts/vendor_skills.py \
    --source D:/path/to/sdo-skills \
    --ref v0.1.0 \
    --extra-source etsi-portal-tool=D:/path/to/etsi-portal-tool
```

See [docs/skills.md](docs/skills.md) for how the layers are laid out and how a new skill is added.

## Development

```bash
mise dev          # create the environment and install everything
mise test         # pytest with a 100% coverage gate
mise lint         # ruff, ty and codespell
mise sort         # check the structural order of the modules (pyreorder)
mise format       # ruff format, isort and pyreorder
mise all          # everything the CI runs
mise docs-serve   # live preview of the documentation
```

The `init` command is the interesting part of the package: it reads a profile, resolves the
vendored skills, writes them into an OpenCode configuration directory and records a manifest so
that `update` and `uninstall` know what belongs to it. The behaviour is covered by tests in
`tests/`.

## Tech stack

| Layer | Tool | Purpose |
| ----- | ---- | ------- |
| Package manager | [uv](https://docs.astral.sh/uv/) | Fast installs, deterministic lockfile |
| Task runner | [mise](https://mise.jdx.dev/) | DAG-based tasks, tool version management, on-demand tools |
| CLI | [Typer](https://typer.tiangolo.com/) | `opencode-sdo-writer init`, `status`, `update`, `uninstall` |
| Linter + formatter | [ruff](https://docs.astral.sh/ruff/) | Single-binary code quality |
| Structural sorter | [pyreorder](https://pypi.org/project/pyreorder/) | Module order and hoisted imports |
| Type checker | [ty](https://github.com/google/ty) | Strict type checking |
| Testing | [pytest](https://pytest.org/) | Test framework with a 100% coverage gate |
| Spell check | [codespell](https://github.com/codespell-project/codespell) | Code and doc spell checking |
| Documentation | [Zensical](https://github.com/zensical/zensical) | MkDocs Material with executable examples |
| Versioning | [uv-dynamic-versioning](https://github.com/ninoseki/uv-dynamic-versioning) | Git tag-based versioning |
| CI/CD | GitHub Actions | Test matrix + PyPI release |

## License

MIT - see [LICENSE](LICENSE) for details.

---

Generated from [copier-uv-plus](https://codeberg.org/jr2804/copier-uv-plus).
