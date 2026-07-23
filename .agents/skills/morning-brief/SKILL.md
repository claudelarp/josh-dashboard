---
name: morning-brief
description: Generate today's one-page brief from calendar, commerce data, health logistics, and tasks. Fires on "morning brief", "daily brief", "what's my day". Not for general questions about the vault.
---

# morning-brief

One page, five fixed sections, before the day starts. This is the product — everything else in `ops/` exists to feed it accurate facts. Scheduled daily 06:30 ET (weekends included) via `scripts/run-morning-brief.sh`; also runs on demand.

## Reads

- Google Calendar connector: today + next 14 days (`joshpnieman@gmail.com` + US holidays — see `ops/connections/google-calendar.md`)
- `ops/commerce/data/sales-daily.json`, `inventory.json`, `sku-performance.json` (if present)
- `ops/content/data/content-calendar.json` (if present)
- `ops/health/data/refills.json`, `appointments.json` (if present)
- `ops/drops/data/drops.json` (if present)
- `ops/tasks.md`
- `ops/context/current-priorities.md`

## Writes

`ops/briefs/brief-YYYY-MM-DD.md` — nothing else. Then move any brief older than 14 days into `ops/briefs/archive/`, and run `python3 scripts/build-dashboard.py` so `dashboard.html` reflects the morning's task state.

Also read `projects/*/tasks.md` — those are the live per-domain task lists; the brief's Open loops section covers them plus `ops/tasks.md`.

## Output format (exactly these sections, this order)

```
# Brief — <Weekday> <D Month YYYY>

## Today
[Calendar events in time order. Class/deadline items marked distinctly from Belated commitments. School items suppressed while current-priorities says summer break.]

## Needs a decision
[Deadlines inside 72h; SKU verdict changes since last brief; drop blockers. Max five items — if more, keep the five that cost most if missed.]

## Belated
[Yesterday's orders + net revenue, one line. Any SKU under 14 days of cover (needs sales history — say "insufficient history" until ~2 weeks of data). Today's content slot + whether its script exists.]

## Health
[Refills where reorder_on <= today. Appointments next 14 days. needs-scheduling items past 50% of their due_by window. Facts and dates only — no medical content beyond logistics.]

## Open loops
[Unchecked ops/tasks.md items older than 5 days.]
```

## Hard rules

- **Stale data:** any source file missing or >48h old gets a `## Stale data` section naming the file and its age. Never report old numbers as current. Distinguish **"not seeded yet (pending phase P3/P4/G-gate)"** from **"stale (was fresh, now old)"** — only the second is an alarm; don't cry wolf during the build-out.
- If the Calendar connector is unreachable (possible headless), say so under Stale data and continue — a partial brief beats none.
- Blossom items ride in Today / Needs a decision / Open loops via calendar + tasks until its ops domain exists (gate G7) — no invented Blossom section.
- Read-and-summarize only: never write to `inputs/`, `context/`, or any `data/` file; no medical advice of any kind.
- Recruiting placeholder: if `current-priorities.md` still says "re-ask ~2026-07-29" and today is on/after that date, add one line under Open loops: "Recruiting question pending (G2) — answer it."

## Known failures

*(append one dated line per failure: trigger → wrong behavior → rule that prevents it)*
