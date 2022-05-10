export const state = () => ({
  allDomains: [],
})

export const mutations = {
  excludeToggle(state, info) {
    for (let i = 0; i < allDomains.length; i++) {
      if (allDomains[i].name == info.domain) {
        let subdomains = allDomains[i].subdomains
        for (const subdomain of subdomains) {
          if (subdomain.name == info.subdomain) {
            subdomain.exclude = !subdomain.exclude
          }
        }
      }
    }
  },
  setDomains(state, data) {
    state.allDomains = data
  },
}

export const actions = {
  async getDomainsFromBackend(context) {
    let access_token = this.$cookies.get('jwt-access')
    this.$axios.setToken(access_token, 'Bearer')
    let domains = []
    try {
      domains = await this.$axios.$get('/domains/')
    } catch (error) {
      return 401
    }
    context.commit('setDomains', domains)
    return 200
  },
}

export const getters = {
  getDomainInfo: (state) => (domain) => {
    return [state.domains]
  },
  getSubdomains: (state) => (domain) => {
    let domains = state.allDomains
    for (let i = 0; i < domains.length; i++) {
      if (domains[i].name == domain) {
        return domains[i].subdomains
      }
    }
  },
  getAllDomains(state) {
    return state.allDomains
  },
}
