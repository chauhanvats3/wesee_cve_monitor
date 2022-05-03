//state are app-wide variables
export const state = () => ({
  domains: [
    {
      name: 'vatsal.dev',
      verified: false,
    },
    {
      name: 'lorem.ipsum',
      verified: true,
    },
  ],
})

//mutations are synchronous and for inside app
export const mutations = {
  addDomain(state, domain) {
    state.domains.push({ name: domain, verified: false })
  },
}

//actions are async calls to 3rd party
export const actions = {}

//getters help inside app to get data from vuex store
export const getters = {
  getAllDomains(state) {
    return state.domains
  },
}
