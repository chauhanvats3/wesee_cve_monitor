<template>
  <div class="dashboard">
    <Nav />
    <div class="domains">
      <h1>All Domains :</h1>
      <ul>
        <li v-for="(domain, index) in domains" :key="index">
          <NuxtLink :to="'/dashboard/' + domain.name" v-if="domain.verified">
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
  data() {
    return {
      isAuthenticated: this.$store.state.user.isAuthenticated,
    }
  },
  computed: {
    ...mapGetters({ domains: 'domains/getAllDomains' }),
  },
  mounted() {
    if (!this.isAuthenticated) this.$router.push('/')
  },
  async asyncData(context) {
    if (!context.store.state.user.isAuthenticated) {
      context.app.router.push('/')
      return 401
    }
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
