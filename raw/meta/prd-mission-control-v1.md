---
type: raw-source
added: 2026-07-22
source_type: upload
---

# PRD — Mission Control

**Owner:** Josh (Belated, LLC)
**Build surface:** Claude Cowork
**Build length:** 8 hours (Block 0 + Blocks 1–8)
**Data layer:** Local plain files at `~/cowork/`, doubling as an Obsidian vault
**Timezone:** America/New_York (US Eastern)
**Version:** 1.0

---

## 1. Executive summary

Mission Control is a single Cowork workspace that holds the recurring decision-making for a one-person clothing brand run alongside university and a health protocol. It sits on Cowork's Productivity plugin, stores everything as plain markdown and JSON in a local folder that is simultaneously an Obsidian vault, and exposes that state through three interaction patterns: an always-on dashboard, scheduled briefs, and on-demand skills.

**The three fully built domains in this window:**

| Domain | Rhythm | What it decides |
|---|---|---|
| `content/` | Daily | What to film, in which voice, using which validated tactic |
| `commerce/` | Daily + weekly | What to restock, discount, kill, or reprice |
| `health/` | Daily + weekly | What protocol step is due, what to log, what to ask a doctor |

**Built if the budget holds (Block 8, first item on the cut list):** `drops/` — the episodic project domain covering manufacturing, tech packs, samples, launch, and postmortem.

**Placeholder folders only:** `studies/` and `finance/`. Studies still contributes to the morning brief via Google Calendar and gets a `deep-research` skill; it just does not get its own data pipeline.

**Why this fits 8 hours.** Block 0 is setup. Block 1 is the data layer plus the Obsidian vault. Block 2 is the Notion migration and the Content Intelligence Log redesign, which is real, unavoidable work and is scheduled explicitly rather than assumed away. Blocks 3–5 build one domain each. Block 6 builds the morning brief, which is the actual product. Block 7 is the dashboard and skills. Block 8 is `drops/`.

**Why it scales.** Every domain is the identical four-folder shape. Adding `finance/` later is: create the folder, write one `CLAUDE.md`, define one schema, add one scheduled task, add one line to the brief prompt. Nothing already built gets touched.

**The system's real job.** The bottleneck for a sole operator running a brand, a degree, and a medical protocol is not missing information. It is the cost of switching between three contexts that share no state. The morning brief is therefore the product; the domains exist to give it accurate facts.

---

## 2. Quick start — moving this into Cowork

### 2.1 Getting into Cowork (Josh does this)

1. Open Claude Desktop and go to the **Cowork** tab.
2. Create a new project and point it at a local folder: `~/cowork/`.
3. Load this PRD into it — either drop `PRD-mission-control.md` into `~/cowork/`, or paste its full contents into the first Cowork message.

Nothing is set up yet at this point. No plugin, no folders, no files. Block 0 handles all of it.

### 2.2 Project instructions (paste this into the Cowork project's custom instructions field)

```
This project is Mission Control, a personal operating system for Josh — founder of
Belated (a DTC clothing LLC), university student, and manager of an ongoing health
protocol. Timezone is America/New_York. Default model is Sonnet unless a task
specifies otherwise.

DATA LAYER
All state lives in plain files under the project root (~/cowork/). This folder is
also an Obsidian vault. Never store system state in a connector. Google Drive,
Gmail, Google Calendar, Notion, Shopify, Slack, HubSpot, Canva, Figma and Ahrefs
are DATA SOURCES you read from or push to. They are never storage.

DOMAINS
Fully built: content/, commerce/, health/
Built last, first to cut: drops/
Placeholder only: studies/, finance/
Each domain has the same shape: CLAUDE.md, inputs/, data/, outputs/

THE INPUTS RULE — CRITICAL
inputs/ is human-maintained. You read from it. You NEVER write to it, overwrite it,
reformat it, or "clean it up." If an input file looks wrong or out of date, say so
and wait. data/ is machine-refreshed and yours to overwrite. outputs/ is yours to
create.

EXECUTION
Build the plan one block at a time, in order. When I say "Start Block N," do that
block only. When it is done, report what was created and the done-check result,
then stop and wait for my go-ahead. Do not run ahead into the next block.

FILE FORMATS
Files a human reads: markdown (.md). Files a workflow parses: JSON (.json). Do not
put machine data in prose and do not put prose in JSON. Obsidian renders the .md
files; the .json files are for workflows.

NEVER AUTOMATED
- No message sends to a customer, manufacturer, or influencer without Josh reading
  it first.
- Nothing posts to either social account automatically.
- The health domain tracks and reminds. It NEVER decides a dose, designs or adjusts
  a medication taper, interprets a symptom, or gives clinical advice. It holds the
  protocol as Josh's doctor defined it and surfaces when something is due.
- No Shopify write operations (price changes, inventory edits, product edits)
  without explicit per-action approval. Read-only by default.
```

### 2.3 How to run the build (instructions to Cowork)

When Josh says to start, **assume nothing is set up.**

1. Run **Block 0 (Setup)** from §7 first. Verify the Productivity plugin is installed and walk him through installing it if not. Have him run `/start`. Verify the required connectors are enabled and name any he must turn on.
2. Only once setup is confirmed, proceed to Block 1.
3. Build one block at a time, in order. After each block, report what was done and the done-check result, then wait.

### 2.4 The first thing Josh says in Cowork

```
Start building Mission Control — begin with Block 0.
```

---

## 3. Goals and non-goals

### Goals

1. One local source of truth for brand, commerce, and health state, readable in Obsidian and writable by Cowork.
2. A daily morning brief that spans all three contexts plus the academic calendar, so no context is silently dropped.
3. Migrate the Notion Content Intelligence Log into a schema that closes the loop — tracks whether an insight was actually tested and what happened — rather than just recording that it was captured.
4. Convert Shopify from a reporting surface into a decision surface: every SKU carries a verdict, not just numbers.
5. Give the health protocol a home that reminds without ever advising.
6. Keep the existing eleven skills usable, now reading from the data layer instead of from nothing.

### Non-goals for this window

