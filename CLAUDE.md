# Josh Brain

This vault is a personal knowledge base maintained by Claude, following the "LLM Wiki" pattern: raw sources stay untouched, Claude reads them and builds/maintains an interlinked markdown wiki that compounds over time instead of being re-derived from scratch on every question.

It's structured in **domains** (business, schoolwork, fitness, health, habits, finances, media, plus `meta` for the wiki's own documentation) so it can grow into the knowledge substrate for a future "mission control OS" without a rewrite — see the Domains table below.

Pattern rationale in full: `raw/meta/llm-wiki-pattern.md`, distilled into [[llm-maintained-wiki]].

**This file is the schema.** It governs every session in this vault. If we agree on a new convention, update this file in the same session — don't let it drift out of sync with what we actually do.

## Architecture

Three layers, plus one transient one:

1. **`raw/`** — immutable, curated source documents (articles, papers, notes, transcripts, images). Claude reads these but **never** edits them. Source of truth.
2. **`wiki/`** — LLM-owned markdown pages: source summaries, entity pages, concept pages, synthesis. Claude creates and maintains all of it.
3. **This file** — the schema layer.
4. **`_review/`** — transient staging area. Everything Claude drafts (whether from a source Josh handed over, something found via research, or a video/article capture) lands here first and only moves into `raw/`/`wiki/` after Josh reviews it. See **Review & Commit** below — this is the mechanism behind the "every session ends with review" rule.

## Domains

The top-level split, in both `raw/` and `wiki/`. A domain is a life area Josh explicitly names — never one Claude infers from an offhand mention (see "How this grows" below).

| Domain | Purpose | Sensitivity |
|---|---|---|
| `business` | Ventures as entity pages: Belated, Seaggs, Manu, others as they show up | normal |
| `schoolwork` | Coursework, assignments, deadlines, notes | normal |
| `fitness` | Training, programs, progress | normal |
| `health` | Medical, wellness, mental health | **high — redact specifics** |
| `habits` | Recurring personal habits and tracking | normal |
| `finances` | Savings, budgeting, investing, subscriptions, bills, personal-vs-business sorting | **high — redact specifics** |
| `media` | Content/media projects (e.g. Blossom Medical / MD-Esti) | normal |
| `meta` | The wiki's own design/pattern docs — infrastructure, not a life domain | normal |

**Sub-domains are tags, not folders.** A page can carry `tags: [budgeting, business]` — freely multi-valued, used both for within-domain grouping and for flagging cross-domain relevance (tagging `business` onto a page that primarily lives under `finances`, say). No filesystem change is ever needed to "add" a sub-domain — it's just a tag someone starts using; `index.md`'s per-domain lists group by it once a domain's list gets crowded. `finances` already has starter vocabulary from how Josh described it: `savings, budgeting, investing, subscriptions, bills, personal, business`. Nothing is pre-seeded for the other domains — their first tags emerge from their first real ingest.

## Sensitive data

`finances` and `health` are marked high-sensitivity above. **Never write a full account number, routing number, SSN, card number, or similarly sensitive identifier into anything Claude authors** — wiki/ pages, or raw/ sources Claude creates from scratch (transcripts, notes, typed-up summaries). Redact to the last 4 digits or a category label instead (e.g. "Chase checking …1234", not the full number).

This does **not** apply to literal source documents Josh provides directly (a PDF statement, an exported CSV) — those stay in `raw/` as faithful, unmodified copies, per the immutability rule. The redaction rule is about what Claude writes, not what it stores verbatim.

## Directory structure

```
raw/
  business/  schoolwork/  fitness/  health/  habits/  finances/  media/  meta/
    (each domain: immutable curated sources — keep original filenames, or slugify a title if there isn't one)
wiki/
  <domain>/
    sources/            one page per ingested source — dated filenames
    entities/           people, organizations, products — "who/what" pages
    concepts/           ideas, themes, methods — "what is X" pages, evolve in place
    synthesis/          overviews, comparisons, theses that span many sources/concepts
  (repeated identically for all 8 domains)
_review/              staging area — drafts awaiting review, mirrors raw/<domain>/ + wiki/<domain>/..., empty between sessions
ops/                  OPERATIONS layer — NOT review-gated; see "Operations layer" section below
scripts/              tooling (transcribe.py, shopify-sync.py, run-morning-brief.sh, check-collisions.sh)
index.md              catalog of every wiki page, domain-first
log.md                append-only history, one unified timeline across all domains (wiki + ops)
```

