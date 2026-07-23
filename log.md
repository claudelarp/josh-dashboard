# Log

Append-only, chronological. Newest entry at the bottom.
Format: `## [YYYY-MM-DD] <ingest|research|query|lint> | <domain> | <title>`

## [2026-07-22] ingest | meta | LLM Wiki pattern (idea document)

- Source: `raw/meta/llm-wiki-pattern.md` (pasted idea file — the founding design doc for this vault)
- New: [[2026-07-22-llm-wiki-pattern]] (source page), [[llm-maintained-wiki]] (concept page)
- `index.md` updated with both.
- This is also the vault's first ingest, run as the worked example.

## [2026-07-22] ingest | meta | Mission Control: PRD v1 + interview v2 + build spec

- Sources committed: `raw/meta/prd-mission-control-v1.md` (Cowork-targeted PRD found in Downloads), `raw/meta/mission-control-interview-v2.md` (blank scoping interview + Fable 5 synthesis prompt).
- New pages: [[2026-07-22-prd-mission-control-v1]], [[2026-07-22-mission-control-interview-v2]] (sources), [[mission-control-spec]] (synthesis — the deliverable).
- Headline rulings in the spec: Claude Code + this vault supersede Cowork/`~/cowork/` as runtime/root; `ops/` layer to be partitioned beside `wiki/` with two contracts; aggressive cut list; v0 = context seed + Shopify sync + morning brief; ten gates (G1–G10) mapped to unanswered interview questions; kill criterion proposed for 2026-10-01.
- Reviewed and approved by Josh same day.

## [2026-07-23] build | meta | Overnight build: P0–P2 + skill scaffolds

- P0: git init (local-only), `.gitignore`/`.env`, `ops/` layer + two-contract `CLAUDE.md` update, `ops/schemas.md`, context templates with evidence-marked drafts, vercel-react-best-practices retired.
- P1: first live Shopify pull (belated / wearbelated.com — Jul 22: 0 orders; 12 variants, all zero inventory, **no SKU codes set store-wide**); `scripts/shopify-sync.py` + daily 05:30 launchd job loaded. Token pending Josh (checklist in `ops/connections/shopify.md`).
- P2: `morning-brief` skill; headless Claude CLI installed + smoke-tested; first brief generated (`ops/briefs/brief-2026-07-23.md`); 06:30 plist staged at `scripts/launchd/` — auto-install blocked by permission classifier, one-line install in the handoff.
- Scaffolds: `wiki-ops`, `intel-intake`, `restock-call`, `scripts/check-collisions.sh` (passing).
- Calendar enumerated (primary + US holidays; empty next 14 days). Handoff: `morning-handoff-2026-07-23.md` (Josh: install job, token, drop facts, context sitting).

## [2026-07-23] build | meta | Course-correction: simple mission control (projects + dashboard)

- Josh's directive (now in CLAUDE.md Scope rules): no reading files outside the vault unless he points at them; start simple, core product is daily task/time organization.
- New: `projects/<domain>/` chatbot folders ×5 (business, fitness-health, marketing, school, self-development) — each a CLAUDE.md persona + tasks.md + notes.md; nested-CLAUDE.md loading makes each folder its own chat context.
- New: `dashboard.html` + `scripts/build-dashboard.py` (validated palette, light/dark, today's-focus strip + 5 columns; due-date pills tested). Morning brief now also regenerates it and reads project task lists.
- Parked, dormant: Shopify token task, 06:30 auto-brief install, phases P3–P5, all ops/context sitting questions. `ops/tasks.md` reduced to system-maintenance only.

## [2026-07-23] build | meta | Interactive dashboard (Jarvis-style, config-driven)

- Replaced the static generated `dashboard.html` with a self-contained interactive app (single file, no build step, localStorage state). Based on a "personal Jarvis" spec Josh supplied, adapted to his 5 domains + a Stats tab.
- Features: dark aesthetic (radial washes, grain, glass), goal ticker (5s cycle, instant updates), SVG day ring (sun-palette, configurable wake/sleep), Today/Plan-Tomorrow cards (streak, segmented bar, inline edit, drag-reorder, queue flag, push-remaining, 6AM day boundary, rollover-with-history), score tiles, per-domain tabs with backlogs, Stats (7-day trend bar/line, domain donut/pie/bars, per-domain rings, 10-week heatmap), custom habit trackers, and a full Settings modal (fonts, colors, domain CRUD, trackers, tab/widget add/remove/reorder/resize, JSON export/import). Config-driven via a widget registry so new widgets/domains/tabs are cheap.
- Data model: localStorage + **seed bridge**. `scripts/build-dashboard.py` rewritten from a whole-file generator into a **marker-based seed injector** — pushes open `projects/*/tasks.md` tasks into the `<!--SEED-->` block only, refuses if markers missing; app merges unseen items (hash-deduped, deletions stick). Rollover now writes `dash_history_v1` before deleting old days (fixes history loss).
- Verified: 50/50 jsdom functional tests (add/check/rollover/streak/seed-dedupe/domain-CRUD/trackers/stats), puppeteer render QA (desktop, Stats, domain tab, settings modal, true 390px mobile), zero console errors, injector idempotent + end-to-end import confirmed. Default domain colors validated colorblind-safe against #050506.
- Docs updated: CLAUDE.md dashboard/seed-bridge section, morning-brief skill. No AI/automation added (deferred per Josh); Polish button ships with empty key + plain-add fallback.
