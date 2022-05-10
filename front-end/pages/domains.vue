<template>
  <div class="domains">
    <Nav />
    <Breadcrumb />
    <div class="content">
      <DomainCard
        v-for="(domainInfo, index) in domains"
        :key="index"
        :domain="domainInfo.name"
        :verified="domainInfo.verified"
      />
    </div>
    <div class="newDomain">
      <NewDomainCard />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      isAuthenticated: this.$store.state.user.isAuthenticated,
    }
  } /* 
  async fetch() {
    let status = await this.$store.dispatch('domains/getDomainsFromBackend')
    console.log('status domains : ' + status)
    if (status != 200) this.$router.push('/')
  }, */,
  async asyncData(context) {
    let status = await context.store.dispatch('domains/getDomainsFromBackend')
    if (status != 200) {
      context.app.router.push('/')
    }
  },
  mounted() {},
  computed: {
    ...mapGetters({ domains: 'domains/getAllDomains' }),
  },
}
</script>

<style lang="sass" scoped>
.domains

  .content
    @include flexify-row
    flex-wrap: wrap
    justify-content: space-evenly

  .newDomain
    @include flexify-row
</style>
