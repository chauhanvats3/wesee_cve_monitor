<template>
  <div class="domains">
    <Nav />
    <Breadcrumb />
    <div class="content">
      <DomainCard domain="https://vatsal.dev" verified="false" />
      <DomainCard domain="https://pwd.dev" verified="true" />
      <DomainCard domain="https://laura.lassan" verified="false" />
      <DomainCard domain="https://one.plus" verified="true" />
      <DomainCard domain="https://john.cena" verified="true" />
    </div>
    <div class="newDomain">
      <NewDomainCard />
    </div>
  </div>
</template>

<script>
import DomainCard from '../components/DomainCard.vue'
import NewDomainCard from '~/components/NewDomainCard.vue'
export default { components: { DomainCard, NewDomainCard } }
</script>

<style lang="sass" scoped>
.domains

  .content
    @include flexify-row
    flex-wrap: wrap
    justify-content: space-evenly

  .newDomain
    @include flexify-row
</style>
