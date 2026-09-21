/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        // "Hunar" (craft) palette: deep indigo + warm brass, evoking hand-loomed textile branding
        ink: "#211A2C",
        indigo: { DEFAULT: "#3D2C6B", light: "#5A4494" },
        brass: { DEFAULT: "#C08A3E", light: "#E4B76A" },
        cream: "#F7F2E9",
      },
      fontFamily: {
        display: ["'Fraunces'", "serif"],
        body: ["'Inter'", "sans-serif"],
      },
    },
  },
  plugins: [],
};
