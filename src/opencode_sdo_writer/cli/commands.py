"""CLI command implementations for OpenCode SDO Writer."""
from __future__ import annotations

import typer

from opencode_sdo_writer.cli import args

# Application name for environment variables
APP_NAME_UPPERCASE = "OPENCODE_SDO_WRITER"

# ═══════════════════════════════════════════════════════════════════════════
# DEMO COMMANDS — REPLACE ME!
#
# `default`, `greet` and `add` only demonstrate the Typer CLI plumbing:
# argument definitions in args.py, command functions in this file, and
# registration in app.py. They are NOT real functionality of this project.
#
# To add your real commands:
#   1. Delete the demo commands below (or repurpose `default`).
#   2. Write each real command as a plain function in this file, using the
#      argument types from args.py and a docstring (it becomes --help text).
#   3. Register each command in app.py: `app.command()(commands.your_cmd)`.
#
# Do NOT add @app.command() decorators here and do NOT import `app` from
# app.py: that creates a circular import and makes pyreorder reorder this
# module into a broken state. Keep every command a plain top-level function.
# ═══════════════════════════════════════════════════════════════════════════

# Default command (runs when no command provided)


def default() -> None:
    """Default command showing welcome message."""
    typer.echo(f"Welcome to OpenCode SDO Writer!")
    typer.echo("Use --help to see available commands.")


# Greet command


def greet(
    name: args.NameArg,
    input_file: args.InputFileArg = None,
    output_file: args.OutputFile = None,
    cache: args.Cache = True,
) -> None:
    """Greet a person by name."""
    if input_file:
        # Read names from file
        names = [line.strip() for line in input_file if line.strip()]
        for n in names:
            typer.echo(f"Hello, {n}!")
    else:
        typer.echo(f"Hello, {name}!")

    # Show option values (for demonstration)
    if output_file:
        typer.echo(f"Output file: {output_file}")
    typer.echo(f"Cache: {'enabled' if cache else 'disabled'}")


# Add command


def add(
    number1: args.NumberArg1,
    number2: args.NumberArg2,
    output_file: args.OutputFile = None,
) -> None:
    """Add two numbers together."""
    result = number1 + number2
    typer.echo(f"The sum of {number1} and {number2} is {result}")

    if output_file:
        with open(output_file, "w") as f:
            f.write(str(result))
        typer.echo(f"Result written to {output_file}")
