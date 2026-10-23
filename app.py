from flask import Flask, jsonify, render_template, request
from pathlib import Path
import json

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "products.json"


def load_products():
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def score_product(product, query):
    q = query.lower().strip()
    if not q:
        return 0

    haystack = " ".join([
        product.get("name", ""),
        product.get("category", ""),
        product.get("brand", ""),
        product.get("tags", " ".join(product.get("tags", [])))
    ]).lower()

    score = 0
    if q in haystack:
        score += 20
    for token in q.split():
        if token in haystack:
            score += 8
    if product.get("source") and q in product["source"].lower():
        score += 3
    return score


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/products")
def api_products():
    query = request.args.get("q", "").strip()
    products = load_products()

    if query:
        scored = [
            {**p, "match_score": score_product(p, query)}
            for p in products
        ]
        filtered = [p for p in scored if p["match_score"] > 0]
        filtered.sort(key=lambda p: p["match_score"], reverse=True)
    else:
        filtered = [{**p, "match_score": 0} for p in products]

    result = {
        "query": query,
        "count": len(filtered),
        "products": [
            {
                "id": p["id"],
                "name": p["name"],
                "brand": p["brand"],
                "category": p["category"],
                "source": p["source"],
                "price": p["price"],
                "original_price": p.get("original_price"),
                "rating": p.get("rating"),
                "reviews": p.get("reviews"),
                "delivery": p.get("delivery"),
                "match_score": p["match_score"],
                "url": p.get("url"),
                "tags": p.get("tags", [])
            }
            for p in filtered
        ],
        "summary": (
            f"Found {len(filtered)} relevant product matches for '{query}' across leading marketplaces."
            if query
            else "Browse trending products from Amazon, Flipkart, and Meesho."
        )
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
