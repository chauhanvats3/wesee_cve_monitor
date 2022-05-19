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
              get techs
            </p>
            <p class="exclude" @click.stop="toggleExclusion(subdomain.name)">
              exclude
            </p>
          </div>
        </div>
        <div class="techs">
          <TechPill
            v-for="(tech, index2) in subdomain.techs"
            :key="index2"
            :tech="tech"
            v-on:pill-clicked="
              subPillClicked({ subdomain: subdomain.name, tech: tech })
            "
          />
        </div>
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
    ...mapActions({ getTechs: 'domains/getTechs' }),
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
                margin: 5px 10px

              .getTech
                  color: $main-color

              .exclude
                  color: $red
        .techs
            @include flexify-row
            flex-wrap: wrap
</style>
