---
name: 3gpp-portal-authentication
description: EOL authentication, AJAX login patterns, 3GPP portal data fetching, and session management. Use when accessing protected 3GPP portal resources that require EOL login, fetching TDoc metadata, or working with 3GPP portal APIs.
---

# 3GPP Portal Authentication

## Overview

The 3GPP portal (<https://portal.3gpp.org/>) provides access to protected resources that require ETSI Online Account (EOL) authentication.

`scripts/portal_session.py` is a ready-made EOL session helper; the full scope,
endpoint and error reference is in `references/auth-scope.md`.

## Ready-Made Session Module

| Component | Purpose |
|---|---|
| `PortalCredentials` | Credential dataclass; `from_environment()` reads `EOL_USERNAME`/`EOL_PASSWORD` |
| `PortalSession` | Authenticated `requests.Session` wrapper (`authenticate()`, `get_tdoc_metadata()`) |
| `PortalAuthenticationError` | Raised on login failure or unauthenticated use |
| `PortalParsingError` | Raised when portal HTML parsing fails |

### Usage

```python
from portal_session import PortalCredentials, PortalSession

credentials = PortalCredentials.from_environment()
session = PortalSession(credentials)
session.authenticate()
metadata = session.get_tdoc_metadata("R1-2301234")
# {"title": "...", "meeting": "...", ...}
```

### Running the Script

```bash
mise x uv -- uv run scripts/portal_session.py --check-auth
mise x uv -- uv run scripts/portal_session.py R1-2301234
```

Credentials are read from the `EOL_USERNAME` and `EOL_PASSWORD` environment variables.

### Login Flow (implemented by `authenticate()`)

1. Visit `https://portal.3gpp.org/` to establish session cookies
2. POST form-encoded `username`/`password` to `LoginEOL.ashx`
3. Parse JSON response; raise `PortalAuthenticationError` unless `success` is true

## Key Facts

- **Login endpoint**: `https://portal.3gpp.org/ngppapp/LoginEOL.ashx` (POST, form-encoded, JSON `success` boolean)
- **TDoc metadata endpoint**: `https://portal.3gpp.org/ngppapp/CreateTdoc.Aspx?mode=view&contributionUid={tdoc_id}` (GET, authenticated)
- **EOL required for**: meeting registration, 3GU portal, protected documents, full TDoc metadata
- **EOL not required for**: public TDoc files on FTP/HTTP, meeting lists, specification downloads, basic TDoc metadata
- **Session**: cookies kept by `requests.Session`, 30 s timeout, no automatic retry
- **Credentials**: `EOL_USERNAME` / `EOL_PASSWORD`; never store them in code

## Reference Files

- `references/auth-scope.md` - EOL scope table, login endpoint, `PortalSession` class, exceptions, credentials, public functions, usage patterns, error handling, best practices

## Cross-References

- `3gpp-tdocs` - TDoc metadata structure and portal URLs
- `3gpp-meetings` - Meeting registration and portal integration
- `3gpp-specifications` - Spec file access patterns
