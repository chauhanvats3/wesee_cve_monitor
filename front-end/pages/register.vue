<script>
import { mapActions } from 'vuex'

export default {
  auth: false,
  data() {
    return {
      userData: {
        first_name: '',
        last_name: '',
        password: '',
        password2: '',
        username: '',
        email: '',
      },
      validity: {
        name: false,
        password: false,
        password2: false,
        username: false,
        email: false,
      },
      disableButton: false,
    }
  },
  computed: {
    dataValid() {
      let { name, password, password2, username, email } = this.validity
      if (name && password && password2 && username && email) return true
      return false
    },
  },
  methods: {
    ...mapActions(['registerUserOnBackend']),
    async registerUser() {
      if (this.disableButton || !this.dataValid) return

      try {
        console.log(this.userData)
        for (property in this.userData) {
          property = property.trim()
        }
        let res = await this.registerUserOnBackend(this.userData)
        console.log(res)
        if (res.status == 201) {
          this.$refs.toast.classList.add('show')

          setTimeout(() => {
            this.$refs.toast.classList.remove('show')
            this.$router.push('/')
          }, 2000)
        }
      } catch (err) {
        console.error(err)
        this.$refs.btnRegister.classList.add('error')
        this.$refs.btnRegister.innerHTML = 'Failed!'
        this.disableButton = true
        setTimeout(() => {
          this.$refs.btnRegister.classList.remove('error')
          this.$refs.btnRegister.innerHTML = 'Register'
          this.disableButton = false
        }, 3000)
      }
    },
  },
  watch: {
    'userData.first_name'(newVal) {
      if (newVal == '') {
        this.$refs.nameErr.innerHTML = ''
        this.validity.name = false
      } else if (newVal.trim() == '') {
        this.$refs.nameErr.innerHTML =
          'First Name Cannot Be Blank'.toLowerCase()
        this.validity.name = false
      } else {
        this.$refs.nameErr.innerHTML = ''
        this.validity.name = true
      }
    },
    'userData.email'(newVal) {
      let emailRegEx =
        /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

      let isValid = newVal.trim().match(emailRegEx)

      if (newVal == '') {
        this.$refs.emailErr.innerHTML = ''.toLowerCase()
        this.validity.email = false
      } else if (newVal.trim() == '') {
        this.$refs.emailErr.innerHTML = 'Email Cannot Be Blank'.toLowerCase()
        this.validity.email = false
      } else if (!isValid) {
        this.$refs.emailErr.innerHTML = 'Email is not Valid'.toLowerCase()
        this.validity.email = false
      } else {
        this.$refs.emailErr.innerHTML = ''
        this.validity.email = true
      }
    },
    'userData.password'(newVal) {
      let passRegEx =
        /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/
      let isValid = newVal.trim().match(passRegEx)

      if (newVal == '') {
        this.$refs.passErr.innerHTML = ''
        this.validity.password = false
      } else if (newVal.trim() == '') {
        this.$refs.passErr.innerHTML = 'password cannot be blank'
        this.validity.password = false
      } else if (newVal.trim().length < 8) {
        this.$refs.passErr.innerHTML =
          'password must be at least 8 characters long'
        this.validity.password = false
      } else if (!isValid) {
        this.$refs.passErr.innerHTML =
          '<strong>Password Requirement : </strong> number, special character, upper & lower case letters.'
        this.validity.password = false
      } else {
        this.$refs.passErr.innerHTML = ''
        this.validity.password = true
      }
    },
    'userData.password2'(newVal) {
      if (newVal == '') {
        this.$refs.passErr.innerHTML = ''
        this.validity.password2 = false
      } else if (newVal.trim() == '') {
        this.$refs.passErr.innerHTML = 'password cannot be blank'
        this.validity.password2 = false
      } else if (newVal.trim() != this.userData.password.trim()) {
        this.$refs.passErr.innerHTML = "passwords don't match"
        this.validity.password2 = false
      } else {
        this.$refs.passErr.innerHTML = ''
        this.validity.password2 = true
      }
    },
    'userData.username'(newVal) {
      if (newVal == '') {
        this.$refs.usernameErr.innerHTML = ''
        this.validity.username = false
      } else if (newVal.trim() == '') {
        this.$refs.usernameErr.innerHTML = 'username cannot be blank'
        this.validity.username = false
      } else {
        this.$refs.usernameErr.innerHTML = ''
        this.validity.username = true
      }
    },
  },
}
</script>

