"""Participant list workbook for any set of ETSI meetings.

One workbook, one sheet, one row per person (portal PersonId). Column A lists the meetings the
person joins, e.g. ``<TC>#<nn>, <sub-TC>#<nn>``. Columns: Meeting, First name, Last name, Organisation,
Role, Presence, Registration date (UTC). Rows: face to face first, then by registration date.
Titles (Dr, Mr, Ms, ...) are not part of the list. No summary, no portal IDs.

Meetings are given by UID (``<TC>#<nn>``) or by portal ID; committees by short code
(``<TC>``, ``<sub-TC code>``) or TBID. A UID is resolved against ``meetings list --tc <TC>``; it
must match exactly one meeting, otherwise the run fails loud.

Source: ``etsi-portal-tool [-p <profile>] register list <portal-id> --json`` (the
registration roster). ``PresenceType`` 2 is face to face, 1 is online. ``RegistrationDate``
is ISO 8601 in UTC.

Personal data: the workbook and the raw rosters are never committed. Raw rosters are
kept under ``tools/var/`` (git-ignored).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

TOOLS = Path(__file__).resolve().parent.parent
RAW_DIR = TOOLS / "var" / "participants"

COLUMNS = ["Meeting", "First name", "Last name", "Organisation", "Role", "Presence", "Registration date (UTC)"]
PRESENCE = {2: "face to face", 1: "online"}
PRESENCE_ORDER = {2: 0, 1: 1}          # face to face first
SHEET_LIMIT = 31
BAD_SHEET_CHARS = re.compile(r"[\[\]:*?/\\]")

HEAD_FILL = PatternFill("solid", fgColor="D9D9D9")
THIN = Side(style="thin", color="999999")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


class ParticipantsError(RuntimeError):
    """A run that cannot produce a correct list; the message says what to fix."""


@dataclass(frozen=True)
class Meeting:
    uid: str        # e.g. "<TC>#<nn>", taken from the portal title
    portal_id: int
    tc: str         # committee short code it was found under, e.g. "<TC>" or "<sub-TC code>"


def _key(text: str) -> str:
    return re.sub(r"\s+", "", text).upper()


def uid_of(title: str) -> str:
    """'<TC>#<nn>' -> '<TC>#<nn>'; '<sub-TC>#<nn>' -> '<sub-TC>#<nn>'."""
    return title.split("-")[0].strip()


class Portal:
    """Thin wrapper around the etsi-portal-tool CLI (JSON output only)."""

    def __init__(self, binary: str | None = None, profile: str | None = None):
        exe = binary or os.environ.get("ETSI_PORTAL_TOOL_BIN") or shutil.which("etsi-portal-tool")
        if not exe:
            raise ParticipantsError(
                "etsi-portal-tool not found: put it on PATH, set ETSI_PORTAL_TOOL_BIN, or pass --bin")
        self.exe = exe
        self.prefix = ["-p", profile] if profile else []

    def json(self, *args: str):
        cmd = [self.exe, *self.prefix, *args, "--json"]
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout).strip()
            raise ParticipantsError(f"{' '.join(args)} failed: {detail}")
        try:
            return json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise ParticipantsError(f"{' '.join(args)} did not return JSON: {exc}") from exc


def resolve(portal: Portal, committees: list[str], meetings: list[str]) -> list[Meeting]:
    """Resolve every requested meeting (UID or portal ID) against the given committees.

    ``meetings find`` searches the whole history itself and returns every match: a UID such as
    ``<TC>#<nn>`` can legitimately match two meetings, which is then an error asking for the portal id.
    """
    resolved: list[Meeting] = []
    for wanted in meetings:
        if wanted.strip().isdigit():
            tcs = committees
            found = portal.json("meetings", "find", wanted.strip(), "--tc", ",".join(tcs))
        else:
            found = portal.json("meetings", "find", wanted, "--tc", ",".join(committees))
        wanted_key = _key(wanted)
        hits = [m for m in found if _key(uid_of(m["Title"])) == wanted_key or str(m["Id"]) == wanted.strip()]
        if not hits:
            raise ParticipantsError(
                f"meeting {wanted!r} not found in committee(s) {', '.join(committees)}. "
                "Check the UID or the committee short code (e.g. <sub-TC code> for <sub-TC>).")
        if len(hits) > 1:
            options = "; ".join(f"{m['Id']} {m['Title']}" for m in hits)
            raise ParticipantsError(
                f"meeting {wanted!r} is ambiguous ({options}); give the portal id instead")
        m = hits[0]
        uid = uid_of(m["Title"])
        if len(uid) > SHEET_LIMIT or BAD_SHEET_CHARS.search(uid):
            raise ParticipantsError(f"meeting UID {uid!r} cannot be used as a sheet name")
        resolved.append(Meeting(uid=uid, portal_id=int(m["Id"]), tc=m.get("TB", "")))
    return resolved


def _registered(p: dict) -> datetime:
    raw = p.get("RegistrationDate") or ""
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ParticipantsError(
            f"unexpected RegistrationDate {raw!r} for {p.get('Lastname')!r} (expected ISO 8601)") from exc


def _presence(p: dict) -> int:
    code = p.get("PresenceType")
    if code not in PRESENCE:
        raise ParticipantsError(
            f"unknown PresenceType {code!r} for {p.get('Lastname')!r}; the portal changed its codes, "
            "check etsi-portal-tool before using this list")
    return code


def roster_rows(raw: list[dict]) -> list[list]:
    """Rows in the order: face to face first, then registration date, then surname."""
    keyed = []
    for p in raw:
        code = _presence(p)
        when = _registered(p)
        keyed.append((PRESENCE_ORDER[code], when, (p.get("Lastname") or "").lower(),
                      (p.get("Firstname") or "").lower(), p, code, when))
    keyed.sort(key=lambda k: k[:4])
    rows = []
    for _, _, _, _, p, code, when in keyed:
        rows.append([
            (p.get("Firstname") or "").strip(),
            (p.get("Lastname") or "").strip(),
            (p.get("RepresentingOrganisation") or {}).get("Name", ""),
            (p.get("Role") or {}).get("Name", ""),
            PRESENCE[code],
            when.date(),
        ])
    return rows


def fetch_rosters(portal: Portal, meetings: list[Meeting], raw_dir: Path) -> dict[str, list[dict]]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    out: dict[str, list[dict]] = {}
    for m in meetings:
        data = portal.json("register", "list", str(m.portal_id))
        (raw_dir / f"{m.uid.replace('#', '-')}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        out[m.uid] = data
    return out


def write_workbook(path: Path, rows: list[list]) -> None:
    """One sheet. Column A is the meeting UID; a person registered for two meetings appears twice."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Participants"
    widths = [14, 18, 18, 44, 14, 14, 20]
    for c, name in enumerate(COLUMNS, start=1):
        cell = ws.cell(row=1, column=c, value=name)
        cell.font = Font(name="Arial", size=10, bold=True)
        cell.fill = HEAD_FILL
        cell.border = BOX
        cell.alignment = Alignment(vertical="top", wrap_text=True)
    for r, row in enumerate(rows, start=2):
        for c, value in enumerate(row, start=1):
            cell = ws.cell(row=r, column=c, value=value)
            cell.font = Font(name="Arial", size=10)
            cell.border = BOX
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if COLUMNS[c - 1].startswith("Registration"):
                cell.number_format = "yyyy-mm-dd"
    for c, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(c)].width = width
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(COLUMNS))}{max(1, len(rows) + 1)}"
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)


