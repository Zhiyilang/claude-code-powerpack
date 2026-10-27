#!/usr/bin/env python3
"""Generate a grouped CHANGELOG.md from git history.

Usage:
    python gen_changelog.py [since-tag-or-date] > CHANGELOG.md

Conventional-Commits aware. Stdlib only — works offline, no pip install.
"""
import subprocess
import re
import sys
import datetime

TYPE_LABELS = [
    ("feat", "Features"),
    ("fix", "Bug Fixes"),
    ("perf", "Performance"),
    ("refactor", "Refactoring"),
    ("docs", "Documentation"),
    ("test", "Tests"),
    ("style", "Styles"),
    ("build", "Build"),
    ("ci", "CI"),
    ("chore", "Chores"),
]


def git_log(since=None):
    cmd = ["git", "log", "--pretty=format:%s|%h|%ad", "--date=short"]
    if since:
        cmd.insert(1, f"{since}..HEAD" if ".." not in since else since)
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode(
            errors="replace"
        )
    except subprocess.CalledProcessError:
        return []
    return [l for l in out.splitlines() if l.strip()]


def parse(msg):
    m = re.match(
        r"^(?P<type>\w+)(?:\((?P<scope>[^)]+)\))?(?P<break>!)?:\s*(?P<desc>.+)$",
        msg,
    )
    if not m:
        return ("other", msg.strip())
    return (m.group("type"), m.group("desc").strip())


def main():
    since = sys.argv[1] if len(sys.argv) > 1 else None
    entries = git_log(since)
    groups = {}
    for line in entries:
        parts = line.split("|")
        if len(parts) < 3:
            continue
        msg, h, d = parts[0], parts[1], parts[2]
        typ, desc = parse(msg)
        groups.setdefault(typ, []).append((d, h, desc))

    lines = ["# Changelog", "", f"_Generated {datetime.date.today()} from git history_", ""]
    order = [t for t, _ in TYPE_LABELS] + ["other"]
    for typ in order:
        items = groups.get(typ)
        if not items:
            continue
        label = dict(TYPE_LABELS).get(typ, "Other")
        lines.append(f"## {label}")
        for d, h, desc in items:
            lines.append(f"- {desc} (`{h}`, {d})")
        lines.append("")
    print("\n".join(lines).rstrip() + "\n")


if __name__ == "__main__":
    main()
