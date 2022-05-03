<template>
  <div class="newDomainCard" @click.stop="openOverlay" ref="card">
    <div class="innerlayer"></div>

    <div class="matter">
      <img src="~static/plus.svg" alt="" />
      <p>New Domain</p>
    </div>

    <div class="overlay" ref="overlay">
      <div class="close" @click.stop="closeOverlay">
        <p>X</p>
      </div>
      <input
        type="text"
        class="txtbx"
        placeholder="https://"
        ref="domainInput"
      />
      <div class="enum">
        <input type="checkbox" class="chckbx" ref="checkbox" />
        <p @click="checkBoxClick">Subdomain Enumeration</p>
      </div>
      <div class="add" @click.stop="addNewDomain">
        <p>Add Domain</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  methods: {
    ...mapMutations(['addDomain']),
    openOverlay() {
      this.$refs.overlay.classList.add('show')
    },
    closeOverlay() {
      this.$refs.overlay.classList.remove('show')
      this.$refs.domainInput.value = ''
    },
    checkBoxClick() {
      this.$refs.checkbox.checked = !this.$refs.checkbox.checked
    },
    addNewDomain() {
      this.addDomain(this.$refs.domainInput.value)
      this.$refs.domainInput.value = ''
    },
  },
}
</script>

<style lang="sass" scoped>
.newDomainCard
    @include flexify-col
    width: 550px
    height: 300px
    background: #c4c4c4
    border-radius: 15px
    margin: 50px 20px
    padding: 20px
    position: relative
    overflow: hidden
    cursor: pointer
    transition: transform 0.4s ease-in
    position: relative

    .innerlayer
        @include flexify-col
        background: #DFDFDFB2
        width: 100%
        height: 100%
        border-radius: 15px
        transition: all 0.4s ease-in-out

    &:hover .innerlayer
        transform: scale(0.9)
        box-shadow: 0 1px 2px rgba(0,0,0,0.07),0 2px 4px rgba(0,0,0,0.07),0 4px 8px rgba(0,0,0,0.07),0 8px 16px rgba(0,0,0,0.07),0 16px 32px rgba(0,0,0,0.07),0 32px 64px rgba(0,0,0,0.07)

    .matter
        @include flexify-col
        position: absolute
        height: calc(100% - 75px)
        width: calc(100% - 75px)
        img
            width: 100px
            height: 100px
            margin: 25px
        p
            letter-spacing: 3px
            color: #6D6D6D

    .overlay
        @include flexify-col
        justify-content: flex-end
        width: 100%
        height: 100%
        position: absolute
        top: 100%
        left: 0
        background: #c4c4c4
        backdrop-filter: blur(10px)
        border-radius: 15px
        z-index: 2
        cursor: default
        opacity: 0
        transition: all 0.4s ease-in-out

        .close
            position: absolute
            top: 0
            right: 0
            background: $black
            color: $main-color
            margin: 10px
            padding: 10px
            border-radius: 5px
            cursor: pointer
            font-size: 0.7rem

        .txtbx
            border: 0
            border-radius: 10px
            font-size: 1rem
            padding: 10px
            width: 85%
            margin: 20px
        .enum
            @include flexify-row
            width: 100%
            margin: 10px
            .chckbx
                margin: 5px 10px
                width: 20px
                height: 20px
            p
                font-size: 0.8rem

        .add
            background: $main-color
            color: white
            padding: 10px 20px
            border-radius: 10px
            cursor: pointer
            transition: all 0.2s ease-in-out
            margin: 30px

            &:hover
                box-shadow:  0 1px 1px rgba(0,0,0,0.15), 0 2px 2px rgba(0,0,0,0.15), 0 4px 4px rgba(0,0,0,0.15), 0 8px 8px rgba(0,0,0,0.15)

        &.show
            opacity: 1
            top: 0
</style>
