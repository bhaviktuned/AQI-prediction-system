export const CATEGORY_STYLES = {
  Good: { bg: "bg-aqi-good/10", text: "text-aqi-good", dot: "bg-aqi-good" },
  Satisfactory: {
    bg: "bg-aqi-satisfactory/10",
    text: "text-aqi-satisfactory",
    dot: "bg-aqi-satisfactory",
  },
  Moderate: {
    bg: "bg-aqi-moderate/10",
    text: "text-aqi-moderate",
    dot: "bg-aqi-moderate",
  },
  Poor: { bg: "bg-aqi-poor/10", text: "text-aqi-poor", dot: "bg-aqi-poor" },
  "Very Poor": {
    bg: "bg-aqi-veryPoor/10",
    text: "text-aqi-veryPoor",
    dot: "bg-aqi-veryPoor",
  },
  Severe: {
    bg: "bg-aqi-severe/10",
    text: "text-aqi-severe",
    dot: "bg-aqi-severe",
  },
};

export function categoryStyle(category) {
  return CATEGORY_STYLES[category] || CATEGORY_STYLES.Moderate;
}
