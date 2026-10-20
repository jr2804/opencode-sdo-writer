"""Tests for the package entry points."""

from __future__ import annotations

import importlib
import importlib.metadata
import runpy

import pytest

import opencode_sdo_writer


def test_version_is_exposed() -> None:

    assert opencode_sdo_writer.__version__


def test_about_module() -> None:
    about = importlib.import_module("opencode_sdo_writer.__about__")

    assert about.__title__ == "opencode_sdo_writer"
    assert about.__license__ == "MIT"
    assert about.__author__ == "Jan.Reimes"
    assert about.__version__


def test_version_falls_back_when_the_package_is_missing(monkeypatch) -> None:

    def boom(name: str) -> str:
        msg = "not found"
        raise importlib.metadata.PackageNotFoundError(msg)

    monkeypatch.setattr(importlib.metadata, "version", boom)
    reloaded = importlib.reload(opencode_sdo_writer)
    try:
        assert reloaded.__version__ == "0.0.0"
    finally:
        monkeypatch.undo()
        importlib.reload(opencode_sdo_writer)


def test_module_can_be_run(monkeypatch) -> None:

    monkeypatch.setattr("sys.argv", ["opencode-sdo-writer", "--version"])
    with pytest.raises(SystemExit):
        runpy.run_module("opencode_sdo_writer", run_name="__main__")
