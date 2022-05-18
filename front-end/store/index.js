//state are app-wide variables
export const state = () => ({
  user: {
    isAuthenticated: false,
  },
})

//mutations are synchronous and for inside app
export const mutations = {
  addTokens(state, { access, refresh }) {
    if (state.user.isAuthenticated) return
    state.user.isAuthenticated = true
    this.$cookies.set('jwt-access', access, { sameSite: true })
    this.$cookies.set('jwt-refresh', refresh, { sameSite: true })
  },

  destroyTokens(state) {
    state.user.isAuthenticated = false

    this.$cookies.set('jwt-access', null, { sameSite: true })
    this.$cookies.set('jwt-refresh', null, { sameSite: true })
  },
  onAuthenticated(state) {
    state.user.isAuthenticated = true
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
    let ping = []
    try {
      ping = await this.$axios.$get('/domains/1')
    } catch (error) {
      if (error.toString().includes('status code 404')) {
        context.commit('onAuthenticated')
        return 404
      } else return 401
    }
    context.commit('onAuthenticated')
    return 200
  },
}

//getters help inside app to get data from vuex store
export const getters = {}
