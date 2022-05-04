<template>
  <div class="tech-pill">
    <p :style="{ background: bgColors[2], color: bgColors[0] }">
      {{ tech.name }}
    </p>
    <p :style="{ background: bgColors[1] }">{{ tech.ver }}</p>
    <p :style="{ background: bgColors[0] }">{{ tech.cves.length }}</p>
  </div>
</template>

<script>
export default {
  props: ['tech'],
  methods: {
    generatePalette() {
      let color = this.tech.color
      let rgb = this.$hexToRgb(color)
      let hsl = this.$rgbToHsl(rgb)
      let palette = []
      if (hsl[1] >= hsl[2]) {
        //If Color is Dark
        for (let i = 0; i < 3; i++)
          palette[i] = [hsl[0], hsl[1], hsl[2] + i * 15, hsl[3]]
      } else {
        //If Color is light
        for (let i = 0, j = 2; i < 3; i++, j--)
          palette[j] = [hsl[0], hsl[1], hsl[2] - i * 15, hsl[3]]
      }
      return palette
    },
  },
  computed: {
    bgColors() {
      let hslValues = this.generatePalette()
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
    p
        margin: 30px 0px
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
