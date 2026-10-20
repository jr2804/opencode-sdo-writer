# ETSI Portal Tooling

The portal is reached with the `etsi-portal-tool` CLI, which also exposes an
MCP server for agents.

| Area | What it does |
|------|--------------|
| `tc` | list committees and their sub-committees |
| `meetings` | list, find and inspect meetings (upcoming and past) |
| `documents` | list, filter and download the documents of a meeting |
| `register` | register a delegate, inspect the profile and the permission tokens |
| `tdoc` | create, edit, revise and upload contributions; bind work items |
| `workitems` | list the open work items of a committee |
| `auth` | log in via SecretSpec, vault, browser or cookie import |

Browsing is read-only and needs no authentication; downloading, registering
and writing need a logged-in session. The full command surface, the
authentication options and the known pitfalls live in the `etsi-portal-tool`
skill.

## Typical sequence

The portal CLI is a member-only tool hosted on a private forge, so mise
pulls it on demand. The full form is shown below; when the CLI is already
on PATH, the plain `etsi-portal-tool` command works as well.

```bash
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool auth login
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool tc list
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool meetings list --tc STQ
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool meetings get 82821 --tc STQ
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool documents list -m 82821 -t stq
mise x uv -- uvx --from git+https://forge.etsi.org/rep/reimes/etsi-portal-tool download meeting -m 82821 -t stq
```

The procedure around those commands -- when a contribution is due, what a
revision is, how a work item is bound -- is in `etsi-procedures`.
