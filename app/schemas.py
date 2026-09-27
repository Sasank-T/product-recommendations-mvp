from pydantic import BaseModel
from typing import List, Optional


class Product(BaseModel):
    id: str
    name: str
    category: Optional[str] = None
    company: Optional[str] = None
    tags: List[str] = []
    popularity: float = 0.0
    score: float = 0.0  # Recommendation strength score


class Weights(BaseModel):
    purchase_history: float
    cart_relationship: float
    preferences: float
    popularity: float


class Preferences(BaseModel):
    companies: List[str] = []
    tags: List[str] = []


class RecommendRequest(BaseModel):
    cart: List[str] = []
    purchase_history: List[str] = []
    preferences: Preferences = Preferences()
    weights: Weights
    top_n: int = 5


class RecommendationResponse(BaseModel):
    recommendations: List[Product]
