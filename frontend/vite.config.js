import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // 讓前端開發階段的 API 請求能順利導向 Python 後端
      '/eel.js': 'http://localhost:8080',
    },
  },
});
