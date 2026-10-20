"""Tests for the profiles."""

from __future__ import annotations

import dataclasses

import pytest

import opencode_sdo_writer.profile as module
from opencode_sdo_writer.profile import ProfileError, available_profiles, load_profile


def test_bundled_profiles() -> None:
    assert available_profiles() == ["3gpp", "etsi", "itut"]


@pytest.mark.parametrize("profile_id", ["3gpp", "etsi", "itut"])
def test_load_bundled_profile(profile_id: str) -> None:
    profile = load_profile(profile_id)
    assert profile.id == profile_id
    assert profile.title
    assert profile.description
    assert profile.agent_name == "sdo-writer"
    assert profile.mode == "primary"
    assert profile.color.startswith("#")
    assert "common" in profile.skill_layers
    assert profile.skill_layers[0] == "common"
    assert profile.notes.strip()


def test_unknown_profile() -> None:
    with pytest.raises(ProfileError, match="Unknown profile"):
        load_profile("nope")


def test_common_layer_is_always_first() -> None:
    profile = load_profile("etsi")
    without_common = dataclasses.replace(profile, layers=("etsi",))
    assert without_common.skill_layers == ("common", "etsi")


def test_broken_profile(tmp_path, monkeypatch) -> None:

    class FakeFile:
        def is_file(self) -> bool:
            return True

        def read_text(self, encoding: str = "utf-8") -> str:
            return "title = 'x'\n"

    class FakeDir:
        def joinpath(self, name: str) -> FakeFile:
            return FakeFile()

        def iterdir(self):
            return []

    monkeypatch.setattr(module, "files", lambda package: FakeDir())
    with pytest.raises(ProfileError, match="missing 'description'"):
        module.load_profile("etsi")


def test_profile_with_invalid_toml(monkeypatch) -> None:
    _fake_files(monkeypatch, "title = 'x\n")
    with pytest.raises(ProfileError, match="is not valid TOML"):
        load_profile("etsi")


def test_profile_with_malformed_sections(monkeypatch) -> None:
    _fake_files(monkeypatch, "title = 'x'\ndescription = 'y'\nagent = 'not a table'\n")
    with pytest.raises(ProfileError, match="malformed"):
        load_profile("etsi")


def test_profile_with_a_non_numeric_temperature(monkeypatch) -> None:
    _fake_files(monkeypatch, "title = 'x'\ndescription = 'y'\n[agent]\ntemperature = 'warm'\n")
    with pytest.raises(ProfileError, match="non-numeric"):
        load_profile("etsi")


def _fake_files(monkeypatch, content: str) -> None:
    """Make the profile package serve a fixed TOML text."""

    class FakeFile:
        def is_file(self) -> bool:
            return True

        def read_text(self, encoding: str = "utf-8") -> str:
            return content

    class FakeDir:
        def joinpath(self, name: str) -> FakeFile:
            return FakeFile()

        def iterdir(self):
            return []

    monkeypatch.setattr(module, "files", lambda package: FakeDir())


def test_profile_defaults() -> None:

    profile = module._build("x", {"title": "T", "description": "D"})
    assert profile.agent_name == "sdo-writer"
    assert profile.mode == "primary"
    assert profile.color == "#2f6f9f"
    assert profile.layers == ("common",)
    assert profile.extra_skills == ()
    assert profile.tools_allow == ()
    assert profile.notes == ""
    assert profile.temperature == 0.1
