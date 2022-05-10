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
import { mapActions } from 'vuex'

export default {
  data() {
    return {
      domains: [],
    }
  },
  mounted() {
    this.getDomains().then((data) => {
      this.domains = data
      console.log(data)
    })
  },
  methods: {
    ...mapActions({ getDomains: 'dashboard/getDomainsFromBackend' }),
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
