<template>
  <div class="tech-pill" @click="$emit('pill-clicked', tech)">
    <p :style="{ background: bgColors[2], color: bgColors[0] }">
      {{ tech.name }}
    </p>
    <p :style="{ background: bgColors[1] }">{{ tech.version }}</p>
    <p :style="{ background: bgColors[0], color: bgColors[2] }">
      {{ tech.cves.length }}
    </p>
  </div>
</template>

<script>
export default {
  props: ['tech'],
  methods: {
    pillClicked() {
      alert(this.tech.name)
    },
  },
  computed: {
    bgColors() {
      let color = this.tech.color
      let hslValues = this.$generatePalette(color)
      let bg = []
      for (let i = 0; i < hslValues.length; i++) {
        bg[
          i
        ] = `hsl(${hslValues[i][0]}deg, ${hslValues[i][1]}%,${hslValues[i][2]}%, ${hslValues[i][3]})`
      }
      return bg
    },
  },
}
</script>

<style lang="sass" scoped>
.tech-pill
    @include flexify-row
    margin: 0 10px
    cursor: pointer
    p
        margin: 20px 0px
        color: white
        padding: 10px 40px 10px 20px
        border-radius: 10px
    p:nth-child(1)
        margin-right: -20px
    p:nth-child(2)
        margin-right: -20px
    p:nth-child(3)
        padding-right: 20px
</style>
