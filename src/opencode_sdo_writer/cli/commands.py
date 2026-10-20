"""CLI command implementations for OpenCode SDO Writer."""

from __future__ import annotations

from pathlib import Path

import typer

from opencode_sdo_writer import installer
from opencode_sdo_writer.cli import args
from opencode_sdo_writer.lockfile import LockError, load_lock
from opencode_sdo_writer.paths import global_config_dir, project_config_dir
from opencode_sdo_writer.profile import ProfileError, available_profiles, load_profile
from opencode_sdo_writer.sources import SkillSource, resolve_source


def update(
    profile: args.ProfileArg = None,
    source: args.SourcePath = None,
    config: args.ConfigPath = None,
    project: args.ProjectPath = None,
    force: args.ForceFlag = False,
) -> None:
    """Re-install a profile, replacing skills whose content changed."""
    init(profile=profile, source=source, config=config, project=project, force=force)


def init(
    profile: args.ProfileArg = None,
    source: args.SourcePath = None,
    config: args.ConfigPath = None,
    project: args.ProjectPath = None,
    force: args.ForceFlag = False,
    dry_run: args.DryRunFlag = False,
) -> None:
    """Install a writer profile and the `sdo-writer` agent."""
    known = available_profiles()
    if profile is None:
        typer.echo("No profile given. Available profiles:")
        profiles()
        raise typer.Exit(code=1)
    if profile not in known:
        typer.echo(f"Unknown profile '{profile}'. Available profiles: {', '.join(known)}")
        raise typer.Exit(code=1)

    try:
        loaded = load_profile(profile)
    except ProfileError as err:
        typer.echo(f"Error: {err}")
        raise typer.Exit(code=1) from err

    try:
        lock = load_lock()
    except LockError as err:
        typer.echo(f"Error: {err}")
        raise typer.Exit(code=1) from err

    try:
        skill_source = _resolve_source(source)
    except FileNotFoundError as err:
        typer.echo(f"Error: {err}")
        raise typer.Exit(code=1) from err

    if not skill_source.skills:
        typer.echo("Error: no skills found. Pass --source with a checkout of the skills repository.")
        raise typer.Exit(code=1)

    config_dir = _config_dir(config, project)
    if dry_run:
        wanted = installer.wanted_skills(lock, loaded)
        missing = skill_source.missing(tuple(wanted))
        typer.echo(f"Would install {len(wanted) - len(missing)} skills into {config_dir}")
        typer.echo(f"Skills: {', '.join(wanted)}")
        if missing:
            typer.echo(f"Missing from source: {', '.join(missing)}")
        return

    report = installer.install(loaded, config_dir, skill_source, lock, force=force)
    _echo_report(report)
    if report.missing:
        raise typer.Exit(code=1)


def _resolve_source(source: str | None) -> SkillSource:
    """Return the skill source to install from."""
    if source:
        return resolve_source(Path(source).expanduser().resolve())
    return resolve_source()


def _echo_report(report: installer.InstallReport) -> None:
    """Print an install report."""
    typer.echo(f"Profile:  {report.profile}")
    typer.echo(f"Config:   {report.config_dir}")
    typer.echo("")
    for label, items in (
        ("Installed", report.installed),
        ("Updated", report.updated),
        ("Unchanged", report.unchanged),
        ("Removed", report.removed),
        ("Missing", report.missing),
        ("Conflicts", report.conflicts),
    ):
        if items:
            typer.echo(f"{label}: {', '.join(items)}")
    if report.agent_path:
        typer.echo(f"Agent:    {report.agent_path}")


def profiles() -> None:
    """List the available writer profiles."""
    for profile_id in available_profiles():
        profile = load_profile(profile_id)
        typer.echo(f"{profile.id:<8} {profile.title} - {profile.description}")


def status(
    config: args.ConfigPath = None,
    project: args.ProjectPath = None,
) -> None:
    """Show what is currently installed."""
    config_dir = _config_dir(config, project)
    manifest, drifted = installer.status(config_dir)
    if manifest is None:
        typer.echo(f"Nothing installed in {config_dir}")
        raise typer.Exit(code=1)

    typer.echo(f"Profile:  {manifest.profile}")
    typer.echo(f"Source:   {manifest.source}")
    typer.echo(f"Updated:  {manifest.installed_at}")
    typer.echo(f"Skills:   {len(manifest.skills)}")
    for skill_id in manifest.installed_skills:
        marker = "!" if skill_id in drifted else " "
        typer.echo(f"  {marker} {skill_id}")
    if drifted:
        typer.echo("")
        typer.echo(f"Changed on disk: {', '.join(drifted)}")
        typer.echo("Run 'update' to restore them.")


def uninstall(
    config: args.ConfigPath = None,
    project: args.ProjectPath = None,
) -> None:
    """Remove the installed skills and agent."""
    config_dir = _config_dir(config, project)
    removed, agent_path = installer.uninstall(config_dir)
    if not removed and agent_path is None:
        typer.echo(f"Nothing to remove in {config_dir}")
        return
    typer.echo(f"Removed {len(removed)} skills from {config_dir}")
    if agent_path:
        typer.echo(f"Removed agent: {agent_path}")


def _config_dir(config: str | None, project: str | None) -> Path:
    """Return the OpenCode configuration directory to work in."""
    if project:
        return project_config_dir(Path(project).expanduser().resolve())
    if config:
        return Path(config).expanduser().resolve()
    return global_config_dir()
