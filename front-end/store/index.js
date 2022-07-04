//state are app-wide variables
export const state = () => ({})

//mutations are synchronous and for inside app
export const mutations = {}

//actions are async calls to 3rd party
export const actions = {
  async registerUserOnBackend(context, userData) {
    try {
      await this.$axios.$post('/auth/register/', userData).then((data) => {
        console.log(data)
      })
    } catch (err) {
      console.log('Error in action')
      console.log(err.message)
      throw err
    }
    return { status: 201, message: 'Registered Success!' }
  },
}

//getters help inside app to get data from vuex store
export const getters = {
  isAuthenticated(state) {
    return state.auth.loggedIn
  },

  loggedInUser(state) {
    return state.auth.user
  },
}
