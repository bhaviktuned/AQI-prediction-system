from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from predict import load_model, predict_one
from fetch_openaq import fetch_live_pollutants, CITY_COORDS

app = FastAPI(title="AQI Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None


class AQIInput(BaseModel):
    pm25: float
    pm10: float
    no2: float
    so2: float
    co: float
    o3: float
    input_date: date = date.today()


@app.on_event("startup")
def startup():
    global model
    try:
        model = load_model()
    except FileNotFoundError:
        model = None


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.get("/cities")
def cities():
    return {"cities": list(CITY_COORDS.keys())}


@app.get("/predict/live")
def predict_live(city: str):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not trained yet")

    try:
        values = fetch_live_pollutants(city)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))

    today = date.today()
    result = predict_one(model, values, today.month, today.weekday())
    result["city"] = city
    result["live_values"] = values
    return result


@app.post("/predict")
def predict(data: AQIInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not trained yet")

    values = {
        "PM2.5": data.pm25,
        "PM10": data.pm10,
        "NO2": data.no2,
        "SO2": data.so2,
        "CO": data.co,
        "O3": data.o3,
    }
    return predict_one(
        model, values, data.input_date.month, data.input_date.weekday()
    )
