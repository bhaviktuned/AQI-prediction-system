import joblib
from preprocess import FEATURES

MODEL_PATH = "../models/xgb_aqi_model.pkl"

BUCKETS = [
    (50, "Good"),
    (100, "Satisfactory"),
    (200, "Moderate"),
    (300, "Poor"),
    (400, "Very Poor"),
    (float("inf"), "Severe"),
]


def load_model(path=MODEL_PATH):
    return joblib.load(path)


def categorize(aqi):
    for limit, label in BUCKETS:
        if aqi <= limit:
            return label
    return "Severe"


def predict_one(model, values: dict, month: int, day_of_week: int):
    row = [[values[f] for f in FEATURES] + [month, day_of_week]]
    aqi = float(model.predict(row)[0])

    importances = sorted(
        zip(FEATURES + ["month", "day_of_week"], model.feature_importances_),
        key=lambda x: -x[1],
    )

    return {
        "aqi": round(aqi, 1),
        "category": categorize(aqi),
        "feature_importance": [
            {"feature": name, "importance": round(float(score), 3)}
            for name, score in importances
        ],
    }
