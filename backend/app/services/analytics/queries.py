# backend/app/services/analytics/queries.py
from backend.app.database.clickhouse import clickhouse_client
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

def run_sql(sql: str):
    ch = clickhouse_client()
    res = ch.query(sql)
    return res.column_names, res.result_rows

def top_products(year_month: int, limit: int = 10):
    ch = clickhouse_client()
    result = ch.query(
        """
        SELECT p.productname, m.total_revenue
        FROM monthly_product_sales m
        JOIN products p ON m.productid = p.productid
        WHERE m.year_month = %(ym)s
        ORDER BY m.total_revenue DESC
        LIMIT %(lim)s
        """,
        parameters={"ym": year_month, "lim": limit}
    )
    return result.result_rows
def top_categories(year_month: int, limit: int=10):
    ch = clickhouse_client()
    return ch.query(
        """
        SELECT c.categoryname, m.total_revenue
        FROM monthly_category_sales m
        JOIN categories c ON m.categoryid = c.categoryid
        WHERE m.year_month = %(ym)s
        ORDER BY m.total_revenue DESC
        LIMIT %(lim)s
        """,parameters={"ym": year_month, "lim":limit}
    ).result_rows

def fetch_product_catalog(product_ids: List[int] | None = None) -> Dict[int, Dict[str, Any]]:
    """
    Returns {productid: {productname, price, categoryid, class, isallergic, vitalitydays, categoryname}}
    """
    ch = clickhouse_client()
    filter_sql = ""
    params = {}

    if product_ids:
        filter_sql = "WHERE p.productid IN {pids:Array(UInt32)}"
        params["pids"] = product_ids

    sql = f"""
        SELECT
            p.productid,
            p.productname,
            p.price,
            p.categoryid,
            p.class,
            p.isallergic,
            p.vitalitydays,
            c.categoryname
        FROM products p
        LEFT JOIN categories c ON c.categoryid = p.categoryid
        {filter_sql}
    """
    res = ch.query(sql, parameters=params)
    cols = res.column_names
    catalog = {}
    for row in res.result_rows:
        d = dict(zip(cols, row))
        catalog[int(d["productid"])] = d
    return catalog

def fetch_top_products_by_category(
    categoryid: int,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    limit: int = 10,
    metric: str = "qty",   # "qty" or "revenue"
) -> List[Dict[str, Any]]:
    """
    Top products in a category by popularity.
    metric:
      - "qty"     -> SUM(quantity)
      - "revenue" -> SUM(totalprice)
    """
    ch = clickhouse_client()

    where = ["p.categoryid = {categoryid:UInt32}"]
    params: Dict[str, Any] = {"categoryid": int(categoryid), "limit": int(limit)}

    if start is not None:
        where.append("s.salesdate >= {start:DateTime64(3)}")
        params["start"] = start
    if end is not None:
        where.append("s.salesdate < {end:DateTime64(3)}")
        params["end"] = end

    metric_sql = "SUM(s.quantity)" if metric == "qty" else "SUM(s.totalprice)"

    sql = f"""
        SELECT
            p.categoryid    AS categoryid,
            p.productid     AS productid,
            p.productname   AS productname,
            p.price         AS price,
            c.categoryname  AS categoryname,
            {metric_sql}    AS popularity
        FROM sales s
        INNER JOIN products p ON p.productid = s.productid
        LEFT JOIN categories c ON c.categoryid = p.categoryid
        WHERE {" AND ".join(where)}
        GROUP BY
            categoryid, productid, productname, price, categoryname
        ORDER BY popularity DESC
        LIMIT {{limit:UInt32}}
    """

    res = ch.query(sql, parameters=params)
    cols = res.column_names
    return [dict(zip(cols, r)) for r in res.result_rows]


def fetch_top_products_all_categories(
    start: datetime,
    end: datetime,
    limit_per_category: int = 10,
    metric: str = "qty",   # "qty" or "revenue"
) -> List[Dict[str, Any]]:
    """
    Top products per category, ranked within each category.
    """
    ch = clickhouse_client()

    metric_sql = "SUM(s.quantity)" if metric == "qty" else "SUM(s.totalprice)"

    sql = f"""
        SELECT
            categoryid,
            productid,
            productname,
            price,
            categoryname,
            popularity,
            rn AS rank
        FROM
        (
            SELECT
                p.categoryid AS categoryid,
                p.productid AS productid,
                p.productname AS productname,
                p.price AS price,
                c.categoryname AS categoryname,
                {metric_sql} AS popularity,
                row_number() OVER (PARTITION BY p.categoryid ORDER BY {metric_sql} DESC) AS rn
            FROM sales s
            INNER JOIN products p ON p.productid = s.productid
            LEFT JOIN categories c ON c.categoryid = p.categoryid
            WHERE s.salesdate >= {{start:DateTime64(3)}} AND s.salesdate < {{end:DateTime64(3)}}
            GROUP BY
                p.categoryid, p.productid, p.productname, p.price, c.categoryname
        )
        WHERE rn <= {{limit_per_category:UInt32}}
        ORDER BY categoryid, rank
    """

    res = ch.query(
        sql,
        parameters={
            "start": start,
            "end": end,
            "limit_per_category": int(limit_per_category),
        },
    )
    cols = res.column_names
    return [dict(zip(cols, r)) for r in res.result_rows]
