import { defineConfig } from 'vite';

export default defineConfig(({ mode }) => ({
  root: 'src',
  publicDir: '../public',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    sourcemap: true,
    manifest: true,
    rollupOptions: {
      output: {
        entryFileNames: 'assets/[name].[hash].js',
        chunkFileNames: 'assets/[name].[hash].js',
        assetFileNames: ({ name }) => {
          const ext = name ? name.split('.').pop() : 'bin';
          return `assets/[name].[hash].${ext}`;
        }
      }
    }
  }
}));



