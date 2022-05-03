<template>
  <div class="domains">
    <Nav />
    <Breadcrumb />
    <div class="content">
      <DomainCard
        v-for="(domainInfo, index) in allDomains"
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
import DomainCard from '../components/DomainCard.vue'
import NewDomainCard from '~/components/NewDomainCard.vue'
export default {
  components: { DomainCard, NewDomainCard, DomainCard },
  computed: {
    allDomains: function () {
      return this.$store.getters.getAllDomains
    },
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
