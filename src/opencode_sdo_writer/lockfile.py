"""The vendor lock file.

``vendor.lock`` pins every skill that can be installed together with the
repository and revision it came from. It is the single source of truth for

* which skills exist,
* which layer a skill belongs to, and
* which upstream revision the skill content was taken from.

The installer never talks to the network: it only reads the vendored snapshot
that the release build put into the package, or a local checkout.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path

LOCK_PACKAGE = "opencode_sdo_writer"
LOCK_FILE = "vendor.lock"


@dataclass(frozen=True)
class Source:
    """An upstream repository that provides skills.

    Attributes:
        id: Short identifier of the source.
        repo: Clone URL of the repository.
        ref: Pinned revision (tag or commit).
        optional: Whether a missing source is an error.
    """

    id: str
    repo: str
    ref: str
    optional: bool = False


@dataclass(frozen=True)
class SkillEntry:
    """One installable skill.

    Attributes:
        id: Skill identifier, equal to the directory name.
        layer: Layer the skill belongs to (``common``, ``etsi``, ``3gpp``,
            ``itut`` or ``tools``).
        source: Identifier of the source repository.
    """

    id: str
    layer: str
    source: str


@dataclass(frozen=True)
class LockFile:
    """The parsed content of ``vendor.lock``."""

    version: int
    sources: tuple[Source, ...]
    skills: tuple[SkillEntry, ...]

    def source(self, source_id: str) -> Source:
        """Return the source with the given identifier.

        Raises:
            KeyError: If the source is not in the lock file.
        """
        for item in self.sources:
            if item.id == source_id:
                return item
        msg = f"Unknown source '{source_id}' in {LOCK_FILE}"
        raise KeyError(msg)

    def skills_for_layers(self, layers: tuple[str, ...]) -> list[SkillEntry]:
        """Return the skills belonging to any of the given layers, in lock order."""
        wanted = set(layers)
        return [skill for skill in self.skills if skill.layer in wanted]

    def skill(self, skill_id: str) -> SkillEntry:
        """Return the entry of a single skill.

        Raises:
            KeyError: If the skill is not in the lock file.
        """
        for item in self.skills:
            if item.id == skill_id:
                return item
        msg = f"Unknown skill '{skill_id}' in {LOCK_FILE}"
        raise KeyError(msg)


class LockError(Exception):
    """Raised when the lock file is missing or malformed."""


def load_lock(path: Path | None = None) -> LockFile:
    """Load the lock file.

    Args:
        path: Explicit path to a lock file. When omitted, the lock file
            shipped inside the package is used.

    Raises:
        LockError: If the file is missing or malformed.
    """
    target = path if path is not None else files(LOCK_PACKAGE).joinpath(LOCK_FILE)
    if not Path(str(target)).is_file():
        msg = f"Lock file not found: {target}"
        raise LockError(msg)

    try:
        data = tomllib.loads(Path(str(target)).read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as err:
        msg = f"Lock file {target} is not valid TOML: {err}"
        raise LockError(msg) from err

    sources = tuple(
        Source(
            id=str(entry.get("id", "")),
            repo=str(entry.get("repo", "")),
            ref=str(entry.get("ref", "")),
            optional=bool(entry.get("optional", False)),
        )
        for entry in data.get("source", [])
    )
    skills = tuple(
        SkillEntry(
            id=skill_id,
            layer=str(entry.get("layer", "common")),
            source=str(entry.get("source", "")),
        )
        for skill_id, entry in data.get("skill", {}).items()
    )

    if not skills:
        msg = f"Lock file {target} does not define any skill"
        raise LockError(msg)

    return LockFile(version=int(data.get("version", 1)), sources=sources, skills=skills)
