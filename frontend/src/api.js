const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function fetchCities() {
  const res = await fetch(`${API_URL}/cities`);
  if (!res.ok) throw new Error("Could not load cities");
  const data = await res.json();
  return data.cities;
}

export async function fetchLivePrediction(city) {
  const res = await fetch(
    `${API_URL}/predict/live?city=${encodeURIComponent(city)}`
  );
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Prediction failed");
  }
  return res.json();
}

export async function fetchManualPrediction(values) {
  const res = await fetch(`${API_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(values),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Prediction failed");
  }
  return res.json();
}
