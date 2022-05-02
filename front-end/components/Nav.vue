<template>
  <div class="navbar" v-bind:class="{ spacedbetween: $route.name != 'index' }">
    <div class="logo">
      <NuxtLink to="/"><img src="~static/logo.svg" alt="" /></NuxtLink>
    </div>

    <div class="menu" v-if="$route.name != 'index'">
      <NuxtLink to="/domains">Domains</NuxtLink>
      <NuxtLink to="/dashboard">Dashboard</NuxtLink>
      <NuxtLink to="/user">User</NuxtLink>
    </div>
  </div>
</template>

<script>
export default {}
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

    .logo
      height: 50px

    .menu
      a
        color: white
        text-decoration: none
        margin: 10px 25px
        letter-spacing: 2px

      .nuxt-link-active
        color: $main-color

.spacedbetween
        justify-content: space-between
</style>
