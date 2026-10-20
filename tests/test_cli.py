"""Tests for the command line interface."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from opencode_sdo_writer.cli.app import app
from opencode_sdo_writer.lockfile import load_lock

runner = CliRunner()


def test_profiles_lists_all_bundled_profiles() -> None:
    result = runner.invoke(app, ["profiles"])
    assert result.exit_code == 0
    for profile_id in ("etsi", "3gpp", "itut"):
        assert profile_id in result.output


def test_init_without_profile_lists_them() -> None:
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 1
    assert "Available profiles" in result.output


def test_init_with_unknown_profile() -> None:
    result = runner.invoke(app, ["init", "--profile", "nope"])
    assert result.exit_code == 1
    assert "Unknown profile" in result.output


def test_init_installs_a_profile(config) -> None:
    result = runner.invoke(app, ["init", "--profile", "etsi", "--config", str(config)])
    assert result.exit_code == 0
    assert "Installed" in result.output
    assert (config / "skills" / "sdo-writing" / "SKILL.md").is_file()
    assert (config / "agents" / "sdo-writer.md").is_file()


def test_init_dry_run_writes_nothing(config) -> None:
    result = runner.invoke(app, ["init", "--profile", "etsi", "--config", str(config), "--dry-run"])
    assert result.exit_code == 0
    assert "Would install" in result.output
    assert not config.exists()


def test_init_with_a_checkout_source(tmp_path, config) -> None:
    checkout = _full_checkout(tmp_path / "checkout")

    result = runner.invoke(app, ["init", "--profile", "etsi", "--config", str(config), "--source", str(checkout)])
    assert result.exit_code == 0
    assert (config / "skills" / "sdo-writing" / "SKILL.md").is_file()
    assert (config / "skills" / "etsi-tools" / "SKILL.md").is_file()


def _full_checkout(root: Path) -> Path:
    """Create a checkout layout that holds every skill of the lock file."""
    for entry in load_lock().skills:
        skill_dir = root / "skills" / entry.layer / entry.id
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(f"---\nname: {entry.id}\n---\nbody\n", encoding="utf-8")
    return root


def test_init_with_a_partial_checkout_reports_missing(tmp_path, config) -> None:
    checkout = tmp_path / "checkout"
    skill_dir = checkout / "skills" / "common" / "sdo-writing"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: sdo-writing\n---\ntext\n", encoding="utf-8")

    result = runner.invoke(app, ["init", "--profile", "etsi", "--config", str(config), "--source", str(checkout)])
    assert result.exit_code == 1
    assert "Missing" in result.output
    assert (config / "skills" / "sdo-writing" / "SKILL.md").is_file()


def test_init_with_a_broken_source(tmp_path, config) -> None:
    result = runner.invoke(app, ["init", "--profile", "etsi", "--config", str(config), "--source", str(tmp_path / "nope")])
    assert result.exit_code == 1
    assert "Error" in result.output


def test_status_without_install(config) -> None:
    result = runner.invoke(app, ["status", "--config", str(config)])
    assert result.exit_code == 1
    assert "Nothing installed" in result.output


def test_status_after_install(config) -> None:
    runner.invoke(app, ["init", "--profile", "etsi", "--config", str(config)])
    result = runner.invoke(app, ["status", "--config", str(config)])
    assert result.exit_code == 0
    assert "sdo-writing" in result.output


def test_update_is_idempotent(config) -> None:
    runner.invoke(app, ["init", "--profile", "etsi", "--config", str(config)])
    result = runner.invoke(app, ["update", "--profile", "etsi", "--config", str(config)])
    assert result.exit_code == 0
    assert "Unchanged" in result.output


def test_uninstall(config) -> None:
    runner.invoke(app, ["init", "--profile", "etsi", "--config", str(config)])
    result = runner.invoke(app, ["uninstall", "--config", str(config)])
    assert result.exit_code == 0
    assert "Removed" in result.output
    assert not (config / "skills" / "sdo-writing").exists()


def test_uninstall_without_install(config) -> None:
    result = runner.invoke(app, ["uninstall", "--config", str(config)])
    assert result.exit_code == 0
    assert "Nothing to remove" in result.output


def test_project_scope(tmp_path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    result = runner.invoke(app, ["init", "--profile", "itut", "--project", str(project)])
    assert result.exit_code == 0
    assert (project / ".opencode" / "skills" / "itut-reference" / "SKILL.md").is_file()


def test_version_flag() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.output.strip()
