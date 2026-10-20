"""Command line for the meeting-report pipeline.

  uv run python -m meeting_report roundtrip  --meeting <meeting.toml> --base <agenda.docx> [--workitems <file>] [--reference <agenda.docx>]
  uv run python -m meeting_report render     --meeting <meeting.toml> --base <agenda.docx> --out <file.docx> [--workitems <file>]
  uv run python -m meeting_report crawl      --meeting <meeting.toml> [--out-dir var/<label>]
  uv run python -m meeting_report lead       --meeting <meeting.toml> --out <file.md>
  uv run python -m meeting_report participants --tc <TC> --tc <sub-TC code> --meeting <TC>#<nn> --meeting <sub-TC>#<nn> --out <file.xlsx>

Rules: `render` writes only to the file given; `lead` refuses to overwrite an existing lead document;
crawled output goes under tools/var/ (git-ignored) and is never committed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

from . import lead as lead_mod
from . import model
from . import participants
from . import render

TOOLS = Path(__file__).resolve().parent.parent
BODY_TEMPLATE = TOOLS / "templates" / "agenda-body.docx"   # built by build_template.py from a committee document


def workitem_rows(meeting: dict, workitems_file: str | None, out_dir: Path | None) -> list[dict]:
    if workitems_file:
        text = Path(workitems_file).read_text(encoding="utf-8")
        rows = model.parse_workitem_table(text)
    else:
        text = model.run_portal(meeting["meeting"]["profile"],
                                ["workitems", "list", "--tc", meeting["meeting"]["tc"], "--json"])
        if out_dir is not None:
            out_dir.mkdir(parents=True, exist_ok=True)
            stamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
            (out_dir / f"workitems-{stamp}.json").write_text(text, encoding="utf-8")
        rows = model.parse_workitem_json(text)
    if not rows:
        raise SystemExit("no work items parsed from the portal output")
    return rows


def manifest_for(meeting: dict) -> dict[str, str]:
    path = meeting.get("local", {}).get("manifest")
    return model.manifest_titles(Path(path)) if path else {}


def source_map(meeting: dict) -> dict[str, str]:
    """Official sources per TDoc from `documents list -m <meeting> -t <tc> --json` (no session needed)."""
    m = meeting["meeting"]
    text = model.run_portal(m["profile"], ["documents", "list", "-m", str(m["portal_meeting_id"]),
                                            "-t", m["tc"], "--json"])
    return model.portal_sources(model.parse_documents_json(text))


def cmd_render(args) -> int:
    meeting = model.load_meeting(Path(args.meeting))
    rows = workitem_rows(meeting, args.workitems, None)
    ctx, diagnostics = model.build_context(meeting, rows, manifest_for(meeting), source_map(meeting))
    render.render_agenda(Path(args.base), BODY_TEMPLATE, ctx, meeting["meeting"]["anchor"], Path(args.out))
    print(f"rendered: {args.out}")
    for d in diagnostics:
        print("  note:", d)
    return 0


def cmd_roundtrip(args) -> int:
    meeting = model.load_meeting(Path(args.meeting))
    out_dir = TOOLS / "var" / meeting["meeting"]["label"].lower().replace("#", "")
    rows = workitem_rows(meeting, args.workitems, out_dir / "raw")
    ctx, diagnostics = model.build_context(meeting, rows, manifest_for(meeting), source_map(meeting))
    rendered = out_dir / "roundtrip.docx"
    render.render_agenda(Path(args.base), BODY_TEMPLATE, ctx, meeting["meeting"]["anchor"], rendered)
    print(f"rendered (scratch): {rendered}")
    if args.reference:
        diff, n = render.compare(Path(args.reference), rendered)
        print(f"differences vs reference: {n}")
        for line in diff:
            print("  " + line)
    for d in diagnostics:
        print("  portal:", d)
    return 0


def cmd_crawl(args) -> int:
    meeting = model.load_meeting(Path(args.meeting))
    out_dir = Path(args.out_dir) if args.out_dir else TOOLS / "var" / meeting["meeting"]["label"].lower().replace("#", "")
    rows = workitem_rows(meeting, None, out_dir / "raw")
    manifest = manifest_for(meeting)
    norm = [model.normalise_workitem(r, meeting.get("wi_titles", {}), meeting.get("wi_notes", {})) for r in rows]
    norm = [{k: v for k, v in n.items() if not k.startswith("_")} for n in norm]
    out_dir.mkdir(parents=True, exist_ok=True)
    import json
    (out_dir / "normalised.json").write_text(
        json.dumps({"workitems": norm, "manifest_documents": len(manifest)}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"crawled: {len(rows)} work items, {len(manifest)} manifest documents -> {out_dir}")
    return 0


def cmd_lead(args) -> int:
    meeting = model.load_meeting(Path(args.meeting))
    rows = workitem_rows(meeting, args.workitems, None)
    ctx, _ = model.build_context(meeting, rows, manifest_for(meeting), source_map(meeting))
    lead_mod.render_lead(TOOLS / "templates" / "lead.md.j2", ctx, meeting, Path(args.out))
    print(f"lead document written: {args.out}")
    return 0


def cmd_participants(args) -> int:
    try:
        counts = participants.build(
            args.tc, args.meeting, Path(args.out),
            binary=args.bin, profile=args.profile,
            raw_dir=Path(args.raw_dir) if args.raw_dir else participants.RAW_DIR)
    except participants.ParticipantsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"participants written: {args.out}")
    for uid, n in counts.items():
        print(f"  {uid}: {n} registered")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="meeting_report")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn in [("render", cmd_render), ("roundtrip", cmd_roundtrip), ("crawl", cmd_crawl), ("lead", cmd_lead)]:
        s = sub.add_parser(name)
        s.add_argument("--meeting", required=True)
        s.add_argument("--workitems", help="read the workitems table from a file instead of the portal")
        if name in ("render", "roundtrip"):
            s.add_argument("--base", required=True, help="the meeting's own agenda document: its head (cover, schedule, IPR) is kept")
        if name == "render":
            s.add_argument("--out", required=True)
        if name == "roundtrip":
            s.add_argument("--reference", help="existing agenda/report to compare the body with")
        if name == "crawl":
            s.add_argument("--out-dir")
        if name == "lead":
            s.add_argument("--out", required=True)
        s.set_defaults(func=fn)
    s = sub.add_parser("participants", help="participant list workbook, one sheet per meeting")
    s.add_argument("--tc", action="append", default=[], help="committee short code or TBID; repeatable (<TC>, <sub-TC code>)")
    s.add_argument("--meeting", action="append", default=[], help="meeting UID (<TC>#<nn>) or portal ID; repeatable")
    s.add_argument("--out", required=True, help="workbook path (keep it outside git: personal data)")
    s.add_argument("--profile", help="etsi-portal-tool profile (default: the tool's own default)")
    s.add_argument("--bin", help="path to etsi-portal-tool (default: PATH or ETSI_PORTAL_TOOL_BIN)")
    s.add_argument("--raw-dir", help="where the raw rosters go (default: tools/var/participants)")
    s.set_defaults(func=cmd_participants)
    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
