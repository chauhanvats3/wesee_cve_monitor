<template>
  <div class="domains">
    <Nav />
    <div v-if="$fetchState.pending">
      <Fetching />
    </div>
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
    console.log(storedDomains)
    if (storedDomains.length == 0) {
      await this.getDomainsFromBackend()
    }
  },
  fetchOnServer: false,
}
</script>

<style lang="sass" scoped>
.domains
  margin-top: 100px
  .fetching
    @include flexify-row
    width: 100vw
    height: 100vh
    svg
      width: 50px
      height: 50px
      margin: 10px 30px
  .content
    @include flexify-row
    flex-wrap: wrap !important
    justify-content: space-evenly !important

  .newDomain
    @include flexify-row
</style>
