# Connection: Shopify

## Store facts (verified live 2026-07-23)

- Store: **belated** — `wearbelated.com` · Basic plan · USD · America/New_York (EDT)
- One location: **"Shop location"** (no 3PL configured)
- Catalog: 4 active products × 3 variants = 12 variants ("Reconnected" hoodie + sweatshorts, heather gray + faded black; variant titles `1/2/3` — presumed sizes, confirm)
- **Data-quality flag: no SKU codes are set on any variant.** Sync keys on `displayName` until Josh assigns SKUs (do it when the drop's inventory lands; pick the scheme in `ops/context/terminology.md`).

## Access

- **Interactive sessions:** claude.ai Shopify connector (already authorized). Read-only usage by policy.
- **Scheduled sync:** `scripts/shopify-sync.py` → Admin **GraphQL** API, token from `.env`. Read-only by construction — the token is created with read scopes only, so write operations are impossible at the credential level.
- Endpoint: `POST https://<SHOPIFY_STORE_DOMAIN>/admin/api/2025-07/graphql.json`, header `X-Shopify-Access-Token`.
- Network scope of the sync job: this host only.

## Token checklist (Josh, ~15 min, once)

1. Shopify admin (`wearbelated.com/admin`) → **Settings → Apps and sales channels → Develop apps** → enable custom app development if prompted.
2. **Create an app** — name it `josh-brain-sync`.
3. **Configure Admin API scopes — check exactly three:** `read_orders`, `read_products`, `read_inventory`. Nothing else, no write scopes.
4. **Install app** → reveal the Admin API access token (starts `shpat_`) — shown once.
5. Paste into `.env` at the vault root:
   `SHOPIFY_STORE_DOMAIN=<your-store>.myshopify.com` (the *.myshopify.com* domain, Settings → Domains)
   `SHOPIFY_ADMIN_TOKEN=shpat_...`
6. Test: `python3 scripts/shopify-sync.py` — should print a one-line success and update both data files. First scheduled run is 05:30 the next morning.

Until the token exists, the scheduled job exits quietly with a "token not configured" line in `ops/commerce/data/sync-errors.log`, and briefs mark commerce data stale past 48h.

## Files owned

- Writes: `ops/commerce/data/sales-daily.json` (append, dedupe by date), `ops/commerce/data/inventory.json` (overwrite), `ops/commerce/data/sync-errors.log` (append on failure only).
- Never writes anywhere else. Never creates/updates/deletes anything in Shopify.
