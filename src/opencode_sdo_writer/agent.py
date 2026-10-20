"""Rendering the OpenCode agent file.

The agent is a Markdown file with a YAML frontmatter block, placed in
``<config>/agents/<name>.md``. OpenCode turns the file name into the agent
name and reads the frontmatter for the description, mode, colour,
temperature and permissions.
"""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path

from .profile import Profile

TEMPLATE_PACKAGE = "opencode_sdo_writer.templates"
FRONTMATTER_TEMPLATE = "sdo-writer.md"
BODY_TEMPLATE = "sdo-writer-body.md"


def render_agent(profile: Profile, skill_ids: tuple[str, ...]) -> str:
    """Render the agent file for a profile.

    Args:
        profile: The profile to render.
        skill_ids: Identifiers of the skills the agent may load.

    Returns:
        The complete agent file, frontmatter and prompt.
    """
    skill_permissions = "\n".join(f'    "{skill_id}": allow' for skill_id in sorted(skill_ids))
    bash_permissions = "\n".join(f'    "{pattern}": allow' for pattern in profile.tools_allow)

    frontmatter = _read_template(FRONTMATTER_TEMPLATE)
    replacements = {
        "{{description}}": _yaml_string(profile.description),
        "{{mode}}": profile.mode,
        "{{color}}": _yaml_string(profile.color),
        "{{temperature}}": str(profile.temperature),
        "{{skill_permissions}}": skill_permissions,
        "{{bash_permissions}}": bash_permissions,
    }
    for marker, value in replacements.items():
        frontmatter = frontmatter.replace(marker, value)

    body = _read_template(BODY_TEMPLATE).rstrip("\n")
    notes = profile.notes.strip()
    body = f"{body}\n\n{notes}\n" if notes else f"{body}\n"

    return f"{frontmatter}\n{body}"


def _read_template(name: str) -> str:
    """Read a template from the package."""
    resource = files(TEMPLATE_PACKAGE).joinpath(name)
    return Path(str(resource)).read_text(encoding="utf-8")


def _yaml_string(value: str) -> str:
    """Quote a string for YAML when it needs it."""
    if value and not any(char in value for char in ":#{}[]&*!|>%@`\"'\n"):
        return value
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    return f'"{escaped}"'