| Not built | Why |
|---|---|
| `finance/` as a live domain | At current volume the useful signals (Shopify payouts, manufacturer wires) are already captured in `commerce/` and `drops/`. A separate domain would mostly duplicate them. Revisit after a full year of transactions. |
| `studies/` as a live domain | Google Calendar already holds deadlines and exam windows. Reading it in the brief delivers most of the value for roughly a tenth of the build cost. Coursework itself is served by the `deep-research` skill. |
| The autonomous-builder pattern | A drop-a-brief-get-a-work-product loop needs its own drop zone, spec format, and review gate. That is a block of its own and there is no room. The `deep-research` skill covers the common case. |
| Shopify write operations | Read-only in window one. An agent editing live prices or inventory is a category of mistake that is expensive and public. |
| Automated posting | Deliberate. See the never-automated list. |
| Any medical decision support | Deliberate and permanent, not a scoping decision. |

---

## 4. Architecture overview

### 4.1 Three layers

```
LAYER 3 — WORKFLOWS      Scheduled tasks + on-demand skills. Stateless per run.
                         Read the data layer, write the data layer, never hold state.
        ↑
LAYER 2 — COWORK PROJECT Custom instructions, Productivity plugin, connectors,
                         toolbox/ skills. The execution environment.
        ↑
LAYER 1 — LOCAL FILES    ~/cowork/ — plain .md and .json. Also an Obsidian vault.
                         The only place state exists.
```

Connectors sit outside all three layers. Shopify, Calendar, Gmail, Notion and Drive are pulled from and occasionally pushed to. They never hold system state, because a connector's schema is not yours and can change without warning.

### 4.2 Interaction patterns

| Pattern | Instance | When |
|---|---|---|
| Dashboard | `dashboard.html` | Always on |
| Brief | Morning brief | Daily 06:30 ET |
| Brief | Sunday review (commerce + content + health) | Sunday 19:00 ET |
| Skill | `script-writer`, `intel-intake`, `restock-call`, `appointment-prep`, `deep-research` | On demand |
| Autonomous builder | Not in this window | See §10 |

### 4.3 Three-tier memory

| Tier | File | Holds |
|---|---|---|
| Cross-cutting | `CLAUDE.md` (root) | People, terminology, shorthand, brand facts that apply everywhere |
| Deep, per domain | `memory/{domain}/*.md` | Accumulated domain knowledge — what has been tried, what the constraints are |
| Role, per domain | `{domain}/CLAUDE.md` | Voice and posture when working inside that folder |

The distinction that matters: `memory/content/tested-tactics.md` is what Claude knows about content. `content/CLAUDE.md` is how Claude behaves when working on content. Do not merge them.

### 4.4 Key architectural decisions and the tension behind each

**The vault is the project root, not a subfolder.** Tension: Obsidian prefers a clean vault of only markdown, and the vault will contain `.json` files, `dashboard.html`, and `toolbox/` scripts that render as noise. Resolved in favour of a single root, because two roots means two mental models and eventual drift. Obsidian's "Excluded files" setting hides the noise.

**JSON for machine data, markdown for human data, no overlap.** Tension: Obsidian cannot render JSON, so `sku-performance.json` is invisible in the vault. Resolved by making every JSON file have a markdown counterpart that a workflow generates — the JSON is the truth, the markdown is the view. This costs one extra write per workflow and is worth it.

**`commerce/` is a decision layer, not a reporting layer.** Tension: Shopify already has analytics that are better than anything built here. Rebuilding revenue charts is waste. Resolved by making the only reason `sku-performance.json` exists the `verdict` field — restock, hold, discount, discontinue — which Shopify cannot produce because it does not know landed cost or content performance.

**`drops/` absorbs supply chain.** Tension: manufacturer relationships outlive any single drop, so a `supply-chain/` domain is defensible. Resolved in favour of merging because every supply-chain decision Josh currently makes is triggered by a drop. Splitting later is a folder move, not a re-architecture.

**Health tracks, never advises.** No tension. This is a hard boundary, not a scoping trade-off.

---

## 5. The data layer

### 5.1 Where it lives

Local. `~/cowork/` on the machine running Claude Desktop. Plain `.md` and `.json` files. The Cowork project points at this folder and Obsidian opens the same folder as a vault.

For backup, `~/cowork/` may be placed inside a synced directory (iCloud, Dropbox, Google Drive desktop client) — Cowork still reads and writes local files. Do not use the Google Drive *connector* as storage.

### 5.2 Folder tree

