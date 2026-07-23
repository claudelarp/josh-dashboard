---
type: source
domain: meta
created: 2026-07-22
updated: 2026-07-22
tags: [second-brain, knowledge-management, llm-agents, obsidian]
source: raw/meta/llm-wiki-pattern.md
---

# LLM Wiki (idea document)

The founding design doc for this vault. Proposes maintaining a personal knowledge base as a persistent, LLM-maintained markdown wiki rather than a RAG-style pile of files retrieved fresh on every query.

## Key takeaways

- **RAG re-derives, a wiki accumulates.** Standard file-upload/RAG tools (NotebookLM, ChatGPT uploads) retrieve chunks at query time and rebuild the synthesis from scratch every time. A maintained wiki does the synthesis once, on ingest, and keeps it current — cross-references, contradictions, and evolving theses persist between sessions instead of being rediscovered.
- **Three-layer architecture:** immutable `raw/` sources → LLM-owned `wiki/` pages (summaries, entities, concepts, synthesis) → a schema document (this vault's `CLAUDE.md`) that tells the LLM the conventions and workflows. The schema is co-evolved with the human over time.
- **Three operations:** *ingest* (new source → summary page + updates to touched entity/concept pages + index + log, often 10-15 pages in one pass), *query* (answer from the wiki, citing pages, and file substantial answers back in as new pages instead of losing them to chat history), *lint* (periodic health check for contradictions, staleness, orphan pages, missing links).
- **`index.md`** (content catalog, organized by category) and **`log.md`** (append-only, chronological, parseable via a consistent `## [date] type | title` prefix) are the two navigation files that let the wiki scale without embedding-based search, up to roughly 100 sources / hundreds of pages.
- **Obsidian is the intended viewer**, not the editor — wikilinks, the graph view, and (optionally) Dataview over frontmatter. The LLM writes; the human reads, browses, and directs.
- **Why it works:** the bottleneck in personal wikis has always been maintenance bookkeeping (updating cross-references, flagging contradictions, keeping summaries current), not the reading or thinking. That's exactly the part LLMs don't get bored of.
- **Historical framing:** explicitly positions this as a realization of Vannevar Bush's Memex (1945) — a private, curated, associatively-linked knowledge store. Bush's unsolved problem was who does the maintenance; the LLM is the answer.
- **Deliberately unopinionated** about the specifics (directory layout, page formats, tooling) — the document's own instruction is to hand it to an LLM agent and jointly instantiate a version fitted to the domain. This vault's `CLAUDE.md` is that instantiation.

## How this applies to Josh Brain

This vault *is* the pattern, applied. The folder structure, frontmatter, and ingest/query/lint workflows in `CLAUDE.md` are the concrete choices made from this document's abstract architecture. This source page and [[llm-maintained-wiki]] are themselves the first live example of the ingest workflow the document describes.

## Related

- [[llm-maintained-wiki]] — the distilled, evolving concept page for the pattern itself

## Source

Raw file: `raw/meta/llm-wiki-pattern.md`
