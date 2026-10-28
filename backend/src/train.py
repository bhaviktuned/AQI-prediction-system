import sys
import joblib
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from preprocess import prepare


def train(data_path, model_path="../models/xgb_aqi_model.pkl", cities=None):
    X, y, df = prepare(data_path, cities=cities)

    split = int(len(X) * 0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    model = XGBRegressor(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = mean_squared_error(y_test, preds) ** 0.5
    r2 = r2_score(y_test, preds)

    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2:   {r2:.3f}")

    importances = sorted(
        zip(X.columns, model.feature_importances_), key=lambda x: -x[1]
    )
    print("\nFeature importance:")
    for name, score in importances:
        print(f"  {name}: {score:.3f}")

    joblib.dump(model, model_path)
    print(f"\nModel saved to {model_path}")
    return model


if __name__ == "__main__":
    data_path = sys.argv[1] if len(sys.argv) > 1 else "../data/city_day.csv"
    cities = sys.argv[2].split(",") if len(sys.argv) > 2 else None
    train(data_path, cities=cities)
