"""Tests for the filesystem locations."""

from __future__ import annotations

from pathlib import Path

from opencode_sdo_writer.paths import (
    GLOBAL_CONFIG_ENV,
    agents_dir,
    global_config_dir,
    manifest_path,
    project_config_dir,
    skills_dir,
)


def test_global_config_dir_uses_xdg_config_home(monkeypatch) -> None:
    monkeypatch.setenv(GLOBAL_CONFIG_ENV, "/tmp/xdg")
    assert global_config_dir() == Path("/tmp/xdg/opencode")


def test_global_config_dir_falls_back_to_home(monkeypatch) -> None:
    monkeypatch.delenv(GLOBAL_CONFIG_ENV, raising=False)
    assert global_config_dir() == Path.home() / ".config" / "opencode"


def test_project_config_dir_for_a_project() -> None:
    assert project_config_dir(Path("/work/project")) == Path("/work/project/.opencode")


def test_project_config_dir_defaults_to_the_working_directory() -> None:
    assert project_config_dir() == Path.cwd() / ".opencode"


def test_sub_directories() -> None:
    root = Path("/cfg")
    assert skills_dir(root) == Path("/cfg/skills")
    assert agents_dir(root) == Path("/cfg/agents")
    assert manifest_path(root) == Path("/cfg/sdo-writer.json")
