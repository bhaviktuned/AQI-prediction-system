import pandas as pd

FEATURES = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
TARGET = "AQI"


def load_data(path):
    df = pd.read_csv(path, parse_dates=["Date"])
    return df


def clean(df, cities=None):
    if cities:
        df = df[df["City"].isin(cities)].copy()
    df = df.dropna(subset=[TARGET]).copy()
    for col in FEATURES:
        df[col] = df.groupby("City")[col].transform(lambda s: s.fillna(s.median()))
        df[col] = df[col].fillna(df[col].median())
    return df


def add_time_features(df):
    df["month"] = df["Date"].dt.month
    df["day_of_week"] = df["Date"].dt.dayofweek
    return df


def prepare(path, cities=None):
    df = load_data(path)
    df = clean(df, cities=cities)
    df = add_time_features(df)
    df = df.sort_values("Date")
    X = df[FEATURES + ["month", "day_of_week"]]
    y = df[TARGET]
    return X, y, df
