# Mission Control — current state (updated after your course-correction, 2026-07-23)

**Open `dashboard.html` in your browser — that's your daily view now.** Add tasks by telling any chatbot, or by editing `projects/<domain>/tasks.md` directly.

## The simple system, as you asked

- **Five chatbots**, one per life area: open a Claude session in `projects/business/`, `projects/fitness-health/`, `projects/marketing/`, `projects/school/`, or `projects/self-development/` and you're talking to that domain's assistant — each has its own persona, task list, and notes file. (Each folder's CLAUDE.md also works as claude.ai Project instructions if you'd rather have them as app chats.)
- **One dashboard** (`dashboard.html`): today's focus strip (overdue / due today) + a column per domain. Refresh: ask me, or `python3 scripts/build-dashboard.py`.
- **Standing rule, now in the schema:** nothing on your computer gets read unless you point at it. Files enter this system only when you bring them.

## Parked (built, dormant, zero maintenance — ignore freely)

- Shopify sync (05:30 job no-ops quietly without a token; checklist in `ops/connections/shopify.md` *if/when* you want store numbers flowing)
- The 06:30 auto-brief (plist staged at `scripts/launchd/`, one-line install inside it — optional; "morning brief" works on demand)
- Everything else in `ops/` and spec phases P3–P5 — on ice until you ask

## Only if/when you feel like it

- Drop a due date on anything: add `!due:YYYY-MM-DD` to the task line
- The one seeded task (business column): fill your current drop's facts so it can be tracked

*Delete this file whenever — the durable record is in the spec, log.md, and git.*
