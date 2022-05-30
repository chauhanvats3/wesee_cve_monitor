<template>
  <div class="domains">
    <Nav />
    <p v-if="$fetchState.pending">Fetching Domains...</p>
    <div v-else>
      <div class="content">
        <DomainCard
          v-for="(domainInfo, index) in domains"
          :key="index"
          :domainInfo="domainInfo"
        />
      </div>
      <div class="newDomain">
        <NewDomainCard />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  middleware: 'auth',

  data() {
    return {}
  },
  computed: {
    ...mapGetters({ domains: 'domains/getAllDomains' }),
    ...mapGetters(['isAuthenticated']),
  },
  methods: {
    ...mapActions({
      getDomainsFromBackend: 'domains/getDomainsFromBackend',
    }),
  },
  async fetch() {
    let storedDomains = this.$store.getters['domains/getAllDomains']
    if (storedDomains.length == 0) {
      console.log('Getting from BAckend')
      await this.getDomainsFromBackend()
    }
  },
  fetchOnServer: false,
}
</script>

<style lang="sass" scoped>
.domains
  margin-top: 100px
  .content
    @include flexify-row
    flex-wrap: wrap
    justify-content: space-evenly

  .newDomain
    @include flexify-row
</style>
