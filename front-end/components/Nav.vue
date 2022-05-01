<template>
  <div class="navbar">
    <div class="logo">
      <img src="~static/logo.svg" alt="" />
    </div>
    <div class="menu"></div>
  </div>
</template>

<script>
export default {}
</script>

<style lang="sass" scoped>
.navbar
    background-color: #252525
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
</style>
