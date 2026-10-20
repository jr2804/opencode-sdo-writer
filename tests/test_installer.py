"""Tests for the installer."""

from __future__ import annotations

from pathlib import Path

import pytest

from opencode_sdo_writer.installer import install, status, uninstall, wanted_skills
from opencode_sdo_writer.lockfile import LockFile, SkillEntry, Source
from opencode_sdo_writer.profile import load_profile
from opencode_sdo_writer.sources import SkillSource


def test_wanted_skills_follows_layers_and_extras(lock) -> None:
    profile = load_profile("etsi")
    wanted = wanted_skills(lock, profile)
    assert "sdo-writing" in wanted
    assert "etsi-tools" in wanted
    assert "etsi-portal-tool" in wanted
    assert wanted.count("etsi-portal-tool") == 1


def test_install_writes_skills_and_agent(tmp_path, lock, source) -> None:
    profile = load_profile("etsi")
    config = tmp_path / "config"
    report = install(profile, config, source, lock)

    assert report.installed
    assert not report.missing
    assert report.agent_path is not None
    assert report.agent_path.is_file()
    assert (config / "skills" / "sdo-writing" / "SKILL.md").is_file()
    assert (config / "sdo-writer.json").is_file()
    assert report.changed == len(report.installed)


def test_second_install_reports_unchanged(tmp_path, lock, source) -> None:
    profile = load_profile("etsi")
    config = tmp_path / "config"
    install(profile, config, source, lock)
    report = install(profile, config, source, lock)

    assert not report.installed
    assert not report.updated
    assert report.unchanged


def test_changed_skill_is_updated(tmp_path, lock, source) -> None:
    profile = load_profile("etsi")
    config = tmp_path / "config"
    install(profile, config, source, lock)

    _skill(source.root, "sdo-writing", body="two")
    report = install(profile, config, source, lock)

    assert "sdo-writing" in report.updated
    assert "two" in (config / "skills" / "sdo-writing" / "SKILL.md").read_text(encoding="utf-8")


def test_switching_profile_removes_old_skills(tmp_path, lock, source) -> None:
    config = tmp_path / "config"
    install(load_profile("etsi"), config, source, lock)
    report = install(load_profile("itut"), config, source, lock)

    assert "etsi-tools" in report.removed
    assert not (config / "skills" / "etsi-tools").exists()
    assert (config / "skills" / "sdo-writing").exists()


def test_foreign_directory_is_not_touched(tmp_path, lock, source) -> None:
    profile = load_profile("etsi")
    config = tmp_path / "config"
    foreign = config / "skills" / "sdo-writing"
    _skill(config / "skills", "sdo-writing", body="mine")

    report = install(profile, config, source, lock)

    assert "sdo-writing" in report.conflicts
    assert "mine" in (foreign / "SKILL.md").read_text(encoding="utf-8")


def test_force_overwrites_foreign_directory(tmp_path, lock, source) -> None:
    profile = load_profile("etsi")
    config = tmp_path / "config"
    _skill(config / "skills", "sdo-writing", body="mine")

    report = install(profile, config, source, lock, force=True)

    assert "sdo-writing" not in report.conflicts
    assert "one" in (config / "skills" / "sdo-writing" / "SKILL.md").read_text(encoding="utf-8")


def test_missing_skill_is_reported(tmp_path, lock, source) -> None:
    profile = load_profile("etsi")
    config = tmp_path / "config"
    without_meeting_report = SkillSource(
        kind="vendored",
        root=source.root,
        skills={k: v for k, v in source.skills.items() if k != "etsi-meeting-report"},
    )
    report = install(profile, config, without_meeting_report, lock)

    assert report.missing
    assert not report.ok


def test_missing_skill_keeps_the_previous_copy(tmp_path, lock, source) -> None:
    profile = load_profile("etsi")
    config = tmp_path / "config"
    install(profile, config, source, lock)

    without_meeting_report = SkillSource(
        kind="vendored",
        root=source.root,
        skills={k: v for k, v in source.skills.items() if k != "etsi-meeting-report"},
    )
    report = install(profile, config, without_meeting_report, lock)

    assert report.missing == ["etsi-meeting-report"]
    assert (config / "skills" / "etsi-meeting-report" / "SKILL.md").is_file()


def test_agent_can_be_skipped(tmp_path, lock, source) -> None:
    config = tmp_path / "config"
    report = install(load_profile("etsi"), config, source, lock, write_agent=False)
    assert report.agent_path is None
    assert not (config / "agents").exists()


def test_status_detects_drift(tmp_path, lock, source) -> None:
    config = tmp_path / "config"
    install(load_profile("etsi"), config, source, lock)

    manifest, drifted = status(config)
    assert manifest is not None
    assert not drifted

    (config / "skills" / "sdo-writing" / "SKILL.md").write_text("changed\n", encoding="utf-8")
    _, drifted = status(config)
    assert "sdo-writing" in drifted


def test_status_without_install(tmp_path) -> None:
    manifest, drifted = status(tmp_path / "nothing")
    assert manifest is None
    assert not drifted


def test_uninstall_removes_everything(tmp_path, lock, source) -> None:
    config = tmp_path / "config"
    install(load_profile("etsi"), config, source, lock)

    removed, agent_path = uninstall(config)

    assert removed
    assert agent_path is not None
    assert not agent_path.exists()
    assert not (config / "sdo-writer.json").exists()
    assert not (config / "skills" / "sdo-writing").exists()


@pytest.fixture
def lock() -> LockFile:
    return LockFile(
        version=1,
        sources=(Source(id="sdo-skills", repo="https://example.invalid/repo.git", ref="v1"),),
        skills=(
            SkillEntry(id="sdo-writing", layer="common", source="sdo-skills"),
            SkillEntry(id="sdo-docx", layer="common", source="sdo-skills"),
            SkillEntry(id="etsi-tools", layer="etsi", source="sdo-skills"),
            SkillEntry(id="etsi-portal-tool", layer="tools", source="sdo-skills"),
        ),
    )


@pytest.fixture
def source(tmp_path) -> SkillSource:
    root = tmp_path / "src"
    for skill_id in ("sdo-writing", "sdo-docx", "etsi-tools", "etsi-portal-tool", "etsi-meeting-report"):
        _skill(root, skill_id)
    return SkillSource(
        kind="vendored",
        root=root,
        skills={skill_id: root / skill_id for skill_id in ("sdo-writing", "sdo-docx", "etsi-tools", "etsi-portal-tool", "etsi-meeting-report")},
    )


def _skill(root: Path, skill_id: str, body: str = "one") -> Path:
    skill_dir = root / skill_id
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(f"---\nname: {skill_id}\n---\n{body}\n", encoding="utf-8")
    return skill_dir


def test_uninstall_without_install(tmp_path) -> None:
    removed, agent_path = uninstall(tmp_path)
    assert not removed
    assert agent_path is None
