---
type: concept
domain: meta
created: 2026-07-22
updated: 2026-07-22
tags: [second-brain, knowledge-management, llm-agents]
---

# LLM-Maintained Wiki

A way of using an LLM to build a personal knowledge base that **compounds** instead of being re-derived from scratch on every question — the pattern this vault (Josh Brain) runs on.

## Definition

Instead of retrieving from raw documents at query time (the RAG pattern), the LLM reads each new source once and integrates it into a persistent, interlinked collection of markdown pages: updating entity pages, revising summaries, flagging contradictions with earlier sources, and refining an evolving synthesis. The synthesis work happens on ingest, not on every query.

## Architecture

1. **Raw sources** (`raw/`) — immutable, curated, source of truth.
2. **The wiki** (`wiki/`) — LLM-owned markdown pages: source summaries, entity pages, concept pages, synthesis. Fully maintained by the LLM.
3. **The schema** (`CLAUDE.md` / `AGENTS.md`) — conventions and workflows, co-evolved between human and LLM.

## Operations

- **Ingest** — new source → summary page, updated entity/concept pages, updated index, logged. Can touch 10-15 pages per source.
- **Query** — answer synthesized from wiki pages with citations; substantial answers get filed back in as new pages rather than lost to chat history.
- **Lint** — periodic health check: contradictions, staleness, orphan pages, missing links, concepts that deserve their own page.

## Why it works

The bottleneck in personal knowledge management has never been reading or thinking — it's the bookkeeping: updating cross-references, catching when new information contradicts old notes, keeping dozens of pages internally consistent. Humans abandon wikis because that maintenance cost grows faster than the value. An LLM doesn't get bored of it and can touch many files in one pass, so the maintenance cost stays near zero as the wiki grows.

## Related ideas

- **RAG** — the more common pattern (NotebookLM, ChatGPT file uploads): retrieves chunks at query time, re-synthesizes from scratch every time, accumulates nothing between sessions. This pattern is a direct response to that limitation.
- **Memex** (Vannevar Bush, 1945) — a proposed personal, curated knowledge store with associative trails between documents; private and actively curated, closer in spirit to this pattern than to how the open web turned out. Bush never solved who does the maintenance — that's the role the LLM fills here. (Not yet a full entity page — revisit if more sources touch on Bush or the Memex specifically.)

## Sources

- [[2026-07-22-llm-wiki-pattern]] — founding idea document; everything above is drawn from this single source so far
