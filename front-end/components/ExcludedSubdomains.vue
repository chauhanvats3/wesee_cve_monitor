<template>
  <div class="excluded">
    <h5 class="heading">Excluded Subdomains</h5>
    <div class="list">
      <div
        class="subdomain"
        v-for="(subdomain, index) in getSubdomains(domain)"
        :key="index"
      >
        <div class="wrapper" v-if="!subdomain.include">
          <div class="top-bar">
            <p class="name">{{ subdomain.name }}</p>

            <img
              src="~static/bin.svg"
              alt="Restore"
              class="include"
              @click.stop="toggleExclusion(subdomain.name)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'

export default {
  props: ['domain'],
  computed: {
    ...mapGetters('domains', ['getSubdomains']),
  },
  methods: {
    ...mapMutations({ excludeToggle: 'domains/excludeToggle' }),
    toggleExclusion(subdomain) {
      let info = {
        domain: this.domain,
        subdomain,
      }
      this.excludeToggle(info)
    },
  },
}
</script>

<style lang="sass" scoped>
.excluded
    width: 100%
    background: #DADADA
    border-radius: 25px 25px 0px 0px
    @include flexify-col
    padding: 5vh 5vw 10vh 5vw
    .heading
        margin: 40px 10px

    .list
        width: 100%
        @include flexify-row
        flex-flow: wrap
        justify-content: flex-start
        .subdomain
            .wrapper
                margin: 10px 2vw
                padding: 10px 30px
                background: #F4F4F4
                border-radius: 10px

                .top-bar
                    @include flexify-row
                    .name
                        font-weight: 400
                        letter-spacing: 0.11em
                        font-weight: 400
                    .include
                        padding: 5px 20px
                        padding-right: 0
                        cursor: pointer
                        height: 48px
</style>