```
~/cowork/                              # Cowork project root AND Obsidian vault root
├── CLAUDE.md                          # plugin: cross-cutting working memory
├── TASKS.md                           # plugin: task list
├── dashboard.html                     # plugin: always-on visual
├── PRD-mission-control.md             # this document, for reference
│
├── memory/                            # plugin: deep memory
│   ├── people.md                      # manufacturers, professors, doctors, creators, contacts
│   ├── terminology.md                 # Belated shorthand, SKU codes, drop codes, medical terms
│   ├── content/
│   │   ├── tested-tactics.md          # what was tried on-platform and what happened
│   │   └── voice-notes.md             # accumulated corrections to the voice profiles
│   ├── commerce/
│   │   ├── pricing-history.md         # every price change and its effect
│   │   └── customer-patterns.md       # observed segment behaviour
│   ├── health/
│   │   └── protocol-history.md        # doctor-stated changes, dated, source-attributed
│   └── drops/
│       └── manufacturer-notes.md      # quality issues, comms patterns, negotiated terms
│
├── toolbox/                           # installable custom skills — source of truth
│   ├── script-writer/SKILL.md
│   ├── intel-intake/SKILL.md
│   ├── restock-call/SKILL.md
│   ├── appointment-prep/SKILL.md
│   └── deep-research/SKILL.md
│
├── briefs/                            # morning-brief output
│   ├── brief-2026-07-22.md            # today's brief
│   └── archive/                       # briefs older than 14 days
│
├── content/                           # DOMAIN — daily content engine
│   ├── CLAUDE.md                      # role: content strategist, dual voice
│   ├── inputs/                        # human-maintained, NEVER auto-written
│   │   ├── voice-personal.md          # personal account voice profile
│   │   ├── voice-brand.md             # brand account voice profile
│   │   ├── hook-bank.md               # curated hooks that have worked
│   │   └── creators.md                # the 10 tracked creators and why each is tracked
│   ├── data/                          # machine-refreshed
│   │   ├── intelligence-log.json      # migrated + redesigned Content Intelligence Log
│   │   ├── content-calendar.json      # rolling 14-day plan
│   │   └── post-performance.json      # observed metrics per posted video
│   └── outputs/
│       ├── scripts/                   # dated script files
│       └── weekly-content-plan-YYYY-MM-DD.md
│
├── commerce/                          # DOMAIN — Shopify decision layer
│   ├── CLAUDE.md                      # role: merchandiser, margin-first
│   ├── inputs/
│   │   ├── product-costs.md           # landed cost per SKU
│   │   └── pricing-rules.md           # margin floors, discount policy, never-discount list
│   ├── data/
│   │   ├── sales-daily.json           # from Shopify connector
│   │   ├── inventory.json             # from Shopify connector
│   │   ├── sku-performance.json       # derived: margin, velocity, verdict
│   │   └── sku-performance.md         # human-readable view of the above
│   └── outputs/
│       └── commerce-weekly-YYYY-MM-DD.md
│
├── health/                            # DOMAIN — protocol tracking, no advice
│   ├── CLAUDE.md                      # role: logistics only, hard clinical boundary
│   ├── inputs/
│   │   ├── protocol.md                # meds, doses, timing — doctor-defined, human-written
│   │   ├── training-plan.md           # current programme
│   │   ├── providers.md               # doctors, pharmacies, portals, phone numbers
│   │   └── recipes/                   # one .md per recipe
│   ├── data/
│   │   ├── metrics.json               # weight, nutrition, training, sleep
│   │   ├── refills.json               # prescription reorder timing
│   │   └── appointments.json          # scheduled AND needs-scheduling
│   └── outputs/
│       ├── appointment-prep-YYYY-MM-DD.md
│       └── weekly-health-review-YYYY-MM-DD.md
│
├── drops/                             # DOMAIN — Block 8, first to cut
│   ├── CLAUDE.md
│   ├── inputs/
│   │   ├── manufacturers.md           # roster, MOQs, lead times, payment terms
│   │   └── drop-brief-{id}.md         # one brief per drop, written by Josh
│   ├── data/
│   │   ├── drops.json                 # pipeline with phase per drop
│   │   └── samples.json               # sample rounds and outstanding corrections
│   └── outputs/
│       ├── launch-plan-{drop-id}.md
│       └── postmortem-{drop-id}.md
│
├── studies/                           # PLACEHOLDER — folder only
│   ├── CLAUDE.md
│   ├── inputs/
│   │   └── syllabi.md                 # seeded, empty
│   ├── data/                          # empty
│   └── outputs/                       # deep-research skill writes here
│
└── finance/                           # PLACEHOLDER — folder only
    ├── CLAUDE.md
    ├── inputs/                        # empty
    ├── data/                          # empty
    └── outputs/                       # empty
```

### 5.3 Inputs vs data

`inputs/` is human-maintained. Josh writes it, Cowork reads it. A refresh task **never** writes to `inputs/`. If a workflow believes an input is stale or wrong, it reports that in its output and stops.

`data/` is machine-refreshed. Cowork owns it. Josh should not hand-edit it, because the next refresh will overwrite him.

`outputs/` is generated. Always safe to delete and regenerate.

### 5.4 Memory files — what goes where

**`memory/people.md`** — one entry per person the system will ever name. Manufacturer contacts (name, factory, timezone, response latency, preferred channel), doctors and pharmacies, the ten tracked creators, professors and TAs, any influencer previously seeded. Format: `### Name` then a short prose block. Not a table; these entries are uneven.

**`memory/terminology.md`** — Belated SKU code structure, drop code structure, internal shorthand, garment and manufacturing terms, and any medical terms that appear in `health/inputs/protocol.md` so a brief can render them correctly.

**`memory/content/tested-tactics.md`** — the loop-closing file. Every insight that reached `status: tested` gets a dated paragraph here: what was tried, on which post, what happened. This is what stops the same failed tactic being re-adopted in six months.

**`memory/commerce/pricing-history.md`** — every price change, dated, with the observed effect on units and margin over the following 30 days.

**`memory/health/protocol-history.md`** — dated log of doctor-stated protocol changes, each attributed to a specific appointment. Append-only. Nothing is ever written here that did not come from a provider.

### 5.5 Schemas

**`content/data/intelligence-log.json`** — the redesigned Content Intelligence Log. Five changes from the Notion original are listed in §9.

```json
{
  "schema_version": 2,
  "last_updated": "2026-07-22",
  "entries": [
    {
      "id": "cil-0142",
      "insight": "Open a drop announcement with date, time and timezone in the first sentence, before any product detail.",
      "category": "marketing-tactic",
      "tier": "act-now",
      "source_creator": "Aston Trejo",
      "source_video": "SS26 Drop Announcement",
      "timestamp": "00:04",
      "date_added": "2026-07-22",
      "cross_source_count": 3,
      "corroborating_creators": ["Dooly", "Eban Corona"],
      "applies_to": ["content", "drops"],
      "status": "tested",
      "outcome": "Used on the 06-14 brand post. Retention at 3s rose from 61% to 68%.",
      "borderline": false
    },
    {
      "id": "cil-0143",
      "insight": "Show landed-cost breakdown on camera to justify price. Works for founder-led accounts only.",
      "category": "customer-psychology",
      "tier": "worth-revisiting",
      "source_creator": "Marshall Crews",
      "source_video": "Why my hoodie costs $120",
      "timestamp": "02:41",
      "date_added": "2026-07-22",
      "cross_source_count": 1,
      "corroborating_creators": [],
      "applies_to": ["content"],
      "status": "new",
      "outcome": null,
      "borderline": false
    }
  ]
}
```

Allowed values — `category`: `product-signal` | `marketing-tactic` | `customer-psychology` | `competitive-intel` | `ops-insight`. `tier`: `act-now` | `worth-revisiting`. `status`: `new` | `queued` | `tested` | `adopted` | `rejected`. `applies_to`: any of `content`, `commerce`, `drops`, `health`.

**`content/data/content-calendar.json`**

```json
{
  "week_of": "2026-07-27",
  "generated": "2026-07-26",
  "slots": [
    {
      "date": "2026-07-27",
      "account": "personal",
      "format": "ditl",
      "concept": "Sample box arrives between lectures",
      "hook_source": "cil-0142",
      "status": "planned",
      "script_path": "content/outputs/scripts/2026-07-27-personal-ditl.md"
    },
    {
      "date": "2026-07-29",
      "account": "brand",
      "format": "garment-breakdown",
      "concept": "Washed tee — fabric weight and wash process",
      "hook_source": null,
      "status": "filmed",
      "script_path": "content/outputs/scripts/2026-07-29-brand-garment.md"
    }
  ]
}
```

