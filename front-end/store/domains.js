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
    let domain = { ...domainInfo }
    domain.name = domainInfo.full_name.split('://')[1]
    domain.verified = false
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
  addSubdomainTechs(state, info) {
    let domains = state.allDomains
    for (let i = 0; i < domains.length; i++) {
      let subdomains = domains[i].subdomains
      for (let j = 0; j < subdomains.length; j++) {
        if (subdomains[j].id == info.id) {
          subdomains[j].techs = info.techs
          return
        }
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
      let domainId = ''
      let errors = []
      try {
        let info = await this.$axios.$post('/domains/', domainInfo)
        domainInfo.id = info.id
      } catch (error) {
        return error
      }
      try {
        let enumRes = await this.$axios.$post(
          `/domains/${domainInfo.id}/enumSubdomains/`
        )
      } catch (error) {
        errors.push(error)
      }
      try {
        let techRes = await this.$axios.$post(
          `/domains/${domainInfo.id}/findTech/`
        )
      } catch (error) {
        errors.push(error)
      }
      try {
        let photoRes = await this.$axios.$post(
          `/domains/${domainInfo.id}/getPhoto/`
        )
        domainInfo.photo = photoRes.photo
      } catch (error) {
        errors.push(error)
      }

      context.commit('addDomain', domainInfo)

      if (errors.length > 0) return errors
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
  async getTechs(context, id) {
    let techRes = await this.$axios.$post(`/subdomains/${id}/findTech/`)
    context.commit('addSubdomainTechs', techRes)
  },
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
    const isPropValuesEqual = (subject, target, propNames) =>
      propNames.every((propName) => subject[propName] === target[propName])

    const getUniqueItemsByProperties = (items, propNames) =>
      items.filter(
        (item, index, array) =>
          index ===
          array.findIndex((foundItem) =>
            isPropValuesEqual(foundItem, item, propNames)
          )
      )
    let domains = state.allDomains
    for (let i = 0; i < domains.length; i++) {
      if (domains[i].name == domain) {
        let uniques = getUniqueItemsByProperties(domains[i].subdomains, [
          'name',
        ])
        return uniques
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
