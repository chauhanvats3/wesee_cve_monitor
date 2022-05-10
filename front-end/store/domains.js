export const state = () => ({
  allDomains: [],
})

export const mutations = {
  excludeToggle(state, info) {
    let domains = state.allDomains
    for (let i = 0; i < domains.length; i++) {
      if (domains[i].name == info.domain) {
        let subdomains = domains[i].subdomains
        console.log(subdomains)
        for (const subdomain of subdomains) {
          if (subdomain.name == info.subdomain) {
            subdomain.include = !subdomain.include
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
  async addDomainToBackend(context, domainInfo) {},
}

export const getters = {
  getDomainInfo: (state) => (domain) => {
    let domains = state.allDomains
    for (let i = 0; i < domains.length; i++) {
      if (domains[i].name == domain) return domains[i]
    }
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
