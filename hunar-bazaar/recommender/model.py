"""
Content-based product recommender: TF-IDF over each product's
title+description+category, cosine similarity for "customers who viewed
this also liked" suggestions on the buyer portal.

Usage:
    model = ProductRecommender()
    model.fit(products_dataframe)   # columns: id, title, description, category
    model.recommend(product_id, top_k=5)
"""
from __future__ import annotations

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ProductRecommender:
    def __init__(self):
        self._vectorizer = TfidfVectorizer(stop_words="english")
        self._matrix = None
        self._ids: list[str] = []

    def fit(self, products: pd.DataFrame) -> "ProductRecommender":
        text = (
            products["title"].fillna("") + " "
            + products["description"].fillna("") + " "
            + products["category"].fillna("")
        )
        self._matrix = self._vectorizer.fit_transform(text)
        self._ids = products["id"].tolist()
        return self

    def recommend(self, product_id: str, product_catalog=None, top_k: int = 5) -> list[str]:
        if self._matrix is None or product_id not in self._ids:
            return []
        idx = self._ids.index(product_id)
        sims = cosine_similarity(self._matrix[idx], self._matrix).flatten()
        ranked = sims.argsort()[::-1]
        results = []
        for i in ranked:
            if self._ids[i] != product_id:
                results.append(self._ids[i])
            if len(results) >= top_k:
                break
        return results
