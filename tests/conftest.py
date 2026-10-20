"""Shared test fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def config(tmp_path) -> Path:
    """Return an empty OpenCode configuration directory."""
    return tmp_path / "config"
