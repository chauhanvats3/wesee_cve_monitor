export const state = () => ({
  'lorem.ipsum': {
    name: 'lorem.ipsum',
    techs: [
      {
        name: 'VueJs',
        ver: '2.5.4',
        cves: ['This is a dummy CVE 1', 'Dummy CVE 2', 'CVE 3'],
        color: '#857036',
      },
      {
        name: 'jQuery',
        ver: '1.9.4',
        cves: ['jQuery CVE this is'],
        color: '0769ad',
      },
    ],
  },
  'vatsal.dev': {
    name: 'vatsal.dev',
    techs: [
      {
        name: 'vuejs',
        ver: '2.5.4',
        cves: ['This is a dummy CVE 1', 'Dummy CVE 2', 'CVE 3'],
        color: '#42b883',
      },
      {
        name: 'jQuery',
        ver: '1.9.4',
        cves: ['jQuery CVE this is'],
        color: '0769ad',
      },
    ],
  },
})

export const mutations = {}

export const actions = {}

export const getters = {
  getDomainInfo: (state) => (domain) => {
    return [state[domain]]
  },
}
