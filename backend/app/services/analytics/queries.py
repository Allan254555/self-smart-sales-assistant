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

def fetch_transactions(start: Optional[datetime] = None, 
                       end: Optional[datetime] = None) -> List[Dict[str, Any]]: # Fetch transactions with optional date filtering
    ch = clickhouse_client()
    sql = "SELECT * FROM transactions"
    where = []
    params = {}
    if start is not None:
        where.append("salesdate >= {start:DateTime64(3)}")
        params["start"] = start
    if end is not None:
        where.append("salesdate < {end:DateTime64(3)}")
        params["end"] = end

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    sql = f"""
        SELECT
            transactionnumber,
            customerid,
            salesdate,
            productid
        FROM sales
        {where_sql}
    """
    res = ch.query(sql, parameters=params)
    cols = res.column_names
    return [dict(zip(cols, r)) for r in res.result_rows]


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