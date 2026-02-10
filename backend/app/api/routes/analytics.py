from fastapi import APIRouter, Query
from etl.load.clickhouse_loader import get_clickhouse_client
from backend.app.services.analytics import queries

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"]
)

ch = get_clickhouse_client()

@router.get("/top-products")
def get_top_products(year_month: int=Query(...), limit: int=10):
    if year_month is None:
        
        year_month = ch.query("SELECT max(year_month) FROM monthly_product_sales").result_rows[0][0]

    rows = queries.top_products(year_month, limit)
    return {
        "year_month": year_month,
        "data": [{"product": r[0], "revenue": float(r[1])} for r in rows]
    }
@router.get("/top_categories")
def get_top_categories(year_month: int= Query(...), limit: int=10):
    rows = queries.top_categories(year_month, limit)
    return{
        "data":[{
            "category":r[0],
            "revenue": float(r[1])
        }for r in rows
        ]
    }