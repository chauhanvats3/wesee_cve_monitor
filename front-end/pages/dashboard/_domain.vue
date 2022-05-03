<template>
  <div class="dashboard-slug">
    <Nav />
  </div>
</template>

<script>
export default {
  async asyncData({ params }) {
    const domain = params.domain
    return { domain }
  },
}
</script>

<style lang="sass" scoped></style>
