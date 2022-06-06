<template>
  <div class="subdomains">
    <div
      class="subdomain"
      v-for="(subdomain, index) in getSubdomains(domain)"
      :key="index"
    >
      <div class="wrapper" v-if="subdomain.include">
        <div class="top-bar">
          <h3>{{ subdomain.name }}</h3>
          <div class="options">
            <p class="getTech" @click.stop="getSubdomainTechs(subdomain.id)">
              refresh
            </p>
            <p class="exclude" @click.stop="toggleExclusion(subdomain.name)">
              exclude
            </p>
          </div>
        </div>
        <div class="techs" v-if="subdomain.techs.length > 0">
          <TechPill
            v-for="(tech, index2) in subdomain.techs"
            :key="index2"
            :tech="tech"
            v-on:pill-clicked="
              subPillClicked({ subdomain: subdomain.name, tech: tech })
            "
          />
        </div>
        <div v-else class="tech_not_found"><p>No Technologies Found</p></div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'

export default {
  props: ['domain'],

  computed: {
    ...mapGetters('domains', ['getSubdomains']),
  },
  methods: {
    ...mapMutations({ excludeToggle: 'domains/excludeToggle' }),
    ...mapActions({ getTechs: 'domains/getSubdomainTechs' }),
    subPillClicked(info) {
      this.$emit('sub-pill-clicked', info)
    },
    toggleExclusion(subdomain) {
      let info = {
        domain: this.domain,
        subdomain,
      }
      this.excludeToggle(info)
    },
    getSubdomainTechs(id) {
      this.getTechs(id)
    },
  },
}
</script>

<style lang="sass" scoped>
.subdomains
    margin: 15vh 10px
    .subdomain
        margin: 10vh 10px
        .top-bar
            @include flexify-row
            justify-content: space-between
            .options
              @include flexify-row
              .getTech,.exclude
                font-size: 0.75rem
                cursor: pointer
                margin: 5px 15px

              .getTech
                  color: $main-color

              .exclude
                  color: $red
        .techs
            @include flexify-row
            flex-wrap: wrap
            margin-top: 40px
        .tech_not_found
            @include flexify
            margin-top: 90px
            text-transform: uppercase
            font-size: 2rem
            color: #aaa
            letter-spacing: 0.3rem
            word-spacing: 1rem
</style>
