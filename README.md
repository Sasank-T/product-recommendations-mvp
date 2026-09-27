# Product Recommendations MVP

A minimal MVP demonstrating a score-based recommendation engine implemented with FastAPI and a small static frontend.

## Important files
- `app/main.py` - FastAPI application and endpoints (`/api/products`, `/api/recommend`).
- `app/engine.py` - Scoring-based recommendation engine and mock product data.
- `app/schemas.py` - Pydantic models for requests and responses.
- `app/static/index.html` - Static demo UI (sliders, product selectors, dynamic recommendations).

## Requirements
- Python 3.10+ recommended.

## Setup and run (from project root `product-recommendations-mvp`)

1. Install dependencies:
```powershell
pip install -r requirements.txt
```

2. Start the server:
```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

3. Open the demo in your browser:

http://127.0.0.1:8000/static/index.html

## API endpoints
- `GET /api/products` — list mock products.
- `POST /api/recommend` — provide JSON body with `cart`, `purchase_history`, `preferences`, and `weights` to get top-N recommendations. Example body:

```json
{
  "cart": ["p1"],
  "purchase_history": ["p3"],
  "preferences": {"companies": ["RunFast"], "tags": ["running"]},
  "weights": {"purchase_history":40, "cart_relationship":30, "preferences":20, "popularity":10},
  "top_n": 5
}
```

## Notes
- The engine normalizes weight percentages and computes a final score from Purchase History (PH), Cart Relationship (CR), Preferences (PR), and Popularity.
- This is a demo; product data is mocked in `app/engine.py`. Replace with a real database or vector store for production.

If you want, I can also commit these changes and remove any remaining redundant files.
