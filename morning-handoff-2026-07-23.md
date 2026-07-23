# Morning handoff — overnight build, 2026-07-23

**Your first brief is ready: `ops/briefs/brief-2026-07-23.md`.** Read that first — it has two real decisions in it.

## What got built (P0–P2 + scaffolds, all committed to git)

- **Rails:** git repo (local-only), `.gitignore`/`.env`, the `ops/` layer beside the wiki (two contracts documented in `CLAUDE.md`), `ops/schemas.md`, `vercel-react-best-practices` retired to `.agents/skills-retired/`.
- **Commerce:** first real data pulled from your live store last night — `sales-daily.json` (Jul 22: 0 orders) and `inventory.json` (12 variants, all zero stock). `scripts/shopify-sync.py` written + tested (graceful no-token mode) and **scheduled daily 05:30** (launchd job loaded and verified).
- **The brief:** `morning-brief` skill built; today's brief generated as its test. Headless Claude CLI installed (`~/.local/bin/claude`, v2.1.218) and smoke-tested OK.
- **Skills:** `wiki-ops`, `intel-intake`, `restock-call` scaffolded with their hard gates; `scripts/check-collisions.sh` passing; all registered and discoverable.
- **Context templates:** `ops/context/` (people/terminology/priorities/voice×4) pre-filled with evidence-marked suggestions for you to confirm — not my inventions, each marked with where it came from.

## Your tasks (≈40 min total, any order)

1. **Install the 06:30 brief schedule (10 seconds).** The permission classifier rightly wouldn't let me auto-install an unattended agent, so:
   `cp "scripts/launchd/com.joshbrain.morning-brief.plist" ~/Library/LaunchAgents/ && launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.joshbrain.morning-brief.plist`
   Until you do, ask me for "morning brief" any time and it generates on demand.
2. **Shopify token (~15 min, once):** checklist in `ops/connections/shopify.md`. Three read-only scopes, paste into `.env`, test with `python3 scripts/shopify-sync.py`. Until then the 05:30 job no-ops quietly.
3. **Drop facts (~5 min):** `ops/drops/inputs/drop-brief-current.md` — your in-flight drop is currently invisible to the system.
4. **Context sitting (~20 min, with me):** confirm/correct the drafts in `ops/context/` — say "context sitting" and I'll walk you through them.

## Findings you should know

- **Store reality:** zero inventory across all 12 variants, no SKU codes set, zero orders Jul 22. The PRD's `BLT-TEE-WSH-M` codes were aspirational. When drop inventory lands, assign real SKUs (brief, decision 2).
- **Calendar is empty** for 14 days out — if your real schedule lives elsewhere (phone calendar, class app), the brief can't see it until it's in Google Calendar.
- **It's on you to ratify:** the kill criterion (Oct 1, two brief-driven actions/week) stands as proposed unless you say otherwise. Recruiting question returns ~Jul 29.

## What's next (when you're ready — nothing blocks today)

P3 needs your Notion export (Content Intelligence Log). P4 is the health sitting. P5 needs product costs + pricing rules (templates ready). Spec: `wiki/meta/synthesis/mission-control-spec.md`.

*Delete this file once you've done the tasks — it's a handoff, not a record. Everything durable is in the spec, the log, and git history.*
