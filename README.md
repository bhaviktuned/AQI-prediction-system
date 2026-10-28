# Smart Air Quality Prediction System

XGBoost model + FastAPI backend + React/Tailwind frontend. Predicts AQI from live pollutant
data (OpenAQ) or manual input.

```
smart-aqi-system/
├── backend/    # model training, FastAPI server, OpenAQ live fetch
└── frontend/   # React + Tailwind UI
```

## Run order
1. `cd backend`, follow `backend/README.md` to train the model and start the API
   (`uvicorn main:app --reload`, needs a free OpenAQ key)
2. `cd frontend`, follow `frontend/README.md` to install and start the UI (`npm run dev`)
3. Open the frontend, pick a city, click "Fetch and predict"

See each folder's own README for full details.
