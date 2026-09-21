"""
Offline training script - pulls products from Mongo (or a CSV export for
local iteration), fits ProductRecommender, and pickles it to model.pkl for
app/services/recommend_service.py to load. Run manually or on a schedule.

    python train.py --source mongo
    python train.py --source csv --path products.csv
"""
import argparse
import pickle

import pandas as pd

from model import ProductRecommender


def load_from_mongo() -> pd.DataFrame:
    import pymongo  # local import: only needed for this path

    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["hunar_bazaar"]
    docs = list(db.products.find({"is_active": True}))
    for d in docs:
        d["id"] = str(d["_id"])
    return pd.DataFrame(docs)[["id", "title", "description", "category"]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["mongo", "csv"], default="mongo")
    parser.add_argument("--path", default="products.csv")
    args = parser.parse_args()

    df = load_from_mongo() if args.source == "mongo" else pd.read_csv(args.path)
    model = ProductRecommender().fit(df)

    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)
    print(f"Trained on {len(df)} products -> model.pkl")


if __name__ == "__main__":
    main()
