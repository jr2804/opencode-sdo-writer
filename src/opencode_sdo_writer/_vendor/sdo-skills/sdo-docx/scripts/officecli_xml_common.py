# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""Common helpers for deterministic officecli XML operations."""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

#: mise spec used to pull OfficeCLI on demand when it is not on PATH.
OFFICECLI_MISE_SPEC = "github:iOfficeAI/OfficeCLI"


def officecli_command(args: list[str]) -> list[str]:
    """Build the officecli argv, pulling it on demand via mise if needed.

    A locally installed ``officecli`` wins; otherwise the binary is fetched
    through mise (``mise x github:iOfficeAI/OfficeCLI -- officecli ...``), so
    the scripts work on a machine where only mise is available.
    """
    if shutil.which("officecli"):
        return ["officecli", *args]
    if shutil.which("mise"):
        return ["mise", "x", OFFICECLI_MISE_SPEC, "--", "officecli", *args]
    raise RuntimeError(
        "officecli not found. Install it (npm i -g @officecli/officecli) or "
        "install mise so it can be pulled on demand."
    )


@dataclass
class CliResult:
    args: list[str]
    returncode: int
    stdout: str
    stderr: str


def load_json_spec(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Spec root must be an object")
    return data


def raw_set(
    doc_path: str, xpath: str, action: str, xml: str, *, verbose: bool = False
) -> CliResult:
    if action not in {"replace", "before", "after"}:
        raise ValueError(f"Unsupported action: {action}")
    if action == "replace" and xml == "":
        raise ValueError("Refusing destructive empty XML replace")
    args = [
        "raw-set",
        doc_path,
        "/document",
        "--xpath",
        xpath,
        "--action",
        action,
        "--xml",
        xml,
    ]
    return run_officecli(args, verbose=verbose)


def validate_doc(doc_path: str, *, verbose: bool = False) -> CliResult:
    return run_officecli(["validate", doc_path], verbose=verbose)


def run_officecli(
    args: list[str], *, check: bool = True, verbose: bool = False
) -> CliResult:
    command = officecli_command(args)
    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    result = CliResult(command, proc.returncode, proc.stdout, proc.stderr)
    if verbose:
        print("$", " ".join(command))
        if result.stdout.strip():
            print(result.stdout.strip())
        if result.stderr.strip():
            print(result.stderr.strip())
    if check and result.returncode != 0:
        raise RuntimeError(
            f"officecli failed ({result.returncode}): {result.stderr.strip()}"
        )
    return result
