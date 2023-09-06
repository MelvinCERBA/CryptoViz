import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    watch: {
      // use polling
      usePolling: true,
      interval: 500 // Check for changes every half second
    }
  }
})
