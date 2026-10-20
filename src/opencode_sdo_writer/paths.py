"""Filesystem locations used by the installer.

OpenCode keeps two kinds of configuration:

* the **global** configuration in ``~/.config/opencode`` (or
  ``$XDG_CONFIG_HOME/opencode``), which every project sees, and
* the **project** configuration in ``<project>/.opencode``.

Both hold a ``skills/`` directory and an ``agents/`` directory, so the
installer only has to decide which root it works in.
"""

from __future__ import annotations

import os
from pathlib import Path

GLOBAL_CONFIG_ENV = "XDG_CONFIG_HOME"


def global_config_dir() -> Path:
    """Return the OpenCode global configuration directory.

    ``XDG_CONFIG_HOME`` wins when it is set, otherwise ``~/.config`` is used.
    """
    xdg = os.environ.get(GLOBAL_CONFIG_ENV)
    base = Path(xdg) if xdg else Path.home() / ".config"
    return base / "opencode"


def project_config_dir(project: Path | None = None) -> Path:
    """Return the OpenCode configuration directory of a project."""
    root = project if project is not None else Path.cwd()
    return root / ".opencode"


def skills_dir(config_dir: Path) -> Path:
    """Return the skills directory inside an OpenCode configuration directory."""
    return config_dir / "skills"


def agents_dir(config_dir: Path) -> Path:
    """Return the agents directory inside an OpenCode configuration directory."""
    return config_dir / "agents"


def manifest_path(config_dir: Path) -> Path:
    """Return the path of the installer manifest inside a configuration directory."""
    return config_dir / "sdo-writer.json"