<template>
  <div class="register">
    <h1>Register Your Account</h1>
    <form @submit.prevent="registerUser" class="registeration-form">
      <div class="wrap">
        <div class="name">
          <input
            name="given-name"
            type="text"
            placeholder="First Name"
            v-model="userData.first_name"
          />
          <input
            name="family-name"
            type="text"
            placeholder="Last Name"
            v-model="userData.last_name"
          />
        </div>
        <div class="err">
          <p ref="nameErr"></p>
        </div>
      </div>
      <div class="wrap">
        <input
          type="text"
          name="email"
          id="email"
          class="email"
          placeholder="Email Address"
          v-model="userData.email"
        />
        <div class="err">
          <p ref="emailErr"></p>
        </div>
      </div>
      <div class="wrap">
        <div class="password">
          <input
            type="password"
            name="new-password"
            id="new-password"
            placeholder="Password"
            v-model="userData.password"
          />
          <input
            type="password"
            id="reenter-password"
            placeholder="Re-Enter Password"
            v-model="userData.password2"
          />
        </div>
        <div class="err">
          <p ref="passErr"></p>
        </div>
      </div>
      <div class="wrap">
        <div class="bottom-row">
          <input
            type="text"
            name="username"
            id="username"
            placeholder="username"
            v-model="userData.username"
          />
          <button ref="btnRegister" v-bind:class="{ invalid: !dataValid }">
            Register
          </button>
        </div>
        <div class="err">
          <p ref="usernameErr"></p>
        </div>
      </div>
    </form>
    <div class="toast" ref="toast">
      <p>Registeration Succesful. Redirecting To Login!</p>
    </div>
  </div>
</template>

<style lang="sass" scoped>
.register
    padding-top: calc(80px + 5vh)
    padding-left: 20px
    @include flexify-col
    width: 100%
    height:100%
    align-items: flex-start
    position: relative


    .registeration-form
        @include flexify-col
        align-items: flex-start
        align-self: center
        max-width: 65ch
        margin: 50px 20px

        .wrap
            @include flexify-col
            width: 100%
            .email,.name,.password,.bottom-row
                @include flexify-row
                justify-content: space-between
                width: 100%
            .err
                width: 100%
                min-height: 0.7rem
                padding: 0 20px
                margin: 0
                p
                    font-size: 0.7rem
                    color: $red

        .name,.password,.bottom-row
            gap: 30px

        input[type="text"],input[type="password"]
            padding: 10px 15px
            border-radius: 10px
            outline: none
            border: 1px solid $black
            transition: all 0.4s ease
            margin: 20px 0px 5px 0
            flex-grow: 1

            &:focus,&:active
                box-shadow: 0 1px 1px rgba(0,0,0,0.11),0 2px 2px rgba(0,0,0,0.11),0 4px 4px rgba(0,0,0,0.11),0 6px 8px rgba(0,0,0,0.11),0 8px 16px rgba(0,0,0,0.11)
                transform: scale(1.1)
                border: 1px solid $main-color

        button
            border: none
            background: $main-color
            border-radius: 10px
            padding: 10px 20px
            margin: 20px 0px 5px 0
            color: white
            flex-grow: 1
            cursor : pointer
            transition: all 0.2s linear
            &:hover,&:active,&:focus
                outline: none
            &.error
                background: $red

            &.invalid
                cursor: default
                background: gray

    .toast
        position: fixed
        bottom: -15%
        width: 100%
        height: max-content
        @include flexify
        transition: all 0.6s ease-in-out
        p
            background: $main-color
            color: white
            border-radius: 10px
            padding: 10px 40px
        &.show
            bottom: 10%
</style>
