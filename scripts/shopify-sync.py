#!/usr/bin/env python3
"""Daily Shopify -> local data sync (read-only, stdlib only).

Pulls yesterday's orders and current inventory into:
  ops/commerce/data/sales-daily.json   (append, dedupe by date)
  ops/commerce/data/inventory.json     (overwrite)

Failure contract: on any API error or partial data, append one line to
ops/commerce/data/sync-errors.log and write NOTHING else. Missing token is a
quiet no-op (logged once per run) so the launchd job can be installed before
the token exists. Never performs a write operation against Shopify — and the
token is created with read scopes only, so it couldn't.
"""
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
DATA = VAULT / "ops" / "commerce" / "data"
ERRLOG = DATA / "sync-errors.log"
API_VERSION = "2025-07"
EASTERN = timezone(timedelta(hours=-4))  # EDT; drop dates are date-level, DST skew is tolerable


def log_error(msg):
    ERRLOG.parent.mkdir(parents=True, exist_ok=True)
    with ERRLOG.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now(EASTERN).isoformat()} {msg}\n")


def read_env():
    env = {}
    env_file = VAULT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env


def gql(domain, token, query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        f"https://{domain}/admin/api/{API_VERSION}/graphql.json",
        data=body,
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": token},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode())
    if payload.get("errors"):
        raise RuntimeError(f"GraphQL errors: {payload['errors']}")
    return payload["data"]


ORDERS_QUERY = """
query Orders($q: String!, $after: String) {
  orders(first: 50, query: $q, after: $after) {
    pageInfo { hasNextPage endCursor }
    nodes {
      currentTotalPriceSet { shopMoney { amount } }
      totalDiscountsSet { shopMoney { amount } }
      totalRefundedSet { shopMoney { amount } }
      customer { numberOfOrders }
      lineItems(first: 50) { nodes { quantity sku name } }
    }
  }
}
"""

INVENTORY_QUERY = """
query Inv($after: String) {
  productVariants(first: 100, after: $after) {
    pageInfo { hasNextPage endCursor }
    nodes {
      sku displayName
      product { status }
      inventoryItem { inventoryLevels(first: 5) { nodes {
        location { name }
        quantities(names: ["available", "committed", "on_hand"]) { name quantity }
      } } }
    }
  }
}
"""


def paginate(domain, token, query, variables, path):
    after = None
    while True:
        data = gql(domain, token, query, {**variables, "after": after})
        conn = data
        for key in path:
            conn = conn[key]
        yield from conn["nodes"]
        if not conn["pageInfo"]["hasNextPage"]:
            break
        after = conn["pageInfo"]["endCursor"]


def main():
    env = read_env()
    domain, token = env.get("SHOPIFY_STORE_DOMAIN"), env.get("SHOPIFY_ADMIN_TOKEN")
    if not domain or not token:
        log_error("token not configured yet (fill .env per ops/connections/shopify.md)")
        print("shopify-sync: no token configured, skipping (logged)")
        return 0

    yesterday = (datetime.now(EASTERN) - timedelta(days=1)).date()
    day_after = yesterday + timedelta(days=1)

    try:
        orders = list(paginate(domain, token, ORDERS_QUERY,
                               {"q": f"created_at:>={yesterday} created_at:<{day_after}"},
                               ["orders"]))
        variants = list(paginate(domain, token, INVENTORY_QUERY, {}, ["productVariants"]))
    except (urllib.error.URLError, RuntimeError, KeyError, json.JSONDecodeError) as e:
        log_error(f"sync failed, nothing written: {e}")
        print(f"shopify-sync: FAILED ({e})", file=sys.stderr)
        return 1

    units, gross, discounts, refunds, new_c, ret_c = 0, 0.0, 0.0, 0.0, 0, 0
    sku_units = {}
    for o in orders:
        gross += float(o["currentTotalPriceSet"]["shopMoney"]["amount"])
        discounts += float(o["totalDiscountsSet"]["shopMoney"]["amount"])
        refunds += float(o["totalRefundedSet"]["shopMoney"]["amount"])
        cust = o.get("customer")
        if cust is not None:
            if int(cust.get("numberOfOrders", 1)) <= 1:
                new_c += 1
            else:
                ret_c += 1
        for li in o["lineItems"]["nodes"]:
            units += li["quantity"]
            key = li["sku"] or li["name"]  # SKUs unset store-wide as of 2026-07-23
            sku_units[key] = sku_units.get(key, 0) + li["quantity"]

    net = gross - refunds
    day_obj = {
        "date": str(yesterday),
        "orders": len(orders),
        "units": units,
        "gross_revenue": round(gross, 2),
        "discounts": round(discounts, 2),
        "refunds": round(refunds, 2),
        "net_revenue": round(net, 2),
        "aov": round(net / len(orders), 2) if orders else 0.0,
        "new_customers": new_c,
        "returning_customers": ret_c,
        "top_sku": max(sku_units, key=sku_units.get) if sku_units else None,
    }

    inv_items = []
    for v in variants:
        if v["product"]["status"] != "ACTIVE":
            continue
        levels = v["inventoryItem"]["inventoryLevels"]["nodes"]
        for lvl in levels:
            q = {x["name"]: x["quantity"] for x in lvl["quantities"]}
            inv_items.append({
                "sku": v["sku"],
                "displayName": v["displayName"],
                "on_hand": q.get("on_hand", 0),
                "committed": q.get("committed", 0),
                "available": q.get("available", 0),
                "location": lvl["location"]["name"],
            })

    # All fetches succeeded — only now touch disk.
    sales_path = DATA / "sales-daily.json"
    sales = json.loads(sales_path.read_text(encoding="utf-8")) if sales_path.exists() else {"days": []}
    if any(d["date"] == day_obj["date"] for d in sales["days"]):
        print(f"shopify-sync: {day_obj['date']} already present, inventory refreshed only")
    else:
        sales["days"].append(day_obj)
        sales["days"].sort(key=lambda d: d["date"])
        sales_path.write_text(json.dumps(sales, indent=2) + "\n", encoding="utf-8")

    (DATA / "inventory.json").write_text(json.dumps({
        "synced": datetime.now(EASTERN).isoformat(timespec="seconds"),
        "items": inv_items,
    }, indent=2) + "\n", encoding="utf-8")

    print(f"shopify-sync: {day_obj['date']} orders={day_obj['orders']} net=${day_obj['net_revenue']} · {len(inv_items)} inventory rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
