//state are app-wide variables
export const state = () => ({
  user: {
    isAuthenticated: false,
  },
})

//mutations are synchronous and for inside app
export const mutations = {
  addTokens(state, { access, refresh }) {
    state.user.isAuthenticated = true

    this.$cookies.set('jwt-access', access, { sameSite: true })
    this.$cookies.set('jwt-refresh', refresh, { sameSite: true })
  },

  destroyTokens(state) {
    state.user.isAuthenticated = false

    this.$cookies.remove('jwt-access')
    this.$cookies.remove('jwt-refresh')
  },
}

//actions are async calls to 3rd party
export const actions = {
  async getTokens(context, { username, password }) {
    let tokens = await this.$axios.$post('/token/', {
      username,
      password,
    })
    context.commit('addTokens', tokens)
  },
  async getPing(context) {
    let access_token = this.$cookies.get('jwt-access')
    this.$axios.setToken(access_token, 'Bearer')
    let users = []
    try {
      users = await this.$axios.$get('/users/')
    } catch (error) {
      return 401
    }
    return 200
  },
}

//getters help inside app to get data from vuex store
export const getters = {}
