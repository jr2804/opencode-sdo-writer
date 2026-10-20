"""Typer CLI app for OpenCode SDO Writer."""

from __future__ import annotations

from importlib.metadata import version

import typer

from opencode_sdo_writer.cli import commands

app = typer.Typer(
    name="opencode_sdo_writer",
    help="OpenCode agent and profiles for writing standards contributions and deliverables (ETSI, 3GPP, ITU-T)",
    add_completion=True,
    no_args_is_help=True,
)

# Register commands. Commands are plain functions in commands.py - no
# @app.command() decorators there, no import of `app`: this avoids the
# circular import (commands.py <-> app.py) and keeps pyreorder from
# re-sorting this file into a broken state.
app.command()(commands.profiles)
app.command()(commands.init)
app.command()(commands.update)
app.command()(commands.status)
app.command()(commands.uninstall)


@app.callback(invoke_without_command=True)
def _callback(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit",
        is_eager=True,
    ),
) -> None:
    """OpenCode agent and profiles for writing standards contributions and deliverables (ETSI, 3GPP, ITU-T)"""
    if version:
        typer.echo(_get_version())
        raise typer.Exit()


# Version management
def _get_version() -> str:
    """Get application version from package metadata."""
    try:
        return version("opencode_sdo_writer")
    except Exception:
        return "0.0.0"  # Fallback for development mode


def main() -> None:
    """Entry point for the CLI application."""
    app()
