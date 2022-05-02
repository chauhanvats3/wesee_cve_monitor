<template>
  <div class="domain-card">
    <div class="overlay" v-bind:class="{ verified: verified == 'true' }">
      <div class="top-row">
        <div class="domain">
          <p>{{ domain }}</p>
        </div>
        <div class="verify-btn" v-if="verified == 'false'">
          <p>how to verify?</p>
        </div>
      </div>

      <div class="content" v-if="verified == 'true'">
        <p>Number Of Subdomains : 5</p>
        <p>No Of Techs : 55</p>
        <p>No Of CVEs : 555</p>
      </div>

      <div class="cta">
        <div class="btn verified">Verified</div>
        <div class="btn dashboard">
          <NuxtLink to="/dashboard">Dashboard</NuxtLink>
        </div>
        <div class="btn delete">Delete</div>
      </div>
    </div>

    <div class="verify-overlay" v-if="verified == 'false'"></div>
  </div>
</template>

<script>
export default {
  props: ['domain', 'verified'],
}
</script>

<style lang="sass" scoped>
$top-row-height : 50px

.domain-card
    width: 550px
    height: 300px
    background: url(https://picsum.photos/550/300) no-repeat
    border-radius: 15px
    margin: 20px
    position: relative
    overflow: hidden

    .overlay
        position: absolute
        width: 100%
        height: 100%
        background: rgb(52 52 52 / 29%)
        top: calc(100% - $top-row-height)
        border-radius: 15px
        transition: all 0.6s ease-in-out
        backdrop-filter: blur(5px)
        color: white
        @include flexify-col
        justify-content: space-between
        flex-wrap: nowrap

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
                background: $red
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
            justify-content: space-around
            width: 100%
            .btn
                background: blue
                border-radius: 7px
                padding: 10px 20px
                margin-bottom: 15px

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



    &:hover .overlay.verified
        top: 0
</style>
