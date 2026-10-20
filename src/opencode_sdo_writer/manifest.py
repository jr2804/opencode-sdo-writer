"""The installer manifest.

The manifest records what a previous install put on disk, so that an update
can replace exactly those skills and an uninstall can remove exactly those
skills, without touching anything the user added themselves.

It is written as JSON next to the skills, in the OpenCode configuration
directory.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

MANIFEST_VERSION = 1


@dataclass
class Manifest:
    """State of an installation.

    Attributes:
        version: Schema version of the manifest.
        profile: Identifier of the profile that was installed.
        source: Description of the skill source, for example
            ``sdo-skills@v0.1.0`` or a checkout path.
        installed_at: Timestamp of the last install, in ISO 8601 format.
        skills: Mapping of skill identifier to content hash.
        agent: File name of the installed agent, or ``None``.
    """

    version: int = MANIFEST_VERSION
    profile: str = ""
    source: str = ""
    installed_at: str = ""
    skills: dict[str, str] = field(default_factory=dict)
    agent: str | None = None

    @property
    def installed_skills(self) -> list[str]:
        """Return the identifiers of the installed skills, sorted."""
        return sorted(self.skills)


def load_manifest(path: Path) -> Manifest | None:
    """Load a manifest, returning ``None`` when it does not exist or is unreadable."""
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(data, dict):
        return None
    skills = data.get("skills")
    agent = data.get("agent")
    return Manifest(
        version=int(data.get("version", MANIFEST_VERSION)),
        profile=str(data.get("profile", "")),
        source=str(data.get("source", "")),
        installed_at=str(data.get("installed_at", "")),
        skills={str(k): str(v) for k, v in skills.items()} if isinstance(skills, dict) else {},
        agent=agent if isinstance(agent, str) and agent else None,
    )


def save_manifest(path: Path, manifest: Manifest) -> None:
    """Write a manifest to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": manifest.version,
        "profile": manifest.profile,
        "source": manifest.source,
        "installed_at": manifest.installed_at or datetime.now(UTC).isoformat(timespec="seconds"),
        "skills": dict(sorted(manifest.skills.items())),
        "agent": manifest.agent,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