def build(committees: list[str], meetings: list[str], out: Path, *,
          binary: str | None = None, profile: str | None = None,
          raw_dir: Path = RAW_DIR) -> dict[str, int]:
    """Produce one deduplicated workbook. Returns {UID: registered count} per meeting.

    One row per person (portal PersonId). Meeting: the meetings the person joins, in the order
    given, joined by ", ". Presence: the value when all meetings agree; otherwise one entry per
    meeting, e.g. ``online (<TC>#<nn>), face to face (<sub-TC>#<nn>)``. Registration date: the earliest.
    Rows: face to face first (a person with face to face at any meeting counts as face to face), then
    registration date, then surname.
    """
    if not committees:
        raise ParticipantsError("give at least one committee with --tc (e.g. --tc <TC> --tc <sub-TC code>)")
    if not meetings:
        raise ParticipantsError("give at least one meeting with --meeting (UID like <TC>#<nn>, or a portal ID)")
    portal = Portal(binary, profile)
    resolved = resolve(portal, committees, meetings)
    rosters = fetch_rosters(portal, resolved, raw_dir)
    people: dict[object, dict] = {}
    counts: dict[str, int] = {}
    for m in resolved:
        counts[m.uid] = len(rosters[m.uid])
        for p in rosters[m.uid]:
            pid = p.get("PersonId")
            if not pid:
                raise ParticipantsError(f"registration of {p.get('Lastname')!r} in {m.uid} has no PersonId; cannot deduplicate")
            code = _presence(p)
            when = _registered(p)
            entry = people.setdefault(pid, {"p": p, "meetings": [], "presence": {}, "when": when})
            entry["meetings"].append(m.uid)
            entry["presence"][m.uid] = code
            if when < entry["when"]:
                entry["when"] = when
    keyed = []
    for e in people.values():
        p = e["p"]
        codes = set(e["presence"].values())
        if len(codes) == 1:
            presence_text = PRESENCE[codes.pop()]
        else:
            presence_text = ", ".join(f"{PRESENCE[e['presence'][uid]]} ({uid})" for uid in e["meetings"])
        group = min(PRESENCE_ORDER[c] for c in e["presence"].values())
        keyed.append((group, e["when"], (p.get("Lastname") or "").lower(), (p.get("Firstname") or "").lower(),
                      [
                          ", ".join(e["meetings"]),
                          (p.get("Firstname") or "").strip(),
                          (p.get("Lastname") or "").strip(),
                          (p.get("RepresentingOrganisation") or {}).get("Name", ""),
                          (p.get("Role") or {}).get("Name", ""),
                          presence_text,
                          e["when"].date(),
                      ]))
    keyed.sort(key=lambda k: k[:4])
    write_workbook(out, [k[4] for k in keyed])
    return counts
