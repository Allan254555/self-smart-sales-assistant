from __future__ import annotations
from datetime import datetime
from typing import Dict, List, Any
import json
import os

from backend.app.services.analytics.queries import fetch_top_products_all_categories
from backend.app.database.redis_store import get_redis_client

CATEGORY_KEY_NS = "reco:category_top"

# This trainer builds top-selling product recommendations for each category based on 2018 sales data.
def build_category_top_recos_2018(limit_per_category: int = 20, 
                                  metric: str = "qty") -> Dict[int, List[Dict[str, Any]]]: 
    start = datetime(2018, 1, 1)
    end = datetime(2019, 1, 1)

    rows = fetch_top_products_all_categories(
        start=start,
        end=end,
        limit_per_category=limit_per_category,
        metric=metric,
    )

    by_cat: Dict[int, List[Dict[str, Any]]] = {}
    for r in rows:
        cid = int(r["categoryid"])
        by_cat.setdefault(cid, []).append(
            {
                "productid": int(r["productid"]),
                "productname": r.get("productname"),
                "price": float(r["price"]) if r.get("price") is not None else None,
                "categoryid": cid,
                "categoryname": r.get("categoryname"),
                "popularity": float(r.get("popularity", 0.0) or 0.0),
                "rank": int(r["rank"]),
                "reason": "Top selling products in the same category",
            }
        )
    return by_cat

# Save the category recommendations to Redis, with optional TTL. Returns the number of categories written.
def save_category_recos_to_redis(by_cat: Dict[int, List[Dict[str, Any]]], ttl_seconds: int | None = None) -> int:
    r = get_redis_client()
    pipe = r.pipeline(transaction=False)

    written = 0
    for cid, items in by_cat.items():
        key = f"{CATEGORY_KEY_NS}:{cid}"
        pipe.set(key, json.dumps(items))
        if ttl_seconds:
            pipe.expire(key, int(ttl_seconds))
        written += 1

    pipe.execute()
    return written

# Main function to run the training process for 2018 category top products. Returns summary of the operation.
def run_training_2018_category_top(metric: str = "qty") -> Dict[str, Any]:
    topk = int(os.getenv("RECO_TOPK", "20"))
    by_cat = build_category_top_recos_2018(limit_per_category=topk, metric=metric)
    written = save_category_recos_to_redis(by_cat)
    return {"categories_trained": len(by_cat), "redis_keys_written": written, "metric": metric, "topk": topk}
