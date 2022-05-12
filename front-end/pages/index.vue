<template>
  <div class="index">
    <Nav />
    <div class="bg"></div>
    <div class="intro">
      <h1 class="main">Why This Tool Is Useful To You!</h1>
      <p class="sub">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin orci.
      </p>
    </div>
    <div class="graphic">
      <img src="~static/home_graphic_1.svg" alt="Home Graphic" />
    </div>
    <div class="login-wrap">
      <div class="login">
        <Login />
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Home',
  data() {
    return {
      isAuthenticated: this.$store.state.user.isAuthenticated,
    }
  } /*
  async fetch() {
    let status = await this.$store.dispatch('domains/getDomainsFromBackend')
    if (status == 200) {
      this.$router.push('/domains')
    }
  }, */,
  async asyncData(context) {
    if (!context.store.state.user.isAuthenticated) {
      context.store.dispatch('destroyTokens')
      return 401
    }
    let status = await context.store.dispatch('getPing')
    if (status == 200) {
      context.app.router.push('/domains')
    }
  },
  mounted() {
    if (!this.isAuthenticated) this.$router.push('/')
  },
}
</script>

<style lang="sass" scoped>
.index
  @include flexify-col
  width: 100vw
  height: 100vh
  position: relative
  flex-wrap: nowrap
  padding-top: calc(80px + 5vh)

  .bg
    position: absolute
    top: 0
    left: 0
    width: 100%
    height: 95vh
    background: url('../static/home_bg.svg') no-repeat
    background-size: cover
    background-position-y: bottom
    background-position-x: center
    z-index: -2

  .intro
    align-self: flex-start
    margin: 20px 50px
    color: white

    .main
      font-weight: bold

    .sub
      font-size: 1.5rem
      max-width: 70%

  .graphic
    @include flexify
    justify-content: flex-end
    align-self: flex-end
    margin: 0 40px
    margin-top: -100px
    img
      width: max-content
      height: max-content
      align-self: flex-end
      width: 50vw
      max-width: 750px

  .login-wrap
    margin-bottom: 30px
    max-width: 90vw
    align-self: flex-start
    position: relative
    width: 100%
    height: 100px
    margin: 50px
    .login
      position: absolute
      width: max-content
      bottom: -30px
      left: 30px


@media screen and (min-width: $medium) and (max-width: $large)
  .index
    .intro
        .main
          font-size: 200%

        .sub
          font-size: 100%
          width: 60%

    .graphic
      margin: 0 40px
      width: 100%

      img
        width: 70%
        max-width: 500px

    .login-wrap
      .login


@media screen and (min-width: $small) and (max-width: $medium)
  .index
    .intro
        .main
          font-size: 200%

        .sub
          font-size: 100%
          width: 60%

    .graphic
      margin: 0 40px
      width: 100%

      img
        width: 50%

    .login-wrap

      .login
        left: -30px

@media screen and (max-width: $small)
  .index
    .intro
      .main
        font-size: 130%

      .sub
        font-size: 75%

    .graphic
      align-self: center
      justify-content: center
      margin: 40px 0
      width: 70%

      img
        width: 90%

    .login-wrap
      display: flex
      height: max-content
      width: 100%
      margin: 30px 0
      max-width: 100%
      justify-content: center

      .login
        position: relative
        width: max-content
        bottom:0
        left: 0
        width: 70%
</style>
