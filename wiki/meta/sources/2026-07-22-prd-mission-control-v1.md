---
type: source
domain: meta
created: 2026-07-22
updated: 2026-07-22
tags: [mission-control, architecture, prd]
source: raw/meta/prd-mission-control-v1.md
---

# PRD — Mission Control v1.0 (Cowork-targeted)

A complete build spec for Mission Control produced before this vault existed. Targets Claude Cowork (Desktop) at `~/cowork/`, an 8-hour blocked build.

## Key takeaways

- **The thesis that survives:** the bottleneck is context-switching cost across brand/school/health, not missing information — so the **morning brief is the product**; domains exist to feed it accurate facts.
- Domain set: `content/`, `commerce/`, `health/` fully built; `drops/` cuttable; `studies/`, `finance/` placeholders. Every domain the same shape: `CLAUDE.md`, `inputs/` (human-only), `data/` (machine-owned), `outputs/` (generated).
- **The inputs rule** — machine never writes `inputs/`; if an input looks stale, say so and stop. The single best convention in the document.
- Concrete schemas: intelligence-log v2 (with `status`/`outcome` loop-closing), `sku-performance.json` with a mandatory `verdict` + `reason` per SKU, sales/inventory/refills/appointments/metrics/drops.
- Hard guardrails: never-automated list (no unsent messages, no auto-posting, Shopify read-only, and a permanent clinical boundary — health tracks and reminds, never advises, with a verbatim `health/CLAUDE.md`).
- A 15-entry decision log with the tension behind each call — most decisions port cleanly to any runtime.
- Its own §10 anticipates migrating scheduling to Claude Code if desktop-must-be-running becomes a problem.

## Status

**Superseded as a plan** by [[mission-control-spec]] (runtime → Claude Code, root → this vault), but most of its content — schemas, the inputs rule, guardrails, the brief structure, the decision log — is adopted there by reference. Its assumption #1 ("no existing Obsidian vault") became false the day Josh Brain was built.

## Related

- [[mission-control-spec]] — the v2 spec that supersedes and absorbs this
- [[2026-07-22-mission-control-interview-v2]] — the rigorous re-scoping interview written after this PRD
