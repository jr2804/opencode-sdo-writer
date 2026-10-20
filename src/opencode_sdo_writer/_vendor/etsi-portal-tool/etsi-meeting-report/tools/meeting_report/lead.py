"""Lead document (agenda-draft.md): generated only when it does not exist yet.

Once the file exists it is edited directly (by an agent or by a targeted patch), never regenerated.
"""
from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined


def render_lead(template: Path, ctx: dict, meeting: dict, out: Path) -> None:
    if out.exists():
        raise SystemExit(
            f"refusing to overwrite {out}: the lead document exists. Edit it directly "
            "(agent or targeted patch); it is not regenerated.")
    env = Environment(loader=FileSystemLoader(str(template.parent)), undefined=StrictUndefined,
                      trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True)
    text = env.get_template(template.name).render(ctx=ctx, meeting=meeting["meeting"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
