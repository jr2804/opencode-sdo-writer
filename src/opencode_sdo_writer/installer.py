"""Installing, updating and removing the writer.

The installer only ever touches what a previous install put on disk. Skills
that the user added themselves are never modified or removed; when an
installed skill name collides with a foreign directory, the install reports
the conflict and leaves the directory alone.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from .agent import render_agent
from .lockfile import LockFile
from .manifest import Manifest, load_manifest, save_manifest
from .paths import agents_dir, manifest_path, skills_dir
from .profile import Profile
from .sources import SkillSource, hash_skill

#: Files that are never copied into the configuration directory.
COPY_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".DS_Store")


@dataclass
class InstallReport:
    """What an install or update did.

    Attributes:
        profile: Identifier of the profile that was installed.
        config_dir: OpenCode configuration directory that was written to.
        installed: Skills that were newly added.
        updated: Skills whose content changed.
        unchanged: Skills that were already up to date.
        removed: Skills that a previous install had put there but that the
            profile no longer contains.
        missing: Skills the profile asks for that the source does not provide.
        conflicts: Skill directories that already existed and were not written.
        agent_path: Path of the installed agent file.
    """

    profile: str
    config_dir: Path
    installed: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    agent_path: Path | None = None

    @property
    def changed(self) -> int:
        """Return the number of skills that were written."""
        return len(self.installed) + len(self.updated)

    @property
    def ok(self) -> bool:
        """Return whether the install completed without missing skills."""
        return not self.missing


def install(
    profile: Profile,
    config_dir: Path,
    source: SkillSource,
    lock: LockFile,
    *,
    force: bool = False,
    write_agent: bool = True,
) -> InstallReport:
    """Install a profile into an OpenCode configuration directory.

    Args:
        profile: The profile to install.
        config_dir: The OpenCode configuration directory to write to.
        source: Where the skill content comes from.
        lock: The lock file, used to map profiles to skills.
        force: Overwrite skill directories that the installer did not create.
        write_agent: Whether to write the agent file.

    Returns:
        A report of what was done.
    """
    report = InstallReport(profile=profile.id, config_dir=config_dir)
    target_root = skills_dir(config_dir)
    target_root.mkdir(parents=True, exist_ok=True)

    manifest_file = manifest_path(config_dir)
    previous = load_manifest(manifest_file)
    previous_skills = previous.skills if previous else {}

    wanted = wanted_skills(lock, profile)
    installed: dict[str, str] = {}

    for skill_id in wanted:
        source_dir = source.path_for(skill_id)
        if source_dir is None:
            report.missing.append(skill_id)
            if skill_id in previous_skills:
                installed[skill_id] = previous_skills[skill_id]
            continue

        target_dir = target_root / skill_id
        if target_dir.exists() and skill_id not in previous_skills and not force:
            report.conflicts.append(skill_id)
            continue

        digest = hash_skill(source_dir)
        if target_dir.exists() and hash_skill(target_dir) == digest:
            report.unchanged.append(skill_id)
            installed[skill_id] = digest
            continue

        _copy_skill(source_dir, target_dir)
        installed[skill_id] = digest
        if skill_id in previous_skills:
            report.updated.append(skill_id)
        else:
            report.installed.append(skill_id)

    for skill_id in previous_skills:
        if skill_id in installed or skill_id in report.missing:
            continue
        target_dir = target_root / skill_id
        if target_dir.is_dir():
            shutil.rmtree(target_dir)
        report.removed.append(skill_id)

    if write_agent:
        agent_path = agents_dir(config_dir) / f"{profile.agent_name}.md"
        agent_path.parent.mkdir(parents=True, exist_ok=True)
        agent_path.write_text(render_agent(profile, tuple(installed)), encoding="utf-8")
        report.agent_path = agent_path

    manifest = Manifest(
        profile=profile.id,
        source=f"{source.kind}:{source.root}",
        installed_at=datetime.now(UTC).isoformat(timespec="seconds"),
        skills=installed,
        agent=f"{profile.agent_name}.md" if write_agent else None,
    )
    save_manifest(manifest_file, manifest)

    return report


def wanted_skills(lock: LockFile, profile: Profile) -> list[str]:
    """Return the identifiers of the skills a profile wants, in a stable order."""
    ids = [entry.id for entry in lock.skills_for_layers(profile.skill_layers)]
    for skill_id in profile.extra_skills:
        if skill_id not in ids:
            ids.append(skill_id)
    return ids


def _copy_skill(source_dir: Path, target_dir: Path) -> None:
    """Copy a skill directory, replacing an existing one."""
    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(source_dir, target_dir, ignore=COPY_IGNORE)


def uninstall(config_dir: Path) -> tuple[list[str], Path | None]:
    """Remove everything a previous install put on disk.

    Returns:
        The identifiers of the removed skills and the path of the removed
        agent file.
    """
    manifest_file = manifest_path(config_dir)
    manifest = load_manifest(manifest_file)
    if manifest is None:
        return [], None

    removed: list[str] = []
    target_root = skills_dir(config_dir)
    for skill_id in manifest.skills:
        target_dir = target_root / skill_id
        if target_dir.is_dir():
            shutil.rmtree(target_dir)
        removed.append(skill_id)

    agent_path: Path | None = None
    if manifest.agent:
        candidate = agents_dir(config_dir) / manifest.agent
        if candidate.is_file():
            candidate.unlink()
            agent_path = candidate

    manifest_file.unlink(missing_ok=True)
    return removed, agent_path


def status(config_dir: Path) -> tuple[Manifest | None, list[str]]:
    """Return the manifest and the skills whose content drifted.

    Returns:
        The manifest, or ``None`` when nothing is installed, and the list of
        skills whose files no longer match the recorded hash.
    """
    manifest = load_manifest(manifest_path(config_dir))
    if manifest is None:
        return None, []

    drifted: list[str] = []
    target_root = skills_dir(config_dir)
    for skill_id, digest in manifest.skills.items():
        target_dir = target_root / skill_id
        if not target_dir.is_dir() or hash_skill(target_dir) != digest:
            drifted.append(skill_id)
    return manifest, drifted
