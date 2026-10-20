"""Tests for the manifest."""

from __future__ import annotations

import json

from opencode_sdo_writer.manifest import Manifest, load_manifest, save_manifest


def test_round_trip(tmp_path) -> None:
    path = tmp_path / "sdo-writer.json"
    manifest = Manifest(profile="etsi", source="vendored:/x", skills={"a": "hash"})
    save_manifest(path, manifest)

    loaded = load_manifest(path)
    assert loaded is not None
    assert loaded.profile == "etsi"
    assert loaded.source == "vendored:/x"
    assert loaded.skills == {"a": "hash"}
    assert loaded.installed_skills == ["a"]
    assert loaded.installed_at


def test_missing_manifest(tmp_path) -> None:
    assert load_manifest(tmp_path / "nope.json") is None


def test_broken_manifest(tmp_path) -> None:
    path = tmp_path / "sdo-writer.json"
    path.write_text("{not json", encoding="utf-8")
    assert load_manifest(path) is None


def test_manifest_with_wrong_types(tmp_path) -> None:
    path = tmp_path / "sdo-writer.json"
    path.write_text(json.dumps({"skills": "not a dict", "agent": 5}), encoding="utf-8")
    manifest = load_manifest(path)
    assert manifest is not None
    assert manifest.skills == {}
    assert manifest.agent is None


def test_manifest_that_is_not_an_object(tmp_path) -> None:
    path = tmp_path / "sdo-writer.json"
    path.write_text(json.dumps([1, 2, 3]), encoding="utf-8")
    assert load_manifest(path) is None
