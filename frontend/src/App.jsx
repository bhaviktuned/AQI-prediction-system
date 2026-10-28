import { useEffect, useState } from "react";
import CitySelector from "./components/CitySelector";
import ResultCard from "./components/ResultCard";
import { fetchCities, fetchLivePrediction } from "./api";

const FALLBACK_CITIES = ["Delhi", "Bengaluru", "Hyderabad"];

export default function App() {
  const [cities, setCities] = useState(FALLBACK_CITIES);
  const [city, setCity] = useState(FALLBACK_CITIES[0]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCities()
      .then((list) => {
        if (list?.length) {
          setCities(list);
          setCity(list[0]);
        }
      })
      .catch(() => {
        // backend not reachable yet — keep the fallback city list
      });
  }, []);

  async function handlePredict() {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchLivePrediction(city);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        {!result && (
          <CitySelector
            cities={cities}
            city={city}
            onCityChange={setCity}
            onPredict={handlePredict}
            loading={loading}
          />
        )}

        {result && (
          <ResultCard result={result} onBack={() => setResult(null)} />
        )}

        {error && (
          <p className="text-sm text-red-600 mt-4 text-center">{error}</p>
        )}
      </div>
    </div>
  );
}