`format`: `ditl` | `grwm` | `garment-breakdown` | `drop-announcement` | `pipeline-teaser` | `talking-head`. `status`: `planned` | `filmed` | `edited` | `posted`.

**`content/data/post-performance.json`** — append-only.

```json
{
  "posts": [
    {
      "post_id": "2026-07-14-brand-reels",
      "account": "brand",
      "platform": "reels",
      "posted": "2026-07-14",
      "format": "drop-announcement",
      "hook_type": "in-media-res",
      "views": 18400,
      "saves": 312,
      "shares": 96,
      "profile_visits": 540,
      "link_clicks": 88,
      "retention_3s_pct": 68,
      "linked_drop": "drop-003",
      "linked_insight": "cil-0142"
    }
  ]
}
```

**`commerce/data/sku-performance.json`** — the decision file. Overwritten weekly.

```json
{
  "generated": "2026-07-26",
  "window_days": 30,
  "currency": "USD",
  "skus": [
    {
      "sku": "BLT-TEE-WSH-M",
      "title": "Washed Logo Tee",
      "variant": "M",
      "units_sold": 34,
      "units_on_hand": 11,
      "revenue": 1326.00,
      "landed_cost_unit": 14.20,
      "gross_margin_pct": 63.6,
      "sell_through_pct": 75.6,
      "days_of_cover": 9.7,
      "return_rate_pct": 2.9,
      "verdict": "restock",
      "reason": "Fastest velocity in the line, under 10 days of cover, margin above the 55% floor."
    },
    {
      "sku": "BLT-CAP-BLK-OS",
      "title": "Logo Cap",
      "variant": "OS",
      "units_sold": 3,
      "units_on_hand": 47,
      "revenue": 105.00,
      "landed_cost_unit": 8.90,
      "gross_margin_pct": 74.6,
      "sell_through_pct": 6.0,
      "days_of_cover": 470.0,
      "return_rate_pct": 0.0,
      "verdict": "discount",
      "reason": "Margin is healthy but velocity is dead. Capital is stuck in 47 units. Bundle or discount before the next production run."
    }
  ]
}
```

`verdict`: `restock` | `hold` | `discount` | `discontinue`. `reason` is required and must be one or two sentences — a verdict without a reason is not actionable.

**`commerce/data/sales-daily.json`** — append-only, one object per day.

```json
{
  "days": [
    {
      "date": "2026-07-21",
      "orders": 7,
      "units": 11,
      "gross_revenue": 428.00,
      "discounts": 32.00,
      "refunds": 0.00,
      "net_revenue": 396.00,
      "aov": 56.57,
      "new_customers": 5,
      "returning_customers": 2,
      "top_sku": "BLT-TEE-WSH-M"
    }
  ]
}
```

**`commerce/data/inventory.json`** — overwritten daily.

```json
{
  "synced": "2026-07-22T05:30:00-04:00",
  "items": [
    { "sku": "BLT-TEE-WSH-M", "on_hand": 11, "committed": 2, "available": 9, "location": "3PL-VA" },
    { "sku": "BLT-CAP-BLK-OS", "on_hand": 47, "committed": 0, "available": 47, "location": "3PL-VA" }
  ]
}
```

**`health/data/refills.json`** — overwritten when a fill occurs; `reorder_on` is what the brief reads.

```json
{
  "last_reviewed": "2026-07-22",
  "medications": [
    {
      "name": "Linzess",
      "dose": "145 mcg",
      "schedule": "Once daily, at least 30 minutes before the first meal",
      "prescriber": "Dr. [name] — GI",
      "pharmacy": "[pharmacy name and number]",
      "last_filled": "2026-07-02",
      "days_supply": 30,
      "refills_remaining": 2,
      "reorder_on": "2026-07-25",
      "notes": "Doctor-defined. This file records the protocol; it does not set it."
    }
  ]
}
```

**`health/data/appointments.json`** — the `needs-scheduling` status is what lets the brief nag.

```json
{
  "appointments": [
    {
      "id": "appt-011",
      "provider": "GI — Dr. [name]",
      "purpose": "Linzess follow-up",
      "datetime": "2026-08-14T10:30:00-04:00",
      "status": "scheduled",
      "on_calendar": true,
      "prep_doc": "health/outputs/appointment-prep-2026-08-14.md"
    },
    {
      "id": "appt-012",
      "provider": "Dentist",
      "purpose": "6-month cleaning",
      "datetime": null,
      "status": "needs-scheduling",
      "due_by": "2026-09-30",
      "on_calendar": false,
      "prep_doc": null
    }
  ]
}
```

`status`: `scheduled` | `needs-scheduling` | `completed` | `cancelled`.

**`health/data/metrics.json`** — append-only, one entry per day.

```json
{
  "entries": [
    {
      "date": "2026-07-21",
      "weight_lb": 172.4,
      "calories": 2740,
      "protein_g": 168,
      "training": "push",
      "sleep_hr": 7.1,
      "notes": ""
    }
  ]
}
```

**`drops/data/drops.json`** — Block 8.

```json
{
  "drops": [
    {
      "id": "drop-004",
      "name": "Fall 26 Capsule",
      "phase": "sampling",
      "launch_date": "2026-10-03",
      "skus": ["BLT-HOOD-CRM", "BLT-PANT-BLK"],
      "manufacturer": "[factory name]",
      "po_total_usd": 4800,
      "deposit_paid": true,
      "balance_due_date": "2026-09-05",
      "sample_round": 2,
      "blockers": ["Round 2 hood drawcord spec unconfirmed"]
    }
  ]
}
```

`phase`: `concept` | `tech-pack` | `sampling` | `production` | `pre-launch` | `live` | `postmortem`.

### 5.6 Refresh strategy

| File | Populated by | Cadence | Write mode | Dedupe |
|---|---|---|---|---|
| `commerce/data/sales-daily.json` | Shopify sync task | Daily 05:30 | Append | Skip if `date` already present |
| `commerce/data/inventory.json` | Shopify sync task | Daily 05:30 | Overwrite | n/a |
| `commerce/data/sku-performance.json` | SKU verdict pass | Weekly Sun 07:00 | Overwrite | n/a |
| `commerce/data/sku-performance.md` | SKU verdict pass | Weekly Sun 07:00 | Overwrite | n/a |
| `content/data/intelligence-log.json` | `intel-intake` skill | On demand | Append | Compare `insight` semantically against existing entries; if a match exists, increment `cross_source_count` and add to `corroborating_creators` instead of adding a row |
| `content/data/content-calendar.json` | Calendar refresh task | Weekly Sun 08:00 | Overwrite forward-dated slots only; never overwrite a slot with status `filmed`, `edited` or `posted` | n/a |
| `content/data/post-performance.json` | Josh, via `intel-intake` or manually | Ad hoc | Append | Skip if `post_id` present |
| `health/data/metrics.json` | Josh, conversationally | Daily | Append | Overwrite the entry if `date` already present |
| `health/data/refills.json` | Josh, on each fill | Ad hoc | Overwrite the affected medication object | n/a |
| `health/data/appointments.json` | Josh + Calendar sync | Ad hoc | Merge by `id` | Match on `id` |
| `drops/data/drops.json` | Josh + drop workflows | Ad hoc | Merge by `id` | Match on `id` |

