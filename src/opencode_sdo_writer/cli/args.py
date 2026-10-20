"""CLI arguments, options, and flags for OpenCode SDO Writer."""

from __future__ import annotations

from typing import Annotated

import typer

# Application name for environment variables
APP_NAME_UPPERCASE = "OPENCODE_SDO_WRITER"

# Global options

OutputFile = Annotated[
    str | None,
    typer.Option(
        "--output-file",
        "-o",
        help="Path to output file",
        envvar=f"{APP_NAME_UPPERCASE}_OUTPUT_FILE",
    ),
]

# Command-specific arguments

ProfileArg = Annotated[
    str | None,
    typer.Option(
        "--profile",
        "-p",
        help="Profile to install: etsi, 3gpp or itut",
    ),
]

SourcePath = Annotated[
    str | None,
    typer.Option(
        "--source",
        "-s",
        help="Path to a local checkout of the skills repository (development mode)",
    ),
]

ConfigPath = Annotated[
    str | None,
    typer.Option(
        "--config",
        "-c",
        help="Path to an OpenCode configuration directory (defaults to the global one)",
    ),
]

ProjectPath = Annotated[
    str | None,
    typer.Option(
        "--project",
        help="Install into the .opencode directory of this project instead of the global one",
    ),
]

ForceFlag = Annotated[
    bool,
    typer.Option(
        "--force",
        "-f",
        help="Overwrite skill directories that were not created by this installer",
    ),
]

DryRunFlag = Annotated[
    bool,
    typer.Option(
        "--dry-run",
        help="Show what would be done without writing anything",
    ),
]
