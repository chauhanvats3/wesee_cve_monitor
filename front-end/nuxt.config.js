export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'We See CVEs',
    htmlAttrs: {
      lang: 'en',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    '~assets/css/normalize.css',
    '~assets/css/main.css',
    '~assets/css/reset.css',
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: ['~plugins/colorConverter.js'],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: ['@nuxtjs/style-resources', 'nuxt-font-loader'],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: ['@nuxtjs/axios', 'cookie-universal-nuxt', '@nuxtjs/auth-next'],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
    baseURL: 'http://localhost:8000/api',
    //baseURL: 'http://104.248.175.4:8000/api',
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},

  router: {
    middleware: ['auth'],
  },
  auth: {
    strategies: {
      local: {
        endpoints: {
          login: { url: 'token/', method: 'post', propertyName: 'data.token' },
          user: false,
          logout: false,
        },
        token: {
          prefix: 'access.',
          property: 'access',
          global: true,
          required: true,
          type: 'Bearer',
        },
        user: {
          property: false,
        },
      },
    },
    redirect: {
      login: '/',
      logout: '/',
      callback: false,
      home: '/domains',
    },
    localStorage: false,
    resetOnError: true,
  },

  fontLoader: {
    url: 'https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap',

    prefetch: true,
    preconnect: true,
  },

  styleResources: {
    scss: [
      '~assets/scss/mixins.scss',
      '~assets/scss/variables.scss',
      '~assets/scss/brands.scss',
    ],
    sass: ['~assets/sass/mixins.sass', '~assets/sass/variables.sass'],
  },
  /*  server: {
    port: 3000,
    host: '104.248.175.4'
  } */
}
