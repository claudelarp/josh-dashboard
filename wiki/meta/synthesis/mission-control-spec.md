---
type: synthesis
domain: meta
created: 2026-07-22
updated: 2026-07-22
tags: [mission-control, architecture, spec, business, health, schoolwork]
---

# Mission Control — Build Specification v2

Produced by the Fable 5 synthesis prompt in [[2026-07-22-mission-control-interview-v2]], run against the evidence that actually exists rather than the interview it was designed for, which is blank. Supersedes [[2026-07-22-prd-mission-control-v1]] as the plan of record while adopting most of its content by reference.

**Rule used throughout:** every build item cites its evidence — a PRD workflow, a file observed on this machine, a connector that responds, or a decision Josh made in-session. Anything resting only on an unanswered interview question is cut or gated, per the synthesis prompt's own instruction. Gates are named `G1`–`G10` and collected in §2.5.

---

## 0. Reconciliation — what exists, what conflicts, what governs

Three artifacts now describe this system. They disagree. Resolutions:

| Conflict | PRD v1 says | Reality / newer intent | Ruling |
|---|---|---|---|
| Runtime | Claude Cowork (Desktop + Productivity plugin) | Synthesis prompt's own inputs name Claude Code + Obsidian vault; Josh built exactly that today and fired this prompt from inside it | **Claude Code.** PRD §10 itself anticipated this migration ("the scheduling layer moves to Claude Code") |
| Root | `~/cowork/`, "no existing vault" (Assumption 1) | `~/Desktop/Josh Brain` exists as of today, is an Obsidian vault and a Claude Code project | **Josh Brain is the root.** PRD Assumption 1 is false; its own correction clause applies ("if a vault already exists… the tree is created inside it") |
| Skills location | `toolbox/` | This project's real convention is `.agents/skills/` (symlinked into `.claude/skills/`) | `.agents/skills/` |
| Skill inventory | "eleven skills, all serving the brand" | 12 project skills + 1 global (graphify). Five serve brand/content (market-research, content-engine, crosspost, brand-discovery, taste); the rest are utilities and process tools. The PRD's "existing five drop skills" (§7 Block 8) **do not exist** — no drop-specific skill is installed | Corrected inventory in §5 |
| Dashboard | `dashboard.html` free with the Cowork plugin | In Claude Code it's a build, not a freebie | Cut — see §7 |
| Blossom Medical | Absent from the PRD entirely | Active client work visible on disk (deliverables in Downloads, a Blossom Medical folder); interview §7.7–7.11 asks about scope, consent, credentials — all unanswered | Wiki domain `media` exists (Josh's call, earlier today). **All Blossom automation gated** (G7, G8) |
| Vault schema | inputs/data/outputs, no review gate | Josh Brain runs the LLM-Wiki pattern with a `_review/` approval gate on everything | **Both, partitioned** — see §3.1. The review gate governs knowledge (`wiki/`, `raw/`); the PRD's inputs-rule governs operational state (`ops/`). One root, two contracts, explicitly documented |

What ports from the PRD unchanged: the morning-brief structure and stale-data rule, the inputs-rule, the never-automated list, the clinical boundary (verbatim), the intelligence-log v2 / sku-performance / sales / inventory / refills / appointments / metrics schemas (§5.5 of the PRD, re-rooted under `ops/`), the refresh table, and 13 of its 15 logged decisions. The PRD is not discarded; it is absorbed and re-targeted.

---

## 1. The cut list

Domain by domain. "Cut" means no folders beyond the wiki shelf that already exists, no skills, no schedules, no data pipeline. Each cut names its un-cut condition.

**Self-development / habits — cut entirely.**
Interview 7.20–7.22 (rank what you care about, define visible progress, argue against inclusion) is blank, and 3.8–3.9 (what would you actually record; what have you ever tracked 60+ days) is blank. There is zero data provenance and zero task evidence. The interview's own 7.22 makes the case: these are things you do, not things you manage, and instrumenting them can make them worse. The wiki `habits` domain folder stays as a knowledge shelf (costs nothing). Un-cut condition: 60 consecutive days of any manual tracking, per 3.9's own baseline test — then it has earned a pipeline.

**Fitness — tracking cut, programming permanently out of v2 scope.**
3.1–3.5 are blank; nobody has stated where lifts, mileage, sleep, or bodyweight live today, and "I'd have to type it in" has a known survival rate. The PRD's `metrics.json` conversational daily entry survives only as an optional habit, never on any critical path — nothing else may depend on it existing. The 7.16 conflict rule (physique vs. running — which loses) is unanswered, so the system stores what Josh volunteers and gives no training recommendations. Un-cut condition (G1): 3.1–3.5 answered, and if the answer is a wearable/app, a real export path named.

**Schoolwork — no pipeline; calendar read + research skill only.**
PRD decision #9 stands and the evidence still supports it: deadlines already live in Google Calendar, and a `studies/` pipeline would re-enter existing data. Coursework research is served by extending `market-research` (§5). One artifact ("Academic Planning Module Workbook.xlsx" in Downloads) is not a repeated task. Open finding the interview surfaced that nothing here answers (G2): **7.14, recruiting.** For a McIntire student the recruiting calendar is frequently the real deadline structure hiding behind coursework. If Josh is recruiting this cycle, that changes the brief's priorities and possibly the whole fall build sequence. This one question outranks every other schoolwork consideration.

**Finances — cut as a live domain (PRD non-goal upheld).**
`~/Desktop/Financials/` contains one sample receipt. Shopify payouts and manufacturer wires will be visible in `ops/commerce/` data anyway. The wiki `finances` domain and its tag vocabulary stay for knowledge. Un-cut condition: a year of transactions, or a concrete tax event that demands categorization — whichever comes first.

**Blossom Medical / media — all automation gated; manual skills continue.**
The work is real (deliverables on disk) and the interview treats it seriously, but 2.10 (whose accounts, whose credentials, what's agreed in writing about access) and 7.11 (footage consent tracking, patient-adjacent obligations) are blank. **This is client data with obligations attached (8.6), and some of it is patient-adjacent.** Nothing automated touches Blossom accounts, files, or metrics until G7 (2.10 answered, in writing) and G8 (7.11 answered) clear. Existing skills (content-engine, crosspost, taste) keep serving Blossom work manually, as they already do. 7.10 (scale to more aesthetics clients?) stays open — answering yes later turns client work into a template and merits its own spec revision.

**Brand (Belated) — keep. The only domain that earns a build.**
Live data source (Shopify connector responds), five relevant skills installed, deliverables and design files across Desktop/Documents, PRD-grade scoping already done, daily and weekly rhythms. Even here, cuts inside the domain: `drops/` is not built until Josh confirms a drop actually in flight (G3 — the PRD's `drop-004` example cannot be verified as real, and its "wired to the existing five drop skills" premise is false); Shopify stays **read-only** (PRD decision #11, upheld — write access is a category of public, expensive mistake, revisit after a month of clean reads).

**Cut regardless of domain:**
- **The web app and any custom dashboard** — see §7 for the argument.
- **The autonomous-builder pattern** — PRD already deferred it; nothing new justifies it.
- **Ahrefs** — connector unauthenticated, no cited need.
- **Gmail/Slack/HubSpot/Canva/Figma connections** — no evidenced repeated task consumes them yet (2.4 blank; HubSpot/Canva/Figma are Blossom-adjacent → behind G7 anyway).
- **`vercel-react-best-practices` skill — retire from this project.** With the web app cut, nothing here builds React. It returns only if §7's decision is ever reversed.
- **Any medical decision support — permanently excluded**, not a scoping decision (PRD decision #10, adopted verbatim).

What this leaves standing: one operational build (Belated commerce + content), one cross-domain product (the morning brief), health *logistics* (refills, appointments — the calendar-shaped part of health, which has provenance because Josh types a date once per event, not daily), and the knowledge vault that already exists.

---

## 2. The one-week version

Three things, using only sources confirmed to exist (Shopify connector, Google Calendar connector, this vault):

1. **Context seed** — one sitting with Josh (~60–90 min): `ops/context/people.md`, `ops/context/terminology.md`, `ops/context/current-priorities.md`, and `ops/tasks.md`. Human-written, Claude-transcribed. Everything downstream reads these.
2. **Shopify sync** — a deterministic script (not an agent): daily pull of yesterday's orders and current inventory into `ops/commerce/data/sales-daily.json` (append, deduped by date) and `inventory.json` (overwrite), per the PRD schemas. Requires Josh to create a scoped custom-app token (~20 min, read-only scopes).
3. **The morning brief** — daily scheduled agent run producing `ops/briefs/brief-YYYY-MM-DD.md` from calendar + commerce data + `ops/tasks.md`, in the PRD's five-section format with its stale-data rule intact.

That's the whole v0. No health yet, no content calendar, no verdicts — the brief's Belated section shows revenue and inventory only. It is real value in week one: one page, every morning, spanning calendar and store, refusing to silently report stale numbers. Monthly cost beyond the Claude plan: $0.

### 2.5 The gates — ten answers that unblock everything else

| Gate | Interview item | Unblocks |
|---|---|---|
| G1 | 3.1–3.5 fitness/health data provenance | Any fitness tracking beyond optional notes |
| G2 | 7.14 recruiting timeline | Correct brief priorities for fall; whether schoolwork stays cut |
| G3 | Confirm a drop actually in flight (7.1 timeline) | Building `ops/drops/` |
| G4 | §4 voice artifacts pasted verbatim | `script-writer` producing in-voice drafts |
| G5 | 6.1 Claude plan / unattended budget | Scheduling more than the v0 three runs |
| G6 | 8.4 phone-first or laptop-first | Brief delivery channel; revisiting §7 if ever warranted |
| G7 | 2.10 Blossom credentials + written access agreement | Any Blossom-facing automation |
| G8 | 7.11 footage consent obligations | Whether consent tracking lives in this system at all |
| G9 | 7.5 revenue/profitability reality | `current-priorities.md` money section; whether commerce thresholds are sane |
| G10 | 9.4 kill criterion ratified (a default is proposed in §11) | The shutdown test having teeth |

These are the only interview questions that currently gate a build. The other ~70 improve quality but block nothing.

---

## 3. Context layer

### 3.1 The vault partition — one root, two contracts

```
Josh Brain/                     ← Claude Code project root = Obsidian vault root
  CLAUDE.md                     ← schema for BOTH contracts (updated in phase P0)
  index.md, log.md              ← existing wiki navigation; log.md becomes the single
                                   unified timeline (ops slugs added to the domain registry)
  raw/  wiki/  _review/         ← KNOWLEDGE: LLM-Wiki pattern, review-gated, as built today
  scripts/                      ← tooling (transcribe.py + new sync scripts)
  ops/                          ← OPERATIONS: PRD contract, NOT review-gated
    context/                    ← human-owned context files (the PRD's memory/, renamed)
    tasks.md                    ← open loops; human-edited, brief-read
    briefs/                     ← generated daily; archive/ after 14 days (the hot cache)
    connections/                ← per-service endpoint reference docs + IDs
    schemas.md                  ← the PRD §5.5 schemas, re-rooted (single source of truth)
    commerce/  content/  health/    ← inputs/ (human-only) · data/ (machine-only) · outputs/
    drops/                      ← created only when G3 clears
```

Why two contracts instead of forcing everything through `_review/`: the review gate exists so knowledge claims get human sign-off before becoming canonical. Operational state (yesterday's order count, current inventory) is not a knowledge claim — it's a machine-refreshed fact that would make daily review a chore Josh abandons, and abandonment is the failure mode this whole spec is designed against. The PRD's inputs-rule provides the equivalent safety on the ops side: machines never touch human files, humans never hand-edit machine files. The root `CLAUDE.md` states both contracts and which paths each governs.

Why ops domains (`commerce`, `content`, `health`) differ from wiki domains (`business`, `media`, `health`, …): operational rhythm is not knowledge taxonomy. The PRD's insight stands — content decides daily, commerce decides daily/weekly, drops is episodic — and smashing them into one `business` ops folder would recreate the undifferentiated pile the domains exist to prevent. The mapping is stated once in `CLAUDE.md`: ops `commerce`+`content`+`drops` ↔ wiki `business`; ops `health` ↔ wiki `health`/`fitness`; Blossom ops (future, gated) ↔ wiki `media`. Durable lessons graduate from ops into the wiki through the normal review gate (e.g., a pricing experiment's outcome becomes a `wiki/business/concepts/` page).

### 3.2 Context files

| File | Owner | Contents | Update cadence |
|---|---|---|---|
| `ops/context/people.md` | Josh (Claude transcribes) | One `### Name` prose block per person: manufacturer contacts, providers (no clinical detail — names/roles/channels only), professors, tracked creators, Blossom contacts | On change; lint checks `last_reviewed` quarterly |
| `ops/context/terminology.md` | Josh | SKU code structure, drop codes, internal shorthand, garment terms | On change |
| `ops/context/current-priorities.md` | Josh | The 3–5 things that matter this month, one money paragraph (carries "profitability unknown — G9" until answered) | Weekly, prompted by the Sunday review |
| `ops/context/voice/` (4 files: brand, personal, client, academic) | Josh | **Created as templates containing interview §4's own paste-instructions.** Empty until G4 | Once, then on drift |
| `ops/tasks.md` | Josh | Open loops; brief reads items older than 5 days | Continuous |
| `ops/connections/*.md` | Claude | Per-service endpoint reference: base URLs, scoped-token setup steps, the exact endpoints used, known IDs (location, SKU list) | When integration changes |
| `ops/schemas.md` | Claude (review-gated changes) | The PRD §5.5 schemas with deltas noted | On schema change only |

### 3.3 Session contract (the write-back contract, explicit)

- **Every session reads at start:** root `CLAUDE.md` (automatic), `ops/context/current-priorities.md`, today's brief if it exists. Nothing else is mandatory — three reads, bounded.
- **Sessions write at end:** one `log.md` entry per operation performed (existing convention; ops runs use ops domain slugs in the registered list), plus whatever `data/`/`outputs/`/`briefs/` files the operation owns.
- **Never overwritten by any agent, ever:** anything under `ops/*/inputs/` or `ops/context/` (the inputs-rule — if it looks stale or wrong, say so in the output and stop); anything under `wiki/` or `raw/` outside the review gate; `log.md` history. Human-authored text is never destroyed. Every agent-generated document carries date, source, and links (already enforced by the wiki frontmatter schema; ops outputs carry a `generated:` header line).
- **Hot cache:** `ops/briefs/` *is* the hot cache — the last 14 days of cross-domain state in readable form. No separate cache file is warranted at this scale.
- **Lint:** the existing wiki lint pass extends to ops: stale `data/` files (>48h for daily files), contract violations (any machine write under `inputs/`), briefs reporting on files that no longer exist, `last_reviewed` drift in context files. Cadence: the brief itself reports staleness daily (cheap, automatic); the full lint runs monthly or after ~10 ingests, per the existing schema rule.

---

## 4. Connections layer

Honest note on the synthesis prompt's MCP claim: in this harness, MCP tool schemas are deferred and loaded on demand, so "MCP loads every function into context" overstates the interactive cost here. The preference for direct API + a saved endpoint doc is still correct for everything *scheduled*: a deterministic script with a scoped token has no session dependency, is testable, and fails loudly. Rule adopted: **connectors for interactive work, direct API for scheduled work.**

| Connection | Access method | Credential handling | Scope | Reference doc |
|---|---|---|---|---|
| Shopify | Scheduled: Admin API via custom app. Interactive: existing connector | Token in `Josh Brain/.env`, gitignored, never in chat, never committed | **Read-only:** `read_orders`, `read_products`, `read_inventory` — nothing else. This is the scoped-service-account pattern: the sync job cannot do what its token cannot do | `ops/connections/shopify.md` — endpoints used, store domain, location ID, SKU list |
| Google Calendar | Connector, read-only usage | OAuth already established via claude.ai | Read events only; the system never creates/edits events in v2 | `ops/connections/google-calendar.md` — which calendars feed the brief |
| Notion | **One-shot manual export by Josh** (Markdown & CSV), then migration script | None needed — no API credential is created at all | The Content Intelligence Log only; the rest of the export parks in `ops/content/_notion-raw/` untouched | Migration report doubles as the record |
| Gmail, Slack, HubSpot, Canva, Figma | **Not connected by this spec** | — | No evidenced repeated task consumes them (2.4 blank); HubSpot/Canva/Figma are Blossom-adjacent → G7 | — |
| Ahrefs | **Cut** — unauthenticated, uncited | — | — | — |
| Wearable / Apple Health | **Not a connection until G1** | — | — | — |

Credential rules (all of them): secrets live in `.env` at the vault root; `.gitignore` (created in P0 alongside `git init`) covers `.env` and `_review/`; no secret ever appears in a chat message, a committed file, a skill body, or an endpoint reference doc. Every scheduled job's network scope is exactly the hosts its reference doc names — the Shopify sync talks to the store's admin API and nothing else.

---

## 5. Capabilities layer

### 5.1 Existing inventory — disposition of all 13

| Skill | Disposition | Reason |
|---|---|---|
| market-research | **Extend → absorbs the PRD's `deep-research`** | The PRD's deep-research duplicates it. Extension adds: domain routing (state which wiki/ops domain before starting), reading that domain's context first, output to `wiki/<domain>/…` via `_review/`, and an academic mode for coursework. Do not build a second research skill |
| content-engine, crosspost, taste | Keep as-is | Serve brand + Blossom content manually today; no change until G4/G7 |
| brand-discovery | Keep; run once for Belated if no brandbook exists, then dormant | Its output (voice, positioning) partially feeds G4 |
| docx | Keep | Cross-domain deliverable utility (papers, client docs) |
| browser-use | Keep | Utility; future candidate for post-metrics capture (3.6) — gated, not built |
| brainstorming, grill-me, skill-creator, find-skills | Keep | Process tools; skill-creator builds what's below; find-skills checks the marketplace before any hand-roll |
| vercel-react-best-practices | **Retire from this project** | Nothing builds React once §7 cuts the web app |
| graphify (global) | Keep global, outside default workflows | Already ruled in the vault schema |

### 5.2 New skills — each cites its evidence

All project-scoped in `.agents/skills/` (symlinked per house convention). **Zero new globals** — every one of these is meaningless outside this vault, and graphify remains the only global. All bodies <500 lines; schemas and IDs live in `ops/schemas.md` / `ops/connections/` and are referenced, not duplicated; where a workflow hits the same endpoints or IDs every run, they are hardcoded in the reference doc, not rediscovered.

**`morning-brief`** *(the product; invoked by the scheduler, also on demand)*
- Evidence: the PRD's core thesis; the context-switching cost is the one problem all three artifacts agree on.
- Description (trigger surface): "Generate today's one-page brief from calendar, commerce data, health logistics, and tasks. Fires on 'morning brief', 'daily brief', 'what's my day'. Not for general questions about the vault."
- Workflow: read calendar (today + 14d) → read `ops/commerce/data/*.json`, `ops/health/data/refills.json` + `appointments.json` (if present), `ops/tasks.md`, `ops/content/data/content-calendar.json` (if present) → write `ops/briefs/brief-YYYY-MM-DD.md` in the PRD's five fixed sections → rotate briefs >14 days to `archive/`.
- Guardrails: stale-data section is mandatory when any file is missing or >48h old — never report old numbers as current; max five items under "Needs a decision"; never writes anywhere except `ops/briefs/`; no medical content beyond dates and logistics.

**`intel-intake`** *(on demand)*
- Evidence: "Aston Trejo TikTok Transcripts - Google Docs.pdf" sitting in Downloads is the manual habit, caught mid-act; the Notion Content Intelligence Log exists and is the PRD's Block 2.
- Description: "Turn a creator-video transcript or link into Content Intelligence Log entries with dedupe. Fires on 'log this transcript', 'intel intake', a pasted transcript about content tactics. Not for general video transcription (that's scripts/transcribe.py)."
- Workflow: ingest transcript (paste, file, or transcribe.py output) → extract insights → semantic-dedupe against `intelligence-log.json`: on match, increment `cross_source_count` and append the creator instead of adding a row → append new entries with sequential `cil-` IDs.
- Guardrails: never lowers a `status`; never edits `outcome` (the Sunday review owns that); flags rows it can't classify rather than guessing.

**`restock-call`** *(on demand)*
- Evidence: PRD §6.6; the decision "should I reorder X" recurs by the nature of a 3PL-stocked DTC line; the connector shows a live store.
- Description: "Answer 'should I restock/reorder/discount SKU X' from current data with margin math shown. Fires on restock/reorder/discount questions about a specific SKU. Not for general revenue questions."
- Workflow: read `sku-performance.json` (or compute from sales+inventory if the weekly pass hasn't run), `inputs/product-costs.md`, `inputs/pricing-rules.md` → answer in chat with the verdict logic, days-of-cover, and margin at current price.
- Guardrails: **hard gate — if `product-costs.md` lacks the SKU's landed cost, say so and stop; no margin, no verdict.** Never recommends a price change without stating margin at both old and new price (PRD rule, adopted). Never writes anything.

**`script-writer`** *(on demand — gated G4)*
- Evidence: content is produced for two accounts today (deliverables on disk); the PRD specifies it. But §4 voice capture is blank.
- Description: "Draft a short-form script for the brand or personal account in the captured voice, from a calendar slot or a stated concept. Fires on 'write the script for…'. Refuses in-voice drafting while voice profiles are empty."
- Workflow: read `ops/context/voice/{account}.md`, `hook-bank`, `intelligence-log.json` (prefer `act-now`, `cross_source_count ≥ 2`), the calendar slot → write to `ops/content/outputs/scripts/`.
- Guardrails: **if the voice file is still the template, produce at most a structural draft with a banner saying no voice profile exists (G4) — never fake the voice.** Never marks a calendar slot `filmed/edited/posted` — only Josh's word does that.

**`appointment-prep`** *(on demand — enters at phase P4)*
- Evidence: PRD §6.6 + the health-logistics rhythm (refills/appointments) which, unlike metrics, requires only one typed date per event.
- Description: "Build the question list and context doc for an upcoming medical appointment from logged protocol history. Fires on 'prep for my appointment'. Never gives medical advice."
- Workflow: read `inputs/protocol.md`, `data/metrics.json` (whatever exists), `context/protocol-history` → write `ops/health/outputs/appointment-prep-YYYY-MM-DD.md`: what changed since last visit, questions to ask, logistics.
- Guardrails: the clinical boundary from PRD §8.7 is adopted **verbatim** as `ops/health/CLAUDE.md` — it is the best-written section of the PRD and is not to be paraphrased. Tracks and reminds; never doses, tapers, interprets, or advises; training programming is explicitly a different risk class.

**`wiki-ops`** *(on demand)*
- Evidence: today's sessions themselves — the ingest/review/commit workflow has now been executed manually three times, which is the definition of a repeated task; the vault schema already names this skill as the intended first build.
- Description: "Run this vault's ingest, lint, or review-commit workflow by the book. Fires on 'ingest this', 'lint the wiki', 'commit the review batch'. Not for ops data refreshes."
- Workflow: encodes CLAUDE.md's Research/Ingest/Lint/Review & Commit steps; bundles `scripts/check-collisions.sh` (the vault-wide basename check) and runs it before creating any page.
- Guardrails: never bypasses `_review/`; never lets a session end with a non-empty `_review/` unsurfaced.

Not built, and why: `sku-verdict` and `content-calendar-refresh` are **scheduled workflows, not skills** — they live as scheduler prompts (§6) because nothing about them is on-demand; a Blossom reporting skill (G7/G8); any fitness skill (G1); any finance skill (cut list); `deep-research` as a separate skill (absorbed into market-research).

---

## 6. Cadence layer

G5 (plan budget) is unanswered; the schedule below is deliberately small enough to fit any paid plan, and ranked so the bottom drops first if budget bites.

**Scheduling mechanism — the constraint the PRD glossed:** scheduled cloud agents cannot reach this local vault; Cowork-style desktop scheduling requires the machine awake — the exact limitation PRD §10 flags. **v2 decision: local scheduling via `launchd`** — jobs fire at their time if the Mac is awake, and coalesce to run at next wake otherwise. A brief generated at 07:40 when the laptop opens is still the brief. Upgrade path (explicitly out of scope until the git remote exists): push the vault to a private remote and move schedules to cloud routines. This is also the standing argument for `git init` in P0.

| # | Job | Type | Schedule | Model intent | Unattended-complete? |
|---|---|---|---|---|---|
| 1 | Shopify sync | **Plain script** (python) | Daily 05:30 ET | none — deterministic | Yes — writes `sync-errors.log` on failure, never partial data |
| 2 | Morning brief | Agent (headless `claude -p`) | Daily 06:30 ET, weekends included (PRD decision #14) | Sonnet-class | Yes — stale-data section replaces any need to ask |
| 3 | SKU verdict pass | Agent | Weekly Sun 07:00 | Opus-class — the one genuinely judgment-heavy schedule | Yes **only after** `product-costs.md` and `pricing-rules.md` are filled; until then it must not run (a verdict without landed cost is fiction) |
| 4 | Content calendar refresh | Agent | Weekly Sun 08:00 | Sonnet-class | Yes — never overwrites slots marked filmed/edited/posted |
| 5 | Sunday review | Agent | Weekly Sun 19:00 | Sonnet-class | Yes — and it's where `tested-tactics` and the kill-criterion instrumentation (§11) get written |

Script-vs-agent ruling per item: #1 is a script because it is pure extraction — an agent would add cost and nondeterminism to a job with zero judgment. Brief archive rotation rides inside #2 (one file mover, not worth a separate job). #3–#5 are agents because verdicts, planning against performance data, and weekly synthesis are judgment. Event-triggered jobs: **none in v2** — at the PRD's own evidenced volume (~7 orders/day), daily polling loses nothing that a webhook would catch, and webhooks add hosting. Long-lived durable schedules: all five. Short-horizon monitoring loops: none exist to justify.

Network scope per unattended job: #1 → the store's admin API host only. #2 → Google Calendar read + local files. #3–#5 → local files only. Anything beyond this list is a spec violation, not a judgment call.

---

## 7. Interface decision

Three candidates: persistent web app; generated dashboard on a schedule; view rendered on demand by conversation.

**Decision: the brief file + conversation-rendered views. No web app. No custom dashboard.**

Against the web app: 8.3 (maintenance hours, forever) and 8.4 (phone vs. laptop) are blank, and a web app is the option most punished by both unknowns — it adds hosting, auth (this vault holds client and health-adjacent data; a hosted surface is a liability decision, 8.6), and a second codebase to a one-operator system whose stated failure mode is abandonment under a semester+drop+training-block collision. The mission-control *intent* mentioned a web-ish OS; the synthesis prompt explicitly forbids defaulting to one on that basis.

Against the scheduled dashboard: it's the brief with extra steps. The brief already *is* a generated artifact on a schedule; rendering it as HTML adds a build and a browser habit without adding information. The PRD only had a dashboard because the Cowork plugin shipped one for free — that subsidy doesn't exist in Claude Code.

For the chosen option: the daily brief is a pushed, zero-habit-change interface (it appears in the vault Josh already opens; Obsidian renders it); anything deeper — "show me SKU performance", "trace this month's content against sales" — is rendered on demand in conversation from `data/` files, which is exactly what an agentic CLI is good at, and can produce a throwaway HTML artifact when a table genuinely needs to be visual. If G6 answers "phone-first," the fix is vault sync + Obsidian mobile (or mailing the brief — a later, gated decision), not a web build.

Standing offer per the synthesis prompt's own rule: if Josh still wants a dashboard after a month of briefs, build the **disposable** version in one evening — static HTML regenerated by job #2 — and instrument it (job #2 appends a one-line open-check question to the Sunday review). Not opened repeatedly within two weeks → deleted, permanently, and the question is settled by data instead of argument.

---

## 8. Build phases

Estimates assume Josh's evidenced level (runs Claude Code well; no `.env`/API integration found on the machine — treat as first integration, 8.7). Honest hours, then +50% per the prompt.

| Phase | Builds | Depends on | Hours (est → padded) | Usable alone as |
|---|---|---|---|---|
| **P0 — rails** | `git init` + `.gitignore` (`.env`, `_review/`); `ops/` partition + contracts written into root `CLAUDE.md`; log-registry extended with ops slugs; connection doc stubs; retire vercel-react; commit the staged meta ingest (this spec + PRD + interview) | Review approval of this spec | 2 → 3 | A versioned vault with the spec of record in it |
| **P1 — commerce rails** | Shopify custom app + token (Josh, ~20 min); `scripts/shopify-sync.py` + launchd job; first real data on disk | P0 | 3 → 4.5 | Daily sales/inventory landing locally |
| **P2 — the brief** | `morning-brief` skill + 06:30 launchd job; context seed sitting with Josh (people/terminology/priorities/tasks) | P1 | 2 → 3 | **The product.** One page every morning |
| **P3 — content loop** | Notion export (Josh) + migration per PRD §8.2 (report included); `intel-intake`; calendar-refresh job | P2 | 3 → 4.5 | Intelligence log queryable; 14-day content plan |
| **P4 — health logistics** | `protocol.md`/`providers.md` sitting with Josh; `refills.json` + `appointments.json` seeded; `appointment-prep`; clinical-boundary `CLAUDE.md` verbatim | P2 | 2 → 3 | Refill/appointment nags in the brief |
| **P5 — verdicts + review** | `product-costs.md` + `pricing-rules.md` sitting with Josh; SKU verdict job; Sunday review job; `tested-tactics` loop | P1, P3 | 2 → 3 | Weekly restock/discount calls with reasons |

Total: ~14 → **21 hours**, sequenced so nothing blocks on a gate: G4 (voice) only gates `script-writer`, which isn't in any phase above — it gets built the week the voice files are filled, not before. `wiki-ops` can be built in any idle hour; it has no dependencies.

**Where the dip lands:** P1. It is pure plumbing — a token, a script, JSON files nobody reads yet — and it will feel like negative progress after the vault-building highs. It is one session. The system starts paying on the first P2 morning, and every phase after P2 compounds a product that already works. Do not mistake P1 for failure; budget it as the toll.

---

## 9. Implementation prompts

Self-contained prompts for a cheaper model, one per phase. Each assumes zero session memory; acceptance criteria are checkable without judgment. (Prompts reference `ops/schemas.md` and PRD §§ by number because both documents live in the vault after P0 — the executing model must read the referenced section before writing, not infer it.)

**P0:**
> In `/Users/joshuanieman/Desktop/Josh Brain`: (1) `git init`; create `.gitignore` containing `.env` and `_review/`. (2) Create `ops/` with `context/`, `briefs/archive/`, `connections/`, and `commerce/`, `content/`, `health/` each containing `inputs/`, `data/`, `outputs/`. Do NOT create `ops/drops/`. (3) Create `ops/schemas.md` by copying §5.5 of `raw/meta/prd-mission-control-v1.md`, re-rooting every path from the PRD's tree to `ops/…`. (4) Append to root `CLAUDE.md` an "Operations layer" section stating: the two-contract partition (wiki = review-gated, ops = inputs/data/outputs with the inputs-rule quoted from PRD §5.3); the ops domain slugs `commerce`, `content`, `health` added to log.md's registered domains; the session contract from `wiki/meta/synthesis/mission-control-spec.md` §3.3 verbatim. (5) Create `ops/context/` files and `ops/tasks.md` as templates whose seed content is fill-in instructions (voice templates use interview §4's questions from `raw/meta/mission-control-interview-v2.md`). (6) First commit, message "P0: ops rails". Acceptance: `git log` shows one commit; `.env` absent from tracking when created; `ls ops` matches (2); root CLAUDE.md names both contracts; no file under `wiki/` or `raw/` modified except via the approved review batch.

**P1:**
> Read `ops/schemas.md` (sales-daily, inventory) and `ops/connections/shopify.md` (Josh will have pasted store domain + token env var name; token itself is in `.env`, never echo it). Write `scripts/shopify-sync.py`: pull yesterday's orders → compute the sales-daily object exactly per schema → append to `ops/commerce/data/sales-daily.json`, skipping if the date exists; pull inventory → overwrite `ops/commerce/data/inventory.json`; on any API error or partial response, append one line to `ops/commerce/data/sync-errors.log` and write nothing else. Then write a launchd plist for daily 05:30 America/New_York with wake-coalescing default behavior, and document load/unload commands in `ops/connections/shopify.md`. Acceptance: a manual run against the live store produces both files validating against the schema; a run with a bad token writes only to `sync-errors.log`; running twice same-day does not duplicate a date; the token string appears in no file except `.env`.

**P2:**
> Build `.agents/skills/morning-brief/SKILL.md` per `wiki/meta/synthesis/mission-control-spec.md` §5.2 (frontmatter description verbatim; five sections in the fixed order of PRD §6.2; stale-data rule word-for-word: any source file missing or >48h old gets a `## Stale data` section naming file and age, and its numbers are not reported as current). Reads: Google Calendar connector (today + 14 days), `ops/commerce/data/*.json`, `ops/health/data/refills.json` and `appointments.json` if present, `ops/content/data/content-calendar.json` if present, `ops/tasks.md`. Writes: `ops/briefs/brief-YYYY-MM-DD.md` only; moves briefs >14 days to `archive/`. Add a launchd job invoking it headless daily 06:30 ET. Acceptance: a manual run with real P1 data produces all five sections; deleting `inventory.json` and re-running produces a Stale data section and no inventory numbers; nothing outside `ops/briefs/` is written.

**P3:**
> Josh has exported Notion to `ops/content/_notion-raw/`. Execute PRD §8.2 exactly (it is a complete prompt: UUID stripping, field mapping table, `cil-` ID assignment, migration report listing every unmappable row and every inferred field). Then build `.agents/skills/intel-intake/SKILL.md` per spec §5.2 including the semantic-dedupe rule from the PRD refresh table (match → increment `cross_source_count`, append creator; no new row). Then add the Sunday 08:00 calendar-refresh launchd job per PRD §8.5, correcting paths to `ops/`. Acceptance: migration report row counts reconcile (rows in = rows out + rows listed); re-running intake on the same transcript adds zero new entries; refresh preserves every slot with status filmed/edited/posted byte-for-byte.

**P4:**
> With Josh present (this phase is mostly his answers): fill `ops/health/inputs/protocol.md` and `providers.md` from what his prescribers actually specified — transcribe, don't improve. Write `ops/health/CLAUDE.md` by copying PRD §8.7 **verbatim — no paraphrase, no additions**. Seed `refills.json` and `appointments.json` per `ops/schemas.md` with real current data. Build `.agents/skills/appointment-prep/SKILL.md` per spec §5.2. Acceptance: `refills.json` has a computable `reorder_on` for every entry; asking the health domain for a dose change produces a refusal plus an offer to add it to appointment prep; the next morning brief's Health section populates.

**P5:**
> With Josh: fill `ops/commerce/inputs/product-costs.md` (landed cost per SKU — the pass must not run while any live SKU lacks one) and `pricing-rules.md` (margin floor, never-discount list). Add the Sunday 07:00 verdict job per PRD §8.4 (paths → `ops/`; every SKU gets exactly one verdict and a 1–2 sentence reason; no price recommendation without margin at old AND new price) and the Sunday 19:00 review job per PRD §6.5 plus one required line: count of brief-driven actions this week (ask Josh in-session when run interactively; mark "unverified" when headless). Acceptance: verdict output has verdict+reason for 100% of SKUs in inventory.json; a SKU missing from product-costs.md aborts the pass with a named error; the review appends to `ops/context/tested-tactics` only entries whose log status is `tested`.

---

## 10. Self-improvement loop

**Failure write-back (per skill, mandatory):** every new skill carries a `## Known failures` section. When a run fails or Josh corrects an output, the fixing session appends one dated line — trigger, wrong behavior, the rule that prevents it — *to the skill file itself*, so the failure cannot recur silently. This is the same mechanism as the vault's contradiction-flagging rule, pointed at skills. (skill-creator's eval loop is available for bigger overhauls; the write-back line is the cheap always-on version.)

**The audit (monthly, first Sunday review of the month, ~15 min):** score each layer and name the weakest —
- *Context:* % of context files whose `last_reviewed` is within their stated cadence.
- *Connections:* days of `sync-errors.log` entries; staleness incidents in briefs.
- *Capabilities:* invocations per skill this month (from `log.md` — this is why ops runs log there); skills with zero invocations for 60 days become retire-candidates, exactly the discipline interview 7.2 demanded of the original eleven.
- *Cadence:* scheduled-run completion rate (briefs that exist ÷ days).
One fix gets scheduled per audit. One — the audit that produces a to-do list produces abandonment.

**Automation-candidate surfacing (same monthly pass):** ask three questions against the month's `log.md` and briefs — what was done manually more than three times; what was copy-pasted between surfaces; what breaks first if volume triples (interview 1.10/1.11/1.14, re-asked against evidence). This is the elegant resolution of the blank interview: **the system's own logs become the task diary Josh didn't keep.** Thirty days of operation answers Section 1 empirically, and the first monthly audit can regenerate the capabilities cut list against real data.

---

## 11. Failure analysis

Three most likely paths to abandonment, each with a design decision already in place:

1. **The brief goes unread — the product fails silently.** A brief nobody opens is indistinguishable from a working system in every log except one. Mitigation: the Sunday review's mandatory brief-driven-actions count (§9 P5) — the number that can't be rationalized. Design supports: briefs stay one page, five sections, max five decisions (PRD's caps, kept); weekends included so trust isn't five-days-a-week (#14); staleness is confessed, never hidden (#15), because one silently-wrong number ends the habit permanently.
2. **Input rot — `product-costs.md`, `protocol.md`, `current-priorities.md` go stale, verdicts and briefs quietly degrade, trust collapses.** Mitigation: the inputs-rule's flip side — jobs that depend on a stale input *say so and stop* rather than computing fiction (verdict pass aborts on a missing cost; the brief banners stale files and escalates any file stale >7 days into "Needs a decision"). Context files carry `last_reviewed`; the monthly audit scores it.
3. **Gate-jumping — building the impressive thing before its gate clears** (Blossom automation before the credential agreement, fitness tracking before provenance, a dashboard before the brief has proven itself). This is the failure the interview's Section 0.6 warns about: building as avoidance. Mitigation: the gates are named G1–G10 *in the committed spec*, and P0 writes the gate list into root `CLAUDE.md` — any future session asked to build a gated item must surface the gate first. The v0 also deliberately requires **zero daily human input** (sync is automatic; metrics are optional; the only recurring human touch is weekly), so the semester+drop+training-block collision week degrades the system to "briefs keep appearing" rather than "the streak broke, why bother."

**Kill criterion (proposed — G10, needs Josh's ratification since 9.4 is blank):** *By October 1, 2026: if the trailing four Sunday reviews record fewer than two brief-driven actions per week on average, shut down the scheduled jobs, keep the vault and on-demand skills, and write the postmortem to `wiki/meta/`.* Instrumentation already specified: the weekly count in the Sunday review (§9 P5) and the monthly audit's cadence score (§10) — both land in files, so the criterion is checkable by grep, not by memory or mood. Note the shutdown target: the *automation* dies, not the knowledge base — the vault has independent value and its own (already met) survival test.

---

## Sources

- [[2026-07-22-prd-mission-control-v1]] — schemas, brief structure, inputs-rule, clinical boundary, decision log (absorbed)
- [[2026-07-22-mission-control-interview-v2]] — the gate questions and the synthesis prompt this document answers
- [[2026-07-22-llm-wiki-pattern]] — the knowledge-layer pattern the ops layer is partitioned against
- [[llm-maintained-wiki]] — same, distilled
- Session evidence, 2026-07-22: vault build and domain decisions; skill inventory recount (13, not 11); connector reality check (Shopify/Calendar live, Ahrefs unauthenticated); Downloads artifacts (Aston Trejo transcripts, Blossom deliverables, Academic Planning workbook, one receipt in Financials)
