# Project Layout

Common directory conventions for standards contribution projects.

```text
<project>/
├── PLAN.md                    # YAML frontmatter = metadata source of truth
├── AGENTS.md                  # Orchestration-only (scope, structure, tool refs)
├── <doc-id> - <title>.docx    # Working document
├── figures/                   # Versioned SVG/PNG figure assets
├── ref/                       # Cited source documents + template copy
├── scripts/                   # Analysis/helper scripts
└── tmp/                       # Transient artifacts (keep root clean)
```

- Keep the project root clean -- only `PLAN.md`, `AGENTS.md`, and the final
  `.docx` file.
- Use `tmp/` for intermediate scripts, draft outputs, and debug artifacts.
- Use `figures/` for versioned figure assets (SVG preferred; PNG as fallback
  at >= 300 dpi).
- Keep cited source documents (PDFs, other specs) in `ref/`. Copy the SDO
  template file here as well when initializing a new project.
