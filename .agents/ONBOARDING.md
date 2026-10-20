# AGENTS.md — ONBOARDING

Read this when starting a new session. After first read, only revisit when
project structure or tooling changes significantly.

## Project

OpenCode agent and profiles for writing standards contributions and deliverables (ETSI, 3GPP, ITU-T) Full docs at `README.md` or `docs/`.

## Quick start

```bash
mise dev        # install dependencies (uv sync --dev)
mise test       # run pytest with coverage
mise lint       # ruff + ty + codespell
mise format     # ruff format + isort + pyreorder
mise all        # test + lint + format in one pass
```

## Entry points (read these first)

| File / Section | Why |
| -------------- | --- |
| `AGENTS.md` | Root rail — rules + `.agents/` index |
| `.agents/POLICIES.md` | Boundaries, priorities, verification |
| `.agents/FILES.md` | Source-of-truth locations for this package |
| `pyproject.toml` | Dependencies, pytest config, build backend |
| `.copier-answers.yml` | Template answers (regenerated on `copier update`) |

## Layout

- **`src/opencode_sdo_writer/`** — primary package source (src layout)
- **`tests/`** — pytest suite (100% coverage gate)
- **`src/opencode_sdo_writer/cli/`** — Typer CLI
- **`docs/`** — Zensical / MkDocs Material documentation
- **`.config/mise/`** — task runner config (`config.toml` + `conf.d/` fragments)

## Where to dig deeper

- `docs/` — user-facing documentation
- `.agents/HISTORY.md` — past decisions and rationale
- Source-tree AGENTS.md files — local contracts for each area

## Available tools

No MCP dev-features enabled. See `.copier-answers.yml` for template answers.
