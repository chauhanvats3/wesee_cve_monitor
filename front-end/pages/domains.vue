<template>
  <div class="domains">
    <Nav />
    <Breadcrumb />
    <div class="content">
      <DomainCard domain="https://vatsal.dev" verified="false" />
      <DomainCard domain="https://pwd.dev" verified="true" />
    </div>
  </div>
</template>

<script>
import DomainCard from '../components/DomainCard.vue'
export default { components: { DomainCard } }
</script>

<style lang="sass" scoped>
.domains

  .content
    @include flexify-row
    justify-content: space-evenly
</style>
