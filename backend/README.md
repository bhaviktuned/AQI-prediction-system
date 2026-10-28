# Smart Air Quality Prediction System — ML pipeline

## Setup
```
pip install -r requirements.txt
```

## Data
Real CPCB pollutant + AQI data (via the Kaggle "Air Quality Data in India" dataset). Expected columns:
`Date, City, PM2.5, PM10, NO2, SO2, CO, O3, AQI`

`data/city_day_cleaned.csv` is included — pre-filtered to Delhi, Bengaluru, and Hyderabad (the
three cities with reliable data coverage in the source file; others like Mumbai and Lucknow had
30–100% missing values in key pollutants and were excluded). Missing values in the used columns
are filled per-city, with a global fallback if a city has none at all (e.g. Lucknow's PM10).

To train on different cities, pass them as a comma-separated second argument (see below), or edit
the `cities` list in your own script.

## Train
```
cd src
python train.py ../data/city_day_cleaned.csv
python train.py ../data/city_day_cleaned.csv "Delhi,Bengaluru"   # optional city filter
```

Prints MAE, RMSE, R², and feature importance, then saves the trained model to `models/xgb_aqi_model.pkl`.

## Run the backend
```
cd src
export OPENAQ_API_KEY=your_key_here   # get one free at explore.openaq.org
uvicorn main:app --reload
```
API docs at `http://localhost:8000/docs`.

- `GET /health` — checks if the model loaded
- `GET /cities` — lists cities available for live fetch (edit `CITY_COORDS` in `fetch_openaq.py` to add more)
- `GET /predict/live?city=Delhi` — fetches live pollutant readings from OpenAQ for that city and returns the model's prediction, plus the raw values used
- `POST /predict` — manual entry, body: `{"pm25": 150, "pm10": 220, "no2": 40, "so2": 15, "co": 1.2, "o3": 60}` (optional `"input_date": "2026-09-15"`)

Both return: predicted AQI, category (Good/Satisfactory/.../Severe), and feature importance.

## Live data source
Uses the [OpenAQ v3 API](https://docs.openaq.org) — free, but requires an API key (sign up at
explore.openaq.org, no broken login flow like data.gov.in). For each city, it finds nearby
monitoring stations, and for each pollutant sensor pulls the **daily average** (via OpenAQ's
`/days` resource) over the last 2 days, averaging where multiple stations report the same
pollutant.

Daily averages are used deliberately, not instantaneous readings — the training data (Kaggle/
CPCB `city_day`) is itself a daily average per city, so this keeps live input consistent with
what the model learned from. Using instant/spot readings instead can produce wildly inflated
predictions during pollution spikes (e.g. evening traffic hours), since a single high moment
isn't representative of a full day.

If a pollutant has no recent daily data anywhere near a city, `/predict/live` returns a 502
error naming which pollutant(s) are missing.

## Known limitation
Even with daily averages, live predictions won't exactly match official published AQI figures
(e.g. from AQI.in or SAFAR) — those may use different station sets, slightly different
averaging windows, or sub-index calculation methods. Treat `/predict/live` as the model's own
estimate from live inputs, not a guaranteed match to any single official source. This is worth
noting explicitly in your report as a real-world data limitation rather than a bug.

## Next
- Build the React frontend: city dropdown → calls `/predict/live` → shows the result
- Optionally cache live fetches for a minute or two to avoid hitting OpenAQ on every page load
