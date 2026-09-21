"""
Thin wrapper around the scikit-learn content-based recommender in
/recommender. Kept out-of-process for the scaffold (loads a pickled model
lazily); swap for a microservice call if the model grows.
"""
from pathlib import Path
import pickle

_MODEL_PATH = Path(__file__).resolve().parents[3] / "recommender" / "model.pkl"
_model_cache = None


def _load_model():
    global _model_cache
    if _model_cache is None and _MODEL_PATH.exists():
        with open(_MODEL_PATH, "rb") as f:
            _model_cache = pickle.load(f)
    return _model_cache


def recommend_similar_products(product_id: str, product_catalog: list[dict], top_k: int = 5) -> list[str]:
    """
    Returns up to top_k product_ids similar to product_id.
    Falls back to same-category products if the trained model isn't present yet
    (keeps the endpoint usable before recommender/train.py has been run).
    """
    model = _load_model()
    if model is None:
        target = next((p for p in product_catalog if p["id"] == product_id), None)
        if not target:
            return []
        return [
            p["id"] for p in product_catalog
            if p["category"] == target["category"] and p["id"] != product_id
        ][:top_k]

    return model.recommend(product_id, product_catalog, top_k=top_k)
