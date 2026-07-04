import path from "path"
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { copyFileSync } from 'fs'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(), 
    tailwindcss(),
    // Custom plugin to copy Chrome extension files
    {
      name: 'copy-extension-files',
      writeBundle() {
        // Copy Chrome extension files to dist
        copyFileSync('public/manifest.json', 'dist/manifest.json')
        copyFileSync('public/background.js', 'dist/background.js')
        copyFileSync('public/content.js', 'dist/content.js')
      }
    }
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'index.html'),
      },
      output: {
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    },
    outDir: 'dist',
    assetsDir: 'assets',
    emptyOutDir: false, // Don't empty so we keep extension files
    sourcemap: false, // Disable sourcemaps for extension
    minify: 'terser', // Better minification for extension
    target: 'es2020' // Chrome extension compatibility
  },
  base: './',
  server: {
    port: 5173,
    host: true
  }
})
