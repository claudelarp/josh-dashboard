#!/usr/bin/env python3
"""Regenerate dashboard.html from projects/*/tasks.md. Stdlib only, no network.

Task line format (forgiving):  - [ ] text (added YYYY-MM-DD) !due:YYYY-MM-DD
Run: python3 scripts/build-dashboard.py   (or ask Claude to "refresh the dashboard")
"""
import html
import re
from datetime import date, datetime, timedelta
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
OUT = VAULT / "dashboard.html"

# Fixed order + fixed color slots (validated palette; color follows the domain, never rank)
DOMAINS = [
    ("business", "Business", "#2a78d6", "#3987e5"),
    ("fitness-health", "Fitness & Health", "#eb6834", "#d95926"),
    ("marketing", "Marketing", "#1baf7a", "#199e70"),
    ("school", "School", "#eda100", "#c98500"),
    ("self-development", "Self-development", "#e87ba4", "#d55181"),
]

TASK_RE = re.compile(r"^\s*-\s*\[(?P<done>[ xX])\]\s*(?P<text>.+)$")
DUE_RE = re.compile(r"!due:(\d{4}-\d{2}-\d{2})")
ADDED_RE = re.compile(r"\(added \d{4}-\d{2}-\d{2}\)")


def parse_tasks(path):
    tasks = []
    if not path.exists():
        return tasks
    for line in path.read_text(encoding="utf-8").splitlines():
        m = TASK_RE.match(line)
        if not m:
            continue
        text = m.group("text").strip()
        due = None
        dm = DUE_RE.search(text)
        if dm:
            try:
                due = date.fromisoformat(dm.group(1))
            except ValueError:
                pass
        text = DUE_RE.sub("", ADDED_RE.sub("", text)).strip(" —-")
        tasks.append({"done": m.group("done") != " ", "text": text, "due": due})
    return tasks


def badge(due, today):
    if due is None:
        return ""
    ds = due.strftime("%b %-d")
    if due < today:
        return f'<span class="pill pill-overdue">⚠ overdue · {ds}</span>'
    if due == today:
        return '<span class="pill pill-today">● due today</span>'
    if due <= today + timedelta(days=3):
        return f'<span class="pill pill-soon">{ds}</span>'
    return f'<span class="pill pill-later">{ds}</span>'


def main():
    today = date.today()
    cols, focus = [], []
    total_open = 0

    for slug, label, light, dark in DOMAINS:
        tasks = parse_tasks(VAULT / "projects" / slug / "tasks.md")
        open_t = [t for t in tasks if not t["done"]]
        done_n = sum(1 for t in tasks if t["done"])
        total_open += len(open_t)
        open_t.sort(key=lambda t: (t["due"] is None, t["due"] or date.max))
        for t in open_t:
            if t["due"] and t["due"] <= today:
                focus.append((slug, label, t))
        rows = "".join(
            f'<li>{badge(t["due"], today)}<span class="task-text">{html.escape(t["text"])}</span></li>'
            for t in open_t
        ) or '<li class="empty">nothing open</li>'
        cols.append(f"""
      <section class="col" style="--accent:{light};--accent-dark:{dark}">
        <h2><span class="chip" aria-hidden="true"></span>{label}
            <span class="count">{len(open_t)} open · {done_n} done</span></h2>
        <ul>{rows}</ul>
      </section>""")

    if focus:
        focus_html = "".join(
            f'<li><span class="chip" style="--accent:{l};--accent-dark:{d}" aria-hidden="true"></span>'
            f'<strong>{lbl}</strong> — {html.escape(t["text"])} {badge(t["due"], today)}</li>'
            for (slug, lbl, t), (s2, l2, l, d) in (
                ((f_, f_[1], f_[2]), (dm[0], dm[1], dm[2], dm[3]))
                for f_ in focus for dm in DOMAINS if dm[0] == f_[0]
            )
        )
    else:
        focus_html = '<li class="empty">Nothing overdue or due today — pick from the columns below.</li>'

    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    day = today.strftime("%A, %B %-d")

    OUT.write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mission Control — {today.isoformat()}</title>
