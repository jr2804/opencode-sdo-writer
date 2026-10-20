"""Tests for the lock file."""

from __future__ import annotations

import pytest

from opencode_sdo_writer.lockfile import LockError, load_lock


def test_packaged_lock_has_sources_and_skills() -> None:
    lock = load_lock()
    assert lock.version == 1
    assert {source.id for source in lock.sources} >= {"sdo-skills"}
    assert lock.skills


def test_skills_for_layers_filters_and_keeps_order() -> None:
    lock = load_lock()
    common = [skill.id for skill in lock.skills_for_layers(("common",))]
    assert "sdo-writing" in common
    assert all(skill.layer == "common" for skill in lock.skills_for_layers(("common",)))
    assert lock.skills_for_layers(()) == []


def test_skill_lookup() -> None:
    lock = load_lock()
    assert lock.skill("sdo-writing").layer == "common"
    with pytest.raises(KeyError):
        lock.skill("does-not-exist")


def test_source_lookup() -> None:
    lock = load_lock()
    assert lock.source("sdo-skills").ref
    with pytest.raises(KeyError):
        lock.source("does-not-exist")


def test_missing_lock_file(tmp_path) -> None:
    with pytest.raises(LockError, match="not found"):
        load_lock(tmp_path / "nope.lock")


def test_broken_lock_file(tmp_path) -> None:
    broken = tmp_path / "vendor.lock"
    broken.write_text("this is not toml = = =", encoding="utf-8")
    with pytest.raises(LockError, match="not valid TOML"):
        load_lock(broken)


def test_lock_without_skills(tmp_path) -> None:
    empty = tmp_path / "vendor.lock"
    empty.write_text('version = 1\n\n[[source]]\nid = "x"\nrepo = "y"\nref = "z"\n', encoding="utf-8")
    with pytest.raises(LockError, match="does not define any skill"):
        load_lock(empty)
