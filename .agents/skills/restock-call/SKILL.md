---
name: restock-call
description: Answer "should I restock/reorder/discount SKU X" from current Belated data with margin math shown. Fires on restock, reorder, or discount questions about a specific product/SKU. Not for general revenue questions.
---

# restock-call

On-the-spot verdict for one SKU/product, in chat, nothing written. Evidence: recurring decision for a 3PL-stocked DTC line (PRD §6.6); live store confirmed.

## Workflow

1. Identify the SKU/variant (note: store SKUs are unset as of 2026-07-23 — match on product/variant displayName until Josh assigns codes).
2. Read `ops/commerce/data/sku-performance.json` if fresh (<8 days); else compute from `sales-daily.json` (30-day window) + `inventory.json`.
3. Read `ops/commerce/inputs/product-costs.md` and `pricing-rules.md`.
4. Answer with the verdict logic (restock / hold / discount / discontinue per `ops/schemas.md`), showing: units sold, days of cover, gross margin %, and the reason in 1–2 sentences.

## Hard gates

- **No landed cost in `product-costs.md` for this SKU → say so and stop. No margin, no verdict.** Offer to note it in `ops/tasks.md` instead.
- <14 days of sales history → say velocity is insufficient; give inventory facts only.
- Never recommend a price change without stating margin at BOTH old and new price.
- Check the never-discount list before any discount verdict.
- Read-only: writes nothing, changes nothing in Shopify.

## Known failures

*(append one dated line per failure)*
