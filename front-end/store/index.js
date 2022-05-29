//state are app-wide variables
export const state = () => ({})

//mutations are synchronous and for inside app
export const mutations = {}

//actions are async calls to 3rd party
export const actions = {}

//getters help inside app to get data from vuex store
export const getters = {
  isAuthenticated(state) {
    return state.auth.loggedIn
  },

  loggedInUser(state) {
    return state.auth.user
  },
}
