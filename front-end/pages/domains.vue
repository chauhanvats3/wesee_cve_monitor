<template>
  <div class="domains">
    <Nav />
    <div class="content">
      {{ isAuthenticated }}
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
</template>

<script>
import { mapGetters, mapState } from 'vuex'

export default {
  middleware: 'auth',

  data() {
    return {}
  },
  computed: {
    ...mapGetters({ domains: 'domains/getAllDomains' }),
    ...mapGetters(['isAuthenticated']),
  },
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