### 5.7 Naming conventions

Folders kebab-case. Memory files `noun.md`. Data files `noun.json`. Date-stamped files `name-YYYY-MM-DD.md`. Drop IDs `drop-NNN`. Intelligence entries `cil-NNNN`. Appointments `appt-NNN`.

---

## 6. Component specifications

### 6.1 Shopify sync (scheduled)

| | |
|---|---|
| Purpose | Pull yesterday's orders and current inventory into the local layer |
| Reads | Shopify connector |
| Writes | `commerce/data/sales-daily.json` (append), `commerce/data/inventory.json` (overwrite) |
| Schedule | Daily 05:30 ET |
| Model | Haiku — structured extraction, no reasoning |
| Output | Silent. Failures are logged into the next morning brief |

### 6.2 Morning brief (scheduled) — the core product

| | |
|---|---|
| Purpose | One page spanning brand, commerce, health and academics before the day starts |
| Reads | `TASKS.md`, Google Calendar, `commerce/data/*.json`, `content/data/content-calendar.json`, `health/data/refills.json`, `health/data/appointments.json`, `drops/data/drops.json` if present |
| Writes | `briefs/brief-YYYY-MM-DD.md`; moves briefs older than 14 days to `briefs/archive/` |
| Schedule | Daily 06:30 ET, every day including weekends |
| Model | Sonnet |

Output structure, in this fixed order:

```
# Brief — Tuesday 22 July 2026

## Today
[Calendar events, in time order, with class/deadline items marked]

## Needs a decision
[Anything with a deadline inside 72 hours, or a SKU verdict that changed]

## Belated
[Yesterday's orders and net revenue, one line. Any SKU under 14 days of cover.
 Today's content slot and whether a script exists.]

## Health
[Anything due today. Refills where reorder_on <= today. Appointments in the next
 14 days. Any appointment with status needs-scheduling past 50% of its due_by
 window.]

## Open loops
[Unchecked items from TASKS.md older than 5 days]
```

Hard rule: if a data file is missing or stale by more than 48 hours, say so under a `## Stale data` heading rather than silently reporting old numbers.

### 6.3 SKU verdict pass (scheduled)

| | |
|---|---|
| Purpose | Turn Shopify numbers into a restock/hold/discount/discontinue call per SKU |
| Reads | `commerce/data/sales-daily.json`, `commerce/data/inventory.json`, `commerce/inputs/product-costs.md`, `commerce/inputs/pricing-rules.md`, `memory/commerce/pricing-history.md` |
| Writes | `commerce/data/sku-performance.json`, `commerce/data/sku-performance.md`, `commerce/outputs/commerce-weekly-YYYY-MM-DD.md` |
| Schedule | Weekly, Sunday 07:00 ET |
| Model | Opus — this is the judgement-heavy workflow |

### 6.4 Content calendar refresh (scheduled)

| | |
|---|---|
| Purpose | Plan the next 14 days of content against validated insights and commerce signals |
| Reads | `content/data/intelligence-log.json`, `content/data/post-performance.json`, `content/inputs/*`, `commerce/data/sku-performance.json`, `drops/data/drops.json` if present |
| Writes | `content/data/content-calendar.json`, `content/outputs/weekly-content-plan-YYYY-MM-DD.md` |
| Schedule | Weekly, Sunday 08:00 ET |
| Model | Sonnet |

### 6.5 Sunday review (scheduled)

| | |
|---|---|
| Purpose | The weekly read: what moved, what did not, what to change |
| Reads | The week's `briefs/`, `commerce/outputs/`, `content/data/post-performance.json`, `health/data/metrics.json` |
| Writes | `health/outputs/weekly-health-review-YYYY-MM-DD.md` and appends to `memory/content/tested-tactics.md` |
| Schedule | Weekly, Sunday 19:00 ET |
| Model | Sonnet |

### 6.6 Skills (on demand, in `toolbox/`)

| Skill | Purpose | Reads | Writes | Model |
|---|---|---|---|---|
| `script-writer` | Generate a short-form script for either account | `content/inputs/voice-*.md`, `hook-bank.md`, `intelligence-log.json`, `content-calendar.json` | `content/outputs/scripts/` | Sonnet |
| `intel-intake` | Turn a transcript into log entries | A pasted or linked transcript, `intelligence-log.json` | `intelligence-log.json` | Sonnet |
| `restock-call` | Answer "should I reorder X" on the spot | `sku-performance.json`, `inventory.json`, `product-costs.md`, `drops.json` | Nothing — answers in chat | Sonnet |
| `appointment-prep` | Build the question list for an upcoming appointment | `health/inputs/protocol.md`, `metrics.json`, `memory/health/protocol-history.md` | `health/outputs/appointment-prep-YYYY-MM-DD.md` | Sonnet |
| `deep-research` | Multi-source research on any topic, business or academic | Web, connectors, relevant domain `inputs/` | `{domain}/outputs/research-{slug}-YYYY-MM-DD.md` | Opus |

---

## 7. The build plan

