#!/usr/bin/env python3
"""Print deterministic context for generating the next FitFriends session."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path


SESSION_RE = re.compile(r"session-(\d{4}-\d{2}-\d{2})\.md$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        default=".",
        help="FitFriends repository root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--today",
        help="Override today's date as YYYY-MM-DD for testing.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of a readable summary.",
    )
    return parser.parse_args()


def upcoming_wednesday(today: date) -> date:
    wednesday = 2
    delta = (wednesday - today.weekday()) % 7
    if delta == 0:
        delta = 7
    return today + timedelta(days=delta)


def session_dates(history_dir: Path) -> list[tuple[date, Path]]:
    sessions: list[tuple[date, Path]] = []
    if not history_dir.exists():
        return sessions

    for path in history_dir.iterdir():
        match = SESSION_RE.match(path.name)
        if not match:
            continue
        sessions.append((datetime.strptime(match.group(1), "%Y-%m-%d").date(), path))

    return sorted(sessions, reverse=True)


def index_contains(index_path: Path, session_date: str) -> bool:
    if not index_path.exists():
        return False
    return f"'{session_date}'" in index_path.read_text(encoding="utf-8")


def count_video_mappings(videos_path: Path) -> int:
    if not videos_path.exists():
        return 0
    return sum(
        1
        for line in videos_path.read_text(encoding="utf-8").splitlines()
        if "–" in line and "youtu" in line
    )


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).expanduser().resolve()
    today = (
        datetime.strptime(args.today, "%Y-%m-%d").date()
        if args.today
        else date.today()
    )
    target_date = upcoming_wednesday(today)
    target_date_text = target_date.isoformat()
    history_dir = repo / "history"
    sessions = session_dates(history_dir)
    recent = sessions[:2]

    payload = {
        "repo": str(repo),
        "today": today.isoformat(),
        "next_wednesday": target_date_text,
        "target_file": str(history_dir / f"session-{target_date_text}.md"),
        "target_exists": (history_dir / f"session-{target_date_text}.md").exists(),
        "recent_sessions": [
            {"date": session_date.isoformat(), "path": str(path)}
            for session_date, path in recent
        ],
        "index_path": str(repo / "index.html"),
        "index_contains_target": index_contains(repo / "index.html", target_date_text),
        "videos_path": str(repo / "videos.md"),
        "video_mapping_count": count_video_mappings(repo / "videos.md"),
    }

    if args.json:
        print(json.dumps(payload, indent=2))
        return 0

    print(f"Repo: {payload['repo']}")
    print(f"Today: {payload['today']}")
    print(f"Next Wednesday: {payload['next_wednesday']}")
    print(f"Target file: {payload['target_file']}")
    print(f"Target exists: {payload['target_exists']}")
    print("Most recent sessions to read:")
    if recent:
        for item in payload["recent_sessions"]:
            print(f"- {item['date']}: {item['path']}")
    else:
        print("- none found")
    print(f"Index file: {payload['index_path']}")
    print(f"Index already contains target: {payload['index_contains_target']}")
    print(f"Video cache: {payload['videos_path']}")
    print(f"Video mappings: {payload['video_mapping_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
