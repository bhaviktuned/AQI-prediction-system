# Smart Air Quality Prediction System — frontend

React + Tailwind CSS. Calls the FastAPI backend's `/cities` and `/predict/live` endpoints.

## Setup
```
npm install
cp .env.example .env    # edit VITE_API_URL if your backend isn't on localhost:8000
npm run dev
```

Make sure the backend (`uvicorn main:app --reload`) is running first — the city dropdown
and predictions both depend on it.

## What it does
1. Loads the list of available cities from `GET /cities`
2. On "Fetch and predict", calls `GET /predict/live?city=...`
3. Shows the predicted AQI, category badge, top pollutant drivers, and the live readings used

## Structure
```
src/
├── api.js                  # fetch calls to the backend
├── categoryStyles.js       # AQI category → color mapping
├── components/
│   ├── CitySelector.jsx    # city dropdown + fetch button
│   └── ResultCard.jsx      # prediction results view
└── App.jsx                 # wires it together
```

## Build for production
```
npm run build
```
Outputs to `dist/` — deploy anywhere static (Vercel, Netlify, GitHub Pages).