| Block | What gets built | Who runs it | Output | Done when… |
|---|---|---|---|---|
| **0** | **Setup.** Confirm Productivity plugin installed (Cowork → Customize → Plugins → "Productivity"); run `/start`; confirm connectors: Shopify, Google Calendar, Gmail, Google Drive, Notion. Name any that are off. | Josh, Cowork verifying | `CLAUDE.md`, `TASKS.md`, `memory/`, `dashboard.html` at root | All four plugin files exist and all five connectors respond to a test call |
| **1** | **Data layer.** Full folder tree per §5.2. All `inputs/` files created with seed content. All `CLAUDE.md` domain files written. Obsidian opened on `~/cowork/` with `.json`, `toolbox/` and `dashboard.html` added to Excluded Files. | Cowork (Josh opens Obsidian) | The tree | `ls ~/cowork` matches §5.2 exactly; Obsidian shows the vault with only `.md` visible |
| **2** | **Notion migration + log redesign.** Josh exports Notion to Markdown & CSV beforehand. Cowork strips UUID suffixes, maps old Content Intelligence Log rows to schema v2, backfills `applies_to` and `status`, flags rows it cannot map. | Cowork (Josh does the export) | `content/data/intelligence-log.json`, `content/outputs/migration-report.md` | Every old row is either migrated or listed in the migration report with a reason |
| **3** | **Content domain.** Calendar refresh task, `script-writer` and `intel-intake` skills, `memory/content/` seeded. | Cowork | 1 scheduled task, 2 skills | Calendar refresh runs manually and produces a valid 14-day `content-calendar.json` |
| **4** | **Commerce domain.** Shopify sync task, SKU verdict pass, `restock-call` skill. `product-costs.md` filled in with Josh. | Cowork (Josh supplies costs) | 2 scheduled tasks, 1 skill | Sync pulls real Shopify data; verdict pass emits a `verdict` and `reason` for every SKU |
| **5** | **Health domain.** `protocol.md` and `providers.md` filled in with Josh, `refills.json` and `appointments.json` seeded, `appointment-prep` skill. Clinical boundary written into `health/CLAUDE.md`. | Cowork (Josh supplies protocol) | 1 skill, 3 seeded data files | `refills.json` has a correct `reorder_on`; asking the health domain for dosing advice produces a refusal |
| **6** | **Morning brief.** The daily 06:30 scheduled task per §6.2, plus archive rotation. | Cowork | `briefs/brief-YYYY-MM-DD.md` | A manual run produces all five sections with real data from all three domains |
| **7** | **Dashboard, Sunday review, `deep-research`.** Customise `dashboard.html` to show today's brief, SKU verdicts, content slots, and health due-items. | Cowork | Updated `dashboard.html`, 1 scheduled task, 1 skill | Dashboard opens in a browser and reflects live file contents |
| **8** | **Drops domain.** Full domain build: `manufacturers.md`, `drops.json`, `samples.json`, launch-plan and postmortem workflows, wired to the existing five drop skills. | Cowork | 1 domain | `drops.json` holds the current drop with a correct `phase`, and it appears in the morning brief |

### Cut order (drop these first, in this order)

1. Block 8 entirely — `drops/` stays a placeholder folder.
2. Block 7 dashboard customisation — keep the plugin default, keep the Sunday review and `deep-research`.
3. Block 2 migration depth — migrate only the Content Intelligence Log; leave the rest of the Notion export sitting in `~/cowork/_notion-raw/` for later.
4. Block 5 health outputs — keep `refills.json` and `appointments.json` feeding the brief, drop `appointment-prep` and the weekly review.
5. Block 3 `intel-intake` — do transcript intake manually until window two.

### Never cut

Block 0 (setup), Block 1 (the data layer), Block 6 (the morning brief). Without all three there is no system, only folders.

---

## 8. Setup details and copy-paste prompts

### 8.1 Folder creation (Block 1)

```
Create the full folder tree from §5.2 of PRD-mission-control.md under the project
root. For every folder, create it even if it will be empty (studies/ and finance/
included). For every inputs/ file listed, create it with a seed template that
explains what belongs in it and includes one worked example. Leave data/ and
outputs/ empty. Write a CLAUDE.md in each of content/, commerce/, health/, drops/,
studies/ and finance/ describing the role and tone for work inside that folder.

Then print the tree you created so I can compare it to the PRD.

CRITICAL: do not create any folders in Google Drive, Notion, or any other
connector. Everything is local.
```

### 8.2 Notion migration (Block 2)

```
I have exported my Notion workspace to Markdown & CSV. The export is at
~/cowork/_notion-raw/.

1. Strip the 32-character UUID suffixes from every filename and folder name in the
   export.
2. Find the Content Intelligence Log CSV. Map every row to schema v2 in §5.5 of
   PRD-mission-control.md:
   - Name -> insight (strip any "[Borderline]" prefix and set borderline: true)
   - Category -> category (map to the five kebab-case values)
   - Tier -> tier
   - Source Creator / Source Video / Timestamp / Date Added -> same fields
   - Cross-Source Signal (checkbox) -> cross_source_count: 2 if checked, 1 if not.
     Flag every converted row in the migration report — the old boolean cannot tell
     us the real count.
   - Actioned (checkbox) -> status: "adopted" if checked, "new" if not
   - applies_to -> infer from category, default ["content"]
   - outcome -> null for every migrated row
3. Assign sequential IDs cil-0001 upward, ordered by date_added.
4. Write the result to content/data/intelligence-log.json.
5. Write content/outputs/migration-report.md listing: total rows in, total rows
   out, every row that could not be mapped and why, and every field that was
   inferred rather than migrated.

Do not delete ~/cowork/_notion-raw/. Do not write anything to inputs/.
```

### 8.3 Shopify sync task (Block 4)

```
Every day at 05:30 America/New_York, using Haiku:

1. Pull yesterday's orders from Shopify. Compute: order count, unit count, gross
   revenue, discounts, refunds, net revenue, AOV, new vs returning customer counts,
   and the top SKU by units.
2. Append one object for that date to commerce/data/sales-daily.json, matching the
   schema in §5.5. If an object for that date already exists, skip it — do not
   duplicate.
3. Pull current inventory levels for every SKU and overwrite
   commerce/data/inventory.json.
4. If Shopify returns an error or partial data, write a line to
   commerce/data/sync-errors.log with the timestamp and error, and do not write
   partial data into either file.

READ-ONLY: never create, update, or delete anything in Shopify. No price changes,
no inventory edits, no product edits.
CRITICAL: never write to commerce/inputs/.
```

### 8.4 SKU verdict pass (Block 4)

