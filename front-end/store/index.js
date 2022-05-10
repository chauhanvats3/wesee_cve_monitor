//state are app-wide variables
export const state = () => ({
  user: {
    access: null,
    refresh: null,
    isAuthenticated: false,
  },
})

//mutations are synchronous and for inside app
export const mutations = {
  addTokens(state, { access, refresh }) {
    state.user.access = access
    state.user.refresh = refresh
    state.user.isAuthenticated = true

    this.$cookies.set('jwt-access', access, { sameSite: true })
    this.$cookies.set('jwt-refresh', refresh, { sameSite: true })
  },

  destroyTokens(state) {
    state.user.access = null
    state.user.refresh = null
    state.user.isAuthenticated = false
    state.domain = [{}]

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
}

//getters help inside app to get data from vuex store
export const getters = {
  getCookies() {
    this.$cookies.get('jwt-access')
  },
}
