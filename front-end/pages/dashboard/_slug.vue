<template>
  <div class="dashboard-slug">
    <Nav />
    <ul>
      <li v-for="domain in getDomainInfo(slug)" :key="domain.name">
        <h1>
          {{ domain.name }}
        </h1>

        <TechPill v-for="tech in domain.techs" :key="tech.name" :tech="tech" />
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  async asyncData({ params }) {
    const slug = params.slug
    return { slug }
  },
  computed: {
    ...mapGetters('dashboard', ['getDomainInfo']),
  },
}
</script>

<style lang="sass" scoped>
.dashboard-slug
  padding-top: 120px
</style>
