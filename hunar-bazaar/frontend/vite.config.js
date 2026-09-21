import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Backend cookies are same-site during dev via this proxy.
      "/api": "http://localhost:8000",
    },
  },
});
