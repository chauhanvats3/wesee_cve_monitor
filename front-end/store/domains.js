export const state = () => ({
  allDomains: [],
})

export const mutations = {
  excludeToggle(state, info) {
    let domains = state.allDomains
    for (let i = 0; i < domains.length; i++) {
      if (domains[i].name == info.domain) {
        let subdomains = domains[i].subdomains
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
  addDomain(state, domainInfo) {
    let domain = {}
    domain.full_name = domainInfo.full_name
    domain.name = domainInfo.full_name.split('://')[1]
    domain.verified = false
    domain.enumerate = domainInfo.enumerate
    domain.verify_code = domainInfo.verify_code
    state.allDomains.push(domain)
  },
  removeDomain(state, domainId) {
    let domains = state.allDomains
    for (let i = 0; i < domains.length; i++) {
      if (domains[i].id == domainId) {
        domains.splice(i, 1)
      }
    }
    state.allDomains = domains
  },
  addSubdomain(state, info) {
    let domains = state.allDomains
    for (let i = 0; i < domains.length; i++) {
      if (domains[i].id == info.id) {
        domains[i].subdomains.push(info.subdomain)
      }
    }
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
  async addDomainToBackend(context, domainInfo) {
    let access_token = this.$cookies.get('jwt-access')
    if (access_token) {
      this.$axios.setToken(access_token, 'Bearer')
      console.log(domainInfo)
      try {
        let status = await this.$axios.$post('/domains/', domainInfo)
        domainInfo.id = status.id
        context.commit('addDomain', domainInfo)
        let enumRes = await this.$axios.$post(
          `/domains/${status.id}/enumSubdomains/`
        )
        console.log(enumRes)
      } catch (error) {
        return error
      }
      return 200
    }
  },
  async verifyDomain(context, domainInfo) {
    let access_token = this.$cookies.get('jwt-access')
    if (access_token) {
      this.$axios.setToken(access_token, 'Bearer')
      try {
        let status = await this.$axios.$post(
          '/domains/' + domainInfo.id + '/verify/'
        )
        return status
      } catch (error) {
        return error
      }
    }
  },
  async deleteDomainFromBackend(context, domainName) {
    let domainId = context.getters.getDomainInfo(domainName, 'id')
    let access_token = this.$cookies.get('jwt-access')
    if (access_token) {
      this.$axios.setToken(access_token, 'Bearer')
      try {
        await this.$axios.$delete('/domains/' + domainId)
        context.commit('removeDomain', domainId)
      } catch (error) {
        return error
      }
      return 200
    }
  },
  async addSubdomainToBackend(context, info) {
    let domainId = context.getters.getDomainInfo(info.domainName, 'id')
    let oldSubdomains = context.getters.getDomainInfo(
      info.domainName,
      'subdomains'
    )
    oldSubdomains = JSON.parse(JSON.stringify(oldSubdomains))
    let updateData = {
      subdomains: [
        ...oldSubdomains,
        {
          name: info.subdomainName,
          include: info.include,
          techs: [],
        },
      ],
    }

    let access_token = this.$cookies.get('jwt-access')
    if (access_token) {
      this.$axios.setToken(access_token, 'Bearer')
      try {
        let response = await this.$axios.$patch(
          '/domains/' + domainId + '/',
          updateData
        )
        context.commit('addSubdomain', {
          id: domainId,
          subdomain: response.subdomains.pop(),
        })
      } catch (error) {
        return error
      }
      return 200
    }
  },
  async getTechs(context, info) {},
}

export const getters = {
  getDomainInfo: (state) => (domainName, infoAsked) => {
    let domains = state.allDomains
    for (let i = 0; i < domains.length; i++) {
      if (domains[i].name.includes(domainName)) {
        if (!infoAsked || infoAsked == undefined) {
          return domains[i]
        } else return domains[i][`${infoAsked}`]
      }
    }
  },
  getDomainId: (state) => (domainName) => {
    let domains = state.allDomains
    for (let i = 0; i < domains.length; i++) {
      if (domains[i].name == domainName) {
        return domains[i].id
      }
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
  getExcludedSubdomains: (state) => (domain) => {
    let domains = state.allDomains
    let excluded = []
    for (let i = 0; i < domains.length; i++) {
      if (domains[i].name == domain) {
        let subdomains = domains[i].subdomains
        for (let j = 0; j < subdomains.length; j++) {
          if (!subdomains[j].include) excluded.push(subdomains[i])
        }
        return excluded
      }
    }
  },
  getAllDomains(state) {
    return state.allDomains
  },
}
