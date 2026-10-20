#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
#   "beautifulsoup4",
# ]
# ///
"""Reusable 3GPP portal authentication session.

Library usage (from another script or REPL):

    # mise x uv -- uv run --with requests,beautifulsoup4 python -c ...
    from portal_session import PortalCredentials, PortalSession

    credentials = PortalCredentials(
        username=os.environ["EOL_USERNAME"],
        password=os.environ["EOL_PASSWORD"],
    )
    session = PortalSession(credentials)
    session.authenticate()
    metadata = session.get_tdoc_metadata("R1-2301234")

Standalone usage (credentials are read from EOL_USERNAME / EOL_PASSWORD):

    mise x uv -- uv run scripts/portal_session.py --check-auth
    mise x uv -- uv run scripts/portal_session.py R1-2301234
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

PORTAL_BASE_URL = "https://portal.3gpp.org/"
LOGIN_URL = "https://portal.3gpp.org/ngppapp/LoginEOL.ashx"
TDOC_VIEW_URL = "https://portal.3gpp.org/ngppapp/CreateTdoc.Aspx?mode=view&contributionUid={tdoc_id}"


class PortalAuthenticationError(Exception):
    """Raised when 3GPP portal authentication fails."""


class PortalParsingError(Exception):
    """Raised when 3GPP portal page HTML parsing fails."""


@dataclass(frozen=True)
class PortalCredentials:
    """3GPP portal (EOL) authentication credentials.

    Read from environment variables when not provided explicitly:
    EOL_USERNAME / EOL_PASSWORD.
    """

    username: str
    password: str

    @classmethod
    def from_environment(cls) -> PortalCredentials:
        try:
            return cls(
                username=os.environ["EOL_USERNAME"],
                password=os.environ["EOL_PASSWORD"],
            )
        except KeyError as exc:
            msg = f"Missing environment variable: {exc.args[0]}"
            raise PortalAuthenticationError(msg) from exc


class PortalSession:
    """Authenticated HTTP session with the 3GPP portal."""

    def __init__(self, credentials: PortalCredentials, timeout: int = 30):
        self.credentials = credentials
        self.timeout = timeout
        self.session = requests.Session()
        self._authenticated = False

    def authenticate(self) -> None:
        """Perform EOL login via the portal's AJAX endpoint."""
        # 1. Visit login page to establish session cookies
        response = self.session.get(PORTAL_BASE_URL, timeout=self.timeout)
        response.raise_for_status()

        # 2. AJAX login (form-encoded)
        payload = {
            "username": self.credentials.username,
            "password": self.credentials.password,
        }
        response = self.session.post(LOGIN_URL, data=payload, timeout=self.timeout)
        response.raise_for_status()

        # 3. Parse JSON response
        try:
            auth_result = response.json()
        except ValueError as exc:
            msg = f"EOL login returned non-JSON response: {response.text[:200]!r}"
            raise PortalAuthenticationError(msg) from exc

        if not auth_result.get("success", False):
            msg = f"EOL authentication failed: {auth_result}"
            raise PortalAuthenticationError(msg)

        self._authenticated = True

    def get_tdoc_metadata(self, tdoc_id: str) -> dict[str, str]:
        """Fetch TDoc metadata from the portal view page.

        URL: TDOC_VIEW_URL with the TDoc number as contributionUid.
        """
        self._ensure_authenticated()

        response = self.session.get(
            TDOC_VIEW_URL.format(tdoc_id=tdoc_id), timeout=self.timeout
        )
        response.raise_for_status()

        try:
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as exc:
            msg = f"Failed to parse portal page for {tdoc_id}"
            raise PortalParsingError(msg) from exc

        metadata: dict[str, str] = {}
        for label in soup.find_all("label"):
            value_element = label.find_next_sibling("input")
            if value_element and value_element.get("value"):
                field_name = label.get_text().strip(": ").lower()
                metadata[field_name] = value_element.get("value")

        return metadata

    def _ensure_authenticated(self) -> None:
        """Ensure session is authenticated before making protected requests."""
        if not self._authenticated:
            msg = "Session not authenticated. Call authenticate() first."
            raise PortalAuthenticationError(msg)


def main(argv: list[str] | None = None) -> int:
    """Authenticate against the 3GPP portal and dump TDoc metadata."""
    parser = argparse.ArgumentParser(
        description="Fetch TDoc metadata from the 3GPP portal using EOL credentials.",
    )
    parser.add_argument("tdoc_ids", nargs="*", help="TDoc numbers, e.g. R1-2301234")
    parser.add_argument(
        "--check-auth",
        action="store_true",
        help="only verify that the EOL login succeeds",
    )
    args = parser.parse_args(argv)

    if not args.tdoc_ids and not args.check_auth:
        parser.error("give at least one TDoc number or --check-auth")

    credentials = PortalCredentials.from_environment()
    session = PortalSession(credentials)
    session.authenticate()
    print("EOL authentication succeeded.")

    for tdoc_id in args.tdoc_ids:
        metadata = session.get_tdoc_metadata(tdoc_id)
        print(f"--- {tdoc_id} ---")
        for key, value in metadata.items():
            print(f"{key}: {value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
