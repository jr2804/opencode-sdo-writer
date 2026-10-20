"""Tests for the skill sources."""

from __future__ import annotations

from pathlib import Path

import pytest

from opencode_sdo_writer.sources import (
    hash_skill,
    load_checkout,
    load_vendored,
    resolve_source,
)


def test_vendored_source_is_not_empty() -> None:
    source = load_vendored()
    assert source.kind == "vendored"
    assert "sdo-writing" in source.skills
    writing = source.path_for("sdo-writing")
    assert writing is not None
    assert writing.is_dir()
    assert source.path_for("does-not-exist") is None
    assert source.missing(("sdo-writing", "nope")) == ["nope"]


def test_checkout_source_with_layers(tmp_path) -> None:
    _make_skill(tmp_path / "skills" / "common", "alpha")
    _make_skill(tmp_path / "skills" / "etsi", "beta")
    source = load_checkout(tmp_path)
    assert source.kind == "checkout"
    assert set(source.skills) == {"alpha", "beta"}


def test_checkout_source_with_flat_layout(tmp_path) -> None:
    _make_skill(tmp_path / "skills", "alpha")
    source = load_checkout(tmp_path)
    assert set(source.skills) == {"alpha"}


def test_checkout_without_skills_directory(tmp_path) -> None:
    with pytest.raises(FileNotFoundError, match="No 'skills' directory"):
        load_checkout(tmp_path)


def test_resolve_source_prefers_checkout(tmp_path) -> None:
    _make_skill(tmp_path / "skills" / "common", "alpha")
    assert resolve_source(tmp_path).kind == "checkout"
    assert resolve_source().kind == "vendored"


def test_hash_skill_detects_changes(tmp_path) -> None:
    skill_dir = _make_skill(tmp_path, "alpha")
    first = hash_skill(skill_dir)
    assert first == hash_skill(skill_dir)
    (skill_dir / "SKILL.md").write_text("---\nname: alpha\n---\nchanged\n", encoding="utf-8")
    assert hash_skill(skill_dir) != first


def test_hash_skill_ignores_noise_files(tmp_path) -> None:
    skill_dir = _make_skill(tmp_path, "alpha")
    first = hash_skill(skill_dir)
    (skill_dir / ".DS_Store").write_bytes(b"junk")
    assert hash_skill(skill_dir) == first


def test_hash_skill_covers_references(tmp_path) -> None:
    skill_dir = _make_skill(tmp_path, "alpha")
    first = hash_skill(skill_dir)
    (skill_dir / "references").mkdir()
    (skill_dir / "references" / "note.md").write_text("note\n", encoding="utf-8")
    assert hash_skill(skill_dir) != first


def test_hash_skill_ignores_line_endings(tmp_path) -> None:
    skill_dir = tmp_path / "alpha"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_bytes(b"---\nname: alpha\n---\ntext\n")
    first = hash_skill(skill_dir)
    (skill_dir / "SKILL.md").write_bytes(b"---\r\nname: alpha\r\n---\r\ntext\r\n")
    assert hash_skill(skill_dir) == first


def test_hash_skill_keeps_binary_files_apart(tmp_path) -> None:
    skill_dir = _make_skill(tmp_path, "alpha")
    (skill_dir / "template.docx").write_bytes(b"PK\x03\x04\x00binary")
    first = hash_skill(skill_dir)
    (skill_dir / "template.docx").write_bytes(b"PK\x03\x04\x00other")
    assert hash_skill(skill_dir) != first


def test_hash_skill_treats_undecodable_files_as_binary(tmp_path) -> None:
    skill_dir = _make_skill(tmp_path, "alpha")
    (skill_dir / "legacy.dat").write_bytes(b"\xff\xfe\xfa")
    first = hash_skill(skill_dir)
    (skill_dir / "legacy.dat").write_bytes(b"\xff\xfe\xfb")
    assert hash_skill(skill_dir) != first


def _make_skill(root: Path, skill_id: str, body: str = "text") -> Path:
    skill_dir = root / skill_id
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(f"---\nname: {skill_id}\n---\n{body}\n", encoding="utf-8")
    return skill_dir
