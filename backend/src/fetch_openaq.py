import os
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
 
import requests
from dotenv import load_dotenv
 
load_dotenv()
 
BASE_URL = "https://api.openaq.org/v3"
API_KEY = os.environ.get("OPENAQ_API_KEY", "")
 
SENSORS_PER_POLLUTANT = 3
CACHE_SECONDS = 600
_cache = {}
 
PARAM_MAP = {
    "pm25": "PM2.5",
    "pm10": "PM10",
    "no2": "NO2",
    "so2": "SO2",
    "co": "CO",
    "o3": "O3",
}
 
EXPECTED_UNITS = {
    "PM2.5": "µg/m³",
    "PM10": "µg/m³",
    "NO2": "µg/m³",
    "SO2": "µg/m³",
    "O3": "µg/m³",
    "CO": "mg/m³",
}
 
CITY_COORDS = {
    "Delhi": (28.6139, 77.2090),
    "Bengaluru": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
}
 
 
def _headers():
    return {"X-API-Key": API_KEY}
 
 
def _convert(param, value, unit):
    expected = EXPECTED_UNITS[param]
    if unit == expected:
        return value
    if unit in ("µg/m³", "ug/m3") and expected == "mg/m³":
        return value / 1000
    if unit in ("mg/m³", "mg/m3") and expected == "µg/m³":
        return value * 1000
    return value
 
 
def get_locations(lat, lon, radius=25000, limit=100):
    url = f"{BASE_URL}/locations"
    params = {"coordinates": f"{lat},{lon}", "radius": radius, "limit": limit}
    r = requests.get(url, params=params, headers=_headers(), timeout=10)
    r.raise_for_status()
    return r.json()["results"]
 
 
def get_recent_daily_average(sensor_id, days_back=2):
    now = datetime.now(timezone.utc)
    params = {
        "datetime_from": (now - timedelta(days=days_back)).isoformat(),
        "datetime_to": now.isoformat(),
        "limit": days_back + 1,
    }
    url = f"{BASE_URL}/sensors/{sensor_id}/days"
    r = requests.get(url, params=params, headers=_headers(), timeout=8)
    r.raise_for_status()
    values = [row["value"] for row in r.json()["results"] if row.get("value") is not None]
    if not values:
        return None
    return sum(values) / len(values)
 
 
def _pick_sensors(locations):
    ranked = sorted(locations, key=lambda loc: loc.get("distance") or 1e12)
    counts = defaultdict(int)
    picked = []
    for loc in ranked:
        for sensor in loc.get("sensors", []):
            name = sensor["parameter"]["name"]
            if name not in PARAM_MAP:
                continue
            param = PARAM_MAP[name]
            if counts[param] >= SENSORS_PER_POLLUTANT:
                continue
            counts[param] += 1
            picked.append((sensor["id"], param, sensor["parameter"].get("units", "")))
    return picked
 
 
def _fetch_one(task):
    sensor_id, param, unit = task
    try:
        avg = get_recent_daily_average(sensor_id)
    except requests.RequestException:
        return None
    if avg is None:
        return None
    return param, _convert(param, avg, unit)
 
 
def fetch_live_pollutants(city):
    if city not in CITY_COORDS:
        raise ValueError(f"No coordinates configured for city: {city}")
 
    cached = _cache.get(city)
    if cached and time.time() - cached[0] < CACHE_SECONDS:
        return cached[1]
 
    lat, lon = CITY_COORDS[city]
    try:
        locations = get_locations(lat, lon)
    except requests.RequestException as e:
        raise ValueError(f"Could not reach OpenAQ: {e}")
    if not locations:
        raise ValueError(f"No monitoring stations found near {city}")
 
    tasks = _pick_sensors(locations)
    values = defaultdict(list)
    with ThreadPoolExecutor(max_workers=6) as pool:
        for outcome in pool.map(_fetch_one, tasks):
            if outcome:
                param, value = outcome
                values[param].append(value)
 
    result = {}
    for param in PARAM_MAP.values():
        readings = values.get(param)
        if readings:
            result[param] = round(sum(readings) / len(readings), 2)
 
    missing = [p for p in PARAM_MAP.values() if p not in result]
    if missing:
        raise ValueError(f"No live data available for: {', '.join(missing)}")
 
    _cache[city] = (time.time(), result)
    return result