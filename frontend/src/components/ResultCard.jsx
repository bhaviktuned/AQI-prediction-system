import { ArrowLeft } from "lucide-react";
import { categoryStyle } from "../categoryStyles";

const LABELS = {
  "PM2.5": "PM2.5",
  PM10: "PM10",
  NO2: "NO2",
  SO2: "SO2",
  CO: "CO",
  O3: "O3",
};

export default function ResultCard({ result, onBack }) {
  const style = categoryStyle(result.category);
  const topFeatures = result.feature_importance
    .filter((f) => LABELS[f.feature])
    .slice(0, 3);

  return (
    <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
      <div className="flex justify-between items-center mb-5">
        <span className="font-medium text-gray-800">
          {result.city} &middot; today
        </span>
        <span
          className={`text-xs font-medium px-3 py-1 rounded-full ${style.bg} ${style.text}`}
        >
          {result.category}
        </span>
      </div>

      <div className="text-center py-4 border-b border-gray-100">
        <div className="text-sm text-gray-500 mb-1">Predicted AQI</div>
        <div className="font-display text-5xl font-semibold">{result.aqi}</div>
      </div>

      <div className="pt-5">
        <div className="text-sm text-gray-500 mb-3">What's driving this</div>
        <div className="flex flex-col gap-3">
          {topFeatures.map((f) => (
            <div key={f.feature}>
              <div className="flex justify-between text-sm mb-1">
                <span>{LABELS[f.feature]}</span>
                <span className="text-gray-500">
                  {Math.round(f.importance * 100)}%
                </span>
              </div>
              <div className="h-1.5 bg-gray-100 rounded-full">
                <div
                  className="h-full bg-teal-600 rounded-full"
                  style={{ width: `${f.importance * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="pt-5 mt-1">
        <div className="text-xs text-gray-400 mb-4">
          Live readings used: {Object.entries(result.live_values)
            .map(([k, v]) => `${LABELS[k] || k} ${Math.round(v)}`)
            .join(" · ")}
        </div>
        <button
          onClick={onBack}
          className="w-full flex items-center justify-center gap-2 border border-gray-300 hover:bg-gray-50 font-medium rounded-lg py-2.5 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Try another city
        </button>
      </div>
    </div>
  );
}
