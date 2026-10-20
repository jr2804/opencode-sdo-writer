"""Tests for the agent renderer."""

from __future__ import annotations

import dataclasses
import re

import yaml

from opencode_sdo_writer.agent import render_agent
from opencode_sdo_writer.profile import available_profiles, load_profile

#: A backticked token that looks like a skill identifier.
SKILL_ID = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`")


def test_render_agent_has_valid_frontmatter() -> None:
    profile = load_profile("etsi")
    rendered = render_agent(profile, ("sdo-writing", "etsi-tools"))

    assert rendered.startswith("---\n")
    data = _frontmatter(rendered)
    assert data["description"] == profile.description
    assert data["mode"] == "primary"
    assert data["color"] == profile.color
    assert data["temperature"] == profile.temperature


def test_skill_permissions_deny_by_default_and_allow_the_listed_ones() -> None:
    profile = load_profile("etsi")
    data = _frontmatter(render_agent(profile, ("sdo-writing", "etsi-tools")))
    permissions = data["permission"]["skill"]

    assert permissions["*"] == "deny"
    assert permissions["sdo-writing"] == "allow"
    assert permissions["etsi-tools"] == "allow"


def test_bash_permissions_ask_by_default_and_allow_the_configured_ones() -> None:
    profile = load_profile("etsi")
    data = _frontmatter(render_agent(profile, ("sdo-writing",)))
    permissions = data["permission"]["bash"]

    assert permissions["*"] == "ask"
    assert permissions["mise *"] == "allow"


def test_body_contains_the_shared_prompt_and_the_profile_notes() -> None:
    profile = load_profile("itut")
    rendered = render_agent(profile, ("itut-reference",))

    assert "You are a standards writer." in rendered
    assert "Skill routing" in rendered
    assert profile.notes.strip().splitlines()[0] in rendered


def test_description_with_a_colon_is_quoted() -> None:
    profile = load_profile("etsi")
    data = _frontmatter(render_agent(profile, ()))
    assert isinstance(data["description"], str)
    assert data["description"] == profile.description


def _frontmatter(rendered: str) -> dict:
    _, _, body = rendered.partition("---")
    frontmatter, _, _ = body.partition("---")
    return yaml.safe_load(frontmatter)


def test_agent_without_notes_has_no_extra_section() -> None:

    profile = dataclasses.replace(load_profile("etsi"), notes="")
    rendered = render_agent(profile, ("sdo-writing",))

    assert "ETSI specifics" not in rendered
    assert "You are a standards writer." in rendered


def test_every_profile_mentions_only_its_own_skills() -> None:
    common = ("sdo-writing", "sdo-docx", "sdo-drafting", "sdo-ipr", "sdo-project-setup")

    for profile_id in available_profiles():
        profile = load_profile(profile_id)
        body_skills = {
            "etsi": (
                "etsi-governance",
                "etsi-directives",
                "etsi-procedures",
                "etsi-tools",
                "etsi-portal-tool",
                "etsi-meeting-report",
            ),
            "3gpp": (
                "3gpp-basics",
                "3gpp-meetings",
                "3gpp-working-groups",
                "3gpp-releases",
                "3gpp-specifications",
                "3gpp-tdocs",
                "3gpp-change-request",
                "3gpp-portal-authentication",
            ),
            "itut": ("itut-reference", "itut-contributions"),
        }[profile_id]
        installed = common + body_skills

        rendered = render_agent(profile, installed)
        mentioned = set(SKILL_ID.findall(rendered))

        foreign = mentioned - set(installed)
        assert not foreign, f"{profile_id} mentions skills it does not have: {sorted(foreign)}"