```
Every Sunday at 07:00 America/New_York, using Opus:

Read:
- commerce/data/sales-daily.json (last 30 days)
- commerce/data/inventory.json
- commerce/inputs/product-costs.md (landed cost per SKU — human-maintained)
- commerce/inputs/pricing-rules.md (margin floors, discount policy, never-discount
  list)
- memory/commerce/pricing-history.md
- content/data/post-performance.json (has any SKU been pushed in content recently?)

For each SKU compute units_sold, units_on_hand, revenue, gross_margin_pct,
sell_through_pct, days_of_cover and return_rate_pct per the schema in §5.5.

Then assign exactly one verdict per SKU:
- restock — velocity is healthy, days_of_cover is under 30, margin clears the floor
  in pricing-rules.md
- hold — performing acceptably, no action needed
- discount — margin is fine but velocity is dead and capital is stuck. Check
  pricing-rules.md never-discount list first.
- discontinue — velocity is dead AND margin is below the floor, or return rate is
  above 15%

Every verdict needs a one-or-two-sentence `reason`. A verdict without a reason is
not acceptable output.

Write commerce/data/sku-performance.json, then write a human-readable markdown view
of the same data to commerce/data/sku-performance.md, then write
commerce/outputs/commerce-weekly-YYYY-MM-DD.md covering: the week's numbers, every
verdict that CHANGED since last week and why, and the single most important
commerce decision facing me this week.

Do not recommend a price change without stating the margin at both the old and new
price.
CRITICAL: never write to commerce/inputs/.
```

### 8.5 Content calendar refresh (Block 3)

```
Every Sunday at 08:00 America/New_York, using Sonnet:

Read:
- content/data/intelligence-log.json — prioritise entries with tier "act-now" and
  cross_source_count >= 2 and status "new" or "queued"
- content/data/post-performance.json — which formats and hook types actually
  performed for me, not in general
- content/inputs/voice-personal.md and voice-brand.md
- content/inputs/hook-bank.md
- commerce/data/sku-performance.json — any SKU with verdict "restock" is worth
  content; any with verdict "discount" needs content to move it
- drops/data/drops.json if it exists — a drop in phase "pre-launch" outranks
  everything else

Plan the next 14 days. Target 4 slots per week on the personal account and 3 on the
brand account, adjusting if post-performance shows a different cadence working.
Each slot needs: date, account, format, a specific concept (not a topic — a
concept), and hook_source pointing at a cil- ID where one applies.

Write content/data/content-calendar.json per the §5.5 schema. NEVER overwrite a
slot whose status is filmed, edited or posted — preserve those exactly and only
write forward-dated planned slots.

Then write content/outputs/weekly-content-plan-YYYY-MM-DD.md: the slots as a table,
plus a short note on why this week's mix looks the way it does.

CRITICAL: never write to content/inputs/. If hook-bank.md or the voice profiles
look stale, say so in the weekly plan and leave them alone.
```

### 8.6 Morning brief (Block 6)

```
Every day at 06:30 America/New_York, including weekends, using Sonnet:

Read:
- TASKS.md
- Google Calendar for today and the next 14 days
- commerce/data/sales-daily.json and sku-performance.json
- content/data/content-calendar.json
- health/data/refills.json and appointments.json
- drops/data/drops.json if it exists

Write briefs/brief-YYYY-MM-DD.md with exactly these sections in this order:

## Today
Calendar events in time order. Mark class sessions and academic deadlines
distinctly from Belated commitments.

## Needs a decision
Anything with a deadline inside 72 hours. Any SKU verdict that changed since the
last brief. Any drop blocker. Maximum five items — if there are more, pick the five
that cost the most if missed.

## Belated
Yesterday's orders and net revenue in one line. Any SKU under 14 days of cover.
Today's content slot and whether the script already exists at its script_path.

## Health
Any medication where reorder_on <= today. Any appointment in the next 14 days. Any
appointment with status "needs-scheduling" that is more than halfway to its due_by
date. State facts and dates only.

## Open loops
Unchecked TASKS.md items older than 5 days.

If any data file is missing, or its most recent entry is more than 48 hours old,
add a "## Stale data" section naming the file and its age. Never report stale
numbers as if they were current.

Move any brief in briefs/ older than 14 days into briefs/archive/.

CRITICAL: this is a read-and-summarise task. Never write to any inputs/ folder and
never modify any data/ file. Give no medical advice of any kind — report protocol
dates and appointment logistics only.
```

### 8.7 `health/CLAUDE.md` (Block 5) — write this file verbatim

```
# Health domain — role

You handle logistics for a health protocol. You are not a clinician and you do not
act like one.

WHAT YOU DO
- Track weight, nutrition, training and sleep in data/metrics.json
- Track when a prescription needs reordering, based on dates in data/refills.json
- Track scheduled appointments and flag ones that need scheduling
- Build question lists for upcoming appointments from logged data
- Surface recipes from inputs/recipes/

WHAT YOU NEVER DO
- Recommend, adjust, or design a medication dose or taper schedule. Not even if
  asked directly. Not even with a disclaimer. Tapering off a medication is a
  decision made with the prescriber, and this system's only role is to record what
  the prescriber decided.
- Interpret a symptom or suggest what a symptom means
- Recommend stopping, starting, or changing any medication
- Suggest a supplement, a diagnosis, or a treatment
- Set a calorie or weight target

If asked to do any of the above, say plainly that this is a prescriber decision,
and offer instead to add the question to the next appointment prep doc.

inputs/protocol.md is the record of what the doctor decided. You read it. You never
write to it or amend it. Only Josh writes that file, and only after an appointment.

TRAINING is different from MEDICATION. You may discuss programming, progression,
and exercise selection in inputs/training-plan.md normally. The restriction above
covers medication, symptoms, and clinical judgement only.
```

### 8.8 `deep-research` skill (Block 7)

```
Create toolbox/deep-research/SKILL.md.

Trigger: Josh asks for research on any topic — competitor analysis, a manufacturing
process, a course concept, a market question.

Behaviour:
1. Ask one clarifying question only if the scope is genuinely ambiguous. Otherwise
   proceed.
2. Determine the domain: content, commerce, drops, health or studies. State which
   one before starting.
3. Read the relevant domain's inputs/ for context before searching.
4. Research using web search and any relevant connector.
5. Write {domain}/outputs/research-{slug}-YYYY-MM-DD.md containing: the question, a
   direct answer up front, the supporting findings, what the evidence does NOT
   support, and the sources.
6. Close with a self-critique section: what is weakest in this research and what
   would change the conclusion.

Pin this skill to Opus in the scheduled-task or skill model selector.

CRITICAL: never write to any inputs/ folder. For health-domain research, report
what published sources say and never convert it into a personal recommendation.
```

---

## 9. Decision log

