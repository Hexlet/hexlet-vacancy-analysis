import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { resolve } from "path";

// https://vite.dev/config/
export default defineConfig({
  root: resolve("src"),
  base: "/static/",
  plugins: [react(), tailwindcss()],
  build: {
    outDir: resolve("static/dist"),
    assetsDir: "",
    manifest: "manifest.json",
    emptyOutDir: true,
    rollupOptions: {
      // Overwrite default .html entry to main.tsx in the static directory
      input: resolve("src/main.tsx"),
    },
  },
});
