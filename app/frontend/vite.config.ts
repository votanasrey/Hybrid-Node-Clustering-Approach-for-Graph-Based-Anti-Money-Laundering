import { defineConfig, loadEnv } from 'vite'
import { resolve } from 'path';
import fs from 'fs/promises';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Set the third parameter to '' to load all env regardless of the `VITE_` prefix.
  const env = loadEnv(mode, process.cwd(), "");
  return {
    define: {
      __APP_ENV__: JSON.stringify(env.APP_ENV),
    },
    resolve: {
      alias: {
        src: resolve(__dirname, 'src'),
      },
    },
    preview: {
      port: 3001
    },
    server: {
      port: parseInt(env.VITE_SERVER_PORT) || 3000
    },
    esbuild: {
      loader: 'tsx',
      include: /src\/.*\.tsx?$/,
      exclude: [],
    },
    build: {
      outDir: 'build', // Specify the output directory here
    },
    optimizeDeps: {
      esbuildOptions: {
        plugins: [
          {
            name: 'load-js-files-as-tsx',
            setup(build) {
              build.onLoad(
                { filter: /src\\.*\.js$/ },
                async (args) => ({
                  loader: 'tsx',
                  contents: await fs.readFile(args.path, 'utf8'),
                })
              );
            },
          },
        ],
      },
    },

  }
})