export const state = () => ({
  'vatsal.dev': {
    name: 'vatsal.dev',
    techs: [],
    enumSubdomains: true,
    subdomains: [],
  },
})

export const mutations = {
  addSubdomain(state, info) {},
  excludeToggle(state, info) {
    let subdomains = state[info.domain].subdomains
    for (const subdomain of subdomains) {
      if (subdomain.name == info.subdomain) {
        subdomain.exclude = !subdomain.exclude
      }
    }
  },
}

export const actions = {
  async getDomainsFromBackend(context) {
    let access_token = this.$cookies.get('jwt-access')
    this.$axios.setToken(access_token, 'Bearer')
    let domains = await this.$axios.$get('/domains/')
    return domains
  },
}

export const getters = {
  getDomainInfo: (state) => (domain) => {
    return [state[domain]]
  },
  getSubdomains: (state) => (domain) => {
    return state[domain].subdomains
  },
}
