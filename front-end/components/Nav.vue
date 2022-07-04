<template>
  <div
    class="navbar"
    v-bind:class="{
      spacedbetween: $route.name != 'index' && $route.name != 'register',
    }"
  >
    <div class="logo">
      <NuxtLink to="/"><img src="~static/logo.svg" alt="" /></NuxtLink>
    </div>

    <div
      class="menu"
      v-if="$route.name != 'index' && $route.name != 'register'"
    >
      <NuxtLink to="/domains">Domains</NuxtLink>
      <NuxtLink to="/dashboard">Dashboard</NuxtLink>
      <a style="cursor: pointer" @click="logout"
        >Logout <span>({{ $auth.user.username }})</span>
      </a>
    </div>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  methods: {
    ...mapMutations({ resetData: 'domains/resetStore' }),
    async logout() {
      this.resetData()
      await this.$auth.logout()
    },
  },
}
</script>

<style lang="sass" scoped>
.navbar
    background-color: $black
    padding: 10px
    position: fixed
    top: 0
    left: 0
    width: 100%
    @include flexify-row
    z-index: 10
    box-shadow: 0 1px 1px rgba(0,0,0,0.11),0 2px 2px rgba(0,0,0,0.11),0 4px 4px rgba(0,0,0,0.11),0 8px 8px rgba(0,0,0,0.11),0 16px 16px rgba(0,0,0,0.11),0 32px 32px rgba(0,0,0,0.11)
    transition: all 0.3s ease

    .logo
      height: 50px
      transition: all 0.4s ease

    .menu
      transition: all 0.4s ease
      a
        color: white
        text-decoration: none
        margin: 10px 25px
        letter-spacing: 2px
        position: relative
        font-size: 0.9rem
        span
          position: absolute
          bottom: -40%
          right: 0
          font-size: 0.4rem

      .nuxt-link-active
        color: $main-color

.spacedbetween
        justify-content: space-between
</style>
