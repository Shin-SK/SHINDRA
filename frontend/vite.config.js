import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { VitePWA } from 'vite-plugin-pwa'
import path from 'path';

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'STUDIO-SHINDRA',
        short_name: 'SHINDRA',
        icons: [
          {
            src: '/icon-192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/icon-512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ],
        start_url: '/',
        display: 'standalone',
        background_color: '#000000',
        theme_color: '#000000'
      },
    })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src') // これで `@` が `src/` を指すようになる
    }
  },
  css: {
    devSourcemap: true
  }
});
