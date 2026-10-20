"""Resolving skill directories to install.

Two sources are supported:

``vendored``
    The snapshot that the release build copied into the package, laid out as
    ``_vendor/<source-id>/<skill-id>/``.

``checkout``
    A local clone of a skills repository, laid out as
    ``<checkout>/skills/<layer>/<skill-id>/``. Used for development, so that
    changes in the skills repository are picked up without a rebuild.

Both expose the same interface, so the installer does not care where the
content came from.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path

VENDOR_PACKAGE = "opencode_sdo_writer"
VENDOR_DIR = "_vendor"

#: Files that never contribute to a skill hash.
HASH_EXCLUDED_NAMES = {".DS_Store", "Thumbs.db"}


@dataclass(frozen=True)
class SkillSource:
    """A resolved set of skill directories.

    Attributes:
        kind: ``vendored`` or ``checkout``.
        root: Directory the skills were read from.
        skills: Mapping of skill identifier to directory.
    """

    kind: str
    root: Path
    skills: dict[str, Path]

    def path_for(self, skill_id: str) -> Path | None:
        """Return the directory of a skill, or ``None`` when it is not present."""
        return self.skills.get(skill_id)

    def missing(self, skill_ids: tuple[str, ...]) -> list[str]:
        """Return the identifiers of skills that are not available."""
        return [skill_id for skill_id in skill_ids if skill_id not in self.skills]


def resolve_source(checkout: Path | None = None) -> SkillSource:
    """Return the best available skill source.

    A checkout is preferred when given, so that development happens against
    the working copy of the skills repository.
    """
    if checkout is not None:
        return load_checkout(checkout)
    return load_vendored()


def load_vendored() -> SkillSource:
    """Return the vendored skill source.

    An empty source is returned when the package was installed without a
    vendored snapshot, for example from a source checkout.
    """
    root = vendored_root()
    skills: dict[str, Path] = {}
    if root.is_dir():
        for source_dir in sorted(p for p in root.iterdir() if p.is_dir()):
            for skill_dir in sorted(p for p in source_dir.iterdir() if p.is_dir()):
                if (skill_dir / "SKILL.md").is_file():
                    skills[skill_dir.name] = skill_dir
    return SkillSource(kind="vendored", root=root, skills=skills)


def vendored_root() -> Path:
    """Return the directory of the vendored skill snapshot inside the package."""
    resource = files(VENDOR_PACKAGE).joinpath(VENDOR_DIR)
    return Path(str(resource))


def load_checkout(checkout: Path) -> SkillSource:
    """Return a skill source backed by a local checkout.

    The checkout may either contain the layer layout
    ``<checkout>/skills/<layer>/<skill-id>/`` or hold skill directories
    directly in ``<checkout>/skills/``.

    Raises:
        FileNotFoundError: If the checkout has no ``skills`` directory.
    """
    root = Path(checkout)
    skills_root = root / "skills"
    if not skills_root.is_dir():
        msg = f"No 'skills' directory in checkout: {root}"
        raise FileNotFoundError(msg)

    skills: dict[str, Path] = {}
    for layer_dir in sorted(p for p in skills_root.iterdir() if p.is_dir()):
        for skill_dir in sorted(p for p in layer_dir.iterdir() if p.is_dir()):
            if (skill_dir / "SKILL.md").is_file():
                skills[skill_dir.name] = skill_dir
                continue
        if (layer_dir / "SKILL.md").is_file():
            skills[layer_dir.name] = layer_dir

    return SkillSource(kind="checkout", root=root, skills=skills)


def hash_skill(directory: Path) -> str:
    """Return a stable hash of a skill directory.

    The hash covers the relative path and the content of every file, so that
    an update detects changes in references and assets as well.

    Line endings are normalized for text files. A checkout that converts the
    line endings on the way out (git with ``core.autocrlf``) then hashes the
    same as the repository it was cloned from, and the status stays quiet.
    """
    digest = hashlib.sha256()
    for path in sorted(p for p in directory.rglob("*") if p.is_file()):
        if path.name in HASH_EXCLUDED_NAMES:
            continue
        relative = path.relative_to(directory).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(_normalized_bytes(path))
        digest.update(b"\0")
    return digest.hexdigest()


def _normalized_bytes(path: Path) -> bytes:
    """Return the file content with normalized line endings for text files.

    Binary files (templates, images) are returned unchanged. A file is
    treated as text when it decodes as UTF-8 and holds no null byte.
    """
    data = path.read_bytes()
    if b"\0" in data:
        return data
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
