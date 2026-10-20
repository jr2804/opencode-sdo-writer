"""Writer profiles.

A profile is the small amount of configuration that differs between the ETSI,
3GPP and ITU-T writers: which skill layers to install, which extra skills to
add, and how the agent is presented.

Profiles are TOML files in the package, so they are readable, commentable and
need no parser beyond the standard library.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from importlib.resources import files
from typing import Any

PROFILE_PACKAGE = "opencode_sdo_writer.profiles"

AGENT_NAME = "sdo-writer"


@dataclass(frozen=True)
class Profile:
    """One writer profile.

    Attributes:
        id: Short identifier used on the command line (``etsi``).
        title: Human readable name.
        description: One line describing what the profile is for.
        agent_name: File name of the installed agent, without extension.
        mode: OpenCode agent mode (``primary`` or ``subagent``).
        color: Agent colour in the OpenCode user interface.
        temperature: Sampling temperature of the agent.
        layers: Skill layers to install. ``common`` is always present.
        extra_skills: Skills from other sources that the profile adds.
        tools_allow: Shell commands the agent may run without asking.
        notes: Markdown appended to the agent prompt, specific to the SDO.
    """

    id: str
    title: str
    description: str
    agent_name: str = AGENT_NAME
    mode: str = "primary"
    color: str = "#2f6f9f"
    temperature: float = 0.1
    layers: tuple[str, ...] = ("common",)
    extra_skills: tuple[str, ...] = ()
    tools_allow: tuple[str, ...] = ()
    notes: str = ""

    @property
    def skill_layers(self) -> tuple[str, ...]:
        """Return the layers to install, with ``common`` first and never missing."""
        layers = list(self.layers)
        if "common" not in layers:
            layers.insert(0, "common")
        return tuple(layers)


class ProfileError(Exception):
    """Raised when a profile cannot be loaded or is invalid."""


def load_profile(profile_id: str) -> Profile:
    """Load a profile by identifier.

    Args:
        profile_id: Identifier of the profile, for example ``etsi``.

    Returns:
        The parsed profile.

    Raises:
        ProfileError: If the profile does not exist or is malformed.
    """
    resource = files(PROFILE_PACKAGE).joinpath(f"{profile_id}.toml")
    if not resource.is_file():
        known = ", ".join(available_profiles())
        msg = f"Unknown profile '{profile_id}'. Available profiles: {known}"
        raise ProfileError(msg)

    try:
        data = tomllib.loads(resource.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as err:
        msg = f"Profile '{profile_id}' is not valid TOML: {err}"
        raise ProfileError(msg) from err

    return _build(profile_id, data)


def available_profiles() -> list[str]:
    """Return the identifiers of all bundled profiles, sorted."""
    directory = files(PROFILE_PACKAGE)
    names = [entry.name[:-5] for entry in directory.iterdir() if entry.name.endswith(".toml")]
    return sorted(names)


def _build(profile_id: str, data: dict[str, Any]) -> Profile:
    """Turn parsed TOML into a :class:`Profile`."""
    for key in ("title", "description"):
        if key not in data:
            msg = f"Profile '{profile_id}' is missing '{key}'"
            raise ProfileError(msg)

    agent = data.get("agent", {})
    layers = data.get("layers", {})
    skills = data.get("skills", {})
    tools = data.get("tools", {})
    notes = data.get("notes", {})

    if not isinstance(agent, dict) or not isinstance(layers, dict):
        msg = f"Profile '{profile_id}' has a malformed [agent] or [layers] section"
        raise ProfileError(msg)

    temperature = agent.get("temperature", 0.1)
    if not isinstance(temperature, (int, float)):
        msg = f"Profile '{profile_id}' has a non-numeric agent.temperature"
        raise ProfileError(msg)

    return Profile(
        id=profile_id,
        title=str(data["title"]),
        description=str(data["description"]),
        agent_name=str(agent.get("name", AGENT_NAME)),
        mode=str(agent.get("mode", "primary")),
        color=str(agent.get("color", "#2f6f9f")),
        temperature=float(temperature),
        layers=tuple(str(layer) for layer in layers.get("include", ["common"])),
        extra_skills=tuple(str(skill) for skill in skills.get("extra", [])),
        tools_allow=tuple(str(tool) for tool in tools.get("allow", [])),
        notes=str(notes.get("body", "")),
    )
