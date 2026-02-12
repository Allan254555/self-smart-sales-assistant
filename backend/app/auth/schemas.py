from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    password: str
class Token(BaseModel):
    access_token: str
    password: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None

class RecommendationItem(BaseModel):
    productid: int
    productname: Optional[str] = None
    price: Optional[float] = None
    categoryid: Optional[int] = None
    categoryname: Optional[str] = None
    score: Optional[float] = None
    rank: Optional[int] = None
    popularity: Optional[float] = None
    reason: str


class BasketRecommendationResponse(BaseModel):
    basket: List[int]
    recommendations: List[RecommendationItem]

class CategoryRecommendationResponse(BaseModel):
    categoryid: int
    metric: str
    recommendations: List[RecommendationItem]