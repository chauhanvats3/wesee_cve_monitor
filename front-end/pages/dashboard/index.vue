<template>
  <div class="dashboard">
    <Nav />
    <div class="domains">
      <h1>All Domains :</h1>
      <ul>
        <li v-for="(domain, index) in domains" :key="index">
          <NuxtLink :to="'/dashboard/' + domain.name">
            {{ domain.name }}
          </NuxtLink>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters({ domains: 'domains/getAllDomains' }),
  },
  mounted() {},
  methods: {},
  async asyncData(context) {
    let status = await context.store.dispatch('domains/getDomainsFromBackend')
    if (status != 200) {
      context.app.router.push('/')
    }
  },
}
</script>

<style lang="sass" scoped>
.dashboard
  @include flexify-col
  justify-content: flex-start
  width: 100%
  height: 100vh
  padding-top: calc( 80px + 5vh )

  .domains
    width: 100%
    height: 100%
    padding: 0 20px
    ul
      margin: 50px 20px
      li
        margin: 20px

        a
          width: 100%
          font-size: 1.5rem
          font-weight: lighter
        &:hover a
          color: $main-color
</style>