A domain's 4 `wiki/` type-folders are pre-created for all 8 domains even when empty (matches the vault's existing precedent). A domain's `raw/<domain>/assets/` is **not** pre-created — add it the first time that domain actually gets an image asset. Don't pre-create sub-domain folders at all (they're tags, not folders — see Domains above).

**How this grows:** a new top-level domain is an explicit decision Josh makes, never inferred — when it happens, give it the same treatment this restructuring gave the other 8 (an entry in the Domains table, `raw/<domain>/`, `wiki/<domain>/{sources,entities,concepts,synthesis}/`). A domain graduates to its own **nested `CLAUDE.md`** only once it has a real, repeated local convention that doesn't apply vault-wide (e.g. "finance concept pages get an `amount`/`currency` field") — not on domain creation, and never for anything safety-critical (that belongs in this root file, which always loads, instead of a subtree file that loads reactively). None exist yet.

## Naming conventions

- Filenames: kebab-case, no spaces.
- `wiki/<domain>/sources/*.md` filenames are date-prefixed: `YYYY-MM-DD-slug.md` — the date it was ingested, not necessarily published.
- `wiki/<domain>/entities/`, `concepts/`, `synthesis/` filenames are undated slugs — timeless pages updated in place as understanding evolves.
- **Never reuse a basename anywhere in the vault.** Obsidian resolves `[[wikilinks]]` by basename across the *whole* vault regardless of folder or domain — a collision breaks linking silently. This now spans 8 domains × up to 4 folders each, so it's worth actually checking on a new page, not just trusting the convention: `find wiki raw -name "*.md" | xargs -n1 basename | sort | uniq -d` should always come back empty. (This is also why source pages are dated — it keeps them from colliding with the raw file they summarize.)
- Cross-reference with Obsidian wikilinks (`[[page-name]]`), not markdown link syntax `[text](path)` — wikilinks are what power the graph view.
- Drafts in `_review/` keep the exact filename/path they'll have once promoted (just rooted under `_review/` instead of the vault root) — that's what makes "promote" a plain move.

## Page frontmatter

Every page under `wiki/` gets:

```yaml
---
type: source | entity | concept | synthesis
domain: business | schoolwork | fitness | health | habits | finances | media | meta
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [kebab-case, tags]
---
```

`domain` is technically redundant with the folder path, but cheap, and it's what lets any future tool (Dataview, a script, the eventual mission-control OS) query by domain without parsing paths. `tags` is where sub-domains live — see Domains above.

`wiki/<domain>/sources/` pages additionally get `source: raw/<domain>/<filename>` (plain relative path, not a wikilink — keeps the YAML unambiguous). Entity/concept/synthesis pages cite sources inline in the page body instead (a `## Sources` section with wikilinks), since they typically draw on more than one.

Raw files carry light provenance frontmatter, written once when first saved (the one time you touch them):

```yaml
---
type: raw-source
added: YYYY-MM-DD
source_type: pasted | upload | article | video | pdf
source_url: <url, if it came from the web>       # omit for pasted/upload
---
```

## Style

Write for fast skimming, not prose. Prefer short sections and bullets over paragraphs. Every page should be useful read in under a minute. Don't pad a page to look thorough.

## Workflows

There are four operations: **Research** (find/capture new material), **Ingest** (turn a source into wiki pages), **Query** (answer from the wiki), **Lint** (health check). Research feeds Ingest; all four end the same way — nothing touches `raw/`, `wiki/`, `index.md`, or `log.md` directly. Everything drafts into `_review/` first and moves in one **Review & Commit** pass. That's the whole point of `_review/` — see that section below before touching any of these.

Every one of these starts the same way now: **which domain is this?** If it's not obvious, ask Josh rather than guessing — getting this wrong means content sitting under the wrong life area until someone notices.

### Research (finding or capturing new material)

Three acquisition methods, all producing something ready for Ingest:

**Web search.** Use the `WebSearch` tool to find candidates, `WebFetch` to pull a specific page's content. Don't save anything to `raw/` yet — draft candidates into `_review/raw/<domain>/` with a one-line note in the session notes on why each is worth ingesting. Let Josh pick before anything is treated as curated. Exploratory searches that don't turn up anything worth keeping don't need to be staged at all.

**Video / audio.** Run `python3 scripts/transcribe.py <url-or-path>`. It handles YouTube/etc. URLs or local files, prints one JSON object (`title`, `source`, `duration_seconds`, `language`, `model`, `transcript`) to stdout, and installs its own dependencies (`yt-dlp`, `mlx-whisper`, `imageio-ffmpeg`) on first use — that first run will be slow (model download) and needs network access; after that it's local and fast. It prefers `mlx-whisper` (fast on Apple Silicon) and falls back to `openai-whisper` if that's unavailable. Take the `transcript` field, write it into `_review/raw/<domain>/YYYY-MM-DD-slug.md` with `source_type: video` and `source_url` frontmatter (the original URL — don't retain the media file itself, the transcript is the durable artifact; re-fetch from the URL if the audio is ever needed again).

**Articles / textbooks / other text.** Web articles: `WebFetch` the URL, save the extracted text into `_review/raw/<domain>/` with `source_type: article` + `source_url`. PDFs (papers, textbooks, whatever Josh drops in): read directly with the `Read` tool, which handles PDF text extraction natively — use the `pages` parameter to work through long documents in chunks rather than skipping the read. Treat each chapter/section as you would a long source: it's fine to produce several `wiki/<domain>/sources/` pages from one big PDF if it doesn't hold together as a single summary.

Once a candidate is approved (see Review & Commit), it proceeds through Ingest exactly like a source Josh handed over directly.

### Ingest (turning a source into wiki pages)

1. If this came from Research, the raw file is already sitting in `_review/raw/<domain>/`. If Josh handed you something directly, draft it into `_review/raw/<domain>/` the same way (still staged, even though the source itself doesn't need "should this exist" scrutiny — keeps one consistent mechanism).
2. Read it fully.
3. Discuss key takeaways with Josh — unless he's explicitly asked for a batch/unsupervised ingest.
4. Draft `_review/wiki/<domain>/sources/YYYY-MM-DD-slug.md`: a summary page with key takeaways and a link back to the raw file.
5. Draft new or updated `_review/wiki/<domain>/entities/` and `concepts/` pages, linked to the new source page. For an update to a page that already exists in the real `wiki/`, draft the **full proposed version** in `_review/` (not a diff) — copy the current page there first, then edit it. **When a new source contradicts an existing page, don't silently overwrite** — note both claims (what it said before, what changed, which source said what) and flag it to Josh explicitly during review.
6. Note the `index.md` additions/changes in the session notes (the actual file gets updated at commit time).
7. A single source can reasonably touch 10-15 pages — don't hesitate to draft that many in one pass.
8. Nothing here is real yet. Continue to Review & Commit.

### Query (answering a question from the wiki)

1. Read `index.md` first to find candidate pages — it's organized by domain, so start with the domain(s) the question is about.
2. Read the relevant pages, following links if they lead somewhere more specific (links can cross domains).
3. Synthesize an answer, citing the specific wiki page (and raw source where it matters).
4. If the answer is substantial — a comparison, an analysis, a connection worth keeping — draft it into `_review/wiki/<domain>/synthesis/` instead of letting it disappear into chat history. Routine lookups that don't produce a new page don't need staging or a log entry at all.

### Lint (health check)

Run when asked, or proactively suggest one after ~10 ingests or a long gap since the last one. Look for:

- Contradictions between pages
- Stale claims that newer sources have superseded
- Orphan pages with no inbound links
- Concepts mentioned repeatedly across pages but with no page of their own
- Missing cross-references between clearly related pages, including across domains
- Basename collisions across domains (see Naming conventions)
- Gaps a web search could fill

Draft proposed fixes into `_review/` (mirroring the affected paths) rather than editing `wiki/` in place — a lint pass is still a change that needs review like any other.

## Review & Commit

This is the step every session ends with — the one Josh explicitly asked for. Nothing is real until it happens.

**During the session:** draft everything into `_review/`, keep a running `_review/YYYY-MM-DD-session-notes.md` (create it the moment you stage the first thing) — a short log of what's staged and why, one entry per item, so the review isn't you re-explaining from scratch.

**At review time** (end of session, or whenever Josh asks to check in — it doesn't have to wait for the literal last message): walk through `_review/session-notes.md` with him. For each staged item say what it is, what domain it's in, what it changes, and why. He can approve, ask for edits (revise the draft, re-present), or reject (discard it). If a session is about to end with anything still sitting in `_review/`, raise it — don't let it end silently.

**On approval, commit:**
1. Move each approved file from `_review/raw/<domain>/...` → `raw/<domain>/...` and `_review/wiki/<domain>/...` → `wiki/<domain>/...` (same relative path, so this is a plain move — new files land fresh, updates overwrite the existing page).
2. Update `index.md` with the real changes, under the right domain section.
3. Append one entry to `log.md` (format below) — this is the only point at which anything gets logged; drafts and rejected candidates never appear in the log.
4. Delete whatever's left in `_review/` for this batch (rejected drafts, the session notes file) so it's empty again.

Structural changes to the schema itself (new domains, restructuring — the kind of thing this file's own history has already been through once) are the one exception: those get reviewed directly with Josh in the moment (planning it out, confirming the design) rather than staged through `_review/` — staging a change Josh is already co-designing live would just be re-approving it twice. `_review/` is for ongoing content operations a session runs on its own judgment.

## Scope rules (Josh's standing directives, 2026-07-23)

- **Never read, scan, or cite files outside this vault unless Josh explicitly points at them in that conversation.** Material enters this system only when he chooses to bring it in. No proactive environment scans.
- **Start simple; add on pull, not push.** The core product is daily task/time organization. Automations, data pipelines, and integrations get built when Josh asks or a real repeated need shows up — not because they'd be impressive.

## Projects (per-domain chatbots) & dashboard

`projects/<domain>/` — one folder per life area: `business`, `fitness-health`, `marketing` (medical aesthetics practices), `school`, `self-development`. Each has a `CLAUDE.md` persona (loads automatically when working in that folder — opening a session there *is* that domain's chatbot), a `tasks.md`, and a `notes.md`. The same CLAUDE.md text doubles as custom instructions for a claude.ai Project if Josh ever wants these as app-side chats.

- **Tasks:** `- [ ] task (added YYYY-MM-DD) !due:YYYY-MM-DD` (due tag optional). Any session that surfaces a task writes it to the right domain's `tasks.md`; done means checked off, not deleted.
- **Dashboard:** `dashboard.html` at the vault root — today's focus (overdue/due-today) + five domain columns. Regenerate with `python3 scripts/build-dashboard.py` (the morning brief also regenerates it). "Refresh the dashboard" means run that script.
- Projects map to wiki domains for durable knowledge: business→`business`, fitness-health→`fitness`/`health`, marketing→`media`, school→`schoolwork`, self-development→`habits`.

## Operations layer (`ops/`)

The vault holds two things under one root: **knowledge** (`raw/` + `wiki/`, review-gated as above) and **operational state** (`ops/` — machine-refreshed data, schedules, briefs). Plan of record: [[mission-control-spec]]. Different contract:

- **`ops/*/inputs/` and `ops/context/` are human-owned.** Claude reads them, **never** writes, overwrites, reformats, or "cleans up" — if an input looks stale or wrong, say so in the output and stop. (Exception: creating a brand-new template file with fill-in instructions is allowed; editing Josh's content is not.)
- **`ops/*/data/` is machine-owned.** Refreshed by scheduled jobs/skills per `ops/schemas.md`; Josh shouldn't hand-edit (the next refresh overwrites).
- **`ops/*/outputs/` and `ops/briefs/`** are generated — safe to delete and regenerate. Briefs older than 14 days rotate to `ops/briefs/archive/`.
- Ops writes do **not** go through `_review/` — that gate is for knowledge claims, not yesterday's order count. Durable lessons graduate from ops into `wiki/` through the normal review gate.
- Ops domains (`commerce`, `content`, `health`, `drops`) are rhythm-based and map to wiki domains: commerce/content/drops ↔ `business`; health ↔ `health`/`fitness`; Blossom ops (future, gated) ↔ `media`. Mapping lives here so no tool invents a parallel taxonomy.

**Session contract:** every session reads root CLAUDE.md (automatic) + `ops/context/current-priorities.md` + today's brief if present. Sessions log operations to `log.md`. Never overwritten by any agent: human inputs (above), `wiki/`/`raw/` outside review, `log.md` history.

**Hard rails (trump any autonomy grant):** no message sends or social posts, ever, without Josh reading first; Shopify is read-only (no write scopes exist on the token); the health domain tracks and reminds but never doses, tapers, interprets, or advises (see `ops/health/CLAUDE.md` once P4 lands); no Blossom-facing automation until gates G7/G8 clear (spec §2.5).

**Build gates:** ten unanswered questions gate specific builds — table in [[mission-control-spec]] §2.5. Any session asked to build a gated item must surface the gate first.

## index.md conventions

Domain-first: one `##` section per domain, in the Domains table's order (`meta` last). Within each, `###` sub-headings for Sources / Entities / Concepts / Synthesis, one line per page: `- [[page-name]] — one-line summary (date or metadata)`, or `_(none yet)_` if empty — don't hide empty domain or type headings, show the placeholder (matches how this file already treats empty categories elsewhere). A quick-nav line under the title links to each domain heading. Update at commit time — it should never drift out of sync with what's actually in `wiki/`.

## log.md conventions

Append-only, **newest entry at the bottom**. One header per operation:

```
## [YYYY-MM-DD] <ingest|research|query|lint|build> | <domain> | <title>
```

`<domain>` must always be a registered slug — the Domains table above, or an ops slug (`commerce`, `content`, `health`, `drops`), never freeform — that's what keeps it filterable. `build` is for infrastructure work (schema changes, new jobs/skills), which doesn't fit the four content operations. Followed by a few bullets on what was committed. Don't edit past entries except to correct a factual error in the log itself.

Stays a single unified file across all domains — not split per domain — so there's one grep-able timeline of everything that's happened in the whole second brain (this is specifically what a future mission-control layer will want to read). Two greps worth keeping handy:
- All entries: `grep "^## \[" log.md | tail -5`
- One domain: `grep "^## \[.*| finances |" log.md | tail -5`

## Other tools already in this folder

- **`scripts/transcribe.py`** — video/audio → transcript JSON, used by the Research workflow above. Self-installing; first real use will pip-install `yt-dlp` + `mlx-whisper` (or `openai-whisper` as fallback) and download model weights, which needs network access and takes a minute. Untested end-to-end as of when this was written — if `mlx-whisper` fails outright (e.g. Python version mismatch; system Python here is the old Apple-bundled 3.9.6), the `openai-whisper` fallback should still work but is slower (CPU/torch-based). Flag it to Josh if both fail rather than quietly giving up.
- **`graphify-out/`** — a separate, automated knowledge-graph tool (invoked via `/graphify`). It builds its own graph from whatever's in this directory but is not part of this wiki's default workflow — don't route ingest/research/query/lint through it unless Josh explicitly asks. Fine for it to coexist; this schema is the default here. Excluded from Obsidian's index.
- **`.obsidian/`** — vault config for browsing (graph view, search). `_review/`, `graphify-out/`, and `scripts/` are excluded from indexing (`app.json` → `userIgnoreFilters`) so drafts and tooling don't clutter search or the graph view.

## Not set up yet (optional, revisit if the need shows up)

- A dedicated search tool like `qmd` (index.md is enough at this scale — reconsider around ~100 sources; note that spanning 8 domains now will likely cross that total sooner than a single-domain wiki would have)
- Obsidian Web Clipper + the attachment-download hotkey for image-heavy sources
- Dataview queries over the frontmatter above
- Marp slide export from wiki content
- An API-based transcription fallback (e.g. a hosted Whisper API) in case the local `mlx-whisper`/`openai-whisper` path proves too unreliable on this machine
- Nested per-domain `CLAUDE.md` files (see "How this grows" above — none needed yet; `ops/health/CLAUDE.md` will be the first, at P4)
- A git remote (repo is local-only; a private remote unlocks cloud-scheduled runs and backup — decide deliberately, this vault will hold sensitive content)
- Actually connecting the real business (Belated/Seaggs/Manu), media (Blossom Medical/MD-Esti), and finances material into the wiki — structure is ready, first real ingest for each is still pending
