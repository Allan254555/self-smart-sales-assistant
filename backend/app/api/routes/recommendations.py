from __future__ import annotations 

from typing import List, Optional
from fastapi import APIRouter, Query
from backend.app.auth.schemas import CategoryRecommendationResponse
from backend.app.services.recommendations.category_services import recommend_top_in_same_category

router = APIRouter(prefix="/reco", tags=["recommendations"])

@router.get("/category-top", response_model=CategoryRecommendationResponse)
def category_top(
    categoryid: int = Query(..., ge=1),
    limit: int = Query(5, ge=1, le=20),
    metric: str = Query("qty", pattern="^(qty|revenue)$"),
):
    recs = recommend_top_in_same_category(categoryid=categoryid, limit=limit, metric=metric)
    return {"categoryid": categoryid, 
            "metric": metric, 
            "recommendations": recs}
