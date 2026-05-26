import vue from "@vitejs/plugin-vue";
import path from "path";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const target = env.BACKEND_URL || "http://127.0.0.1:8000/";

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    server: {
      port: 5173,
      proxy: {
        "/api": target,
      },
    },
    build: {
      outDir: "../backend/arq_dashboard/frontend",
      emptyOutDir: true,
    },
  };
});
