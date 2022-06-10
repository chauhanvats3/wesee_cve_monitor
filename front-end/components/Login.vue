<template>
  <div style="display: flex; flex-flow: column nowrap; align-items: center">
    <div class="login-box">
      <input
        type="text"
        class="txtbox"
        id="user"
        placeholder="username"
        v-model.trim="username"
      />

      <div class="pass-row">
        <input
          type="password"
          class="txtbox"
          id="pass"
          placeholder="password"
          v-model.trim="password"
          @keypress.enter="login"
        />
        <button class="button" @click="login">
          <svg
            clip-rule="evenodd"
            fill-rule="evenodd"
            stroke-linejoin="round"
            stroke-miterlimit="2"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
            width="70px"
            height="70px"
          >
            <path
              d="m10.211 7.155c-.141-.108-.3-.157-.456-.157-.389 0-.755.306-.755.749v8.501c0 .445.367.75.755.75.157 0 .316-.05.457-.159 1.554-1.203 4.199-3.252 5.498-4.258.184-.142.29-.36.29-.592 0-.23-.107-.449-.291-.591-1.299-1.002-3.945-3.044-5.498-4.243z"
              fill="white"
            />
          </svg>
        </button>
      </div>
    </div>

    <div v-if="incorrectAuth" class="error"><p>Wrong Credentials</p></div>
  </div>
</template>

<script>
import { mapActions, mapMutations } from 'vuex'

export default {
  data() {
    return {
      username: '',
      password: '',
      incorrectAuth: false,
      error: '',
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
        this.incorrectAuth = true
        this.error = e
      }
    },
  },
}
</script>

<style lang="sass" scoped>
.error
  @include flexify
  position: absolute
  z-index: -1
  background: $red
  color: white
  font-size: 0.8rem
  width: calc(100% - 40px)
  padding: 40px 20px 20px 20px
  bottom: -40px
  border-radius: 10px
  transition: all 0.3s ease

.login-box
    @include flexify-col
    margin: 20px
    padding: 20px
    background: rgba(216, 216, 216, 0.5)
    backdrop-filter: blur(10px)
    border-radius: 15px
    position: relative
    z-index: 1

    .pass-row
      @include flexify-row
      position: relative
    .txtbox
        margin: 10px 0px
        border: none
        border-radius: 10px
        font-size: 1.2rem
        padding: 15px
        width: 100%
        position: relative

    .button
        @include flexify
        border-radius: 10px
        border: none
        background: #00A7A7
        cursor: pointer
        color: white
        position: absolute
        right: 0
        top: 0
        width: 80px
        margin: 10px 0px
        height: calc(100% - 20px)

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
