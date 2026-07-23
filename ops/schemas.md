# ops/ schemas

Single source of truth for machine-parsed files. Adopted from PRD §5.5 (`raw/meta/prd-mission-control-v1.md`), re-rooted under `ops/`. JSON for machine data, markdown for human data; key JSON files get a generated `.md` view. Changes to this file are review-gated (it's a contract, not state).

## commerce/data/sales-daily.json — append-only, one object per day

```json
{ "days": [ {
  "date": "YYYY-MM-DD", "orders": 0, "units": 0,
  "gross_revenue": 0.0, "discounts": 0.0, "refunds": 0.0, "net_revenue": 0.0,
  "aov": 0.0, "new_customers": 0, "returning_customers": 0, "top_sku": "..." } ] }
```
Dedupe: skip if `date` already present.

## commerce/data/inventory.json — overwritten daily

```json
{ "synced": "ISO-8601", "items": [
  { "sku": "...", "on_hand": 0, "committed": 0, "available": 0, "location": "..." } ] }
```

## commerce/data/sku-performance.json — overwritten weekly by the verdict pass (P5)

Fields per SKU: `sku, title, variant, units_sold, units_on_hand, revenue, landed_cost_unit, gross_margin_pct, sell_through_pct, days_of_cover, return_rate_pct, verdict, reason`.
`verdict`: `restock | hold | discount | discontinue`. `reason` is mandatory, 1–2 sentences. Companion human view: `sku-performance.md`. **The pass must abort if any live SKU lacks a landed cost in `inputs/product-costs.md`.**

## content/data/intelligence-log.json — append via intel-intake (P3 creates it via Notion migration)

Entry fields: `id (cil-NNNN), insight, category, tier, source_creator, source_video, timestamp, date_added, cross_source_count, corroborating_creators[], applies_to[], status, outcome, borderline`.
`category`: `product-signal | marketing-tactic | customer-psychology | competitive-intel | ops-insight`. `tier`: `act-now | worth-revisiting`. `status`: `new | queued | tested | adopted | rejected`. `applies_to` ⊆ `content, commerce, drops, health`.
Dedupe: semantic match → increment `cross_source_count` + append creator, no new row.

## content/data/content-calendar.json — refreshed weekly (P3)

Slot fields: `date, account (personal|brand), format, concept, hook_source (cil-ID|null), status, script_path`.
`format`: `ditl | grwm | garment-breakdown | drop-announcement | pipeline-teaser | talking-head`. `status`: `planned | filmed | edited | posted`. **Never overwrite a slot with status filmed/edited/posted.**

## content/data/post-performance.json — append-only, manual/intel-intake

Post fields: `post_id, account, platform, posted, format, hook_type, views, saves, shares, profile_visits, link_clicks, retention_3s_pct, linked_drop, linked_insight`. Dedupe on `post_id`.

## health/data/refills.json — overwritten per fill (P4)

Medication fields: `name, dose, schedule, prescriber, pharmacy, last_filled, days_supply, refills_remaining, reorder_on, notes`. This file records the protocol; it never sets it.

## health/data/appointments.json — merged by id (P4)

Fields: `id (appt-NNN), provider, purpose, datetime|null, status, due_by, on_calendar, prep_doc`.
`status`: `scheduled | needs-scheduling | completed | cancelled`. `needs-scheduling` past 50% of its `due_by` window is what lets the brief nag.

## health/data/metrics.json — append-only, optional daily

Entry: `date, weight_lb, calories, protein_g, training, sleep_hr, notes`. Same-date entry is overwritten. **Optional — nothing may depend on this existing** (spec cut list).

## drops/data/drops.json — merged by id (G3 partially cleared; facts pending Josh)

Drop fields: `id (drop-NNN), name, phase, launch_date, skus[], manufacturer, po_total_usd, deposit_paid, balance_due_date, sample_round, blockers[]`.
`phase`: `concept | tech-pack | sampling | production | pre-launch | live | postmortem`.

## Refresh table

| File | Populated by | Cadence | Mode |
|---|---|---|---|
| sales-daily.json | scripts/shopify-sync.py | Daily 05:30 ET | Append, dedupe by date |
| inventory.json | scripts/shopify-sync.py | Daily 05:30 ET | Overwrite |
| sku-performance.json/.md | SKU verdict pass | Weekly Sun 07:00 (P5) | Overwrite |
| intelligence-log.json | intel-intake skill | On demand (P3+) | Append w/ semantic dedupe |
| content-calendar.json | calendar refresh | Weekly Sun 08:00 (P3) | Forward slots only |
| post-performance.json | Josh / intel-intake | Ad hoc | Append, dedupe by post_id |
| metrics.json | Josh, conversationally | Optional | Append/overwrite by date |
| refills.json, appointments.json | Josh + P4 flows | Ad hoc | Overwrite med / merge by id |
| drops.json | Josh + drop workflows | Ad hoc | Merge by id |
