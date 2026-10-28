/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        display: ["Space Grotesk", "sans-serif"],
      },
      colors: {
        aqi: {
          good: "#0F9D58",
          satisfactory: "#7CB342",
          moderate: "#F9A825",
          poor: "#F4511E",
          veryPoor: "#C62828",
          severe: "#6A1B9A",
        },
      },
    },
  },
  plugins: [],
};
