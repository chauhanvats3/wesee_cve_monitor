<template>
  <div class="breadcrumbs">
    <NuxtLink to="/">Home</NuxtLink> /
    <NuxtLink to="/domains">Domains</NuxtLink> /
    <NuxtLink to="/dashboard">Dashboard</NuxtLink> /
    <NuxtLink to="/user">User</NuxtLink>
  </div>
</template>

<script>
export default {}
</script>

<style lang="sass" scoped>
.breadcrumbs
  margin-top: calc(80px + 2vh)
  margin-left: 40px
  margin-bottom: 40px
  color: #666

  a
    text-decoration: none
    color: #aaa

  a:hover
    color: #555
</style>
