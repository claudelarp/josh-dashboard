---
name: intel-intake
description: Turn a creator-video transcript or link into Content Intelligence Log entries with dedupe. Fires on "log this transcript", "intel intake", or a pasted transcript about content tactics. Not for general video transcription (that's scripts/transcribe.py).
---

# intel-intake

Transcript in → structured, deduped insights in `ops/content/data/intelligence-log.json`. Evidence: the manual habit exists (creator-transcript PDFs in Downloads); the Notion Content Intelligence Log is the P3 migration source.

## Workflow

1. Ingest the transcript: pasted text, a file path, or a URL (URL → run `scripts/transcribe.py` first, use its `transcript` field).
2. Extract discrete insights. Each entry per `ops/schemas.md`: `insight` (one actionable sentence), `category`, `tier`, `source_creator` (match against `ops/content/inputs/creators.md`), `source_video`, `timestamp`, `date_added`, `applies_to`, `status: "new"`, `outcome: null`.
3. **Dedupe before writing:** compare each candidate semantically against existing entries. Match → increment `cross_source_count` + append to `corroborating_creators` — do NOT add a row. This is the mechanism that turns repetition into signal strength.
4. Append survivors with sequential `cil-NNNN` IDs. Report what was added vs. merged.

## Guardrails

- **Gate: if `intelligence-log.json` doesn't exist yet** (P3 migration pending), say so and stash the raw transcript in `ops/content/_intake-queue/` instead — do not create the log file; the migration owns its creation and ID sequence.
- Never lower a `status`; never edit `outcome` (the Sunday review owns outcomes).
- A claim you can't classify gets `borderline: true`, not a guessed category.
- Unknown creator → add entry anyway, flag "not in creators.md" in the report; never edit `creators.md` yourself (human-owned).

## Known failures

*(append one dated line per failure)*
