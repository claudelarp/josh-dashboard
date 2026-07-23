#!/usr/bin/env python3
"""Push open tasks from projects/<domain>/tasks.md into dashboard.html's seed block.

The dashboard is a self-contained interactive app whose state lives in the browser
(localStorage). This script does NOT generate the page — it only rewrites the JSON
between the <!--SEED--> ... <!--/SEED--> markers, so the app is never clobbered.
The dashboard merges unseen seed items on next load (deduped by hash; deletions in
the browser stick). Edit a task's text and it re-imports as a new item — expected.

Refuses to write if the markers are missing (that means the file isn't the app).

Usage:  python3 scripts/build-dashboard.py            # inject
        python3 scripts/build-dashboard.py --dry-run   # print what would inject
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
DASH = VAULT / "dashboard.html"
PROJECTS = VAULT / "projects"
# Folder names here are also the dashboard's default domain ids (kept in sync with CLAUDE.md).
DOMAINS = ["business", "fitness-health", "marketing", "school", "self-development"]

SEED_RE = re.compile(r"(<!--SEED-->)(.*?)(<!--/SEED-->)", re.DOTALL)
TASK_RE = re.compile(r"^\s*-\s*\[ \]\s*(?P<text>.+)$")   # only OPEN tasks
DUE_RE = re.compile(r"!due:(\d{4}-\d{2}-\d{2})")
ADDED_RE = re.compile(r"\(added \d{4}-\d{2}-\d{2}\)")


def fnv1a(s: str) -> str:
    """32-bit FNV-1a over UTF-16 code units, base36 — stable id for dedupe."""
    h = 0x811c9dc5
    for ch in s:
        for unit in _utf16_units(ch):
            h ^= unit
            h = (h * 0x01000193) & 0xFFFFFFFF
    return _base36(h)


def _utf16_units(ch: str):
    cp = ord(ch)
    if cp <= 0xFFFF:
        return (cp,)
    cp -= 0x10000
    return (0xD800 + (cp >> 10), 0xDC00 + (cp & 0x3FF))


def _base36(n: int) -> str:
    if n == 0:
        return "0"
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    while n:
        n, r = divmod(n, 36)
        out = digits[r] + out
    return out


def clean(text: str):
    """Return (display_text, due_or_None). Strips markers; keeps original case for display."""
    due_m = DUE_RE.search(text)
    due = due_m.group(1) if due_m else None
    t = DUE_RE.sub("", ADDED_RE.sub("", text))
    t = re.sub(r"\s+", " ", t).strip(" -—")
    return t, due


def collect():
    items, seen_hashes = [], set()
    for dom in DOMAINS:
        f = PROJECTS / dom / "tasks.md"
        if not f.exists():
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            m = TASK_RE.match(line)
            if not m:
                continue
            text, due = clean(m.group("text"))
            if not text:
                continue
            h = fnv1a(dom + "|" + re.sub(r"\s+", " ", text.lower()).strip())
            if h in seen_hashes:
                continue
            seen_hashes.add(h)
            item = {"h": h, "domain": dom, "text": text}
            if due:
                item["due"] = due
            items.append(item)
    return items


def main():
    dry = "--dry-run" in sys.argv
    if not DASH.exists():
        print("dashboard.html not found — nothing to inject into.", file=sys.stderr)
        return 1
    html = DASH.read_text(encoding="utf-8")
    if not SEED_RE.search(html):
        print("REFUSING: <!--SEED--> markers not found in dashboard.html.\n"
              "This file is not the interactive dashboard (or the markers were removed).\n"
              "No changes written.", file=sys.stderr)
        return 2
    items = collect()
    payload = json.dumps({"generated": date.today().isoformat(), "items": items}, ensure_ascii=False)
    block = '\n<script type="application/json" id="claude-seed">' + payload + '</script>\n'
    if dry:
        print(payload)
        print(f"\n(dry run) {len(items)} open task(s) across {len(DOMAINS)} domains would be injected.")
        return 0
    new_html = SEED_RE.sub(lambda m: m.group(1) + block + m.group(3), html, count=1)
    DASH.write_text(new_html, encoding="utf-8")
    print(f"Injected {len(items)} open task(s) into dashboard.html seed. "
          f"Reload the page (or reopen it) to pull them in.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
