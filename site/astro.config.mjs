// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://samueltauil.github.io',
  base: '/skills-hub',
  output: 'static',
  build: {
    assets: 'assets'
  }
});
