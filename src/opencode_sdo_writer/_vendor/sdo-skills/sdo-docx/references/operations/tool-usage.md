# Tool Usage

<!-- lint:allow-tooling -->
<!-- This file intentionally shows both the mise form and the plain
     package-manager form, so the tooling linter is switched off here. -->

## The rule: nothing is assumed to be installed

Every external tool in these skills runs through **mise**, which downloads and
pins it on first use. The user needs only `mise` (or a package manager such
as `uv`, `npm`/`npx`, `bun`/`bunx`) on PATH -- never a manually installed
tool.

Write the invocation as:

```bash
mise x <tool-spec> -- <command> [args]
```

`mise x` is the short form of `mise exec`. The tool spec is a mise tool
request; the command after `--` runs with that tool on PATH. The first call
needs network access; later calls reuse the cached install.

If the user prefers a package manager directly, the equivalent forms are
given in the table below.

## Tool table

| Task | mise form | Package-manager form |
|---|---|---|
| Word/Excel/PowerPoint editing | `mise x github:iOfficeAI/OfficeCLI -- officecli ...` | `npm i -g @officecli/officecli` |
| Run a skill helper script | `mise x uv -- uv run scripts/<script>.py` | `uv run scripts/<script>.py` |
| One-off Python package | `mise x uv -- uvx <package> ...` | `uvx <package> ...` |
| One-off Node package | `mise x node -- npx <package> ...` | `npx <package> ...` |
| One-off Bun package | `mise x bun -- bunx <package> ...` | `bunx <package> ...` |
| Document conversion | `mise x pandoc -- pandoc ...` | `pandoc ...` |
| ETSI portal CLI | `mise x uv -- uvx --from "git+https://forge.etsi.org/rep/reimes/etsi-portal-tool" etsi-portal-tool ...` | same, with `uvx` on PATH |

Pin a version when reproducibility matters:
`mise x github:iOfficeAI/OfficeCLI@v1.0.158 -- officecli ...`.

## Primary tool: officecli

`officecli` is the primary tool for all Word document editing. It ships as a
single self-contained binary, so the mise `github:` backend installs it
without a runtime.

```bash
mise x github:iOfficeAI/OfficeCLI -- officecli view <doc> text
mise x github:iOfficeAI/OfficeCLI -- officecli open <doc>
mise x github:iOfficeAI/OfficeCLI -- officecli close <doc>
```

Invocation order:

1. Via the MCP server `officecli` (if available in the session).
2. Via the CLI as above -- mise installs it on first use.
3. If mise is unavailable, use `uvx`/`npm` equivalents, or locate an
   existing `officecli` binary and invoke it with the full path.

## Secondary tool: python-docx (fallback only)

Use `python-docx` only for tasks `officecli` cannot do, such as
programmatic table creation or image insertion. Do not use it for general
document editing -- it does not support all template styles and can
introduce formatting inconsistencies.

```bash
mise x uv -- uv run --with python-docx <script>.py
```

## Figures and illustrations

- Use the Draw.io MCP server as the primary tool for creating diagrams.
- As a fallback, use the `drawio` skill for file-based diagram creation
  via the Draw.io desktop app.

## SVG export

Always export figures in SVG format for maximum quality in Word. If SVG
insertion fails:

1. First fallback: use python-docx with the SVG patch (`docx-svg` skill).
2. Last fallback: export as PNG at >= 300 dpi.

When exporting Draw.io diagrams to SVG, follow the
[Draw.io SVG text rendering guidelines](https://www.drawio.com/doc/faq/svg-export-text-problems)
to prevent text display issues in Word.

## Notes

- `mise x` is the short form of `mise exec`; both work.
- On Windows, quote tool specs that carry options:
  `mise x "github:owner/repo[option=value]" -- tool ...`.
- mise installs missing tools before running the command
  (`exec_auto_install`); if it is disabled, the command still runs with
  whatever is already on PATH.