| # | Decision | Reasoning / trade-off |
|---|---|---|
| 1 | Three domains fully built, `drops/` fourth and cuttable, two placeholders | Eight hours supports 2–3 domains well. Content, commerce and health have daily or weekly rhythms with no current home. Drops is episodic and already served by five standalone skills, so it loses least by waiting. |
| 2 | Vault root = project root, not `~/cowork/vault/` | Two roots means two mental models and eventual drift. Cost: Obsidian sees `.json` and `toolbox/` as noise. Mitigated by Obsidian's Excluded Files setting. |
| 3 | JSON for machine data, markdown for human data, plus a generated `.md` view of key JSON | Obsidian cannot render JSON, so a JSON-only commerce layer would be invisible in the vault Josh actually reads. One extra write per workflow buys visibility. |
| 4 | `cross_source_count` (integer) replaces the Notion `Cross-Source Signal` checkbox | A boolean tells you a signal repeated. An integer tells you how strong it is, which is the thing that decides whether to act. Migration cost: old checked rows become `2` and are flagged as imprecise. |
| 5 | `status` (5 states) replaces the `Actioned` checkbox | `Actioned` cannot distinguish "tried and it worked" from "tried and it failed," so failed tactics get re-adopted months later. The `rejected` state is the point of this change. |
| 6 | Added `applies_to` and `outcome` to the intelligence log | `applies_to` routes an insight to the domain that consumes it, so the content calendar and the commerce pass can both read the same log. `outcome` closes the loop back into `memory/content/tested-tactics.md`. |
| 7 | `commerce/` is a decision layer, not a reporting layer | Shopify's own analytics beat anything rebuilt here. The only defensible reason to duplicate the data locally is to add landed cost and content performance, which Shopify does not have, and emit a `verdict`. If the verdict field were removed, this domain should be deleted. |
| 8 | `drops/` absorbs supply chain rather than a separate `supply-chain/` domain | Every supply-chain decision is currently triggered by a drop, so shared state is the whole value. Trade-off: manufacturer relationships outlive drops, so if factory count grows past three or four, split it out. That is a folder move, not a re-architecture. |
| 9 | Studies gets calendar integration and a research skill, not a domain | Academic deadlines live in Calendar already. Building a `studies/` pipeline would mostly re-enter data that exists. The genuine need — occasional deep research — is a skill, not a domain. |
| 10 | Health tracks and reminds, never advises | Not a scoping trade-off. An LLM producing a medication taper schedule is a serious harm risk regardless of how well it is prompted. Training programming is explicitly carved out as a different risk class. |
| 11 | Shopify read-only in window one | An agent with write access to live prices and inventory makes mistakes that are public and expensive. Write access can be added per-operation later once the read path is trusted. |
| 12 | Notion migration is its own block (Block 2) rather than folded into Block 1 | Notion's Markdown & CSV export mangles filenames, flattens nested databases and drops relations. Pretending it is a 10-minute job is how an 8-hour build becomes a 12-hour build. |
| 13 | Model routing specified per workflow as intent, not enforced config | Cowork's scheduled-task form does expose a model selector, but there is a reported bug where desktop scheduled tasks run on Sonnet regardless. Specifying intent costs nothing and pays off when the bug is fixed. |
| 14 | Morning brief runs weekends too | The health protocol and the content calendar do not observe weekends, and a brief you only trust five days a week is a brief you stop reading. |
| 15 | The brief refuses to report stale data silently | A brief that shows Tuesday's inventory on Friday without saying so is worse than no brief, because decisions get made on it. |

---

## 10. Out of scope / future work

### Deferred domains (placeholder folders exist in the tree)

**`finance/`** — LLC expense categorisation for tax, drop-level P&L, quarterly set-aside, runway. Blocked on volume rather than on architecture: the domain becomes useful once there is a year of transactions to categorise and manufacturer wire volume is high enough that payment timing matters. Build as: one `inputs/chart-of-accounts.md`, one `data/transactions.json`, one monthly scheduled task. Roughly one block.

**`studies/`** — syllabus parsing, assignment tracking, reading-list management, exam preparation. Currently served indirectly by the Calendar integration in the brief and by `deep-research`. Build when a term arrives that has enough structured coursework to justify it.

**`drops/`** — if Block 8 is cut, this is the first thing built in window two, and it is roughly a full block on its own.

### Patterns not built

**Autonomous builder.** Drop a brief file into `builds/`, get a finished work product back. This would need a `builds/` drop zone at root, a brief format spec, a review gate, and a scheduled task that watches the folder. Roughly two blocks. It is the highest-value future addition once the data layer is proven, because it is what turns the system from a dashboard into a coworker.

**Shopify write operations.** Price updates, inventory adjustments and product edits, each gated behind explicit approval. Add after the read path has run clean for a month.

**Cross-domain correlation.** The interesting question — does content activity actually move commerce numbers — needs several months of `post-performance.json` and `sales-daily.json` before it can be answered. The schemas already carry the join keys (`linked_drop`, `linked_insight`, `top_sku`), so nothing needs restructuring; it just needs data.

### How this scales without restructuring

Adding a domain is five steps: create `{domain}/` with the four-folder pattern, write `{domain}/CLAUDE.md`, create `memory/{domain}/`, define the schemas for its `data/` files, add one line to the morning brief prompt. Nothing already built is modified.

### What would force a re-architecture

- Multiple people needing write access. The entire design assumes one operator and one machine, with no locking and no conflict resolution.
- Data volume outgrowing flat files. Roughly 5,000+ intelligence-log entries or 3+ years of daily sales would make full-file reads slow enough to matter, at which point `data/` moves to SQLite and the `.md` views become the only readable surface.
- A move off Cowork to a hosted runtime. Cowork's scheduled tasks require the desktop app to be running; if tasks need to fire with the laptop closed and remote sessions do not cover it, the scheduling layer moves to Claude Code and the local data layer moves to a repository.

---

## Assumptions flagged for correction

These were set as defaults because they could not be inferred. Correct any of them before Block 0.

1. No existing Obsidian vault. The build creates `~/cowork/` and Obsidian is pointed at it. If a vault already exists, say where, and the tree is created inside it instead.
2. Morning brief at 06:30 ET, seven days a week.
3. The never-automated list in §2.2 is accurate and complete.
4. Josh has admin access to the Shopify store, so the connector can read orders, inventory, products and customers.
5. `commerce/inputs/product-costs.md` will be filled in during Block 4. Without landed cost per SKU, the verdict pass cannot compute margin and the commerce domain does not work.
6. `health/inputs/protocol.md` will be filled in during Block 5, transcribed from what the prescriber actually specified.
