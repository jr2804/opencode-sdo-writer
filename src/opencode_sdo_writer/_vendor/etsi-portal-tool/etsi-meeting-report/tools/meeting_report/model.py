"""Read the chair's meeting data and the portal data, and build the render context.

Portal data is read at run time:
  * work items: `etsi-portal-tool workitems list --tc <TC>` (table output; `--json` once released)
  * documents: the cache manifest written by `download meeting` (titles used for checks only)
Nothing read here is written back into the repository.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tomllib
from pathlib import Path

from . import participants as participants_mod

STATUS_MAP = [
    ("Work item adopted", "0a", "Work item adopted"),
    ("Start of work", "1", "Start of work"),
    ("Early draft", "2", "Early draft"),
    ("Stable draft", "4", "Stable draft"),
    ("Final draft registered", "8", "Final draft registered"),
    ("Final draft", "6", "Final draft for approval"),
    ("Published", "12", "Published"),
]
ETSI_TYPES = {"TS", "TR", "EG", "ES", "GS"}


def load_meeting(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def run_portal(profile: str, args: list[str]) -> str:
    exe = os.environ.get("ETSI_PORTAL_TOOL_BIN") or shutil.which("etsi-portal-tool")
    if exe is None:
        raise SystemExit("etsi-portal-tool is not on PATH")
    proc = subprocess.run([exe, "-p", profile, *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=False)
    if proc.returncode != 0:
        raise SystemExit(f"etsi-portal-tool {' '.join(args)} failed ({proc.returncode}):\n{proc.stderr}")
    return proc.stdout


def parse_workitem_table(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 7 or cols[0] == "WI Code":
            continue
        rows.append({"code": cols[0], "title": cols[1], "version": cols[2], "status": cols[3],
                     "next": cols[4], "rapporteur": cols[5], "sub_tc": cols[6]})
    return rows


def parse_workitem_json(text: str) -> list[dict]:
    """Rows from `etsi-portal-tool workitems list --json` (v2026.10.11+): all fields are split."""
    data = json.loads(text)
    rows = []
    for w in data:
        rows.append({
            "code": w["code"], "wki_id": w["wki_id"], "number": w.get("number", ""),
            "title": w.get("title", ""), "version": w.get("version", ""),
            "status": w.get("status", ""), "next": w.get("next_status", ""),
            "rapporteur": w.get("rapporteur", ""), "sub_tc": w.get("sub_committee", ""),
            "report_url": w.get("report_url", ""),
        })
    return rows


def normalise_workitem(row: dict, titles: dict, notes: dict) -> dict:
    if "wki_id" in row:          # JSON row from the portal tool: fields already split
        wi = row["code"]
        number = row.get("number") or ""
        if not number:
            number = "number not yet assigned"
        elif number == wi:            # the tool reports the code itself when no ETSI number exists
            number = "number not yet assigned"
        elif number.startswith(("TS ", "TR ", "EG ", "ES ", "GS ")):
            number = f"{number} ({wi})"
        else:
            number = f"{number} ({wi})"
        date_m = re.search(r"\((\d{4}-\d{2}-\d{2})\)", row["status"])
        date = date_m.group(1) if date_m else ""
        code, label = "?", row["status"].split(" (")[0]
        for prefix, c, lbl in STATUS_MAP:
            if row["status"].startswith(prefix):
                code, label = c, lbl
                break
        head = " ".join(x for x in [f"v{row['version']}" if row["version"] else "", f"({date})" if date else ""] if x)
        last_draft = f"{head} — {code} {label}" if head else f"{code} {label}"
        return {
            "wi": wi, "wki_id": row["wki_id"], "number": number,
            "title": titles.get(wi, row["title"]), "rapporteur": row["rapporteur"],
            "last_draft": last_draft, "next": row["next"], "note": notes.get(wi, ""),
            "_portal_title": row["title"], "_truncated": False,
        }
    return normalise_table_row(row, titles, notes)


def normalise_table_row(row: dict, titles: dict, notes: dict) -> dict:
    m = re.match(r"^(\S+)\s*\((.*)\)\s*$", row["code"])
    wi, etsi = (m.group(1), m.group(2).strip()) if m else (row["code"], "")
    if etsi in ETSI_TYPES:
        number = "number not yet assigned"
    elif etsi:
        number = f"{etsi} ({wi})"
    else:
        number = wi
    date_m = re.search(r"\((\d{4}-\d{2}-\d{2})\)", row["status"])
    date = date_m.group(1) if date_m else ""
    code, label = "?", row["status"].split(" (")[0]
    for prefix, c, lbl in STATUS_MAP:
        if row["status"].startswith(prefix):
            code, label = c, lbl
            break
    head = " ".join(x for x in [f"v{row['version']}" if row["version"] else "", f"({date})" if date else ""] if x)
    last_draft = f"{head} — {code} {label}" if head else f"{code} {label}"
    return {
        "wi": wi,
        "number": number,
        "title": titles.get(wi, row["title"]),
        "rapporteur": row["rapporteur"],
        "last_draft": last_draft,
        "next": row["next"],
        "note": notes.get(wi, ""),
        "_portal_title": row["title"],
        "_truncated": row["title"].endswith("…") or row["status"].endswith("…"),
    }


def portal_sources(rows: list[dict]) -> dict[str, str]:
    """uid -> official source from `documents list --json` rows."""
    return {r["uid"]: r["source"] for r in rows if r.get("source")}


def parse_documents_json(text: str) -> list[dict]:
    return json.loads(text)


def manifest_titles(path: Path | None) -> dict[str, str]:
    if path is None or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {d["uid"]: d.get("title", "") for d in data.get("documents", [])}


def doc_entry(d: dict, m: dict, manifest: dict[str, str], diagnostics: list[str], sources: dict[str, str]) -> dict:
    """One TDoc block. Source is the official portal source (documents list --json); the chair's
    text is only a fallback, and every difference from the portal is reported."""
    portal = manifest.get(d["uid"])
    if portal and portal != d["title"]:
        diagnostics.append(f"title differs from the portal: {d['uid']}: agenda={d['title']!r} portal={portal!r}")
    official = sources.get(d["uid"])
    chair = d["source"]
    if official:
        chair_org = re.sub(r"\s*\([^()]*\)\s*$", "", chair).strip()
        if chair_org != official:
            diagnostics.append(f"source differs from the portal: {d['uid']}: chair text={chair!r} portal={official!r} (portal used)")
        source = official
    else:
        diagnostics.append(f"no portal source for {d['uid']}: chair text used")
        source = chair
    return {
        "uid": d["uid"], "title": d["title"], "source": source,
        "presenter": m["presenter_placeholder"], "summary": d["summary"],
        "outcome": m["outcome_placeholder"],
    }


def annex_context(meeting: dict) -> dict | None:
    """Annex A: the participant list of the meeting, read from the local roster (never from the network).

    The roster is written by `meeting_report participants`; run that first to refresh it.
    """
    cfg = meeting.get("annex")
    if not cfg:
        return None
    uid = cfg["roster"]
    path = participants_mod.RAW_DIR / (uid.replace("#", "-") + ".json")
    if not path.exists():
        raise SystemExit(f"roster for {uid} not found at {path}; run `meeting_report participants` first")
    raw = json.loads(path.read_text(encoding="utf-8"))
    rows = [
        {"first": first, "last": last, "org": org, "role": role, "presence": presence,
         "date": when.strftime("%Y-%m-%d")}
        for first, last, org, role, presence, when in participants_mod.roster_rows(raw)
    ]
    return {"heading": cfg["heading"], "caption": cfg["caption"], "rows": rows}


def build_context(meeting: dict, workitem_rows: list[dict], manifest: dict[str, str],
                  sources: dict[str, str] | None = None):
    """Return (context for the agenda template, diagnostics list).

    Liaison statements IN are listed in 1.4 (from [[ls.docs]]), not in section 2.
    """
    sources = sources or {}
    m = meeting["meeting"]
    diagnostics: list[str] = []
    topics = []
    for t in meeting["topics"]:
        docs = [doc_entry(d, m, manifest, diagnostics, sources) for d in t["docs"]]
        topics.append({"title": t["title"], "docs": docs})
    ls_in = [doc_entry(d, m, manifest, diagnostics, sources) for d in meeting["ls"].get("docs", [])]
    wi = []
    for row in workitem_rows:
        item = normalise_workitem(row, meeting.get("wi_titles", {}), meeting.get("wi_notes", {}))
        if item["_truncated"] and item["wi"] not in meeting.get("wi_titles", {}):
            diagnostics.append(f"portal list truncated (title or status): {item['wi']}; list shows {item['_portal_title']!r}")
        wi.append({k: v for k, v in item.items() if not k.startswith("_") and k != "wi"})
    ctx = {
        "meeting": {"tc": m["tc"], "label": m["label"]},
        "agenda": meeting["agenda"],
        "ls": {"docs": ls_in, "out": meeting["ls"]["out"]},
        "board": meeting["board"],
        "sub_tc": meeting["sub_tc"],
        "admin_items": meeting.get("admin_items", []),
        "topics": topics,
        "wi": wi,
        "wrapup": meeting["wrapup"],
        "annex": annex_context(meeting),
    }
    return ctx, diagnostics
