# TOOLS — development-time tooling inventory

OpenCode coding agent project. Tooling surface:

| Tool | When to use |
| ---- | ----------- |
| `mise` | Every skill invokes tools through it: `mise x <tool> -- <command>`. Install once. |
| `uv` / `uvx` | Run installer and tests; publish. |
| `pytest` | Test suite, 100% coverage gate. |
| `ruff` + `pyreorder` | Lint/format; `mise run format`. |
| `ty` | Type checking (lint). |
| `rumdl` | Markdown lint: `mise run format-md`. |
| `zensical` | Docs site build. |
| `copier`-adjacent none — see `scripts/vendor_skills.py`. |
| `git` | History. |

MCP servers: none configured for this repo. OpenCode agent/skills run in user's environment.