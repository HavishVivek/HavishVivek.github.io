import { defineConfig } from 'vite'
   import vue from '@vitejs/plugin-vue'

    module.exports = defineConfig({
      publicPath: process.env.NODE_ENV === 'production'
       ? '/e-library/'
       : '/'

   export default defineConfig({
     plugins: [vue()],
     base: '/HavishVivek.github.io/',
   })
