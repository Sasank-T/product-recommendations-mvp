from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from typing import List
from app.schemas import RecommendationResponse, Product, RecommendRequest
from app.engine import RecommendationEngine

app = FastAPI(title="Shopping Product Recommendation API", version="1.0.0")

# serve demo static frontend
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Dependency injection for the engine
def get_rec_engine():
    return RecommendationEngine()


@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "healthy", "service": "recommendation-engine"}


@app.get("/api/products", response_model=List[Product], tags=["Products"])
def list_products(engine: RecommendationEngine = Depends(get_rec_engine)):
    return engine.get_all_products()


@app.post("/api/recommend", response_model=RecommendationResponse, tags=["Recommendations"])
def recommend(req: RecommendRequest, engine: RecommendationEngine = Depends(get_rec_engine)):
    # validate weights are non-negative
    w = req.weights
    weights = {
        "purchase_history": max(0.0, w.purchase_history),
        "cart_relationship": max(0.0, w.cart_relationship),
        "preferences": max(0.0, w.preferences),
        "popularity": max(0.0, w.popularity),
    }

    prefs = {"companies": req.preferences.companies, "tags": req.preferences.tags}
    recs = engine.recommend(req.cart, req.purchase_history, prefs, weights, top_n=req.top_n)
    return RecommendationResponse(recommendations=recs)


@app.get("/recommendations/{user_id}", response_model=RecommendationResponse, tags=["Recommendations"])
def get_recommendations(user_id: str, engine: RecommendationEngine = Depends(get_rec_engine)):
    if not user_id.isalnum():
        raise HTTPException(status_code=400, detail="Invalid User ID format. Must be alphanumeric.")

    recommendations = engine.get_recommendations_for_user(user_id)
    return RecommendationResponse(recommendations=recommendations)
