from typing import List, Dict, Any
from app.schemas import Product


# Mock product profiles for demo
MOCK_PRODUCTS: List[Dict[str, Any]] = [
    {
        "id": "p1",
        "name": "Lightweight Running Shoes",
        "category": "Footwear",
        "company": "RunFast",
        "tags": ["running", "lightweight", "breathable"],
        "popularity": 0.9,
    },
    {
        "id": "p2",
        "name": "Trail Running Shoes",
        "category": "Footwear",
        "company": "TrailPro",
        "tags": ["running", "trail", "durable"],
        "popularity": 0.7,
    },
    {
        "id": "p3",
        "name": "Minimalist Running Shoe",
        "category": "Footwear",
        "company": "RunFast",
        "tags": ["running", "minimal", "lightweight"],
        "popularity": 0.6,
    },
    {
        "id": "p4",
        "name": "City Sneakers",
        "category": "Footwear",
        "company": "UrbanWear",
        "tags": ["casual", "walking"],
        "popularity": 0.5,
    },
    {
        "id": "p5",
        "name": "Orthopedic Running Shoe",
        "category": "Footwear",
        "company": "ComfortRun",
        "tags": ["running", "support"],
        "popularity": 0.4,
    },
    {
        "id": "p6",
        "name": "Wireless Headphones",
        "category": "Electronics",
        "company": "SoundBeat",
        "tags": ["audio", "wireless", "music"],
        "popularity": 0.85,
    },
    {
        "id": "p7",
        "name": "Fitness Tracker",
        "category": "Electronics",
        "company": "PulseTech",
        "tags": ["fitness", "running", "health"],
        "popularity": 0.75,
    },
    {
        "id": "p8",
        "name": "Breathable Socks (3-pack)",
        "category": "Apparel",
        "company": "SockWorks",
        "tags": ["running", "breathable", "accessory"],
        "popularity": 0.65,
    },
    {
        "id": "p9",
        "name": "Sport Water Bottle",
        "category": "Accessories",
        "company": "HydroFlow",
        "tags": ["hydration", "running", "accessory"],
        "popularity": 0.6,
    },
    {
        "id": "p10",
        "name": "Compression Shorts",
        "category": "Apparel",
        "company": "FitWear",
        "tags": ["running", "support", "apparel"],
        "popularity": 0.55,
    },
    {
        "id": "p11",
        "name": "GPS Running Watch",
        "category": "Electronics",
        "company": "RunFast",
        "tags": ["running", "gps", "fitness"],
        "popularity": 0.8,
    },
    {
        "id": "p12",
        "name": "Reflective Vest",
        "category": "Accessories",
        "company": "SafeRun",
        "tags": ["running", "safety", "reflective"],
        "popularity": 0.45,
    },
    {
        "id": "p13",
        "name": "Wireless Earbuds",
        "category": "Electronics",
        "company": "SoundBeat",
        "tags": ["audio", "wireless", "running"],
        "popularity": 0.78,
    },
    {
        "id": "p14",
        "name": "Running Hat",
        "category": "Apparel",
        "company": "SunGuard",
        "tags": ["running", "sun", "accessory"],
        "popularity": 0.5,
    },
    {
        "id": "p15",
        "name": "Foam Roller",
        "category": "Home Fitness",
        "company": "RecoverWell",
        "tags": ["recovery", "fitness", "accessory"],
        "popularity": 0.48,
    },
]


class RecommendationEngine:
    def get_all_products(self) -> List[Product]:
        return [Product(**p) for p in MOCK_PRODUCTS]

    def _tags_overlap_score(self, product_tags: List[str], other_tags: List[str]) -> float:
        if not product_tags or not other_tags:
            return 0.0
        overlap = len(set(product_tags) & set(other_tags))
        return overlap / max(len(set(other_tags)), 1)

    def _preference_score(self, product: Dict[str, Any], preferences: Dict[str, List[str]]) -> float:
        score = 0.0
        total = 0
        if preferences.get("companies"):
            total += 1
            score += 1.0 if product.get("company") in preferences.get("companies") else 0.0
        if preferences.get("tags"):
            total += 1
            # fraction of preferred tags present
            pref_tags = preferences.get("tags")
            score += self._tags_overlap_score(product.get("tags", []), pref_tags)
        return score / total if total > 0 else 0.0

    def _purchase_history_score(self, product: Dict[str, Any], purchase_history_ids: List[str]) -> float:
        # if user already purchased exact product, give high score
        if product["id"] in purchase_history_ids:
            return 1.0
        # otherwise compare tags to previously purchased products
        if not purchase_history_ids:
            return 0.0
        purchased = [p for p in MOCK_PRODUCTS if p["id"] in purchase_history_ids]
        if not purchased:
            return 0.0
        # average tag overlap with purchased items
        scores = [self._tags_overlap_score(product.get("tags", []), p.get("tags", [])) for p in purchased]
        return sum(scores) / len(scores)

    def _cart_relationship_score(self, product: Dict[str, Any], cart_ids: List[str]) -> float:
        if not cart_ids:
            return 0.0
        cart_items = [p for p in MOCK_PRODUCTS if p["id"] in cart_ids]
        if not cart_items:
            return 0.0
        # measure how related the product is to items in cart (tag overlap averaged)
        scores = [self._tags_overlap_score(product.get("tags", []), c.get("tags", [])) for c in cart_items]
        return sum(scores) / len(scores)

    def recommend(self, cart: List[str], purchase_history: List[str], preferences: Dict[str, List[str]], weights: Dict[str, float], top_n: int = 5) -> List[Product]:
        # normalize weights to sum to 1
        total_w = sum(weights.values()) if sum(weights.values()) > 0 else 1.0
        norm = {k: float(v) / total_w for k, v in weights.items()}

        scored: List[Product] = []
        for p in MOCK_PRODUCTS:
            ph = self._purchase_history_score(p, purchase_history)
            cr = self._cart_relationship_score(p, cart)
            pr = self._preference_score(p, preferences)
            pop = float(p.get("popularity", 0.0))

            final = (
                ph * norm.get("purchase_history", 0)
                + cr * norm.get("cart_relationship", 0)
                + pr * norm.get("preferences", 0)
                + pop * norm.get("popularity", 0)
            )

            prod = Product(**p, score=round(final, 4))
            scored.append(prod)

        # sort by score desc and return top_n
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_n]

    # keep compatibility method used earlier
    def get_recommendations_for_user(self, user_id: str) -> List[Product]:
        # simple stub to keep existing endpoint working
        return self.get_all_products()[:3]
