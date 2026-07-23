---
name: wiki-ops
description: Run this vault's ingest, lint, or review-commit workflow by the book. Fires on "ingest this", "lint the wiki", "commit the review batch". Not for ops data refreshes or briefs.
---

# wiki-ops

Operationalizes the knowledge-layer workflows defined in root `CLAUDE.md` (Research → Ingest → Review & Commit, plus Lint). Evidence: the workflow has been run manually three times (2026-07-22) — this codifies it.

## Before creating ANY new page

Run `scripts/check-collisions.sh`, and also check the proposed basename manually:
`find wiki raw _review -name "<proposed-basename>.md"` must return nothing. A collision means pick a different slug — never proceed.

## Ingest (follow CLAUDE.md's steps exactly)

1. Confirm the wiki domain — ask Josh if not obvious; never guess.
2. Raw file → `_review/raw/<domain>/` (faithful copy + provenance frontmatter, the one time it's touched).
3. Read fully; discuss takeaways with Josh unless batch mode was requested.
4. Draft source page (`_review/wiki/<domain>/sources/YYYY-MM-DD-slug.md`) + touched entity/concept pages. Full proposed versions for updates, never diffs. Contradictions flagged, never silently overwritten.
5. Session notes entry per staged item (`_review/YYYY-MM-DD-session-notes.md`).
6. Nothing is real until Review & Commit.

## Review & Commit

Walk session notes with Josh → approved items move (plain `mv`, same relative path) → update `index.md` under the right domain → one `log.md` entry → clear `_review/`. Never let a session end with a non-empty `_review/` unsurfaced.

## Lint

Per CLAUDE.md's checklist (contradictions, staleness, orphans, missing pages/links, collisions, gaps) **plus** ops checks: stale `data/` files, machine writes under `inputs/` (contract violations), briefs referencing files that no longer exist, `last_reviewed` drift in `ops/context/`. Findings → `_review/`, fixes only on approval.

## Known failures

*(append one dated line per failure: trigger → wrong behavior → rule that prevents it)*
