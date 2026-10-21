"""Vendor the skills of the skills repository into this package.

The script copies the skill directories of one or more source repositories
into the package, and writes the lock file that records where they came
from and which layer they belong to.

It never talks to the network: it works on local checkouts, so the person
running a release decides exactly what goes into the package.

Usage:
    uv run python scripts/vendor_skills.py \
        --source /path/to/sdo-skills \
        --ref v0.2.0 \
        --output src/opencode_sdo_writer/vendor.lock \
        --vendor-dir src/opencode_sdo_writer/_vendor \
        --extra-source etsi-portal-tool=/path/to/etsi-portal-tool \
        --extra-repo etsi-portal-tool=https://forge.etsi.org/rep/reimes/etsi-portal-tool \
        --extra-ref etsi-portal-tool=239b2d9
"""

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent.parent / "src" / "opencode_sdo_writer"
DEFAULT_LOCK = PACKAGE_ROOT / "vendor.lock"
DEFAULT_VENDOR = PACKAGE_ROOT / "_vendor"

IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".DS_Store", ".git")


@dataclass
class Skill:
    """One vendored skill."""

    id: str
    layer: str
    source: str
    path: Path


def main(argv: list[str] | None = None) -> int:
    """Run the vendoring."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", required=True, type=Path, help="Checkout of the skills repository")
    parser.add_argument("--ref", required=True, help="Revision to record in the lock file")
    parser.add_argument("--repo", default="https://github.com/jr2804/sdo-skills.git", help="Repository URL to record")
    parser.add_argument("--output", type=Path, default=DEFAULT_LOCK, help="Lock file to write")
    parser.add_argument("--vendor-dir", type=Path, default=DEFAULT_VENDOR, help="Directory of the vendored snapshot")
    parser.add_argument(
        "--extra-source",
        action="append",
        default=[],
        type=parse_extra,
        metavar="ID=PATH",
        help="Additional source of skills, for example a tool repository",
    )
    parser.add_argument(
        "--extra-repo",
        action="append",
        default=[],
        metavar="ID=URL",
        help="Repository URL to record for an extra source",
    )
    parser.add_argument(
        "--extra-ref",
        action="append",
        default=[],
        metavar="ID=REF",
        help="Revision to record for an extra source (defaults to --ref)",
    )
    args = parser.parse_args(argv)

    source_root = args.source.resolve()
    skills_root = source_root / "skills"
    if not skills_root.is_dir():
        print(f"Error: no 'skills' directory in {source_root}", file=sys.stderr)
        return 1

    skills = find_skills(skills_root, "sdo-skills", layered=True)
    if not skills:
        print(f"Error: no skills found in {skills_root}", file=sys.stderr)
        return 1

    sources = [("sdo-skills", args.repo, args.ref, False)]
    extra_repos = dict(parse_extra_pair(item) for item in args.extra_repo)
    extra_refs = dict(parse_extra_pair(item) for item in args.extra_ref)
    for source_id, path in args.extra_source:
        extra_root = path.resolve()
        if not extra_root.is_dir():
            print(f"Skipping extra source '{source_id}': {extra_root} not found", file=sys.stderr)
            continue
        nested = extra_root / "skills"
        root = nested if nested.is_dir() else extra_root
        extra_skills = find_skills(root, source_id, layered=False)
        if not extra_skills:
            print(f"Skipping extra source '{source_id}': no skills in {root}", file=sys.stderr)
            continue
        skills.extend(extra_skills)
        sources.append(
            (source_id, extra_repos.get(source_id, str(extra_root)), extra_refs.get(source_id, args.ref), True)
        )

    if args.vendor_dir.exists():
        shutil.rmtree(args.vendor_dir)
    for skill in skills:
        copy_skill(skill, args.vendor_dir)

    write_lock(args.output, sources, skills)

    print(f"Vendored {len(skills)} skills into {args.vendor_dir}")
    print(f"Lock file: {args.output}")
    for skill in skills:
        print(f"  {skill.layer:<8} {skill.id:<28} ({skill.source})")
    return 0


def find_skills(root: Path, source_id: str, layered: bool) -> list[Skill]:
    """Return the skills found below a source root.

    Args:
        root: Directory to scan.
        source_id: Identifier of the source, used in the lock file.
        layered: Whether the skills sit in layer directories below the root.
    """
    found: list[Skill] = []
    if not root.is_dir():
        return found

    if layered:
        for layer_dir in sorted(p for p in root.iterdir() if p.is_dir()):
            for skill_dir in sorted(p for p in layer_dir.iterdir() if p.is_dir()):
                if (skill_dir / "SKILL.md").is_file():
                    found.append(Skill(skill_dir.name, layer_dir.name, source_id, skill_dir))
    else:
        for skill_dir in sorted(p for p in root.iterdir() if p.is_dir()):
            if (skill_dir / "SKILL.md").is_file():
                found.append(Skill(skill_dir.name, "tools", source_id, skill_dir))

    return found


def write_lock(path: Path, sources: list[tuple[str, str, str, bool]], skills: list[Skill]) -> None:
    """Write the lock file.

    Args:
        path: Where to write the lock file.
        sources: Tuples of identifier, repository URL, revision and optional flag.
        skills: The skills to record.
    """
    lines = ["version = 1", ""]
    for source_id, repo, ref, optional in sources:
        lines.append("[[source]]")
        lines.append(f"id = {_toml_string(source_id)}")
        lines.append(f"repo = {_toml_string(repo)}")
        lines.append(f"ref = {_toml_string(ref)}")
        if optional:
            lines.append("optional = true")
        lines.append("")

    lines.append("[skill]")
    for skill in skills:
        lines.append(f'"{skill.id}" = {{ layer = "{skill.layer}", source = "{skill.source}" }}')
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _toml_string(value: str) -> str:
    """Escape a value for a TOML basic string."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def copy_skill(skill: Skill, vendor_root: Path) -> Path:
    """Copy a skill into the vendored snapshot and return the target."""
    target = vendor_root / skill.source / skill.id
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(skill.path, target, ignore=IGNORE)
    return target


def parse_extra(value: str) -> tuple[str, Path]:
    """Parse an ``id=path`` argument."""
    if "=" not in value:
        msg = f"Expected 'id=path', got '{value}'"
        raise argparse.ArgumentTypeError(msg)
    source_id, _, raw_path = value.partition("=")
    return source_id.strip(), Path(raw_path.strip())


def parse_extra_pair(value: str) -> tuple[str, str]:
    """Parse an ``id=value`` argument."""
    if "=" not in value:
        msg = f"Expected 'id=value', got '{value}'"
        raise argparse.ArgumentTypeError(msg)
    source_id, _, raw = value.partition("=")
    return source_id.strip(), raw.strip()


if __name__ == "__main__":
    raise SystemExit(main())
