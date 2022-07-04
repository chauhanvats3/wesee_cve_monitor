<template>
  <div style="display: flex; flex-flow: column nowrap; align-items: center">
    <div class="login-box">
      <input
        type="text"
        class="txtbox"
        id="user"
        name="username"
        placeholder="username"
        v-model.trim="username"
      />

      <input
        type="password"
        class="txtbox"
        id="pass"
        placeholder="password"
        name="current-password"
        v-model.trim="password"
        @keypress.enter="login"
      />
      <div class="bottom-row">
        <NuxtLink to="/register">
          <p class="btn register">Register?</p>
        </NuxtLink>
        <div class="button" @click="login">
          <p class="btn login">Login</p>
        </div>
      </div>
    </div>

    <div class="error" ref="errorToast">
      <p>{{ this.error }}</p>
    </div>
  </div>
</template>

<script>
import { mapActions, mapMutations } from 'vuex'

export default {
  data() {
    return {
      username: '',
      password: '',
      error: 'Some Error',
    }
  },
  methods: {
    ...mapMutations({ resetData: 'domains/resetStore' }),

    async login() {
      this.resetData()
      try {
        let response = await this.$auth.loginWith('local', {
          data: {
            username: this.username,
            password: this.password,
          },
        })
      } catch (e) {
        this.error = e

        if (e.toString().indexOf('status code 401') != -1)
          this.error = 'Username/Password Invalid!'

        this.$refs.errorToast.classList.add('show')
        setTimeout(() => {
          this.$refs.errorToast.classList.remove('show')
        }, 3000)

        console.log(e.toString())
      }
    },
  },
}
</script>

<style lang="sass" scoped>
.error
  @include flexify
  position: fixed
  bottom: -100%
  background: $red
  color: white
  font-size: 0.8rem
  width: max-content
  height: max-content
  padding: 20px 30px
  border-radius: 10px
  transition: all 0.4s ease-in-out

.error.show
  bottom:10px

.login-box
    @include flexify-col
    align-items: flex-start
    margin: 20px
    padding: 20px
    background: rgba(216, 216, 216, 0.5)
    backdrop-filter: blur(10px)
    border-radius: 15px
    position: relative
    z-index: 1

    .bottom-row
      @include flexify-row
      width: 100%
      justify-content: space-between

      .btn
          font-size: 0.75rem
          margin: 10px 0 0 5px
          padding: 10px 20px
          color: $black
          border-radius: 3px
          background: rgb(255 255 255 / 9%)
          backdrop-filter: blur(4px)
          transition: all 0.4s ease
          &:hover
            color: $main-color

      .login
          background: $main-color
          color: white
          cursor: pointer
          &:hover
            color:$black
    .txtbox
        margin: 10px 0px
        border: none
        border-radius: 10px
        font-size: 1.2rem
        padding: 15px
        width: 100%
        position: relative



    @media screen and (min-width: $medium) and (max-width: $large)
        .txtbox
            font-size: 1rem

        .button
            font-size: 1rem

    @media screen and (min-width: $small) and (max-width: $medium)
        .txtbox
            font-size: 0.75rem

        .button
            font-size: 0.75rem

    @media screen and (max-width: $small)
        .txtbox
            font-size: 0.50rem
            padding: 10px
            margin: 10px 0
        .button
            font-size: 0.5rem
            margin-top: 10px
</style>
