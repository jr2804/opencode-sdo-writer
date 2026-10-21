"""Tests for the failure paths of the command line interface."""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from opencode_sdo_writer.cli import app as app_module, commands as commands_module
from opencode_sdo_writer.cli.app import app
from opencode_sdo_writer.lockfile import LockError, load_lock
from opencode_sdo_writer.profile import ProfileError
from opencode_sdo_writer.sources import load_checkout

runner = CliRunner()


def test_broken_profile_is_reported(monkeypatch, config) -> None:
    def boom(profile_id: str):
        msg = "profile is broken"
        raise ProfileError(msg)

    monkeypatch.setattr(commands_module, "load_profile", boom)
    result = runner.invoke(app, ["init", "--profile", "etsi", "--config", str(config)])
    assert result.exit_code == 1
    assert "profile is broken" in result.output


def test_broken_lock_file_is_reported(monkeypatch, config) -> None:
    def boom(path=None):
        msg = "lock file is broken"
        raise LockError(msg)

    monkeypatch.setattr(commands_module, "load_lock", boom)
    result = runner.invoke(app, ["init", "--profile", "etsi", "--config", str(config)])
    assert result.exit_code == 1
    assert "lock file is broken" in result.output


def test_source_without_skills_is_reported(tmp_path, config) -> None:
    empty = tmp_path / "empty"
    (empty / "skills").mkdir(parents=True)
    result = runner.invoke(app, ["init", "--profile", "etsi", "--config", str(config), "--source", str(empty)])
    assert result.exit_code == 1
    assert "no skills found" in result.output


def test_dry_run_reports_missing_skills(tmp_path, config) -> None:
    checkout = _partial_checkout(tmp_path / "checkout")
    result = runner.invoke(
        app,
        ["init", "--profile", "etsi", "--config", str(config), "--source", str(checkout), "--dry-run"],
    )
    assert result.exit_code == 0
    assert "Missing from source" in result.output
    assert "sdo-docx" in result.output


def _partial_checkout(root: Path) -> Path:
    """Create a checkout with a single skill."""
    skill_dir = root / "skills" / "common" / "sdo-writing"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: sdo-writing\n---\ntext\n", encoding="utf-8")
    return root


def test_status_reports_drift(tmp_path, config) -> None:

    checkout = tmp_path / "checkout"
    for entry in load_lock().skills:
        skill_dir = checkout / "skills" / entry.layer / entry.id
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(f"---\nname: {entry.id}\n---\nbody\n", encoding="utf-8")

    result = runner.invoke(app, ["init", "--profile", "etsi", "--config", str(config), "--source", str(checkout)])
    assert result.exit_code == 0

    (config / "skills" / "sdo-writing" / "SKILL.md").write_text("changed\n", encoding="utf-8")
    result = runner.invoke(app, ["status", "--config", str(config)])

    assert result.exit_code == 0
    assert "Changed on disk" in result.output
    assert "sdo-writing" in result.output
    assert load_checkout(checkout).kind == "checkout"


def test_init_without_a_config_option_uses_the_global_directory(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    result = runner.invoke(app, ["init", "--profile", "etsi", "--dry-run"])
    assert result.exit_code == 0
    assert str(tmp_path / "opencode") in result.output


def test_version_falls_back_when_the_package_is_not_installed(monkeypatch) -> None:
    def boom(name: str) -> str:
        msg = "not installed"
        raise RuntimeError(msg)

    monkeypatch.setattr(app_module, "version", boom)
    assert app_module._get_version() == "0.0.0"


def test_main_entry_point(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["opencode-sdo-writer", "--version"])
    with pytest.raises(SystemExit):
        app_module.main()