<style>
:root {{
  color-scheme: light;
  --page:#f9f9f7; --surface:#fcfcfb; --ink:#0b0b0b; --ink-2:#52514e; --muted:#898781;
  --hairline:#e1e0d9; --ring:rgba(11,11,11,.10);
  --overdue:#d03b3b; --warning:#fab219;
}}
@media (prefers-color-scheme: dark) {{ :root:where(:not([data-theme="light"])) {{
  color-scheme: dark;
  --page:#0d0d0d; --surface:#1a1a19; --ink:#ffffff; --ink-2:#c3c2b7; --muted:#898781;
  --hairline:#2c2c2a; --ring:rgba(255,255,255,.10);
}} }}
:root[data-theme="dark"] {{
  color-scheme: dark;
  --page:#0d0d0d; --surface:#1a1a19; --ink:#ffffff; --ink-2:#c3c2b7; --muted:#898781;
  --hairline:#2c2c2a; --ring:rgba(255,255,255,.10);
}}
* {{ box-sizing:border-box; margin:0 }}
body {{ background:var(--page); color:var(--ink);
  font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif; padding:24px; }}
header {{ max-width:1200px; margin:0 auto 20px }}
header h1 {{ font-size:22px; font-weight:650 }}
header p {{ color:var(--ink-2); margin-top:2px }}
.focus {{ max-width:1200px; margin:0 auto 24px; background:var(--surface);
  border:1px solid var(--ring); border-radius:10px; padding:14px 18px }}
.focus h2 {{ font-size:13px; text-transform:uppercase; letter-spacing:.04em;
  color:var(--muted); margin-bottom:8px }}
.focus ul {{ list-style:none }} .focus li {{ padding:4px 0; display:flex; gap:8px; align-items:baseline; flex-wrap:wrap }}
.grid {{ max-width:1200px; margin:0 auto; display:grid;
  grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:14px }}
.col {{ background:var(--surface); border:1px solid var(--ring); border-radius:10px; padding:14px 16px }}
.col h2 {{ font-size:15px; font-weight:650; display:flex; align-items:center; gap:8px; flex-wrap:wrap;
  padding-bottom:10px; border-bottom:1px solid var(--hairline); margin-bottom:10px }}
.chip {{ width:10px; height:10px; border-radius:3px; background:var(--accent); flex:none }}
@media (prefers-color-scheme: dark) {{ :root:where(:not([data-theme="light"])) .chip {{ background:var(--accent-dark) }} }}
:root[data-theme="dark"] .chip {{ background:var(--accent-dark) }}
.count {{ margin-left:auto; font-size:12px; font-weight:400; color:var(--muted);
  font-variant-numeric:tabular-nums }}
.col ul {{ list-style:none }}
.col li {{ padding:6px 0; border-bottom:1px solid var(--hairline); display:flex; gap:6px;
  align-items:baseline; flex-wrap:wrap }}
.col li:last-child {{ border-bottom:none }}
.task-text {{ color:var(--ink) }}
.empty {{ color:var(--muted); font-style:italic }}
.pill {{ font-size:11px; font-weight:600; border-radius:999px; padding:1px 8px;
  white-space:nowrap; font-variant-numeric:tabular-nums }}
.pill-overdue {{ background:var(--overdue); color:#fff }}
.pill-today {{ background:var(--warning); color:#0b0b0b }}
.pill-soon {{ border:1px solid var(--hairline); color:var(--ink-2) }}
.pill-later {{ color:var(--muted) }}
footer {{ max-width:1200px; margin:20px auto 0; color:var(--muted); font-size:12px }}
</style></head><body>
<header><h1>Mission Control</h1><p>{day} · {total_open} open tasks</p></header>
<div class="focus"><h2>Today's focus</h2><ul>{focus_html}</ul></div>
<div class="grid">{"".join(cols)}</div>
<footer>Generated {generated} · refresh: ask Claude “refresh the dashboard” or run
<code>python3 scripts/build-dashboard.py</code> · tasks live in <code>projects/&lt;domain&gt;/tasks.md</code></footer>
</body></html>
""", encoding="utf-8")
    print(f"dashboard.html: {total_open} open tasks across {len(DOMAINS)} domains, {len(focus)} in today's focus")


if __name__ == "__main__":
    main()
