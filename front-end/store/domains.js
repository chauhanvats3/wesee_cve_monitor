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
    for (let i = 0; i < domains.length; i++) {
      if (domains[i].id == info.id) {
        state.allDomains[i].subdomains.push(info.subdomain)
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
          subdomains[j].techSearched = true
          return
        }
      }
    }
  },
  updateStateTech(state, tech) {
    let domains = state.allDomains
    for (let i = 0; domains.length; i++) {
      let subdomains = domains[i].subdomains
      let domainTechs = domains[i].techs
      for (let j = 0; j < domainTechs.length; j++) {
        if (domainTechs[j].id == tech.id) {
          domainTechs[j] = tech
          return
        }
      }

      for (let j = 0; j < subdomains.length; j++) {
        let subdomainTechs = subdomains[j].techs
        for (let k = 0; k < subdomainTechs.length; k++) {
          if (subdomainTechs[k].id == tech.id) {
            subdomainTechs[k] = tech
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
  },
  async getSubdomainTechs(context, id) {
    let techRes = {}
    try {
      techRes = await this.$axios.$post(`/subdomains/${id}/findTech/`)
    } catch (error) {
      context.commit('addSubdomainTechs', techRes)
    }
    context.commit('addSubdomainTechs', techRes)
  },
  async updateTech(context, info) {
    let techRes = ''
    try {
      techRes = await this.$axios.$patch(`/techs/${info.id}/`, {
        versions: { arr: [info.newVer] },
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
  async toggleCVESeen(context, info) {
    try {
      await this.$axios.$patch(`/cves/${info.id}/`, {
        isSeen: true,
        isNew: false,
      })
    } catch (e) {
      console.log('Error Occurred')
      console.log(e)
    }

    //context.commit('cveSeenToggle',info.id)
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
  getTech: (state) => (techId) => {
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
