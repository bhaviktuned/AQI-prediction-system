import { Wind, RefreshCw } from "lucide-react";

export default function CitySelector({ cities, city, onCityChange, onPredict, loading }) {
  return (
    <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
      <div className="flex flex-col items-center text-center mb-6">
        <Wind className="w-7 h-7 text-teal-600 mb-2" />
        <h1 className="font-display text-xl font-semibold">Predict air quality</h1>
        <p className="text-sm text-gray-500 mt-1">
          Live pollutant data, fetched automatically
        </p>
      </div>

      <label className="block text-sm text-gray-600 mb-1">City</label>
      <select
        value={city}
        onChange={(e) => onCityChange(e.target.value)}
        className="w-full border border-gray-300 rounded-lg px-3 py-2 mb-4 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
      >
        {cities.map((c) => (
          <option key={c} value={c}>
            {c}
          </option>
        ))}
      </select>

      <button
        onClick={onPredict}
        disabled={loading}
        className="w-full flex items-center justify-center gap-2 bg-teal-600 hover:bg-teal-700 disabled:opacity-60 text-white font-medium rounded-lg py-2.5 transition-colors"
      >
        <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
        {loading ? "Fetching..." : "Fetch and predict"}
      </button>

      <p className="text-xs text-gray-400 mt-3 text-center">
        Source: CPCB stations, via OpenAQ live API
      </p>
    </div>
  );
}
