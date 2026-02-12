from __future__ import annotations
from typing import List, Dict, Any, Optional
import json

from backend.app.core.config import settings
from backend.app.database.redis_store import get_redis_client
from backend.app.services.analytics.queries import fetch_top_products_by_category

RECO_KEY_NS = "reco:category_top"

#
def _as_dict_rows(rows: list,
                  cols: list | None = None) -> List[Dict[str, Any]]:
    if not rows:
        return []
    if isinstance(rows[0],dict):
        return rows
    if cols is None:
        raise ValueError("Tuple rows returned but no column names provided to map them")
    return [dict(zip(cols, r)) for r in rows]
def recommend_top_in_same_category(categoryid: int, limit: int = 5, metric: str = "qty") -> List[Dict[str, Any]]:
    cid = int(categoryid)
    r = get_redis_client()

    cache_key = f"{RECO_KEY_NS}:{metric}:{cid}"
    raw = r.get(cache_key)
    if raw:
        try:
            items = json.loads(raw)
            return items[:limit]
        except json.JSONDecodeError:
            pass

    # Fallback live query (slower)
    rows = fetch_top_products_by_category(categoryid=cid, limit=limit, metric=metric)

    if rows and not isinstance(rows[0], dict):
        raise ValueError()
    out: List[Dict[str, Any]] = []
    for idx, row in enumerate(rows, start=1):
        out.append(
            {
                "productid": int(row["productid"]),
                "productname": row.get("productname"),
                "price": float(row["price"]) if row.get("price") is not None else None,
                "categoryid": int(row["categoryid"]),
                "categoryname": row.get("categoryname"),
                "popularity": float(row.get("popularity", 0.0) or 0.0),
                "rank": idx,
                "reason": "Top selling products in the same category",
            }
        )
    return out