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
  enumToggle(state, domainName) {
    let domains = state.allDomains
    for (let i = 0; i < domains.length; i++) {
      if (domains[i].name == domainName) {
        state.allDomains[i].enumerate = !state.allDomains[i].enumerate
      }
    }
  },
  setDomains(state, data) {
    state.allDomains = data
  },
  resetStore(state) {
    state.allDomains = []
  },
  addDomain(state, domainInfo) {
    let domain = { ...domainInfo }
    domain.name = domainInfo.full_name.split('://')[1]
    domain.verified = false
    state.allDomains.push(domain)
  },
  updateDomain(state, domainInfo) {
    for (let i = 0; i < state.allDomains.length; i++) {
      if (state.allDomains[i].name == domainInfo.name)
        state.allDomains[i] = domainInfo
      return
    }
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
    console.log(info)
    for (let i = 0; i < domains.length; i++) {
      if (domains[i].id == info.id) {
        state.allDomains[i].subdomains = [
          info.subdomain,
          ...state.allDomains[i].subdomains,
        ]
      }
    }
  },
  searchingSubdomainTechs(state, id) {
    let domains = state.allDomains
    for (let i = 0; i < domains.length; i++) {
      let subdomains = domains[i].subdomains
      for (let j = 0; j < subdomains.length; j++) {
        if (subdomains[j].id == id) {
          subdomains[j].techs_fetched = false
          subdomains[j].techs = []
          return
        }
      }
    }
  },
  updateStateTech(state, tech) {
    console.log('Updating state tech')
    let domains = state.allDomains
    for (let i = 0; domains.length; i++) {
      let subdomains = domains[i].subdomains
      let domainTechs = domains[i].techs
      for (let j = 0; j < domainTechs.length; j++) {
        if (domainTechs[j].id == tech.id) {
          console.log('Ho gaya')
          //domainTechs[j] = tech
          console.log(state.allDomains[i].techs[j])
          console.log(tech)
          state.allDomains[i].techs[j] = tech
          state.allDomains[i].techs.push(1)
          state.allDomains[i].techs.pop()

          return
        }
      }

      for (let j = 0; j < subdomains.length; j++) {
        let subdomainTechs = subdomains[j].techs
        for (let k = 0; k < subdomainTechs.length; k++) {
          if (subdomainTechs[k].id == tech.id) {
            //subdomainTechs[k] = tech
            state.allDomains[i].subdomains[j].techs[k] = tech
            state.allDomains[i].subdomains[j].techs.push(1)
            state.allDomains[i].subdomains[j].techs.pop()
            return
          }
        }
      }
    }
  },
}

export const actions = {
  async getDomainsFromBackend(context) {
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
    let errors = []
    try {
      context.commit('addDomain', domainInfo)
      let info = await this.$axios.$post('/domains/', domainInfo)
      domainInfo = info
      context.commit('updateDomain', domainInfo)
    } catch (error) {
      return error
    }

    if (errors.length > 0) return errors
    return 200
  },
  async verifyDomain(context, domainInfo) {
    try {
      let status = await this.$axios.$post(
        '/domains/' + domainInfo.id + '/verify/'
      )
      return status
    } catch (error) {
      return error
    }
  },
  async deleteDomainFromBackend(context, domainName) {
    let domainId = context.getters.getDomainInfo(domainName, 'id')
    try {
      await this.$axios.$delete('/domains/' + domainId)
      context.commit('removeDomain', domainId)
    } catch (error) {
      return error
    }
    return 200
  },
  async addSubdomainToBackend(context, info) {
    let newSubdomain = {
      name: info.subdomainName,
      include: true,
      techs: [],
      techs_fetched: false,
    }
    try {
      let response = await this.$axios.$post(
        '/domains/' + info.domainId + '/addNewSubdomain/',
        newSubdomain
      )
      context.commit('addSubdomain', {
        id: info.domainId,
        subdomain: newSubdomain,
      })
    } catch (error) {
      return error
    }
    return 200
  },
  async getSubdomainTechs(context, id) {
    let techRes = {}
    context.commit('searchingSubdomainTechs', id)
    try {
      techRes = await this.$axios.$post(`/subdomains/${id}/findTech/`)
    } catch (error) {
      console.log('Some Error in getting subdomain techs!')
    }
  },
  async updateTechBackend(context, info) {
    let techRes = ''
    try {
      techRes = await this.$axios.$patch(`/techs/${info.id}/`, {
        versions: { arr: [info.newVer] },
        updating_cve: true,
      })
      context.commit('updateStateTech', techRes)
      return techRes
    } catch (error) {
      return error
    }
  },
  async toggleEnumeration(context, info) {
    try {
      await this.$axios.$patch(`/domains/${info.id}/`, {
        enumerate: !info.enumerate,
      })
    } catch (e) {
      console.log('Error Occurred')
      console.log(e)
    }

    context.commit('enumToggle', info.name)
  },
  async toggleCVESeen(context, techId) {
    try {
      await this.$axios.$post(`/techs/${techId}/markCVEsSeen/`)
    } catch (e) {
      console.log('Error Occurred')
      console.log(e)
    }

    context.commit('cveSeenToggle', techId)
  },
  async changeCronInterval(context, info) {
    try {
      await this.$axios.$patch(`/domains/${info.id}/`, {
        cron_interval: parseInt(info.cronInterval),
      })
    } catch (e) {
      console.log('Error Occurred')
      console.log(e)
    }
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
  getTechFromStore: (state) => (techId) => {
    let domains = state.allDomains
    for (let i = 0; domains.length; i++) {
      let subdomains = domains[i].subdomains
      let domainTechs = domains[i].techs
      for (let j = 0; j < domainTechs.length; j++) {
        if (domainTechs[j].id == techId) {
          return domainTechs[j]
        }
      }

      for (let j = 0; j < subdomains.length; j++) {
        let subdomainTechs = subdomains[j].techs
        for (let k = 0; k < subdomainTechs.length; k++) {
          if (subdomainTechs[k].id == techId) {
            return subdomainTechs[k]
          }
        }
      }
    }
  },
}
