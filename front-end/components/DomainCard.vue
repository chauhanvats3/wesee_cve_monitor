<template>
  <div class="domain-card">
    <div
      class="overlay"
      v-bind:class="{ verified: verified == true }"
      @mouseleave="resetDeleteClicked"
    >
      <div class="top-row">
        <div class="domain">
          <p>{{ domain }}</p>
        </div>
        <div
          class="verify-btn"
          v-if="verified == false"
          @click.stop="openVerifyInstructions"
        >
          <p>how to verify?</p>
        </div>
      </div>

      <div class="content" v-if="verified == true">
        <p>Number Of Subdomains : 5</p>
        <p>No Of Techs Found : 55</p>
        <p>No Of CVEs Discovered: 555</p>
      </div>

      <div class="cta" v-if="verified == true" ref="cta">
        <div class="btn verified">Verified</div>
        <div class="btn dashboard">
          <NuxtLink :to="'/dashboard/' + domain">Dashboard</NuxtLink>
        </div>
        <div class="btn delete" @click="deleteClicked">Delete</div>
        <p>I want to DELETE this domain</p>
      </div>
    </div>

    <div class="verify-overlay" v-if="verified == false" ref="verifyOverlay">
      <div class="close" @click.stop="closeVerifyInstructions">
        <p>X</p>
      </div>
      <div class="content">
        <p>1. Sign In to your DNS provider</p>
        <p>
          2. Copy the text record below into the DNS configuration for
          <span>{{ domain }}</span>
        </p>
        <p>3. Press “verify" after a while</p>
      </div>
      <div class="bottom-row">
        <div class="verification-code">
          <p>we-see-verification.{{ domain }}=as21db6537r2a</p>
        </div>
        <div class="btn verify-now">
          <p>verify</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['domain', 'verified'],
  data() {
    return {
      deleteDomain: false,
    }
  },
  methods: {
    openVerifyInstructions() {
      this.$refs.verifyOverlay.classList.toggle('show')
    },
    closeVerifyInstructions() {
      this.$refs.verifyOverlay.classList.toggle('show')
    },
    deleteClicked() {
      this.$refs.cta.children[0].classList.add('hide')
      this.$refs.cta.children[1].classList.add('hide')
      this.$refs.cta.children[2].innerText = 'Yes'
      this.$refs.cta.children[2].style.marginRight = '15px'
      this.$refs.cta.classList.add('deleteClicked')
      this.$refs.cta.children[3].classList.add('show')
    },
    resetDeleteClicked() {
      if (!this.$refs.cta) return

      setTimeout(() => {
        this.$refs.cta.children[0].classList.remove('hide')
        this.$refs.cta.children[1].classList.remove('hide')
        this.$refs.cta.children[2].innerText = 'Delete'
        this.$refs.cta.children[2].style.marginRight = '0px'
        this.$refs.cta.classList.remove('deleteClicked')
        this.$refs.cta.children[3].classList.remove('show')
      }, 500)
    },
  },
}
</script>

<style lang="sass" scoped>
$top-row-height : 50px

.domain-card
    width: 550px
    height: 300px
    background: url(https://picsum.photos/550/300) no-repeat
    border-radius: 15px
    margin: 50px 20px
    position: relative
    overflow: hidden
    transition: all 0.4s ease-in-out

    .overlay
        @include flexify-col
        position: absolute
        width: 100%
        height: 100%
        background: rgb(52 52 52 / 29%)
        top: calc(100% - $top-row-height)
        border-radius: 15px
        transition: all 0.6s ease-in-out
        backdrop-filter: blur(5px)
        color: white
        justify-content: space-between
        overflow-y: scroll

        &.verified
            .top-row
                justify-content: center

                p
                    letter-spacing: 2px

        .top-row
            @include flexify-row
            flex-wrap: nowrap
            justify-content: space-between
            width: 100%
            height: $top-row-height
            background: rgb(52 52 52 / 50%)
            border-top-right-radius: 15px
            border-top-left-radius: 15px


            .domain
                margin-left: 15px
                overflow-x: hidden
                max-height: $top-row-height
                padding-right: 5px

                p
                    color: white
                    font-size: 0.8rem

            .verify-btn
                background: $main-color
                border-radius: 15px
                height: $top-row-height
                @include flexify
                cursor: pointer
                flex-shrink: 0

                p
                    margin: 10px 20px
                    color: white
                    font-size: 0.6rem

        .content
            @include flexify-col
            width: 100%
            align-items: flex-start
            padding-left: 50px
            p
                font-size: 0.85rem
                margin: 10px
                letter-spacing: 1px

        .cta
            @include flexify-row
            flex-wrap: wrap
            justify-content: space-around
            width: 100%
            padding: 0 15px

            &.deleteClicked
              justify-content: flex-start
            p
              display: none
              margin-bottom: 15px
              transition: all 0.4s ease-in-out
            p.show
              display: flex
            .btn
                background: blue
                border-radius: 7px
                padding: 10px 20px
                margin-bottom: 15px
                transition: all 0.2s ease-in

                &.verified
                    background: #00A7A726
                    color: $main-color
                &.dashboard
                    background: #00A7A7D9
                    a
                        width: 100%
                        height: 100%
                        color: white
                &.delete
                    background: #C80000CC
                    cursor: pointer

                &.delete:hover,&.dashboard:hover
                  box-shadow: 0 1px 1px rgba(0,0,0,0.11), 0 2px 2px rgba(0,0,0,0.11), 0 4px 4px rgba(0,0,0,0.11), 0 6px 8px rgba(0,0,0,0.11),0 8px 16px rgba(0,0,0,0.11)

                &.hide
                  opacity: 0
                  position: absolute
                  right: 200%


    .verify-overlay
        @include flexify-col
        width: 100%
        height: 100%
        border-radius: 15px
        background: #c4c4c4
        position: absolute
        top: 100%
        justify-content: space-between
        padding: 20px
        transition: all 0.4s ease-in-out
        opacity: 0
        overflow-y: scroll

        &.show
          top: 0%
          opacity: 1

        .close
          position: absolute
          top: 0
          right: 0
          background: rgba(37, 37, 37)
          color: $main-color
          padding: 5px 10px
          margin: 5px
          border-radius: 10px
          cursor: pointer

        .content
            p
                margin: 15px
                font-size: 0.85rem
                line-height: 1.2rem
            span
                font-weight: bold
        .bottom-row
            @include flexify-row
            justify-content: space-evenly
            width: 100%
            .verification-code
              max-width: 80%
              height: 100%
              overflow-x: scroll
              font-size: 0.75rem
              background: white
              border-radius: 10px
              padding: 10px
              @include flexify
              justify-content: flex-start
              p
                white-space: nowrap


            .btn
              font-size: 0.8rem
              background: $main-color
              color: white
              padding: 15px
              margin-left: 15px
              border-radius: 10px
              cursor: pointer


    &:hover .overlay.verified
        top: 0

    &:hover
      box-shadow: 0 1px 1px rgba(0,0,0,0.11), 0 2px 2px rgba(0,0,0,0.11), 0 4px 4px rgba(0,0,0,0.11), 0 8px 8px rgba(0,0,0,0.11), 0 16px 16px rgba(0,0,0,0.11), 0 32px 32px rgba(0,0,0,0.11)
</style>
